# -*- coding: utf-8 -*-
"""Testes do material de apoio da Aula 03.

O material é o artefato que o aluno abre depois da aula, sozinho. Uma âncora
quebrada ou um número que não confere manda quem for verificar procurar no lugar
errado e desacredita os corretos ao lado.

Aqui os números do dataset são conferidos contra o próprio dataset, e não contra
uma constante transcrita: o material afirma valores que o deck não cita, e sem
esta suíte eles ficariam sem trava nenhuma.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

MATERIAL = RAIZ / "materiais" / "aula03-material-de-apoio.html"
XLSX = RAIZ / "dados" / "datasets_case_modulo2.xlsx"


@pytest.fixture(scope="module")
def html() -> str:
    return MATERIAL.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def analise():
    from dados import analise_aula03

    return analise_aula03


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


def test_toda_citacao_numerada_tem_referencia(html):
    citadas = set(re.findall(r'href="#(r\d+)"', html))
    definidas = set(re.findall(r'id="(r\d+)"', html))
    assert citadas, "nenhuma citacao numerada"
    assert citadas <= definidas, citadas - definidas


def test_nenhuma_referencia_fica_sem_uso(html):
    citadas = set(re.findall(r'href="#(r\d+)"', html))
    definidas = set(re.findall(r'id="(r\d+)"', html))
    assert definidas <= citadas, definidas - citadas


def test_toda_figura_existe_e_tem_texto_alternativo(html):
    imagens = re.findall(r"<img\b[^>]*>", html)
    assert imagens, "o material nao usa figura"
    for tag in imagens:
        assert re.search(r'alt="[^"]{4,}"', tag), tag
        src = re.search(r'src="(\.\./[^"]+)"', tag)
        assert src, tag
        assert (RAIZ / "materiais" / src.group(1)).resolve().exists(), src.group(1)


def test_convencoes_editoriais(html):
    assert "—" not in html, "travessao em dash (U+2014)"
    emoji = re.findall(
        "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]", html
    )
    assert not emoji, emoji


def test_usa_classe_de_codigo_que_existe_no_tema(html):
    """`doc-prompt` não existe no inteli-material.css: um bloco com essa classe
    renderiza sem estilo e passa despercebido na revisão em Markdown."""
    css = (RAIZ / "assets" / "css" / "inteli-material.css").read_text(encoding="utf-8")
    for classe in set(re.findall(r'class="(doc-[a-z-]+)"', html)):
        if classe == "doc-figura":  # definida no <style> do proprio material
            continue
        assert f".{classe}" in css, classe


def test_separa_o_que_e_citavel_do_que_e_construcao_do_modulo(html):
    """A frase atravessa quebra de linha e uma tag <strong>: comparar contra o
    HTML cru falharia por formatação, e não por conteúdo."""
    texto = " ".join(re.sub(r"<[^>]+>", " ", html).split())
    assert "não são framework publicado" in texto


# ---------------------------------------------------------------------------
# Números que só o material cita
# ---------------------------------------------------------------------------

pytestmark_dataset = pytest.mark.skipif(
    not XLSX.exists(),
    reason="dados/datasets_case_modulo2.xlsx ausente: dado real, distribuído fora do repositório",
)


@pytestmark_dataset
def test_a_mediana_de_meses_ativos(html, analise):
    assert analise.contas().meses_ativos.median() == 2
    assert "mediana de meses ativos por conta é 2" in html


@pytestmark_dataset
def test_o_canal_de_aquisicao_e_constante(html, analise):
    assert analise.carregar()["cadastro"].canal_aquisicao.nunique() == 1
    assert "um único valor distinto" in html


@pytestmark_dataset
def test_a_cobertura_do_engajamento_enviesa_a_prevalencia(html, analise):
    c = analise.contas()
    tem = c.index.isin(set(analise.carregar()["engajamento"].account_id))
    assert round(c.churn[tem].mean(), 3) == 0.201
    assert round(c.churn[~tem].mean(), 3) == 0.187
    assert "20,1%" in html and "18,7%" in html and "63,2%" in html


@pytestmark_dataset
def test_as_faixas_do_pareto(html, analise):
    p = analise.pareto((0.01, 0.05, 0.10, 0.20))
    assert round(p[0.20], 3) == 0.956
    for contas, pct in ((82, "65,1%"), (414, "84,4%"), (828, "90,6%"), (1656, "95,6%")):
        assert f"<td>{contas:,}</td>".replace(",", ".") in html or f"<td>{contas}</td>" in html
        assert pct in html


@pytestmark_dataset
def test_o_par_de_medidas_no_grao_da_linha(html, analise):
    painel = analise.carregar()["painel"]
    assert round(painel.receita_usd.mean()) == 150559
    assert round(painel.receita_usd.median()) == 6462
    assert "150.559" in html and "6.462" in html


@pytestmark_dataset
def test_a_receita_de_cada_corte(html, analise):
    cortes = analise.limiar_de_inatividade()
    for corte, texto in ((6, "978,3"), (9, "671,1"), (12, "604,2"), (13, "275,4")):
        milhoes = cortes[corte]["receita_da_fila"] / 1e6
        assert f"{milhoes:.1f}".replace(".", ",") == texto, (corte, milhoes)
        assert texto in html


@pytestmark_dataset
def test_a_tabela_de_vazamento(html, analise):
    c = analise.contas()
    alto = c[c.tempo_como_cliente >= 17]
    assert len(alto) == 3788
    assert round(alto.churn.mean(), 3) == 0.421
    assert "3.788" in html and "42,1%" in html


@pytestmark_dataset
def test_a_assimetria_some_em_log(html, analise):
    assert abs(analise.receita_univariada()["assimetria_log10"]) < 0.5
    assert "-0,2" in html
