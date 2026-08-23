# -*- coding: utf-8 -*-
"""As skills da Aula 04 existem em duplicata (acervo e repositório de clone),
cobrem os passos que o deck cita e não usam paralelismo."""

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from tools.check_retorica import analisar  # noqa: E402

CLONE = RAIZ / "inteli-pos-2026-2a-eda"

pytestmark = pytest.mark.skipif(
    not CLONE.exists(),
    reason="inteli-pos-2026-2a-eda/ ausente: repositório de clone da turma, não versionado no acervo",
)

PARES = {
    "perfil-por-segmento": (RAIZ / "materiais" / "skill-perfil-por-segmento.md",
                            CLONE / "skills" / "perfil-por-segmento.md"),
    "figura-que-decide": (RAIZ / "materiais" / "skill-figura-que-decide.md",
                          CLONE / "skills" / "figura-que-decide.md"),
}


@pytest.mark.parametrize("nome", PARES)
def test_a_skill_e_identica_no_acervo_e_no_clone(nome):
    acervo, clone = PARES[nome]
    assert acervo.read_text(encoding="utf-8") == clone.read_text(encoding="utf-8")


def test_perfil_por_segmento_cobre_a_elegibilidade_e_as_cinco_medidas():
    t = PARES["perfil-por-segmento"][1].read_text(encoding="utf-8")
    for trecho in ("primeiro mês", "2025-02", "receita mediana", "dias de compra",
                   "marcas", "intervalo", "marca dominante"):
        assert trecho in t, trecho


def test_figura_que_decide_cobre_forma_titulo_e_teste():
    t = PARES["figura-que-decide"][1].read_text(encoding="utf-8")
    for trecho in ("Histograma", "Boxplot", "Scatterplot", "título", "intervalo de confiança",
                   "capacidade"):
        assert trecho in t, trecho


def test_bivariada_ganhou_elegibilidade_e_estratificacao():
    t = (CLONE / "skills" / "bivariada.md").read_text(encoding="utf-8")
    assert "## Passo 1a: quem pode exibir o desfecho" in t
    assert "## Passo 4a: estratifique antes de concluir" in t
    assert "qui-quadrado" in t


@pytest.mark.parametrize("caminho", [
    CLONE / "CHECKLIST-ARTEFATO-1.md", RAIZ / "materiais" / "checklist-artefato-1-tecnologia.md",
])
def test_o_checklist_ganhou_os_itens_da_aula04(caminho):
    t = caminho.read_text(encoding="utf-8")
    assert "população que o rótulo consegue marcar" in t
    assert "teste escrito embaixo de cada figura" in t
    assert "Fecha na oficina da Aula 04" in t


@pytest.mark.parametrize("caminho", [p for par in PARES.values() for p in par]
                         + [CLONE / "skills" / "bivariada.md", CLONE / "AGENTS.md"])
def test_sem_paralelismo_nem_em_dash(caminho):
    t = caminho.read_text(encoding="utf-8")
    assert "—" not in t
    bloqueios = [a for a in analisar(t) if a.bloqueia]
    assert not bloqueios, [(a.construcao, a.trecho) for a in bloqueios]
