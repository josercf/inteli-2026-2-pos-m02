#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mede quanto da area util de cada slide esta efetivamente ocupada.

"O slide tem muito espaco em branco" e uma observacao correta e nao mensuravel.
Este script a torna mensuravel: para cada slide, calcula a menor caixa que
contem todo o conteudo real (ignorando faixa do topo, logo e rodape, que sao
moldura) e compara com a area util.

Duas medidas por slide:

- `ocupacao`: area da caixa de conteudo dividida pela area util. Diz se o
  conteudo se espalha pelo quadro ou se aglomera num canto.
- `fundo_vazio`: altura da faixa morta entre o fim do conteudo e o inicio do
  rodape, em pixels. E o sintoma que se ve na projecao: o slide "acaba" na
  metade e sobra tela embaixo.

Nao existe alvo unico: um divisor de secao ocupa pouco de proposito. O que o
script entrega e a lista ordenada por faixa morta, que e onde olhar primeiro.

Uso:
    python3 tools/medir_ocupacao.py                 # todos os decks
    python3 tools/medir_ocupacao.py aulas/aula01.html
    python3 tools/medir_ocupacao.py --json          # saida para teste
"""

from __future__ import annotations

import http.server
import json
import os
import socketserver
import sys
import threading

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LARGURA, ALTURA = 1280, 720

# Moldura do slide: nao conta como conteudo. Sao os tres elementos que o tema
# posiciona em absolute (documentado em inteli-theme.css).
MOLDURA = ".top-bar, .inteli-logo-header, .slide-footer"

# Area util, descontando a moldura. O rodape comeca em 720-24-altura da linha.
TOPO_UTIL = 30
BASE_UTIL = 660

MEDIDA = """
(seletorMoldura) => {
  const slides = [...document.querySelectorAll('.slides > section')];
  return slides.map((s, i) => {
    const anterior = s.style.display;
    s.style.display = 'flex';
    s.classList.add('present');
    const moldura = new Set([...s.querySelectorAll(seletorMoldura)]);
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity, contados = 0;
    for (const el of s.querySelectorAll('*')) {
      if (moldura.has(el)) continue;
      if ([...moldura].some(m => m.contains(el))) continue;
      const r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) continue;
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none') continue;
      // So conta o que produz tinta: folha da arvore (texto, imagem) ou
      // elemento com fundo ou borda propria. Um container esticado e vazio
      // tem caixa grande e nao desenha nada, e media-lo fazia um slide com o
      // conteudo parando na metade aparecer com 0,97 de ocupacao.
      const temFundo = cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent';
      const temBorda = parseFloat(cs.borderTopWidth) + parseFloat(cs.borderLeftWidth)
                     + parseFloat(cs.borderBottomWidth) + parseFloat(cs.borderRightWidth) > 0;
      const ehFolha = el.children.length === 0;
      if (!ehFolha && !temFundo && !temBorda) continue;
      x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top);
      x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom);
      contados++;
    }
    const h = s.querySelector('h1, h2');
    s.classList.remove('present');
    s.style.display = anterior;
    if (!contados) return {indice: i + 1, vazio: true};
    return {
      indice: i + 1,
      // O Reveal acrescenta classes de estado (present, past, future) que nao
      // dizem nada sobre o tipo do slide.
      classe: [...s.classList].filter(c => !['present','past','future','stack'].includes(c)).join(' '),
      titulo: h ? h.textContent.trim() : '(sem titulo)',
      caixa: {x0: Math.round(x0), y0: Math.round(y0), x1: Math.round(x1), y1: Math.round(y1)},
      elementos: contados,
    };
  });
}
"""


def _servidor(porta=0):
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=RAIZ, **k)
    servidor = socketserver.TCPServer(("127.0.0.1", porta), handler)
    servidor.allow_reuse_address = True
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return servidor, servidor.server_address[1]


def medir(decks: list[str]) -> list[dict]:
    from playwright.sync_api import sync_playwright

    servidor, porta = _servidor()
    resultados = []
    try:
        with sync_playwright() as p:
            navegador = p.chromium.launch()
            pagina = navegador.new_page(viewport={"width": LARGURA, "height": ALTURA})
            for deck in decks:
                rel = os.path.relpath(deck, RAIZ).replace(os.sep, "/")
                pagina.goto(f"http://127.0.0.1:{porta}/{rel}")
                pagina.wait_for_timeout(900)
                for medida in pagina.evaluate(MEDIDA, MOLDURA):
                    if medida.get("vazio"):
                        continue
                    caixa = medida["caixa"]
                    util = (LARGURA - 112) * (BASE_UTIL - TOPO_UTIL)
                    area = max(0, caixa["x1"] - caixa["x0"]) * max(0, caixa["y1"] - caixa["y0"])
                    resultados.append(
                        {
                            "deck": rel,
                            "slide": medida["indice"],
                            "classe": medida["classe"],
                            "titulo": medida["titulo"],
                            "ocupacao": round(area / util, 3),
                            "fundo_vazio": max(0, BASE_UTIL - caixa["y1"]),
                            "elementos": medida["elementos"],
                        }
                    )
            navegador.close()
    finally:
        servidor.shutdown()
    return resultados


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--json"]
    como_json = "--json" in sys.argv
    if args:
        decks = [os.path.join(RAIZ, a) for a in args]
    else:
        pasta = os.path.join(RAIZ, "aulas")
        decks = [
            os.path.join(pasta, n)
            for n in sorted(os.listdir(pasta))
            if n.endswith(".html") and not n.startswith("_")
        ]
    if not decks:
        print("nenhum deck para medir", file=sys.stderr)
        return 1

    resultados = medir(decks)
    if not resultados:
        print("nada foi medido", file=sys.stderr)
        return 1

    if como_json:
        print(json.dumps(resultados, ensure_ascii=False, indent=1))
        return 0

    conteudo = [r for r in resultados if r["classe"] in ("content-slide", "quiz-slide", "exercise-slide")]
    print(f"{len(resultados)} slides medidos, {len(conteudo)} de conteudo\n")
    print(f"{'#':>3}  {'ocup':>5}  {'fundo':>5}  titulo")
    for r in sorted(conteudo, key=lambda r: -r["fundo_vazio"]):
        print(f"{r['slide']:>3}  {r['ocupacao']:>5.2f}  {r['fundo_vazio']:>5}  {r['titulo'][:58]}")
    if conteudo:
        media = sum(r["fundo_vazio"] for r in conteudo) / len(conteudo)
        print(f"\nfaixa morta media nos slides de conteudo: {media:.0f}px")
        print(f"ocupacao media: {sum(r['ocupacao'] for r in conteudo) / len(conteudo):.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
