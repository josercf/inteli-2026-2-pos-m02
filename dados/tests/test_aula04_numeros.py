# -*- coding: utf-8 -*-
"""Trava os números da Aula 04 contra o dataset oficial.

Valores transcritos de forma literal, nunca importados do módulo de análise:
teste que importa a constante que o gerador usa concorda consigo mesmo.

Sem o xlsx em dados/, o módulo inteiro é pulado (ADR-005).
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
def an():
    import sys

    sys.path.insert(0, str(RAIZ))
    from dados import analise_aula04

    return analise_aula04


# ---------------------------------------------------------------------------
# Bloco 1: quem podia ser marcado
# ---------------------------------------------------------------------------

def test_as_tres_populacoes(an):
    p = an.populacoes()
    assert (p["carteira"]["contas"], p["carteira"]["perdidas"]) == (8282, 1593)
    assert round(p["carteira"]["prevalencia"], 3) == 0.192
    assert (p["elegiveis"]["contas"], p["elegiveis"]["perdidas"]) == (3748, 1593)
    assert round(p["elegiveis"]["prevalencia"], 3) == 0.425
    assert round(p["elegiveis"]["ic_inferior"], 3) == 0.409
    assert round(p["elegiveis"]["ic_superior"], 3) == 0.441
    assert (p["nao_elegiveis"]["contas"], p["nao_elegiveis"]["perdidas"]) == (4534, 0)


def test_elegivel_e_primeira_compra_ate_fevereiro_de_2025(an):
    c = an.contas_enriquecidas()
    assert c.elegivel.sum() == 3748
    assert c[c.elegivel].primeiro_mes.max() == "2025-02"
    assert c[~c.elegivel].primeiro_mes.min() == "2025-03"


def test_perfil_por_segmento_nas_elegiveis(an):
    t = an.perfil_por_segmento()
    esperado = {
        # segmento: (contas, perdidas, prev, receita mediana, dias, marcas, intervalo, marca dominante)
        "PUBLIC SECTOR": (449, 261, 0.581, 42388, 3, 3, 18.0, "DESKTOP"),
        "MID MARKET": (1508, 716, 0.475, 10016, 2, 2, 45.5, "NOTEBOOK"),
        "SMALL MARKET": (366, 173, 0.473, 7692, 2, 1, 20.0, "NOTEBOOK"),
        "LARGE ENTERPRISE": (786, 263, 0.335, 36926, 4, 3, 24.0, "NOTEBOOK"),
        "GLOBAL ACCOUNT": (568, 162, 0.285, 56294, 4, 3, 16.0, "NOTEBOOK"),
        "STRATEGIC ACCOUNT": (71, 18, 0.254, 125757, 8, 4, 12.0, "NOTEBOOK"),
    }
    assert list(t.index) == list(esperado)
    for seg, (n, k, prev, rec, dias, marcas, intervalo, dominante) in esperado.items():
        l = t.loc[seg]
        assert int(l.contas) == n and int(l.perdidas) == k
        assert round(l.prevalencia, 3) == prev
        assert round(l.receita_mediana) == rec
        assert l.dias_mediano == dias and l.marcas_mediana == marcas
        assert l.intervalo_mediano == intervalo
        assert l.marca_dominante == dominante


def test_periodicidade_so_existe_para_quem_comprou_duas_vezes(an):
    c = an.contas_enriquecidas()
    assert (c.dias_de_compra >= 2).sum() == 4910
    assert c.meses_ativos.median() == 2


# ---------------------------------------------------------------------------
# Bloco 2: a diferença é maior que o ruído
# ---------------------------------------------------------------------------

def test_prevalencia_por_segmento_com_ic(an):
    t, qui2, gl, p = an.tabela_com_ic("segmento")
    assert round(qui2, 1) == 143.8 and gl == 5 and p < 1e-20
    assert (round(t.loc["STRATEGIC ACCOUNT", "ic_inferior"], 3),
            round(t.loc["STRATEGIC ACCOUNT", "ic_superior"], 3)) == (0.167, 0.366)
    assert (round(t.loc["PUBLIC SECTOR", "ic_inferior"], 3),
            round(t.loc["PUBLIC SECTOR", "ic_superior"], 3)) == (0.535, 0.626)


def test_amplitude_de_mix(an):
    t, qui2, gl, _ = an.tabela_com_ic("faixa_marcas")
    assert round(qui2, 1) == 615.4 and gl == 3
    esperado = {"1": (1086, 721, 0.664, 0.635, 0.691),
                "2": (915, 471, 0.515, 0.482, 0.547),
                "3": (640, 223, 0.348, 0.313, 0.386),
                "4+": (1107, 178, 0.161, 0.140, 0.184)}
    for faixa, (n, k, prev, lo, hi) in esperado.items():
        l = t.loc[faixa]
        assert (int(l.contas), int(l.perdidas)) == (n, k)
        assert (round(l.prevalencia, 3), round(l.ic_inferior, 3), round(l.ic_superior, 3)) == (prev, lo, hi)


def test_frequencia_de_compra(an):
    t, qui2, gl, _ = an.tabela_com_ic("faixa_dias")
    assert round(qui2, 1) == 1671.4 and gl == 3
    esperado = {"1": (1194, 1020, 0.854), "2": (620, 324, 0.523),
                "3 a 5": (861, 189, 0.220), "6+": (1073, 60, 0.056)}
    for faixa, (n, k, prev) in esperado.items():
        l = t.loc[faixa]
        assert (int(l.contas), int(l.perdidas), round(l.prevalencia, 3)) == (n, k, prev)


def test_setor_nas_elegiveis(an):
    t, qui2, gl, _ = an.tabela_com_ic("setor")
    assert round(qui2, 1) == 93.9 and gl == 12
    assert (int(t.loc["GOVERNMENT", "contas"]), round(t.loc["GOVERNMENT", "prevalencia"], 3)) == (310, 0.597)
    assert (int(t.loc["EDUCATION", "contas"]), round(t.loc["EDUCATION", "prevalencia"], 3)) == (189, 0.556)
    assert (int(t.loc["WHOLESALE TRADE", "contas"]), round(t.loc["WHOLESALE TRADE", "prevalencia"], 3)) == (463, 0.341)


def test_regiao_nas_elegiveis(an):
    e = an.elegiveis()
    t, qui2, gl, _ = an.tabela_com_ic("regiao", e[e.regiao.isin(an.regioes_principais())])
    assert round(qui2, 1) == 33.5 and gl == 6
    assert (int(t.loc["BR", "contas"]), round(t.loc["BR", "prevalencia"], 3)) == (2171, 0.455)
    assert (int(t.loc["MX", "contas"]), round(t.loc["MX", "prevalencia"], 3)) == (551, 0.334)


def test_regiao_na_carteira_inteira(an):
    t, _, _, _ = an.tabela_com_ic("regiao", an.contas_enriquecidas())
    assert round(t.loc["BR", "prevalencia"], 3) == 0.282
    assert round(t.loc["MX", "prevalencia"], 3) == 0.125


def test_canal_e_engajamento_nao_respondem(an):
    assert an.canal_e_constante() is True
    e = an.engajamento_nas_elegiveis()
    assert e["contas_cobertas"] == 1560
    assert e["mediana_contatos_ativas"] == 4 and e["mediana_contatos_perdidas"] == 3


# ---------------------------------------------------------------------------
# Bloco 3: a hipótese sobrevive ao controle
# ---------------------------------------------------------------------------

def test_mix_sobrevive_ao_controle_por_segmento(an):
    t = an.estratificar("marcas", 1, 3, "segmento")
    esperado = {"GLOBAL ACCOUNT": (133, 0.632, 307, 0.114),
                "LARGE ENTERPRISE": (196, 0.668, 413, 0.143),
                "MID MARKET": (466, 0.674, 601, 0.251),
                "PUBLIC SECTOR": (83, 0.843, 273, 0.469),
                "SMALL MARKET": (192, 0.573, 105, 0.229)}
    for seg, (na, pa, nb, pb) in esperado.items():
        l = t.loc[seg]
        assert (int(l.n_a), round(l.prev_a, 3), int(l.n_b), round(l.prev_b, 3)) == (na, pa, nb, pb)
        assert l.hi_b < l.lo_a, seg


def test_mix_desaparece_sob_controle_por_frequencia(an):
    t = an.estratificar("marcas", 1, 3, "faixa_dias")
    esperado = {"1": (719, 0.815, 161, 0.925),
                "2": (198, 0.525, 204, 0.534),
                "3 a 5": (126, 0.214, 473, 0.203),
                "6+": (43, 0.093, 909, 0.052)}
    for faixa, (na, pa, nb, pb) in esperado.items():
        l = t.loc[faixa]
        assert (int(l.n_a), round(l.prev_a, 3), int(l.n_b), round(l.prev_b, 3)) == (na, pa, nb, pb)
    # Nas faixas 2, 3 a 5 e 6+, os intervalos se cruzam.
    for faixa in ("2", "3 a 5", "6+"):
        l = t.loc[faixa]
        assert max(l.lo_a, l.lo_b) <= min(l.hi_a, l.hi_b), faixa


def test_brasil_inverte_dentro_do_segmento(an):
    t = an.estratificar("regiao", "BR", "outros", "segmento")
    esperado = {"GLOBAL ACCOUNT": (161, 0.186, 407, 0.324),
                "LARGE ENTERPRISE": (381, 0.312, 405, 0.356),
                "MID MARKET": (1168, 0.482, 340, 0.450),
                "PUBLIC SECTOR": (346, 0.601, 103, 0.515),
                "SMALL MARKET": (73, 0.726, 293, 0.410)}
    for seg, (na, pa, nb, pb) in esperado.items():
        l = t.loc[seg]
        assert (int(l.n_a), round(l.prev_a, 3), int(l.n_b), round(l.prev_b, 3)) == (na, pa, nb, pb)
    c = an.composicao_br()
    assert round(c["share_mid_public_br"], 3) == 0.697
    assert round(c["share_mid_public_outros"], 3) == 0.281


# ---------------------------------------------------------------------------
# PBL e Bloco 4
# ---------------------------------------------------------------------------

def test_o_par_da_pbl(an):
    p = an.par_da_pbl()
    assert (p["candidatas"], p["ativas"], p["perdidas"]) == (66, 63, 3)
    a, b = p["conta_a"], p["conta_b"]
    assert a["segmento"] == b["segmento"] == "GLOBAL ACCOUNT"
    assert a["regiao"] == b["regiao"] == "BR"
    assert a["primeiro_mes"] == b["primeiro_mes"] == "2024-04"
    assert (a["churn"], b["churn"]) == (0, 1)
    assert (round(a["receita_semestre_1"]), round(a["receita_semestre_2"])) == (270790, 2499)
    assert (round(b["receita_semestre_1"]), round(b["receita_semestre_2"])) == (134697, 1840)
    assert (a["ultimo_mes"], b["ultimo_mes"]) == ("2025-04", "2024-12")
    assert (a["marcas"], b["marcas"]) == (3, 1)
    assert (a["dias_de_compra"], b["dias_de_compra"]) == (22, 28)
    assert list(p["series"].columns) == ["conta_a", "conta_b"]
    assert len(p["series"]) == 24


def test_fila_por_segmento_contra_a_capacidade(an):
    f = an.fila_por_segmento()
    assert f.to_dict() == {"MID MARKET": 716, "LARGE ENTERPRISE": 263, "PUBLIC SECTOR": 261,
                           "SMALL MARKET": 173, "GLOBAL ACCOUNT": 162, "STRATEGIC ACCOUNT": 18}
    assert an.CAPACIDADE_OPERACIONAL == 138
    assert (f > 138).sum() == 5
