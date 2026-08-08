# -*- coding: utf-8 -*-
"""
Testes dos diagramas de ciclo embutidos.

Eles sao SVG dentro do HTML, e nao <img>, por tres razoes que os testes abaixo
protegem: o fragment do Reveal precisa alcancar cada fase, a cor precisa vir do
tema (senao o validador de fidelidade deixa de valer quando o SVG entra no
HTML) e o desenho precisa caber no proprio viewBox.

Rodar: python3 -m pytest tools/tests/test_diagramas_svg.py -q
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from tools.gerar_diagramas_svg import DIAGRAMAS, LARGURA  # noqa: E402

IMG = RAIZ / "assets" / "img"
DECK = (RAIZ / "aulas" / "aula01.html").read_text(encoding="utf-8")


@pytest.mark.parametrize("nome", list(DIAGRAMAS))
def test_o_diagrama_existe(nome):
    assert (IMG / nome).exists(), f"rode tools/gerar_diagramas_svg.py: falta {nome}"


@pytest.mark.parametrize("nome", list(DIAGRAMAS))
def test_o_diagrama_nao_declara_cor_literal(nome):
    """A cor vem do tema, que consome os tokens da marca.

    Se o SVG trouxesse hex literal, ele entraria no HTML e o check_brand.py
    passaria a reprovar o deck (ou, pior, seria afrouxado para deixar passar) e
    o diagrama deixaria de acompanhar uma troca de segmento.
    """
    texto = (IMG / nome).read_text(encoding="utf-8")
    literais = re.findall(r"#[0-9a-fA-F]{3,8}\b", texto)
    assert not literais, (nome, literais)


@pytest.mark.parametrize("nome", list(DIAGRAMAS))
def test_cada_fase_e_um_passo_revelavel(nome):
    """Sem isso o diagrama volta a chegar inteiro, e a ordem do processo deixa
    de ser conduzida pelo professor."""
    texto = (IMG / nome).read_text(encoding="utf-8")
    fases = re.findall(r'<g class="([^"]*fase[^"]*)"', texto)
    assert len(fases) == 6, (nome, len(fases))
    assert all("fragment" in f for f in fases), fases


@pytest.mark.parametrize("nome", list(DIAGRAMAS))
def test_o_desenho_cabe_na_largura_do_viewbox(nome):
    """Conferencia aritmetica, sem navegador: a ultima caixa nao pode passar da
    borda direita. E o mesmo defeito que cortou 26px da arvore de hipoteses,
    aqui pego antes de publicar."""
    texto = (IMG / nome).read_text(encoding="utf-8")
    direitas = [
        float(x) + float(w)
        for x, w in re.findall(r'<rect x="([\d.]+)"[^>]*width="([\d.]+)"', texto)
    ]
    assert direitas, nome
    assert max(direitas) <= LARGURA, (nome, max(direitas), LARGURA)


@pytest.mark.parametrize("nome", list(DIAGRAMAS))
def test_o_deck_embute_o_diagrama_em_vez_de_apontar_para_ele(nome):
    """Em <img> o fragment nao alcanca o interior da figura, e o diagrama
    voltaria a ser uma imagem que a turma assiste."""
    assert f'src="../assets/img/{nome}"' not in DECK, nome


def test_o_deck_tem_os_dois_diagramas_embutidos():
    assert DECK.count('class="diagrama-ciclo"') == 2, DECK.count('class="diagrama-ciclo"')


def test_os_marcadores_de_seta_tem_id_unico():
    """Dois SVG no mesmo documento com o mesmo id de marker fazem o segundo
    herdar o marcador do primeiro. Aqui os dois sao pintados igual, entao o
    defeito seria invisivel ate alguem mudar um deles."""
    ids = re.findall(r'<marker id="([^"]+)"', DECK)
    assert len(ids) == len(set(ids)), ids
