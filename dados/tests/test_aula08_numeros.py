# -*- coding: utf-8 -*-
"""Trava os números da Aula 08 contra a fila que `app.publicar` grava.

Valores transcritos de forma literal, sem importar constante do gerador: teste
que lê o mesmo número que o deck usa concorda consigo mesmo.

Pula quando o repositório de prática ou a base longa não estão presentes, que
é o caso do CI (ADR-009).

Rodar: .venv/bin/python -m pytest dados/tests/test_aula08_numeros.py -q
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
PRATICA = RAIZ.parent / "inteli-pos-2026-2a-eda"
CACHE = PRATICA / "dados" / ".cache"
DECK = RAIZ / "aulas" / "aula08.html"

pytestmark = pytest.mark.skipif(
    not (PRATICA / "app" / "publicar.py").exists() or not CACHE.exists(),
    reason="a fila publicada sai do repositório de prática (ADR-009)")


@pytest.fixture(scope="module")
def fila():
    if str(PRATICA) not in sys.path:
        sys.path.insert(0, str(PRATICA))
    from app import publicar
    from app.churn import lista, modelo
    from app.treinar import preparar

    X, y = preparar()
    escore = modelo.escore_fora_da_amostra(X, y)
    t = lista.priorizar(escore, valor_em_risco=X.receita_12m)
    return publicar.registros(t, X)


@pytest.fixture(scope="module")
def deck() -> str:
    return DECK.read_text(encoding="utf-8")


def test_a_fila_tem_138_contas(fila, deck):
    assert len(fila) == 138
    assert "138 contas gravadas" in deck


def test_o_valor_esperado_somado(fila, deck):
    assert sum(r["valor_esperado_usd"] for r in fila) == 23_120_906
    assert "USD 23.120.906" in deck


def test_a_conta_d_abre_a_fila(fila, deck):
    d = fila[0]
    assert d["account_id"] == "CLI052938"
    assert d["posicao_por_probabilidade"] == 3024
    assert d["escore"] == 0.448
    assert d["valor_em_risco_usd"] == 4_642_422
    assert d["valor_esperado_usd"] == 2_082_084
    for trecho in ('"posicao_por_probabilidade": 3024', '"escore": 0.448',
                   '"valor_em_risco_usd": 4642422', '"valor_esperado_usd": 2082084'):
        assert trecho in deck


def test_a_conta_usada_como_fora_da_fila_esta_mesmo_fora(fila, deck):
    assert "CLI000001" not in {r["account_id"] for r in fila}
    assert "CLI000001" in deck
