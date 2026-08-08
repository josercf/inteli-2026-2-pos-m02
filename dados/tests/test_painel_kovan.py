# -*- coding: utf-8 -*-
"""
Trava os numeros canonicos do case sobre o painel gerado.

Cada teste aqui existe porque um numero especifico aparece impresso no case
(Case_Modulo2_Lenovo_Kovan_v2) ou no Caderno de Exhibits. Se o gerador mudar e
um desses numeros deixar de fechar, o material didatico passa a citar um numero
que o dado nao sustenta, e a aula quebra na frente da turma.

Rodar: python3 -m pytest dados/tests -q
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from dados.gerar_painel_kovan import (  # noqa: E402
    ANDIRA_ID,
    N_T,
    TALVERA,
    TALVERA_ID,
    TRIMESTRES,
    gerar,
)


@pytest.fixture(scope="module")
def painel() -> pd.DataFrame:
    return gerar()


@pytest.fixture(scope="module")
def limpo() -> pd.DataFrame:
    """Painel antes da injecao da receita ausente: a estrutura canonica.

    Nao serve reconstruir a lacuna por interpolacao: quando o trimestre
    ausente cai dentro de um episodio, a interpolacao suaviza justamente a
    queda que define o episodio, e a contagem por corte de limiar deixa de
    fechar. Foi assim que a primeira versao deste gerador perdeu dois dos 76
    episodios do corte de 25%. O painel entregue ao aluno segue com a lacuna:
    e o conteudo da segunda aula.
    """
    return gerar(com_lacunas=False)


# ---------------------------------------------------------------------------
# Deteccao de episodios: a definicao operacional usada pelo case
# ---------------------------------------------------------------------------


def episodios(df: pd.DataFrame, limiar: float, segmento: str = "Estrategico") -> pd.DataFrame:
    """Episodios de erosao: corridas maximas de duas ou mais quedas trimestre a
    trimestre consecutivas, cada uma de pelo menos `limiar`.

    Devolve uma linha por episodio, com a conta, o trimestre inicial e final.
    """
    base = df[df["segmento"] == segmento].copy()
    base["ordem"] = base["trimestre"].map({t: i for i, t in enumerate(TRIMESTRES)})
    base = base.sort_values(["conta_id", "ordem"])
    base["var"] = base.groupby("conta_id")["receita_brl"].pct_change()
    # Uma conta encerrada zera a receita: a queda para zero e ruptura, nao
    # episodio de erosao. O case conta episodios de contracao em conta que
    # segue comprando.
    base["em_queda"] = (base["var"] <= -limiar) & (base["receita_brl"] > 0)

    achados = []
    for conta_id, g in base.groupby("conta_id", sort=False):
        corrida = 0
        inicio = None
        for _, linha in g.iterrows():
            if linha["em_queda"]:
                corrida += 1
                if inicio is None:
                    inicio = linha["ordem"]
            else:
                if corrida >= 2:
                    achados.append(
                        {"conta_id": conta_id, "inicio": inicio, "fim": linha["ordem"] - 1}
                    )
                corrida, inicio = 0, None
        if corrida >= 2:
            achados.append({"conta_id": conta_id, "inicio": inicio, "fim": int(g["ordem"].max())})
    return pd.DataFrame(achados, columns=["conta_id", "inicio", "fim"])


def contas_rompidas(df: pd.DataFrame, segmento: str = "Estrategico") -> set[str]:
    base = df[df["segmento"] == segmento]
    return set(base.loc[base["status_conta"] == "Encerrada", "conta_id"].unique())


# ---------------------------------------------------------------------------
# Forma do painel (Exhibit 3)
# ---------------------------------------------------------------------------


def test_forma_do_painel(painel):
    assert len(painel) == 16_618
    assert painel["conta_id"].nunique() == 1_187
    assert painel["trimestre"].nunique() == 14
    assert list(painel["trimestre"].unique()) == TRIMESTRES or set(
        painel["trimestre"]
    ) == set(TRIMESTRES)


def test_colunas_do_dicionario(painel):
    esperadas = [
        "conta_id", "trimestre", "segmento", "regiao", "am_id", "receita_brl",
        "pedidos", "linhas_produto_ativas", "valor_medio_pedido_brl",
        "recencia_dias", "devolucoes_brl", "desconto_medio_pct",
        "oportunidades_abertas", "oportunidades_perdidas", "valor_pipeline_brl",
        "visitas_registradas", "interacoes_crm", "troca_de_am_no_trimestre",
        "status_conta", "taxonomia_mix",
    ]
    assert list(painel.columns) == esperadas


def test_o_painel_nao_traz_rotulo_de_risco(painel):
    """A decisao em aberto do case e justamente qual rotulo construir."""
    proibidas = {"churn", "risco", "propensao", "score", "rotulo", "label", "target"}
    for coluna in painel.columns:
        assert not any(p in coluna.lower() for p in proibidas), coluna


def test_tamanho_dos_segmentos(painel):
    contagem = painel.groupby("segmento")["conta_id"].nunique().to_dict()
    assert contagem == {"Estrategico": 118, "Medio": 356, "Cauda": 713}


def test_observacoes_do_segmento_estrategico(painel):
    assert len(painel[painel["segmento"] == "Estrategico"]) == 1_652


# ---------------------------------------------------------------------------
# Rupturas e prevalencia
# ---------------------------------------------------------------------------


def test_trinta_e_quatro_rupturas_no_segmento_estrategico(limpo):
    assert len(contas_rompidas(limpo)) == 34


def test_prevalencia_de_ruptura_de_dois_virgula_um_por_cento(limpo):
    assert len(contas_rompidas(limpo)) / 1_652 == pytest.approx(0.021, abs=0.001)


# ---------------------------------------------------------------------------
# Episodios de erosao por corte de limiar (Exhibit 5 e o registro de Otavio)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("limiar,esperado", [(0.10, 192), (0.15, 176), (0.25, 76)])
def test_contagem_de_episodios_por_corte(limpo, limiar, esperado):
    assert len(episodios(limpo, limiar)) == esperado


@pytest.mark.parametrize("limiar,esperado", [(0.10, 31), (0.15, 29), (0.25, 17)])
def test_rupturas_capturadas_por_corte(limpo, limiar, esperado):
    rompidas = contas_rompidas(limpo)
    com_episodio = set(episodios(limpo, limiar)["conta_id"])
    assert len(rompidas & com_episodio) == esperado


def test_cinco_rupturas_sem_episodio_detectavel_no_corte_de_quinze(limpo):
    """O registro de Otavio: cinco romperam a partir de patamar estavel."""
    rompidas = contas_rompidas(limpo)
    com_episodio = set(episodios(limpo, 0.15)["conta_id"])
    assert len(rompidas - com_episodio) == 5


# ---------------------------------------------------------------------------
# Desfecho dos 176 episodios do corte de 15%
# ---------------------------------------------------------------------------


def desfechos(df: pd.DataFrame) -> dict[str, int]:
    eps = episodios(df, 0.15)
    rompidas = contas_rompidas(df)
    base = df[df["segmento"] == "Estrategico"].copy()
    base["ordem"] = base["trimestre"].map({t: i for i, t in enumerate(TRIMESTRES)})
    receita = base.set_index(["conta_id", "ordem"])["receita_brl"]

    out = {"rompe": 0, "recupera": 0, "persiste": 0}
    for _, ep in eps.iterrows():
        if ep["conta_id"] in rompidas:
            out["rompe"] += 1
            continue
        antes = receita.get((ep["conta_id"], ep["inicio"] - 1), np.nan)
        vale = receita.get((ep["conta_id"], ep["fim"]), np.nan)
        depois = [
            receita.get((ep["conta_id"], ep["fim"] + k), np.nan) for k in (1, 2)
        ]
        depois = [v for v in depois if pd.notna(v)]
        # Recuperou: voltou ao patamar anterior ao episodio em ate dois
        # trimestres. Caso contrario, seguiu contraindo sem romper.
        if depois and max(depois) >= 0.95 * antes:
            out["recupera"] += 1
        else:
            out["persiste"] += 1
    return out


def test_desfecho_dos_episodios_bate_com_o_case(limpo):
    d = desfechos(limpo)
    assert d["rompe"] == 29
    assert d["recupera"] == 56
    assert d["persiste"] == 91
    assert sum(d.values()) == 176


def test_proporcao_de_recuperacao_espontanea(limpo):
    d = desfechos(limpo)
    assert d["recupera"] / 176 == pytest.approx(0.318, abs=0.005)


# ---------------------------------------------------------------------------
# O insight plantado: a ordem separa, a magnitude nao
# ---------------------------------------------------------------------------


def _magnitude_e_ordem(df: pd.DataFrame):
    """Para cada episodio de 15%: queda acumulada e se o mix estreitou antes."""
    eps = episodios(df, 0.15)
    rompidas = contas_rompidas(df)
    base = df[df["segmento"] == "Estrategico"].copy()
    base["ordem"] = base["trimestre"].map({t: i for i, t in enumerate(TRIMESTRES)})
    receita = base.set_index(["conta_id", "ordem"])["receita_brl"]
    mix = base.set_index(["conta_id", "ordem"])["linhas_produto_ativas"]

    linhas = []
    for _, ep in eps.iterrows():
        conta, i0, fim = ep["conta_id"], int(ep["inicio"]), int(ep["fim"])
        antes = receita.get((conta, i0 - 1), np.nan)
        vale = receita.get((conta, fim), np.nan)
        if pd.isna(antes) or pd.isna(vale) or antes <= 0:
            continue
        mix_antes = mix.get((conta, i0 - 2), np.nan)
        mix_no_inicio = mix.get((conta, i0 - 1), np.nan)
        if pd.isna(mix_antes) or pd.isna(mix_no_inicio):
            continue
        d = desfechos_de_um(df, conta, i0, fim, rompidas, receita)
        linhas.append(
            {
                "conta_id": conta,
                "queda_pct": 1 - vale / antes,
                # O mix ja tinha estreitado no trimestre anterior a primeira
                # queda de receita?
                "mix_liderou": bool(mix_no_inicio < mix_antes),
                "reversivel": d == "recupera",
            }
        )
    return pd.DataFrame(linhas)


def desfechos_de_um(df, conta, i0, fim, rompidas, receita) -> str:
    if conta in rompidas:
        return "rompe"
    antes = receita.get((conta, i0 - 1), np.nan)
    depois = [receita.get((conta, fim + k), np.nan) for k in (1, 2)]
    depois = [v for v in depois if pd.notna(v)]
    if depois and max(depois) >= 0.95 * antes:
        return "recupera"
    return "persiste"


def test_a_magnitude_da_queda_nao_separa_reversivel_de_irreversivel(limpo):
    """O que Otavio escreveu e classificou como nao testado."""
    d = _magnitude_e_ordem(limpo)
    rev = d[d["reversivel"]]["queda_pct"].mean()
    irrev = d[~d["reversivel"]]["queda_pct"].mean()
    assert abs(rev - irrev) < 0.06, (rev, irrev)


def test_a_ordem_dos_sinais_separa_reversivel_de_irreversivel(limpo):
    """O insight que a EDA precisa descobrir, e que o texto do case nao entrega."""
    d = _magnitude_e_ordem(limpo)
    lidera_entre_irreversiveis = d[~d["reversivel"]]["mix_liderou"].mean()
    lidera_entre_reversiveis = d[d["reversivel"]]["mix_liderou"].mean()
    # Forte o bastante para ser achado numa tarde, sujo o bastante para exigir
    # evidencia: nem 100% de um lado nem 0% do outro.
    assert 0.62 < lidera_entre_irreversiveis < 0.92, lidera_entre_irreversiveis
    assert 0.02 < lidera_entre_reversiveis < 0.28, lidera_entre_reversiveis
    # E a separacao precisa ser grande o bastante para sobreviver a uma tabela
    # de contingencia montada as pressas por um grupo em 30 minutos.
    assert lidera_entre_irreversiveis / lidera_entre_reversiveis > 4.0


# ---------------------------------------------------------------------------
# NRR do cohort (Exhibit 2)
# ---------------------------------------------------------------------------


def _receita_anual(df: pd.DataFrame, ano: int) -> float:
    base = df[(df["segmento"] == "Estrategico") & (df["trimestre"].str.startswith(str(ano)))]
    return float(base["receita_brl"].sum())


def test_nrr_do_segmento_estrategico(limpo):
    r2023 = _receita_anual(limpo, 2023) / 1e6
    r2024 = _receita_anual(limpo, 2024) / 1e6
    r2025 = _receita_anual(limpo, 2025) / 1e6
    assert r2023 == pytest.approx(1296.8, rel=0.02)
    assert r2024 / r2023 == pytest.approx(1.090, abs=0.015)
    assert r2025 / r2024 == pytest.approx(0.930, abs=0.015)


def test_o_painel_entregue_nao_fecha_com_o_razao_contabil(painel):
    """Nota metodologica do Exhibit 2: o painel tem lacuna de extracao."""
    entregue = _receita_anual(painel, 2024) / 1e6
    lacuna = 1 - entregue / 1412.9
    assert 0.003 < lacuna < 0.035, lacuna


# ---------------------------------------------------------------------------
# Advertencias de qualidade do dado (Exhibit 3)
# ---------------------------------------------------------------------------


def test_advertencia_1_cerca_de_um_por_cento_de_receita_ausente(painel):
    ativos = painel[painel["status_conta"] == "Ativa"]
    fracao = ativos["receita_brl"].isna().mean()
    assert 0.008 <= fracao <= 0.013


def test_advertencia_2_devolucoes_sempre_em_valor_negativo(painel):
    assert (painel["devolucoes_brl"] <= 0).all()


def test_advertencia_3_mix_da_um_salto_artificial_na_virada_da_taxonomia(painel):
    """A quebra e de taxonomia, nao de comportamento da conta.

    Comparar a media de todo o periodo pre_2023 contra a media de todo o
    pos_2023 mistura duas coisas: o salto de taxonomia e a erosao de mix que se
    acumula em 2024 e 2025. O teste olha os dois trimestres adjacentes a
    virada, so nas contas em que nenhum episodio mexeu no mix ali, e o salto
    tem que ser de exatamente duas linhas: as tres de infraestrutura que ate
    2022Q4 eram registradas como uma so.
    """
    base = painel[painel["segmento"] == "Estrategico"]
    largo = base.pivot(index="conta_id", columns="trimestre", values="linhas_produto_ativas")
    estaveis = largo[
        (largo["2022Q3"] == largo["2022Q4"]) & (largo["2023Q1"] == largo["2023Q2"])
    ]
    salto = estaveis["2023Q1"] - estaveis["2022Q4"]
    assert len(estaveis) > 40, len(estaveis)
    assert (salto == 2).all(), salto.value_counts().to_dict()


def test_advertencia_4_engajamento_incompleto_e_desigual(painel):
    ativos = painel[painel["status_conta"] == "Ativa"]
    janela = ativos[ativos["trimestre"] >= "2023Q2"]
    cobertura = janela["interacoes_crm"].notna().mean()
    assert 0.60 <= cobertura <= 0.75, cobertura
    # A cobertura e pior nas contas menores, como o case afirma.
    por_segmento = janela.groupby("segmento")["interacoes_crm"].apply(lambda s: s.notna().mean())
    assert por_segmento["Estrategico"] > por_segmento["Cauda"]


def test_atividade_do_am_so_existe_a_partir_de_2023Q2(painel):
    antes = painel[painel["trimestre"] < "2023Q2"]
    assert antes["interacoes_crm"].isna().all()
    assert antes["visitas_registradas"].isna().all()


# ---------------------------------------------------------------------------
# Confundidor de troca de Account Manager
# ---------------------------------------------------------------------------


def test_onze_territorios_trocam_de_am_em_2025(painel):
    em_2025 = painel[painel["trimestre"].str.startswith("2025")]
    territorios = em_2025.loc[em_2025["troca_de_am_no_trimestre"] == 1, "am_id"].nunique()
    assert territorios == 11


def test_troca_de_am_derruba_a_atividade_registrada(painel):
    com_atividade = painel[painel["interacoes_crm"].notna()]
    com_troca = com_atividade[com_atividade["troca_de_am_no_trimestre"] == 1]["interacoes_crm"].mean()
    sem_troca = com_atividade[com_atividade["troca_de_am_no_trimestre"] == 0]["interacoes_crm"].mean()
    assert com_troca < 0.6 * sem_troca, (com_troca, sem_troca)


# ---------------------------------------------------------------------------
# Contas nomeadas pelo case
# ---------------------------------------------------------------------------


# Exhibit 1, transcrito do Caderno de Exhibits. Os valores ficam aqui de forma
# literal, e nao importados do gerador, de proposito: importar a mesma
# constante que o gerador usa faz o teste concordar consigo mesmo. Uma versao
# anterior deste arquivo fazia isso e passava mesmo depois de o mix do Talvera
# ser alterado, que e justamente a assinatura que o exhibit existe para provar.
EXHIBIT_1 = [
    # trimestre, receita, pedidos, linhas de produto, recencia em dias
    ("2024Q3", 9_239_623.49, 14, 6, 9),
    ("2024Q4", 9_245_926.85, 14, 6, 25),
    ("2025Q1", 9_006_362.75, 25, 5, 20),
    ("2025Q2", 7_925_599.22, 15, 4, 23),
    ("2025Q3", 6_419_735.37, 12, 3, 25),
    ("2025Q4", 4_686_406.82, 7, 2, 19),
]


def test_grupo_talvera_bate_linha_a_linha_com_o_exhibit_1(painel):
    t = painel[painel["conta_id"] == TALVERA_ID].set_index("trimestre")
    assert t["am_id"].iloc[0] == "AM-41"
    for trimestre, receita, pedidos, linhas, recencia in EXHIBIT_1:
        assert t.loc[trimestre, "receita_brl"] == pytest.approx(receita, abs=0.01), trimestre
        assert t.loc[trimestre, "pedidos"] == pedidos, trimestre
        assert t.loc[trimestre, "linhas_produto_ativas"] == linhas, trimestre
        assert t.loc[trimestre, "recencia_dias"] == recencia, trimestre


def test_talvera_estreita_o_mix_de_seis_para_duas_linhas(painel):
    """A assinatura do case: o mix estreitou junto com a receita."""
    t = painel[painel["conta_id"] == TALVERA_ID].set_index("trimestre")
    mix = [t.loc[q, "linhas_produto_ativas"] for q, *_ in EXHIBIT_1]
    assert mix[0] == 6 and mix[-1] == 2
    assert all(b <= a for a, b in zip(mix, mix[1:])), mix


def test_talvera_segue_ativa_no_painel(painel):
    """Ele encerra o contrato em janeiro de 2026, depois da janela."""
    t = painel[painel["conta_id"] == TALVERA_ID]
    assert (t["status_conta"] == "Ativa").all()


def test_grupo_andira_cai_mais_que_o_talvera_e_nao_estreita_o_mix(painel):
    a = painel[painel["conta_id"] == ANDIRA_ID].set_index("trimestre")
    assert a.loc["2024Q2", "receita_brl"] / a.loc["2024Q1", "receita_brl"] - 1 == pytest.approx(
        -0.35, abs=0.02
    )
    assert a.loc["2024Q3", "receita_brl"] / a.loc["2024Q2", "receita_brl"] - 1 == pytest.approx(
        -0.28, abs=0.02
    )
    assert a.loc["2024Q4", "receita_brl"] > a.loc["2024Q1", "receita_brl"]
    # O contraexemplo: a receita despencou e o mix nunca estreitou. A leitura
    # vale sobre a taxonomia nova; em 2022 a contagem e menor por causa da
    # advertencia 3, que nao tem nada a ver com o comportamento da conta.
    pos = a[a["taxonomia_mix"] == "pos_2023"]
    assert (pos["linhas_produto_ativas"] == 6).all()


# ---------------------------------------------------------------------------
# Volume de contracao na base inteira
# ---------------------------------------------------------------------------


def test_media_de_episodios_por_trimestre_na_base(limpo):
    """O case: media de 82 por trimestre, faixa entre 22 e 154."""
    total = []
    for segmento in ("Estrategico", "Medio", "Cauda"):
        eps = episodios(limpo, 0.15, segmento=segmento)
        total.append(eps)
    eps = pd.concat(total)
    # Um episodio e detectado no trimestre em que fecha a segunda queda. Os
    # dois primeiros trimestres da janela nao tem historico para detectar nada,
    # e o ultimo trunca corridas em andamento: a faixa do case vale sobre os
    # trimestres em que a deteccao e possivel de ponta a ponta.
    por_trimestre = eps.groupby("fim").size().reindex(range(2, N_T - 1), fill_value=0)
    assert 68 <= por_trimestre.mean() <= 96, por_trimestre.mean()
    assert por_trimestre.min() >= 22, por_trimestre.to_dict()
    assert por_trimestre.max() <= 154, por_trimestre.to_dict()


# ---------------------------------------------------------------------------
# Reprodutibilidade
# ---------------------------------------------------------------------------


def test_geracao_e_deterministica():
    a = gerar()
    b = gerar()
    pd.testing.assert_frame_equal(a, b)


# ---------------------------------------------------------------------------
# Mecanismos de ausencia: o exercicio da Aula 01 depende do contraste
# ---------------------------------------------------------------------------


def test_ausencia_de_receita_e_uniforme_entre_segmentos(painel):
    """Compativel com "completamente ao acaso": e a ausencia por atraso no
    fechamento contabil, que nao tem relacao com a conta.

    Se este contraste sumir, o exercicio de mecanismo de ausencia da Aula 01
    deixa de ter as duas pontas que ele compara.
    """
    taxa = painel.groupby("segmento")["receita_brl"].apply(lambda s: s.isna().mean())
    assert taxa.max() / taxa.min() < 1.8, taxa.round(4).to_dict()


def test_ausencia_de_engajamento_depende_do_segmento(painel):
    """NAO e completamente ao acaso: a cobertura e pior nas contas menores, como
    a advertencia 4 do Exhibit 3 afirma. E a outra ponta do contraste."""
    janela = painel[painel["trimestre"] >= "2023Q2"]
    taxa = janela.groupby("segmento")["interacoes_crm"].apply(lambda s: s.isna().mean())
    assert taxa.max() / taxa.min() > 2.5, taxa.round(4).to_dict()
    assert taxa["Cauda"] > taxa["Estrategico"], taxa.round(4).to_dict()
