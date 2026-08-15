# -*- coding: utf-8 -*-
"""Convenções do deck da Aula 02.

Reaproveita as regras de tools/tests/test_deck_aula01.py e acrescenta as da
diretiva editorial de 15/08: sem paralelismo negativo, sem antítese simétrica e
sem escalada com dois-pontos, travadas por tools/check_retorica.py.
"""

import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from tools.check_retorica import analisar, texto_visivel  # noqa: E402

DECK = RAIZ / "aulas" / "aula02.html"


@pytest.fixture(scope="module")
def html() -> str:
    assert DECK.exists(), "rode tools/montar_deck_aula02.py"
    return DECK.read_text(encoding="utf-8")


def test_secoes_abrem_e_fecham(html):
    assert html.count("<section") == html.count("</section>")


def test_rodape_numerado_em_sequencia(html):
    paginas = [int(n) for n in re.findall(r'class="footer-page">(\d+)<', html)]
    assert paginas, "nenhum slide numerado"
    assert paginas == list(range(2, 2 + len(paginas))), paginas


def test_todo_src_local_existe(html):
    for src in re.findall(r'src="(\.\./[^"]+)"', html):
        alvo = (RAIZ / "aulas" / src).resolve()
        assert alvo.exists(), src


def test_toda_imagem_tem_texto_alternativo(html):
    for tag in re.findall(r"<img\b[^>]*>", html):
        assert re.search(r'alt="[^"]{4,}"', tag), tag


def test_convencoes_editoriais(html):
    assert "—" not in html, "em dash proibido"
    assert not re.search(r"[\U0001F300-\U0001FAFF☀-➿]", html), "emoji proibido"


def test_o_deck_nao_usa_paralelismo(html):
    """A diretiva editorial de 15/08, travada por validador."""
    problemas = []
    for numero, texto in texto_visivel(html):
        for achado in analisar(texto):
            if achado.bloqueia:
                problemas.append((numero, achado.construcao, achado.trecho))
    assert not problemas, problemas


def test_titulo_de_conteudo_e_afirmativo(html):
    for bloco in re.findall(r'<section class="content-slide".*?</section>', html, re.S):
        titulo = re.search(r"<h2>(.*?)</h2>", bloco, re.S)
        if not titulo:
            continue
        texto = re.sub(r"<[^>]+>", "", titulo.group(1)).strip()
        assert not texto.endswith("?"), f"pergunta em slide de conteudo: {texto}"


def test_titulo_de_quiz_nao_entrega_o_gabarito(html):
    blocos = re.findall(r'<section class="quiz-slide".*?</section>', html, re.S)
    assert blocos, "nenhum quiz no deck"
    for bloco in blocos:
        titulo = re.search(r"<h2>(.*?)</h2>", bloco, re.S)
        texto = re.sub(r"<[^>]+>", "", titulo.group(1)).strip()
        assert len(texto.split()) <= 8, f"titulo de quiz longo demais: {texto}"
        assert not texto.endswith("."), texto


def test_todo_slide_de_conteudo_fecha_com_implicacao(html):
    blocos = re.findall(r'<section class="content-slide".*?</section>', html, re.S)
    assert blocos
    for bloco in blocos:
        assert 'class="fecho"' in bloco, bloco[:200]


def test_quiz_tem_uma_resposta_correta_por_pergunta(html):
    for bloco in re.findall(r'<section class="quiz-slide".*?</section>', html, re.S):
        assert bloco.count('data-correct="true"') == 1


def test_a_alternativa_correta_nao_e_a_mais_longa(html):
    for bloco in re.findall(r'<section class="quiz-slide".*?</section>', html, re.S):
        itens = re.findall(r'data-correct="(true|false)"[^>]*>([^<]+)</li>', bloco)
        assert len(itens) == 4, itens
        certa = [t for c, t in itens if c == "true"][0]
        assert len(certa) < max(len(t) for _, t in itens), certa


def test_as_alternativas_tem_comprimento_comparavel(html):
    for bloco in re.findall(r'<section class="quiz-slide".*?</section>', html, re.S):
        itens = re.findall(r'data-correct="(true|false)"[^>]*>([^<]+)</li>', bloco)
        tamanhos = [len(t) for _, t in itens]
        assert max(tamanhos) - min(tamanhos) <= 25, tamanhos


def test_a_correta_nao_fica_sempre_na_mesma_posicao(html):
    posicoes = []
    for bloco in re.findall(r'<section class="quiz-slide".*?</section>', html, re.S):
        itens = re.findall(r'data-correct="(true|false)"', bloco)
        posicoes.append(itens.index("true"))
    assert len(set(posicoes)) > 1, posicoes


def test_as_praticas_rodam_em_gemini(html):
    praticas = re.findall(r'<section class="exercise-slide".*?</section>', html, re.S)
    assert len(praticas) == 4
    for bloco in praticas:
        assert "Gemini" in bloco
        assert "Colab" not in bloco


def test_o_deck_cita_os_numeros_travados(html):
    """Nenhum número do case sem teste. Estes vêm de test_aula02_numeros.py."""
    for numero in ("160", "8.280", "29,4", "49,9", "53,2", "98,5", "30,4",
                   "217,4", "15.999", "16.618", "1.187", "34"):
        assert numero in html, numero


def test_os_slides_de_sequencia_revelam_por_passos(html):
    """Onde o argumento tem ordem, a turma não pode ler o fim antes do começo."""
    assert html.count("fragment") >= 12, html.count("fragment")


def test_a_implicacao_e_o_ultimo_passo_onde_ha_revelacao(html):
    for classe, corpo in re.findall(
        r'<section class="([^"]+)">(.*?)</section>', html, re.S
    ):
        if classe != "content-slide" or "fragment" not in corpo:
            continue
        faixa = re.search(r'<div class="faixa-conclusao([^"]*)"', corpo)
        assert faixa and "fragment" in faixa.group(1), corpo[:120]
