# -*- coding: utf-8 -*-
"""
Construtores de slide compartilhados entre os decks das aulas.

Extraido de tools/montar_deck_aula01.py: os construtores sao 220 linhas
identicas que qualquer segunda aula precisaria duplicar. Como funcao, a
estrutura de faixas (sobrelinha, titulo, corpo, faixa de conclusao, fonte) e
igual em todo slide; duplicada em dois geradores, ela diverge na primeira
correcao de layout aplicada de um lado so.

Cada deck que consome este modulo chama `configurar()` com o texto de rodape
proprio e `reiniciar_paginacao()` antes de montar os slides, porque o contador
de paginas e global ao processo.
"""

from __future__ import annotations

import html as _html
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
LOGO = '<img class="inteli-logo-header" src="../assets/img/inteli-exec-logo-positiva.png" alt="Logo Inteli">'

RODAPE_TEXTO = "Módulo 2 &middot; Aula 01"   # sobrescrito por configurar()

_pagina = 1


def configurar(rodape_texto: str) -> None:
    """Define o texto do rodapé do deck em construção."""
    global RODAPE_TEXTO
    RODAPE_TEXTO = rodape_texto


def reiniciar_paginacao() -> None:
    """Zera o contador de páginas. Obrigatório entre dois decks no mesmo processo."""
    global _pagina
    _pagina = 1


def _proxima() -> int:
    global _pagina
    _pagina += 1
    return _pagina


def _rodape() -> str:
    return (
        '        <div class="slide-footer">\n'
        f'          <p class="footer-bar">{RODAPE_TEXTO}</p>\n'
        f'          <p class="footer-page">{_proxima()}</p>\n'
        "        </div>\n"
    )


def _cabecalho(sobrelinha: str | None, titulo: str, contexto: str | None) -> str:
    partes = ['        <div class="slide-title-area">\n']
    if sobrelinha:
        partes.append(f'          <p class="sobrelinha">{sobrelinha}</p>\n')
    partes.append('          <div class="accent-bar"></div>\n')
    partes.append(f"          <h2>{titulo}</h2>\n")
    if contexto:
        partes.append(f'          <p class="linha-contexto">{contexto}</p>\n')
    partes.append("        </div>\n")
    return "".join(partes)


def _conclusao(texto: str | None, rotulo: str = "Implicação", clara: bool = False,
               fragmento: bool = False) -> str:
    """A faixa de implicacao.

    Quando o slide revela por passos, ela e o ultimo fragment: o titulo afirma
    o achado, a exposicao o constroi e a implicacao fecha. Sem isso a turma le
    a conclusao antes da primeira frase do professor, e o resto do slide vira
    confirmacao do que ja foi lido.

    O Reveal esconde fragment com `visibility: hidden`, nao com `display: none`:
    o espaco continua reservado e o layout nao pula ao revelar.
    """
    if not texto:
        return ""
    classe = "faixa-conclusao clara" if clara else "faixa-conclusao"
    if fragmento:
        classe += " fragment"
    return (
        f'        <div class="{classe}">\n'
        f'          <span class="rotulo">{rotulo}</span>\n'
        f"          <p>{texto}</p>\n"
        "        </div>\n"
    )


def _fonte(texto: str | None) -> str:
    return f'        <p class="fonte-nota">{texto}</p>\n' if texto else ""


def _fecho(conclusao, rotulo, clara, fonte, fragmento=False) -> str:
    """Faixa de conclusao e linha de fonte, no mesmo bloco, coladas na base.

    Precisam sair juntas: com `margin-top: auto` na faixa sozinha, a linha de
    fonte vinha depois dela e caia fora da area util. Quatro slides estouravam
    por 10 a 63px exatamente por isso.
    """
    corpo = _conclusao(conclusao, rotulo, clara, fragmento) + _fonte(fonte)
    return f'        <div class="fecho">\n{corpo}        </div>\n' if corpo else ""


def conteudo(titulo, corpo, sobrelinha=None, contexto=None, conclusao=None,
             rotulo_conclusao="Implicação", conclusao_clara=False, fonte=None,
             por_passos=False) -> str:
    """Slide de conteudo. `por_passos` faz a faixa de implicacao ser o ultimo
    fragment, para os slides cujo corpo tambem e revelado por partes."""
    return (
        '      <section class="content-slide">\n'
        '        <div class="top-bar"></div>\n'
        f"        {LOGO}\n"
        + _cabecalho(sobrelinha, titulo, contexto)
        + corpo
        + _fecho(conclusao, rotulo_conclusao, conclusao_clara, fonte, por_passos)
        + _rodape()
        + "      </section>\n"
    )


def figura(titulo, arquivo, alt, sobrelinha=None, contexto=None, conclusao=None,
           rotulo_conclusao="Implicação", fonte=None) -> str:
    """Slide de figura.

    Quando a figura e animada, o slide carrega tambem o ultimo quadro em PNG:
    o PDF exportado congela um GIF no primeiro quadro, e o handout da aula sai
    desse PDF.
    """
    animada = arquivo.endswith(".gif")
    classe = "figura figura-animada" if animada else "figura"
    corpo = f'        <img class="{classe}" src="../assets/img/{arquivo}" alt="{alt}">\n'
    if animada:
        estatica = arquivo[:-4] + ".png"
        corpo += f'        <img class="figura figura-print" src="../assets/img/{estatica}" alt="{alt}">\n'
    return conteudo(titulo, corpo, sobrelinha, contexto, conclusao,
                    rotulo_conclusao, conclusao_clara=True, fonte=fonte)


def figura_embutida(titulo, arquivo, sobrelinha=None, contexto=None, conclusao=None,
                    rotulo_conclusao="Implicação", fonte=None) -> str:
    """Slide de diagrama vetorial embutido no proprio HTML.

    Embutido, e nao em <img>: so assim o fragment do Reveal alcanca cada grupo
    de dentro da figura, e o professor revela fase a fase em vez de assistir a
    um GIF rodar sozinho. Imprime como vetor, sem congelar num quadro.
    """
    svg = (RAIZ / "assets" / "img" / arquivo).read_text(encoding="utf-8")
    corpo = "".join(f"        {linha}\n" for linha in svg.strip().splitlines())
    return conteudo(titulo, corpo, sobrelinha, contexto, conclusao,
                    rotulo_conclusao, conclusao_clara=True, fonte=fonte,
                    por_passos=True)


def pratica(numero, tarefa, minutos, formato, entrega, checkpoint, passos, criterio,
            ambiente="Colab", trilho=True, sobrelinha=None) -> str:
    """Slide de pratica.

    `trilho=False` omite a faixa de tempo, formato, entrega e checkpoint. Serve
    para dividir uma pratica longa em dois slides: o primeiro enquadra e o
    segundo lista os passos com os prompts. Em 15/08 a turma leu uma pratica de
    cinco passos com prompt como se fosse um prompt unico, e como se fosse uma
    etapa unica.
    """
    linhas = []
    for i, passo in enumerate(passos, 1):
        detalhe = f'\n            <p class="detalhe">{passo["detalhe"]}</p>' if passo.get("detalhe") else ""
        prompt = f'\n            <code class="prompt-literal">{passo["prompt"]}</code>' if passo.get("prompt") else ""
        linhas.append(
            '          <div class="pratica-passo">\n'
            f'            <span class="num">{i:02d}</span>\n'
            "            <div>\n"
            f'              <p class="acao">{passo["acao"]}</p>{detalhe}{prompt}\n'
            "            </div>\n"
            "          </div>\n"
        )
    faixa = (
        '          <div class="pratica-trilho">\n'
        '            <div class="pratica-tempo">\n'
        f'              <p class="tempo">{minutos}</p>\n'
        '              <p class="tempo-unidade">minutos</p>\n'
        '            </div>\n'
        "            <dl>\n"
        f"              <dt>Formato</dt><dd>{formato}</dd>\n"
        f"              <dt>Entrega</dt><dd>{entrega}</dd>\n"
        f"              <dt>Checkpoint</dt><dd>{checkpoint}</dd>\n"
        "            </dl>\n"
        "          </div>\n"
    ) if trilho else ""
    if trilho:
        corpo = (
            '        <div class="pratica">\n' + faixa +
            '          <div class="pratica-passos">\n' + "".join(linhas) + "          </div>\n"
            "        </div>\n"
        )
    else:
        # `.pratica` e uma grade de duas colunas dimensionada para o trilho.
        # Sem ele os passos caiam na coluna estreita e o slide estourava por
        # 80 a 260px. Sem trilho, os passos usam a largura inteira, como no
        # bloco de checklist.
        corpo = (
            '        <div class="exercise-steps">\n' + "".join(linhas) + "        </div>\n"
        )
    return (
        '      <section class="exercise-slide">\n'
        '        <div class="top-bar"></div>\n'
        f"        {LOGO}\n"
        + _cabecalho(sobrelinha or f"Prática {numero} &middot; {minutos} minutos &middot; {ambiente}",
                     tarefa, None)
        + corpo
        + _fecho(criterio, "Critério de conclusão", True, None)
        + _rodape()
        + "      </section>\n"
    )


def quiz(sobrelinha, titulo, pergunta, opcoes, cenario) -> str:
    itens = []
    for letra, o in zip("ABCD", opcoes):
        itens.append(
            f'              <li data-letra="{letra}"\n'
            f'                  data-correct="{"true" if o["certa"] else "false"}"\n'
            f'                  data-correct-msg="{_html.escape(o["certo"], quote=True)}"\n'
            f'                  data-incorrect-msg="{_html.escape(o["errado"], quote=True)}">{o["texto"]}</li>\n'
        )
    fichas = "".join(
        f"              <dt>{d}</dt><dd>{v}</dd>\n" for d, v in cenario["fichas"]
    )
    corpo = (
        '        <div class="quiz-container">\n'
        '          <div class="quiz-grade">\n'
        "            <div>\n"
        f'              <p class="quiz-question">{pergunta}</p>\n'
        '              <ul class="quiz-options">\n' + "".join(itens) + "              </ul>\n"
        "            </div>\n"
        "            <div>\n"
        '              <dl class="quiz-cenario">\n' + fichas + "              </dl>\n"
        # O paragrafo ja existe no HTML: o JS preenche em vez de criar, senao o
        # layout salta no clique, ao vivo e projetado.
        '              <p class="quiz-feedback"></p>\n'
        "            </div>\n"
        "          </div>\n"
        "        </div>\n"
    )
    return (
        '      <section class="quiz-slide">\n'
        '        <div class="top-bar"></div>\n'
        f"        {LOGO}\n"
        + _cabecalho(sobrelinha, titulo, None)
        + corpo
        + _rodape()
        + "      </section>\n"
    )


def secao(numero, titulo, apoio, condicoes=None) -> str:
    blocos = ""
    if condicoes:
        itens = "".join(
            f'          <div><span class="num">{i:02d}</span>{c}</div>\n'
            for i, c in enumerate(condicoes, 1)
        )
        blocos = f'        <div class="secao-condicoes">\n{itens}        </div>\n'
    return (
        '      <section class="section-slide">\n'
        f'        <p class="secao-numero">{numero}</p>\n'
        '        <div class="accent-bar"></div>\n'
        f"        <h2>{titulo}</h2>\n"
        f"        <h3>{apoio}</h3>\n"
        + blocos
        + "      </section>\n"
    )


def montar(slides: list[str], esqueleto: str, saida: Path) -> int:
    """Escreve o deck e devolve o número da última página."""
    saida.write_text(esqueleto.format(slides="\n".join(slides)), encoding="utf-8")
    return _pagina
