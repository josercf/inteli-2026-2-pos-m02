# -*- coding: utf-8 -*-
"""Gera as seis figuras da Aula 04 em assets/img/.

Duas são didáticas, com semente fixa, para o conceito chegar antes do número.
Quatro saem do dataset oficial através de dados/analise_aula04.py, cujos valores
estão travados em dados/tests/test_aula04_numeros.py.

Figura é governada pela largura: 1168px, renderizada 1:1 no slide.

Uso: .venv/bin/python tools/gerar_figuras_aula04.py
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
    BRANCO, CINZA_CLARO, CINZA_ESCURO, CINZA_MEDIO, CORAL, ROXO, VERDE_ESCURO,
)
from tools.gerar_figuras_aula03 import ROTULO_SEGMENTO, _estilo_eixo, _figura, _fmt, salvar  # noqa: E402
from dados import analise_aula04 as an  # noqa: E402

MESES_CURTOS = {"01": "jan", "02": "fev", "03": "mar", "04": "abr", "05": "mai", "06": "jun",
                "07": "jul", "08": "ago", "09": "set", "10": "out", "11": "nov", "12": "dez"}


def _pct(v: float) -> str:
    return f"{_fmt(v * 100)}%"


def _barras_com_ic(ax, nomes, prev, lo, hi, cor, xlim=1.0):
    y = np.arange(len(nomes))
    ax.barh(y, prev, height=0.55, color=cor)
    ax.errorbar(prev, y, xerr=[prev - lo, hi - prev], fmt="none", ecolor=ROXO,
                elinewidth=2.2, capsize=6, capthick=2.2)
    for yi, (p, h) in enumerate(zip(prev, hi)):
        ax.text(h + 0.012, yi, _pct(p), fontsize=15, color=ROXO, va="center", weight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(nomes, fontsize=16)
    ax.invert_yaxis()
    ax.set_xlim(0, xlim)
    ax.set_xticks(np.linspace(0, xlim, 6))
    ax.set_xticklabels([_pct(v) for v in np.linspace(0, xlim, 6)], fontsize=14)


# ---------------------------------------------------------------------------
# Didática 1: IC que se cruzam e IC que não se cruzam
# ---------------------------------------------------------------------------

def ic_didatico() -> Path:
    """Dois pares de proporções. No primeiro, 30 contas de cada lado: os
    intervalos se cruzam e a diferença de 10 pontos não sustenta conclusão. No
    segundo, 600 contas de cada lado, a mesma diferença, e os intervalos se
    separam."""
    from scipy import stats
    pares = [("Grupo A, 30 contas", 12, 30), ("Grupo B, 30 contas", 9, 30),
             ("Grupo A, 600 contas", 240, 600), ("Grupo B, 600 contas", 180, 600)]
    nomes, prev, lo, hi = [], [], [], []
    for nome, k, n in pares:
        l, h = stats.binomtest(k, n).proportion_ci(method="wilson")
        nomes.append(nome); prev.append(k / n); lo.append(float(l)); hi.append(float(h))
    prev, lo, hi = map(np.array, (prev, lo, hi))

    fig = _figura(360)
    ax = fig.add_axes([0.21, 0.2, 0.76, 0.6])
    _estilo_eixo(ax)
    _barras_com_ic(ax, nomes, prev, lo, hi, [CINZA_MEDIO, CINZA_MEDIO, VERDE_ESCURO, VERDE_ESCURO], xlim=0.7)
    ax.axhline(1.5, color=CINZA_CLARO, linewidth=1.5)
    ax.set_title("A mesma diferença de 10 pontos, com 30 e com 600 contas por grupo",
                 fontsize=17, color=CINZA_ESCURO, loc="left", pad=14)
    ax.text(0.0, -0.3, "IC de 95% (Wilson). Quando os intervalos se cruzam, "
            "o ruído explica a diferença.", transform=ax.transAxes, fontsize=14, color=CINZA_ESCURO)
    return salvar(fig, "aula04-ic-didatico.png")


# ---------------------------------------------------------------------------
# Didática 2: uma associação que desaparece sob estratificação
# ---------------------------------------------------------------------------

def estratificacao_didatica() -> Path:
    """Grupo X perde mais que Y no total, e dentro de cada estrato os dois são
    iguais. O que muda entre X e Y é a composição por estrato. Números
    inteiros escolhidos à mão, sem aleatoriedade."""
    # (n_x, k_x, n_y, k_y) por estrato
    estratos = {"Estrato 1": (300, 240, 100, 80), "Estrato 2": (100, 20, 300, 60)}
    total_x = (sum(v[0] for v in estratos.values()), sum(v[1] for v in estratos.values()))
    total_y = (sum(v[2] for v in estratos.values()), sum(v[3] for v in estratos.values()))
    grupos = ["Total"] + list(estratos)
    px = [total_x[1] / total_x[0]] + [v[1] / v[0] for v in estratos.values()]
    py = [total_y[1] / total_y[0]] + [v[3] / v[2] for v in estratos.values()]

    fig = _figura(340)
    ax = fig.add_axes([0.13, 0.2, 0.84, 0.58])
    _estilo_eixo(ax)
    y = np.arange(len(grupos))
    ax.barh(y - 0.19, px, height=0.36, color=CORAL, label="grupo X")
    ax.barh(y + 0.19, py, height=0.36, color=VERDE_ESCURO, label="grupo Y")
    for yi, (a, b) in enumerate(zip(px, py)):
        ax.text(a + 0.01, yi - 0.19, _pct(a), fontsize=14, color=CORAL, va="center", weight="bold")
        ax.text(b + 0.01, yi + 0.19, _pct(b), fontsize=14, color=VERDE_ESCURO, va="center", weight="bold")
    ax.set_yticks(y); ax.set_yticklabels(grupos, fontsize=16); ax.invert_yaxis()
    ax.set_xlim(0, 1.0)
    ax.set_xticks(np.linspace(0, 1, 6)); ax.set_xticklabels([_pct(v) for v in np.linspace(0, 1, 6)], fontsize=14)
    ax.legend(fontsize=15, frameon=False, loc="lower left", bbox_to_anchor=(0, 1.02), ncol=2)
    ax.set_title("No total X perde 65% e Y perde 35%; dentro de cada estrato os dois perdem igual",
                 fontsize=17, color=CINZA_ESCURO, loc="left", pad=40)
    ax.text(0.0, -0.3, "X tem 300 contas no estrato 1 e 100 no 2; Y tem 100 e 300. A diferença do total é composição.",
            transform=ax.transAxes, fontsize=14, color=CINZA_ESCURO)
    return salvar(fig, "aula04-estratificacao-didatica.png")


# ---------------------------------------------------------------------------
# Real 1: prevalência por segmento nas elegíveis, com IC
# ---------------------------------------------------------------------------

def prevalencia_elegiveis() -> Path:
    t, qui2, gl, _ = an.tabela_com_ic("segmento")
    t = t.sort_values("prevalencia", ascending=False)
    nomes = [ROTULO_SEGMENTO[s] for s in t.index]
    fig = _figura(380)
    ax = fig.add_axes([0.17, 0.19, 0.8, 0.64])
    _estilo_eixo(ax)
    _barras_com_ic(ax, nomes, t.prevalencia.to_numpy(), t.ic_inferior.to_numpy(),
                   t.ic_superior.to_numpy(), CORAL, xlim=0.8)
    p = an.populacoes()["elegiveis"]
    n_estrategicas = int(t.loc["STRATEGIC ACCOUNT", "contas"])
    ax.axvline(p["prevalencia"], color=ROXO, linestyle="--", linewidth=1.6)
    ax.text(p["prevalencia"] + 0.01, -0.75, f"carteira elegível {_pct(p['prevalencia'])}",
            fontsize=14, color=ROXO)
    ax.set_title(f"Prevalência de churn por segmento, nas {_fmt(p['contas'], 0)} contas elegíveis",
                 fontsize=17, color=CINZA_ESCURO, loc="left", pad=30)
    ax.text(0.0, -0.26, f"IC de 95% (Wilson). Qui-quadrado {_fmt(qui2)}, {gl} graus de liberdade. "
            f"Estratégicas: {_fmt(n_estrategicas, 0)} contas.",
            transform=ax.transAxes, fontsize=14, color=CINZA_ESCURO)
    return salvar(fig, "aula04-prevalencia-elegiveis.png")


# ---------------------------------------------------------------------------
# Real 2: amplitude de mix, estratificada por frequência de compra
# ---------------------------------------------------------------------------

def marcas_por_dias() -> Path:
    t = an.estratificar("marcas", 1, 3, "faixa_dias").loc[["1", "2", "3 a 5", "6+"]]
    nomes = [f"{f} dia{'s' if f != '1' else ''} de compra" for f in t.index]
    fig = _figura(380)
    ax = fig.add_axes([0.22, 0.19, 0.75, 0.6])
    _estilo_eixo(ax)
    y = np.arange(len(nomes))
    for desloc, cor, rotulo, p, lo, hi in (
        (-0.19, CORAL, "uma marca", t.prev_a, t.lo_a, t.hi_a),
        (0.19, VERDE_ESCURO, "três ou mais marcas", t.prev_b, t.lo_b, t.hi_b),
    ):
        p, lo, hi = p.to_numpy(), lo.to_numpy(), hi.to_numpy()
        ax.barh(y + desloc, p, height=0.36, color=cor, label=rotulo)
        ax.errorbar(p, y + desloc, xerr=[p - lo, hi - p], fmt="none", ecolor=ROXO,
                    elinewidth=2, capsize=5, capthick=2)
        for yi, (v, h) in enumerate(zip(p, hi)):
            ax.text(h + 0.012, yi + desloc, _pct(v), fontsize=14, color=cor, va="center", weight="bold")
    ax.set_yticks(y); ax.set_yticklabels(nomes, fontsize=16); ax.invert_yaxis()
    ax.set_xlim(0, 1.05)
    ax.set_xticks(np.linspace(0, 1, 6)); ax.set_xticklabels([_pct(v) for v in np.linspace(0, 1, 6)], fontsize=14)
    ax.legend(fontsize=15, frameon=False, loc="lower left", bbox_to_anchor=(0, 1.02), ncol=2)
    ax.set_title("Em cada faixa de frequência, 1 marca e 3+ marcas perdem igual",
                 fontsize=17, color=CINZA_ESCURO, loc="left", pad=40)
    ax.text(0.0, -0.28, "Contas elegíveis, IC 95% (Wilson). Carteira toda: 1 marca perde 66,4%; 4+, 16,1%.",
            transform=ax.transAxes, fontsize=14, color=CINZA_ESCURO)
    return salvar(fig, "aula04-marcas-por-dias.png")


# ---------------------------------------------------------------------------
# Real 3: o par da PBL, série mensal lado a lado
# ---------------------------------------------------------------------------

def _plural(n: int, singular: str, plural: str) -> str:
    return singular if n == 1 else plural


def par_pbl() -> Path:
    p = an.par_da_pbl()
    s = p["series"] / 1000
    meses = list(s.index)
    rotulos = [f"{MESES_CURTOS[m[5:]]}/{m[2:4]}" for m in meses]
    rotulos_mostrados = [r if i % 2 == 0 else "" for i, r in enumerate(rotulos)]
    fig = _figura(400)
    ax = fig.add_axes([0.09, 0.22, 0.88, 0.5])
    _estilo_eixo(ax)
    x = np.arange(len(meses))
    ax.bar(x - 0.2, s.conta_a, width=0.4, color=VERDE_ESCURO, label="Conta A, seguiu na base")
    ax.bar(x + 0.2, s.conta_b, width=0.4, color=CORAL, label="Conta B, marcada como perdida")
    corte = meses.index("2025-02")
    ax.axvline(corte + 0.5, color=ROXO, linestyle="--", linewidth=1.6)
    ax.text(corte + 0.7, ax.get_ylim()[1] * 0.9, "corte do rótulo", fontsize=14, color=ROXO)
    ax.set_xticks(x); ax.set_xticklabels(rotulos_mostrados, fontsize=14, rotation=45, ha="right")
    ax.set_ylabel("receita mensal, USD mil", fontsize=14)
    ax.legend(fontsize=15, frameon=False, loc="lower left", bbox_to_anchor=(0, 1.03), ncol=2)
    ax.set_title("Duas contas caíram mais de 90%, mas só a conta B foi marcada como perdida",
                 fontsize=17, color=CINZA_ESCURO, loc="left", pad=34)
    a, b = p["conta_a"], p["conta_b"]
    marcas_a, dias_a = int(a["marcas"]), int(a["dias_de_compra"])
    marcas_b, dias_b = int(b["marcas"]), int(b["dias_de_compra"])
    ax.text(0.0, -0.34, f"GLOBAL ACCOUNT, Brasil. Conta A: {marcas_a} "
            f"{_plural(marcas_a, 'marca', 'marcas')}, {dias_a} dias de compra. "
            f"Conta B: {marcas_b} {_plural(marcas_b, 'marca', 'marcas')}, {dias_b} dias.",
            transform=ax.transAxes, fontsize=14, color=CINZA_ESCURO)
    return salvar(fig, "aula04-par-pbl.png")


# ---------------------------------------------------------------------------
# Real 4: fila por segmento contra a capacidade operacional
# ---------------------------------------------------------------------------

def fila_por_segmento() -> Path:
    f = an.fila_por_segmento()
    nomes = [ROTULO_SEGMENTO[s] for s in f.index]
    fig = _figura(360)
    ax = fig.add_axes([0.17, 0.2, 0.8, 0.62])
    _estilo_eixo(ax)
    y = np.arange(len(nomes))
    cores = [CORAL if v > an.CAPACIDADE_OPERACIONAL else VERDE_ESCURO for v in f]
    ax.barh(y, f.to_numpy(), height=0.55, color=cores)
    for yi, v in enumerate(f):
        ax.text(v + 8, yi, _fmt(v, 0), fontsize=15, color=ROXO, va="center", weight="bold")
    n_acima = int((f > an.CAPACIDADE_OPERACIONAL).sum())
    n_total = len(f)
    ax.axvline(an.CAPACIDADE_OPERACIONAL, color=ROXO, linestyle="--", linewidth=1.8)
    ax.text(an.CAPACIDADE_OPERACIONAL + 8, len(nomes) - 0.4,
            f"capacidade: {an.CAPACIDADE_OPERACIONAL} planos por trimestre",
            fontsize=14, color=ROXO)
    ax.set_yticks(y); ax.set_yticklabels(nomes, fontsize=16); ax.invert_yaxis()
    ax.set_xlim(0, 800)
    ax.set_xlabel("contas marcadas como perdidas, entre as elegíveis", fontsize=14)
    ax.set_title(f"{n_acima} dos {n_total} segmentos ultrapassam sozinhos a capacidade de "
                 f"{an.CAPACIDADE_OPERACIONAL} planos",
                 fontsize=17, color=CINZA_ESCURO, loc="left", pad=14)
    return salvar(fig, "aula04-fila-por-segmento.png")


def main() -> None:
    if not an.XLSX.exists():
        raise SystemExit(f"{an.XLSX} não encontrado. O dataset oficial não é versionado (ADR-005).")
    for fn in (ic_didatico, estratificacao_didatica, prevalencia_elegiveis,
               marcas_por_dias, par_pbl, fila_por_segmento):
        print(f"  {fn().relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
