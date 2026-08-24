# -*- coding: utf-8 -*-
"""Testes do material de apoio da Aula 04.

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

MATERIAL = RAIZ / "materiais" / "aula04-material-de-apoio.html"
XLSX = RAIZ / "dados" / "datasets_case_modulo2.xlsx"


@pytest.fixture(scope="module")
def html() -> str:
    return MATERIAL.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def analise():
    from dados import analise_aula04

    return analise_aula04


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
def test_as_tres_populacoes(html, analise):
    p = analise.populacoes()
    assert p["elegiveis"]["contas"] == 3748 and p["nao_elegiveis"]["contas"] == 4534
    assert "3.748" in html and "4.534" in html and "42,5%" in html


@pytestmark_dataset
def test_o_intervalo_de_wilson_da_carteira_elegivel(html, analise):
    p = analise.populacoes()["elegiveis"]
    assert (round(p["ic_inferior"], 3), round(p["ic_superior"], 3)) == (0.409, 0.441)
    assert "40,9%" in html and "44,1%" in html


@pytestmark_dataset
def test_o_mix_sob_controle_por_frequencia(html, analise):
    t = analise.estratificar("marcas", 1, 3, "faixa_dias")
    assert round(t.loc["2", "prev_a"], 3) == 0.525 and round(t.loc["2", "prev_b"], 3) == 0.534
    assert "52,5%" in html and "53,4%" in html


@pytestmark_dataset
def test_a_composicao_do_brasil(html, analise):
    c = analise.composicao_br()
    assert round(c["share_mid_public_br"], 3) == 0.697
    assert "69,7%" in html and "28,1%" in html


@pytestmark_dataset
def test_o_engajamento_nas_elegiveis(html, analise):
    e = analise.engajamento_nas_elegiveis()
    assert e["contas_cobertas"] == 1560
    assert "1.560" in html


@pytestmark_dataset
def test_a_pbl_em_numeros(html, analise):
    p = analise.par_da_pbl()
    assert (p["candidatas"], p["ativas"], p["perdidas"]) == (66, 63, 3)
    assert "66 contas" in html and "Conta A" in html and "Conta B" in html
    assert "CLI000269" not in html and "CLI000264" not in html


def test_o_material_aponta_as_skills_novas(html):
    assert "skills/perfil-por-segmento.md" in html and "skills/figura-que-decide.md" in html


# ---------------------------------------------------------------------------
# Seção 6: os setores, um a um
# ---------------------------------------------------------------------------

@pytestmark_dataset
def test_a_tabela_de_setores_esta_no_material(html, analise):
    t = analise.perfil_por_setor()
    assert len(t) == 13
    assert round(t.loc["GOVERNMENT", "intervalo_mediano"], 1) == 18.5
    for trecho in ("59,7%", "55,6%", "34,1%", "18,5", "38.079", "DESKTOP"):
        assert trecho in html, trecho


@pytestmark_dataset
def test_a_rajada_do_setor_publico(html, analise):
    t = analise.rajada_por_setor()
    assert round(t.loc["GOVERNMENT", "pico_mediano"], 3) == 0.905
    assert round(t.loc["GOVERNMENT", "recorrentes"], 3) == 0.126
    for trecho in ("90,5%", "98,2%", "97,1%", "69,5%", "12,6%", "20,3%"):
        assert trecho in html, trecho


@pytestmark_dataset
def test_a_conta_c_no_material(html, analise):
    c = analise.conta_c()
    assert round(c["receita"] / 1e6, 1) == 147.3
    assert round(c["participacao_na_receita_perdida"], 3) == 0.657
    for trecho in ("147,3", "65,7%", "224,2", "76,9", "174,8", "27,5", "El Salvador"):
        assert trecho in html, trecho
    assert "CLI002953" not in html


@pytestmark_dataset
def test_setor_e_segmento_declarados_como_recortes_diferentes(html, analise):
    x = analise.setor_x_segmento()
    assert x["contas_government"] == 631
    for trecho in ("631", "479", "837"):
        assert trecho in html, trecho
