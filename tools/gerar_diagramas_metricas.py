# -*- coding: utf-8 -*-
"""Gera os quatro diagramas de métrica da Aula 06, para embutir no slide.

Por que SVG embutido, e não imagem: o fragment do Reveal precisa alcançar cada
grupo de dentro da figura. Numerador, denominador e resultado aparecem no tempo
do professor, e não numa animação que roda sozinha. Vetor também imprime, e GIF
congela no primeiro quadro.

As cores não são literais aqui: o SVG usa classes e quem pinta é o tema, que
consome os tokens da marca. Assim o check_brand.py continua valendo depois que
o SVG entra no HTML.

Os números vêm da base longa, no limiar de 0,5, e estão travados em
dados/tests/test_diagramas_metricas.py.

Uso: PYTHONPATH=. .venv/bin/python tools/gerar_diagramas_metricas.py
"""

from __future__ import annotations

from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "assets" / "img"

# Matriz de confusão do escore de oito colunas no limiar de 0,5, sobre as 4.708
# contas elegíveis da base longa. Transcrita, e conferida contra a análise pelo
# teste: importar a função aqui faria o teste concordar consigo mesmo.
VP, FP, FN, VN = 2018, 643, 438, 1609
TOTAL = VP + FP + FN + VN

# O mesmo escore cortado pela capacidade operacional de 138 contas.
VP138, FP138, FN138 = 114, 24, 2342

# A altura foi de 348 para 300 depois que o validador reprovou os slides por
# 6px. Duas armadilhas apareceram no caminho, e as duas passam pelo validador
# de layout, que mede a caixa do <svg> e não o que está desenhado dentro dela:
#
# 1. Em 348, as linhas de rótulo caíam em y=342 e y=368, a segunda inteira fora
#    da viewBox.
# 2. Em 300 com célula de 84, a linha do numerador caía em y=308 e saía cortada
#    ao meio na projeção.
#
# A regra que resolve as duas: depois de mexer em Y0, CEL_A ou GAP, conferir que
# Y0 + CEL_A * 2 + GAP + 48 continua menor que ALTURA. O teste em
# dados/tests/test_diagramas_metricas.py cobra isso.
LARGURA, ALTURA = 1168, 300

# Grade da matriz.
X0, Y0 = 250, 74
CEL_L, CEL_A = 240, 78
GAP = 12
PAINEL_X = 806
PAINEL_L = LARGURA - PAINEL_X


def _pct(x: float) -> str:
    return f"{x * 100:.1f}".replace(".", ",") + "%"


def _milhar(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def _celula(col: int, lin: int, sigla: str, nome: str, valor: int, acerto: bool) -> str:
    x = X0 + col * (CEL_L + GAP)
    y = Y0 + lin * (CEL_A + GAP)
    classe = "celula acerto" if acerto else "celula"
    return (
        f'  <g class="{classe}">\n'
        f'    <rect x="{x}" y="{y}" width="{CEL_L}" height="{CEL_A}" rx="10"/>\n'
        f'    <text class="sigla" x="{x + 16}" y="{y + 22}">{sigla}</text>\n'
        f'    <text class="valor" x="{x + 16}" y="{y + 52}">{_milhar(valor)}</text>\n'
        f'    <text class="legenda" x="{x + 16}" y="{y + 70}">{nome}</text>\n'
        "  </g>"
    )


def _realce(celulas: list[tuple[int, int]], classe: str, folga: int) -> str:
    partes = []
    for col, lin in celulas:
        x = X0 + col * (CEL_L + GAP) - folga
        y = Y0 + lin * (CEL_A + GAP) - folga
        partes.append(
            f'    <rect class="{classe}" x="{x}" y="{y}" '
            f'width="{CEL_L + folga * 2}" height="{CEL_A + folga * 2}" rx="12"/>'
        )
    return "\n".join(partes)


def _grade() -> str:
    """Cabeçalhos e as quatro caixas, sempre visíveis."""
    c0 = X0 + CEL_L / 2
    c1 = X0 + CEL_L + GAP + CEL_L / 2
    l0 = Y0 + CEL_A / 2
    l1 = Y0 + CEL_A + GAP + CEL_A / 2
    return "\n".join([
        f'  <text class="eixo" x="{X0}" y="26">O QUE ACONTECEU DE VERDADE</text>',
        f'  <text class="cabecalho" x="{c0:.0f}" y="60" text-anchor="middle">Perdeu a conta</text>',
        f'  <text class="cabecalho" x="{c1:.0f}" y="60" text-anchor="middle">Seguiu comprando</text>',
        f'  <text class="eixo" x="16" y="26">O QUE O MODELO DISSE</text>',
        f'  <text class="cabecalho" x="230" y="{l0 + 6:.0f}" text-anchor="end">Marcou</text>',
        f'  <text class="cabecalho" x="230" y="{l1 + 6:.0f}" text-anchor="end">Não marcou</text>',
        _celula(0, 0, "VP", "acertou o alarme", VP, True),
        _celula(1, 0, "FP", "alarme falso", FP, False),
        _celula(0, 1, "FN", "perda que passou", FN, False),
        _celula(1, 1, "VN", "acertou o silêncio", VN, True),
    ])


def _painel(formula: str, conta: str, resultado: str, rotulo: str) -> str:
    """Painel da direita, revelado como último passo."""
    x = PAINEL_X
    return "\n".join([
        f'  <g class="painel fragment">',
        f'    <rect x="{x}" y="{Y0}" width="{PAINEL_L - 16}" height="{CEL_A * 2 + GAP}" rx="10"/>',
        f'    <text class="formula" x="{x + 20}" y="{Y0 + 32}">{formula}</text>',
        f'    <text class="conta" x="{x + 20}" y="{Y0 + 58}">{conta}</text>',
        f'    <text class="resultado" x="{x + 20}" y="{Y0 + 122}">{resultado}</text>',
        f'    <text class="resultado-rotulo" x="{x + 20}" y="{Y0 + 148}">{rotulo}</text>',
        "  </g>",
    ])


def _svg(rotulo_aria: str, corpo: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGURA} {ALTURA}"\n'
        f'     class="matriz-confusao" role="img" aria-label="{rotulo_aria}">\n'
        f"{corpo}\n"
        "</svg>\n"
    )


def _diagrama_de_matriz(nome, aria, numerador, denominador,
                        rotulo_num, rotulo_den, formula, conta, resultado, rotulo) -> str:
    partes = [_grade()]
    partes.append(
        '  <g class="fragment">\n'
        + _realce(denominador, "realce-den", 7) + "\n"
        + f'    <text class="rotulo-den" x="16" y="{Y0 + CEL_A * 2 + GAP + 26}">'
        + f"{rotulo_den}</text>\n"
        "  </g>"
    )
    partes.append(
        '  <g class="fragment">\n'
        + _realce(numerador, "realce-num", 2) + "\n"
        + f'    <text class="rotulo-num" x="16" y="{Y0 + CEL_A * 2 + GAP + 48}">'
        + f"{rotulo_num}</text>\n"
        "  </g>"
    )
    partes.append(_painel(formula, conta, resultado, rotulo))
    return _svg(aria, "\n".join(partes))


def acuracia() -> tuple[str, str]:
    valor = (VP + VN) / TOTAL
    return "aula06-metrica-acuracia.svg", _diagrama_de_matriz(
        "acuracia", f"Acurácia: as duas caixas de acerto sobre as quatro, {_pct(valor)}",
        numerador=[(0, 0), (1, 1)],
        denominador=[(0, 0), (1, 0), (0, 1), (1, 1)],
        rotulo_num="Numerador: VP mais VN, as duas caixas em que o modelo acertou",
        rotulo_den="Denominador: as quatro caixas, ou seja, a carteira elegível inteira",
        formula="(VP + VN) dividido pelo total",
        conta=f"({_milhar(VP)} + {_milhar(VN)}) / {_milhar(TOTAL)}",
        resultado=_pct(valor), rotulo="ACURÁCIA")


def precisao() -> tuple[str, str]:
    valor = VP / (VP + FP)
    return "aula06-metrica-precisao.svg", _diagrama_de_matriz(
        "precisao", f"Precisão: acertos sobre tudo que o modelo marcou, {_pct(valor)}",
        numerador=[(0, 0)],
        denominador=[(0, 0), (1, 0)],
        rotulo_num="Numerador: VP, as contas marcadas que estavam mesmo se perdendo",
        rotulo_den="Denominador: a linha de cima, tudo que o modelo marcou",
        formula="VP dividido por (VP + FP)",
        conta=f"{_milhar(VP)} / {_milhar(VP + FP)}",
        resultado=_pct(valor), rotulo="PRECISÃO")


def revocacao() -> tuple[str, str]:
    valor = VP / (VP + FN)
    return "aula06-metrica-revocacao.svg", _diagrama_de_matriz(
        "revocacao", f"Revocação: acertos sobre todas as perdas reais, {_pct(valor)}",
        numerador=[(0, 0)],
        denominador=[(0, 0), (0, 1)],
        rotulo_num="Numerador: VP, as perdas que o modelo conseguiu enxergar",
        rotulo_den="Denominador: a coluna da esquerda, todas as perdas que existiram",
        formula="VP dividido por (VP + FN)",
        conta=f"{_milhar(VP)} / {_milhar(VP + FN)}",
        resultado=_pct(valor), rotulo="REVOCAÇÃO")


def _barra(y: int, rotulo: str, valor: float, baixa: bool = False) -> str:
    # A barra ia até 820 e o valor caía em 836, atrás do painel da direita,
    # que começa em 806. Os dois números da fila de 138 ficavam invisíveis.
    x, largura, altura = 300, 420, 26
    preenchida = max(6, int(largura * valor))
    classe = "barra baixa" if baixa else "barra"
    return "\n".join([
        f'    <text class="barra-rotulo" x="290" y="{y + 18}" text-anchor="end">{rotulo}</text>',
        f'    <rect class="barra-fundo" x="{x}" y="{y}" width="{largura}" height="{altura}" rx="6"/>',
        f'    <rect class="{classe}" x="{x}" y="{y}" width="{preenchida}" height="{altura}" rx="6"/>',
        f'    <text class="barra-valor" x="{x + largura + 16}" y="{y + 18}">{_pct(valor)}</text>',
    ])


def f1() -> tuple[str, str]:
    p = VP / (VP + FP)
    r = VP / (VP + FN)
    f = 2 * p * r / (p + r)
    p138 = VP138 / (VP138 + FP138)
    r138 = VP138 / (VP138 + FN138)
    f138 = 2 * p138 * r138 / (p138 + r138)
    media = (p138 + r138) / 2

    corpo = "\n".join([
        '  <text class="eixo" x="16" y="24">LIMIAR DE 0,5</text>',
        '  <g class="fragment">',
        _barra(36, "Precisão", p),
        _barra(70, "Revocação", r),
        "  </g>",
        '  <g class="fragment">',
        _barra(104, "F1", f),
        '    <text class="legenda" x="300" y="152">Com precisão e revocação parecidas, '
        "a média harmônica fica entre as duas.</text>",
        "  </g>",
        '  <text class="eixo" x="16" y="196">FILA DE 138 CONTAS</text>',
        '  <g class="fragment">',
        _barra(208, "Precisão", p138),
        _barra(242, "Revocação", r138, baixa=True),
        "  </g>",
        '  <g class="painel fragment">',
        f'    <rect x="{PAINEL_X}" y="190" width="{PAINEL_L - 16}" height="90" rx="10"/>',
        f'    <text class="formula" x="{PAINEL_X + 20}" y="218">Média simples: {_pct(media)}</text>',
        f'    <text class="resultado" x="{PAINEL_X + 20}" y="262">F1 {_pct(f138)}</text>',
        "  </g>",
    ])
    return "aula06-metrica-f1.svg", _svg(
        f"F1: {_pct(f)} no limiar de 0,5 e {_pct(f138)} na fila de 138", corpo)


def main() -> None:
    for gerar in (acuracia, precisao, revocacao, f1):
        nome, svg = gerar()
        (SAIDA / nome).write_text(svg, encoding="utf-8")
        print(f"{nome}: {len(svg)} bytes")


if __name__ == "__main__":
    main()
