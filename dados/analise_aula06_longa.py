# -*- coding: utf-8 -*-
"""Números da Aula 06 sobre a base longa, de 65 meses.

A base de cinco anos chegou em 12/09/2026, no meio da aula. Ela renomeia
praticamente todas as colunas de cadastro e de pedido, então este módulo tem
carregador próprio em vez de reaproveitar o da Aula 03.

O rótulo desta base marca a conta cuja última compra é até 07/03/2024, o que
equivale a cerca de 30 meses de inatividade contados do fim do painel, em
2026-08. A partição fica:

    2021-04 .. 2024-03   janela de observação, 36 meses
    2024-04 .. 2026-08   janela do rótulo, 29 meses

Com 36 meses de observação cabe janela de 12 meses, que os 11 meses da base
curta não comportavam.

Cada número que aparece no deck está travado em
dados/tests/test_aula06_longa.py.

Uso: PYTHONPATH=. .venv/bin/python dados/analise_aula06_longa.py
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[1]
XLSX = RAIZ / "dados" / "datasets_case_modulo2_5yrs.xlsx"
CACHE = RAIZ / "dados" / ".cache_5yrs"

ABAS = {"painel": "Dataset 1", "mix": "Dataset 2", "engajamento": "Dataset 3",
        "cadastro": "Dataset 4", "pedidos": "raw data"}

INICIO_DO_PAINEL = "2021-04"
CORTE = "2024-03"
INICIO_DO_ROTULO = "2024-04"
FIM_DO_PAINEL = "2026-08"
MESES_DE_OBSERVACAO = 36
MESES_DE_ROTULO = 29
DATA_LIMITE_DO_ROTULO = "2024-03-07"

BLOCO_RECENTE = ("2024-01", "2024-03")
BLOCO_ANTERIOR = ("2023-10", "2023-12")
BLOCO_12M = ("2023-04", "2024-03")
BLOCO_12M_ANTERIOR = ("2022-04", "2023-03")


class DatasetAusente(FileNotFoundError):
    """O xlsx longo não está em dados/. Não é erro de código."""


def _meses_entre(inicio: str, fim: str) -> int:
    ay, am = (int(p) for p in inicio.split("-"))
    by, bm = (int(p) for p in fim.split("-"))
    return (by - ay) * 12 + (bm - am)


@lru_cache(maxsize=1)
def carregar() -> dict[str, pd.DataFrame]:
    """Lê as cinco abas, com cache local em pickle.

    O xlsx tem 69 MB e a aba de pedidos tem 492.393 linhas: ler direto custa
    mais de um minuto, e em sala isso é tempo de projetor parado.
    """
    # Pasta existente e vazia não é cache: a primeira tentativa criou a pasta
    # e morreu antes de escrever, e o guarda por pasta transformou isso em
    # FileNotFoundError em vez de reler o xlsx.
    if all((CACHE / f"{nome}.pkl").exists() for nome in ABAS):
        return {nome: pd.read_pickle(CACHE / f"{nome}.pkl") for nome in ABAS}
    if not XLSX.exists():
        raise DatasetAusente(
            f"{XLSX} não encontrado. A base longa não é versionada (ADR-005): "
            "peça o arquivo pelo canal da turma e coloque-o em dados/.")
    xl = pd.ExcelFile(XLSX)
    dados = {nome: xl.parse(aba) for nome, aba in ABAS.items()}
    CACHE.mkdir(exist_ok=True)
    for nome, df in dados.items():
        df.to_pickle(CACHE / f"{nome}.pkl")
    return dados


def _wilson(k: int, n: int) -> tuple[float, float, float]:
    lo, hi = stats.binomtest(int(k), int(n)).proportion_ci(method="wilson")
    return k / n, float(lo), float(hi)


def auc(valores: pd.Series, alvo: pd.Series) -> float:
    a = valores[alvo == 1].to_numpy(dtype=float)
    b = valores[alvo == 0].to_numpy(dtype=float)
    u = stats.mannwhitneyu(a, b, alternative="two-sided").statistic
    return float(u / (len(a) * len(b)))


@lru_cache(maxsize=1)
def _pedidos() -> pd.DataFrame:
    ped = carregar()["pedidos"].copy()
    ped["billing_dt"] = pd.to_datetime(ped["billing_dt"])
    return ped


@lru_cache(maxsize=1)
def contas() -> pd.DataFrame:
    d = carregar()
    painel = d["painel"]
    c = painel.groupby("account_id").agg(
        churn=("churn_label", "max"),
        segmento=("segment", "first"),
        pais=("country", "first"),
        receita=("receita_usd", "sum"),
        meses_ativos=("periodo", "nunique"),
        ultimo_mes=("periodo", "max"),
        primeiro_mes=("periodo", "min"),
    )
    cad = d["cadastro"].drop_duplicates("account_id").set_index("account_id")
    return c.join(cad[["industry", "tempo_como_cliente", "canal_aquisicao"]])


@lru_cache(maxsize=1)
def painel_de_features() -> pd.DataFrame:
    c = contas()
    d = carregar()
    painel, ped = d["painel"], _pedidos()

    elegivel = c[c.primeiro_mes <= CORTE].copy()
    idx = elegivel.index

    obs = painel[painel.periodo <= CORTE]
    pos = painel[painel.periodo >= INICIO_DO_ROTULO]
    ped_obs = ped[ped.periodo <= CORTE]

    def por_conta(serie, preencher=0.0):
        return serie.reindex(idx).fillna(preencher)

    ultimo_obs = obs.groupby("account_id").periodo.max()
    elegivel["recencia_corte"] = por_conta(
        ultimo_obs.map(lambda m: _meses_entre(m, CORTE)), MESES_DE_OBSERVACAO)
    elegivel["recencia_fim"] = elegivel.ultimo_mes.map(
        lambda m: _meses_entre(m, FIM_DO_PAINEL))

    elegivel["freq_meses"] = por_conta(obs.groupby("account_id").periodo.nunique())
    elegivel["freq_dias"] = por_conta(
        ped_obs.groupby("account_id")["billing_dt"].nunique())
    elegivel["freq_meses_painel"] = elegivel.meses_ativos

    elegivel["valor_obs"] = por_conta(obs.groupby("account_id").receita_usd.sum())
    elegivel["valor_painel"] = elegivel.receita
    elegivel["ticket_medio"] = np.where(
        elegivel.freq_dias > 0, elegivel.valor_obs / elegivel.freq_dias.clip(lower=1), 0.0)

    def soma_bloco(bloco):
        ini, fim = bloco
        faixa = obs[(obs.periodo >= ini) & (obs.periodo <= fim)]
        return por_conta(faixa.groupby("account_id").receita_usd.sum())

    def razao(recente, anterior):
        num = soma_bloco(recente).to_numpy(dtype=float)
        den = soma_bloco(anterior).to_numpy(dtype=float)
        r = np.divide(num, den, out=np.ones(len(elegivel)), where=den > 0)
        return np.clip(r, 0, 10)

    elegivel["receita_3m"] = soma_bloco(BLOCO_RECENTE)
    elegivel["receita_3m_anterior"] = soma_bloco(BLOCO_ANTERIOR)
    elegivel["razao_3m"] = razao(BLOCO_RECENTE, BLOCO_ANTERIOR)
    # A janela de 12 meses só existe nesta base: 11 meses de observação não a
    # comportavam.
    elegivel["razao_12m"] = razao(BLOCO_12M, BLOCO_12M_ANTERIOR)

    elegivel["marcas_obs"] = por_conta(
        ped_obs.groupby("account_id").brand_lenovo.nunique())
    elegivel["meses_ativos_pos_corte"] = por_conta(
        pos.groupby("account_id").periodo.nunique())
    return elegivel


FEATURES_HONESTAS = ["recencia_corte", "freq_meses", "freq_dias", "valor_obs",
                     "ticket_medio", "razao_3m", "razao_12m", "marcas_obs"]

CANDIDATAS = [
    ("recencia_fim", "Recência no fim do painel", "painel inteiro"),
    ("freq_meses_painel", "Meses ativos no painel inteiro", "painel inteiro"),
    ("valor_painel", "Receita do painel inteiro", "painel inteiro"),
    ("recencia_corte", "Recência no corte", "janela de observação"),
    ("freq_meses", "Meses ativos até o corte", "janela de observação"),
    ("freq_dias", "Dias com pedido até o corte", "janela de observação"),
    ("valor_obs", "Receita até o corte", "janela de observação"),
    ("ticket_medio", "Ticket médio até o corte", "janela de observação"),
    ("razao_3m", "Razão de 3 meses", "janela de observação"),
    ("razao_12m", "Razão de 12 meses", "janela de observação"),
    ("marcas_obs", "Marcas distintas até o corte", "janela de observação"),
]


def do_evento_a_conta() -> dict[str, int]:
    d = carregar()
    return {
        "itens_de_pedido": len(d["pedidos"]),
        "linhas_de_painel": len(d["painel"]),
        "contas_na_carteira": int(d["painel"].account_id.nunique()),
        "contas_elegiveis": len(painel_de_features()),
        "colunas_de_entrada": len(FEATURES_HONESTAS),
    }


def particao_temporal() -> dict:
    e = painel_de_features()
    c = contas()
    return {
        "inicio_painel": INICIO_DO_PAINEL, "corte": CORTE,
        "inicio_rotulo": INICIO_DO_ROTULO, "fim_painel": FIM_DO_PAINEL,
        "meses_observacao": MESES_DE_OBSERVACAO, "meses_rotulo": MESES_DE_ROTULO,
        "carteira": len(c), "perdidas_carteira": int(c.churn.sum()),
        "contas": len(e), "perdidas": int(e.churn.sum()),
        "prevalencia": float(e.churn.mean()),
        "nao_elegiveis": len(c) - len(e),
    }


def auc_das_candidatas() -> pd.DataFrame:
    e = painel_de_features()
    linhas = []
    for coluna, rotulo, janela in CANDIDATAS:
        a = auc(e[coluna], e.churn)
        linhas.append({"coluna": coluna, "variavel": rotulo, "janela": janela,
                       "auc": a, "auc_orientada": max(a, 1 - a)})
    return pd.DataFrame(linhas).set_index("coluna")


def concordancia_do_vazamento(meses: int = 30) -> dict:
    e = painel_de_features()
    previsto = (e.recencia_fim >= meses).astype(int)
    iguais = int((previsto == e.churn).sum())
    return {"contas": len(e), "meses": meses, "iguais": iguais,
            "concordancia": iguais / len(e), "auc": auc(e.recencia_fim, e.churn)}


def _logistica(X, y, iteracoes=60, ridge=1e-6):
    beta = np.zeros(X.shape[1])
    for _ in range(iteracoes):
        p = 1 / (1 + np.exp(-np.clip(X @ beta, -500, 500)))
        w = np.clip(p * (1 - p), 1e-9, None)
        H = X.T @ (X * w[:, None]) + ridge * np.eye(X.shape[1])
        passo = np.linalg.solve(H, X.T @ (y - p) - ridge * beta)
        beta = beta + passo
        if np.max(np.abs(passo)) < 1e-8:
            break
    return beta


def _matriz(features=None):
    e = painel_de_features()
    colunas = features or FEATURES_HONESTAS
    bruto = e[colunas].to_numpy(dtype=float)
    z = (bruto - bruto.mean(axis=0)) / bruto.std(axis=0)
    return e, colunas, np.column_stack([np.ones(len(z)), z])


def pesos_do_modelo(features=None) -> pd.DataFrame:
    e, colunas, X = _matriz(features)
    beta = _logistica(X, e.churn.to_numpy(dtype=float))
    t = pd.DataFrame({"coeficiente": beta[1:], "razao_de_chances": np.exp(beta[1:])},
                     index=colunas)
    t["peso_relativo"] = t.coeficiente.abs() / t.coeficiente.abs().sum()
    t["auc_isolada"] = [max(a, 1 - a) for a in (auc(e[c], e.churn) for c in colunas)]
    return t.sort_values("peso_relativo", ascending=False)


def escore(features=None) -> pd.Series:
    e, _, X = _matriz(features)
    beta = _logistica(X, e.churn.to_numpy(dtype=float))
    return pd.Series(1 / (1 + np.exp(-np.clip(X @ beta, -500, 500))), index=e.index)


def qualidade_do_modelo(features=None) -> dict:
    e, colunas, _ = _matriz(features)
    a = auc(escore(features), e.churn)
    return {"contas": len(e), "features": len(colunas), "auc": max(a, 1 - a)}


def lista_priorizada(n: int) -> dict:
    e = painel_de_features()
    ordem = escore().sort_values(ascending=False)
    marcadas = set(ordem.index[:n])
    previsto = e.index.isin(marcadas).astype(int)
    real = e.churn.to_numpy(dtype=int)
    vp = int(((previsto == 1) & (real == 1)).sum())
    fp = int(((previsto == 1) & (real == 0)).sum())
    fn = int(((previsto == 0) & (real == 1)).sum())
    vn = int(((previsto == 0) & (real == 0)).sum())
    return {"n": n, "limiar": float(ordem.iloc[n - 1]),
            "verdadeiros_positivos": vp, "falsos_positivos": fp,
            "falsos_negativos": fn, "verdadeiros_negativos": vn,
            "precisao": vp / (vp + fp), "revocacao": vp / (vp + fn),
            "acuracia": (vp + vn) / len(e)}


def main() -> None:
    p = particao_temporal()
    print(f"Painel {p['inicio_painel']} a {p['fim_painel']}, {p['carteira']} contas")
    print(f"Observação {p['inicio_painel']} a {p['corte']} ({p['meses_observacao']} meses), "
          f"rótulo {p['inicio_rotulo']} a {p['fim_painel']} ({p['meses_rotulo']} meses)")
    print(f"Elegíveis {p['contas']}, perdidas {p['perdidas']} ({p['prevalencia']:.1%}), "
          f"fora {p['nao_elegiveis']}")
    print()
    print(auc_das_candidatas().to_string())
    print()
    print(concordancia_do_vazamento())
    print()
    print(pesos_do_modelo().to_string())
    print()
    print("honesto", qualidade_do_modelo())
    print("vazado ", qualidade_do_modelo(FEATURES_HONESTAS + ["recencia_fim"]))
    print()
    print(do_evento_a_conta())


if __name__ == "__main__":
    main()
