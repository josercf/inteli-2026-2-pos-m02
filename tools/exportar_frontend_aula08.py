# -*- coding: utf-8 -*-
"""Copia o painel da Aula 08 para frontend/ do repositorio de pratica.

O painel vive em painel/ no acervo e e publicado no GitHub Pages da
disciplina. A turma modifica a copia em frontend/, que precisa abrir sozinha:
sem ../assets/ e com as fontes vindas do Google Fonts, ja que o repositorio de
pratica nao carrega a pasta vendor.

Gerada, nunca editada a mao no repositorio de pratica: a correcao entra aqui
no acervo e e copiada de novo.

Uso: .venv/bin/python tools/exportar_frontend_aula08.py
"""

from __future__ import annotations

import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ.parent / "inteli-pos-2026-2a-eda" / "frontend"

FONTES = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700'
          '&family=Platypi:wght@500;600&family=Space+Mono&display=swap">\n'
          '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined">')


def index() -> str:
    s = (RAIZ / "painel" / "index.html").read_text(encoding="utf-8")
    s = s.replace('<link rel="stylesheet" href="../assets/vendor/fontes/fontes.css">', FONTES)
    s = s.replace('href="../assets/css/inteli-brand.css"', 'href="inteli-brand.css"')
    assert "../" not in s, "o painel ainda aponta para fora da propria pasta"
    return s


def marca() -> str:
    s = (RAIZ / "assets" / "css" / "inteli-brand.css").read_text(encoding="utf-8")
    # As fontes vêm do Google Fonts, pelo <link> do index.html.
    return s.replace('@import url("../vendor/fontes/fontes.css");', "")


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    (DESTINO / "index.html").write_text(index(), encoding="utf-8")
    (DESTINO / "inteli-brand.css").write_text(marca(), encoding="utf-8")
    for nome in ("modelo.js", "workflow_n8n.json"):
        shutil.copyfile(RAIZ / "painel" / nome, DESTINO / nome)
    print(f"frontend/ atualizado em {DESTINO}")


if __name__ == "__main__":
    main()
