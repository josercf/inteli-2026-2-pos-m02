# -*- coding: utf-8 -*-
"""Convenções do deck da Aula 04. Mesmas regras da Aula 03, com os números e as práticas desta aula."""

import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from tools.check_retorica import analisar, texto_visivel  # noqa: E402

DECK = RAIZ / "aulas" / "aula04.html"


@pytest.fixture(scope="module")
def html() -> str:
    assert DECK.exists(), "rode tools/montar_deck_aula04.py"
    return DECK.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Estrutura
# ---------------------------------------------------------------------------

def test_secoes_abrem_e_fecham(html):
    assert html.count("<section") == html.count("</section>")


def test_divs_abrem_e_fecham(html):
    """Par de section balanceado não garante DOM correto: ver docstring."""
    abre = len(re.findall(r"<div[ >]", html))
    fecha = html.count("</div>")
    assert abre == fecha, f"{abre} aberturas contra {fecha} fechamentos"


def test_todo_slide_e_filho_direto_do_container(html):
    """Cada section fecha antes da próxima abrir, sem aninhamento."""
    marcas = re.findall(r"<section|</section>", html)
    profundidade = 0
    for marca in marcas:
        profundidade += 1 if marca == "<section" else -1
        assert profundidade in (0, 1), "section aninhada dentro de outra"
    assert profundidade == 0


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


# ---------------------------------------------------------------------------
# Convenções editoriais
# ---------------------------------------------------------------------------

def test_convencoes_editoriais(html):
    assert "—" not in html, "em dash proibido"
    assert not re.search(r"[\U0001F300-\U0001FAFF☀-➿]", html), "emoji proibido"


def test_o_deck_nao_usa_paralelismo(html):
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


def test_todo_slide_que_mede_fecha_com_implicacao(html):
    """Slide analítico declara o "e daí"; slide de referência, não.

    Um slide cujo corpo é só uma tabela de especificação (entregáveis,
    checklist) não tem achado a declarar, e a faixa vira frase de efeito. A
    exceção é fechada: o corpo precisa ser uma tabela e nada mais.
    """
    blocos = re.findall(r'<section class="content-slide".*?</section>', html, re.S)
    assert blocos
    sem_faixa = []
    for bloco in blocos:
        if 'class="fecho"' in bloco:
            continue
        corpo = re.search(r"</h2>(.*?)<div class=\"slide-footer", bloco, re.S)
        assert corpo, bloco[:200]
        texto = corpo.group(1)
        assert "<table" in texto, bloco[:200]
        assert "<p" not in texto.replace('<p class="linha-contexto"', ""), bloco[:200]
        sem_faixa.append(bloco)
    assert len(sem_faixa) <= 2, len(sem_faixa)


# ---------------------------------------------------------------------------
# Quiz
# ---------------------------------------------------------------------------

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
    """Só se aplica com dois ou mais quizzes: a Aula 04 tem um único quiz."""
    posicoes = []
    for bloco in re.findall(r'<section class="quiz-slide".*?</section>', html, re.S):
        itens = re.findall(r'data-correct="(true|false)"', bloco)
        posicoes.append(itens.index("true"))
    if len(posicoes) < 2:
        return
    assert len(set(posicoes)) > 1, posicoes


# ---------------------------------------------------------------------------
# O que é próprio desta aula
# ---------------------------------------------------------------------------

def test_as_praticas_rodam_em_antigravity(html):
    """ADR-006: ambiente único na tarde inteira.

    Conta práticas distintas, e não slides: as Práticas 2 e 3 ocupam três
    slides cada, porque uma prática de quatro passos com prompt foi lida em
    15/08 como se fosse um pedido único.
    """
    blocos = re.findall(r'<section class="exercise-slide".*?</section>', html, re.S)
    assert blocos
    numeros = set()
    for bloco in blocos:
        assert "Gemini" not in bloco
        m = re.search(r"Prática (\d+)", bloco)
        if m:
            numeros.add(int(m.group(1)))
    assert numeros == {1, 2, 3, 4}, numeros
    assert sum("Antigravity" in b for b in blocos) >= 4


def test_pratica_longa_vem_dividida(html):
    """O slide de enquadramento traz o trilho; os de passo a passo, não."""
    for numero in (1, 2):
        # Casa contra a sobrelinha, e não contra qualquer menção: a oficina
        # cita "Prática 2" e "Prática 3" no corpo dos passos.
        blocos = [b for b in re.findall(r'<section class="exercise-slide".*?</section>', html, re.S)
                  if re.search(rf'class="sobrelinha">Prática {numero} ', b)]
        assert len(blocos) == 2, (numero, len(blocos))
        com_trilho = [b for b in blocos if "pratica-trilho" in b]
        assert len(com_trilho) == 1, numero


def test_o_deck_cita_os_numeros_travados(html):
    """Nenhum número do case sem teste. Estes vêm de test_aula04_numeros.py."""
    for numero in (
        "8.282", "1.593", "19,2", "3.748", "42,5", "4.534",
        "58,1", "47,5", "33,5", "28,5", "25,4", "143,8",
        "66,4", "51,5", "34,8", "16,1", "615,4",
        "85,4", "52,3", "22,0", "5,6",
        "63,2", "11,4", "84,3", "46,9",
        "81,5", "92,5", "52,5", "53,4", "21,4", "20,3",
        "28,2", "12,5", "18,6", "32,4", "72,6", "41,0", "69,7", "28,1",
        "59,7", "55,6", "1.560",
        "147,3", "65,7",
        "66 contas", "63 seguem", "716", "263", "261", "173", "162", "138",
    ):
        assert numero in html, numero


def test_o_deck_nao_expoe_os_ids_do_par(html):
    assert "CLI000269" not in html and "CLI000264" not in html
    assert "Conta A" in html and "Conta B" in html


def test_a_implicacao_e_o_ultimo_passo_onde_ha_revelacao(html):
    for classe, corpo in re.findall(
        r'<section class="([^"]+)">(.*?)</section>', html, re.S
    ):
        if classe != "content-slide" or "fragment" not in corpo:
            continue
        faixa = re.search(r'<div class="faixa-conclusao([^"]*)"', corpo)
        assert faixa and "fragment" in faixa.group(1), corpo[:120]
