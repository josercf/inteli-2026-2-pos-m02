# -*- coding: utf-8 -*-
"""
Gera os dois diagramas de ciclo da Aula 01 em SVG, para embutir no slide.

Por que SVG embutido, e nao GIF:

- Vetor. Os GIFs eram raster de 1168px renderizados 1:1 a 1280, mas o Reveal
  escala o palco inteiro: a 1920x1080 a figura era reamostrada em 1,5x. As
  outras figuras SVG do mesmo deck nao sofriam isso, e o deck tinha duas
  qualidades de imagem.
- Ritmo. Um GIF roda sozinho. Embutido, cada fase do ciclo e um <g> com classe
  `fragment`, e o professor avanca no proprio tempo. A medicao mostrou que a
  chance de o passo destacado coincidir com o que ele esta dizendo era de 1/6.
- Impressao. Vetor imprime; GIF congela no primeiro quadro.

As cores NAO sao literais aqui: o SVG usa classes e quem pinta e o tema, que
consome os tokens da marca. Assim o validador de fidelidade continua valendo
depois que o SVG entra no HTML, e o diagrama acompanha qualquer troca de
segmento.

Uso: python3 tools/gerar_diagramas_svg.py
"""

from __future__ import annotations

import math
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "assets" / "img"

LARGURA, ALTURA = 1168, 334

# Fluxo horizontal com retorno, e nao anel.
#
# A primeira versao punha as seis caixas numa elipse. Numa faixa de 1168 por
# 334 a elipse fica achatada, os arcos entre caixas vizinhas se cruzam e o
# rotulo central disputa espaco com as caixas laterais. Em fluxo horizontal a
# ordem de leitura ja e a ordem do processo, a faixa inteira e usada e o
# retorno ao inicio fica explicito numa curva so.
N = 6
GAP = 27
CAIXA_L = (LARGURA - GAP * (N - 1)) // N
CAIXA_A = 116
TOPO = 26
BASE_RETORNO = 296


def _posicoes(n: int) -> list[float]:
    """Coordenada x da borda esquerda de cada caixa."""
    return [i * (CAIXA_L + GAP) for i in range(n)]


def _setas(xs: list[float]) -> str:
    partes = []
    meio = TOPO + CAIXA_A / 2
    for i in range(len(xs) - 1):
        x1 = xs[i] + CAIXA_L
        x2 = xs[i + 1]
        partes.append(
            f'  <path class="arco" d="M {x1 + 4:.0f} {meio:.0f} L {x2 - 6:.0f} {meio:.0f}" '
            f'marker-end="url(#ponta)"/>'
        )
    # Retorno do ultimo ao primeiro, por baixo: e o que faz o processo ser
    # ciclo e nao lista.
    xi = xs[-1] + CAIXA_L / 2
    xf = xs[0] + CAIXA_L / 2
    y = TOPO + CAIXA_A
    partes.append(
        f'  <path class="arco retorno" d="M {xi:.0f} {y + 6:.0f} '
        f'C {xi:.0f} {BASE_RETORNO:.0f} {xf:.0f} {BASE_RETORNO:.0f} {xf:.0f} {y + 10:.0f}" '
        f'marker-end="url(#ponta)"/>'
    )
    return "\n".join(partes)


def _caixas(itens, xs) -> str:
    partes = []
    for i, (titulo, apoio, destaque) in enumerate(itens):
        x = xs[i]
        cx = x + CAIXA_L / 2
        classe = "fase fragment" + (" destaque" if destaque else "")
        # O titulo quebra em ate duas linhas: a caixa tem 158px de largura.
        palavras = titulo.split()
        if len(palavras) > 2:
            meio = len(palavras) // 2 + len(palavras) % 2
            linhas = [" ".join(palavras[:meio]), " ".join(palavras[meio:])]
        else:
            linhas = [titulo]
        textos = "".join(
            f'\n    <text class="fase-titulo" x="{cx:.0f}" y="{TOPO + 40 + k * 24:.0f}" '
            f'text-anchor="middle">{linha}</text>'
            for k, linha in enumerate(linhas)
        )
        partes.append(f"""  <g class="{classe}">
    <rect x="{x:.0f}" y="{TOPO}" width="{CAIXA_L}" height="{CAIXA_A}" rx="10"/>
    <text class="fase-num" x="{cx:.0f}" y="{TOPO + 22:.0f}" text-anchor="middle">{i + 1:02d}</text>{textos}
    <text class="fase-apoio" x="{cx:.0f}" y="{TOPO + CAIXA_A - 14:.0f}" text-anchor="middle">{apoio}</text>
  </g>""")
    return "\n".join(partes)


def _svg(itens, centro, sub) -> str:
    xs = _posicoes(len(itens))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGURA} {ALTURA}"
     class="diagrama-ciclo" role="img" aria-label="{centro}: {sub}">
  <defs>
    <marker id="ponta-{centro.split()[0].lower()}" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path class="ponta" d="M 0 0 L 10 5 L 0 10 z"/>
    </marker>
  </defs>
{_setas(xs).replace("url(#ponta)", f"url(#ponta-{centro.split()[0].lower()})")}
{_caixas(itens, xs)}
  <text class="centro-apoio" x="{LARGURA / 2:.0f}" y="{BASE_RETORNO + 26:.0f}"
        text-anchor="middle">{sub}</text>
</svg>
"""


CRISP = [
    ("Entendimento do negócio", "S1", True),
    ("Entendimento dos dados", "S1 a S3", True),
    ("Preparação dos dados", "S2 e S3", False),
    ("Modelagem", "S6", False),
    ("Avaliação", "S6 tarde", False),
    ("Implantação", "S7 e S8", False),
]

CICLO = [
    ("Pergunta de negócio", "você", True),
    ("Contexto: o schema", "você", True),
    ("Prompt com restrição", "você", True),
    ("Código", "a IA", False),
    ("Execução", "a máquina", False),
    ("Verificação e refutação", "você", True),
]

DIAGRAMAS = {
    "aula01-crisp-dm.svg": lambda: _svg(
        CRISP, "CRISP-DM", "as duas primeiras fases consomem 6 das 26 semanas"
    ),
    "aula01-ciclo-eda-ia.svg": lambda: _svg(
        CICLO, "EDA assistida por IA", "quatro dos seis passos continuam com você"
    ),
}


def main() -> None:
    for nome, gerar in DIAGRAMAS.items():
        alvo = SAIDA / nome
        alvo.write_text(gerar(), encoding="utf-8")
        print(f"{nome}: {alvo.stat().st_size} bytes")


if __name__ == "__main__":
    main()
