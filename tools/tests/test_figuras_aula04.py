# -*- coding: utf-8 -*-
"""As seis figuras da Aula 04 existem, têm a largura da convenção e não estão vazias."""

from pathlib import Path

import pytest
from PIL import Image

RAIZ = Path(__file__).resolve().parents[2]
IMG = RAIZ / "assets" / "img"

FIGURAS = (
    # Didáticas, com semente fixa: o conceito chega antes do número da Kovan.
    "aula04-ic-didatico.png",
    "aula04-estratificacao-didatica.png",
    # Reais, a partir do dataset oficial.
    "aula04-prevalencia-elegiveis.png",
    "aula04-marcas-por-dias.png",
    "aula04-par-pbl.png",
    "aula04-fila-por-segmento.png",
    "aula04-prevalencia-setor.png",
    "aula04-rajada-setor.png",
)


@pytest.mark.parametrize("nome", FIGURAS)
def test_largura_da_convencao(nome):
    largura, altura = Image.open(IMG / nome).size
    assert largura == 1168
    assert altura > 200


@pytest.mark.parametrize("nome", FIGURAS)
def test_figura_nao_esta_em_branco(nome):
    img = Image.open(IMG / nome).convert("RGB")
    cores = img.getcolors(maxcolors=1_000_000)
    assert cores is not None
    dominante = max(c for c, _ in cores)
    assert dominante / (img.width * img.height) < 0.97
