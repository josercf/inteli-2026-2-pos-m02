# -*- coding: utf-8 -*-
"""
Gera as tres figuras da Aula 03 em assets/img/.

Todas partem de dados/datasets_case_modulo2.xlsx, o dataset oficial, atraves de
dados/analise_aula03.py. Os valores que cada figura desenha estao travados por
dados/tests/test_dataset_oficial.py.

O xlsx nao e versionado (ADR-005). Sem ele, este gerador falha com mensagem
explicita em vez de produzir figura vazia: figura de aula com eixo em branco
passa despercebida ate o projetor.

Convencao herdada da Aula 01: figura e governada pela LARGURA. Desenhadas em
1168px e renderizadas 1:1 no slide.

Uso: .venv/bin/python tools/gerar_figuras_aula03.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from tools.gerar_figuras_aula01 import (  # noqa: E402
    BRANCO, CINZA_CLARO, CINZA_ESCURO, CINZA_MEDIO, CORAL, DPI,
    LARGURA_FAIXA, ROXO, VERDE_ESCURO,
)
from dados import analise_aula03 as an  # noqa: E402

SAIDA = RAIZ / "assets" / "img"

ROTULO_SEGMENTO = {
    "PUBLIC SECTOR": "Setor público",
    "MID MARKET": "Mid market",
    "STRATEGIC ACCOUNT": "Estratégicas",
    "LARGE ENTERPRISE": "Grandes contas",
    "SMALL MARKET": "Small market",
    "GLOBAL ACCOUNT": "Contas globais",
}


def _fmt(valor: float, casas: int = 1) -> str:
    return f"{valor:,.{casas}f}".replace(",", "@").replace(".", ",").replace("@", ".")


def _estilo_eixo(ax) -> None:
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(CINZA_MEDIO)


def _figura(altura_px: int):
    fig = plt.figure(figsize=(LARGURA_FAIXA / DPI, altura_px / DPI), dpi=DPI)
    fig.patch.set_facecolor(BRANCO)
    return fig


def salvar(fig, nome: str) -> Path:
    destino = SAIDA / nome
    fig.savefig(destino, dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)
    return destino


# ---------------------------------------------------------------------------
# 1. A cauda da carteira
# ---------------------------------------------------------------------------

def distribuicao_receita() -> Path:
    """Histograma em log10 com media e mediana marcadas.

    Em escala linear a figura e uma barra unica colada no zero e um pixel a
    377 milhoes: com assimetria de 44, a escala linear nao desenha nada. O log
    e declarado no eixo, porque eixo transformado sem aviso engana quem le
    rapido.
    """
    c = an.contas()
    r = c.receita.clip(lower=1)
    medidas = an.receita_univariada()

    fig = _figura(400)
    ax = fig.add_axes([0.075, 0.28, 0.895, 0.52])
    _estilo_eixo(ax)

    ax.hist(np.log10(r), bins=60, color=CINZA_MEDIO, edgecolor=BRANCO, linewidth=0.6)
    for valor, cor, nome, desloc in (
        (medidas["mediana"], VERDE_ESCURO, "mediana", -0.30),
        (medidas["media"], CORAL, "média", 0.30),
    ):
        x = np.log10(max(valor, 1))
        ax.axvline(x, color=cor, linewidth=2.4)
        ax.text(x + desloc, ax.get_ylim()[1] * 0.92,
                f"{nome}\nUSD {_fmt(valor, 0)}", fontsize=15, color=cor,
                ha="center", va="top", weight="bold", linespacing=1.4)

    ax.set_xticks(range(0, 9))
    ax.set_xticklabels(["1", "10", "100", "1 mil", "10 mil", "100 mil",
                        "1 mi", "10 mi", "100 mi"], fontsize=14)
    ax.set_xlabel("receita acumulada da conta nos 24 meses, em dólares, escala logarítmica",
                  fontsize=15)
    ax.set_ylabel("contas", fontsize=15)
    ax.set_title("A média da receita fica 24 vezes acima da mediana",
                 fontsize=19, color=ROXO, loc="left", pad=14)
    ax.text(0.0, -0.34,
            f"8.282 contas. Assimetria {_fmt(medidas['assimetria'])}, "
            f"curtose {_fmt(medidas['curtose'], 0)}. O 1% do topo concentra "
            f"{_fmt(an.pareto()[0.01] * 100)}% da receita.",
            transform=ax.transAxes, fontsize=14, color=CINZA_ESCURO)
    return salvar(fig, "aula03-distribuicao-receita.png")


# ---------------------------------------------------------------------------
# 2. O corte que define o rotulo
# ---------------------------------------------------------------------------

def contingencia_rotulo() -> Path:
    """Contas por ultimo mes com receita, separadas pelo rotulo.

    A figura inteira existe para mostrar que so uma coluna tem as duas cores.
    """
    ct = an.contingencia_rotulo()
    meses = list(ct.index)
    ativas = ct[0].to_numpy()
    perdidas = ct[1].to_numpy()

    fig = _figura(400)
    ax = fig.add_axes([0.075, 0.28, 0.895, 0.53])
    _estilo_eixo(ax)

    x = np.arange(len(meses))
    ax.bar(x, perdidas, color=CORAL, label="rotuladas como perdidas", width=0.74)
    ax.bar(x, ativas, bottom=perdidas, color=CINZA_MEDIO, label="rotuladas como ativas",
           width=0.74)

    i = meses.index("2025-02")
    ax.annotate("único mês com as duas cores:\n111 perdidas e 382 ativas",
                xy=(i + 0.4, perdidas[i] + ativas[i] + 20), xytext=(i + 2.4, 720),
                fontsize=15, color=ROXO, weight="bold", linespacing=1.4,
                arrowprops=dict(arrowstyle="->", color=ROXO, linewidth=1.6))

    ax.set_xticks(x)
    ax.set_xticklabels([m if m.endswith(("-01", "-04", "-07", "-10")) else ""
                        for m in meses], fontsize=13, rotation=45, ha="right")
    ax.set_ylabel("contas", fontsize=15)
    ax.set_xlabel("último mês com receita registrada", fontsize=15, labelpad=8)
    ax.legend(fontsize=15, frameon=False, loc="upper left")
    ax.set_title("O rótulo separa as contas pelo último mês de compra",
                 fontsize=19, color=ROXO, loc="left", pad=14)
    return salvar(fig, "aula03-contingencia-rotulo.png")


# ---------------------------------------------------------------------------
# 3. Prevalencia contra receita
# ---------------------------------------------------------------------------

def prevalencia_por_segmento() -> Path:
    """Prevalencia de churn e participacao na receita, lado a lado.

    Duas barras por segmento, e nao um scatter: a leitura que a aula precisa e
    "onde as duas nao andam juntas", e isso se ve comparando alturas na mesma
    categoria.
    """
    t = an.prevalencia_por("segmento")
    nomes = [ROTULO_SEGMENTO[s] for s in t.index]
    prev = t.prevalencia.to_numpy() * 100
    receita = t.participacao_receita.to_numpy() * 100

    fig = _figura(400)
    ax = fig.add_axes([0.155, 0.26, 0.815, 0.50])
    _estilo_eixo(ax)

    y = np.arange(len(nomes))
    ax.barh(y - 0.20, prev, height=0.38, color=CORAL, label="prevalência de churn")
    ax.barh(y + 0.20, receita, height=0.38, color=VERDE_ESCURO,
            label="participação na receita")
    for yi, (p, r) in enumerate(zip(prev, receita)):
        ax.text(p + 0.6, yi - 0.20, f"{_fmt(p)}%", fontsize=14, color=CORAL,
                va="center", weight="bold")
        ax.text(r + 0.6, yi + 0.20, f"{_fmt(r)}%", fontsize=14, color=VERDE_ESCURO,
                va="center", weight="bold")

    ax.set_yticks(y)
    ax.set_yticklabels(nomes, fontsize=16)
    ax.invert_yaxis()
    ax.set_xlim(0, 36)
    ax.set_xlabel("por cento", fontsize=15)
    ax.legend(fontsize=15, frameon=False, loc="lower left",
              bbox_to_anchor=(0, 1.02), ncol=2, columnspacing=2.4)
    ax.set_title("O setor público reúne 31,2% de churn e 21,9% da receita",
                 fontsize=19, color=ROXO, loc="left", pad=46)
    ax.text(0.0, -0.32,
            "8.282 contas, das quais 1.593 rotuladas como perdidas. Prevalência medida no grão da conta.",
            transform=ax.transAxes, fontsize=14, color=CINZA_ESCURO)
    return salvar(fig, "aula03-prevalencia-segmento.png")


def main() -> None:
    if not an.XLSX.exists():
        raise SystemExit(
            f"{an.XLSX} não encontrado. O dataset oficial não é versionado (ADR-005): "
            "coloque o arquivo em dados/ antes de gerar as figuras."
        )
    for fn in (distribuicao_receita, contingencia_rotulo, prevalencia_por_segmento):
        destino = fn()
        print(f"  {destino.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
