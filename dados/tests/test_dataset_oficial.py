# -*- coding: utf-8 -*-
"""Trava os números da Aula 03 contra o dataset oficial da Lenovo.

Os valores são transcritos de forma literal. Importar a constante que o material
usa faria o teste concordar consigo mesmo: foi assim que o teste do Grupo
Talvera passou mesmo com o dado alterado, na Aula 01.

O xlsx não é versionado (ADR-005). Sem ele em `dados/`, o módulo inteiro é
pulado, e a ausência aparece como skip e não como falha: quem clona o acervo
público não tem o arquivo e não deveria ver a suíte vermelha por isso.
"""

from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
XLSX = RAIZ / "dados" / "datasets_case_modulo2.xlsx"

pytestmark = pytest.mark.skipif(
    not XLSX.exists(),
    reason="dados/datasets_case_modulo2.xlsx ausente: dado real, distribuído fora do repositório",
)


@pytest.fixture(scope="module")
def analise():
    import sys

    sys.path.insert(0, str(RAIZ))
    from dados import analise_aula03

    return analise_aula03


# ---------------------------------------------------------------------------
# Formato das cinco abas, slide de abertura
# ---------------------------------------------------------------------------

def test_formato_das_abas(analise):
    assert analise.formato_das_abas() == {
        "painel": (24071, 7),
        "mix": (19948, 4),
        "engajamento": (80848, 6),
        "cadastro": (8382, 6),
        "pedidos": (207826, 18),
    }


def test_total_de_linhas_das_cinco_abas(analise):
    assert analise.total_de_linhas() == 341075


def test_grao_do_painel(analise):
    q = analise.qualidade()
    assert q["contas"] == 8282
    assert q["meses"] == 24
    assert q["primeiro_mes"] == "2024-04"
    assert q["ultimo_mes"] == "2026-03"


# ---------------------------------------------------------------------------
# As advertências de qualidade que substituem as do painel sintético
# ---------------------------------------------------------------------------

def test_engajamento_quase_nao_cruza_com_o_painel(analise):
    q = analise.qualidade()
    assert q["engaj_contas"] == 47185
    assert q["engaj_fora_do_painel"] == 44140
    assert q["engaj_dentro_do_painel"] == 3045
    assert round(q["engaj_cobertura"], 3) == 0.368


def test_grao_temporal_incompativel(analise):
    # Painel mensal com 24 períodos, engajamento trimestral com 14.
    q = analise.qualidade()
    assert q["meses"] == 24
    assert q["engaj_periodos"] == 14


def test_cadastro_repete_conta(analise):
    assert analise.qualidade()["cadastro_duplicado"] == 100


def test_mix_tem_participacao_ausente(analise):
    assert analise.qualidade()["mix_pct_nulo"] == 53


def test_receita_negativa_e_zerada(analise):
    q = analise.qualidade()
    assert q["receita_negativa"] == 25
    assert q["receita_zero"] == 143


# ---------------------------------------------------------------------------
# Univariada, Bloco 2
# ---------------------------------------------------------------------------

def test_receita_por_conta_tem_media_muito_acima_da_mediana(analise):
    r = analise.receita_univariada()
    assert round(r["media"]) == 437588
    assert round(r["mediana"]) == 18552
    assert round(r["maximo"]) == 377639854
    # O título da figura de distribuição afirma "24 vezes".
    assert round(r["razao_media_mediana"]) == 24


def test_forma_da_distribuicao_de_receita(analise):
    r = analise.receita_univariada()
    assert round(r["assimetria"], 1) == 44.5
    assert round(r["curtose"]) == 2597
    # Em log10 a assimetria some: é o argumento da transformação no slide.
    assert abs(r["assimetria_log10"]) < 0.5


def test_concentracao_da_receita(analise):
    p = analise.pareto()
    assert round(p[0.01], 3) == 0.651
    assert round(p[0.05], 3) == 0.844
    assert round(p[0.10], 3) == 0.906


# ---------------------------------------------------------------------------
# Bivariada, Bloco 3
# ---------------------------------------------------------------------------

def test_prevalencia_de_churn_na_carteira(analise):
    p = analise.perfil_do_rotulo()
    assert p["contas_perdidas"] == 1593
    assert round(p["prevalencia"], 3) == 0.192


def test_prevalencia_por_segmento(analise):
    t = analise.prevalencia_por("segmento")
    esperado = {
        "PUBLIC SECTOR": (837, 261, 0.312, 0.219),
        "MID MARKET": (3134, 716, 0.228, 0.103),
        "STRATEGIC ACCOUNT": (117, 18, 0.154, 0.063),
        "LARGE ENTERPRISE": (1711, 263, 0.154, 0.219),
        "SMALL MARKET": (1234, 173, 0.140, 0.267),
        "GLOBAL ACCOUNT": (1249, 162, 0.130, 0.129),
    }
    for segmento, (contas, perdidas, prev, receita) in esperado.items():
        linha = t.loc[segmento]
        assert int(linha["contas"]) == contas
        assert int(linha["perdidas"]) == perdidas
        assert round(linha["prevalencia"], 3) == prev
        assert round(linha["participacao_receita"], 3) == receita


def test_public_sector_lidera_prevalencia(analise):
    # O slide afirma que o segmento de maior prevalência não é o de menor receita.
    t = analise.prevalencia_por("segmento")
    assert t.index[0] == "PUBLIC SECTOR"
    assert t.loc["PUBLIC SECTOR", "participacao_receita"] > t.loc["MID MARKET", "participacao_receita"]


def test_prevalencia_por_setor_no_topo(analise):
    t = analise.prevalencia_por("setor")
    assert t.index[0] == "GOVERNMENT"
    assert int(t.loc["GOVERNMENT", "contas"]) == 631
    assert round(t.loc["GOVERNMENT", "prevalencia"], 3) == 0.293
    assert int(t.loc["EDUCATION", "contas"]) == 434
    assert round(t.loc["EDUCATION", "prevalencia"], 3) == 0.242


# ---------------------------------------------------------------------------
# O rótulo, que é o eixo da aula
# ---------------------------------------------------------------------------

def test_rotulo_e_constante_dentro_da_conta(analise):
    assert analise.perfil_do_rotulo()["rotulo_constante_na_conta"] is True


def test_contingencia_separa_o_rotulo_pelo_ultimo_mes(analise):
    ct = analise.contingencia_rotulo()
    # Antes de 2025-02 não há conta ativa; depois não há conta perdida.
    assert ct.loc["2024-04":"2025-01", 0].sum() == 0
    assert ct.loc["2024-04":"2025-01", 1].sum() == 1482
    assert ct.loc["2025-02", 0] == 382
    assert ct.loc["2025-02", 1] == 111
    assert ct.loc["2025-03":"2026-03", 1].sum() == 0
    assert ct.loc["2025-03":"2026-03", 0].sum() == 6307


def test_corte_mensal_captura_tudo_e_marca_a_mais(analise):
    cortes = analise.limiar_de_inatividade()
    assert cortes[13]["fila"] == 1975
    assert cortes[13]["captura_do_rotulo_oficial"] == 1.0
    assert analise.corte_diario_do_rotulo()["sobra_do_corte_mensal"] == 382


def test_a_regra_do_rotulo_e_diaria(analise):
    d = analise.corte_diario_do_rotulo()
    assert d["ultima_compra_maxima_das_perdidas"] == "2025-02-08"
    assert d["ultima_compra_minima_das_ativas"] == "2025-02-10"
    assert d["separacao_perfeita"] is True
    assert d["contas_no_mes_de_sobreposicao"] == 493


def test_fila_cresce_conforme_o_corte_afrouxa(analise):
    cortes = analise.limiar_de_inatividade()
    assert cortes[6]["fila"] == 5128
    assert cortes[9]["fila"] == 3719
    assert cortes[12]["fila"] == 2716
    assert cortes[13]["fila"] == 1975
    assert cortes[6]["fila"] > cortes[9]["fila"] > cortes[12]["fila"] > cortes[13]["fila"]


def test_nenhuma_conta_nova_aparece_como_perdida(analise):
    t = analise.tempo_de_casa_por_rotulo()
    assert t["piso_de_tempo_das_perdidas"] == 17
    assert t["contas_com_menos_de_17_meses"] == 4494
    assert t["perdidas_entre_elas"] == 0
