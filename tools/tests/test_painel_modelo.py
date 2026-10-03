# -*- coding: utf-8 -*-
"""O modelo do painel (painel/modelo.js) bate com a referência em Python.

O painel treina a regressão logística dentro do navegador. Se o JavaScript e
dados/analise_aula08.py divergirem, o deck cita um número que a tela do aluno
não mostra. Os testes com carteira de brinquedo rodam no CI; o teste sobre a
planilha real pula quando ela não está presente.

Também trava duas regressões encontradas ao construir o laboratório:

- a bateria lia o "1165" de CLI001165 como número inventado e reprovava
  resposta certa;
- a base curta de 24 meses gerava zero contas elegíveis e um erro sem
  explicação.

Rodar: .venv/bin/python -m pytest tools/tests/test_painel_modelo.py -q
"""

from __future__ import annotations

import http.server
import json
import socketserver
import sys
import threading
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from dados import analise_aula08 as ref  # noqa: E402


def _carteira(semente: int = 7, contas: int = 240) -> pd.DataFrame:
    """Painel mensal de brinquedo no formato da aba Dataset 1."""
    rng = np.random.default_rng(semente)
    meses = pd.period_range("2021-04", "2026-08", freq="M").astype(str)
    linhas = []
    for i in range(contas):
        inicio = int(rng.integers(0, 30))
        fim = int(rng.integers(inicio + 3, len(meses)))
        perdida = int(meses[fim] <= "2024-03")
        for m in meses[inicio:fim + 1]:
            if rng.random() < 0.45:
                linhas.append({"account_id": f"CLI{i:06d}", "periodo": m,
                               "segment": ["PUBLIC SECTOR", "SMALL MARKET"][i % 2], "country": "BR",
                               "churn_label": perdida, "receita_usd": float(rng.integers(500, 90000)),
                               "qtd_pedidos": int(rng.integers(1, 4))})
    return pd.DataFrame(linhas)


@pytest.fixture(scope="module")
def navegador():
    from playwright.sync_api import sync_playwright

    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=str(RAIZ), **k)
    servidor = socketserver.TCPServer(("127.0.0.1", 0), handler)
    porta = servidor.server_address[1]
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b, f"http://127.0.0.1:{porta}"
        b.close()
    servidor.shutdown()


def _rodar_js(navegador, linhas: list[dict], capacidade: int = 138):
    b, base = navegador
    pg = b.new_page()
    pg.goto(base + "/laboratorio/index.html")   # carrega painel/modelo.js
    r = pg.evaluate(
        "([l, c]) => { const r = KovanModelo.rodar(l, c);"
        " return {auc: r.auc, contas: r.contas, perdidas: r.perdidas, pesos: r.pesos,"
        " ids: r.fila.map(x => x.account_id), escore: r.fila.map(x => x.escore),"
        " acertos: r.acertos_fila, valor: r.valor_esperado_fila}; }",
        [linhas, capacidade])
    pg.close()
    return r


def test_javascript_e_python_concordam_na_carteira_de_brinquedo(navegador, monkeypatch):
    painel = _carteira()
    monkeypatch.setattr(ref, "CAPACIDADE", 40)
    py = ref.rodar(painel)
    js = _rodar_js(navegador, json.loads(painel.to_json(orient="records")), 40)
    assert js["contas"] == len(py["tabela"])
    assert js["auc"] == pytest.approx(py["auc"], abs=1e-9)
    assert js["ids"] == list(py["fila"].account_id)
    assert np.allclose(js["escore"], py["fila"].escore.to_numpy(), atol=1e-9)
    for c in ref.COLUNAS:
        assert js["pesos"][c] == pytest.approx(py["pesos"][c], abs=1e-7)
    assert js["acertos"] == py["acertos_fila"]


def test_a_base_curta_recebe_mensagem_que_explica(navegador):
    curta = _carteira(contas=30)
    curta = curta[curta.periodo >= "2024-04"]
    b, base = navegador
    pg = b.new_page()
    pg.goto(base + "/laboratorio/index.html")
    msg = pg.evaluate("(l) => { try { KovanModelo.rodar(l, 10); return ''; } catch (e) { return e.message; } }",
                      json.loads(curta.to_json(orient="records")))
    pg.close()
    assert "2024-04" in msg and "base longa" in msg


def test_a_conferencia_da_bateria_ignora_o_identificador_da_conta(navegador):
    """Regressão: CLI001165 virava o número 1165, ausente da fila, e a resposta
    certa era reprovada. Visto falhando antes da correção, em 03/10/2026."""
    b, base = navegador
    pg = b.new_page()
    pg.goto(base + "/laboratorio/index.html")
    ctx = {"modelo": {"contas_elegiveis": 4593}, "contas": [
        {"posicao_na_fila": 1, "account_id": "CLI001165", "receita_12m_usd": 4415489, "valor_esperado_usd": 1532326}]}
    pg.evaluate("(c) => localStorage.setItem('kovan-contexto', JSON.stringify(c))", ctx)
    pg.goto(base + "/laboratorio/bateria.html")
    certo = pg.evaluate("KovanBateria.numerosForaDaFila('A conta CLI001165 tem receita de USD 4.415.489.')")
    inventado = pg.evaluate("KovanBateria.numerosForaDaFila('A conta CLI001165 comprou USD 3.100.000 em 2025.')")
    pg.close()
    assert certo == []
    assert inventado == [3100000]


@pytest.mark.skipif(not ref.PLANILHA.exists(), reason="a base longa do case não é versionada (ADR-005)")
def test_painel_e_referencia_concordam_na_planilha_real(navegador):
    painel = ref.carregar()
    py = ref.rodar(painel)
    js = _rodar_js(navegador, json.loads(painel.to_json(orient="records")))
    assert js["auc"] == pytest.approx(py["auc"], abs=1e-9)
    assert js["ids"] == list(py["fila"].account_id)
    assert js["valor"] == pytest.approx(py["valor_esperado_fila"], rel=1e-12)
