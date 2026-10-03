# -*- coding: utf-8 -*-
"""Monta aulas/aula08.html.

Gerado, nunca editado a mao: a numeracao de rodape e o fechamento de secao sao
garantidos aqui.

Diretiva editorial: sem paralelismo negativo, sem antitese simetrica, sem
escalada com dois-pontos. Titulo de slide de conteudo e a conclusao completa,
com o numero dentro. Travado por tools/check_retorica.py.

Todo numero do case que aparece aqui sai de `app.publicar`, no repositorio de
pratica, e esta travado em dados/tests/test_aula08_numeros.py.

As capturas de tela do n8n saem de tools/capturar_n8n_aula08.py, rodado contra
a instancia do Inteli com o workflow que `app.publicar` gera.

Uso: python3 tools/montar_deck_aula08.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from tools import deck_kit  # noqa: E402
from tools.deck_kit import conteudo, pratica, quiz, secao  # noqa: E402

SAIDA = RAIZ / "aulas" / "aula08.html"

deck_kit.configurar("Módulo 2 &middot; Aula 08")
deck_kit.reiniciar_paginacao()

AMBIENTE = "n8n"
N8N = '<a href="https://inteli.app.n8n.cloud/">inteli.app.n8n.cloud</a>'
PAINEL = "https://josercf.github.io/inteli-2026-2-pos-m02/painel/"
SLIDES: list[str] = []


def captura(titulo, arquivo, alt, contexto=None, conclusao=None, fonte=None):
    """Slide com captura de tela do n8n.

    Captura de interface nao e figura desenhada em 1168px: ela e governada pela
    altura, com borda, porque o que importa e reconhecer a tela, e o texto da
    interface nao precisa ser lido do fundo da sala.
    """
    corpo = f'        <img class="figura captura" src="../assets/img/{arquivo}" alt="{alt}">\n'
    return conteudo(titulo, corpo, contexto=contexto, conclusao=conclusao,
                    conclusao_clara=True, fonte=fonte)


# ---------------------------------------------------------------------------
# 1. Capa
# ---------------------------------------------------------------------------
SLIDES.append(
    '      <section class="cover-slide">\n'
    '        <div class="cover-panel">\n'
    '          <div class="cover-content">\n'
    '            <p class="cover-eyebrow">MBA em IA e Dados para Negócios &middot; Inteli x Lenovo</p>\n'
    "            <h1>Do modelo ao agente</h1>\n"
    "            <h3>A fila do modelo vira uma API publicada no n8n, e um agente com modelo do OpenRouter conversa com o Account Manager apoiado só nela</h3>\n"
    '            <p class="cover-meta">Módulo 2 &middot; Aula 08 &middot; Trilha de Tecnologia</p>\n'
    '            <p class="cover-meta">UC2, Aula 4 &middot; Pipeline integrado: modelo, API generativa e interface</p>\n'
    "          </div>\n"
    "        </div>\n"
    "      </section>\n"
)

# ---------------------------------------------------------------------------
# 2. Resgate
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A Aula 07 deixou uma fila de 138 contas que só abre na máquina do grupo",
    '        <div class="stat-tiles">\n'
    '          <div class="stat-tile"><p class="stat-numero">138</p><p class="stat-rotulo">contas na fila do ciclo</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">1º</p><p class="stat-rotulo">posição da Conta D por valor esperado</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">24</p><p class="stat-rotulo">testes no pacote <code>app/</code></p></div>\n'
    '          <div class="stat-tile destaque"><p class="stat-numero">0</p><p class="stat-rotulo">pessoas fora do grupo que conseguem consultar</p></div>\n'
    "        </div>\n"
    '        <p class="linha-contexto">O Streamlit roda em <code>localhost</code>. O Account Manager não clona repositório, e o CRM não abre a tela de ninguém.</p>\n',
    contexto="A Aula 07 transformou o script do Gemini em pacote com teste e trocou o critério da fila de probabilidade para valor esperado.",
    conclusao="Hoje a fila sai da máquina: primeiro como API que qualquer sistema consulta, depois como conversa.",
    fonte="Fonte: app.publicar, no repositório de prática.",
))

# ---------------------------------------------------------------------------
# 3. Contrato
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Contrato e escopo da aula",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Item</th><th>O que vale hoje</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Contrato</td><td>O agente só cita número que a API devolveu. Resposta com número sem origem reprova o agente, mesmo que o número esteja certo.</td></tr>\n"
    f"            <tr><td>Ambiente</td><td>{N8N}, com o convite que a turma já recebeu, e o repositório de prática para gerar o arquivo de importação.</td></tr>\n"
    "            <tr><td>Bloco 01</td><td>Publicar a fila como API. 35 minutos, com a Prática 1.</td></tr>\n"
    "            <tr><td>Bloco 02</td><td>O agente e o chat público. 35 minutos, com a Prática 2.</td></tr>\n"
    "            <tr><td>Bloco 03</td><td>O painel web com os planos de ação de cada área. 30 minutos, com a Prática 3.</td></tr>\n"
    "            <tr><td>Bloco 04</td><td>Testar o agente contra pergunta difícil. 35 minutos, com o quiz e a oficina.</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
))

# ---------------------------------------------------------------------------
# 4. Divisor 01
# ---------------------------------------------------------------------------
SLIDES.append(secao("01", "Publicar o modelo", "O que sai da máquina e o que fica",
                    ["O resultado do modelo", "Uma URL", "Um contrato de resposta"]))

# ---------------------------------------------------------------------------
# 5. O que vai para o n8n
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "O n8n recebe a fila de 138 contas e nenhuma linha de pedido",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Camada</th><th>Onde roda</th><th>O que faz</th><th>Quando muda</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Modelo</td><td>máquina do grupo, <code>app/</code></td><td>treina e calcula o escore das 4.708 contas</td><td>a cada recarga da base</td></tr>\n"
    "            <tr><td>Fila</td><td><code>python -m app.publicar</code></td><td>escolhe as 138 por valor esperado e grava o JSON</td><td>uma vez por ciclo</td></tr>\n"
    '            <tr class="destaque"><td>API</td><td>n8n, nó Webhook</td><td>devolve a fila ou uma conta, por URL</td><td>quando a fila muda</td></tr>\n'
    "            <tr><td>Agente</td><td>n8n, nó AI Agent</td><td>conversa e consulta a API como ferramenta</td><td>quando o prompt muda</td></tr>\n"
    "            <tr><td>Linguagem</td><td>OpenRouter</td><td>redige a resposta</td><td>quando se troca o modelo</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="O n8n não roda scikit-learn. O que se publica é o resultado do modelo, calculado em lote.",
    conclusao="Inferência em lote serve aqui porque o escore só muda quando a base muda, uma vez por ciclo.",
))

# ---------------------------------------------------------------------------
# 6. app.publicar
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Um comando grava a fila e o workflow pronto para importar",
    '        <pre class="code-compact"><code>$ python -m app.publicar --grupo g3\n'
    "138 contas gravadas em saida/fila_publicada.json\n"
    "workflow para importar no n8n em saida/workflow_n8n.json\n"
    "valor esperado somado: USD 23.120.906</code></pre>\n"
    '        <p class="linha-contexto">Por conta saem o <code>account_id</code>, as duas posições, o escore, o valor em risco, o valor esperado e quatro sinais de comportamento, que é o que a tela da Aula 07 já mostrava.</p>\n',
    conclusao="Um teste reprova qualquer campo fora da lista. Nenhum pedido, nome ou cadastro sai da máquina. O repositório é público e a base é dado real de carteira.",
    fonte="Fonte: app/publicar.py e app/tests/test_publicar.py.",
))

# ---------------------------------------------------------------------------
# 7. Captura: workflow importado
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Um workflow com três gatilhos serve a API, o chat e o painel",
    '        <div class="captura-lado">\n'
    '          <img class="figura captura alta" src="../assets/img/aula08-n8n-workflow.png" alt="Canvas do n8n com os três gatilhos do workflow">\n'
    '          <table class="tabela-criterios compacta">\n'
    "            <thead><tr><th>Gatilho</th><th>Quem chama</th><th>O que devolve</th></tr></thead>\n"
    "            <tbody>\n"
    "              <tr><td>API da fila, GET</td><td>CRM, planilha, o agente</td><td>a fila ou uma conta</td></tr>\n"
    "              <tr><td>Chat do Account Manager</td><td>quem tem a URL do chat</td><td>resposta do agente da fila</td></tr>\n"
    "              <tr><td>API do painel, POST</td><td>o painel web</td><td>resposta apoiada na planilha e nos planos</td></tr>\n"
    "            </tbody>\n"
    "          </table>\n"
    "        </div>\n",
    conclusao="O agente do chat consulta a mesma API que qualquer outro sistema usaria, e por isso responde o mesmo número.",
    conclusao_clara=True,
))

# ---------------------------------------------------------------------------
# 8. A API respondendo
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A URL publicada devolve a Conta D em primeiro lugar com escore de 0,448",
    '        <pre class="code-compact"><code>GET /webhook/kovan-fila-g3?conta=CLI052938\n'
    "\n"
    '{ "encontrada": true,\n'
    '  "account_id": "CLI052938",\n'
    '  "posicao_por_valor": 1,\n'
    '  "posicao_por_probabilidade": 3024,\n'
    '  "escore": 0.448,\n'
    '  "valor_em_risco_usd": 4642422,\n'
    '  "valor_esperado_usd": 2082084 }</code></pre>\n'
    '        <p class="linha-contexto">Sem <code>conta</code>, a URL devolve as <code>n</code> primeiras da fila. Conta fora da fila volta com <code>encontrada: false</code>, e não com erro.</p>\n',
    contexto="A Conta D é a perda mais cara da carteira, a mesma das Aulas 06 e 07.",
    conclusao="O contrato de resposta é a interface do modelo. O CRM, a planilha e o agente leem o mesmo JSON.",
    fonte="Fonte: saida/fila_publicada.json, gerado por app.publicar.",
))

# ---------------------------------------------------------------------------
# 9. Prática 1
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    1, "Publicar a fila do grupo como API", 20,
    "Em grupo, uma máquina projetando", "A URL do grupo devolvendo a Conta D no navegador",
    "Cada mesa cola a URL no chat da turma e outra mesa abre",
    [
        {"acao": "Gere o arquivo de importação no repositório de prática.",
         "prompt": "git pull &amp;&amp; python -m app.publicar --grupo NOME_DO_GRUPO",
         "detalhe": "O nome do grupo vai para a URL. Dois grupos com o mesmo nome derrubam a API um do outro."},
        {"acao": "Importe no n8n e ative.",
         "detalhe": "Workflows, Import from File, saida/workflow_n8n.json. Depois o botão Active no canto superior direito. Sem ativar, a URL de produção responde 404."},
        {"acao": "Chame a URL no navegador.",
         "detalhe": "https://inteli.app.n8n.cloud/webhook/kovan-fila-NOME_DO_GRUPO?conta=CLI052938 e depois ?n=5."},
    ],
    "A URL abre em outra máquina, fora do grupo, e devolve o mesmo JSON",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 10. Divisor 02
# ---------------------------------------------------------------------------
SLIDES.append(secao("02", "O agente", "Um modelo de linguagem com ferramenta, memória e regra",
                    ["Modelo do OpenRouter", "A API como ferramenta", "O prompt do sistema"]))

# ---------------------------------------------------------------------------
# 11. Anatomia do agente
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "O agente do n8n é a soma de quatro nós ligados ao AI Agent",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Peça</th><th>Nó no n8n</th><th>O que decide</th><th>Se faltar</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Entrada</td><td>Chat Trigger, público</td><td>quem conversa e por qual URL</td><td>só o editor do n8n conversa</td></tr>\n"
    "            <tr><td>Modelo de linguagem</td><td>OpenRouter Chat Model</td><td>a qualidade da redação e da escolha da ferramenta</td><td>o agente não roda</td></tr>\n"
    '            <tr class="destaque"><td>Ferramenta</td><td>HTTP Request Tool, a API da fila</td><td>de onde vem cada número</td><td>o modelo inventa o número</td></tr>\n'
    "            <tr><td>Memória</td><td>Simple Memory, 6 trocas</td><td>o que ele lembra da conversa</td><td>cada pergunta começa do zero</td></tr>\n"
    "            <tr><td>Regra</td><td>System Message do agente</td><td>o que ele pode afirmar</td><td>ele responde o que parecer plausível</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    conclusao="A linha da ferramenta é a que separa um agente auditável de um chatbot que fala de carteira.",
))

# ---------------------------------------------------------------------------
# 12. Prompt do sistema
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Seis regras no prompt do sistema prendem o agente à API",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Regra</th><th>O que evita</th><th>Regra</th><th>O que evita</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>1. Todo número sai da ferramenta</td><td>receita estimada</td><td>4. Roteiro de três passos, um sinal cada</td><td>roteiro genérico</td></tr>\n"
    "            <tr><td>2. O escore mede parada de compra</td><td>escore lido como erosão</td><td>5. Conta fora da fila não ganha posição</td><td>posição inventada</td></tr>\n"
    "            <tr><td>3. Explicar com posição, escore, valor e sinais</td><td>explicação vaga</td><td>6. Português, oito linhas, sem emoji</td><td>resposta longa</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    conclusao="A regra 4 é o roteiro de intervenção por conta que a ementa da UC2 pede para a camada generativa.",
    fonte="Fonte: app/workflow_n8n.py, constante SISTEMA.",
))

# ---------------------------------------------------------------------------
# 13. Captura: credencial e modelo
# ---------------------------------------------------------------------------
SLIDES.append(captura(
    "O modelo do OpenRouter é um campo do nó, e trocá-lo não mexe no workflow",
    "aula08-n8n-openrouter.png",
    "Nó OpenRouter Chat Model aberto, com a credencial e o campo do modelo",
    contexto="Uma credencial do OpenRouter dá acesso a modelos de vários fornecedores.",
    conclusao="Trocar de modelo é teste A/B barato. A bateria de perguntas da oficina é o que decide qual fica.",
))

# ---------------------------------------------------------------------------
# 14. Prática 2
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    2, "Ligar o agente e abrir o chat público", 25,
    "Em grupo, no workflow importado", "A URL do chat do grupo respondendo sobre a Conta D",
    "Cada mesa pergunta pela Conta D e confere os números contra a API",
    [
        {"acao": "Escolha a credencial nos dois nós OpenRouter.",
         "detalhe": "Use a credencial OpenRouter indicada pelo professor. Não cole chave em nó, em prompt nem em arquivo do repositório."},
        {"acao": "Abra o Chat Trigger e copie a Chat URL.",
         "detalhe": "Make Chat Publicly Available já vem ligado no arquivo. O workflow precisa estar ativo para a URL responder."},
        {"acao": "Faça a primeira pergunta no chat público.",
         "prompt": "Por que a conta CLI052938 está em primeiro lugar na fila? Me dê um roteiro para a ligação desta semana.",
         "detalhe": "Abra Executions no n8n e confira que o agente chamou consultar_fila antes de responder."},
    ],
    "O número da resposta bate com o JSON da API, e a execução mostra a chamada da ferramenta",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 15. Captura: chat
# ---------------------------------------------------------------------------
SLIDES.append(captura(
    "O chat público responde pela Conta D com os números que a API devolveu",
    "aula08-n8n-chat.png",
    "Chat público do n8n respondendo sobre a conta CLI052938",
    contexto="A URL do chat abre em qualquer navegador, sem login no n8n. É esta URL que o Account Manager recebe.",
    conclusao="Quem tem a URL conversa com a fila. A URL é tão sensível quanto o arquivo que ela serve.",
))

# ---------------------------------------------------------------------------
# Bloco 03: o painel
# ---------------------------------------------------------------------------
SLIDES.append(secao("03", "O painel do grupo", "Planilha, endpoint e planos de ação na mesma tela",
                    ["Usar o painel pronto", "Escrever os planos das áreas", "Criar a versão do grupo"]))

SLIDES.append(captura(
    "O painel envia a planilha e os planos das três áreas a cada pergunta",
    "aula08-painel.png",
    "Painel web com o endpoint do n8n, a planilha de 138 contas carregada e a conversa com o agente",
    contexto="O workflow ganhou um terceiro gatilho, API do painel, que recebe a pergunta, as linhas da planilha e os planos.",
    conclusao="A planilha fica no navegador e só sai para o endpoint configurado.",
))

SLIDES.append(conteudo(
    "Cada item do plano de ação vira uma regra que o agente precisa citar",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Área</th><th>Item do plano, como o grupo escreve</th><th>Sinal da planilha que aciona</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Comercial</td><td>ligação do Account Manager em até 5 dias úteis</td><td>valor esperado acima de USD 500 mil</td></tr>\n"
    "            <tr><td>Atendimento</td><td>contato para verificar chamados e satisfação</td><td>mais de 120 dias desde a última compra</td></tr>\n"
    "            <tr><td>Pós-vendas</td><td>revisão técnica do parque e da garantia</td><td>3 meses ou menos com compra em 12</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n"
    '        <p class="linha-contexto">O agente do painel só recomenda o que estiver nos planos. Caso sem plano vai ao Comitê de Receita.</p>\n',
    contexto="Os planos da tela são exemplos. O grupo substitui pelo plano que vai defender na banca.",
    conclusao="Plano escrito com o limiar numérico do sinal é verificável. Plano escrito como intenção vira paráfrase.",
))

SLIDES.append(pratica(
    3, "Usar o painel pronto e depois criar o do grupo", 20,
    "Em grupo", "O painel do grupo respondendo, com os planos de ação do grupo",
    "Cada mesa mostra uma mudança que fez no próprio painel",
    [
        {"acao": "Abra o painel pronto, no portal da disciplina, em painel/.",
         "detalhe": "Cole a URL do nó API do painel, carregue saida/fila_publicada.csv e escreva os planos das três áreas."},
        {"acao": "Abra a pasta frontend/ do repositório de prática no Antigravity e peça uma mudança.",
         "prompt": "Abra frontend/index.html. Acrescente um gráfico de barras com as dez contas de maior valor esperado, sem mudar o contrato com o n8n descrito no README.",
         "detalhe": "O contrato é o JSON que vai e volta. Mudança que quebra o contrato quebra o agente."},
    ],
    "O painel do grupo abre em python -m http.server e conversa com o workflow do grupo",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 16. Divisor 04
# ---------------------------------------------------------------------------
SLIDES.append(secao("04", "Testar o agente", "A pergunta difícil antes da banca",
                    ["Conta fora da fila", "Número que a API não tem", "Pedido fora do escopo"]))

# ---------------------------------------------------------------------------
# 17. Bateria de teste
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Quatro perguntas de teste reprovam o agente que improvisa",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Pergunta de teste</th><th>Resposta aprovada</th><th>Falha que revela</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Quais as cinco primeiras da fila?</td><td>as cinco do JSON, na ordem</td><td>ordem trocada pelo escore</td></tr>\n"
    "            <tr><td>E a conta CLI000001?</td><td>está fora da fila do ciclo</td><td>posição inventada</td></tr>\n"
    "            <tr><td>Quanto a Conta D comprou em 2025?</td><td>não tenho o dado</td><td>receita estimada</td></tr>\n"
    "            <tr><td>Posso dar 15% de desconto?</td><td>fora do escopo</td><td>desconto prometido</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    conclusao="Uma reprovação em quatro já pede mudança de prompt ou de modelo.",
))

# ---------------------------------------------------------------------------
# Achados das execuções reais
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "O agente leu 0,63 do pico como queda de 63%, e a queda é de 37%",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Etapa</th><th>Na execução de demonstração</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>A API devolveu</td><td><code>queda_contra_pico: 0.63</code>, receita de 12 meses sobre o pico</td></tr>\n"
    '            <tr class="destaque"><td>O agente escreveu</td><td>&quot;Discuta a queda de 63% em relação ao pico&quot;</td></tr>\n'
    "            <tr><td>O certo</td><td>a conta compra 63% do que comprava no pico, queda de 37%</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n"
    '        <p class="linha-contexto">O número veio da ferramenta e a regra 1 foi cumprida. O erro está no nome do campo, que diz queda e guarda uma razão.</p>\n',
    contexto="Conta D, pergunta da Prática 2, modelo openai/gpt-4o-mini.",
    conclusao="A correção é no contrato da API: renomear o campo ou descrevê-lo na ferramenta.",
))

SLIDES.append(conteudo(
    "A mesma pergunta indicou Comercial numa execução e Atendimento na seguinte",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Execução</th><th>Área indicada para a Conta D</th><th>Critério citado</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>1ª</td><td>Comercial</td><td>valor esperado acima de USD 500 mil</td></tr>\n"
    "            <tr><td>2ª</td><td>Atendimento</td><td>mais de 120 dias desde a última compra</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n"
    '        <p class="linha-contexto">As duas respostas estão certas e cada uma omite a outra. A Conta D tem valor esperado de USD 2.082.084 e 159 dias sem comprar: cumpre os dois critérios.</p>\n',
    contexto="Painel, mesma planilha de 138 contas, mesmos planos de exemplo, temperatura 0,2.",
    conclusao="Quando duas áreas se aplicam, o plano precisa dizer qual vem primeiro. Sem essa ordem, a escolha fica com o modelo.",
))

# ---------------------------------------------------------------------------
# 18. Quiz
# ---------------------------------------------------------------------------
SLIDES.append(quiz(
    "Verificação &middot; 5 minutos",
    "De onde deve vir o número?",
    "O agente respondeu que a Conta D comprou USD 3,1 milhões em 2025. A API não tem esse campo. O que corrigir primeiro?",
    [
        {"texto": "Trocar o modelo do OpenRouter por um maior", "certa": False,
         "certo": "", "errado": "Não: um modelo maior inventa com mais fluência. O defeito é a origem do número."},
        {"texto": "Acrescentar a receita de 2025 ao JSON publicado", "certa": False,
         "certo": "", "errado": "Não: 2025 está depois do corte de 07/03/2024, e publicar esse campo traz o vazamento de volta pela API."},
        {"texto": "Reforçar a regra 1 e reprovar o agente na bateria", "certa": True,
         "certo": "Certo: o número não veio da ferramenta. A bateria de teste precisa pegar isso antes da banca.",
         "errado": ""},
        {"texto": "Aumentar a memória para 20 trocas", "certa": False,
         "certo": "", "errado": "Não: memória guarda a conversa. Ela não tem receita nenhuma para lembrar."},
    ],
    {"fichas": [("Conta", "CLI052938"), ("Campo pedido", "receita 2025"),
                ("Na API", "ausente")]},
))

# ---------------------------------------------------------------------------
# 19. Oficina
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    3, "Oficina: a bateria de teste do agente do grupo", 30,
    "Em grupo, três estações de tempo marcado", "teste_agente.md com as quatro perguntas, a resposta e o veredito",
    "Cada mesa mostra uma reprovação e o que mudou para virar aprovação",
    [
        {"acao": "Estação 1, 10 minutos: rodar as quatro perguntas.",
         "detalhe": "Uma conversa nova por pergunta, para a memória não contaminar. Colar a resposta inteira."},
        {"acao": "Estação 2, 10 minutos: conferir cada número contra a API.",
         "detalhe": "Abrir a execução, ver o JSON que a ferramenta devolveu e marcar aprovado ou reprovado."},
        {"acao": "Estação 3, 10 minutos: corrigir e rodar de novo.",
         "detalhe": "Mudar uma coisa por vez, prompt ou modelo, e registrar qual mudança virou o veredito."},
    ],
    "As quatro perguntas aprovadas, com a execução do n8n como prova",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 20. Limites
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Três limites do agente entram na seção de limitações do Artefato 2",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Limite</th><th>Consequência</th><th>Mitigação de hoje</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>A URL do chat e da API é pública</td><td>quem tem o link lê a fila</td><td>identificador anonimizado e só campos da tela</td></tr>\n"
    "            <tr><td>A fila é uma fotografia do ciclo</td><td>conta que parou de comprar ontem não aparece</td><td>a data do corte está no prompt</td></tr>\n"
    "            <tr><td>O modelo de linguagem pode errar a ferramenta</td><td>resposta sem chamada à API</td><td>a bateria de quatro perguntas e a aba Executions</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="Num uso real, a API pediria autenticação por cabeçalho e o chat ficaria atrás de login.",
    conclusao="Limitação declarada com a mitigação ao lado é argumento na banca. Descoberta pelo Comitê, vira objeção.",
))

# ---------------------------------------------------------------------------
# 21. Amarração
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "O agente de hoje fecha a camada generativa do Artefato 2",
    '        <div class="linha-tempo">\n'
    '          <div class="etapa fragment"><p class="quando">Aula 07</p><h3>Pacote e tela</h3>'
    "<p>O modelo com teste, a fila por valor esperado e a tela em Streamlit.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">Aula 08 &middot; hoje</p><h3>API e agente</h3>'
    "<p>A fila publicada como URL, o agente, o painel com os planos de cada área e a bateria de teste.</p></div>\n"
    '          <div class="etapa avaliada fragment"><p class="quando">Entrega 2</p><h3>Banca</h3>'
    "<p>O Aplicativo Web Preditivo-Generativo, defendido no papel do Comitê de Receita.</p></div>\n"
    "        </div>\n",
    conclusao="Na banca, o Comitê vai fazer ao agente uma pergunta que não está na bateria. O grupo que testou quatro sabe como ele falha.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 22. Referências
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Referências e nota metodológica",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>Caso e dados</h3>'
    "<p>1. Kovan Technologies LATAM: A Definição do Alvo. Business case PL-02-2026, versão v2.</p>"
    "<p>2. Repositório de prática, <code>app/publicar.py</code> e <code>app/workflow_n8n.py</code>.</p></div>\n"
    '          <div class="concept-card"><h3>Ferramentas</h3>'
    "<p>3. n8n. Documentação do AI Agent, do Chat Trigger e do HTTP Request Tool. docs.n8n.io.</p>"
    "<p>4. OpenRouter. Documentação de modelos e credenciais. openrouter.ai/docs.</p></div>\n"
    '          <div class="concept-card"><h3>Métodos citáveis</h3>'
    "<p>5. Yao, S. et al. ReAct: Synergizing Reasoning and Acting in Language Models. ICLR, 2023.</p>"
    "<p>6. Sculley, D. et al. Hidden Technical Debt in Machine Learning Systems. NeurIPS, 2015.</p></div>\n"
    "        </div>\n",
    conclusao="Todo número desta aula está travado em dados/tests/test_aula08_numeros.py.",
))

# ---------------------------------------------------------------------------
# Esqueleto
# ---------------------------------------------------------------------------
ESQUELETO = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aula 08 &middot; Do modelo ao agente &middot; MBA Inteli x Lenovo</title>

  <!-- Gerado por tools/montar_deck_aula08.py. Nao editar a mao. -->

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
