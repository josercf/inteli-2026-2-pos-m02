# -*- coding: utf-8 -*-
"""Números da Aula 07, lidos do próprio aplicativo que a turma vai rodar.

Este módulo não reimplementa nada. Ele importa o pacote `app` do repositório de
prática, que é o mesmo código que o aluno executa em sala. Duplicar a lógica
aqui faria o deck e o aplicativo divergirem na primeira correção aplicada de um
lado só, e o número do slide deixaria de descrever o que roda na tela.

O repositório de prática é irmão deste, em
~/Projects/Inteli/MBA/inteli-pos-2026-2a-eda, e não é versionado aqui (ADR-006).
Sem ele, e sem a base longa, este módulo não roda e os testes pulam.

Uso: PYTHONPATH=. .venv/bin/python dados/analise_aula07.py
"""

from __future__ import annotations

import sys
import time
from functools import lru_cache
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
PRATICA = RAIZ.parent / "inteli-pos-2026-2a-eda"
SCRIPT_EXPORTADO = Path.home() / "Downloads" / "churn_model.py"

CONTA_D = "CLI052938"   # a perda mais cara, invisível para o escore
CONTA_E = "CLI053457"   # compra única de 2021, no topo do escore


class PraticaAusente(FileNotFoundError):
    """O repositório de prática não está ao lado deste. Não é erro de código."""


def _app():
    if not (PRATICA / "app" / "churn").is_dir():
        raise PraticaAusente(
            f"{PRATICA} não encontrado. O aplicativo da Aula 07 vive no "
            "repositório de prática, clonado ao lado deste (ADR-006).")
    if str(PRATICA) not in sys.path:
        sys.path.insert(0, str(PRATICA))
    import app.churn as churn  # noqa: PLC0415

    return churn


@lru_cache(maxsize=1)
def tabela():
    """A tabela de entrada e o rótulo, saídos do aplicativo."""
    churn = _app()
    ped = churn.dados.pedidos()
    contas = churn.rotulo.elegiveis()
    X = churn.features.construir(ped, churn.rotulo.CORTE, contas=contas)
    y = churn.rotulo.rotulo().reindex(X.index).astype(int)
    return X, y


@lru_cache(maxsize=1)
def escore() -> pd.Series:
    churn = _app()
    X, y = tabela()
    return churn.modelo.escore_fora_da_amostra(X, y)


def formato() -> dict[str, int]:
    churn = _app()
    X, y = tabela()
    ped = churn.dados.pedidos()
    return {
        "linhas_de_pedido": len(ped),
        "contas_na_carteira": int(ped.account_id.nunique()),
        "contas_elegiveis": len(X),
        "perdidas": int(y.sum()),
        "colunas": X.shape[1],
        "colunas_do_gemini": len(churn.features.FEATURES_BASE),
        "colunas_de_erosao": len(churn.features.FEATURES_EROSAO),
    }


def qualidade() -> dict[str, float]:
    churn = _app()
    X, y = tabela()
    return {"auc_fora_da_amostra": churn.modelo.auc(escore(), y)}


@lru_cache(maxsize=1)
def filas() -> pd.DataFrame:
    """As duas ordenações da fila, lado a lado."""
    churn = _app()
    X, y = tabela()
    t = churn.lista.priorizar(escore(), valor_em_risco=X.receita_12m)
    perdidas = y[y == 1].index
    risco_total = float(X.loc[perdidas, "receita_12m"].sum())
    linhas = []
    for coluna, nome in (("na_fila", "Por probabilidade"),
                         ("na_fila_por_valor", "Por valor esperado")):
        c = churn.lista.matriz_de_confusao(t, y, coluna)
        acertos = t[t[coluna]].index.intersection(perdidas)
        linhas.append({
            "criterio": nome, "contas": int(t[coluna].sum()),
            "acertos": c["verdadeiros_positivos"], "precisao": c["precisao"],
            "revocacao": c["revocacao"],
            "receita_alcancada": float(X.loc[acertos, "receita_12m"].sum()),
            "fracao_do_risco": float(X.loc[acertos, "receita_12m"].sum()) / risco_total,
        })
    return pd.DataFrame(linhas).set_index("criterio")


def risco_total() -> float:
    X, y = tabela()
    return float(X.loc[y[y == 1].index, "receita_12m"].sum())


def par_de_contas() -> pd.DataFrame:
    churn = _app()
    X, y = tabela()
    t = churn.lista.priorizar(escore(), valor_em_risco=X.receita_12m)
    saida = {}
    for apelido, cid in (("Conta D", CONTA_D), ("Conta E", CONTA_E)):
        r = t.loc[cid]
        saida[apelido] = {
            "escore": float(r.escore), "posicao": int(r.posicao),
            "posicao_por_valor": int(r.posicao_por_valor),
            "receita_12m": float(r.valor_em_risco),
            "na_fila_por_valor": bool(r.na_fila_por_valor),
        }
    return pd.DataFrame(saida).T


def importancia() -> pd.DataFrame:
    churn = _app()
    X, y = tabela()
    return churn.modelo.importancia(churn.modelo.treinar(X, y), X, y)


def custo_de_carga() -> dict[str, float]:
    """Quanto custa montar a tabela com o cache já quente.

    A primeira carga, que lê o xlsx de 69 MB, leva perto de quatro minutos e é
    medida à mão: repeti-la em teste tornaria a suíte inutilizável.
    """
    _app()
    tabela.cache_clear()
    inicio = time.time()
    tabela()
    return {"segundos_com_cache": time.time() - inicio}


def tamanho_do_script_exportado() -> int | None:
    """Linhas do churn_model.py que saiu do Gemini, se ele estiver por perto."""
    if not SCRIPT_EXPORTADO.exists():
        return None
    return len(SCRIPT_EXPORTADO.read_text(encoding="utf-8").splitlines())


def main() -> None:
    f = formato()
    print(f"pedidos: {f['linhas_de_pedido']:,} linhas, {f['contas_na_carteira']:,} contas")
    print(f"elegíveis: {f['contas_elegiveis']:,}, perdidas {f['perdidas']:,}")
    print(f"colunas: {f['colunas']} ({f['colunas_do_gemini']} do Gemini "
          f"mais {f['colunas_de_erosao']} de erosão)")
    print(f"AUC fora da amostra: {qualidade()['auc_fora_da_amostra']:.4f}")
    print(f"risco total: USD {risco_total():,.0f}\n")
    print(filas().to_string(float_format=lambda v: f"{v:,.4f}"))
    print()
    print(par_de_contas().to_string(float_format=lambda v: f"{v:,.3f}"))
    print()
    print(importancia().head(4).to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print(f"\ncarga com cache: {custo_de_carga()['segundos_com_cache']:.1f}s")
    print(f"script exportado: {tamanho_do_script_exportado()} linhas")


if __name__ == "__main__":
    main()
