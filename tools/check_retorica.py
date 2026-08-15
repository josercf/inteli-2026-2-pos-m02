# -*- coding: utf-8 -*-
"""Trava as três construções retóricas proibidas pela diretiva editorial de
15/08/2026.

A referência de escrita do acervo é a linguagem das apresentações da McKinsey:
o título de um slide de conteúdo é a conclusão completa, com o número dentro, e
o corpo sustenta essa conclusão.

Duas construções reprovam a build, porque são mecânicas e reconhecíveis sem
ambiguidade. A terceira (antítese simétrica) é reportada como candidata: fazer
regex decidir sobre ela produz falso positivo em frase legítima, e um validador
que reprova texto correto acaba desligado.

Uso: python3 tools/check_retorica.py [arquivo ...]
Sem argumento, examina os decks, os materiais e o esqueleto da skill.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NamedTuple

RAIZ = Path(__file__).resolve().parents[1]


class Achado(NamedTuple):
    construcao: str
    trecho: str
    bloqueia: bool


# `não é X, é Y` e `é X, não Y`, com X e Y curtos o bastante para serem o
# mesmo sintagma contrastado, que é o que caracteriza a construção.
_NEGATIVO = [
    re.compile(r"n[ãa]o\s+(?:é|s[ãa]o|era|foi)\s+[^,.;:!?]{2,45},\s*(?:e\s+sim|mas\s+sim|é|s[ãa]o)\b", re.I),
    re.compile(r"\b(?:é|s[ãa]o)\s+[^,.;:!?]{2,45},\s*n[ãa]o\s+[^,.;:!?]{2,45}[.;!?]", re.I),
]

_ESCALADA = re.compile(r"n[ãa]o\s+(?:apenas|s[óo]|somente)\s+[^:.;!?]{2,80}:", re.I)

# Duas orações espelhadas: sujeitos diferentes, verbos no mesmo tempo,
# separadas por vírgula ou ponto e vírgula, sem conjunção subordinativa.
_ANTITESE = re.compile(
    r"\b([OA]s?\s+\w+)\s+(\w+[aeiou])\s*[,;]\s*([oa]s?\s+\w+)\s+(\w+[aeiou])\s*[.;]",
    re.I,
)

_TAG = re.compile(r"<[^>]+>")
_SECTION = re.compile(r"<section\b", re.I)


def analisar(texto: str) -> list[Achado]:
    achados: list[Achado] = []
    for rx in _NEGATIVO:
        for m in rx.finditer(texto):
            achados.append(Achado("paralelismo negativo", m.group(0).strip(), True))
    for m in _ESCALADA.finditer(texto):
        achados.append(Achado("escalada com dois-pontos", m.group(0).strip(), True))
    for m in _ANTITESE.finditer(texto):
        achados.append(Achado("antítese simétrica (candidata)", m.group(0).strip(), False))
    return achados


def texto_visivel(html: str) -> list[tuple[int, str]]:
    """Devolve (numero_do_slide, texto sem marcacao) para cada <section>."""
    partes = _SECTION.split(html)[1:]
    saida = []
    for i, parte in enumerate(partes, 1):
        limpo = _TAG.sub(" ", "<section" + parte)
        limpo = re.sub(r"&middot;", " ", limpo)
        limpo = re.sub(r"\s+", " ", limpo).strip()
        saida.append((i, limpo))
    return saida


ALVOS_PADRAO = [
    "aulas/aula01.html",
    "aulas/aula02.html",
    "materiais/aula01-material-de-apoio.html",
    "materiais/aula02-material-de-apoio.html",
    "materiais/skill-limpeza-kovan.md",
    "materiais/caderno-de-hipoteses.md",
]


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    caminhos = [Path(a) for a in argv] if argv else [RAIZ / a for a in ALVOS_PADRAO]

    examinados = 0
    bloqueios = 0
    avisos = 0

    for caminho in caminhos:
        if not caminho.exists():
            continue
        conteudo = caminho.read_text(encoding="utf-8")
        if caminho.suffix == ".html":
            trechos = texto_visivel(conteudo)
        else:
            trechos = [(i, l) for i, l in enumerate(conteudo.splitlines(), 1) if l.strip()]
        for numero, texto in trechos:
            examinados += 1
            for achado in analisar(texto):
                marca = "REPROVA" if achado.bloqueia else "revisar"
                alvo = "slide" if caminho.suffix == ".html" else "linha"
                print(f"{marca}  {caminho.name} {alvo} {numero}: {achado.construcao}")
                print(f"         {achado.trecho}")
                if achado.bloqueia:
                    bloqueios += 1
                else:
                    avisos += 1

    # Licao 8.1: nada medido nunca pode ler como sucesso.
    if examinados == 0:
        print("Nenhum trecho examinado. Verifique os caminhos.")
        return 2

    print(f"\n{examinados} trechos examinados, {bloqueios} reprovações, {avisos} a revisar.")
    return 1 if bloqueios else 0


if __name__ == "__main__":
    raise SystemExit(main())
