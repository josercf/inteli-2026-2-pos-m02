# -*- coding: utf-8 -*-
"""
Testes estruturais do deck da Aula 01.

O check_slides.py mede layout num navegador; ele nao percebe secao sem
fechamento, rodape fora de ordem nem imagem apontando para arquivo que nao
existe. Uma edicao no meio do deck que engula um </section> faz o Reveal
juntar dois slides num so, e isso so aparece na projecao.

Rodar: python3 -m pytest tools/tests -q
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

DECK = RAIZ / "aulas" / "aula01.html"


@pytest.fixture(scope="module")
def html() -> str:
    return DECK.read_text(encoding="utf-8")


def test_secoes_abrem_e_fecham(html):
    """Uma substituicao de bloco que come o </section> junta dois slides.

    Aconteceu ao trocar o slide de referencias: o deck passou de 32 para 31
    secoes e o rodape do slide sumiu junto, sem nenhum erro aparecer.
    """
    assert html.count("<section") == html.count("</section>")


def test_rodape_numerado_em_sequencia(html):
    numeros = [int(n) for n in re.findall(r'footer-page">(\d+)<', html)]
    assert numeros, "nenhum slide numerado"
    assert numeros[0] == 2, numeros[0]
    assert numeros == sorted(numeros), numeros
    assert numeros == list(range(2, 2 + len(numeros))), numeros


def test_todo_src_local_existe(html):
    faltando = []
    for src in re.findall(r'src="([^"]+)"', html):
        if src.startswith(("http://", "https://", "data:")):
            continue
        alvo = (DECK.parent / src).resolve()
        if not alvo.exists():
            faltando.append(src)
    assert not faltando, faltando


def test_toda_imagem_tem_texto_alternativo(html):
    sem_alt = [
        tag for tag in re.findall(r"<img\b[^>]*>", html)
        if not re.search(r'alt="[^"]{4,}"', tag)
    ]
    assert not sem_alt, sem_alt


def test_convencoes_editoriais(html):
    """Travessao em dash e emoji sao proibidos no acervo inteiro."""
    assert "—" not in html, "travessao em dash (U+2014) no deck"
    emoji = re.findall(
        "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]", html
    )
    assert not emoji, emoji


def test_as_figuras_do_deck_sao_as_que_o_gerador_produz(html):
    """Figura solta em assets/img que ninguem gera vira arquivo orfao, e o
    contrario (deck citando figura que o gerador nao produz) quebra o site."""
    from tools.gerar_figuras_aula01 import FIGURAS

    citadas = {
        Path(src).name
        for src in re.findall(r'src="([^"]+)"', html)
        if "aula01-" in src
    }
    assert citadas, "o deck nao usa nenhuma figura da aula"
    assert citadas <= set(FIGURAS), citadas - set(FIGURAS)


def test_o_deck_apresenta_os_frameworks_da_aula(html):
    """Se um framework sair do deck sem sair do planejamento, a aula passa a
    prometer no papel o que nao entrega na sala."""
    for termo in ("CRISP-DM", "Nível 0", "Nível 2", "critérios para escolher o alvo"):
        assert termo in html, termo


def test_quiz_tem_uma_resposta_correta_por_pergunta(html):
    blocos = re.findall(r'<ul class="quiz-options">(.*?)</ul>', html, re.S)
    assert blocos, "nenhum quiz no deck"
    for bloco in blocos:
        corretas = bloco.count('data-correct="true"')
        assert corretas == 1, corretas
