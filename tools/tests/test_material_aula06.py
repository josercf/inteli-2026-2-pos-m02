# -*- coding: utf-8 -*-
"""Testes do material de apoio da Aula 06.

O material é o artefato que o aluno abre depois da aula, sozinho. Uma âncora
quebrada ou um número que não confere manda quem for verificar procurar no lugar
errado e desacredita os corretos ao lado.

Os números conferidos aqui saem do próprio dataset, através de
dados/analise_aula06.py, e não de constante transcrita nos dois lados.

Rodar: .venv/bin/python -m pytest tools/tests/test_material_aula06.py -q
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

MATERIAL = RAIZ / "materiais" / "aula06-material-de-apoio.html"
DECK = RAIZ / "aulas" / "aula06.html"
XLSX = RAIZ / "dados" / "datasets_case_modulo2.xlsx"


@pytest.fixture(scope="module")
def html() -> str:
    return MATERIAL.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def texto(html) -> str:
    """Texto visível, sem marcação e com espaço colapsado.

    Assertiva de frase precisa rodar sobre isto, não sobre o HTML cru: a frase
    do material quebra linha no meio de um <strong> e o `in` falha por causa da
    indentação do arquivo, sem que o texto tenha mudado.
    """
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


@pytest.fixture(scope="module")
def analise():
    from dados import analise_aula06

    return analise_aula06


# ---------------------------------------------------------------------------
# Estrutura, independente do dataset
# ---------------------------------------------------------------------------

def test_o_material_existe_e_tem_corpo(html):
    texto = re.sub(r"<[^>]+>", " ", html)
    assert len(texto.split()) > 1500, len(texto.split())


def test_toda_ancora_do_sumario_resolve(html):
    ids = set(re.findall(r'id="([^"]+)"', html))
    alvos = re.findall(r'<a href="#([^"]+)"', html)
    assert alvos, "o sumario nao aponta para nada"
    quebradas = [a for a in alvos if a not in ids]
    assert not quebradas, quebradas


def test_o_sumario_cobre_todas_as_secoes(html):
    """Seção sem entrada no sumário some da navegação lateral sem erro nenhum."""
    secoes = set(re.findall(r'<section class="doc-secao" id="([^"]+)"', html))
    no_sumario = set(re.findall(r'<li><a href="#([^"]+)"', html))
    assert secoes == no_sumario, secoes ^ no_sumario


def test_toda_citacao_numerada_tem_referencia(html):
    citadas = set(re.findall(r'href="#(r\d+)"', html))
    definidas = set(re.findall(r'id="(r\d+)"', html))
    assert citadas, "nenhuma citacao numerada"
    assert citadas <= definidas, citadas - definidas


def test_nenhuma_referencia_fica_sem_uso(html):
    citadas = set(re.findall(r'href="#(r\d+)"', html))
    definidas = set(re.findall(r'id="(r\d+)"', html))
    assert definidas <= citadas, definidas - citadas


def test_convencoes_editoriais(html):
    assert "—" not in html, "travessao em dash (U+2014)"
    emoji = re.findall(
        "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]", html)
    assert not emoji, emoji


def test_separa_o_que_e_citavel_do_que_e_construcao_do_modulo(texto):
    """As três perguntas de vazamento foram organizadas para esta trilha. Se o
    material as apresentar como framework publicado, a turma cita errado lá
    fora."""
    assert "não são framework publicado" in texto


def test_o_material_nao_repete_o_deck_em_prosa(texto):
    """O material precisa acrescentar o que o slide só pôde apontar. Estes três
    assuntos não cabem em slide nenhum e são a prova de que a página deriva em
    vez de transcrever."""
    for assunto in ("Hanley", "seleção induzida pela definição da variável",
                    "grupo de controle"):
        assert assunto in texto, assunto


def test_a_retorica_do_material_e_do_deck_passa(html):
    """O allowlist padrão de check_retorica.py já cobre os dois arquivos, mas um
    material novo não pode depender de alguém lembrar de atualizar aquela lista.
    """
    sys.path.insert(0, str(RAIZ / "tools"))
    from tools.check_retorica import main

    assert main([str(MATERIAL), str(DECK)]) == 0


# ---------------------------------------------------------------------------
# Os números, conferidos contra o dataset
# ---------------------------------------------------------------------------

pytestmark_dataset = pytest.mark.skipif(
    not XLSX.exists(), reason="dataset oficial não versionado (ADR-005)")


@pytestmark_dataset
def test_a_particao_citada_bate_com_a_analise(html, analise):
    p = analise.particao_temporal()
    assert p["corte"] in html
    assert p["inicio_painel"] in html
    assert p["fim_painel"] in html
    assert f"{p['contas']:,}".replace(",", ".") in html
    assert f"{p['perdidas']:,}".replace(",", ".") in html


@pytestmark_dataset
def test_a_tabela_de_auc_do_material_bate_com_a_analise(html, analise):
    t = analise.auc_das_candidatas()
    for coluna in t.index:
        valor = f"{t.loc[coluna, 'auc_orientada']:.3f}".replace(".", ",")
        assert valor in html, (coluna, valor)


@pytestmark_dataset
def test_a_auc_bruta_citada_no_texto_bate(html, analise):
    """O material explica a orientação da AUC usando o valor bruto de
    freq_meses. Se a coluna mudar, o exemplo do texto para de fazer sentido."""
    t = analise.auc_das_candidatas()
    bruta = f"{t.loc['freq_meses', 'auc']:.3f}".replace(".", ",")
    assert bruta in html, bruta


@pytestmark_dataset
def test_a_tabela_de_pesos_do_material_bate_com_a_analise(html, analise):
    t = analise.pesos_do_modelo()
    for coluna in t.index:
        coef = t.loc[coluna, "coeficiente"]
        sinal = "+" if coef > 0 else "-"
        assert f"{sinal}{abs(coef):.3f}".replace(".", ",") in html, coluna
        assert f"{t.loc[coluna, 'razao_de_chances']:.3f}".replace(".", ",") in html, coluna
        assert f"{t.loc[coluna, 'peso_relativo'] * 100:.1f}%".replace(".", ",") in html, coluna


@pytestmark_dataset
def test_as_somas_de_peso_citadas_no_texto_batem(html, analise):
    t = analise.pesos_do_modelo()
    frequencia = t.loc[["freq_meses", "freq_dias"], "peso_relativo"].sum() * 100
    recencia_e_frequencia = frequencia + t.loc["recencia_corte", "peso_relativo"] * 100
    valor = t.loc[["valor_obs", "ticket_medio"], "peso_relativo"].sum() * 100
    resto = t.loc[["marcas_obs", "razao_3m"], "peso_relativo"].sum() * 100
    for soma in (frequencia, recencia_e_frequencia, valor, resto):
        assert f"{soma:.1f}%".replace(".", ",") in html, soma


@pytestmark_dataset
def test_as_faixas_da_razao_batem(html, analise):
    t = analise.perfil_da_razao()
    for faixa in t.index:
        assert f"{int(t.loc[faixa, 'contas']):,}".replace(",", ".") in html, faixa
        assert f"{t.loc[faixa, 'prevalencia'] * 100:.1f}%".replace(".", ",") in html, faixa


@pytestmark_dataset
def test_a_concordancia_do_vazamento_bate(html, analise):
    c = analise.concordancia_do_vazamento()
    assert f"{c['iguais']:,}".replace(",", ".") in html
    assert f"{c['concordancia'] * 100:.1f}%".replace(".", ",") in html
    # Os casos em que a regra de treze meses erra o rótulo.
    assert str(c["contas"] - c["iguais"]) in html


@pytestmark_dataset
def test_a_matriz_de_confusao_dos_dois_cortes_bate(html, analise):
    """A seção do limiar compara o corte por capacidade com o 0,5 padrão."""
    fila = analise.lista_priorizada()
    padrao = analise.limiar_padrao()
    for valor in (fila["precisao"], fila["revocacao"], fila["acuracia"],
                  padrao["precisao"], padrao["revocacao"], padrao["acuracia"]):
        assert f"{valor * 100:.1f}%".replace(".", ",") in html, valor
    assert f"{padrao['marcadas']:,}".replace(",", ".") in html
    assert str(fila["verdadeiros_positivos"]) in html
    assert str(fila["falsos_positivos"]) in html
    assert f"{fila['limiar']:.3f}".replace(".", ",") in html


@pytestmark_dataset
def test_a_linha_de_base_de_marcar_ninguem_aparece(html, analise):
    p = analise.particao_temporal()
    base = (1 - p["perdidas"] / p["contas"]) * 100
    assert f"{base:.1f}%".replace(".", ",") in html
    assert f"{138 / p['perdidas'] * 100:.1f}%".replace(".", ",") in html


@pytestmark_dataset
def test_os_tres_graos_da_abertura_aparecem(html, analise):
    g = analise.do_evento_a_conta()
    for chave in ("itens_de_pedido", "linhas_de_painel"):
        assert f"{g[chave]:,}".replace(",", ".") in html, chave


@pytestmark_dataset
def test_as_duas_auc_do_escore_batem(html, analise):
    honesto = analise.qualidade_do_modelo()
    vazado = analise.qualidade_do_modelo(analise.FEATURES_HONESTAS + ["recencia_fim"])
    assert f"{honesto['auc']:.3f}".replace(".", ",") in html
    assert f"{vazado['auc']:.3f}".replace(".", ",") in html
    assert f"{vazado['auc'] - honesto['auc']:.3f}".replace(".", ",") in html
