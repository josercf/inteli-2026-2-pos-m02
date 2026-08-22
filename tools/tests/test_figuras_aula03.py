# -*- coding: utf-8 -*-
"""As tres figuras da Aula 03 existem, tem a largura da convencao e nao estao vazias."""

from pathlib import Path

import pytest
from PIL import Image

RAIZ = Path(__file__).resolve().parents[2]
IMG = RAIZ / "assets" / "img"

FIGURAS = (
    "aula03-distribuicao-receita.png",
    "aula03-contingencia-rotulo.png",
    "aula03-prevalencia-segmento.png",
)


@pytest.mark.parametrize("nome", FIGURAS)
def test_largura_da_convencao(nome):
    """1168px de largura: a figura e governada pela largura e renderiza 1:1."""
    largura, altura = Image.open(IMG / nome).size
    assert largura == 1168
    assert altura > 200


@pytest.mark.parametrize("nome", FIGURAS)
def test_figura_nao_esta_em_branco(nome):
    """Sem o xlsx o gerador falha, mas um PNG antigo poderia ficar para tras."""
    img = Image.open(IMG / nome).convert("RGB")
    cores = img.getcolors(maxcolors=1_000_000)
    assert cores is not None
    dominante = max(c for c, _ in cores)
    assert dominante / (img.width * img.height) < 0.97
