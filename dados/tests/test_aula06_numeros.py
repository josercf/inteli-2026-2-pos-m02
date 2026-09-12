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

import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

DECK = RAIZ / "aulas" / "aula06.html"
XLSX = RAIZ / "dados" / "datasets_case_modulo2.xlsx"

pytestmark = pytest.mark.skipif(
    not XLSX.exists(), reason="dataset oficial não versionado (ADR-005)")


@pytest.fixture(scope="module")
def a():
    from dados import analise_aula06

    return analise_aula06


@pytest.fixture(scope="module")
def deck() -> str:
    return DECK.read_text(encoding="utf-8")


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
# O deck cita os mesmos números
# ---------------------------------------------------------------------------

NUMEROS_NO_DECK = [
    "3.748", "1.593", "42,5%", "2025-02", "2024-04", "2026-03", "2025-03",
    "0,994", "0,885", "0,752", "0,772", "0,693", "0,680", "0,618", "0,608",
    "0,567", "0,540", "89,8%", "3.366", "0,794", "0,995", "0,201",
    "+0,804", "2,234", "33,1%", "-0,588", "0,555", "24,2%",
    "-0,554", "0,574", "22,8%", "-0,159", "0,853", "6,6%",
    "80,1%", "10,0%", "13,3%",
    "735", "420", "57,1%", "218", "17,0%", "2.426", "1.088", "44,8%",
    "369", "13,0%",
]


@pytest.mark.parametrize("numero", NUMEROS_NO_DECK)
def test_o_numero_aparece_no_deck(deck, numero):
    assert numero in deck, numero


def test_o_deck_nao_cita_numero_de_auc_fora_da_faixa_medida(deck):
    """Uma AUC solta no texto, escrita à mão e nunca medida, é o defeito que
    esta trava procura. Toda AUC citada precisa estar na lista acima."""
    citadas = set(re.findall(r"0,\d{3}", deck))
    conhecidas = {n.lstrip("+-") for n in NUMEROS_NO_DECK
                  if re.fullmatch(r"[+-]?0,\d{3}", n)}
    # As razões de chances e os coeficientes menores, que a lista acima cobre
    # por linha da tabela de pesos.
    conhecidas |= {"0,555", "0,574", "0,853", "0,892", "0,923",
                   "0,129", "0,114", "0,080"}
    assert citadas <= conhecidas, citadas - conhecidas
