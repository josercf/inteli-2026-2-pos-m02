# -*- coding: utf-8 -*-
"""
Gera as tres figuras da Aula 02 em assets/img/.

Todas partem de dados/kovan_painel_contas.csv, o painel COM as lacunas, que e
o mesmo que a turma recebe: nenhum numero desta aula e digitado a mao. Os
valores que cada figura desenha estao travados por
dados/tests/test_aula02_numeros.py, e este gerador nao importa essa suite (a
producao de um asset nao pode depender da suite de teste): a funcao
`visitas_por_segmento` esta replicada aqui, de forma identica ao teste.

Paleta, fontes e a convencao de 1168px de largura vem de
tools/gerar_figuras_aula01.py: figura e governada pela LARGURA, nunca pela
altura. Sao desenhadas em 1168px e renderizam 1:1 no slide.

Uso: python3 tools/gerar_figuras_aula02.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from tools.gerar_figuras_aula01 import (  # noqa: E402
    BRANCO,
    CINZA_CLARO,
    CINZA_ESCURO,
    CINZA_MEDIO,
    CORAL,
    DPI,
    LARGURA_FAIXA,
    ROXO,
    VERDE_ESCURO,
)

SAIDA = RAIZ / "assets" / "img"
CSV = RAIZ / "dados" / "kovan_painel_contas.csv"

SEGMENTOS = ("Cauda", "Estrategico", "Medio")


def _fmt(valor: float, casas: int = 2) -> str:
    """Numero no formato pt-BR: virgula decimal."""
    return f"{valor:.{casas}f}".replace(".", ",")


def _estilo_eixo(ax) -> None:
    """Espinhas e grade no padrao do acervo (ver gerar_figuras_aula01)."""
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(CINZA_MEDIO)


def salvar_png(fig, destino: Path) -> None:
    """Salva a figura com a largura exata da convencao (1168px, 1:1).

    Sem bbox_inches="tight": ele recorta a figura ao conteudo e o resultado
    deixa de bater com o figsize declarado, que e o que garante os 1168px.
    """
    fig.savefig(destino, dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


def visitas_por_segmento(df: pd.DataFrame, tratamento: str) -> pd.Series:
    """Visitas medias por segmento sob cada decisao de tratamento da ausencia.

    Replicada de dados/tests/test_aula02_numeros.py de forma identica: e o
    calculo que aquela suite trava, e esta figura precisa desenhar exatamente
    os mesmos numeros, sem depender do modulo de teste para produzi-los.
    """
    if tratamento == "zero":
        base = df.assign(v=df["visitas_registradas"].fillna(0))
    elif tratamento == "excluir":
        base = df.dropna(subset=["visitas_registradas"]).rename(
            columns={"visitas_registradas": "v"}
        )
    else:
        raise ValueError(f"tratamento desconhecido: {tratamento}")
    return base.groupby("segmento")["v"].mean()


# ---------------------------------------------------------------------------
# 1. A inversao do estrategico entre os dois tratamentos da ausencia
# ---------------------------------------------------------------------------

ALTURA_INVERSAO = 380

PAINEIS_INVERSAO = [
    ("zero", "Ausência vira zero"),
    ("excluir", "Excluir sem registro"),
]


def fig_inversao_segmentos(destino: Path) -> None:
    df = pd.read_csv(CSV)

    series = {trat: visitas_por_segmento(df, trat) for trat, _ in PAINEIS_INVERSAO}
    limite = max(s.max() for s in series.values()) * 1.22

    fig, eixos = plt.subplots(
        1, 2,
        figsize=(LARGURA_FAIXA / DPI, ALTURA_INVERSAO / DPI),
        dpi=DPI,
        sharex=True,
    )
    fig.patch.set_facecolor(BRANCO)

    for ax, (tratamento, titulo) in zip(eixos, PAINEIS_INVERSAO):
        ax.set_facecolor(BRANCO)
        serie = series[tratamento].sort_values()
        cores = [CORAL if segmento == "Estrategico" else ROXO for segmento in serie.index]
        posicoes = np.arange(len(serie))
        ax.barh(posicoes, serie.values, color=cores, height=0.56, zorder=3)
        ax.set_yticks(posicoes)
        ax.set_yticklabels(serie.index, fontsize=17)
        ax.set_xlim(0, limite)
        ax.set_title(titulo, fontsize=18, color=ROXO, loc="left", pad=12)
        ax.set_xlabel("visitas médias por conta-trimestre", fontsize=15)
        ax.grid(axis="x", color=CINZA_CLARO, linewidth=1, zorder=0)
        ax.set_axisbelow(True)
        _estilo_eixo(ax)
        ax.tick_params(axis="x", labelsize=14)
        for y, valor, cor in zip(posicoes, serie.values, cores):
            ax.text(valor + limite * 0.02, y, _fmt(valor), fontsize=15,
                     color=cor, va="center", weight="bold")

    fig.tight_layout(w_pad=4.0)
    salvar_png(fig, destino)


# ---------------------------------------------------------------------------
# 2. A mudanca de taxonomia em 2023Q1 quebra a serie de linhas de produto
# ---------------------------------------------------------------------------

ALTURA_TAXONOMIA = 420


def fig_quebra_taxonomia(destino: Path) -> None:
    from dados.gerar_painel_kovan import IDX, TRIMESTRES

    df = pd.read_csv(CSV)
    media = df.groupby("trimestre")["linhas_produto_ativas"].mean().reindex(TRIMESTRES)

    i_corte = IDX["2023Q1"]
    i_antes = IDX["2022Q4"]
    i_fim = IDX["2025Q4"]

    salto = media.iloc[i_corte] / media.iloc[i_antes] - 1
    queda = media.iloc[i_fim] / media.iloc[i_corte] - 1

    fig, ax = plt.subplots(
        figsize=(LARGURA_FAIXA / DPI, ALTURA_TAXONOMIA / DPI), dpi=DPI
    )
    fig.patch.set_facecolor(BRANCO)
    ax.set_facecolor(BRANCO)

    xs = np.arange(len(TRIMESTRES))
    ax.axvspan(i_corte - 0.5, i_corte + 0.5, color=CINZA_CLARO, zorder=0)
    ax.text(i_corte, media.max() + 0.32, "mudança de taxonomia", fontsize=14,
             color=ROXO, ha="center")

    ax.plot(xs, media.values, color=ROXO, linewidth=2.8, marker="o", markersize=6,
             zorder=3)

    ax.annotate(
        f"{_fmt(media.iloc[i_antes])} → {_fmt(media.iloc[i_corte])}\n({salto:+.1%})".replace(".", ","),
        xy=(i_corte, media.iloc[i_corte]),
        xytext=(i_antes - 1.1, media.iloc[i_corte] + 0.55),
        fontsize=14, color=CORAL, weight="bold", ha="left",
        arrowprops=dict(arrowstyle="-", color=CORAL, linewidth=1.6),
    )
    ax.annotate(
        f"{_fmt(media.iloc[i_corte])} → {_fmt(media.iloc[i_fim])}\n({queda:+.1%})".replace(".", ","),
        xy=(i_fim, media.iloc[i_fim]),
        xytext=(i_fim - 3.0, media.iloc[i_fim] - 0.95),
        fontsize=14, color=VERDE_ESCURO, weight="bold", ha="left",
        arrowprops=dict(arrowstyle="-", color=VERDE_ESCURO, linewidth=1.6),
    )

    ax.set_ylabel("linhas de produto ativas (média)", fontsize=13)
    ax.set_xticks(xs)
    ax.set_xticklabels(TRIMESTRES, fontsize=14, rotation=45, ha="right")
    ax.set_ylim(1.2, media.max() + 0.9)
    ax.set_xlim(-0.6, len(TRIMESTRES) - 0.4)
    ax.grid(axis="y", color=CINZA_CLARO, linewidth=1, zorder=0)
    ax.set_axisbelow(True)
    _estilo_eixo(ax)

    fig.tight_layout()
    salvar_png(fig, destino)


# ---------------------------------------------------------------------------
# 3. O mapa de ausencia: quais colunas faltam, em qual segmento, e o zero de
#    referencia de uma coluna sem lacuna
# ---------------------------------------------------------------------------

ALTURA_AUSENCIA = 380

COLUNAS_COM_LACUNA = [
    "receita_brl",
    "valor_medio_pedido_brl",
    "visitas_registradas",
    "interacoes_crm",
]
COLUNA_REFERENCIA = "pedidos"

ROTULOS_COLUNA = {
    "receita_brl": "receita_brl",
    "valor_medio_pedido_brl": "valor_medio_pedido_brl",
    "visitas_registradas": "visitas_registradas",
    "interacoes_crm": "interacoes_crm",
    "pedidos": "pedidos (referência, sem lacuna)",
}


def fig_mapa_ausencia(destino: Path) -> None:
    df = pd.read_csv(CSV)

    linhas = COLUNAS_COM_LACUNA + [COLUNA_REFERENCIA]
    matriz = pd.DataFrame(
        {
            segmento: [
                df.loc[df["segmento"] == segmento, coluna].isna().mean()
                for coluna in linhas
            ]
            for segmento in SEGMENTOS
        },
        index=linhas,
    )

    cmap = LinearSegmentedColormap.from_list("ausencia", [BRANCO, CORAL])

    fig, ax = plt.subplots(
        figsize=(LARGURA_FAIXA / DPI, ALTURA_AUSENCIA / DPI), dpi=DPI
    )
    fig.patch.set_facecolor(BRANCO)

    dados = matriz.values
    ax.imshow(dados, cmap=cmap, vmin=0, vmax=dados.max(), aspect="auto")

    ax.set_xticks(range(len(SEGMENTOS)))
    ax.set_xticklabels(SEGMENTOS, fontsize=16, color=ROXO)
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")

    ax.set_yticks(range(len(linhas)))
    ax.set_yticklabels([ROTULOS_COLUNA[c] for c in linhas], fontsize=15, color=ROXO)

    # Linha de separacao acima da referencia: ela nao mede o mesmo fenomeno que
    # as quatro de cima, e a separacao evita que alguem a leia como uma quinta
    # coluna com lacuna.
    ax.axhline(len(COLUNAS_COM_LACUNA) - 0.5, color=ROXO, linewidth=1.6)

    for i, linha in enumerate(linhas):
        for j, segmento in enumerate(SEGMENTOS):
            valor = matriz.loc[linha, segmento]
            cor_texto = BRANCO if valor > dados.max() * 0.55 else ROXO
            ax.text(j, i, f"{_fmt(valor * 100, 1)}%", ha="center", va="center",
                     fontsize=17, color=cor_texto, weight="bold")

    for lado in ax.spines.values():
        lado.set_visible(False)
    ax.tick_params(length=0)

    fig.tight_layout()
    salvar_png(fig, destino)


# ---------------------------------------------------------------------------

FIGURAS = {
    "aula02-inversao-segmentos.png": fig_inversao_segmentos,
    "aula02-quebra-taxonomia.png": fig_quebra_taxonomia,
    "aula02-mapa-ausencia.png": fig_mapa_ausencia,
}


def main() -> None:
    SAIDA.mkdir(parents=True, exist_ok=True)
    for nome, funcao in FIGURAS.items():
        alvo = SAIDA / nome
        funcao(alvo)
        print(f"{nome}: {alvo.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
