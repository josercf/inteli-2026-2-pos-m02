# -*- coding: utf-8 -*-
"""
Trava a ocupacao do quadro nos slides de conteudo.

"Tem muito espaco em branco" foi a critica que originou este teste. Sem medida,
a correcao dura ate a proxima edicao: alguem tira um bloco, o slide volta a
acabar na metade e ninguem percebe ate a projecao.

O teste nao exige slide cheio. Exige que o conteudo alcance a base da area util:
o defeito especifico e a faixa morta entre o fim do conteudo e o rodape.

Rodar: python3 -m pytest tools/tests/test_ocupacao.py -q
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from tools.medir_ocupacao import medir  # noqa: E402

DECK = RAIZ / "aulas" / "aula01.html"

# Faixa morta tolerada, em pixels, entre o fim do conteudo e o rodape.
# A medicao antes da revisao dava 192px de media e 330px no pior caso.
FAIXA_MORTA_MAXIMA = 130
FAIXA_MORTA_MEDIA_MAXIMA = 70
OCUPACAO_MINIMA_MEDIA = 0.80

DE_CONTEUDO = {"content-slide", "quiz-slide", "exercise-slide"}


@pytest.fixture(scope="module")
def medidas():
    resultados = medir([str(DECK)])
    assert resultados, "nada foi medido: o deck carregou?"
    return [r for r in resultados if r["classe"] in DE_CONTEUDO]


def test_ha_slides_de_conteudo_para_medir(medidas):
    """Zero slides medidos nao pode ler como aprovacao."""
    assert len(medidas) >= 15, len(medidas)


def test_nenhum_slide_acaba_na_metade(medidas):
    piores = [
        (m["slide"], m["fundo_vazio"], m["titulo"])
        for m in medidas
        if m["fundo_vazio"] > FAIXA_MORTA_MAXIMA
    ]
    assert not piores, piores


def test_faixa_morta_media(medidas):
    media = sum(m["fundo_vazio"] for m in medidas) / len(medidas)
    assert media <= FAIXA_MORTA_MEDIA_MAXIMA, round(media)


def test_ocupacao_media_do_quadro(medidas):
    media = sum(m["ocupacao"] for m in medidas) / len(medidas)
    assert media >= OCUPACAO_MINIMA_MEDIA, round(media, 2)
