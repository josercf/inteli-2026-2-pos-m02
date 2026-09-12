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
# Hiperparâmetro: a varredura de regularização
# ---------------------------------------------------------------------------

def test_a_particao_de_treino_e_validacao(a):
    t = a.tamanho_da_particao()
    assert t["treino"] == 3295
    assert t["validacao"] == 1413
    assert t["treino"] + t["validacao"] == 4708


CURVA_ESPERADA = {
    0.0: (0.8339, 0.8312, 3.35),
    10.0: (0.8338, 0.8312, 2.76),
    100.0: (0.8322, 0.8294, 2.28),
    1000.0: (0.8287, 0.8256, 1.20),
    10000.0: (0.8263, 0.8230, 0.28),
}


@pytest.mark.parametrize("lam,esperado", sorted(CURVA_ESPERADA.items()))
def test_a_curva_de_regularizacao(a, lam, esperado):
    treino, validacao, pesos = esperado
    t = a.curva_de_regularizacao()
    assert round(float(t.loc[lam, "auc_treino"]), 4) == treino
    assert round(float(t.loc[lam, "auc_validacao"]), 4) == validacao
    assert round(float(t.loc[lam, "soma_dos_pesos"]), 2) == pesos


def test_regularizar_a_tabela_real_nao_ajuda(a):
    """O achado do slide. Se um dia isto deixar de valer, o slide vira mentira:
    a validação precisa parar de melhorar conforme a penalidade sobe."""
    t = a.curva_de_regularizacao()
    melhor = t.auc_validacao.idxmax()
    assert melhor <= 10.0, melhor
    assert round(float(t.loc[0.0, "auc_validacao"]), 4) == 0.8312


def test_a_distancia_entre_treino_e_validacao_e_de_00027(a):
    """Sem essa distância não existe sobreajuste para o botão corrigir."""
    t = a.curva_de_regularizacao()
    gap = t.loc[0.0, "auc_treino"] - t.loc[0.0, "auc_validacao"]
    assert round(float(gap), 4) == 0.0027


RUIDO_ESPERADO = {
    0.0: (0.8568, 0.8084),
    1000.0: (0.8486, 0.8110),
}


@pytest.mark.parametrize("lam,esperado", sorted(RUIDO_ESPERADO.items()))
def test_a_curva_com_ruido(a, lam, esperado):
    treino, validacao = esperado
    t = a.curva_com_ruido()
    assert int(t.loc[lam, "colunas"]) == 208
    assert round(float(t.loc[lam, "auc_treino"]), 4) == treino
    assert round(float(t.loc[lam, "auc_validacao"]), 4) == validacao


def test_o_ruido_abre_a_distancia_em_dezoito_vezes(a):
    """É o contraste que dá sentido ao slide: na tabela real a distância é de
    0,0027 e com ruído ela vai a 0,0484."""
    limpa = a.curva_de_regularizacao()
    suja = a.curva_com_ruido()
    gap_limpo = float(limpa.loc[0.0, "auc_treino"] - limpa.loc[0.0, "auc_validacao"])
    gap_sujo = float(suja.loc[0.0, "auc_treino"] - suja.loc[0.0, "auc_validacao"])
    assert round(gap_sujo, 4) == 0.0484
    assert gap_sujo > gap_limpo * 15


def test_a_regularizacao_devolve_pouco_do_que_o_ruido_tirou(a):
    """0,0026 recuperados de 0,0228 perdidos. O botão remedia, não conserta."""
    limpa = a.curva_de_regularizacao()
    suja = a.curva_com_ruido()
    perdido = float(limpa.loc[0.0, "auc_validacao"] - suja.loc[0.0, "auc_validacao"])
    devolvido = float(suja.loc[1000.0, "auc_validacao"] - suja.loc[0.0, "auc_validacao"])
    assert round(perdido, 4) == 0.0228
    assert round(devolvido, 4) == 0.0026
    assert devolvido < perdido / 5


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
# O par de contas
# ---------------------------------------------------------------------------

def test_as_duas_contas_do_par_estao_marcadas(a):
    """Se uma delas deixar de ser churn, o slide inteiro perde o sentido."""
    t = a.par_de_contas()
    assert int(t.loc["Conta D", "churn"]) == 1
    assert int(t.loc["Conta E", "churn"]) == 1


def test_a_conta_d_e_a_perda_mais_cara_da_carteira_elegivel(a):
    """O argumento do slide depende disto: não existe perdida com receita maior
    na janela de observação."""
    e = a.painel_de_features()
    perdidas = e[e.churn == 1]
    assert perdidas.valor_obs.idxmax() == a.CONTA_D


def test_a_conta_d_cai_para_3787(a):
    t = a.par_de_contas()
    d = t.loc["Conta D"]
    assert int(d["posicao"]) == 3787
    assert round(float(d["escore"]), 3) == 0.215
    assert round(float(d["valor_obs"])) == 12054974
    assert int(d["recencia_corte"]) == 6
    assert int(d["freq_meses"]) == 4
    assert int(d["freq_dias"]) == 16
    assert round(float(d["razao_12m"]), 3) == 0.347
    assert round(float(d["razao_3m"]), 3) == 1.000


def test_a_conta_e_entra_na_fila_de_138(a):
    t = a.par_de_contas()
    e = t.loc["Conta E"]
    assert int(e["posicao"]) == 105
    assert int(e["posicao"]) <= 138
    assert round(float(e["escore"]), 3) == 0.934
    assert round(float(e["valor_obs"])) == 77797
    assert int(e["recencia_corte"]) == 34
    assert int(e["freq_meses"]) == 1


def test_a_conta_de_maior_valor_fica_atras_da_de_menor(a):
    """A inversão é o achado. Se um dia a D subir acima da E, o slide vira
    mentira e precisa ser refeito."""
    t = a.par_de_contas()
    assert float(t.loc["Conta D", "valor_obs"]) > float(t.loc["Conta E", "valor_obs"]) * 100
    assert int(t.loc["Conta D", "posicao"]) > int(t.loc["Conta E", "posicao"]) * 30


def test_a_serie_da_conta_d_tem_quatro_meses_com_receita(a):
    s = a.serie_da_conta(a.CONTA_D)
    assert len(s) == 4
    assert list(s.periodo) == ["2022-08", "2023-03", "2023-07", "2023-09"]
    assert round(float(s.receita_usd.iloc[0])) == 7412553
    assert round(float(s.receita_usd.iloc[-1])) == 1844687
    assert int(s.qtd_pedidos.iloc[-1]) == 31


def test_o_deck_nao_expoe_o_id_real_das_contas(a):
    """O repositório é público e o aluno chega nele. Os ids vivem no módulo e
    nas notas de condução, e o deck usa apelido."""
    deck = DECK.read_text(encoding="utf-8")
    assert a.CONTA_D not in deck
    assert a.CONTA_E not in deck
    assert "Conta D" in deck and "Conta E" in deck


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
    "3.295", "1.413", "0,8339", "0,8312", "0,8338", "0,8322", "0,8294",
    "0,8287", "0,8256", "0,8263", "0,8230", "3,35", "2,76", "2,28",
    "1,20", "0,28", "0,8568", "0,8084", "0,8486", "0,8110",
    "0,0027", "0,0484", "0,0376", "0,0228", "0,0026", "0,0229", "208",
    "3.787", "105", "0,215", "0,934", "12.054.974", "77.797", "0,347",
    "7.412.553", "1.534.746", "1.262.988", "1.844.687",
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
