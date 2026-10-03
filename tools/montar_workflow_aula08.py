# -*- coding: utf-8 -*-
"""Monta painel/workflow_n8n.json, o workflow que o painel da Aula 08 oferece
para baixar.

Tres agentes em sequencia, cada um com o proprio modelo do OpenRouter: Atlas
(analista) responde com os numeros da fila, Vera (estrategista) aplica os planos
de acao das areas, Ciro (revisor) confere cada numero antes de a resposta sair.
O modelo de linguagem vem do painel, no campo modelo_llm, e cai no gratuito
quando o painel nao manda nenhum.

Gerado, nunca editado a mao. Nao leva dado nenhum: a fila chega a cada pergunta,
calculada pelo painel no navegador. Por isso o mesmo arquivo serve a todos os
grupos, e o aluno nao precisa rodar nada local para importar.

Depois de importar, o grupo troca NOME_DO_GRUPO no caminho do Webhook, escolhe a
propria credencial OpenRouter e ativa.

Uso: .venv/bin/python tools/montar_workflow_aula08.py
"""

from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "painel" / "workflow_n8n.json"

# Gratuito no OpenRouter (sufixo :free) e com bom desempenho no teste de
# 03/10/2026. Plano gratuito: 20 requisicoes por minuto e 50 por dia por conta
# sem credito comprado.
MODELO = "nvidia/nemotron-3-super-120b-a12b:free"
CAMINHO = "kovan-chat-NOME_DO_GRUPO"

LEITURA = """Como ler as colunas da fila:
- escore_de_perda: probabilidade de a conta parar de comprar, entre 0 e 1.
- receita_12m_usd: receita dos 12 meses até 2024-02.
- valor_esperado_usd: escore_de_perda vezes receita_12m_usd. É o critério de ordem da fila.
- receita_12m_como_fracao_do_pico_anual: 0,63 quer dizer que a conta comprou 63% do seu melhor ano, uma queda de 37%.
- receita_12m_dividida_pela_dos_12m_anteriores: acima de 1 cresceu, abaixo de 1 caiu.
- O escore mede parada de compra. Ele não mede conta que encolhe e continua comprando."""

DADOS = """RESUMO DO MODELO:
{{ JSON.stringify($('API do painel').first().json.body.modelo || {}) }}

FILA DO CICLO ({{ ($('API do painel').first().json.body.contas || []).length }} contas):
{{ JSON.stringify($('API do painel').first().json.body.contas || []) }}"""

PLANOS = """PLANOS DE AÇÃO POR ÁREA:
{{ JSON.stringify($('API do painel').first().json.body.planos || {}, null, 1) }}"""

ATLAS = """Você é Atlas, o analista da fila de retenção da Kovan Technologies LATAM. Você trabalha numa equipe de três agentes: você responde à pergunta com os números; Vera, a estrategista, recomenda a ação; Ciro, o revisor, confere tudo antes de a resposta chegar ao Account Manager.

O painel treinou uma regressão logística sobre a planilha original do case, com histórico até 2024-02, e ordenou a fila por valor esperado.

""" + LEITURA + """

Regras:
1. Todo número sai do material abaixo. Se o número não está lá, diga que não tem esse dado. Nunca estime.
2. Responda só com fatos e números da fila. Não recomende ação: isso é trabalho da Vera.
3. Português, no máximo seis linhas, sem emoji.

""" + DADOS

VERA = """Você é Vera, a estrategista de retenção da Kovan Technologies LATAM. Atlas, o analista, já respondeu com os números. Seu trabalho é dizer o que fazer, usando só os planos de ação das áreas.

""" + LEITURA + """

Regras:
1. Recomende só itens que estão nos planos abaixo. Para cada recomendação, diga a área, o item do plano e a coluna da conta que aciona o item, com o valor.
2. Se mais de uma área se aplica, cite todas. Se nenhum plano cobre o caso, diga isso e sugira levar ao Comitê de Receita.
3. Não invente ação, desconto nem condição comercial.
4. Se a pergunta não pede ação, responda apenas: Sem ação a recomendar para esta pergunta.
5. Português, no máximo oito linhas, sem emoji.

""" + PLANOS + """

""" + DADOS

CIRO = """Você é Ciro, o revisor da equipe de retenção da Kovan Technologies LATAM. Atlas respondeu com os números e Vera recomendou a ação. Você confere antes de a resposta chegar ao Account Manager.

""" + LEITURA + """

O que conferir:
1. Cada número citado por Atlas e Vera existe na fila abaixo, na conta certa.
2. Cada ação da Vera existe nos planos, e a coluna que ela citou de fato aciona o item.
3. Nenhum dos dois estimou dado ausente, prometeu desconto ou leu o escore como medida de encolhimento.

Formato obrigatório da sua resposta:
Primeira linha: VEREDITO: aprovado, ou VEREDITO: corrigido, seguido do motivo em uma frase.
Linha em branco.
Depois, a resposta final ao Account Manager, juntando o que Atlas e Vera disseram e corrigindo o que não confere. Português, no máximo dez linhas, sem emoji.

""" + PLANOS + """

""" + DADOS

MODELO_EXPR = "={{ $('API do painel').first().json.body.modelo_llm || '" + MODELO + "' }}"


def _agente(id_, nome, x, texto, sistema):
    return {"id": id_, "name": nome, "type": "@n8n/n8n-nodes-langchain.agent",
            "typeVersion": 1.7, "position": [x, 0],
            "parameters": {"promptType": "define", "text": texto,
                           "options": {"systemMessage": "=" + sistema}}}


def _llm(id_, nome, x):
    return {"id": id_, "name": nome, "type": "@n8n/n8n-nodes-langchain.lmChatOpenRouter",
            "typeVersion": 1, "position": [x, 240],
            "parameters": {"model": MODELO_EXPR, "options": {"temperature": 0.2}}}


PERGUNTA = "{{ $('API do painel').first().json.body.pergunta }}"


def montar() -> dict:
    u = "b1a1c1d1-0000-4000-8000-0000000000"
    nos = [
        {"id": u + "01", "name": "API do painel",
         "type": "n8n-nodes-base.webhook", "typeVersion": 2, "position": [0, 0],
         "webhookId": u + "aa",
         "parameters": {"httpMethod": "POST", "path": CAMINHO,
                        "responseMode": "responseNode",
                        "options": {"allowedOrigins": "*"}}},
        _agente(u + "02", "Atlas", 260, "=" + PERGUNTA, ATLAS),
        _agente(u + "03", "Vera", 560, "=Pergunta do Account Manager: " + PERGUNTA +
                "\n\nResposta do Atlas:\n{{ $('Atlas').first().json.output }}", VERA),
        _agente(u + "04", "Ciro", 860, "=Pergunta do Account Manager: " + PERGUNTA +
                "\n\nResposta do Atlas:\n{{ $('Atlas').first().json.output }}"
                "\n\nRecomendação da Vera:\n{{ $('Vera').first().json.output }}", CIRO),
        _llm(u + "05", "Modelo do Atlas", 200),
        {"id": u + "06", "name": "Memória do Atlas",
         "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow", "typeVersion": 1.3,
         "position": [360, 240],
         "parameters": {"sessionIdType": "customKey",
                        "sessionKey": "={{ $('API do painel').first().json.body.sessionId }}",
                        "contextWindowLength": 6}},
        _llm(u + "07", "Modelo da Vera", 560),
        _llm(u + "08", "Modelo do Ciro", 860),
        {"id": u + "09", "name": "Responder ao painel",
         "type": "n8n-nodes-base.respondToWebhook", "typeVersion": 1.1, "position": [1140, 0],
         "parameters": {"respondWith": "json", "options": {},
                        "responseBody": (
                            "={{ { modelo: $('API do painel').first().json.body.modelo_llm || '" + MODELO + "', "
                            "agentes: ["
                            "{ nome: 'Atlas', papel: 'Analista da fila', texto: $('Atlas').first().json.output }, "
                            "{ nome: 'Vera', papel: 'Estrategista de retenção', texto: $('Vera').first().json.output }, "
                            "{ nome: 'Ciro', papel: 'Revisor', texto: $json.output } ] } }}")}},
    ]

    def liga(origem, destino, tipo="main"):
        return {origem: {tipo: [[{"node": destino, "type": tipo, "index": 0}]]}}

    conexoes = {}
    for c in [liga("API do painel", "Atlas"), liga("Atlas", "Vera"), liga("Vera", "Ciro"),
              liga("Ciro", "Responder ao painel"),
              liga("Modelo do Atlas", "Atlas", "ai_languageModel"),
              liga("Memória do Atlas", "Atlas", "ai_memory"),
              liga("Modelo da Vera", "Vera", "ai_languageModel"),
              liga("Modelo do Ciro", "Ciro", "ai_languageModel")]:
        conexoes.update(c)
    return {"name": "Kovan · Equipe de agentes do painel", "nodes": nos, "connections": conexoes,
            "settings": {"executionOrder": "v1"}}


def main() -> None:
    SAIDA.write_text(json.dumps(montar(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{SAIDA.relative_to(RAIZ)} gravado")


if __name__ == "__main__":
    main()
