# -*- coding: utf-8 -*-
"""
O deck precisa abrir numa sala sem rede.

O Reveal.js ja estava vendorizado exatamente por isso, mas as fontes da marca
vinham de fonts.googleapis.com por @import: numa rede corporativa filtrada, ou
sem rede, o deck inteiro caia para Georgia e system-ui e o material projetado
deixava de ser o material aprovado.

Este teste bloqueia toda requisicao que nao seja para o servidor local e
confere que nada externo e pedido e que as tres familias da marca carregam.

Rodar: python3 -m pytest tools/tests/test_offline.py -q
"""

from __future__ import annotations

import http.server
import socketserver
import threading
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
FAMILIAS = {"Platypi", "Manrope", "Space Mono"}


@pytest.fixture(scope="module")
def medida():
    from playwright.sync_api import sync_playwright

    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=str(RAIZ), **k)
    servidor = socketserver.TCPServer(("127.0.0.1", 0), handler)
    porta = servidor.server_address[1]
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    externas: list[str] = []
    try:
        with sync_playwright() as p:
            navegador = p.chromium.launch()
            contexto = navegador.new_context(viewport={"width": 1280, "height": 720})

            def filtro(rota):
                url = rota.request.url
                if "127.0.0.1" in url or "localhost" in url:
                    rota.continue_()
                else:
                    externas.append(url)
                    rota.abort()

            contexto.route("**/*", filtro)
            pagina = contexto.new_page()
            pagina.goto(f"http://127.0.0.1:{porta}/aulas/aula01.html")
            pagina.wait_for_timeout(3000)
            carregadas = set(
                pagina.evaluate(
                    "[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family)"
                )
            )
            familia = pagina.evaluate(
                "getComputedStyle(document.querySelector('.present h2, h1')).fontFamily.split(',')[0]"
            )
            navegador.close()
    finally:
        servidor.shutdown()
    return {"externas": externas, "carregadas": carregadas, "familia": familia}


def test_o_deck_nao_pede_nada_de_fora(medida):
    assert not medida["externas"], medida["externas"][:5]


def test_as_fontes_da_marca_carregam_sem_rede(medida):
    faltando = FAMILIAS - medida["carregadas"]
    assert not faltando, faltando


def test_o_titulo_resolve_para_a_fonte_da_marca(medida):
    """Sem esta checagem, um fallback silencioso para Georgia passaria: a
    familia declarada continua sendo Platypi mesmo quando o arquivo nao carrega.
    """
    assert medida["familia"].strip("\"'") == "Platypi", medida["familia"]
