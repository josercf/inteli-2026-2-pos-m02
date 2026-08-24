# -*- coding: utf-8 -*-
"""Números da Aula 04, lidos do dataset oficial da Lenovo.

A aula testa hipóteses de causa do churn sobre a população que o rótulo
consegue marcar. O rótulo exige treze meses de inatividade e o painel cobre
24 meses: conta cuja primeira compra é posterior a 2025-02 não tem como ser
marcada. Toda tabela daqui roda sobre as elegíveis, salvo indicação.

Cada número que aparece no deck ou no material está transcrito de forma literal
em dados/tests/test_aula04_numeros.py.

Uso: .venv/bin/python dados/analise_aula04.py
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np
import pandas as pd
from scipy import stats

from dados.analise_aula03 import XLSX, carregar, contas  # noqa: F401

# Última primeira-compra que ainda deixa treze meses de painel pela frente.
ULTIMO_MES_ELEGIVEL = "2025-02"
CAPACIDADE_OPERACIONAL = 138
REGIOES_PRINCIPAIS = ("BR", "MX", "CO", "PE", "CL", "AR", "PA")

# O par da PBL. Apelidos no deck, ids reais só aqui e nas notas de condução.
CONTA_A = "CLI000269"   # seguiu comprando
CONTA_B = "CLI000264"   # foi marcada


def _wilson(k: int, n: int) -> tuple[float, float, float]:
    lo, hi = stats.binomtest(int(k), int(n)).proportion_ci(method="wilson")
    return k / n, float(lo), float(hi)


@lru_cache(maxsize=1)
def contas_enriquecidas() -> pd.DataFrame:
    d = carregar()
    c = contas().copy()
    ped = d["pedidos"].copy()
    ped["Order Date"] = pd.to_datetime(ped["Order Date"])
    por_conta = ped.sort_values("Order Date").groupby("account_id")["Order Date"]
    c["dias_de_compra"] = por_conta.nunique()
    c["intervalo_mediano"] = por_conta.apply(
        lambda s: s.drop_duplicates().diff().dt.days.median())
    mix = d["mix"]
    c["marcas"] = mix.groupby("account_id").Brand.nunique()
    c["marca_dominante"] = (mix.sort_values("pct_receita", ascending=False)
                            .drop_duplicates("account_id").set_index("account_id").Brand)
    c["elegivel"] = c.primeiro_mes <= ULTIMO_MES_ELEGIVEL
    c["faixa_marcas"] = c.marcas.clip(upper=4).astype(int).astype(str).replace("4", "4+")
    c["faixa_dias"] = pd.cut(c.dias_de_compra, [0, 1, 2, 5, 10**6],
                             labels=["1", "2", "3 a 5", "6+"]).astype(str)
    return c


def elegiveis() -> pd.DataFrame:
    c = contas_enriquecidas()
    return c[c.elegivel]


def regioes_principais() -> tuple[str, ...]:
    return REGIOES_PRINCIPAIS


def populacoes() -> dict[str, dict]:
    c = contas_enriquecidas()
    saida = {}
    for nome, mascara in (("carteira", np.ones(len(c), dtype=bool)),
                          ("elegiveis", c.elegivel.to_numpy()),
                          ("nao_elegiveis", (~c.elegivel).to_numpy())):
        s = c[mascara]
        prev, lo, hi = _wilson(int(s.churn.sum()), len(s))
        saida[nome] = {"contas": len(s), "perdidas": int(s.churn.sum()),
                       "prevalencia": prev, "ic_inferior": lo, "ic_superior": hi}
    return saida


def perfil_por_segmento() -> pd.DataFrame:
    e = elegiveis()
    t = e.groupby("segmento").agg(
        contas=("churn", "size"), perdidas=("churn", "sum"), prevalencia=("churn", "mean"),
        receita_mediana=("receita", "median"), dias_mediano=("dias_de_compra", "median"),
        marcas_mediana=("marcas", "median"), intervalo_mediano=("intervalo_mediano", "median"),
        marca_dominante=("marca_dominante", lambda s: s.mode().iloc[0]),
    )
    return t.sort_values("prevalencia", ascending=False)


def tabela_com_ic(coluna: str, df: pd.DataFrame | None = None):
    """Contingência com IC de Wilson por categoria e qui-quadrado da tabela."""
    df = elegiveis() if df is None else df
    t = df.groupby(coluna, observed=True).churn.agg(contas="size", perdidas="sum")
    ics = [_wilson(int(k), int(n)) for n, k in zip(t.contas, t.perdidas)]
    t["prevalencia"] = [p for p, _, _ in ics]
    t["ic_inferior"] = [lo for _, lo, _ in ics]
    t["ic_superior"] = [hi for _, _, hi in ics]
    qui2, p, gl, _ = stats.chi2_contingency(pd.crosstab(df[coluna], df.churn))
    return t, float(qui2), int(gl), float(p)


def estratificar(coluna_teste: str, valor_a, valor_b, estrato: str) -> pd.DataFrame:
    """Prevalência do grupo A contra o grupo B dentro de cada estrato.

    Para `marcas`, `valor_b` é um piso: 3 significa três ou mais marcas. Para
    `regiao`, `valor_b == "outros"` significa todas as regiões exceto `valor_a`.
    Estrato com menos de 30 contas em qualquer dos grupos fica de fora.
    """
    e = elegiveis()
    if coluna_teste == "marcas":
        grupo_a, grupo_b = e.marcas == valor_a, e.marcas >= valor_b
    elif coluna_teste == "regiao" and valor_b == "outros":
        grupo_a, grupo_b = e.regiao == valor_a, e.regiao != valor_a
    else:
        grupo_a, grupo_b = e[coluna_teste] == valor_a, e[coluna_teste] == valor_b
    linhas = {}
    for nome, g in e.groupby(estrato, observed=True):
        a, b = g[grupo_a.loc[g.index]], g[grupo_b.loc[g.index]]
        if len(a) < 30 or len(b) < 30:
            continue
        pa, loa, hia = _wilson(int(a.churn.sum()), len(a))
        pb, lob, hib = _wilson(int(b.churn.sum()), len(b))
        linhas[nome] = {"n_a": len(a), "prev_a": pa, "lo_a": loa, "hi_a": hia,
                        "n_b": len(b), "prev_b": pb, "lo_b": lob, "hi_b": hib}
    return pd.DataFrame.from_dict(linhas, orient="index")


def composicao_br() -> dict[str, float]:
    e = elegiveis()
    pesados = e.segmento.isin(["MID MARKET", "PUBLIC SECTOR"])
    return {"share_mid_public_br": float(pesados[e.regiao == "BR"].mean()),
            "share_mid_public_outros": float(pesados[e.regiao != "BR"].mean())}


def canal_e_constante() -> bool:
    return carregar()["cadastro"].canal_aquisicao.nunique() == 1


def engajamento_nas_elegiveis() -> dict[str, float]:
    contatos = carregar()["engajamento"].groupby("account_id").contatos_realizados.sum()
    e = elegiveis().join(contatos, how="inner")
    return {"contas_cobertas": len(e),
            "mediana_contatos_ativas": float(e[e.churn == 0].contatos_realizados.median()),
            "mediana_contatos_perdidas": float(e[e.churn == 1].contatos_realizados.median())}


def _receita_mensal() -> pd.DataFrame:
    painel = carregar()["painel"]
    return painel.pivot_table(index="account_id", columns="periodo",
                              values="receita_usd", aggfunc="sum").fillna(0)


def par_da_pbl() -> dict:
    """Contas que caíram igual e terminaram diferente.

    Candidata: receita do primeiro semestre do painel acima de 50 mil, segundo
    semestre abaixo de 30% do primeiro, seis ou mais meses ativos. O par é
    escolhido à mão entre as candidatas do mesmo segmento e região.
    """
    pm = _receita_mensal()
    meses = sorted(pm.columns)
    s1, s2 = pm[meses[:6]].sum(axis=1), pm[meses[6:12]].sum(axis=1)
    c = contas_enriquecidas().join(s1.rename("receita_semestre_1")).join(s2.rename("receita_semestre_2"))
    cand = c[(c.receita_semestre_1 > 50_000)
             & (c.receita_semestre_2 < 0.3 * c.receita_semestre_1)
             & (c.meses_ativos >= 6)]
    campos = ["segmento", "regiao", "primeiro_mes", "ultimo_mes", "churn", "marcas",
              "dias_de_compra", "meses_ativos", "receita_semestre_1", "receita_semestre_2"]
    return {"candidatas": len(cand), "ativas": int((cand.churn == 0).sum()),
            "perdidas": int(cand.churn.sum()),
            "conta_a": {k: (v.item() if hasattr(v, "item") else v) for k, v in c.loc[CONTA_A, campos].items()},
            "conta_b": {k: (v.item() if hasattr(v, "item") else v) for k, v in c.loc[CONTA_B, campos].items()},
            "series": pd.DataFrame({"conta_a": pm.loc[CONTA_A], "conta_b": pm.loc[CONTA_B]})}


def fila_por_segmento() -> pd.Series:
    e = elegiveis()
    return e[e.churn == 1].groupby("segmento").size().sort_values(ascending=False)


# ---------------------------------------------------------------------------
# Setores: o mapa dos 13, o padrão de rajada e a mega-conta de licitação
# ---------------------------------------------------------------------------

# A conta de governo que sozinha concentra a maior parte da receita perdida
# elegível: um ciclo único de compra que o rótulo lê como conta perdida. O id
# real fica aqui e nas notas de condução; o material a apelida de Conta C.
CONTA_C = "CLI002953"


def perfil_por_setor() -> pd.DataFrame:
    """Prevalência com IC e perfil de compra por setor, nas elegíveis."""
    t, _, _, _ = tabela_com_ic("setor")
    e = elegiveis()
    perfil = e.groupby("setor").agg(
        receita_mediana=("receita", "median"), dias_mediano=("dias_de_compra", "median"),
        marcas_mediana=("marcas", "median"), intervalo_mediano=("intervalo_mediano", "median"),
        marca_dominante=("marca_dominante", lambda s: s.mode().iloc[0]),
    )
    return t.join(perfil).sort_values("prevalencia", ascending=False)


def rajada_por_setor() -> pd.DataFrame:
    """Concentração temporal da compra, por setor, nas elegíveis.

    `pico` é a fração da receita da conta concentrada no melhor mês dela;
    `recorrentes` é a fração de contas do setor com seis ou mais meses ativos.
    Compra por edital deixa assinatura nas duas medidas.
    """
    pm = _receita_mensal()
    pico = (pm.max(axis=1) / pm.sum(axis=1).replace(0, np.nan)).rename("pico")
    e = elegiveis().join(pico)
    return e.groupby("setor").agg(
        contas=("churn", "size"), pico_mediano=("pico", "median"),
        recorrentes=("meses_ativos", lambda s: float((s >= 6).mean())),
    ).sort_values("pico_mediano", ascending=False)


def conta_c() -> dict:
    """A mega-conta de licitação, com a participação dela na receita perdida."""
    e = elegiveis()
    perdidas = e[e.churn == 1]
    c = e.loc[CONTA_C]
    return {"setor": c.setor, "segmento": c.segmento, "regiao": c.regiao,
            "receita": float(c.receita), "meses_ativos": int(c.meses_ativos),
            "dias_de_compra": int(c.dias_de_compra), "ultimo_mes": c.ultimo_mes,
            "churn": int(c.churn),
            "participacao_na_receita_perdida": float(c.receita / perdidas.receita.sum()),
            "receita_perdida_total": float(perdidas.receita.sum())}


def receita_perdida_por_setor(incluir_conta_c: bool = True) -> pd.Series:
    """Receita, em USD, das contas perdidas elegíveis, por setor."""
    e = elegiveis()
    perdidas = e[e.churn == 1]
    if not incluir_conta_c:
        perdidas = perdidas.drop(CONTA_C)
    return perdidas.groupby("setor").receita.sum().sort_values(ascending=False)


def setor_x_segmento() -> dict[str, int]:
    """O quanto o setor GOVERNMENT e o segmento PUBLIC SECTOR se cruzam.

    Setor vem do cadastro e segmento do painel: os dois recortes não coincidem,
    e a leitura do material precisa declarar isso antes de comparar."""
    c = contas_enriquecidas()
    return {"contas_government": int((c.setor == "GOVERNMENT").sum()),
            "government_em_public_sector": int(((c.setor == "GOVERNMENT")
                                                & (c.segmento == "PUBLIC SECTOR")).sum()),
            "contas_public_sector": int((c.segmento == "PUBLIC SECTOR").sum())}


# ---------------------------------------------------------------------------
# O corte por segmento: ritmo de recompra e o efeito de abandonar o corte único
# ---------------------------------------------------------------------------

def _meses_ativos_por_conta() -> pd.Series:
    """Lista ordenada dos meses com receita positiva de cada conta, como
    índice inteiro (ano vezes 12 mais mês), para medir silêncio em meses."""
    painel = carregar()["painel"]
    com_receita = painel[painel.receita_usd > 0].copy()
    m = com_receita.periodo.str[:4].astype(int) * 12 + com_receita.periodo.str[5:].astype(int)
    return com_receita.assign(m=m).groupby("account_id").m.apply(lambda s: sorted(s.unique()))


def gaps_de_retorno() -> pd.DataFrame:
    """Silêncios seguidos de retorno, em meses, por segmento.

    Cada observação é um intervalo entre dois meses com receita da mesma
    conta. A medida é censurada à direita: um silêncio longo só aparece aqui
    se o retorno coube nos 24 meses do painel, então os percentis subestimam
    o silêncio tolerável nos grupos de ciclo longo. `retornos_13_ou_mais`
    conta os silêncios de 13 meses ou mais que terminaram em recompra: contas
    que o corte oficial teria marcado como perdidas no meio do silêncio.
    """
    seq = _meses_ativos_por_conta()
    linhas = []
    for conta, meses in seq.items():
        for a, b in zip(meses, meses[1:]):
            linhas.append((conta, b - a))
    g = pd.DataFrame(linhas, columns=["account_id", "gap"])
    g = g.join(contas_enriquecidas()[["segmento"]], on="account_id")
    return g.groupby("segmento").gap.agg(
        gaps="size",
        p50="median",
        p75=lambda s: float(s.quantile(0.75)),
        p90=lambda s: float(s.quantile(0.90)),
        p95=lambda s: float(s.quantile(0.95)),
        maximo="max",
        retornos_13_ou_mais=lambda s: int((s >= 13).sum()),
    )


def corte_por_segmento(percentil: float = 0.95) -> pd.DataFrame:
    """O efeito de trocar o corte único de 13 meses por um corte por segmento.

    O corte sugerido é o teto do percentil dos silêncios com retorno, mais um
    mês de margem. Elegibilidade e fila são recalculadas sob o corte do
    próprio segmento: mudar o corte muda quem tem painel suficiente para ser
    marcado. `captura_do_oficial` mede quantas das contas do rótulo oficial,
    entre as elegíveis do corte novo, o corte novo mantém marcadas.
    """
    g = gaps_de_retorno()
    c = contas_enriquecidas()
    fim_ano, fim_mes = (int(p) for p in "2026-03".split("-"))
    fim = fim_ano * 12 + fim_mes
    prim = c.primeiro_mes.str[:4].astype(int) * 12 + c.primeiro_mes.str[5:].astype(int)
    linhas = {}
    for seg, row in g.iterrows():
        corte = int(np.ceil(row[f"p{int(percentil * 100)}"])) + 1
        sub = c[c.segmento == seg]
        eleg = sub[prim.loc[sub.index] <= fim - corte]
        fila = eleg[eleg.inatividade >= corte]
        oficial = eleg[eleg.churn == 1]
        capturadas = len(fila.index.intersection(oficial.index))
        linhas[seg] = {
            "corte_meses": corte, "elegiveis": len(eleg), "fila": len(fila),
            "fila_corte_13": int(sub[prim.loc[sub.index] <= fim - 13].churn.sum()),
            "captura_do_oficial": capturadas / len(oficial) if len(oficial) else float("nan"),
        }
    t = pd.DataFrame.from_dict(linhas, orient="index")
    return t.sort_values("fila", ascending=False)


def main() -> None:
    print("=== populações ===")
    for nome, v in populacoes().items():
        print(f"  {nome:14} {v['contas']:5} contas  {v['perdidas']:5} perdidas  "
              f"{v['prevalencia']:.3f} [{v['ic_inferior']:.3f}, {v['ic_superior']:.3f}]")
    print("\n=== perfil por segmento (elegíveis) ===")
    print(perfil_por_segmento().round(3).to_string())
    for col in ("segmento", "faixa_marcas", "faixa_dias", "setor"):
        t, q, gl, p = tabela_com_ic(col)
        print(f"\n=== {col}: qui2={q:.1f} gl={gl} p={p:.1e} ===")
        print(t.round(3).to_string())
    print("\n=== marcas 1 contra 3+, por segmento ===")
    print(estratificar("marcas", 1, 3, "segmento").round(3).to_string())
    print("\n=== marcas 1 contra 3+, por faixa de dias de compra ===")
    print(estratificar("marcas", 1, 3, "faixa_dias").round(3).to_string())
    print("\n=== BR contra outros, por segmento ===")
    print(estratificar("regiao", "BR", "outros", "segmento").round(3).to_string())
    p = par_da_pbl()
    print(f"\n=== PBL: {p['candidatas']} candidatas, {p['ativas']} ativas, {p['perdidas']} perdidas ===")
    print("  conta A", p["conta_a"])
    print("  conta B", p["conta_b"])
    print("\n=== fila por segmento ===")
    print(fila_por_segmento().to_string())
    print("\n=== perfil por setor (elegíveis) ===")
    print(perfil_por_setor().round(3).to_string())
    print("\n=== rajada por setor ===")
    print(rajada_por_setor().round(3).to_string())
    c = conta_c()
    print(f"\n=== Conta C: {c['participacao_na_receita_perdida']:.1%} da receita perdida ===")
    print(" ", c)
    print("\n=== receita perdida por setor, USD mi (com e sem a Conta C) ===")
    lado_a_lado = pd.DataFrame({"com": receita_perdida_por_setor() / 1e6,
                                "sem": receita_perdida_por_setor(False) / 1e6})
    print(lado_a_lado.round(1).to_string())
    print("\n=== setor x segmento ===")
    print(" ", setor_x_segmento())
    print("\n=== silêncios com retorno, por segmento ===")
    print(gaps_de_retorno().round(2).to_string())
    print("\n=== corte por segmento (p95 + 1) contra o corte único de 13 ===")
    print(corte_por_segmento().round(3).to_string())


if __name__ == "__main__":
    main()
