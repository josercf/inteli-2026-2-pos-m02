# -*- coding: utf-8 -*-
"""Monta aulas/aula09.html.

Gerado, nunca editado a mao: a numeracao de rodape e o fechamento de secao sao
garantidos aqui.

A Aula 09 e o fechamento conjunto do modulo, conduzido pelos professores das
duas trilhas. A programacao veio do professor da trilha de Tecnologia em
09/10/2026: recap das duas trilhas, tira-duvidas, finalizacao dos artefatos e
apresentacao. Horario de cada bloco e tempo por grupo nao foram definidos, e o
deck nao os inventa (ver PLANEJAMENTO_AULA_A_AULA.md).

O recap de Negocios sintetiza os decks do Prof. Rafael Donaire, que ficam em
recebidos/ e nao sao republicados: o deck cita os conceitos e as fontes
originais, sem copiar slide (ADR-011).

Nenhum numero novo do case entra aqui. Todo numero vem de um deck anterior e
esta travado em dados/tests; tools/tests/test_deck_aula09.py confere isso
numero a numero.

Diretiva editorial: sem paralelismo negativo, sem antitese simetrica, sem
escalada com dois-pontos. Titulo de slide de conteudo e a conclusao completa,
com o numero dentro; slide de referencia leva titulo descritivo.

Uso: python3 tools/montar_deck_aula09.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from tools import deck_kit  # noqa: E402
from tools.deck_kit import conteudo, pratica, quiz, secao  # noqa: E402

SAIDA = RAIZ / "aulas" / "aula09.html"

deck_kit.configurar("Módulo 2 &middot; Aula 09 &middot; Negócios e Tecnologia")
deck_kit.reiniciar_paginacao()

NEG = "Prof. Rafael Donaire"
TEC = "Prof. José Romualdo da Costa Filho"
SLIDES: list[str] = []


def tabela(cabecalho, linhas, classe="tabela-criterios enxuta", marcas=None, th_classes=None):
    """Tabela do tema. `marcas` mapeia indice de linha para classe de <tr>."""
    marcas = marcas or {}
    th_classes = th_classes or [None] * len(cabecalho)
    th = "".join(
        f'<th class="{c}">{t}</th>' if c else f"<th>{t}</th>"
        for t, c in zip(cabecalho, th_classes)
    )
    corpo = ""
    for i, linha in enumerate(linhas):
        attr = f' class="{marcas[i]}"' if i in marcas else ""
        corpo += f"            <tr{attr}>" + "".join(f"<td>{c}</td>" for c in linha) + "</tr>\n"
    return (f'        <table class="{classe}">\n'
            f"          <thead><tr>{th}</tr></thead>\n"
            "          <tbody>\n" + corpo + "          </tbody>\n"
            "        </table>\n")


def icone(nome):
    return f'<span class="material-symbols-outlined">{nome}</span>'


# ---------------------------------------------------------------------------
# Capa
# ---------------------------------------------------------------------------
SLIDES.append(
    '      <section class="cover-slide">\n'
    '        <div class="cover-panel">\n'
    '          <div class="cover-content">\n'
    '            <p class="cover-eyebrow">MBA em IA e Dados para Negócios &middot; Inteli x Lenovo</p>\n'
    "            <h1>Fechamento do módulo</h1>\n"
    "            <h3>Recap das duas trilhas, tira-dúvidas, finalização e apresentação do Artefato 2 ao Comitê de Receita da Kovan</h3>\n"
    '            <p class="cover-meta">Módulo 2 &middot; Aula 09 &middot; Aula conjunta, Negócios e Tecnologia</p>\n'
    f'            <p class="cover-meta">{NEG} e {TEC}</p>\n'
    "          </div>\n"
    "        </div>\n"
    "      </section>\n"
)

# ---------------------------------------------------------------------------
# Programação
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Programação do encontro",
    tabela(["Bloco", "O que acontece", "Quem conduz", "O que sai"], [
        ["a) Recap", "as duas trilhas, aula a aula, e o que cada uma entrega ao Artefato 2",
         "os dois professores", "o mapa do que já está pronto"],
        ["b) Tira-dúvidas", "dúvidas de negócio e de tecnologia, triadas por trilha",
         "os dois professores", "a lista do que falta, por grupo"],
        ["c) Finalização", "os grupos fecham o deck executivo e o aplicativo",
         "os grupos, com os professores nas mesas", "os dois artefatos prontos"],
        ["d) Apresentação", "cada grupo defende o projeto no papel do Comitê de Receita",
         "os grupos, com os dois professores na banca", "feedback das duas trilhas"],
    ], classe="tabela-criterios"),
    conclusao="Cada bloco usa o produto do anterior: a lista do tira-dúvidas organiza a finalização, e a finalização vira a apresentação.",
))

# ---------------------------------------------------------------------------
# Resgate
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A Aula 08 deixou a fila de 138 contas no painel publicado, e hoje ela entra no plano de retenção",
    '        <div class="stat-tiles">\n'
    '          <div class="stat-tile"><p class="stat-numero">4.593</p><p class="stat-rotulo">contas elegíveis no modelo do painel</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">0,814</p><p class="stat-rotulo">AUC fora da amostra, calculada no navegador</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">138</p><p class="stat-rotulo">contas na fila, o teto de planos do ciclo</p></div>\n'
    '          <div class="stat-tile destaque"><p class="stat-numero">USD 26,6 mi</p><p class="stat-rotulo">valor esperado da fila</p></div>\n'
    "        </div>\n"
    '        <p class="linha-contexto">Na trilha de Negócios, a última aula discutiu agentes de IA em vendas B2B a partir da pesquisa da BCG, com a mesma restrição de 138 planos.</p>\n',
    contexto="O painel lê a planilha original, treina a regressão logística e envia a fila aos três agentes no n8n.",
    conclusao="O Artefato 2 junta o plano de retenção da Negócios ao aplicativo da Tecnologia, com os mesmos números nos dois.",
    fonte="Fonte: dados/analise_aula08.py, travado em dados/tests/test_aula08_numeros.py.",
))

# ---------------------------------------------------------------------------
# Mapa do módulo
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Mapa do módulo nas duas trilhas",
    tabela(["Encontro", "Negócios", "Tecnologia"], [
        ["08/08", "Do problema à hipótese", "Da hipótese à evidência"],
        ["15/08", "Segmentação de contas B2B", "O dado sujo é o case"],
        ["22/08", "Personas como arquétipo de conta", "O corte que define o rótulo"],
        ["29/08", "Valor contra risco na priorização", "A figura que decide"],
        ["05/09", f"{icone('flag')}Entrega 1: Customer Segmentation Analysis Report",
         f"{icone('flag')}Entrega 1: Análise Exploratória de Dados"],
        ["12/09", "manhã conduzida pela trilha de Tecnologia", "As variáveis de entrada, treino e avaliação"],
        ["Aulas 6 e 7", "Intervenção a partir do caso HubSpot", "Do script à tela"],
        ["Aula 08", "Agentes de IA em vendas B2B", "Do modelo à equipe de agentes"],
        ["Hoje", f"{icone('flag')}Entrega 2: Plano de Inteligência de Retenção",
         f"{icone('flag')}Entrega 2: Aplicativo Web Preditivo-Generativo"],
    ], classe="tabela-criterios enxuta mapa", marcas={4: "entrega", 8: "entrega"},
        th_classes=[None, "negocios", "tecnologia"]),
    conclusao="As duas entregas do módulo caíram no mesmo encontro nas duas trilhas, e a de hoje é apresentada aos dois professores.",
))

# ---------------------------------------------------------------------------
# 01 Recap de Negócios
# ---------------------------------------------------------------------------
SLIDES.append(secao("01", "Recap da trilha de Negócios", f"{NEG}: da hipótese aos agentes de IA em vendas",
                    ["Hipótese e segmentação", "Valor, risco e intervenção", "Agentes em vendas B2B"]))

SLIDES.append(conteudo(
    "Uma hipótese só entra no modelo quando é clara, mensurável e falseável",
    tabela(["Forma", "Exemplo da aula", "O que permite"], [
        ["Vaga", "&quot;O preço deve estar alto, é por isso que cancelam.&quot;",
         "nada: não tem variável nem prazo, e nenhum dado a refuta"],
        ["Específica", "&quot;Plano mensal cancela 5x mais que plano anual nos primeiros 30 dias.&quot;",
         "teste direto, com variável e janela declaradas"],
        ["Condicional", "&quot;SE o preço for a causa, ENTÃO reduzir 15% corta o churn em 3 pp ou mais em 60 dias.&quot;",
         "plano de ação com gatilho de abandono"],
    ], marcas={2: "destaque"}),
    contexto="O HIPPO, a opinião de quem ganha mais na sala, decide sem dado. A hipótese falseável tira a decisão dele.",
    conclusao="Na Kovan, a hipótese declara o alvo (Caminho A ou B), o sinal na base e a restrição de 138 planos por trimestre.",
    fonte="Fonte: Donaire, aula 1 de Negócios; Popper (1934); Courtney, Kirkland e Viguerie, HBR (1997).",
))

SLIDES.append(conteudo(
    "Um segmento que falha em dois dos cinco critérios de Kotler sai da proposta",
    tabela(["Critério", "Pergunta que o segmento precisa responder"], [
        ["Mensurável", "dá para saber o tamanho do grupo?"],
        ["Acessível", "dá para chegar até ele pelos canais da Kovan?"],
        ["Substancial", "o grupo é grande o bastante para ser lucrativo?"],
        ["Diferenciável", "ele reage de forma distinta aos estímulos?"],
        ["Acionável", "dá para formular um programa efetivo para ele?"],
    ]),
    contexto="No B2B a unidade de análise é a conta, descrita por firmografia e por comportamento de compra.",
    conclusao="Contas-chave atípicas saem antes da segmentação, pelo critério de Spoor, para não distorcer o resto da carteira.",
    fonte="Fonte: Donaire, aula 2 de Negócios; Kotler; Spoor, Journal of Marketing Analytics (2022).",
))

SLIDES.append(conteudo(
    "A persona da Kovan é um arquétipo de conta, e cada atributo dela precisa de uma variável na EDA",
    tabela(["Campo da persona", "O que contém"], [
        ["Nome", "curto e memorável, pelo padrão de comportamento, nunca nome de pessoa"],
        ["Tamanho", "quantas contas o segmento tem, contadas na base"],
        ["Perfil de compra", "faixas reais de receita, linhas ativas, recência e pedidos"],
        ["Dor inferida", "hipótese justificada pelo padrão observado"],
        ["Valor estratégico", "por que o segmento importa para a receita da Kovan"],
        ["Driver e prioridade", "intervenção imediata ou monitoramento, pelo valor do segmento contra o risco do sinal"],
    ]),
    conclusao="Persona sem âncora em dado é o primeiro erro da lista de erros comuns da trilha de Negócios.",
    fonte="Fonte: Donaire, aulas 1, 3 e 4 de Negócios.",
))

SLIDES.append(conteudo(
    "Importância e dificuldade de gerir são eixos separados, e cada quadrante pede um tratamento",
    '        <div class="matriz">\n'
    "          <div></div>\n"
    '          <div class="eixo">Baixa dificuldade de gerir</div>\n'
    '          <div class="eixo">Alta dificuldade de gerir</div>\n'
    '          <div class="eixo linha">Alta importância</div>\n'
    '          <div class="quadrante forte"><h3>Parceria</h3><p>cooperação extrema e desenvolvimento conjunto de produto</p></div>\n'
    '          <div class="quadrante medio"><h3>Investir com cautela</h3><p>importância alta numa relação custosa de manter</p></div>\n'
    '          <div class="eixo linha">Baixa importância</div>\n'
    '          <div class="quadrante"><h3>Manter</h3><p>atendimento padronizado, com custo mínimo de gestão</p></div>\n'
    '          <div class="quadrante saida"><h3>Desinvestir</h3><p>migrar para atendimento automatizado ou sair</p></div>\n'
    "        </div>\n",
    contexto="A reversibilidade da decisão define quanta deliberação ela merece antes de agir sobre o quadrante.",
    conclusao="Best Buy, Netflix, State Farm e Microsoft mostraram que a decisão sobre o quadrante de saída tem custo além do financeiro.",
    fonte="Fonte: Donaire, aula 4 de Negócios.",
))

SLIDES.append(conteudo(
    "No caso HubSpot, a prioridade de atendimento pesa risco, valor, resposta e esforço",
    tabela(["Critério", "Pergunta para o público escolhido"], [
        ["Risco", "qual perda pode ocorrer, e em que horizonte?"],
        ["Valor", "qual contribuição econômica está em jogo?"],
        ["Resposta", "por que a ação pode fazer diferença neste cliente?"],
        ["Esforço", "qual custo e qual capacidade a intervenção exige?"],
    ], marcas={2: "destaque"}),
    contexto="O CHI, índice de saúde do cliente, localiza o risco e, quando vira meta da equipe, sobe sem o cliente ganhar valor.",
    conclusao="Na Kovan, a resposta à intervenção é o critério que um modelo de churn não mede, e por isso Cláudia Meireles exige grupo de controle.",
    fonte="Fonte: Martínez-Jerez, Steenburgh, Avery e Brem, caso HubSpot, Harvard Business School; Donaire, aulas 6 e 7.",
))

SLIDES.append(conteudo(
    "Os sinais da Kovan vêm da compra, e a intervenção passa pelo Account Manager",
    tabela(["Dimensão", "HubSpot", "Kovan"], [
        ["Relação comercial", "assinatura com avaliação recorrente de valor", "compras corporativas em ciclos longos"],
        ["Sinais", "uso e resultados observáveis do software", "cadência, receita e amplitude de mix"],
        ["Perda", "cancelamento da assinatura", "ruptura e erosão de compras"],
        ["Intervenção", "atendimento, adoção, produto e aquisição", "diagnóstico e atuação do Account Manager"],
    ], classe="tabela-criterios pares"),
    conclusao="Com ciclo longo de renovação, parte das quedas de compra é calendário, e o plano precisa separar esse caso do risco real.",
    fonte="Fonte: Donaire, aulas 6 e 7 de Negócios.",
))

SLIDES.append(conteudo(
    "A BCG põe 70% do esforço de uma transformação com IA em pessoas e processos",
    '        <div class="processo-fases quatro degraus">\n'
    '          <div class="processo-fase"><p class="nivel">Nível 1</p><h4>Tradicional</h4><p>intuição e experiência do vendedor</p></div>\n'
    '          <div class="processo-fase"><p class="nivel">Nível 2</p><h4>Aumentada</h4><p>a IA sugere próximas ações e materiais</p></div>\n'
    '          <div class="processo-fase ativa"><p class="nivel">Nível 3</p><h4>Assistida</h4><p>a IA acompanha a chamada e atualiza o CRM</p></div>\n'
    '          <div class="processo-fase"><p class="nivel">Nível 4</p><h4>Autônoma</h4><p>o agente engaja o cliente e aciona um humano quando precisa</p></div>\n'
    "        </div>\n"
    '        <div class="stat-tiles tres">\n'
    '          <div class="stat-tile"><p class="stat-numero">10%</p><p class="stat-rotulo">do esforço em algoritmos</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">20%</p><p class="stat-rotulo">em tecnologia e dados</p></div>\n'
    '          <div class="stat-tile destaque"><p class="stat-numero">70%</p><p class="stat-rotulo">em pessoas e processos</p></div>\n'
    "        </div>\n",
    conclusao="Na Kovan, a BCG indica autonomia maior do agente na cauda longa, que hoje só recebe contato reativo.",
    fonte="Fonte: BCG, How AI Agents Will Transform B2B Sales (2025); Donaire, aula de agentes de IA em vendas B2B.",
))

# ---------------------------------------------------------------------------
# 02 Recap de Tecnologia
# ---------------------------------------------------------------------------
SLIDES.append(secao("02", "Recap da trilha de Tecnologia", f"{TEC}: da base oficial ao painel com três agentes",
                    ["EDA e rótulo", "Modelo e fila", "Agentes e painel"]))

SLIDES.append(conteudo(
    "A EDA fixou o rótulo em 08/02/2025 e a perda entre 25,4% e 58,1% por segmento",
    tabela(["Aula", "Achado", "Número"], [
        ["01", "hipótese testável declara variável, operação, janela e critério de refutação", "caderno de hipóteses"],
        ["02", "o sinal das devoluções muda a receita líquida", "R$ 217,4 milhões"],
        ["03", "o rótulo marca quem parou de comprar até 08/02/2025", "19,2% de 8.282 contas"],
        ["03", "a receita se concentra no topo da carteira", "1% das contas, 65,1% da receita"],
        ["04", "conta com primeira compra depois de 2025-02 não pode ser marcada", "4.534 contas"],
        ["04", "a perda entre elegíveis varia com o segmento", "de 25,4% a 58,1%"],
    ], marcas={5: "destaque"}),
    conclusao="O Artefato 1 entregou esses números, e o diagnóstico do deck executivo parte deles.",
    fonte="Fonte: dados/analise_aula03.py e dados/analise_aula04.py, travados em dados/tests.",
))

SLIDES.append(conteudo(
    "Retirar a coluna vazada leva a AUC de 0,9999 para 0,834",
    tabela(["Aula", "Decisão", "Número"], [
        ["06", "o corte temporal separa observação de rótulo na base longa", "36 meses de observação e 29 de rótulo"],
        ["06", "a recência no corte lidera as colunas honestas", "AUC isolada de 0,818"],
        ["06", "a fila de 138 é medida pelo erro que custa mais caro", "precisão de 75,8% e revocação de 82,2%"],
        ["07", "o critério de ordenação decide a receita alcançada", "68,4% da receita em risco"],
        ["08", "o modelo roda no navegador, sobre a planilha original", "AUC de 0,814 em 4.593 contas"],
    ]),
    conclusao="Uma AUC perto de 1 é sinal de vazamento antes de ser sinal de modelo bom.",
    fonte="Fonte: dados/analise_aula06_longa.py, analise_aula07.py e analise_aula08.py, travados em dados/tests.",
))

SLIDES.append(conteudo(
    "Ordenar a fila por valor esperado leva a receita alcançada de 0,01% para 68,4%",
    '        <table class="tabela-duelo">\n'
    "          <thead><tr><th>Fila de 138 contas</th><th>Por probabilidade</th><th>Por valor esperado</th></tr></thead>\n"
    "          <tbody>\n"
    '            <tr><td>Precisão: perdas reais entre as sinalizadas</td><td class="num vence">85,5%</td><td class="num">29,7%</td></tr>\n'
    '            <tr><td>Receita em risco que a fila alcança</td><td class="num">0,01%</td><td class="num vence">68,4%</td></tr>\n'
    '            <tr><td>Posição da Conta D, a maior da carteira</td><td class="num">3.024º</td><td class="num vence">1º</td></tr>\n'
    "          </tbody>\n"
    "        </table>\n",
    contexto="Mesmo modelo e mesmas 138 vagas. Só o critério de ordenação muda entre as duas colunas.",
    conclusao="A escolha do critério é a decisão que o Comitê vai cobrar, porque cada coluna atende uma voz diferente da mesa.",
    fonte="Fonte: dados/analise_aula07.py, travado em dados/tests/test_aula07_numeros.py.",
))

ELOS = [
    ("table_view", "Planilha", "a base longa do case, lida no navegador", "65 meses"),
    ("event", "Corte", "histórico antes do corte, sem compra posterior", "07/03/2024"),
    ("model_training", "Modelo", "regressão logística treinada no próprio painel", "AUC 0,814"),
    ("format_list_numbered", "Fila", "ordenada pelo critério do grupo", "138 contas"),
    ("groups", "Agentes", "Atlas analisa, Vera recomenda e Ciro revisa", "3 agentes"),
    ("public", "Painel", "publicado no GitHub Pages pelo grupo", "URL do grupo"),
]
cadeia = '        <div class="cadeia">\n'
for i, (ic, titulo, texto, metrica) in enumerate(ELOS):
    classe = "elo destaque" if i == len(ELOS) - 1 else "elo"
    cadeia += (f'          <div class="{classe}">{icone(ic)}<h4>{titulo}</h4><p>{texto}</p>'
               f'<p class="metrica">{metrica}</p></div>\n')
    if i < len(ELOS) - 1:
        cadeia += f'          <span class="seta material-symbols-outlined">arrow_forward</span>\n'
cadeia += "        </div>\n"

SLIDES.append(conteudo(
    "O Artefato 2 encadeia seis etapas, da planilha original ao painel publicado",
    cadeia,
    contexto="Cada etapa da cadeia foi construída numa aula e reaproveitada pela seguinte, sem reimplementar a conta.",
    conclusao="Na apresentação, cada etapa precisa de uma prova na tela, e o número da fila precisa ser o mesmo do deck executivo.",
    fonte="Fonte: painel/modelo.js e dados/analise_aula08.py; corte temporal em dados/tests/test_aula06_longa.py.",
))

SLIDES.append(quiz(
    "Verificação &middot; integração das trilhas",
    "Qual voz do Comitê essa fila atende?",
    "A fila de 138 contas ordenada por probabilidade acerta 85,5% e alcança 0,01% da receita em risco. Qual voz da mesa ela atende?",
    [
        {"texto": "Bruno, Diretor Comercial", "certa": True,
         "certo": "Certo: Bruno pede um modelo que fale pouco e erre pouco, e 85,5% de precisão atende esse pedido. Priscila recusaria a mesma fila pela receita alcançada.",
         "errado": ""},
        {"texto": "Priscila Nakamura, Head de Analytics e CS", "certa": False,
         "certo": "", "errado": "Não: Priscila quer proteger a receita, e a fila alcança só 0,01% da receita em risco."},
        {"texto": "Cláudia Meireles, VP Financeira", "certa": False,
         "certo": "", "errado": "Não: Cláudia cobra grupo de controle, e nenhuma ordenação da fila responde a isso sozinha."},
        {"texto": "As três ao mesmo tempo", "certa": False,
         "certo": "", "errado": "Não: a fila atende a precisão que Bruno pede e falha na receita que Priscila cobra."},
    ],
    {"fichas": [("Critério", "probabilidade"), ("Precisão", "85,5%"), ("Receita alcançada", "0,01%")]},
))

# ---------------------------------------------------------------------------
# 03 Tira-dúvidas
# ---------------------------------------------------------------------------
SLIDES.append(secao("03", "Sessão de tira-dúvidas", "Cada dúvida vai para a trilha que a responde",
                    ["Triagem", "Erros recorrentes", "Lista do grupo"]))

SLIDES.append(conteudo(
    "Triagem das dúvidas por trilha",
    tabela(["Tipo de dúvida", "Exemplos", "Quem responde", "Onde consultar"], [
        ["Negócio", "persona, priorização, plano de 10 semanas, ROI", NEG, "checklist de Negócios, neste deck"],
        ["Dado e modelo", "rótulo, corte temporal, métrica, critério da fila", TEC, "materiais das Aulas 03, 04 e 06"],
        ["Aplicativo", "painel, n8n, chave, bateria, publicação", TEC, "guia passo a passo da Aula 08"],
        ["Integração", "número do aplicativo que entra no deck executivo", "os dois professores", "slide Do aplicativo ao deck executivo"],
    ], classe="tabela-criterios", marcas={3: "destaque"}),
    conclusao="Dúvida que não fecha na sessão vira item da lista do grupo para a finalização.",
))

SLIDES.append(conteudo(
    "Erros recorrentes que a banca procura",
    tabela(["Erro", "Trilha", "Correção"], [
        ["Persona sem âncora em dado", "Negócios", "todo atributo com variável correspondente na EDA"],
        ["Segmento genérico demais", "Negócios", "nome com intenção estratégica e os cinco critérios de Kotler"],
        ["Valor financeiro ausente", "Negócios", "receita em risco declarada no documento final"],
        ["AUC perto de 1", "Tecnologia", "procurar a coluna que repete o rótulo"],
        ["Número fora da fila na resposta do agente", "Tecnologia", "reprovar na bateria e reforçar a regra de origem no prompt"],
        ["0,63 do pico lido como queda de 63%", "Tecnologia", "nome de coluna explícito e leitura explicada no prompt"],
        ["Test URL do n8n colada no painel", "Tecnologia", "Production URL, com o workflow publicado"],
    ], classe="tabela-criterios enxuta rotulo-largo"),
    conclusao="Conferir esta lista antes da apresentação custa menos que ouvir o item pela primeira vez na banca.",
    fonte="Fonte: Donaire, aula 1 de Negócios (erros comuns); demonstrações das Aulas 06 a 08 de Tecnologia.",
))

# ---------------------------------------------------------------------------
# 04 Finalização
# ---------------------------------------------------------------------------
SLIDES.append(secao("04", "Sessão de finalização", "Deck executivo e aplicativo, com os mesmos números",
                    ["Checklist de Negócios", "Checklist de Tecnologia", "Do aplicativo ao deck"]))

SLIDES.append(conteudo(
    "Checklist do Artefato 2 de Negócios: Plano de Inteligência de Retenção",
    tabela(["Seção", "O que precisa conter"], [
        ["Diagnóstico", "o churn da Kovan em linguagem de negócio, com a receita em risco"],
        ["Segmentos", "os segmentos de cancelamento identificados ao longo do módulo"],
        ["Caminhos A e B", "comparação em impacto financeiro, prazo, risco e posicionamento competitivo"],
        ["Recomendação", "o caminho escolhido, a oferta por persona e o papel da IA generativa"],
        ["Plano de ação", "milestones das primeiras 10 semanas"],
        ["Grupo de controle", "contas sinalizadas fora da intervenção, para provar o ROI"],
        ["Riscos", "riscos e contingências de cada um"],
    ]),
    conclusao="O deck é lido como num Conselho de Administração: cada seção abre pelo número e fecha pela decisão pedida.",
    fonte="Fonte: Donaire, aulas 1, 2, 6 e 7 de Negócios.",
))

SLIDES.append(conteudo(
    "Checklist do Artefato 2 de Tecnologia: Aplicativo Web Preditivo-Generativo",
    tabela(["Item", "Prova na apresentação"], [
        ["Modelo treinado", "AUC fora da amostra na tela, sem coluna posterior ao corte"],
        ["Fila priorizada", "o critério de ordenação declarado e as 138 contas"],
        ["Camada generativa", "texto de retenção por conta, escrito pela equipe de agentes"],
        ["Planos de ação", "três planos com limiar numérico em cada item"],
        ["Bateria de teste", "o placar e uma reprovação corrigida em <code>teste_agente.md</code>"],
        ["Interface publicada", "a URL do GitHub Pages aberta em outra máquina"],
        ["Limitações", "o que o modelo não sabe, escrito na própria tela"],
    ]),
    conclusao="A planilha, a chave de API e o endpoint do n8n ficam fora do repositório público do grupo.",
    fonte="Fonte: PLANO_DE_ENSINO.md, seção 4; checkpoints das Aulas 07 e 08.",
))

SLIDES.append(conteudo(
    "Do aplicativo ao deck executivo",
    tabela(["Seção do deck", "Número que vem do aplicativo", "Origem"], [
        ["Diagnóstico", "prevalência de 19,2% e perda de 25,4% a 58,1% por segmento", "Artefato 1"],
        ["Caminhos A e B", "precisão da fila contra receita em risco alcançada", "Aula 07"],
        ["Plano de ação", "138 contas por ciclo, na ordem do critério do grupo", "painel"],
        ["Business case de ROI", "valor esperado da fila, USD 26,6 milhões", "painel"],
        ["Grupo de controle", "a parte da fila que fica fora da intervenção", "decisão do grupo"],
    ], marcas={3: "destaque"}),
    conclusao="Número diferente entre o deck e o aplicativo é a primeira pergunta da banca.",
))

SLIDES.append(pratica(
    1, "Fechar os dois artefatos com os mesmos números", None,
    None, None, None,
    [
        {"acao": "Abra os dois checklists e marque o que já tem prova.",
         "detalhe": "Item sem prova na tela ou no deck conta como pendente."},
        {"acao": "Confira que cada número do aplicativo é o mesmo no deck executivo.",
         "detalhe": "Prevalência, tamanho da fila, precisão, receita alcançada e valor esperado."},
        {"acao": "Rode a bateria uma última vez e registre o placar.",
         "detalhe": "Faça também uma pergunta fora da bateria, como a banca fará."},
        {"acao": "Ensaie a apresentação com a demonstração ao vivo do painel.",
         "detalhe": "Deixe a planilha local e a URL publicada abertas antes de começar."},
    ],
    "Os dois checklists sem item pendente e a URL do painel aberta",
    trilho=False,
    sobrelinha="Sessão de finalização &middot; em grupo &middot; deck executivo e aplicativo",
))

# ---------------------------------------------------------------------------
# 05 Apresentação
# ---------------------------------------------------------------------------
SLIDES.append(secao("05", "Sessão de apresentação", "O grupo defende o projeto no papel do Comitê de Receita da Kovan",
                    ["Roteiro", "As perguntas da mesa", "Feedback das duas trilhas"]))

SLIDES.append(conteudo(
    "Roteiro da apresentação ao Comitê",
    tabela(["Ordem", "Momento", "O que mostrar"], [
        ["1", "Diagnóstico", "o churn da Kovan e a receita em risco"],
        ["2", "Segmentos e personas", "quem perde, com o número de cada segmento"],
        ["3", "Caminhos A e B", "a comparação nas quatro dimensões e o caminho escolhido"],
        ["4", "Aplicativo ao vivo", "a fila, uma conta aberta e a resposta da equipe de agentes"],
        ["5", "Plano e ROI", "as primeiras 10 semanas, o grupo de controle e o retorno esperado"],
        ["6", "Riscos", "o que pode falhar e a contingência de cada risco"],
    ], marcas={3: "destaque"}),
    conclusao="A demonstração entra no meio do argumento, como prova da recomendação.",
))

SLIDES.append(conteudo(
    "Bruno, Priscila e Cláudia cobram precisão, receita alcançada e grupo de controle",
    tabela(["Voz", "Posição no case", "Pergunta provável", "Evidência do grupo"], [
        ["Bruno, Diretor Comercial", "um modelo que fale pouco e erre pouco",
         "quantas contas sinalizadas são perda real?", "precisão da fila"],
        ["Priscila Nakamura, Head de Analytics e CS", "o modelo precisa proteger a receita",
         "quanto da receita em risco a fila alcança?", "receita alcançada"],
        ["Cláudia Meireles, VP Financeira", "exige grupo de controle",
         "como o ROI será provado no fim do ano?", "desenho do grupo de controle"],
    ], classe="tabela-criterios"),
    conclusao="A banca também faz uma pergunta ao vivo para a equipe de agentes, fora da bateria do grupo.",
    fonte="Fonte: Kovan Technologies LATAM, business case PL-02-2026; Donaire, aula 1 de Negócios.",
))

SLIDES.append(conteudo(
    "O módulo começou num backlog de hipóteses e fecha com um aplicativo defendido em banca",
    '        <div class="linha-tempo">\n'
    '          <div class="etapa fragment"><p class="quando">Aula 01</p><h3>Hipóteses</h3>'
    "<p>O backlog do grupo e um rótulo que não existia no painel.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">Entrega 1</p><h3>Diagnóstico</h3>'
    "<p>A EDA e a segmentação com personas ancoradas em dado.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">Aulas 06 a 08</p><h3>Modelo e agentes</h3>'
    "<p>As colunas sem vazamento, a fila por valor esperado e a equipe no n8n.</p></div>\n"
    '          <div class="etapa avaliada fragment"><p class="quando">Hoje &middot; Entrega 2</p><h3>Banca</h3>'
    "<p>O plano de retenção e o aplicativo, apresentados aos dois professores.</p></div>\n"
    "        </div>\n",
    conclusao="O método atravessa as duas trilhas: hipótese falseável, número com origem e decisão declarada.",
    por_passos=True,
))

SLIDES.append(conteudo(
    "Referências e nota metodológica",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>Caso e material</h3>'
    "<p>1. Kovan Technologies LATAM: A Definição do Alvo. Business case PL-02-2026, versão v2.</p>"
    "<p>2. Donaire, R. Inteligência de Mercado e Modelagem Preditiva. Aulas da trilha de Negócios, 2026.</p>"
    "<p>3. Decks e materiais das Aulas 01 a 08 da trilha de Tecnologia.</p></div>\n"
    '          <div class="concept-card"><h3>Negócios</h3>'
    "<p>4. Courtney, H.; Kirkland, J.; Viguerie, P. Strategy Under Uncertainty. HBR, 1997.</p>"
    "<p>5. Spoor, J. M. Improving customer segmentation via classification of key accounts as outliers. JMA, 2022.</p>"
    "<p>6. BCG. How AI Agents Will Transform B2B Sales. 2025.</p></div>\n"
    '          <div class="concept-card"><h3>Tecnologia</h3>'
    "<p>7. Kaufman, S. et al. Leakage in Data Mining. ACM TKDD, 2012.</p>"
    "<p>8. Martínez-Jerez, F. A. et al. Caso HubSpot. Harvard Business School.</p>"
    "<p>9. Yao, S. et al. ReAct. ICLR, 2023.</p></div>\n"
    "        </div>\n",
    conclusao="A Aula 09 não introduz número novo do case: cada número vem de uma aula anterior e está travado em dados/tests.",
))

SLIDES.append(
    '      <section class="end-slide">\n'
    "        <h1>Obrigado</h1>\n"
    "        <h3>Módulo 2 &middot; Inteligência de Mercado e Modelagem Preditiva</h3>\n"
    '        <div class="assinaturas">\n'
    f'          <div><p class="papel">Negócios</p><p>{NEG}</p></div>\n'
    f'          <div><p class="papel">Tecnologia</p><p>{TEC}</p></div>\n'
    "        </div>\n"
    "      </section>\n"
)

# ---------------------------------------------------------------------------
# Esqueleto
# ---------------------------------------------------------------------------
ESQUELETO = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aula 09 &middot; Fechamento do Módulo 2 &middot; MBA Inteli x Lenovo</title>

  <!-- Gerado por tools/montar_deck_aula09.py. Nao editar a mao. -->

  <link rel="stylesheet" href="../assets/vendor/reveal/reveal.css">
  <link rel="stylesheet" href="../assets/css/inteli-brand.css">
  <link rel="stylesheet" href="../assets/css/inteli-theme.css">
  <link rel="stylesheet" href="../assets/css/inteli-print.css" media="print">
</head>
<body>
  <div class="reveal">
    <div class="slides">

{slides}
    </div>
  </div>

  <script src="../assets/vendor/reveal/reveal.js"></script>
  <script>
    Reveal.initialize({{
      width: 1280, height: 720, center: false, margin: 0,
      hash: true, slideNumber: false, transition: 'fade'
    }});
  </script>
  <script src="../assets/js/inteli-quiz.js"></script>
  <script src="../assets/js/inteli-zoom.js"></script>
  <script src="../assets/js/inteli-print.js"></script>
</body>
</html>
"""


def main() -> None:
    ultima = deck_kit.montar(SLIDES, ESQUELETO, SAIDA)
    print(f"{SAIDA.name}: {len(SLIDES)} slides, numerados de 2 a {ultima}")


if __name__ == "__main__":
    main()
