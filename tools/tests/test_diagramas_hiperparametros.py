# -*- coding: utf-8 -*-
"""Testes dos dois diagramas conceituais de hiperparâmetro.

As mesmas duas armadilhas dos diagramas de métrica valem aqui, e as duas passam
pelo tools/check_slides.py, que mede a caixa do <svg> e não o conteúdo dela:
texto fora da viewBox some sem erro, e elemento coberto por outro fica
invisível. Por isso a varredura de coordenadas se repete neste arquivo.

Rodar: PYTHONPATH=. .venv/bin/python -m pytest tools/tests/test_diagramas_hiperparametros.py -q
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
ARQUIVOS = ["aula06-hiper-fluxo.svg", "aula06-hiper-curva.svg"]


def _svg(nome: str) -> str:
    return (IMG / nome).read_text(encoding="utf-8")


def _viewbox(svg: str) -> tuple[float, float]:
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    assert m, "sem viewBox"
    return float(m.group(1)), float(m.group(2))


@pytest.mark.parametrize("nome", ARQUIVOS)
def test_o_arquivo_existe_e_e_svg(nome):
    svg = _svg(nome)
    assert svg.startswith("<svg") and 'class="diagrama-aula06"' in svg
    assert svg.rstrip().endswith("</svg>")


@pytest.mark.parametrize("nome", ARQUIVOS)
def test_nenhuma_cor_literal_no_svg(nome):
    svg = _svg(nome)
    assert not re.search(r"(?<!&)#[0-9a-fA-F]{3,8}\b", svg), nome
    assert "rgb(" not in svg and "hsl(" not in svg


@pytest.mark.parametrize("nome", ARQUIVOS)
def test_todo_texto_cabe_dentro_da_viewbox(nome):
    svg = _svg(nome)
    largura, altura = _viewbox(svg)
    fora = [(float(m.group(1)), float(m.group(2)))
            for m in re.finditer(r'<text[^>]*\bx="([\d.-]+)"[^>]*\by="([\d.-]+)"', svg)
            if not (10 <= float(m.group(2)) <= altura - 4
                    and 0 <= float(m.group(1)) <= largura)]
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


def test_o_fluxo_revela_em_sete_passos():
    """A figura existe para o professor contar a história em ordem. Sem passo,
    a turma lê o fim antes da primeira frase."""
    svg = _svg("aula06-hiper-fluxo.svg")
    indices = {m.group(1) for m in re.finditer(r'data-fragment-index="(\d+)"', svg)}
    assert indices == {"1", "2", "3", "4", "5", "6", "7"}


def test_o_fluxo_separa_o_que_voce_escolhe_do_que_o_modelo_aprende():
    svg = _svg("aula06-hiper-fluxo.svg")
    assert "VOCÊ ESCOLHE" in svg and "O MODELO APRENDE" in svg
    assert "VEM DO DADO" in svg
    # A caixa do hiperparâmetro é a única pintada, e é ela que carrega a ideia.
    assert svg.count('class="fluxo fragment escolhido"') == 1


def test_a_curva_se_declara_esquema():
    """Curva conceitual com número em eixo seria dado inventado com cara de
    medição. A figura precisa dizer que não tem escala, e não pode ter eixo
    numerado."""
    svg = _svg("aula06-hiper-curva.svg")
    assert "ESQUEMA, SEM ESCALA NUMÉRICA" in svg
    textos = re.findall(r"<text[^>]*>([^<]*)</text>", svg)
    numerados = [t for t in textos if re.fullmatch(r"[\d.,]+", t.strip())]
    assert not numerados, numerados


def test_a_curva_de_validacao_sobe_de_novo():
    """O U é o argumento da figura. Uma curva monótona não mostra sobreajuste."""
    from tools.gerar_diagramas_hiperparametros import _ponto

    # Atenção à inversão: o eixo vertical mede erro e cresce para cima, então
    # em coordenada de tela o menor erro é o MAIOR y. Escrever este teste na
    # direção intuitiva o fez reprovar contra uma curva correta.
    ys = [_ponto(i / 40, "validacao")[1] for i in range(41)]
    menor_erro = max(ys)
    assert ys[0] < menor_erro and ys[-1] < menor_erro
    assert 0 < ys.index(menor_erro) < len(ys) - 1
    # A de treino só melhora, ou seja, o y só cresce.
    yt = [_ponto(i / 40, "treino")[1] for i in range(41)]
    assert all(b >= a for a, b in zip(yt, yt[1:]))
    # E ela termina abaixo da de validação: o treino sempre parece melhor.
    assert yt[-1] > ys[-1]


@pytest.mark.parametrize("nome", ARQUIVOS)
def test_o_deck_embute_o_svg(nome):
    deck = DECK.read_text(encoding="utf-8")
    assinatura = re.search(r'aria-label="([^"]+)"', _svg(nome), re.S).group(1)
    # A aria-label do gerador quebra linha ao entrar no HTML indentado.
    primeira = assinatura.split("\n")[0].strip()
    assert primeira in deck, nome
    assert f'src="../assets/img/{nome}"' not in deck, f"{nome} entrou como <img>"
