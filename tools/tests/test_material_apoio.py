# -*- coding: utf-8 -*-
"""
Testes do material de apoio da Aula 01.

O material e o artefato que o aluno abre depois da aula, sozinho, sem o
professor para consertar uma ancora quebrada ou uma citacao que aponta para o
lugar errado. Uma referencia com numero errado e pior que nenhuma referencia:
manda quem for conferir procurar no lugar errado e desacredita as corretas ao
lado dela.

Rodar: python3 -m pytest tools/tests/test_material_apoio.py -q
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
MATERIAL = RAIZ / "materiais" / "aula01-material-de-apoio.html"


@pytest.fixture(scope="module")
def html() -> str:
    return MATERIAL.read_text(encoding="utf-8")


def test_o_material_existe_e_tem_corpo(html):
    texto = re.sub(r"<[^>]+>", " ", html)
    palavras = len(texto.split())
    assert palavras > 1500, palavras


def test_toda_ancora_do_sumario_resolve(html):
    ids = set(re.findall(r'id="([^"]+)"', html))
    alvos = re.findall(r'<a href="#([^"]+)"', html)
    assert alvos, "o sumario nao aponta para nada"
    quebradas = [a for a in alvos if a not in ids]
    assert not quebradas, quebradas


def test_toda_citacao_numerada_tem_referencia(html):
    """Citacao no corpo aponta para um item da lista de referencias."""
    citadas = set(re.findall(r'href="#(r\d+)"', html))
    definidas = set(re.findall(r'id="(r\d+)"', html))
    assert citadas, "nenhuma citacao numerada"
    assert citadas <= definidas, citadas - definidas


def test_nenhuma_referencia_fica_sem_uso(html):
    """Referencia definida e nunca citada e sinal de que o texto foi cortado e
    a lista nao acompanhou."""
    citadas = set(re.findall(r'href="#(r\d+)"', html))
    definidas = set(re.findall(r'id="(r\d+)"', html))
    assert definidas <= citadas, definidas - citadas


def test_convencoes_editoriais(html):
    assert "—" not in html, "travessao em dash (U+2014)"
    emoji = re.findall(
        "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]", html
    )
    assert not emoji, emoji


def test_separa_o_que_e_citavel_do_que_e_construcao_do_modulo(html):
    """Os cinco criterios de escolha de alvo nao sao framework publicado. Se o
    material os apresentar como se fossem, a turma cita errado la fora."""
    assert "não são framework publicado" in html or "não é framework publicado" in html


def test_os_numeros_do_painel_batem_com_o_dataset(html):
    """O material afirma taxas de ausencia por segmento. Se o gerador mudar e o
    texto nao, o aluno confere e encontra outra coisa."""
    import pandas as pd

    painel = pd.read_csv(RAIZ / "dados" / "kovan_painel_contas.csv")
    taxa = painel.groupby("segmento")["receita_brl"].apply(lambda s: s.isna().mean() * 100)
    for segmento, esperado in (("Cauda", 1.07), ("Estrategico", 0.85), ("Medio", 0.78)):
        assert f"{esperado:.2f}".replace(".", ",") in html, (segmento, esperado)
        assert abs(taxa[segmento] - esperado) < 0.02, (segmento, taxa[segmento], esperado)

    janela = painel[painel["trimestre"] >= "2023Q2"]
    eng = janela.groupby("segmento")["interacoes_crm"].apply(lambda s: s.isna().mean() * 100)
    for segmento, esperado in (("Estrategico", 10.2), ("Cauda", 40.4)):
        assert f"{esperado:.1f}".replace(".", ",") in html, (segmento, esperado)
        assert abs(eng[segmento] - esperado) < 0.1, (segmento, eng[segmento], esperado)
