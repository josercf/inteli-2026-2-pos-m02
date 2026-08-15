# -*- coding: utf-8 -*-
"""Trava os números da Aula 02 contra o painel entregue.

O painel lido aqui é `dados/kovan_painel_contas.csv`, a base COM as lacunas,
que é a mesma que a turma recebe. Os valores são transcritos de forma literal:
importar a constante que o material usa faria o teste concordar consigo mesmo.
"""

from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
CSV = RAIZ / "dados" / "kovan_painel_contas.csv"

SEGMENTOS = ("Cauda", "Estrategico", "Medio")


@pytest.fixture(scope="module")
def painel() -> pd.DataFrame:
    return pd.read_csv(CSV)


def visitas_por_segmento(df: pd.DataFrame, tratamento: str) -> pd.Series:
    """Visitas médias por segmento sob cada decisão de tratamento.

    `zero` preenche a ausência com 0; `excluir` descarta a linha sem registro.
    """
    if tratamento == "zero":
        base = df.assign(v=df["visitas_registradas"].fillna(0))
    elif tratamento == "excluir":
        base = df.dropna(subset=["visitas_registradas"]).rename(
            columns={"visitas_registradas": "v"}
        )
    else:
        raise ValueError(f"tratamento desconhecido: {tratamento}")
    return base.groupby("segmento")["v"].mean()


# --- Advertência 1: receita ausente -----------------------------------------


def test_cento_e_sessenta_linhas_sem_receita(painel):
    assert int(painel["receita_brl"].isna().sum()) == 160


def test_toda_receita_ausente_esta_em_conta_ativa(painel):
    faltando = painel[painel["receita_brl"].isna()]
    assert sorted(faltando["status_conta"].unique()) == ["Ativa"]


def test_valor_medio_do_pedido_falta_nas_mesmas_linhas(painel):
    assert painel["receita_brl"].isna().equals(painel["valor_medio_pedido_brl"].isna())


def test_quatorze_lacunas_de_receita_no_segmento_estrategico(painel):
    estrategico = painel[painel["segmento"] == "Estrategico"]
    assert int(estrategico["receita_brl"].isna().sum()) == 14


# --- Advertência 2: engajamento incompleto e enviesado ----------------------


def test_oito_mil_duzentas_e_oitenta_linhas_sem_engajamento(painel):
    assert int(painel["visitas_registradas"].isna().sum()) == 8_280
    assert int(painel["interacoes_crm"].isna().sum()) == 8_280


def test_visita_e_interacao_faltam_sempre_juntas(painel):
    assert painel["visitas_registradas"].isna().equals(painel["interacoes_crm"].isna())


@pytest.mark.parametrize(
    "segmento,esperado",
    [("Estrategico", 0.2942), ("Medio", 0.4990), ("Cauda", 0.5317)],
)
def test_taxa_de_ausencia_de_engajamento_por_segmento(painel, segmento, esperado):
    base = painel[painel["segmento"] == segmento]
    assert base["visitas_registradas"].isna().mean() == pytest.approx(esperado, abs=0.0001)


@pytest.mark.parametrize(
    "segmento,esperado",
    [("Cauda", 2.1012), ("Medio", 2.2959), ("Estrategico", 2.4479)],
)
def test_visitas_medias_tratando_ausente_como_zero(painel, segmento, esperado):
    assert visitas_por_segmento(painel, "zero")[segmento] == pytest.approx(
        esperado, abs=0.0001
    )


@pytest.mark.parametrize(
    "segmento,esperado",
    [("Estrategico", 3.4683), ("Cauda", 4.4864), ("Medio", 4.5827)],
)
def test_visitas_medias_excluindo_ausentes(painel, segmento, esperado):
    assert visitas_por_segmento(painel, "excluir")[segmento] == pytest.approx(
        esperado, abs=0.0001
    )


def test_a_ordem_dos_segmentos_inverte_entre_os_dois_tratamentos(painel):
    """O achado da aula.

    Preenchendo com zero, o segmento estratégico tem a MAIOR média de visitas
    dos três. Excluindo as linhas sem registro, ele tem a MENOR. As duas
    leituras sustentam recomendações opostas sobre cobertura comercial.
    """
    zero = visitas_por_segmento(painel, "zero").sort_values()
    excluir = visitas_por_segmento(painel, "excluir").sort_values()

    assert list(zero.index) == ["Cauda", "Medio", "Estrategico"]
    assert list(excluir.index) == ["Estrategico", "Cauda", "Medio"]

    assert zero.index[-1] == "Estrategico", "com zero, o estrategico e o maior"
    assert excluir.index[0] == "Estrategico", "excluindo, o estrategico e o menor"


@pytest.mark.parametrize(
    "tratamento,rompeu,nao_rompeu",
    [("zero", 1.5063, 2.8291), ("excluir", 2.2476, 3.9280)],
)
def test_visitas_de_quem_rompeu_no_estrategico(painel, tratamento, rompeu, nao_rompeu):
    estrategico = painel[painel["segmento"] == "Estrategico"]
    rompidas = set(
        estrategico.loc[estrategico["status_conta"] == "Encerrada", "conta_id"]
    )
    marcado = estrategico.assign(rompeu=estrategico["conta_id"].isin(rompidas))
    if tratamento == "zero":
        marcado = marcado.assign(v=marcado["visitas_registradas"].fillna(0))
    else:
        marcado = marcado.dropna(subset=["visitas_registradas"]).rename(
            columns={"visitas_registradas": "v"}
        )
    media = marcado.groupby("rompeu")["v"].mean()
    assert media[True] == pytest.approx(rompeu, abs=0.0001)
    assert media[False] == pytest.approx(nao_rompeu, abs=0.0001)


# --- Advertência 3: mudança de taxonomia em 2023Q1 --------------------------


def test_taxonomia_antiga_existe_apenas_em_dois_trimestres(painel):
    antiga = painel[painel["taxonomia_mix"] == "pre_2023"]
    assert sorted(antiga["trimestre"].unique()) == ["2022Q3", "2022Q4"]


@pytest.mark.parametrize(
    "trimestre,esperado",
    [("2022Q4", 1.8484), ("2023Q1", 3.6698), ("2025Q4", 2.5535)],
)
def test_media_de_linhas_de_produto_por_trimestre(painel, trimestre, esperado):
    base = painel[painel["trimestre"] == trimestre]
    assert base["linhas_produto_ativas"].mean() == pytest.approx(esperado, abs=0.0001)


def test_o_salto_da_taxonomia_e_de_noventa_e_oito_e_meio_por_cento(painel):
    media = painel.groupby("trimestre")["linhas_produto_ativas"].mean()
    salto = media["2023Q1"] / media["2022Q4"] - 1
    assert salto == pytest.approx(0.985, abs=0.001)


def test_a_erosao_dentro_da_taxonomia_comparavel_e_de_trinta_por_cento(painel):
    media = painel.groupby("trimestre")["linhas_produto_ativas"].mean()
    queda = media["2025Q4"] / media["2023Q1"] - 1
    assert queda == pytest.approx(-0.304, abs=0.001)


def test_a_janela_completa_inverte_o_sinal_da_erosao(painel):
    """Comparar 2022Q4 com 2025Q4 mostra crescimento onde houve queda."""
    media = painel.groupby("trimestre")["linhas_produto_ativas"].mean()
    aparente = media["2025Q4"] / media["2022Q4"] - 1
    real = media["2025Q4"] / media["2023Q1"] - 1
    assert aparente == pytest.approx(0.381, abs=0.001)
    assert aparente > 0 > real


# --- Advertência 4: devoluções em coluna própria, com sinal negativo --------


def test_devolucoes_nunca_sao_positivas(painel):
    assert int((painel["devolucoes_brl"] > 0).sum()) == 0
    assert int((painel["devolucoes_brl"] < 0).sum()) == 15_999
    assert int((painel["devolucoes_brl"] == 0).sum()) == 619


def test_o_erro_de_sinal_custa_duzentos_e_dezessete_milhoes(painel):
    bruta = painel["receita_brl"].sum()
    devolucoes = painel["devolucoes_brl"].sum()
    assert bruta == pytest.approx(8_406_227_803.71, abs=0.01)
    assert (bruta + devolucoes) == pytest.approx(8_297_527_227.90, abs=0.01)
    assert (bruta - devolucoes) == pytest.approx(8_514_928_379.52, abs=0.01)
    assert abs(2 * devolucoes) == pytest.approx(217_401_151.62, abs=0.01)
