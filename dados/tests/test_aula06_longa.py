# -*- coding: utf-8 -*-
"""Trava os números da Aula 06 sobre a base longa, de 65 meses.

A base chegou em 12/09/2026, no meio da aula, e o deck migrou para ela a partir
do slide da partição. Todo valor esperado aqui está transcrito de forma literal.

O xlsx longo não é versionado (ADR-005), então a suíte inteira pula quando ele
não está em dados/. Pular por ausência de arquivo é diferente de passar: o CI
não mede estes números, e é o teste local que vale.

Rodar: PYTHONPATH=. .venv/bin/python -m pytest dados/tests/test_aula06_longa.py -q
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

DECK = RAIZ / "aulas" / "aula06.html"
XLSX = RAIZ / "dados" / "datasets_case_modulo2_5yrs.xlsx"
CACHE = RAIZ / "dados" / ".cache_5yrs"

pytestmark = pytest.mark.skipif(
    not (XLSX.exists() or CACHE.exists()),
    reason="base longa não versionada (ADR-005)")


@pytest.fixture(scope="module")
def a():
    from dados import analise_aula06_longa

    return analise_aula06_longa


@pytest.fixture(scope="module")
def deck() -> str:
    return DECK.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# A partição
# ---------------------------------------------------------------------------

def test_a_particao_tem_36_meses_de_observacao_e_29_de_rotulo(a):
    p = a.particao_temporal()
    assert p["inicio_painel"] == "2021-04"
    assert p["corte"] == "2024-03"
    assert p["inicio_rotulo"] == "2024-04"
    assert p["fim_painel"] == "2026-08"
    assert p["meses_observacao"] == 36
    assert p["meses_rotulo"] == 29
    assert p["meses_observacao"] + p["meses_rotulo"] == 65


def test_a_carteira_longa_tem_7259_contas_e_4708_elegiveis(a):
    p = a.particao_temporal()
    assert p["carteira"] == 7259
    assert p["perdidas_carteira"] == 2456
    assert p["contas"] == 4708
    assert p["perdidas"] == 2456
    assert p["nao_elegiveis"] == 2551
    assert round(p["prevalencia"] * 100, 1) == 52.2


def test_toda_conta_marcada_e_elegivel(a):
    """As 2.551 contas fora da elegibilidade entraram depois do corte, então
    nenhuma delas pode estar marcada. Se este teste falhar, o critério de
    elegibilidade não corresponde à regra do rótulo desta base."""
    p = a.particao_temporal()
    assert p["perdidas"] == p["perdidas_carteira"]


def test_os_graos_da_abertura(a):
    g = a.do_evento_a_conta()
    assert g["itens_de_pedido"] == 492393
    assert g["linhas_de_painel"] == 44818
    assert g["contas_na_carteira"] == 7259
    assert g["contas_elegiveis"] == 4708
    assert g["colunas_de_entrada"] == 8


# ---------------------------------------------------------------------------
# AUC isolada
# ---------------------------------------------------------------------------

AUC_ESPERADA = {
    "freq_meses_painel": 0.919,
    "valor_painel": 0.832,
    "recencia_corte": 0.818,
    "freq_meses": 0.771,
    "freq_dias": 0.771,
    "valor_obs": 0.742,
    "marcas_obs": 0.705,
    "ticket_medio": 0.651,
    "razao_12m": 0.637,
    "razao_3m": 0.534,
}


@pytest.mark.parametrize("coluna,esperado", sorted(AUC_ESPERADA.items()))
def test_a_auc_isolada_de_cada_candidata(a, coluna, esperado):
    t = a.auc_das_candidatas()
    assert round(float(t.loc[coluna, "auc_orientada"]), 3) == esperado


def test_a_recencia_do_fim_do_painel_marca_09999(a):
    t = a.auc_das_candidatas()
    assert round(float(t.loc["recencia_fim", "auc_orientada"]), 4) == 0.9999


def test_a_janela_de_12_meses_separa_mais_que_a_de_3(a):
    """O ganho que a base longa comprou. Com 11 meses de observação a razão de
    12 meses não existia."""
    t = a.auc_das_candidatas()
    doze = float(t.loc["razao_12m", "auc_orientada"])
    tres = float(t.loc["razao_3m", "auc_orientada"])
    assert doze > tres
    assert round(doze, 3) == 0.637
    assert round(tres, 3) == 0.534


def test_nenhuma_coluna_honesta_passa_de_0818(a):
    t = a.auc_das_candidatas()
    honestas = t[t.janela == "janela de observação"]
    assert round(float(honestas.auc_orientada.max()), 3) == 0.818


# ---------------------------------------------------------------------------
# Vazamento
# ---------------------------------------------------------------------------

def test_a_regra_de_30_meses_reproduz_o_rotulo_em_4691_contas(a):
    c = a.concordancia_do_vazamento()
    assert c["contas"] == 4708
    assert c["iguais"] == 4691
    assert round(c["concordancia"] * 100, 1) == 99.6


def test_o_escore_honesto_marca_0834_e_o_vazado_marca_09999(a):
    honesto = a.qualidade_do_modelo()
    vazado = a.qualidade_do_modelo(a.FEATURES_HONESTAS + ["recencia_fim"])
    assert honesto["features"] == 8
    assert vazado["features"] == 9
    assert round(honesto["auc"], 3) == 0.834
    assert round(vazado["auc"], 4) == 0.9999
    assert round(vazado["auc"] - honesto["auc"], 3) == 0.166


def test_nenhuma_feature_honesta_muda_quando_o_painel_e_truncado(a, monkeypatch):
    """A propriedade que sustenta a aula, agora na base longa.

    Visto falhando: incluir `recencia_fim` na lista acusa 4.708 diferenças.
    """
    import pandas as pd

    completo = a.painel_de_features()[a.FEATURES_HONESTAS].copy()
    bruto = a.carregar()
    truncado = dict(bruto)
    truncado["painel"] = bruto["painel"][bruto["painel"].periodo <= a.CORTE]
    truncado["pedidos"] = bruto["pedidos"][bruto["pedidos"].periodo <= a.CORTE]

    a.painel_de_features.cache_clear()
    a._pedidos.cache_clear()
    a.contas.cache_clear()
    monkeypatch.setattr(a, "carregar", lambda: truncado)
    try:
        depois = a.painel_de_features()[a.FEATURES_HONESTAS].copy()
    finally:
        a.painel_de_features.cache_clear()
        a._pedidos.cache_clear()
        a.contas.cache_clear()

    assert list(completo.index) == list(depois.index)
    for coluna in a.FEATURES_HONESTAS:
        diferentes = int((~pd.Series(
            completo[coluna].to_numpy() == depois[coluna].to_numpy())).sum())
        assert diferentes == 0, (coluna, diferentes)


# ---------------------------------------------------------------------------
# Pesos
# ---------------------------------------------------------------------------

PESOS_ESPERADOS = {
    "freq_meses": (-1.366, 0.255, 41.2),
    "recencia_corte": (0.867, 2.379, 26.1),
    "freq_dias": (0.352, 1.422, 10.6),
    "razao_3m": (-0.274, 0.760, 8.3),
    "razao_12m": (-0.202, 0.817, 6.1),
    "marcas_obs": (-0.148, 0.863, 4.4),
    "ticket_medio": (-0.101, 0.904, 3.0),
    "valor_obs": (-0.009, 0.991, 0.3),
}


@pytest.mark.parametrize("coluna,esperado", sorted(PESOS_ESPERADOS.items()))
def test_o_peso_de_cada_coluna(a, coluna, esperado):
    coeficiente, razao, peso = esperado
    t = a.pesos_do_modelo()
    assert round(float(t.loc[coluna, "coeficiente"]), 3) == coeficiente
    assert round(float(t.loc[coluna, "razao_de_chances"]), 3) == razao
    assert round(float(t.loc[coluna, "peso_relativo"]) * 100, 1) == peso


def test_recencia_e_frequencia_somam_779_por_cento(a):
    t = a.pesos_do_modelo()
    soma = t.loc[["recencia_corte", "freq_meses", "freq_dias"], "peso_relativo"].sum()
    assert round(float(soma) * 100, 1) == 77.9


def test_as_duas_de_frequencia_somam_518_por_cento(a):
    t = a.pesos_do_modelo()
    soma = t.loc[["freq_meses", "freq_dias"], "peso_relativo"].sum()
    assert round(float(soma) * 100, 1) == 51.8


def test_freq_dias_entra_no_modelo_com_sinal_invertido(a):
    """Sozinha ela protege (AUC de 0,771 na direção protetora) e no modelo
    aparece com coeficiente positivo. É o efeito da correlação com freq_meses,
    e o slide do sinal invertido existe por causa disto."""
    t = a.pesos_do_modelo()
    assert float(t.loc["freq_dias", "coeficiente"]) > 0
    assert float(t.loc["freq_meses", "coeficiente"]) < 0
    assert round(float(t.loc["freq_dias", "auc_isolada"]), 3) == 0.771


# ---------------------------------------------------------------------------
# Limiar
# ---------------------------------------------------------------------------

def test_a_fila_de_138_contas_acerta_114(a):
    r = a.lista_priorizada(138)
    assert r["verdadeiros_positivos"] == 114
    assert r["falsos_positivos"] == 24
    assert round(r["precisao"] * 100, 1) == 82.6
    assert round(r["revocacao"] * 100, 1) == 4.6
    assert round(r["acuracia"] * 100, 1) == 49.7


def test_a_fila_de_138_nao_alcanca_mais_que_56_por_cento_das_perdas(a):
    p = a.particao_temporal()
    assert round(138 / p["perdidas"] * 100, 1) == 5.6


def test_marcar_conta_nenhuma_ja_entrega_478_de_acuracia(a):
    p = a.particao_temporal()
    assert round((1 - p["prevalencia"]) * 100, 1) == 47.8


# ---------------------------------------------------------------------------
# Faixas da razão de 3 meses
# ---------------------------------------------------------------------------

def test_as_faixas_da_razao_de_3_meses(a):
    import pandas as pd

    e = a.painel_de_features().copy()
    e["faixa"] = pd.cut(e.razao_3m, [-0.01, 0.001, 0.5, 1.0, 10.01],
                        labels=["sem receita", "queda acima de 50%",
                                "queda até 50%", "estável ou em alta"])
    t = e.groupby("faixa", observed=True).churn.agg(contas="size", perdidas="sum")
    esperado = {"sem receita": (606, 257, 42.4),
                "queda acima de 50%": (278, 17, 6.1),
                "queda até 50%": (3485, 2166, 62.2),
                "estável ou em alta": (339, 16, 4.7)}
    for faixa, (contas, perdidas, prev) in esperado.items():
        assert int(t.loc[faixa, "contas"]) == contas, faixa
        assert int(t.loc[faixa, "perdidas"]) == perdidas, faixa
        assert round(t.loc[faixa, "perdidas"] / t.loc[faixa, "contas"] * 100, 1) == prev
    assert int(t.contas.sum()) == 4708


# ---------------------------------------------------------------------------
# O deck cita os mesmos números
# ---------------------------------------------------------------------------

NUMEROS_NO_DECK = [
    "492.393", "7.259", "4.708", "2.456", "2.551", "52,2%",
    "2021-04", "2024-03", "2024-04", "2026-08", "07/03/2024", "36", "29", "65",
    "0,9999", "0,919", "0,832", "0,818", "0,771", "0,742", "0,705", "0,651",
    "0,637", "0,534", "99,6%", "4.691", "0,834", "0,166",
    "-1,366", "0,255", "41,2%", "+0,867", "2,379", "26,1%",
    "+0,352", "1,422", "10,6%", "-0,274", "0,760", "8,3%",
    "-0,202", "0,817", "6,1%", "77,9%", "51,8%", "7,7%", "0,3%",
    "606", "257", "42,4%", "278", "3.485", "2.166", "62,2%", "339", "4,7%",
    "138", "114", "82,6%", "4,6%", "49,7%", "2.661", "75,8%", "82,2%",
    "77,0%", "47,8%", "5,6%",
]


@pytest.mark.parametrize("numero", NUMEROS_NO_DECK)
def test_o_numero_aparece_no_deck(deck, numero):
    assert numero in deck, numero


def test_o_deck_nao_cita_a_particao_da_base_curta(deck):
    """As datas da base curta contradizem tudo que vem depois da partição."""
    for antigo in ("2025-02", "2025-03", "2026-03", "1.593", "42,5%"):
        assert antigo not in deck, antigo


def test_o_3748_aparece_uma_vez_so_e_como_historia(deck):
    """As 3.748 contas são o número do Artefato 1, sobre o painel de 24 meses.
    Ele fica no resgate, declarado como história. Uma segunda ocorrência
    significa que algum slide da manhã ficou na base antiga."""
    assert deck.count("3.748") == 1
    assert "Artefato 1 sobre o painel de 24 meses, com 3.748" in deck
