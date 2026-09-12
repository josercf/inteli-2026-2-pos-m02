# -*- coding: utf-8 -*-
"""Gera os dois diagramas conceituais de hiperparâmetro da Aula 06.

O primeiro mostra por onde o hiperparâmetro entra no treino, e por que ele não
sai do dado. O segundo é o esquema de subajuste e sobreajuste, que explica para
que serve o botão.

O segundo é declaradamente um esquema: ele não tem número em eixo nenhum, e a
medição de verdade vive nos dois slides de tabela ao lado. Curva conceitual com
número desenhado seria dado inventado com cara de medição.

SVG embutido, e não imagem, pelo mesmo motivo dos outros diagramas do acervo: o
fragment do Reveal precisa alcançar cada grupo de dentro da figura.

Uso: PYTHONPATH=. .venv/bin/python tools/gerar_diagramas_hiperparametros.py
"""

from __future__ import annotations

from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "assets" / "img"

LARGURA, ALTURA = 1168, 300


def _svg(aria: str, corpo: str, defs: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGURA} {ALTURA}"\n'
        f'     class="diagrama-aula06" role="img" aria-label="{aria}">\n'
        f"{defs}{corpo}\n"
        "</svg>\n"
    )


PONTA = (
    "  <defs>\n"
    '    <marker id="ponta-hiper" viewBox="0 0 10 10" refX="9" refY="5"\n'
    '            markerWidth="6" markerHeight="6" orient="auto-start-reverse">\n'
    '      <path class="ponta" d="M 0 0 L 10 5 L 0 10 z"/>\n'
    "    </marker>\n"
    "  </defs>\n"
)


def _caixa(x, y, w, h, titulo, apoio, marca=None, escolhido=False, indice=None):
    classe = "fluxo escolhido" if escolhido else "fluxo"
    if indice is not None:
        classe += f'" data-fragment-index="{indice}'
        classe = classe.replace("fluxo", "fluxo fragment", 1)
    partes = [f'  <g class="{classe}">',
              f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>']
    if marca:
        partes.append(f'    <text class="fluxo-marca" x="{x + 14}" y="{y + 22}">{marca}</text>')
        base = y + 46
    else:
        base = y + 32
    partes.append(f'    <text class="fluxo-titulo" x="{x + 14}" y="{base}">{titulo}</text>')
    for i, linha in enumerate(apoio):
        partes.append(
            f'    <text class="fluxo-apoio" x="{x + 14}" y="{base + 22 + i * 18}">{linha}</text>')
    partes.append("  </g>")
    return "\n".join(partes)


def _seta(x1, y1, x2, y2, indice, retorno=False, rotulo=None, rx=None, ry=None):
    classe = "seta retorno fragment" if retorno else "seta fragment"
    if retorno:
        d = f"M {x1} {y1} C {x1} {y1 + 60} {x2} {y2 + 60} {x2} {y2}"
    else:
        d = f"M {x1} {y1} L {x2} {y2}"
    partes = [f'  <path class="{classe}" data-fragment-index="{indice}" d="{d}" '
              f'marker-end="url(#ponta-hiper)"/>']
    if rotulo:
        partes.append(f'  <text class="fluxo-apoio fragment" data-fragment-index="{indice}" '
                      f'x="{rx}" y="{ry}" text-anchor="middle">{rotulo}</text>')
    return "\n".join(partes)


def fluxo() -> tuple[str, str]:
    """Por onde o hiperparâmetro entra."""
    corpo = "\n".join([
        _caixa(0, 30, 236, 84, "Tabela de treino",
               ["3.295 contas", "8 colunas fechadas em 2024-03"],
               marca="VEM DO DADO", indice=1),
        _caixa(0, 150, 236, 84, "Hiperparâmetros",
               ["força da regularização,", "profundidade da árvore"],
               marca="VOCÊ ESCOLHE", escolhido=True, indice=2),
        _seta(240, 72, 316, 110, 3),
        _seta(240, 192, 316, 154, 3),
        _caixa(320, 92, 168, 84, "Ajuste", ["o algoritmo roda"], indice=3),
        _seta(492, 134, 556, 134, 4),
        _caixa(560, 92, 236, 84, "Parâmetros",
               ["8 coeficientes e o intercepto", "saem do ajuste"],
               marca="O MODELO APRENDE", indice=4),
        _seta(800, 134, 864, 134, 5),
        _caixa(868, 92, 236, 84, "Escore por conta",
               ["probabilidade entre 0 e 1"], indice=5),
        _caixa(868, 206, 236, 62, "Validação", ["1.413 contas separadas"], indice=6),
        _seta(986, 180, 986, 202, 6),
        _seta(866, 240, 240, 200, 7, retorno=True,
              rotulo="a validação diz qual botão girar, e o ciclo recomeça",
              rx=553, ry=292),
    ])
    return "aula06-hiper-fluxo.svg", _svg(
        "Onde o hiperparâmetro entra: ele é escolhido antes do ajuste, e a "
        "validação diz se a escolha foi boa", corpo, PONTA)


# ---------------------------------------------------------------------------
# Esquema de subajuste e sobreajuste
# ---------------------------------------------------------------------------

EIXO_X0, EIXO_X1 = 150, 780
EIXO_Y0, EIXO_Y1 = 60, 230
OTIMO = 0.42


def _ponto(t: float, curva: str) -> tuple[float, float]:
    """t de 0 (modelo simples) a 1 (modelo complexo)."""
    x = EIXO_X0 + t * (EIXO_X1 - EIXO_X0)
    if curva == "treino":
        # O erro de treino só cai conforme o modelo ganha liberdade.
        v = 0.92 - 0.82 * t ** 0.8
    else:
        # O de validação cai, encosta no mínimo e volta a subir.
        v = 0.92 - 1.55 * t + 1.75 * t ** 2
    y = EIXO_Y0 + (1 - v) * (EIXO_Y1 - EIXO_Y0)
    return x, y


def _caminho(curva: str) -> str:
    pontos = [_ponto(i / 40, curva) for i in range(41)]
    d = " ".join(f"{'M' if i == 0 else 'L'} {x:.1f} {y:.1f}"
                 for i, (x, y) in enumerate(pontos))
    return d


def curva_de_ajuste() -> tuple[str, str]:
    xo, _ = _ponto(OTIMO, "validacao")
    corpo = "\n".join([
        # Eixos
        f'  <path class="eixo-linha" d="M {EIXO_X0} {EIXO_Y0 - 14} L {EIXO_X0} {EIXO_Y1 + 14} '
        f'L {EIXO_X1 + 14} {EIXO_Y1 + 14}"/>',
        f'  <text class="eixo" x="{EIXO_X0 - 12}" y="{EIXO_Y0 - 4}" text-anchor="end">ERRO</text>',
        f'  <text class="eixo" x="{EIXO_X0}" y="{EIXO_Y1 + 38}">MODELO MAIS SIMPLES</text>',
        f'  <text class="eixo" x="{EIXO_X1 + 14}" y="{EIXO_Y1 + 38}" text-anchor="end">'
        "MODELO MAIS COMPLEXO</text>",
        # Curvas
        f'  <g class="fragment" data-fragment-index="1">',
        f'    <path class="curva treino" d="{_caminho("treino")}"/>',
        f'    <text class="fluxo-apoio" x="{EIXO_X1 + 20}" y="{_ponto(1.0, "treino")[1] + 5}">'
        "erro no treino</text>",
        "  </g>",
        f'  <g class="fragment" data-fragment-index="2">',
        f'    <path class="curva validacao" d="{_caminho("validacao")}"/>',
        f'    <text class="fluxo-titulo" x="{EIXO_X1 + 20}" y="{_ponto(1.0, "validacao")[1] + 5}">'
        "erro na validação</text>",
        "  </g>",
        # Ponto de equilibrio
        f'  <g class="fragment" data-fragment-index="3">',
        f'    <path class="marca-otimo" d="M {xo:.0f} {EIXO_Y0 - 14} L {xo:.0f} {EIXO_Y1 + 14}"/>',
        f'    <text class="zona-titulo" x="{xo:.0f}" y="{EIXO_Y0 - 22}" text-anchor="middle">'
        "onde o botão deve parar</text>",
        "  </g>",
        # Painel de leitura
        '  <g class="painel fragment" data-fragment-index="3">',
        '    <rect x="836" y="46" width="316" height="208" rx="10"/>',
        '    <text class="zona-titulo" x="856" y="76">À esquerda: subajuste</text>',
        '    <text class="zona-apoio" x="856" y="98">O modelo é simples demais e erra</text>',
        '    <text class="zona-apoio" x="856" y="116">nos dois conjuntos.</text>',
        '    <text class="zona-titulo" x="856" y="150">À direita: sobreajuste</text>',
        '    <text class="zona-apoio" x="856" y="172">Ele decora o treino e piora na</text>',
        '    <text class="zona-apoio" x="856" y="190">validação. A distância entre as</text>',
        '    <text class="zona-apoio" x="856" y="208">duas curvas é o sintoma.</text>',
        '    <text class="fluxo-marca" x="856" y="238">ESQUEMA, SEM ESCALA NUMÉRICA</text>',
        "  </g>",
    ])
    return "aula06-hiper-curva.svg", _svg(
        "Esquema de subajuste e sobreajuste: o erro de treino cai sempre e o de "
        "validação volta a subir", corpo)


def main() -> None:
    for gerar in (fluxo, curva_de_ajuste):
        nome, svg = gerar()
        (SAIDA / nome).write_text(svg, encoding="utf-8")
        print(f"{nome}: {len(svg)} bytes")


if __name__ == "__main__":
    main()
