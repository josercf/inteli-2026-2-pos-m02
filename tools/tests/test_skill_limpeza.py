# -*- coding: utf-8 -*-
"""O esqueleto da skill precisa cobrir as quatro advertências e permanecer
portátil entre agentes."""

from pathlib import Path
import sys

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from tools.check_retorica import analisar  # noqa: E402

SKILL = RAIZ / "materiais" / "skill-limpeza-kovan.md"


@pytest.fixture(scope="module")
def texto() -> str:
    return SKILL.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "coluna",
    ["receita_brl", "visitas_registradas", "interacoes_crm", "taxonomia_mix", "devolucoes_brl"],
)
def test_o_esqueleto_pede_decisao_para_cada_coluna_afetada(texto, coluna):
    assert coluna in texto


def test_o_esqueleto_tem_uma_lacuna_por_advertencia(texto):
    assert texto.count("PREENCHER") == 4


def test_o_esqueleto_exige_o_custo_medido(texto):
    """O custo mede o indicador que a decisão afeta, recalculado sob as duas
    alternativas, não a contagem de linhas: imputar não move linha nenhuma e
    zeraria o custo para metade das decisões possíveis."""
    minusculo = texto.lower()
    assert "custo medido" in minusculo
    assert "indicador afetado" in minusculo
    assert "valor do indicador com a decisão" in minusculo or "valor do indicador com a decisao" in minusculo
    assert "valor do indicador com a alternativa descartada" in minusculo
    assert "linhas afetadas" in minusculo


def test_o_esqueleto_e_markdown_puro(texto):
    """Sem sintaxe proprietária de agente: ele roda colado no Gemini e lido
    por um agente que trabalha sobre arquivos."""
    for proibido in ("---\nname:", "<system>", "{{", "@workspace"):
        assert proibido not in texto, proibido


def test_o_esqueleto_respeita_a_diretiva_editorial(texto):
    problemas = [a for linha in texto.splitlines() for a in analisar(linha) if a.bloqueia]
    assert not problemas, problemas


def test_convencoes_editoriais(texto):
    assert "—" not in texto
