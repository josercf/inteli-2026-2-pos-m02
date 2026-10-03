# -*- coding: utf-8 -*-
"""Importa o workflow da Aula 08 no n8n do Inteli e tira as capturas do deck.

Pré-requisitos:

- `python -m app.publicar --grupo demo-aula08` no repositório de prática, que
  grava `saida/workflow_n8n.json`;
- um perfil de navegador com sessão aberta em inteli.app.n8n.cloud (o login é
  feito à mão, uma vez, numa janela visível; a senha nunca passa por aqui).

Uso: python tools/capturar_n8n_aula08.py <pasta-do-perfil>

As capturas vão para assets/img/aula08-n8n-*.png. A credencial OpenRouter é a
que já existe no workspace: o script procura pelo tipo, nunca recebe a chave.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[1]
BASE = "https://inteli.app.n8n.cloud"
WORKFLOW = RAIZ.parent / "inteli-pos-2026-2a-eda" / "saida" / "workflow_n8n.json"
IMG = RAIZ / "assets" / "img"
PERGUNTA = ("Por que a conta CLI052938 está em primeiro lugar na fila? "
            "Me dê um roteiro para a ligação desta semana.")

API_JS = """async ([metodo, caminho, corpo]) => {
  const bid = localStorage.getItem('n8n-browserId') || '';
  const r = await fetch(caminho, {method: metodo, credentials: 'include',
    headers: {'Content-Type': 'application/json', 'browser-id': bid},
    body: corpo ? JSON.stringify(corpo) : undefined});
  return {status: r.status, texto: await r.text()};
}"""


def api(page, metodo, caminho, corpo=None):
    r = page.evaluate(API_JS, [metodo, caminho, corpo])
    try:
        dados = json.loads(r["texto"])
    except ValueError:
        dados = r["texto"]
    if isinstance(dados, dict) and "data" in dados:
        dados = dados["data"]
    return r["status"], dados


def main(perfil: str) -> None:
    wf = json.loads(WORKFLOW.read_text(encoding="utf-8"))
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            perfil, headless=False, channel="chrome",
            viewport={"width": 1600, "height": 900}, device_scale_factor=2)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(f"{BASE}/home/workflows")
        page.wait_for_timeout(6000)
        print("url:", page.url)

        st, creds = api(page, "GET", "/rest/credentials")
        print("credenciais:", st)
        orr = [c for c in creds if c.get("type") == "openRouterApi"]
        print("openRouterApi:", [(c["id"], c["name"]) for c in orr])
        if orr:
            for n in wf["nodes"]:
                if n["type"].endswith("lmChatOpenRouter"):
                    n["credentials"] = {"openRouterApi": {"id": orr[0]["id"], "name": orr[0]["name"]}}

        for n in wf["nodes"]:
            if n["type"].endswith("lmChatOpenRouter") and orr:
                n["credentials"] = {"openRouterApi": {"id": orr[0]["id"], "name": orr[0]["name"]}}
        if len(sys.argv) > 2:
            wid = sys.argv[2]
            st, atual = api(page, "GET", f"/rest/workflows/{wid}")
            st, criado = api(page, "PATCH", f"/rest/workflows/{wid}",
                             {"nodes": wf["nodes"], "connections": wf["connections"],
                              "versionId": atual["versionId"]})
            print("atualizar:", st, str(criado)[:200] if st >= 300 else "ok")
        else:
            st, criado = api(page, "POST", "/rest/workflows", wf)
            print("criar:", st, str(criado)[:200] if st >= 300 else criado["id"])
            wid = criado["id"]
        ver = criado.get("versionId")
        st, r = api(page, "POST", f"/rest/workflows/{wid}/activate", {"versionId": ver})
        if st >= 300:
            st, r = api(page, "PATCH", f"/rest/workflows/{wid}", {"active": True, "versionId": ver})
        print("ativar:", st, str(r)[:300])

        caminho = next(n for n in wf["nodes"] if n["type"].endswith(".webhook"))["parameters"]["path"]
        time.sleep(2)
        resp = page.request.get(f"{BASE}/webhook/{caminho}?conta=CLI052938")
        print("API:", resp.status, resp.text()[:400])

        page.goto(f"{BASE}/workflow/{wid}")
        page.wait_for_timeout(5000)
        for sel in ['[data-test-id="evaluations-canvas-info-card-dismiss"]']:
            if page.locator(sel).count():
                page.locator(sel).first.click(force=True, timeout=3000)
        fechar = page.locator("text=Production Checklist").locator("xpath=..").locator("button, [role=button], svg").first
        if page.locator("text=Production Checklist").count():
            try:
                fechar.click(timeout=3000)
            except Exception:
                page.keyboard.press("Escape")
        page.wait_for_timeout(800)
        page.locator('[data-test-id="zoom-to-fit"]').click(force=True, timeout=5000)
        page.wait_for_timeout(1500)
        page.screenshot(path=str(IMG / "aula08-n8n-workflow.png"))
        print("captura: workflow")

        page.locator('[data-node-name="OpenRouter"]').first.dblclick(force=True, timeout=8000)
        page.wait_for_timeout(2500)
        page.screenshot(path=str(IMG / "aula08-n8n-openrouter.png"))
        print("captura: openrouter")
        page.keyboard.press("Escape")

        chat = next(n for n in wf["nodes"] if n["type"].endswith("chatTrigger"))
        url_chat = f"{BASE}/webhook/{chat['webhookId']}/chat"
        print("chat:", url_chat)
        c = ctx.new_page()
        c.goto(url_chat)
        c.wait_for_timeout(3000)
        caixa = c.locator("textarea").first
        caixa.fill(PERGUNTA)
        caixa.press("Enter")
        c.wait_for_timeout(30000)
        c.screenshot(path=str(IMG / "aula08-n8n-chat.png"))
        print("captura: chat")
        print("RESPOSTA:", c.locator("body").inner_text()[-1500:])
        print("WORKFLOW_ID:", wid)
        ctx.close()


if __name__ == "__main__":
    main(sys.argv[1])
