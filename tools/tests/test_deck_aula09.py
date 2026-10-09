# -*- coding: utf-8 -*-
"""Convenções do deck e do material da Aula 09, o fechamento conjunto.

A Aula 09 não calcula número novo: ela retoma números das Aulas 03 a 08. O
risco próprio desta aula é um recap que cita um número com uma casa trocada, ou
um número que nunca foi travado. Por isso cada número com cara de dado do case
(vírgula decimal, porcentagem, ordinal, milhar ou data com ano) precisa estar
em NUMEROS_DO_CASE, apontando para o arquivo de teste que o trava, transcrito
de forma literal. Número ilustrativo do material de Negócios ou da BCG fica em
NUMEROS_FORA_DO_CASE, com o motivo.

Rodar: python3 -m pytest tools/tests/test_deck_aula09.py -q
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from tools.check_retorica import analisar, texto_visivel  # noqa: E402

DECK = RAIZ / "aulas" / "aula09.html"
MATERIAL = RAIZ / "materiais" / "aula09-material-de-apoio.html"

# número como aparece no deck -> (arquivo que o trava, trecho literal nesse arquivo)
NUMEROS_DO_CASE = {
    "0,01%": ("dados/tests/test_aula07_numeros.py", '"0,01%"'),
    "85,5%": ("dados/tests/test_aula07_numeros.py", '"85,5%"'),
    "29,7%": ("dados/tests/test_aula07_numeros.py", '"29,7%"'),
    "68,4%": ("dados/tests/test_aula07_numeros.py", '"68,4%"'),
    "3.024º": ("dados/tests/test_aula07_numeros.py", '"3.024º"'),
    "1º": ("dados/tests/test_aula07_numeros.py", "test_a_conta_d_sai_de_3024_para_primeiro"),
    "138": ("dados/tests/test_aula08_numeros.py", 'len(r["fila"]) == 138'),
    "0,814": ("dados/tests/test_aula08_numeros.py", '"0,814"'),
    "4.593": ("dados/tests/test_aula08_numeros.py", "== 4593"),
    "26,6": ("dados/tests/test_aula08_numeros.py", '"26,6 milhões"'),
    "0,9999": ("dados/tests/test_aula06_longa.py", '"0,9999"'),
    "0,834": ("dados/tests/test_aula06_longa.py", '"0,834"'),
    "0,818": ("dados/tests/test_aula06_longa.py", '"0,818"'),
    "75,8%": ("dados/tests/test_aula06_longa.py", '"75,8%"'),
    "82,2%": ("dados/tests/test_aula06_longa.py", '"82,2%"'),
    "36": ("dados/tests/test_aula06_longa.py", '"36", "29", "65"'),
    "29": ("dados/tests/test_aula06_longa.py", '"36", "29", "65"'),
    "65": ("dados/tests/test_aula06_longa.py", '"36", "29", "65"'),
    "07/03/2024": ("dados/tests/test_aula06_longa.py", '"07/03/2024"'),
    "19,2%": ("tools/tests/test_deck_aula04.py", '"19,2"'),
    "4.534": ("tools/tests/test_deck_aula04.py", '"4.534"'),
    "8.282": ("tools/tests/test_deck_aula04.py", '"8.282"'),
    "25,4%": ("dados/tests/test_aula04_numeros.py", '"STRATEGIC ACCOUNT": (71, 18, 0.254'),
    "58,1%": ("dados/tests/test_aula04_numeros.py", '"PUBLIC SECTOR": (449, 261, 0.581'),
    "65,1%": ("tools/tests/test_material_aula03.py", '(82, "65,1%")'),
    "1%": ("dados/tests/test_dataset_oficial.py", "round(p[0.01], 3) == 0.651"),
    "08/02/2025": ("dados/tests/test_dataset_oficial.py", '== "2025-02-08"'),
    "217,4": ("tools/tests/test_deck_aula02.py", '"217,4"'),
    # Leitura errada observada na demonstração da Aula 08: o teste do workflow
    # trava a leitura correta (queda de 37%) que o prompt passou a ensinar.
    "0,63": ("tools/tests/test_workflow_aula08.py", "queda de 37%"),
    "63%": ("tools/tests/test_workflow_aula08.py", "queda de 37%"),
}

# Números que não são dado do case, com o motivo.
NUMEROS_FORA_DO_CASE = {
    "10%", "20%", "70%", "10/20/70",  # regra 10/20/70 da BCG, aula de agentes de Negócios
    "15%",                            # hipótese ilustrativa da aula 1 de Negócios
}

PADRAO = re.compile(r"\d+(?:[.,/]\d+)*(?:%|º)?")


def _com_cara_de_case(token: str) -> bool:
    if re.fullmatch(r"\d{1,2}/\d{2}", token):      # data sem ano: calendário
        return False
    if re.fullmatch(r"(19|20)\d{2}", token):        # ano de referência
        return False
    return bool(re.search(r"[,%º]|\d\.\d|/\d{4}", token)) or token in {"138", "36", "29", "65"}


@pytest.fixture(scope="module")
def html() -> str:
    assert DECK.exists(), "rode tools/montar_deck_aula09.py"
    return DECK.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def material() -> str:
    return MATERIAL.read_text(encoding="utf-8")


def _numeros_do_deck(html):
    vistos = set()
    for _, texto in texto_visivel(html):
        vistos |= set(PADRAO.findall(texto))
    return {t for t in vistos if _com_cara_de_case(t)}


def _numeros_do_material(material):
    corpo = re.sub(r"<[^>]+>", " ", material.split("<body>", 1)[1])
    corpo = re.sub(r"p\.\s*\d+-\d+", " ", corpo)  # paginação de referência
    return {t for t in PADRAO.findall(corpo) if _com_cara_de_case(t)}


# ---------------------------------------------------------------------------
# Estrutura
# ---------------------------------------------------------------------------

def test_o_deck_esta_em_dia_com_o_gerador(html, tmp_path):
    """O HTML é gerado. Se alguém editou à mão, a próxima geração apaga a edição."""
    import subprocess
    gerado = subprocess.run(
        [sys.executable, str(RAIZ / "tools" / "montar_deck_aula09.py")],
        capture_output=True, text=True, cwd=RAIZ,
    )
    assert gerado.returncode == 0, gerado.stderr
    assert DECK.read_text(encoding="utf-8") == html, "aula09.html difere do gerador"


def test_secoes_balanceadas_e_sem_aninhamento(html):
    profundidade = 0
    for marca in re.findall(r"<section|</section>", html):
        profundidade += 1 if marca == "<section" else -1
        assert profundidade in (0, 1)
    assert profundidade == 0
    assert len(re.findall(r"<div[ >]", html)) == html.count("</div>")


def test_rodape_numerado_em_sequencia(html):
    paginas = [int(n) for n in re.findall(r'class="footer-page">(\d+)<', html)]
    assert paginas == list(range(2, 2 + len(paginas)))


def test_a_programacao_tem_os_quatro_blocos_na_ordem(html):
    texto = re.sub(r"<[^>]+>", " ", html)
    posicoes = [texto.find(b) for b in ("a) Recap", "b) Tira-dúvidas", "c) Finalização", "d) Apresentação")]
    assert -1 not in posicoes and posicoes == sorted(posicoes), posicoes


def test_as_duas_trilhas_e_os_dois_professores_aparecem(html):
    for termo in ("Prof. Rafael Donaire", "Prof. José Romualdo da Costa Filho",
                  "Recap da trilha de Negócios", "Recap da trilha de Tecnologia",
                  "Checklist do Artefato 2 de Negócios", "Checklist do Artefato 2 de Tecnologia"):
        assert termo in html, termo


def test_o_quiz_tem_uma_unica_resposta_certa(html):
    assert html.count('data-correct="true"') == 1


def test_o_deck_nao_expoe_peso_de_avaliacao(html):
    """Pesos de avaliação ficam fora dos slides (convenção do acervo)."""
    texto = re.sub(r"<[^>]+>", " ", html).lower()
    assert not re.search(r"\bpesos?\b|\bnota (?:de )?\d|de 0 a 10", texto)


# ---------------------------------------------------------------------------
# Números
# ---------------------------------------------------------------------------

def test_todo_numero_do_case_no_deck_esta_travado(html):
    soltos = _numeros_do_deck(html) - NUMEROS_DO_CASE.keys() - NUMEROS_FORA_DO_CASE
    assert not soltos, f"número sem trava em NUMEROS_DO_CASE: {sorted(soltos)}"


def test_todo_numero_do_case_no_material_esta_travado(material):
    soltos = _numeros_do_material(material) - NUMEROS_DO_CASE.keys() - NUMEROS_FORA_DO_CASE
    assert not soltos, f"número sem trava em NUMEROS_DO_CASE: {sorted(soltos)}"


@pytest.mark.parametrize("numero", sorted(NUMEROS_DO_CASE))
def test_a_trava_existe_no_arquivo_de_teste(numero):
    arquivo, literal = NUMEROS_DO_CASE[numero]
    assert literal in (RAIZ / arquivo).read_text(encoding="utf-8"), (numero, arquivo)


def test_a_extracao_pega_numero_solto():
    """Sem este teste, um PADRAO quebrado aprovaria qualquer deck."""
    falso = '<section class="content-slide"><h2>A fila alcança 71,3% da receita</h2></section>'
    assert "71,3%" in _numeros_do_deck(falso)


# ---------------------------------------------------------------------------
# Convenções editoriais
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("arquivo", [DECK, MATERIAL])
def test_convencoes_editoriais(arquivo):
    texto = arquivo.read_text(encoding="utf-8")
    assert "—" not in texto, "em dash proibido"
    assert not re.search(r"[\U0001F300-\U0001FAFF☀-➿]", texto), "emoji proibido"


def test_o_deck_nao_usa_paralelismo(html):
    problemas = [
        (n, a.construcao, a.trecho)
        for n, texto in texto_visivel(html)
        for a in analisar(texto) if a.bloqueia
    ]
    assert not problemas, problemas


def test_titulo_de_quiz_e_pergunta(html):
    """Título afirmativo em quiz entrega o gabarito."""
    for bloco in re.findall(r'<section class="quiz-slide">.*?</section>', html, re.S):
        titulo = re.search(r"<h2>(.*?)</h2>", bloco).group(1)
        assert titulo.endswith("?"), titulo


# ---------------------------------------------------------------------------
# Material de apoio
# ---------------------------------------------------------------------------

def test_material_ancoras_e_referencias(material):
    ids = set(re.findall(r'id="([^"]+)"', material))
    assert not [a for a in re.findall(r'<a href="#([^"]+)"', material) if a not in ids]
    citadas = set(re.findall(r'href="#(r\d+)"', material))
    definidas = set(re.findall(r'id="(r\d+)"', material))
    assert citadas == definidas, (citadas ^ definidas)


def test_material_links_locais_existem(material):
    for href in re.findall(r'href="([^"#:]+\.html)"', material):
        assert (MATERIAL.parent / href).resolve().exists(), href


def test_material_nao_republica_o_deck_de_negocios(material):
    """O deck do Prof. Rafael Donaire fica em recebidos/ (ADR-011)."""
    assert "recebidos/" not in material
    assert ".pdf" not in material and ".pptx" not in material
