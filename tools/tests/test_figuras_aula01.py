# -*- coding: utf-8 -*-
"""
Testes das figuras da Aula 01.

Uma figura errada nao quebra nada: ela e projetada na frente da turma com a cor
de outro segmento, com um quadro so, ou com um numero que nao existe mais no
dataset. Nenhuma dessas falhas aparece em log.

Rodar: python3 -m pytest tools/tests -q
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
from PIL import Image, ImageSequence

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from tools.gerar_figuras_aula01 import (  # noqa: E402
    BRANCO,
    CINZA_CLARO,
    CINZA_ESCURO,
    CINZA_MEDIO,
    CORAL,
    FIGURAS,
    ROXO,
    VERDE_ESCURO,
    QUADRO_MS,
    FINAL_MS,
    series_indexadas,
)

IMG = RAIZ / "assets" / "img"

# Paleta oficial do brandbook (p.66). O lilas e o verde claro pertencem a outros
# segmentos e nao podem aparecer numa figura deste acervo.
PALETA_EXEC = {ROXO, CORAL, VERDE_ESCURO, CINZA_ESCURO, CINZA_MEDIO, CINZA_CLARO, BRANCO}
OUTRO_SEGMENTO = {"#90a5e5", "#89cea5"}

GIFS = [n for n in FIGURAS if n.endswith(".gif")]
SVGS = [n for n in FIGURAS if n.endswith(".svg")]


@pytest.mark.parametrize("nome", list(FIGURAS))
def test_figura_existe(nome):
    assert (IMG / nome).exists(), f"rode tools/gerar_figuras_aula01.py: falta {nome}"


@pytest.mark.parametrize("nome", GIFS)
def test_gif_tem_mais_de_um_quadro(nome):
    """Um GIF de um quadro so e uma imagem estatica com extensao errada."""
    with Image.open(IMG / nome) as im:
        assert getattr(im, "is_animated", False), nome
        assert im.n_frames >= 3, (nome, im.n_frames)


@pytest.mark.parametrize("nome", GIFS)
def test_gif_toca_uma_vez_e_para(nome):
    """Em loop infinito a figura reinicia durante a discussao e disputa a
    atencao com quem esta falando. Ausencia da chave `loop` e o que produz
    "tocar uma vez" num GIF."""
    with Image.open(IMG / nome) as im:
        assert "loop" not in im.info, (nome, im.info.get("loop"))


@pytest.mark.parametrize("nome", GIFS)
def test_gif_tem_quadro_estatico_para_impressao(nome):
    """O PDF exportado congela o GIF no primeiro quadro, e o handout sai desse
    PDF: sem o PNG do ultimo quadro, o aluno recebe o grafico pela metade."""
    png = (IMG / nome).with_suffix(".png")
    assert png.exists(), png.name
    with Image.open(IMG / nome) as gif, Image.open(png) as estatico:
        assert estatico.size == gif.size, (gif.size, estatico.size)


@pytest.mark.parametrize("nome", GIFS)
def test_gif_segura_o_ultimo_quadro(nome):
    """O quadro final e onde esta a leitura: ele precisa durar mais que os outros."""
    with Image.open(IMG / nome) as im:
        duracoes = []
        for quadro in ImageSequence.Iterator(im):
            duracoes.append(quadro.info.get("duration", 0))
    assert duracoes[-1] > duracoes[0], (nome, duracoes)
    assert duracoes[-1] >= FINAL_MS * 0.9, (nome, duracoes[-1])
    assert duracoes[0] >= QUADRO_MS * 0.9, (nome, duracoes[0])


@pytest.mark.parametrize("nome", GIFS)
def test_gif_cabe_no_slide(nome):
    """A area util do slide e larga e baixa: figura alta demais estoura."""
    with Image.open(IMG / nome) as im:
        largura, altura = im.size
    assert largura >= 900, (nome, largura)
    assert largura / altura >= 1.7, (nome, largura / altura)


@pytest.mark.parametrize("nome", GIFS)
def test_gif_muda_de_um_quadro_para_o_outro(nome):
    """Protege contra o bug que ja aconteceu: todos os quadros saindo iguais.

    A primeira versao deste gerador usava FuncAnimation, que muta os artistas
    da figura no lugar; o GIF saia com a serie inteira ja desenhada em todos os
    quadros. O arquivo existia, tinha o numero certo de quadros e estava errado.
    """
    with Image.open(IMG / nome) as im:
        quadros = [q.convert("RGB").tobytes() for q in ImageSequence.Iterator(im)]
    distintos = len(set(quadros))
    assert distintos == len(quadros), (nome, distintos, len(quadros))


@pytest.mark.parametrize("nome", SVGS)
def test_svg_so_usa_a_paleta_do_segmento(nome):
    texto = (IMG / nome).read_text(encoding="utf-8")
    cores = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", texto)}
    fora = cores - {c.lower() for c in PALETA_EXEC}
    assert not fora, (nome, sorted(fora))
    assert not (cores & OUTRO_SEGMENTO), nome


@pytest.mark.parametrize("nome", SVGS)
def test_svg_tem_descricao_acessivel(nome):
    texto = (IMG / nome).read_text(encoding="utf-8")
    assert 'role="img"' in texto, nome
    rotulo = re.search(r'aria-label="([^"]+)"', texto)
    assert rotulo and len(rotulo.group(1)) > 40, nome


@pytest.mark.parametrize("nome", SVGS)
def test_svg_tem_viewbox_e_proporcao_de_slide(nome):
    texto = (IMG / nome).read_text(encoding="utf-8")
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', texto)
    assert vb, nome
    largura, altura = int(vb.group(1)), int(vb.group(2))
    assert largura / altura >= 1.7, (nome, largura / altura)


# ---------------------------------------------------------------------------
# A figura das duas contas sai do painel, nao de numeros digitados na figura
# ---------------------------------------------------------------------------


def test_series_das_contas_vem_do_painel_gerado():
    talvera, andira = series_indexadas()
    # As duas comecam indexadas em 100 no trimestre anterior ao episodio.
    assert talvera[0] == pytest.approx(100.0)
    assert andira[0] == pytest.approx(100.0)


def test_o_andira_cai_mais_e_mesmo_assim_se_recupera():
    """E o que a figura afirma. Se o dataset mudar e isso deixar de valer, a
    legenda do slide passa a dizer o contrario do que o grafico mostra."""
    talvera, andira = series_indexadas()
    vale_talvera = min(talvera)
    vale_andira = min(andira)
    assert vale_andira < vale_talvera, (vale_andira, vale_talvera)
    assert andira[-1] > 100, andira[-1]
    assert talvera[-1] < 70, talvera[-1]


def test_a_serie_do_talvera_para_antes_da_do_andira():
    """Ele encerra o contrato em janeiro de 2026, fora da janela do painel."""
    talvera, andira = series_indexadas()
    assert len(talvera) < len(andira)


# ---------------------------------------------------------------------------
# O SVG cabe dentro do proprio viewBox
# ---------------------------------------------------------------------------


def _bbox_do_svg(caminho: Path) -> tuple[float, float]:
    """(altura do viewBox, y final do conteudo), medidos num navegador real.

    getBBox so existe com o SVG renderizado: nao da para conferir isso lendo o
    arquivo, e foi por isso que o defeito passou. A arvore de hipoteses ficou
    publicada com viewBox de 350 e conteudo terminando em 376, cortando os
    quatro rotulos de coluna, que sao a carga util da figura. A caixa do <img>
    estava correta, entao nem o check_slides nem o olho no DOM pegavam.
    """
    import http.server
    import socketserver
    import threading

    from playwright.sync_api import sync_playwright

    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=str(RAIZ), **k)
    servidor = socketserver.TCPServer(("127.0.0.1", 0), handler)
    porta = servidor.server_address[1]
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            navegador = p.chromium.launch()
            pagina = navegador.new_page(viewport={"width": 1280, "height": 720})
            pagina.goto(f"http://127.0.0.1:{porta}/assets/img/{caminho.name}")
            pagina.wait_for_timeout(400)
            medida = pagina.evaluate(
                """() => {const s = document.querySelector('svg');
                   const vb = s.getAttribute('viewBox').split(' ').map(Number);
                   const bb = s.getBBox();
                   return [vb[3], bb.y + bb.height, vb[2], bb.x + bb.width];}"""
            )
            navegador.close()
    finally:
        servidor.shutdown()
    return medida


@pytest.mark.parametrize("nome", SVGS)
def test_svg_nao_corta_o_proprio_conteudo(nome):
    altura_vb, fim_y, largura_vb, fim_x = _bbox_do_svg(IMG / nome)
    assert fim_y <= altura_vb + 0.5, (nome, fim_y, altura_vb)
    assert fim_x <= largura_vb + 0.5, (nome, fim_x, largura_vb)


@pytest.mark.parametrize("nome", SVGS)
def test_conector_do_svg_alcanca_o_minimo_de_contraste(nome):
    """Elemento grafico que carrega significado sozinho precisa de 3:1 (WCAG).

    A regra vale para o conector, que e um traco sem preenchimento: e ele que
    diz de onde para onde a decomposicao vai, e cinza escuro sobre branco mede
    2,03:1. Nao vale para a borda de uma caixa que ja tem preenchimento
    proprio: ali a borda e acabamento, e quem separa a caixa do fundo e o
    preenchimento. Um teste que nao faz essa distincao reprova design correto.
    """
    texto = (IMG / nome).read_text(encoding="utf-8")
    conectores = re.findall(r'<path[^>]*fill="none"[^>]*>', texto)
    assert conectores, f"{nome}: nenhum conector encontrado"
    fracos = []
    for tag in conectores:
        traco = re.search(r'stroke="(#[0-9a-fA-F]{6})"', tag)
        if traco and traco.group(1).lower() in {CINZA_ESCURO.lower(), CINZA_MEDIO.lower()}:
            fracos.append(traco.group(1))
    assert not fracos, (nome, sorted(set(fracos)))
