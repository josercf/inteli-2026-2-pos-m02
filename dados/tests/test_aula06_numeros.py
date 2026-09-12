# -*- coding: utf-8 -*-
"""Trava os números da Aula 06 contra o dataset oficial.

Todo valor esperado aqui está transcrito de forma literal. Teste que importa a
constante que o gerador usa concorda consigo mesmo: foi assim que o teste do
Grupo Talvera passou mesmo com o dado alterado (ver CLAUDE.md).

Além dos valores, a suíte guarda a propriedade que sustenta a aula inteira:
nenhuma feature honesta pode mudar de valor quando o painel é truncado no
corte. Uma feature que muda leu dado da janela do rótulo.

Rodar: .venv/bin/python -m pytest dados/tests/test_aula06_numeros.py -q
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

XLSX = RAIZ / "dados" / "datasets_case_modulo2.xlsx"

pytestmark = pytest.mark.skipif(
    not XLSX.exists(), reason="dataset oficial não versionado (ADR-005)")


@pytest.fixture(scope="module")
def a():
    from dados import analise_aula06

    return analise_aula06


# ---------------------------------------------------------------------------
# A partição temporal
# ---------------------------------------------------------------------------

def test_a_particao_tem_11_meses_de_observacao_e_13_de_rotulo(a):
    p = a.particao_temporal()
    assert p["inicio_painel"] == "2024-04"
    assert p["corte"] == "2025-02"
    assert p["fim_painel"] == "2026-03"
    assert p["meses_observacao"] == 11
    assert p["meses_rotulo"] == 13


def test_as_duas_janelas_cobrem_o_painel_sem_buraco_nem_sobreposicao(a):
    """11 mais 13 fecham os 24 meses do painel. Um mês perdido entre as janelas
    seria um mês de comportamento que nenhuma das duas enxerga."""
    p = a.particao_temporal()
    assert p["meses_observacao"] + p["meses_rotulo"] == 24
    assert a.INICIO_DO_ROTULO == "2025-03"


def test_os_tres_graos_que_a_tabela_atravessa(a):
    """A abertura da aula contrasta o grão do dado bruto com o grão da decisão.
    Somar linhas de aba à mão já errou por 20 na Aula 03."""
    g = a.do_evento_a_conta()
    assert g["itens_de_pedido"] == 207826
    assert g["linhas_de_painel"] == 24071
    assert g["contas_na_carteira"] == 8282
    assert g["contas_elegiveis"] == 3748
    assert g["colunas_de_entrada"] == 7


def test_a_populacao_elegivel_tem_3748_contas_e_1593_perdidas(a):
    p = a.particao_temporal()
    assert p["contas"] == 3748
    assert p["perdidas"] == 1593
    assert round(p["perdidas"] / p["contas"] * 100, 1) == 42.5


# ---------------------------------------------------------------------------
# A AUC isolada de cada candidata
# ---------------------------------------------------------------------------

AUC_ESPERADA = {
    "recencia_fim": 0.994,
    "freq_meses_painel": 0.885,
    "valor_painel": 0.752,
    "recencia_corte": 0.772,
    "freq_dias": 0.693,
    "freq_meses": 0.680,
    "valor_obs": 0.618,
    "marcas_obs": 0.608,
    "razao_3m": 0.567,
    "ticket_medio": 0.540,
}


@pytest.mark.parametrize("coluna,esperado", sorted(AUC_ESPERADA.items()))
def test_a_auc_isolada_de_cada_candidata(a, coluna, esperado):
    t = a.auc_das_candidatas()
    assert round(float(t.loc[coluna, "auc_orientada"]), 3) == esperado


def test_nenhuma_coluna_da_janela_de_observacao_passa_de_0772(a):
    """O achado da aula. Se uma coluna honesta subir para perto de 1,0, ou o
    corte vazou ou a coluna deixou de ser honesta."""
    t = a.auc_das_candidatas()
    honestas = t[t.janela == "janela de observação"]
    assert round(float(honestas.auc_orientada.max()), 3) == 0.772


# ---------------------------------------------------------------------------
# O vazamento
# ---------------------------------------------------------------------------

def test_a_recencia_do_fim_do_painel_reproduz_o_rotulo_em_3366_contas(a):
    c = a.concordancia_do_vazamento()
    assert c["contas"] == 3748
    assert c["iguais"] == 3366
    assert round(c["concordancia"] * 100, 1) == 89.8


def test_o_escore_honesto_marca_0794_e_o_vazado_marca_0995(a):
    honesto = a.qualidade_do_modelo()
    vazado = a.qualidade_do_modelo(a.FEATURES_HONESTAS + ["recencia_fim"])
    assert honesto["features"] == 7
    assert vazado["features"] == 8
    assert round(honesto["auc"], 3) == 0.794
    assert round(vazado["auc"], 3) == 0.995
    assert round(vazado["auc"] - honesto["auc"], 3) == 0.201


# ---------------------------------------------------------------------------
# O peso de cada variável
# ---------------------------------------------------------------------------

PESOS_ESPERADOS = {
    # coluna: (coeficiente, razao de chances, peso relativo em %)
    "recencia_corte": (0.804, 2.234, 33.1),
    "freq_meses": (-0.588, 0.555, 24.2),
    "freq_dias": (-0.554, 0.574, 22.8),
    "marcas_obs": (-0.159, 0.853, 6.6),
    "ticket_medio": (0.129, 1.138, 5.3),
    "valor_obs": (-0.114, 0.892, 4.7),
    "razao_3m": (-0.080, 0.923, 3.3),
}


@pytest.mark.parametrize("coluna,esperado", sorted(PESOS_ESPERADOS.items()))
def test_o_peso_de_cada_coluna(a, coluna, esperado):
    coeficiente, razao, peso = esperado
    t = a.pesos_do_modelo()
    assert round(float(t.loc[coluna, "coeficiente"]), 3) == coeficiente
    assert round(float(t.loc[coluna, "razao_de_chances"]), 3) == razao
    assert round(float(t.loc[coluna, "peso_relativo"]) * 100, 1) == peso


def test_recencia_e_frequencia_somam_801_por_cento_do_peso(a):
    t = a.pesos_do_modelo()
    soma = t.loc[["recencia_corte", "freq_meses", "freq_dias"], "peso_relativo"].sum()
    assert round(float(soma) * 100, 1) == 80.1


def test_as_duas_colunas_de_valor_somam_100_por_cento_do_peso(a):
    t = a.pesos_do_modelo()
    soma = t.loc[["valor_obs", "ticket_medio"], "peso_relativo"].sum()
    assert round(float(soma) * 100, 1) == 10.0


def test_a_recencia_e_a_unica_coluna_que_empurra_para_a_perda(a):
    """Coeficiente positivo empurra para perda. Recência e ticket médio são os
    dois positivos; toda medida de atividade segura a conta."""
    t = a.pesos_do_modelo()
    positivas = set(t[t.coeficiente > 0].index)
    assert positivas == {"recencia_corte", "ticket_medio"}


# ---------------------------------------------------------------------------
# O limiar de decisão
# ---------------------------------------------------------------------------

def test_a_lista_de_138_contas_acerta_105(a):
    """O corte por capacidade operacional, medido na Aula 04."""
    r = a.lista_priorizada()
    assert r["n"] == 138
    assert round(r["limiar"], 3) == 0.873
    assert r["verdadeiros_positivos"] == 105
    assert r["falsos_positivos"] == 33
    assert r["falsos_negativos"] == 1488
    assert r["verdadeiros_negativos"] == 2122
    assert round(r["precisao"] * 100, 1) == 76.1
    assert round(r["revocacao"] * 100, 1) == 6.6
    assert round(r["acuracia"] * 100, 1) == 59.4


def test_o_limiar_padrao_de_05_marca_1295_contas(a):
    r = a.limiar_padrao()
    assert r["marcadas"] == 1295
    assert r["verdadeiros_positivos"] == 889
    assert r["falsos_positivos"] == 406
    assert round(r["precisao"] * 100, 1) == 68.6
    assert round(r["revocacao"] * 100, 1) == 55.8
    assert round(r["acuracia"] * 100, 1) == 70.4


def test_marcar_conta_nenhuma_ja_entrega_575_de_acuracia(a):
    """A linha de base que torna a acurácia inútil nesta população."""
    p = a.particao_temporal()
    assert round((1 - p["perdidas"] / p["contas"]) * 100, 1) == 57.5


def test_a_fila_de_138_nao_alcanca_mais_que_87_por_cento_das_perdas(a):
    """Mesmo um modelo perfeito bate no teto da capacidade. A revocação baixa
    mede a fila, e não a qualidade do escore."""
    p = a.particao_temporal()
    assert round(138 / p["perdidas"] * 100, 1) == 8.7


# ---------------------------------------------------------------------------
# A variável de sequência
# ---------------------------------------------------------------------------

FAIXAS_ESPERADAS = {
    "sem receita nos 3 meses": (735, 420, 57.1),
    "queda acima de 50%": (218, 37, 17.0),
    "queda até 50%": (2426, 1088, 44.8),
    "estável ou em alta": (369, 48, 13.0),
}


@pytest.mark.parametrize("faixa,esperado", sorted(FAIXAS_ESPERADAS.items()))
def test_a_prevalencia_por_faixa_da_razao(a, faixa, esperado):
    contas, perdidas, prevalencia = esperado
    t = a.perfil_da_razao()
    assert int(t.loc[faixa, "contas"]) == contas
    assert int(t.loc[faixa, "perdidas"]) == perdidas
    assert round(float(t.loc[faixa, "prevalencia"]) * 100, 1) == prevalencia


def test_as_quatro_faixas_cobrem_as_3748_elegiveis(a):
    assert int(a.perfil_da_razao().contas.sum()) == 3748


# ---------------------------------------------------------------------------
# A propriedade que sustenta a aula: nenhuma feature honesta cruza o corte
# ---------------------------------------------------------------------------

def test_nenhuma_feature_honesta_muda_quando_o_painel_e_truncado(a, monkeypatch):
    """Truncar o painel no corte não pode mudar nenhuma feature honesta.

    Este é o teste que pega o vazamento de verdade: os valores esperados acima
    continuariam batendo se alguém trocasse uma coluna por outra igualmente
    estável, mas uma coluna que lê a janela do rótulo muda de valor assim que
    essa janela some da entrada.

    Visto falhando: incluir `recencia_fim` na lista faz a comparação acusar
    3.748 diferenças, porque a recência do fim do painel depende do que foi
    apagado.
    """
    import pandas as pd

    completo = a.painel_de_features()[a.FEATURES_HONESTAS].copy()

    bruto = a.carregar()
    truncado = {
        "painel": bruto["painel"][bruto["painel"].periodo <= a.CORTE],
        "mix": bruto["mix"],
        "engajamento": bruto["engajamento"],
        "cadastro": bruto["cadastro"],
        "pedidos": bruto["pedidos"][bruto["pedidos"].periodo <= a.CORTE],
    }
    a.painel_de_features.cache_clear()
    a._pedidos.cache_clear()
    monkeypatch.setattr(a, "carregar", lambda: truncado)
    try:
        depois = a.painel_de_features()[a.FEATURES_HONESTAS].copy()
    finally:
        a.painel_de_features.cache_clear()
        a._pedidos.cache_clear()

    assert list(completo.index) == list(depois.index)
    for coluna in a.FEATURES_HONESTAS:
        diferentes = int((~pd.Series(
            completo[coluna].to_numpy() == depois[coluna].to_numpy())).sum())
        assert diferentes == 0, (coluna, diferentes)


# ---------------------------------------------------------------------------
# O deck migrou para a base longa em 12/09/2026
# ---------------------------------------------------------------------------
# As asserções de presença no deck viviam aqui. Elas foram para
# dados/tests/test_aula06_longa.py junto com o deck, que passou a usar a base
# de 65 meses. Este arquivo continua guardando dados/analise_aula06.py, que é
# o que o material de apoio cita.
