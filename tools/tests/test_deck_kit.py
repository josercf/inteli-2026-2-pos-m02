# -*- coding: utf-8 -*-
"""A extracao do deck_kit nao pode mudar uma virgula do deck da Aula 01."""

import hashlib
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from tools import deck_kit  # noqa: E402

DECK = RAIZ / "aulas" / "aula01.html"


def _sha(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def test_regerar_a_aula01_produz_o_mesmo_arquivo():
    antes = _sha(DECK)
    subprocess.run(
        [sys.executable, str(RAIZ / "tools" / "montar_deck_aula01.py")],
        cwd=RAIZ, check=True, capture_output=True,
    )
    assert _sha(DECK) == antes, "a extracao mudou a saida do deck da Aula 01"


def test_pratica_usa_colab_por_padrao_e_aceita_outro_ambiente():
    deck_kit.reiniciar_paginacao()
    passos = [{"acao": "Subir o painel"}]
    padrao = deck_kit.pratica(1, "Tarefa", 20, "Trios", "Base", "Numero", passos, "Criterio")
    assert "&middot; Colab" in padrao

    deck_kit.reiniciar_paginacao()
    gemini = deck_kit.pratica(
        1, "Tarefa", 20, "Trios", "Base", "Numero", passos, "Criterio", ambiente="Gemini"
    )
    assert "&middot; Gemini" in gemini
    assert "Colab" not in gemini


def test_a_paginacao_reinicia_entre_decks():
    deck_kit.reiniciar_paginacao()
    primeiro = deck_kit.secao(1, "T", "A")
    deck_kit.reiniciar_paginacao()
    segundo = deck_kit.secao(1, "T", "A")
    assert primeiro == segundo
