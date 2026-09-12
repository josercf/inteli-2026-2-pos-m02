# -*- coding: utf-8 -*-
"""Trava os números da Aula 07 contra o aplicativo que a turma roda.

Os valores esperados estão transcritos de forma literal. A fonte deles é o
pacote `app` do repositório de prática, importado por dados/analise_aula07.py:
o deck e o aplicativo precisam contar a mesma história, e reimplementar a conta
aqui faria os dois divergirem na primeira correção aplicada de um lado só.

A suíte pula quando o repositório de prática ou a base longa não estão
presentes, que é o caso do CI.

Rodar: PYTHONPATH=. .venv/bin/python -m pytest dados/tests/test_aula07_numeros.py -q
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

DECK = RAIZ / "aulas" / "aula07.html"
PRATICA = RAIZ.parent / "inteli-pos-2026-2a-eda"
CACHE = PRATICA / "dados" / ".cache"

pytestmark = pytest.mark.skipif(
    not (PRATICA / "app" / "churn").is_dir() or not CACHE.exists(),
    reason="o aplicativo da Aula 07 vive no repositório de prática (ADR-006)")


@pytest.fixture(scope="module")
def a():
    from dados import analise_aula07

    return analise_aula07


@pytest.fixture(scope="module")
def deck() -> str:
    return DECK.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# O que entra
# ---------------------------------------------------------------------------

def test_o_formato_da_entrada(a):
    f = a.formato()
    assert f["linhas_de_pedido"] == 492393
    assert f["contas_na_carteira"] == 7259
    assert f["contas_elegiveis"] == 4708
    assert f["perdidas"] == 2456
    assert f["colunas"] == 11
    assert f["colunas_do_gemini"] == 8
    assert f["colunas_de_erosao"] == 3


def test_o_script_exportado_tem_94_linhas(a):
    n = a.tamanho_do_script_exportado()
    if n is None:
        pytest.skip("churn_model.py não está em ~/Downloads")
    assert n == 94


def test_a_carga_com_cache_fica_abaixo_de_cinco_segundos(a):
    """O slide afirma 0,6s. A trava é frouxa de propósito, porque o número
    depende da máquina: o que não pode voltar é a ordem de grandeza de 219s.
    """
    assert a.custo_de_carga()["segundos_com_cache"] < 5.0


# ---------------------------------------------------------------------------
# O modelo
# ---------------------------------------------------------------------------

def test_a_auc_fora_da_amostra_e_08249(a):
    assert round(a.qualidade()["auc_fora_da_amostra"], 4) == 0.8249


def test_a_recencia_e_a_coluna_mais_importante(a):
    imp = a.importancia()
    assert imp.coluna.iloc[0] == "dias_desde_ultima_compra"
    assert round(float(imp.queda_de_auc.iloc[0]), 3) == 0.148


# ---------------------------------------------------------------------------
# O achado: as duas ordenações da fila
# ---------------------------------------------------------------------------

def test_o_risco_total_da_carteira_elegivel(a):
    assert round(a.risco_total()) == 36903303


def test_a_fila_por_probabilidade(a):
    linha = a.filas().loc["Por probabilidade"]
    assert int(linha.contas) == 138
    assert int(linha.acertos) == 118
    assert round(float(linha.precisao) * 100, 1) == 85.5
    assert round(float(linha.receita_alcancada)) == 2641
    assert round(float(linha.fracao_do_risco) * 100, 2) == 0.01


def test_a_fila_por_valor_esperado(a):
    linha = a.filas().loc["Por valor esperado"]
    assert int(linha.contas) == 138
    assert int(linha.acertos) == 41
    assert round(float(linha.precisao) * 100, 1) == 29.7
    assert round(float(linha.receita_alcancada)) == 25242093
    assert round(float(linha.fracao_do_risco) * 100, 1) == 68.4


def test_a_fila_mais_precisa_e_a_que_alcanca_menos_dinheiro(a):
    """O achado da aula. Se um dia isto se inverter, o deck precisa ser refeito
    inteiro: a comparação é o eixo da tarde."""
    t = a.filas()
    prob = t.loc["Por probabilidade"]
    valor = t.loc["Por valor esperado"]
    assert prob.precisao > valor.precisao * 2
    assert valor.fracao_do_risco > prob.fracao_do_risco * 1000


# ---------------------------------------------------------------------------
# O par de contas
# ---------------------------------------------------------------------------

def test_a_conta_d_sai_de_3024_para_primeiro(a):
    d = a.par_de_contas().loc["Conta D"]
    assert int(d.posicao) == 3024
    assert int(d.posicao_por_valor) == 1
    assert round(float(d.escore), 3) == 0.448
    assert round(float(d.receita_12m)) == 4642422
    assert bool(d.na_fila_por_valor) is True


def test_a_conta_e_desce_quando_o_criterio_muda(a):
    e = a.par_de_contas().loc["Conta E"]
    assert int(e.posicao) == 910
    assert int(e.posicao_por_valor) == 4085
    assert float(e.receita_12m) == 0.0
    assert bool(e.na_fila_por_valor) is False


def test_o_deck_nao_expoe_o_id_real_das_contas(a, deck):
    assert a.CONTA_D not in deck
    assert a.CONTA_E not in deck
    assert "Conta D" in deck and "Conta E" in deck


# ---------------------------------------------------------------------------
# O deck cita os mesmos números
# ---------------------------------------------------------------------------

NUMEROS_NO_DECK = [
    "492.393", "4.708", "2.456", "11", "94", "8",
    "0,8249", "36.903.303", "138", "118", "85,5%", "0,01%",
    "41", "29,7%", "25.242.093", "68,4%", "2.641",
    "0,448", "0,820", "3.024º", "910º", "4.085º", "4.642.422",
    "219", "0,6", "33,8%", "2022-06-30", "07/03/2024", "2024-12-31",
]


@pytest.mark.parametrize("numero", NUMEROS_NO_DECK)
def test_o_numero_aparece_no_deck(deck, numero):
    assert numero in deck, numero


def test_o_deck_nao_promete_a_camada_generativa_como_pronta(deck):
    """A chave de API é pendência registrada no planejamento. Prometer no slide
    o que depende dela é combinar entrega que pode não acontecer."""
    assert "Pendente" in deck
    assert "Depende da chave de API" in deck
