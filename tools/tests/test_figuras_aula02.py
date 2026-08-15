# -*- coding: utf-8 -*-
"""As figuras da Aula 02 existem, têm a largura da convenção, e o deck usa
exatamente as que o gerador produz."""

import re
from pathlib import Path

import pytest
from PIL import Image

RAIZ = Path(__file__).resolve().parents[2]
IMG = RAIZ / "assets" / "img"

FIGURAS = [
    "aula02-inversao-segmentos.png",
    "aula02-quebra-taxonomia.png",
    "aula02-mapa-ausencia.png",
]


@pytest.mark.parametrize("nome", FIGURAS)
def test_a_figura_existe_e_tem_1168px_de_largura(nome):
    caminho = IMG / nome
    assert caminho.exists(), f"rode tools/gerar_figuras_aula02.py: falta {nome}"
    assert Image.open(caminho).width == 1168


@pytest.mark.skipif(
    not (RAIZ / "aulas" / "aula02.html").exists(),
    reason="o deck da Aula 02 e construido na Task 5",
)
def test_o_deck_referencia_apenas_figuras_que_o_gerador_produz():
    html = (RAIZ / "aulas" / "aula02.html").read_text(encoding="utf-8")
    citadas = set(re.findall(r'src="\.\./assets/img/(aula02-[^"]+)"', html))
    assert citadas, "nenhuma figura da aula02 referenciada no deck"
    assert citadas <= set(FIGURAS), citadas - set(FIGURAS)
