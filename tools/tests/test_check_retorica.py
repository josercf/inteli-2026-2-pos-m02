# -*- coding: utf-8 -*-
"""O validador de retórica precisa reprovar o que a diretiva proíbe, e precisa
aprovar a reescrita correspondente. Um validador que só aprova não protege."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from tools.check_retorica import Achado, analisar, main, texto_visivel  # noqa: E402


REPROVADOS = [
    ("Alucinação não é defeito, é propriedade do modelo.", "paralelismo negativo"),
    ("Isso é conteúdo, não escolha de estilo.", "paralelismo negativo"),
    ("O prompt é parte da análise, não um acessório.", "paralelismo negativo"),
    ("A quebra não apenas fabrica sinal falso: ela inverte o sinal.", "escalada"),
    ("O painel não só tem lacunas: as lacunas são enviesadas.", "escalada"),
]

APROVADOS = [
    "A ausência de registro de engajamento varia de 29% a 53% entre segmentos.",
    "A quebra de taxonomia produz duas distorções simultâneas.",
    "O tratamento preserva a direção da relação e altera a magnitude em até 49%.",
    "Nenhuma conta comprou linha de produto adicional entre 2022Q4 e 2023Q1.",
    "O erro de sinal em devolucoes_brl custa R$ 217,4 milhões.",
]


@pytest.mark.parametrize("frase,construcao", REPROVADOS)
def test_reprova_as_construcoes_proibidas(frase, construcao):
    achados = analisar(frase)
    assert achados, f"deveria reprovar: {frase}"
    assert any(construcao in a.construcao for a in achados), [a.construcao for a in achados]


@pytest.mark.parametrize("frase", APROVADOS)
def test_aprova_a_reescrita_correspondente(frase):
    assert analisar(frase) == []


def test_antitese_simetrica_e_candidata_e_nao_reprova():
    """Reconhecer antítese por regex gera falso positivo. Ela vira aviso."""
    achados = analisar("O Gemini descobre, o Antigravity registra.")
    assert any("antítese" in a.construcao for a in achados)
    assert all(a.bloqueia is False for a in achados if "antítese" in a.construcao)


def test_texto_visivel_ignora_marcacao_e_numera_os_slides():
    html = (
        '<section class="content-slide"><h2>Título</h2>'
        "<p>Não é decisão, é acidente.</p></section>\n"
        '<section class="quiz-slide"><p>Pergunta neutra.</p></section>'
    )
    trechos = texto_visivel(html)
    assert [n for n, _ in trechos] == [1, 2]
    assert "Não é decisão, é acidente." in trechos[0][1]
    assert "<h2>" not in trechos[0][1]


def test_nada_examinado_nunca_le_como_sucesso(tmp_path):
    """Lição 8.1: zero itens examinados é erro, não aprovação."""
    assert texto_visivel("<html><body></body></html>") == []
    inexistente = tmp_path / "nao-existe.html"
    assert main([str(inexistente)]) == 2
