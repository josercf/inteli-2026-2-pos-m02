# -*- coding: utf-8 -*-
"""Números da Aula 06, lidos do dataset oficial da Lenovo.

A aula constrói as variáveis de entrada do modelo. O rótulo da Aula 03 exige
treze meses de inatividade num painel de 24 meses que termina em 2026-03: quem
comprou pela última vez até 2025-02 está marcado. Isso parte o painel em dois
pedaços que não podem se misturar:

    2024-04 .. 2025-02   janela de observação, 11 meses, de onde saem as features
    2025-03 .. 2026-03   janela do rótulo, 13 meses, de onde sai o alvo

Feature calculada sobre o painel inteiro atravessa esse corte e carrega o
próprio rótulo dentro dela. A demonstração da aula é medir a AUC univariada de
cada candidata dos dois lados do corte.

Cada número que aparece no deck está transcrito de forma literal em
dados/tests/test_aula06_numeros.py.

Uso: .venv/bin/python dados/analise_aula06.py
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np
import pandas as pd
from scipy import stats

from dados.analise_aula03 import FIM_DO_PAINEL, carregar, contas  # noqa: F401

INICIO_DO_PAINEL = "2024-04"
CORTE = "2025-02"            # último mês da janela de observação
INICIO_DO_ROTULO = "2025-03"
MESES_DE_OBSERVACAO = 11
MESES_DE_ROTULO = 13

# Blocos de três meses usados na variável de sequência.
BLOCO_RECENTE = ("2024-12", "2025-02")
BLOCO_ANTERIOR = ("2024-09", "2024-11")


def _meses_entre(inicio: str, fim: str) -> int:
    ay, am = (int(p) for p in inicio.split("-"))
    by, bm = (int(p) for p in fim.split("-"))
    return (by - ay) * 12 + (bm - am)


def auc(valores: pd.Series, alvo: pd.Series) -> float:
    """AUC univariada pela estatística de Mann-Whitney.

    A AUC de uma variável isolada é a probabilidade de uma conta perdida
    receber valor maior que uma conta mantida, empate contando meio. É o mesmo
    número que uma regressão logística de uma variável só produziria, sem
    precisar treinar nada, e é o que deixa o vazamento visível em uma linha.
    """
    a = valores[alvo == 1].to_numpy(dtype=float)
    b = valores[alvo == 0].to_numpy(dtype=float)
    u = stats.mannwhitneyu(a, b, alternative="two-sided").statistic
    return float(u / (len(a) * len(b)))


@lru_cache(maxsize=1)
def _pedidos() -> pd.DataFrame:
    ped = carregar()["pedidos"].copy()
    ped["Order Date"] = pd.to_datetime(ped["Order Date"])
    return ped


@lru_cache(maxsize=1)
def painel_de_features() -> pd.DataFrame:
    """Uma linha por conta elegível, com as features dos dois lados do corte.

    Elegível é a conta cuja primeira compra é até 2025-02: quem entrou depois
    não teve treze meses de painel pela frente e não podia ser marcada
    (Aula 04). Testar feature em quem não podia ser marcado mede a data de
    entrada, não a deterioração.
    """
    c = contas()
    d = carregar()
    painel, ped = d["painel"], _pedidos()

    elegivel = c[c.primeiro_mes <= CORTE].copy()
    idx = elegivel.index

    obs = painel[painel.periodo <= CORTE]
    pos = painel[painel.periodo >= INICIO_DO_ROTULO]
    ped_obs = ped[ped.periodo <= CORTE]

    def por_conta(serie: pd.Series, preencher=0.0) -> pd.Series:
        return serie.reindex(idx).fillna(preencher)

    # --- Recência, dos dois lados do corte ---------------------------------
    ultimo_obs = obs.groupby("account_id").periodo.max()
    elegivel["recencia_corte"] = por_conta(
        ultimo_obs.map(lambda m: _meses_entre(m, CORTE)), MESES_DE_OBSERVACAO)
    elegivel["recencia_fim"] = elegivel.ultimo_mes.map(
        lambda m: _meses_entre(m, FIM_DO_PAINEL))

    # --- Frequência ---------------------------------------------------------
    elegivel["freq_meses"] = por_conta(obs.groupby("account_id").periodo.nunique())
    elegivel["freq_dias"] = por_conta(
        ped_obs.groupby("account_id")["Order Date"].nunique())
    elegivel["freq_meses_painel"] = elegivel.meses_ativos

    # --- Valor --------------------------------------------------------------
    elegivel["valor_obs"] = por_conta(obs.groupby("account_id").receita_usd.sum())
    elegivel["valor_painel"] = elegivel.receita
    elegivel["ticket_medio"] = np.where(
        elegivel.freq_dias > 0, elegivel.valor_obs / elegivel.freq_dias.clip(lower=1), 0.0)

    # --- Sequência: os três meses mais recentes contra os três anteriores ----
    def soma_bloco(bloco: tuple[str, str]) -> pd.Series:
        ini, fim = bloco
        faixa = obs[(obs.periodo >= ini) & (obs.periodo <= fim)]
        return por_conta(faixa.groupby("account_id").receita_usd.sum())

    elegivel["receita_3m"] = soma_bloco(BLOCO_RECENTE)
    elegivel["receita_3m_anterior"] = soma_bloco(BLOCO_ANTERIOR)
    # Sem receita nos dois blocos, a razão é indefinida e vira 1,0: a conta não
    # acelerou nem desacelerou dentro da janela, ela sumiu antes dela, e é a
    # recência que carrega esse caso.
    denominador = elegivel.receita_3m_anterior.to_numpy(dtype=float)
    numerador = elegivel.receita_3m.to_numpy(dtype=float)
    razao = np.divide(numerador, denominador, out=np.ones(len(elegivel)),
                      where=denominador > 0)
    elegivel["razao_3m"] = np.clip(razao, 0, 10)

    # --- Marcas -------------------------------------------------------------
    elegivel["marcas_obs"] = por_conta(ped_obs.groupby("account_id").Brand.nunique())

    # --- Atividade depois do corte (nunca é feature: é o rótulo) ------------
    elegivel["meses_ativos_pos_corte"] = por_conta(
        pos.groupby("account_id").periodo.nunique())
    return elegivel


# ---------------------------------------------------------------------------
# Tabelas da aula
# ---------------------------------------------------------------------------

def formato_das_fontes() -> dict[str, tuple[int, int]]:
    """Linhas e colunas de cada aba, no grão em que ela chega.

    A abertura da aula precisa do contraste entre o grão do dado bruto (uma
    linha por item de pedido) e o grão que o modelo exige (uma linha por conta).
    Somar essas linhas à mão errou por 20 na Aula 03, então o número sai daqui.
    """
    return {nome: df.shape for nome, df in carregar().items()}


def do_evento_a_conta() -> dict[str, int]:
    """Os três grãos que a tabela de features atravessa."""
    d = carregar()
    return {
        "itens_de_pedido": len(d["pedidos"]),
        "linhas_de_painel": len(d["painel"]),
        "contas_na_carteira": int(d["painel"].account_id.nunique()),
        "contas_elegiveis": len(painel_de_features()),
        "colunas_de_entrada": len(FEATURES_HONESTAS),
    }


def particao_temporal() -> dict[str, int | str]:
    e = painel_de_features()
    return {
        "inicio_painel": INICIO_DO_PAINEL,
        "corte": CORTE,
        "fim_painel": FIM_DO_PAINEL,
        "meses_observacao": MESES_DE_OBSERVACAO,
        "meses_rotulo": MESES_DE_ROTULO,
        "contas": len(e),
        "perdidas": int(e.churn.sum()),
    }


CANDIDATAS = [
    ("recencia_fim", "Recência no fim do painel", "painel inteiro"),
    ("freq_meses_painel", "Meses ativos no painel inteiro", "painel inteiro"),
    ("valor_painel", "Receita do painel inteiro", "painel inteiro"),
    ("recencia_corte", "Recência no corte", "janela de observação"),
    ("freq_meses", "Meses ativos até o corte", "janela de observação"),
    ("freq_dias", "Dias com pedido até o corte", "janela de observação"),
    ("valor_obs", "Receita até o corte", "janela de observação"),
    ("ticket_medio", "Ticket médio até o corte", "janela de observação"),
    ("razao_3m", "Razão dos três meses recentes", "janela de observação"),
    ("marcas_obs", "Marcas distintas até o corte", "janela de observação"),
]


def auc_das_candidatas() -> pd.DataFrame:
    e = painel_de_features()
    linhas = []
    for coluna, rotulo, janela in CANDIDATAS:
        a = auc(e[coluna], e.churn)
        linhas.append({"coluna": coluna, "variavel": rotulo, "janela": janela,
                       "auc": a, "auc_orientada": max(a, 1 - a)})
    return pd.DataFrame(linhas).set_index("coluna")


def concordancia_do_vazamento() -> dict[str, float | int]:
    """Quanto a recência do fim do painel repete o rótulo, conta a conta."""
    e = painel_de_features()
    previsto = (e.recencia_fim >= 13).astype(int)
    iguais = int((previsto == e.churn).sum())
    return {"contas": len(e), "iguais": iguais, "concordancia": iguais / len(e),
            "auc": auc(e.recencia_fim, e.churn)}


def perfil_da_razao() -> pd.DataFrame:
    """Prevalência por faixa da variável de sequência."""
    e = painel_de_features().copy()
    e["faixa"] = pd.cut(e.razao_3m, [-0.01, 0.001, 0.5, 1.0, 10.01],
                        labels=["sem receita nos 3 meses", "queda acima de 50%",
                                "queda até 50%", "estável ou em alta"])
    t = e.groupby("faixa", observed=True).churn.agg(contas="size", perdidas="sum")
    t["prevalencia"] = t.perdidas / t.contas
    return t


def main() -> None:
    p = particao_temporal()
    print(f"Partição: observação {p['inicio_painel']} a {p['corte']} "
          f"({p['meses_observacao']} meses), rótulo {INICIO_DO_ROTULO} a "
          f"{p['fim_painel']} ({p['meses_rotulo']} meses)")
    print(f"Elegíveis: {p['contas']} contas, {p['perdidas']} perdidas "
          f"({p['perdidas'] / p['contas']:.1%})\n")
    print(auc_das_candidatas().to_string(
        formatters={"auc": "{:.3f}".format, "auc_orientada": "{:.3f}".format}))
    print()
    print("Concordância do vazamento:", concordancia_do_vazamento())
    print()
    print(perfil_da_razao().to_string())


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Peso de cada variável: regressão logística por IRLS, sem dependência nova
# ---------------------------------------------------------------------------

FEATURES_HONESTAS = ["recencia_corte", "freq_meses", "freq_dias", "valor_obs",
                     "ticket_medio", "razao_3m", "marcas_obs"]


def _logistica(X: np.ndarray, y: np.ndarray, iteracoes: int = 40,
               ridge: float = 1e-6) -> np.ndarray:
    """Máxima verossimilhança por Newton-Raphson (IRLS), com intercepto na
    coluna 0. O ridge mínimo só evita matriz singular quando duas colunas
    entram quase colineares, que é o caso de freq_meses e freq_dias."""
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


def pesos_do_modelo(features: list[str] | None = None) -> pd.DataFrame:
    """Coeficiente padronizado de cada feature, em log-odds e em razão de
    chances. Padronizado porque coeficiente bruto compara receita em dólar com
    contagem de marcas e a maior escala parece o maior peso.

    A leitura é: mantendo as demais fixas, um desvio padrão a mais nesta
    variável multiplica a chance de perda pela razão de chances da linha.
    """
    e = painel_de_features()
    colunas = features or FEATURES_HONESTAS
    bruto = e[colunas].to_numpy(dtype=float)
    media, desvio = bruto.mean(axis=0), bruto.std(axis=0)
    z = (bruto - media) / desvio
    X = np.column_stack([np.ones(len(z)), z])
    y = e.churn.to_numpy(dtype=float)
    beta = _logistica(X, y)
    t = pd.DataFrame({"coeficiente": beta[1:], "razao_de_chances": np.exp(beta[1:])},
                     index=colunas)
    t["peso_relativo"] = t.coeficiente.abs() / t.coeficiente.abs().sum()
    t["auc_isolada"] = [max(a, 1 - a) for a in
                        (auc(e[c], e.churn) for c in colunas)]
    return t.sort_values("peso_relativo", ascending=False)


def qualidade_do_modelo(features: list[str] | None = None) -> dict[str, float]:
    """AUC do escore conjunto e a matriz que a capacidade operacional recorta.

    Não é a avaliação da tarde: aqui o modelo serve de régua para comparar duas
    listas de features, e é a única forma de mostrar que a versão com vazamento
    parece melhor sem prever nada.
    """
    e = painel_de_features()
    colunas = features or FEATURES_HONESTAS
    bruto = e[colunas].to_numpy(dtype=float)
    z = (bruto - bruto.mean(axis=0)) / bruto.std(axis=0)
    X = np.column_stack([np.ones(len(z)), z])
    y = e.churn.to_numpy(dtype=float)
    escore = X @ _logistica(X, y)
    a = auc(pd.Series(escore, index=e.index), e.churn)
    return {"contas": len(e), "features": len(colunas), "auc": max(a, 1 - a)}
