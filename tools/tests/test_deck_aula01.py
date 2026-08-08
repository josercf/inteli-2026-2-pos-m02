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
    # O deck tambem cita o PNG do ultimo quadro de cada GIF, que e o fallback
    # de impressao gerado junto com ele.
    validas = set(FIGURAS) | {n[:-4] + ".png" for n in FIGURAS if n.endswith(".gif")}
    assert citadas <= validas, citadas - validas


def test_o_deck_apresenta_os_frameworks_da_aula(html):
    """Se um framework sair do deck sem sair do planejamento, a aula passa a
    prometer no papel o que nao entrega na sala.

    Os termos verificados sao de conteudo, nao de titulo: o titulo e reescrito
    com frequencia e a checagem nao pode quebrar por causa disso.
    """
    for termo in ("CRISP-DM", "Nível 0", "Nível 2", "Observabilidade",
                  "Verificabilidade", "aula01-arvore-hipoteses"):
        assert termo in html, termo


# Padroes de titulo rejeitados na revisao de diagramacao. Nao sao "erros de
# portugues": sao registros que o professor recusou explicitamente, e que
# reapareceriam a cada aula nova sem um teste para segura-los.
TITULO_PROIBIDO = [
    ("pergunta retórica em slide de conteúdo", lambda t: t.endswith("?")),
    ("abertura conversacional", lambda t: t.lower().startswith(("onde ", "o que a ", "o que o ", "como a ", "como o "))),
    ("metáfora conhecida", lambda t: any(m in t.lower() for m in ("escada", "máquina", "desemboca", "anatomia", "guarda-chuva"))),
    ("título de percurso", lambda t: t.lower().startswith("da ") and " às " in t.lower()),
]


def _titulos_por_tipo(html: str) -> dict[str, list[str]]:
    import re as _re

    fora = {"cover-slide", "section-slide", "end-slide", "exercise-slide", "quiz-slide"}
    achados: dict[str, list[str]] = {}
    for bloco in _re.findall(r'<section class="([^"]+)">(.*?)</section>', html, _re.S):
        classe, corpo = bloco
        titulo = _re.search(r"<h2>(.*?)</h2>", corpo, _re.S)
        if not titulo:
            continue
        chave = "conteudo" if classe not in fora else classe
        achados.setdefault(chave, []).append(_re.sub(r"<[^>]+>", "", titulo.group(1)).strip())
    return achados


def test_titulos_de_conteudo_sao_afirmativos_e_sobrios(html):
    titulos = _titulos_por_tipo(html).get("conteudo", [])
    assert len(titulos) >= 10, len(titulos)
    problemas = [
        (t, motivo) for t in titulos for motivo, regra in TITULO_PROIBIDO if regra(t)
    ]
    assert not problemas, problemas


def test_titulo_de_conteudo_cabe_em_duas_linhas(html):
    """Convencao de titulo afirmativo: ate 15 palavras, no maximo duas linhas.

    O limite de caracteres vem da medida real: a 38px, com max-width de 1030px,
    duas linhas comportam cerca de 100 caracteres. Acima disso o titulo invade
    a area do logo ou empurra a faixa de conclusao para fora do slide.
    """
    longos = [t for t in _titulos_por_tipo(html).get("conteudo", []) if len(t) > 100]
    assert not longos, longos
    prolixos = [t for t in _titulos_por_tipo(html).get("conteudo", []) if len(t.split()) > 15]
    assert not prolixos, prolixos


def test_slide_de_quiz_nao_entrega_o_gabarito_no_titulo(html):
    """Titulo afirmativo em quiz mata o exercicio: ele nomeia o objeto avaliado."""
    for titulo in _titulos_por_tipo(html).get("quiz-slide", []):
        assert not titulo.endswith("."), titulo
        assert len(titulo.split()) <= 8, titulo


def test_todo_slide_de_conteudo_fecha_com_implicacao(html):
    """A faixa de conclusao e o que ocupa o fundo do slide e o que obriga o
    autor a declarar o "e dai" de cada pagina."""
    import re as _re

    sem_fecho = []
    for classe, corpo in _re.findall(r'<section class="([^"]+)">(.*?)</section>', html, _re.S):
        if classe != "content-slide":
            continue
        if "faixa-conclusao" not in corpo:
            titulo = _re.search(r"<h2>(.*?)</h2>", corpo, _re.S)
            sem_fecho.append(titulo.group(1)[:60] if titulo else "?")
    assert not sem_fecho, sem_fecho


def test_quiz_tem_uma_resposta_correta_por_pergunta(html):
    blocos = re.findall(r'<ul class="quiz-options">(.*?)</ul>', html, re.S)
    assert blocos, "nenhum quiz no deck"
    for bloco in blocos:
        corretas = bloco.count('data-correct="true"')
        assert corretas == 1, corretas


# ---------------------------------------------------------------------------
# Construcao do item de quiz
# ---------------------------------------------------------------------------


def _quizzes(html: str) -> list[list[tuple[str, bool]]]:
    saida = []
    for bloco in re.findall(r'<ul class="quiz-options">(.*?)</ul>', html, re.S):
        itens = []
        for li in re.findall(r"<li\b(.*?)</li>", bloco, re.S):
            correta = 'data-correct="true"' in li
            texto = re.sub(r"<[^>]+>", "", li.split(">", 1)[1]).strip()
            itens.append((texto, correta))
        saida.append(itens)
    return saida


def test_a_alternativa_correta_nao_e_a_mais_longa(html):
    """A correta media 112 caracteres contra 49 a 58 dos distratores, e era a
    unica em duas linhas: 97px contra 63px de altura. Numa turma senior, "a
    mais longa e a mais qualificada e a certa" resolve o item sem ler o painel.
    """
    for i, itens in enumerate(_quizzes(html), 1):
        tamanhos = [len(t) for t, _ in itens]
        correta = next(len(t) for t, c in itens if c)
        assert correta != max(tamanhos), (i, tamanhos)


def test_as_alternativas_tem_comprimento_comparavel(html):
    for i, itens in enumerate(_quizzes(html), 1):
        tamanhos = [len(t) for t, _ in itens]
        assert max(tamanhos) - min(tamanhos) <= 25, (i, tamanhos)


def test_a_correta_nao_fica_sempre_na_mesma_posicao(html):
    posicoes = [
        next(j for j, (_, c) in enumerate(itens) if c) for itens in _quizzes(html)
    ]
    assert len(set(posicoes)) > 1, posicoes


# ---------------------------------------------------------------------------
# Revelacao por passos
# ---------------------------------------------------------------------------


def test_os_slides_de_sequencia_revelam_por_passos(html):
    """Onde o argumento tem ordem, a turma nao pode ler o fim antes do comeco.

    O caso mais claro e o slide dos quatro niveis de prompt: a tese e que cada
    nivel ACRESCENTA uma restricao, e com os quatro visiveis de uma vez ninguem
    sente o acrescimo.
    """
    assert html.count("fragment") >= 15, html.count("fragment")


def test_a_implicacao_e_o_ultimo_passo_onde_ha_revelacao(html):
    """Se a faixa aparece junto com o corpo, a turma le a conclusao antes da
    primeira frase e o resto do slide vira confirmacao."""
    import re as _re

    for classe, corpo in _re.findall(r'<section class="([^"]+)">(.*?)</section>', html, _re.S):
        if classe != "content-slide" or "fragment" not in corpo:
            continue
        faixa = _re.search(r'<div class="faixa-conclusao([^"]*)"', corpo)
        assert faixa and "fragment" in faixa.group(1), corpo[:120]
