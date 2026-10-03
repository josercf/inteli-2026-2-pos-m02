# -*- coding: utf-8 -*-
"""O workflow que o painel oferece para baixar.

Ele vai para o n8n de cada grupo sem passar por revisão, então o que não pode
quebrar fica travado aqui: a ordem dos agentes, o modelo vindo do painel, o
modelo gratuito como padrão, a resposta com os três agentes e a ausência de
credencial no arquivo.

Rodar: .venv/bin/python -m pytest tools/tests/test_workflow_aula08.py -q
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from tools import montar_workflow_aula08 as m  # noqa: E402

ARQUIVO = RAIZ / "painel" / "workflow_n8n.json"


def _wf():
    return json.loads(ARQUIVO.read_text(encoding="utf-8"))


def test_o_arquivo_publicado_e_o_que_o_gerador_produz():
    assert _wf() == json.loads(json.dumps(m.montar(), ensure_ascii=False))


def test_os_tres_agentes_em_sequencia():
    c = _wf()["connections"]
    cadeia = ["API do painel", "Atlas", "Vera", "Ciro", "Responder ao painel"]
    for origem, destino in zip(cadeia, cadeia[1:]):
        assert c[origem]["main"][0][0]["node"] == destino


def test_o_modelo_vem_do_painel_e_cai_no_gratuito():
    modelos = [n for n in _wf()["nodes"] if n["type"].endswith("lmChatOpenRouter")]
    assert len(modelos) == 3
    for n in modelos:
        assert "modelo_llm" in n["parameters"]["model"]
        assert ":free" in n["parameters"]["model"]


def test_nenhuma_credencial_no_arquivo():
    assert all("credentials" not in n for n in _wf()["nodes"])


def test_o_painel_de_qualquer_origem_consegue_chamar():
    api = next(n for n in _wf()["nodes"] if n["name"] == "API do painel")
    assert api["parameters"]["options"]["allowedOrigins"] == "*"
    assert api["parameters"]["path"] == "kovan-chat-NOME_DO_GRUPO"


def test_a_resposta_traz_os_tres_agentes():
    resp = next(n for n in _wf()["nodes"] if n["name"] == "Responder ao painel")
    corpo = resp["parameters"]["responseBody"]
    for nome in ("Atlas", "Vera", "Ciro"):
        assert f"nome: '{nome}'" in corpo


def test_o_revisor_devolve_o_veredito_que_o_painel_le():
    ciro = next(n for n in _wf()["nodes"] if n["name"] == "Ciro")
    assert "VEREDITO: aprovado" in ciro["parameters"]["options"]["systemMessage"]


def test_os_prompts_explicam_a_coluna_que_ja_foi_lida_errado():
    for nome in ("Atlas", "Vera", "Ciro"):
        no = next(n for n in _wf()["nodes"] if n["name"] == nome)
        assert "queda de 37%" in no["parameters"]["options"]["systemMessage"]
