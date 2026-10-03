# -*- coding: utf-8 -*-
"""O painel da Aula 08 lê a planilha sem trocar o número.

Regressão: a primeira versão lia "0.448" como milhar e mostrava escore 448, e
era esse valor que seguia para o agente do n8n.

Rodar: .venv/bin/python -m pytest tools/tests/test_painel.py -q
"""

from __future__ import annotations

import http.server
import socketserver
import threading
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
CSV = ("account_id,escore,valor_em_risco_usd,valor_esperado_usd\n"
       "A,0.448,4642422,2082084\n"
       'B,"0,5","1.000,5",500\n')


@pytest.fixture(scope="module")
def pagina(tmp_path_factory):
    from playwright.sync_api import sync_playwright

    arquivo = tmp_path_factory.mktemp("painel") / "fila.csv"
    arquivo.write_text(CSV, encoding="utf-8")
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=str(RAIZ), **k)
    servidor = socketserver.TCPServer(("127.0.0.1", 0), handler)
    porta = servidor.server_address[1]
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(f"http://127.0.0.1:{porta}/painel/index.html")
        pg.wait_for_function("typeof XLSX !== 'undefined'", timeout=20000)
        pg.set_input_files("#arquivo", str(arquivo))
        pg.wait_for_selector("#resumo:not([hidden])")
        yield pg
        b.close()
    servidor.shutdown()


def test_ponto_decimal_continua_decimal(pagina):
    celulas = pagina.locator("#tabela tbody tr:first-child td").all_inner_texts()
    assert celulas[1] == "0,448"


def test_formato_brasileiro_com_virgula(pagina):
    celulas = pagina.locator("#tabela tbody tr:nth-child(2) td").all_inner_texts()
    assert celulas[1] == "0,5" and celulas[2] == "1.000,5"


def test_os_indicadores_somam_a_planilha(pagina):
    assert pagina.inner_text("#k-contas") == "2"
    assert pagina.inner_text("#k-escore") == "0,474"
    assert pagina.inner_text("#k-esperado") == "2,1 mi"
