# -*- coding: utf-8 -*-
"""Testes dos quatro diagramas de métrica da Aula 06.

Duas classes de defeito já apareceram aqui, e as duas passam pelo
tools/check_slides.py, que mede a caixa do <svg> e não o que está desenhado
dentro dela:

1. Texto com `y` maior que a altura da viewBox. Some da figura sem erro nenhum.
   Aconteceu duas vezes: em ALTURA 348 a linha do numerador caía em y=368, e em
   ALTURA 300 com célula de 84 ela caía em y=308 e saía cortada ao meio.
2. Elemento coberto por outro. Os valores das duas barras da fila de 138 caíam
   em x=836, atrás do painel que começa em x=806.

Rodar: PYTHONPATH=. .venv/bin/python -m pytest tools/tests/test_diagramas_metricas.py -q
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

IMG = RAIZ / "assets" / "img"
DECK = RAIZ / "aulas" / "aula06.html"
XLSX = RAIZ / "dados" / "datasets_case_modulo2_5yrs.xlsx"
CACHE = RAIZ / "dados" / ".cache_5yrs"

ARQUIVOS = ["aula06-metrica-acuracia.svg", "aula06-metrica-precisao.svg",
            "aula06-metrica-revocacao.svg", "aula06-metrica-f1.svg"]


@pytest.fixture(scope="module")
def gerador():
    from tools import gerar_diagramas_metricas

    return gerar_diagramas_metricas


def _svg(nome: str) -> str:
    return (IMG / nome).read_text(encoding="utf-8")


def _viewbox(svg: str) -> tuple[float, float]:
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    assert m, "sem viewBox"
    return float(m.group(1)), float(m.group(2))


# ---------------------------------------------------------------------------
# Estrutura
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("nome", ARQUIVOS)
def test_o_arquivo_existe_e_e_svg(nome):
    svg = _svg(nome)
    assert svg.startswith("<svg"), nome
    assert 'class="matriz-confusao"' in svg
    assert svg.rstrip().endswith("</svg>")


@pytest.mark.parametrize("nome", ARQUIVOS)
def test_nenhuma_cor_literal_no_svg(nome):
    """Cor literal aqui entraria no HTML do deck e reprovaria o check_brand."""
    svg = _svg(nome)
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b", svg), nome
    assert "rgb(" not in svg and "hsl(" not in svg


@pytest.mark.parametrize("nome", ARQUIVOS)
def test_todo_texto_cabe_dentro_da_viewbox(nome):
    """O defeito que o validador de layout não vê.

    Visto falhando: com CEL_A em 84 e ALTURA em 300, a linha do numerador
    ficava em y=308 e este teste acusava 1 texto fora.
    """
    svg = _svg(nome)
    largura, altura = _viewbox(svg)
    fora = []
    for m in re.finditer(r'<text[^>]*\bx="([\d.-]+)"[^>]*\by="([\d.-]+)"', svg):
        x, y = float(m.group(1)), float(m.group(2))
        # Uma linha de texto desce cerca de 6px abaixo da baseline.
        if y > altura - 4 or y < 10 or x < 0 or x > largura:
            fora.append((x, y))
    assert not fora, (nome, fora)


@pytest.mark.parametrize("nome", ARQUIVOS)
def test_todo_retangulo_cabe_dentro_da_viewbox(nome):
    svg = _svg(nome)
    largura, altura = _viewbox(svg)
    fora = []
    for m in re.finditer(
            r'<rect[^>]*\bx="([\d.-]+)"[^>]*\by="([\d.-]+)"[^>]*\bwidth="([\d.-]+)"[^>]*\bheight="([\d.-]+)"',
            svg):
        x, y, w, h = (float(m.group(i)) for i in range(1, 5))
        if x < 0 or y < 0 or x + w > largura or y + h > altura:
            fora.append((x, y, w, h))
    assert not fora, (nome, fora)


def test_a_invariante_de_altura_da_matriz(gerador):
    """A regra que resolve as duas quebras de viewBox de uma vez."""
    g = gerador
    ultima_linha = g.Y0 + g.CEL_A * 2 + g.GAP + 48
    assert ultima_linha < g.ALTURA, (ultima_linha, g.ALTURA)


def test_o_valor_da_barra_nao_fica_atras_do_painel(gerador):
    """A barra do F1 termina antes de onde o painel da direita começa."""
    x, largura = 300, 420
    assert x + largura + 16 + 60 <= gerador.PAINEL_X, "o valor invade o painel"


@pytest.mark.parametrize("nome", ARQUIVOS)
def test_cada_diagrama_tem_pelo_menos_dois_passos(nome):
    """Sem fragment o slide vira figura estática e o professor perde o ritmo."""
    assert _svg(nome).count('class="fragment"') >= 2 or \
        _svg(nome).count("fragment") >= 2, nome


# ---------------------------------------------------------------------------
# Os números do diagrama batem com a análise
# ---------------------------------------------------------------------------

precisa_da_base = pytest.mark.skipif(
    not (XLSX.exists() or CACHE.exists()),
    reason="base longa não versionada (ADR-005)")


@precisa_da_base
def test_a_matriz_transcrita_bate_com_o_dataset(gerador):
    """Os quatro valores estão transcritos no gerador. Aqui eles são conferidos
    contra o escore de verdade, no limiar de 0,5."""
    from dados import analise_aula06_longa as a

    e = a.painel_de_features()
    previsto = (a.escore() >= 0.5).astype(int).to_numpy()
    real = e.churn.to_numpy(dtype=int)
    vp = int(((previsto == 1) & (real == 1)).sum())
    fp = int(((previsto == 1) & (real == 0)).sum())
    fn = int(((previsto == 0) & (real == 1)).sum())
    vn = int(((previsto == 0) & (real == 0)).sum())
    assert (gerador.VP, gerador.FP, gerador.FN, gerador.VN) == (vp, fp, fn, vn)
    assert gerador.TOTAL == len(e)


@precisa_da_base
def test_a_fila_transcrita_bate_com_o_dataset(gerador):
    from dados import analise_aula06_longa as a

    r = a.lista_priorizada(138)
    assert gerador.VP138 == r["verdadeiros_positivos"]
    assert gerador.FP138 == r["falsos_positivos"]
    assert gerador.FN138 == r["falsos_negativos"]


# ---------------------------------------------------------------------------
# As porcentagens desenhadas
# ---------------------------------------------------------------------------

def test_as_porcentagens_desenhadas(gerador):
    g = gerador
    assert "77,0%" in _svg("aula06-metrica-acuracia.svg")
    assert "75,8%" in _svg("aula06-metrica-precisao.svg")
    assert "82,2%" in _svg("aula06-metrica-revocacao.svg")
    f1 = _svg("aula06-metrica-f1.svg")
    for valor in ("75,8%", "82,2%", "78,9%", "82,6%", "4,6%", "8,8%", "43,6%"):
        assert valor in f1, valor
    # O F1 fica entre precisão e revocação quando as duas são parecidas, e
    # abaixo das duas quando uma desaba. É o argumento do slide.
    p = g.VP / (g.VP + g.FP)
    r = g.VP / (g.VP + g.FN)
    f = 2 * p * r / (p + r)
    assert min(p, r) < f < max(p, r)
    p138 = g.VP138 / (g.VP138 + g.FP138)
    r138 = g.VP138 / (g.VP138 + g.FN138)
    f138 = 2 * p138 * r138 / (p138 + r138)
    assert f138 < (p138 + r138) / 2


# ---------------------------------------------------------------------------
# O deck embute os quatro
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("nome", ARQUIVOS)
def test_o_deck_embute_o_svg(nome):
    """Embutido, e não em <img>: em <img> o fragment do Reveal não alcança o
    interior da figura."""
    deck = DECK.read_text(encoding="utf-8")
    svg = _svg(nome)
    assinatura = re.search(r'aria-label="([^"]+)"', svg).group(1)
    assert assinatura in deck, nome
    assert f'src="../assets/img/{nome}"' not in deck, f"{nome} entrou como <img>"
