# -*- coding: utf-8 -*-
"""O esqueleto da skill precisa cobrir as quatro advertências e permanecer
portátil entre agentes."""

import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from tools.check_retorica import analisar  # noqa: E402

SKILL = RAIZ / "materiais" / "skill-limpeza-kovan.md"


@pytest.fixture(scope="module")
def texto() -> str:
    return SKILL.read_text(encoding="utf-8")


def _secao(texto: str, numero: int) -> str:
    """Devolve o texto de um `## Passo {numero}:` ate o proximo `## `."""
    padrao = re.compile(rf"## Passo {numero}:.*?(?=\n## )", re.S)
    m = padrao.search(texto)
    assert m, f"Passo {numero} não encontrado no esqueleto"
    return m.group(0)


@pytest.mark.parametrize(
    "coluna",
    ["receita_brl", "visitas_registradas", "interacoes_crm", "taxonomia_mix", "devolucoes_brl"],
)
def test_o_esqueleto_pede_decisao_para_cada_coluna_afetada(texto, coluna):
    assert coluna in texto


def test_o_esqueleto_tem_uma_lacuna_por_advertencia(texto):
    """O marcador é `A DECIDIR`, não `PREENCHER`: imputar é literalmente
    preencher a lacuna, e um agente lendo `Decisão do grupo: PREENCHER` sem
    substituição pode entender aquilo como a própria decisão de tratamento."""
    assert texto.count("A DECIDIR") == 4
    assert "PREENCHER" not in texto


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


def test_o_esqueleto_associa_o_indicador_certo_a_cada_passo(texto):
    """A receita ausente (Passo 2) desloca a contagem de rupturas. O sinal de
    `devolucoes_brl` (Passo 5) desloca a receita líquida total. Trocados, a
    sugestão do arquivo aponta um grupo pouco técnico para o indicador
    errado em metade dos passos."""
    passo2 = _secao(texto, 2).lower()
    passo5 = _secao(texto, 5).lower()
    assert "contagem de rupturas" in passo2
    assert "receita líquida total" not in passo2
    assert "receita líquida total" in passo5
    assert "contagem de rupturas" not in passo5


def test_o_esqueleto_pede_o_indicador_do_passo_3_por_segmento(texto):
    """Os números da Prática 3 são três por tratamento, um por segmento. Um
    branco único por alternativa produz uma média agregada que nunca bate."""
    passo3 = _secao(texto, 3).lower()
    for segmento in ("cauda", "médio", "estratégico"):
        assert segmento in passo3


def test_o_esqueleto_passo_6_segmenta_o_indicador_do_passo_3(texto):
    passo6 = _secao(texto, 6).lower()
    for segmento in ("cauda", "médio", "estratégico"):
        assert segmento in passo6


def test_o_esqueleto_enumera_alternativas_dos_passos_4_e_5(texto):
    """Os Passos 2 e 3 herdam o par implícito excluir/imputar da própria
    situação descrita. Os Passos 4 e 5 não têm esse par óbvio e precisam
    enumerar as alternativas em jogo dentro do próprio arquivo."""
    passo4 = _secao(texto, 4).lower()
    passo5 = _secao(texto, 5).lower()
    assert "alternativas em jogo" in passo4
    assert "alternativas em jogo" in passo5


def test_o_esqueleto_explica_a_reutilizacao_de_codigo(texto):
    """O arquivo precisa funcionar sozinho, colado numa conversa, sem o
    deck ao lado: a instrução de reaproveitar o mesmo código, trocando só a
    linha do tratamento, é o que torna o trabalho viável em 30 minutos."""
    minusculo = texto.lower()
    assert "trocando" in minusculo and "linha do tratamento" in minusculo
    assert "trinta minutos" in minusculo or "30 minutos" in minusculo


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
