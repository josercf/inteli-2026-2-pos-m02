# -*- coding: utf-8 -*-
"""Trava os números da Aula 08 contra a base longa do case.

Os valores esperados estão transcritos de forma literal, sem importar constante
do gerador: teste que lê o mesmo número que o deck usa concorda consigo mesmo.
A referência é dados/analise_aula08.py, que tools/tests/test_painel_modelo.py
compara com o modelo que roda no painel.

Pula quando a base longa não está presente, que é o caso do CI (ADR-005).

Rodar: .venv/bin/python -m pytest dados/tests/test_aula08_numeros.py -q
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from dados import analise_aula08 as a  # noqa: E402

DECK = RAIZ / "aulas" / "aula08.html"
GUIA = RAIZ / "materiais" / "aula08-guia.html"

pytestmark = pytest.mark.skipif(not a.PLANILHA.exists(),
                                reason="a base longa do case não é versionada (ADR-005)")


@pytest.fixture(scope="module")
def r():
    return a.rodar(a.carregar())


@pytest.fixture(scope="module")
def textos() -> str:
    return DECK.read_text(encoding="utf-8") + GUIA.read_text(encoding="utf-8")


def test_contas_elegiveis_e_perdidas(r, textos):
    assert len(r["tabela"]) == 4593
    assert int(r["tabela"].churn.sum()) == 2446
    assert "4.593" in textos


def test_auc_fora_da_amostra(r, textos):
    assert round(r["auc"], 4) == 0.8138
    assert "0,814" in textos


def test_a_fila_de_138(r, textos):
    assert len(r["fila"]) == 138
    assert r["acertos_fila"] == 35
    assert round(r["valor_esperado_fila"]) == 26_601_312
    assert "35 das 138" in textos and "26,6 milhões" in textos


def test_a_primeira_conta_da_fila(r):
    primeira = r["fila"].iloc[0]
    assert primeira.account_id == "CLI001165"
    assert round(primeira.escore, 3) == 0.347
