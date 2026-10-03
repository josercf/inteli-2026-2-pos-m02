# -*- coding: utf-8 -*-
"""Referência em Python do modelo que o painel da Aula 08 roda no navegador.

O painel (painel/index.html) lê a aba "Dataset 1" da planilha original do case,
monta seis colunas por conta, treina uma regressão logística e ordena a fila por
valor esperado, tudo em JavaScript. Este módulo faz a mesma conta, com as mesmas
regras, para que tools/tests/test_painel_modelo.py compare os dois números a
número. Divergência entre os dois é defeito de um deles.

Regras, iguais às do painel:

- histórico até 2024-02, o último mês inteiro antes do corte de 07/03/2024 que
  define o churn_label; usar março vazaria o rótulo, porque uma compra depois
  do dia 7 só existe em conta não perdida;
- mês com compra é linha com qtd_pedidos > 0;
- elegível é a conta com pelo menos uma compra até 2024-02;
- escore fora da amostra, em 5 dobras: a conta i (na ordem do account_id) cai
  na dobra i % 5;
- fila por valor esperado, escore vezes a receita dos 12 meses até o corte,
  desempate pelo account_id.

Uso: .venv/bin/python dados/analise_aula08.py [caminho-do-xlsx]
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

# A base longa, com o nome que a turma recebeu. No acervo ela fica em dados/ com
# o sufixo _5yrs e não é versionada (ADR-005).
PLANILHA = Path(__file__).resolve().parent / "datasets_case_modulo2_5yrs.xlsx"
ULTIMO_MES = "2024-02"
CAPACIDADE = 138
DOBRAS = 5
RIDGE = 1e-6
TETO_DA_RAZAO = 10.0

COLUNAS = [
    "meses_desde_ultima_compra",
    "meses_com_compra_12m",
    "log_receita_12m",
    "razao_receita_12m",
    "receita_12m_sobre_pico",
    "meses_de_casa",
]


def _mes(periodo: pd.Series) -> np.ndarray:
    a = periodo.str.slice(0, 4).astype(int).to_numpy()
    m = periodo.str.slice(5, 7).astype(int).to_numpy()
    return a * 12 + m - 1


def carregar(caminho: Path = PLANILHA) -> pd.DataFrame:
    return pd.read_excel(caminho, sheet_name="Dataset 1")


def tabela(painel: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por conta elegível, com as seis colunas, o rótulo e a receita."""
    p = painel[painel.qtd_pedidos > 0].copy()
    p["m"] = _mes(p.periodo.astype(str))
    corte = _mes(pd.Series([ULTIMO_MES]))[0]
    rotulo = painel.groupby("account_id").churn_label.max()
    cadastro = painel.groupby("account_id")[["segment", "country"]].first()
    h = p[p.m <= corte]

    def receita_entre(ini, fim):  # meses em (corte - fim, corte - ini]
        f = h[(h.m > corte - fim) & (h.m <= corte - ini)]
        return f.groupby("account_id").receita_usd.sum()

    g = h.groupby("account_id")
    t = pd.DataFrame(index=pd.Index(sorted(g.groups), name="account_id"))
    t["meses_desde_ultima_compra"] = corte - g.m.max()
    t["meses_de_casa"] = corte - g.m.min()
    t["meses_com_compra_12m"] = h[h.m > corte - 12].groupby("account_id").m.nunique()
    r12 = receita_entre(0, 12).reindex(t.index).fillna(0.0)
    r24 = receita_entre(12, 24).reindex(t.index).fillna(0.0)
    r36 = receita_entre(24, 36).reindex(t.index).fillna(0.0)
    t["receita_12m"] = r12
    t["log_receita_12m"] = np.log1p(np.maximum(r12, 0.0))
    t["razao_receita_12m"] = np.clip(np.divide(r12, r24, out=np.ones(len(t)), where=r24 > 0),
                                      0.0, TETO_DA_RAZAO)
    pico = np.maximum.reduce([r12.to_numpy(), r24.to_numpy(), r36.to_numpy()])
    t["receita_12m_sobre_pico"] = np.clip(
        np.divide(r12.to_numpy(), pico, out=np.ones(len(t)), where=pico > 0), 0.0, 1.0)
    t = t.fillna({"meses_com_compra_12m": 0})
    t["churn"] = rotulo.reindex(t.index).astype(int)
    return t.join(cadastro)


def _ajustar(X: np.ndarray, y: np.ndarray, iteracoes: int = 50) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Regressão logística por IRLS sobre colunas padronizadas (ADR-008)."""
    media = X.mean(axis=0)
    desvio = X.std(axis=0)
    desvio[desvio == 0] = 1.0
    Z = np.column_stack([np.ones(len(X)), (X - media) / desvio])
    w = np.zeros(Z.shape[1])
    for _ in range(iteracoes):
        p = 1 / (1 + np.exp(-Z @ w))
        W = p * (1 - p)
        H = Z.T @ (Z * W[:, None]) + RIDGE * np.eye(len(w))
        passo = np.linalg.solve(H, Z.T @ (y - p) - RIDGE * w)
        w = w + passo
        if np.max(np.abs(passo)) < 1e-10:
            break
    return w, media, desvio


def _prever(w, media, desvio, X):
    Z = np.column_stack([np.ones(len(X)), (X - media) / desvio])
    return 1 / (1 + np.exp(-Z @ w))


def auc(escore: np.ndarray, y: np.ndarray) -> float:
    r = pd.Series(escore).rank(method="average").to_numpy()
    pos = y == 1
    n1, n0 = pos.sum(), (~pos).sum()
    return float((r[pos].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def rodar(painel: pd.DataFrame) -> dict:
    t = tabela(painel)
    X = t[COLUNAS].to_numpy(dtype=float)
    y = t.churn.to_numpy()
    dobra = np.arange(len(t)) % DOBRAS
    escore = np.zeros(len(t))
    for k in range(DOBRAS):
        tr, te = dobra != k, dobra == k
        escore[te] = _prever(*_ajustar(X[tr], y[tr]), X[te])
    w, media, desvio = _ajustar(X, y)
    t["escore"] = escore
    t["valor_em_risco"] = np.maximum(t.receita_12m, 0.0)
    t["valor_esperado"] = t.escore * t.valor_em_risco
    ordem = t.reset_index().sort_values(["valor_esperado", "account_id"],
                                        ascending=[False, True])
    fila = ordem.head(CAPACIDADE)
    return {
        "tabela": t,
        "auc": auc(escore, y),
        "pesos": dict(zip(COLUNAS, w[1:])),
        "fila": fila,
        "acertos_fila": int(fila.churn.sum()),
        "valor_esperado_fila": float(fila.valor_esperado.sum()),
    }


def main() -> None:
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else PLANILHA
    r = rodar(carregar(caminho))
    t = r["tabela"]
    print(f"elegíveis: {len(t)}, perdidas: {int(t.churn.sum())} ({t.churn.mean():.1%})")
    print(f"AUC fora da amostra: {r['auc']:.4f}")
    print("pesos padronizados:")
    for c, v in r["pesos"].items():
        print(f"  {c:28s} {v:+.3f}")
    f = r["fila"]
    print(f"fila de {CAPACIDADE}: {r['acertos_fila']} perdidas, "
          f"valor esperado somado USD {r['valor_esperado_fila']:,.0f}")
    print(f[["account_id", "segment", "escore", "valor_em_risco", "valor_esperado",
             "meses_desde_ultima_compra", "churn"]].head(8).to_string(index=False))


if __name__ == "__main__":
    main()
