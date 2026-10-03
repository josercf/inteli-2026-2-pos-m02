# -*- coding: utf-8 -*-
"""Monta aulas/aula08.html.

Gerado, nunca editado a mao: a numeracao de rodape e o fechamento de secao sao
garantidos aqui.

A aula e invertida. O deck abre com os tres experimentos do laboratorio e
depois serve de roteiro da trilha de dez passos, que o guia
(materiais/aula08-guia.html) detalha clique a clique.

Diretiva editorial: sem paralelismo negativo, sem antitese simetrica, sem
escalada com dois-pontos. Titulo de slide de conteudo e a conclusao completa,
com o numero dentro. Travado por tools/check_retorica.py.

Todo numero do case sai de dados/analise_aula08.py e esta travado em
dados/tests/test_aula08_numeros.py. Tempos e respostas de modelo de linguagem
vem das execucoes de demonstracao de 03/10/2026, e a fonte diz isso.

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

SITE = "josercf.github.io/inteli-2026-2-pos-m02"
DEMO = "Fonte: execução de demonstração no n8n do Inteli, 03/10/2026."
SLIDES: list[str] = []


def captura(titulo, arquivo, alt, contexto=None, conclusao=None, fonte=None):
    """Captura de tela, governada pela altura e com borda (ver .figura.captura)."""
    corpo = f'        <img class="figura captura" src="../assets/img/{arquivo}" alt="{alt}">\n'
    return conteudo(titulo, corpo, contexto=contexto, conclusao=conclusao,
                    conclusao_clara=True, fonte=fonte)


def captura_lado(titulo, arquivo, alt, tabela_html, contexto=None, conclusao=None, fonte=None):
    """Captura estreita ao lado de uma tabela."""
    corpo = (
        '        <div class="captura-lado">\n'
        f'          <img class="figura captura alta" src="../assets/img/{arquivo}" alt="{alt}">\n'
        f"{tabela_html}"
        "        </div>\n"
    )
    return conteudo(titulo, corpo, contexto=contexto, conclusao=conclusao,
                    conclusao_clara=True, fonte=fonte)


def tabela(cabecalho, linhas, classe="tabela-criterios compacta", destaque=None):
    th = "".join(f"<th>{c}</th>" for c in cabecalho)
    corpo = ""
    for i, linha in enumerate(linhas):
        attr = ' class="destaque"' if destaque == i else ""
        corpo += f"            <tr{attr}>" + "".join(f"<td>{c}</td>" for c in linha) + "</tr>\n"
    return (f'        <table class="{classe}">\n'
            f"          <thead><tr>{th}</tr></thead>\n"
            "          <tbody>\n" + corpo + "          </tbody>\n"
            "        </table>\n")


# ---------------------------------------------------------------------------
# Capa
# ---------------------------------------------------------------------------
SLIDES.append(
    '      <section class="cover-slide">\n'
    '        <div class="cover-panel">\n'
    '          <div class="cover-content">\n'
    '            <p class="cover-eyebrow">MBA em IA e Dados para Negócios &middot; Inteli x Lenovo</p>\n'
    "            <h1>Do modelo à equipe de agentes</h1>\n"
    "            <h3>A planilha original vira fila no navegador, três agentes no n8n respondem sobre ela e cada grupo publica o próprio painel no GitHub Pages</h3>\n"
    '            <p class="cover-meta">Módulo 2 &middot; Aula 08 &middot; Trilha de Tecnologia</p>\n'
    '            <p class="cover-meta">UC2, Aula 4 &middot; Pipeline integrado: modelo, API generativa e interface</p>\n'
    "          </div>\n"
    "        </div>\n"
    "      </section>\n"
)

# ---------------------------------------------------------------------------
# Resgate
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A Aula 07 deixou a fila por valor esperado, e hoje ela sai da máquina do grupo",
    '        <div class="stat-tiles">\n'
    '          <div class="stat-tile"><p class="stat-numero">4.593</p><p class="stat-rotulo">contas elegíveis, com compra até 2024-02</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">0,814</p><p class="stat-rotulo">AUC fora da amostra, calculada no navegador</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">138</p><p class="stat-rotulo">contas na fila do ciclo</p></div>\n'
    '          <div class="stat-tile destaque"><p class="stat-numero">3</p><p class="stat-rotulo">agentes que respondem sobre a fila</p></div>\n'
    "        </div>\n"
    '        <p class="linha-contexto">Nada para instalar: o painel lê <code>datasets_case_modulo2.xlsx</code> como chegou e treina o modelo dentro do navegador.</p>\n',
    contexto="A Aula 07 mostrou que ordenar por valor esperado alcança a receita em risco que a ordem por probabilidade deixava de fora.",
    conclusao="Hoje cada grupo sai com um painel publicado na internet e uma equipe de agentes que responde sobre a fila.",
    fonte="Fonte: dados/analise_aula08.py, sobre a base longa do case.",
))

# ---------------------------------------------------------------------------
# Contrato
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Contrato e formato da aula invertida",
    tabela(["Momento", "Duração", "O que acontece"], [
        ["Abertura", "20 min", "os três experimentos do laboratório, projetados pelo professor"],
        ["Trilha", "100 min", "os dez passos do guia, em grupo; o professor circula pelas mesas"],
        ["Checkpoint", "20 min", "cada grupo abre o painel publicado e roda a bateria ao vivo"],
        ["Contrato", "toda a aula", "nenhum número sem origem na fila, e nenhuma chave ou planilha fora do lugar"],
    ]),
    contexto=f"O guia completo está em <code>{SITE}/materiais/aula08-guia.html</code>, com cada clique e cada prompt.",
))

# ---------------------------------------------------------------------------
# 01 Abertura
# ---------------------------------------------------------------------------
SLIDES.append(secao("01", "A abertura", "Três experimentos que rodam no navegador",
                    ["O painel e a equipe", "Jev contra gratuito", "A bateria de teste"]))

SLIDES.append(captura(
    "O laboratório reúne os três experimentos que abrem a aula",
    "aula08-laboratorio.png",
    "Página do laboratório com os três experimentos numerados",
    contexto=f"<code>{SITE}/laboratorio/</code>. Cada experimento usa a fila que o anterior calculou.",
    conclusao="Os três rodam sobre a planilha original, e a planilha não sai do navegador.",
))

SLIDES.append(captura(
    "O painel treina o modelo no navegador e chega a AUC de 0,814",
    "aula08-painel.png",
    "Painel com a planilha carregada, os indicadores e a conversa com a equipe",
    contexto="35 das 138 contas da fila são perdidas no case. Valor esperado da fila: USD 26,6 milhões.",
    conclusao="Mesmo cálculo em Python e em JavaScript: um teste compara os dois conta a conta.",
    fonte="Fonte: dados/analise_aula08.py e painel/modelo.js.",
))

SLIDES.append(conteudo(
    "O histórico para em 2024-02, antes do corte de 07/03/2024",
    tabela(["Coluna", "O que mede, até 2024-02"], [
        ["<code>meses_desde_ultima_compra</code>", "recência"],
        ["<code>meses_com_compra_12m</code>", "frequência no último ano"],
        ["<code>log_receita_12m</code>", "valor no último ano, em escala logarítmica"],
        ["<code>razao_receita_12m</code>", "último ano dividido pelo anterior"],
        ["<code>receita_12m_sobre_pico</code>", "último ano como fração do melhor ano"],
        ["<code>meses_de_casa</code>", "tempo desde a primeira compra"],
    ]),
    conclusao="Compra depois de 7 de março só existe em conta não perdida. Usá-la vazaria o rótulo para dentro das colunas.",
))

SLIDES.append(captura(
    "Três agentes dividem cada pergunta em análise, ação e revisão",
    "aula08-n8n-equipe.png",
    "Canvas do n8n com o webhook e os três agentes em sequência",
    contexto="Atlas responde com os números da fila, Vera recomenda pelo plano de cada área e Ciro confere tudo e dá o veredito.",
    conclusao="Cada agente é um nó AI Agent com o próprio modelo. O painel escolhe qual modelo os três usam.",
))

SLIDES.append(conteudo(
    "O Jev respondeu em 12 s com os números que o gratuito omitiu",
    tabela(["Primeira conta da fila", "Nemotron 3 Super, gratuito", "Jev Router, TypeSafe"], [
        ["Tempo, três agentes", "16 s", "12 s"],
        ["Modelo que respondeu", "o próprio Nemotron", "<code>deepseek/deepseek-v4.1-flash</code>"],
        ["Atlas trouxe os números", "não", "sim"],
        ["Veredito do Ciro", "&quot;corrigido&quot;, com motivo que aprova", "&quot;aprovado&quot;, com motivo coerente"],
    ], destaque=1),
    conclusao="O Jev Router, da TypeSafe, escolhe qual modelo responde e cobra por uso.",
    fonte=DEMO,
))

# ---------------------------------------------------------------------------
# 02 A trilha
# ---------------------------------------------------------------------------
SLIDES.append(secao("02", "A trilha do grupo", "Dez passos, do arquivo ao painel publicado",
                    ["Modelo e agentes", "Teste", "Interface e publicação"]))

SLIDES.append(conteudo(
    "Os dez passos da trilha",
    tabela(["Passo", "O que fazer", "Quem", "Prova"], [
        ["1", "rodar o painel pronto com a planilha", "cada pessoa", "AUC de 0,814 na tela"],
        ["2 e 3", "criar a chave gratuita e guardar no n8n", "cada pessoa", "credencial na lista"],
        ["4", "importar a equipe de agentes", "uma pessoa", "workflow publicado"],
        ["5", "conectar o painel e escrever os planos", "o grupo", "resposta com selo do Ciro"],
        ["6 e 7", "rodar a bateria e comparar com o Jev", "o grupo", "placar e <code>teste_agente.md</code>"],
        ["8 e 9", "clonar e modificar a interface no Antigravity", "o grupo", "mudança no <code>localhost</code>"],
        ["10", "publicar no GitHub Pages", "uma pessoa", "URL aberta em outra máquina"],
    ]),
    conclusao="Cada passo do guia termina num quadro que diz como saber que deu certo. Só avance quando ele confere.",
))

SLIDES.append(pratica(
    1, "Passos 1 a 3: painel, chave e credencial", 20,
    "Cada pessoa", "A credencial OpenRouter salva no n8n",
    "Cada pessoa vê a AUC de 0,814 no painel e a credencial na lista do n8n",
    [
        {"acao": "Abra o painel no laboratório e arraste <code>datasets_case_modulo2.xlsx</code>.",
         "detalhe": "A base longa, de cerca de 68 MB. A versão de 24 MB começa depois do corte e o painel avisa."},
        {"acao": "Em openrouter.ai/settings/keys, crie a chave <code>kovan-NOME_DO_GRUPO</code>.",
         "detalhe": "Entrar com Google ou GitHub, sem cartão. A chave aparece uma vez só."},
        {"acao": "No n8n, Credentials, Create credential, OpenRouter: cole em API Key e salve.",
         "detalhe": "A chave não passa por chat, e-mail nem arquivo."},
    ],
    "A chave existe só no OpenRouter e na credencial do n8n",
    ambiente="navegador",
))

SLIDES.append(captura(
    "A chave gratuita libera 50 requisições por dia, e cada pergunta à equipe usa 3",
    "aula08-n8n-credencial.png",
    "Diálogo de nova credencial OpenRouter no n8n",
    contexto="Modelo terminado em <code>:free</code> não cobra. Limite por conta: 20 por minuto e 50 por dia.",
    conclusao="O workflow guarda só o nome da credencial, então o arquivo pode circular sem expor a chave.",
    fonte="Fonte: openrouter.ai/docs, página de limites, consultada em 03/10/2026.",
))

SLIDES.append(pratica(
    2, "Passo 4: importar a equipe de agentes", 10,
    "Uma pessoa por grupo", "A Production URL do nó API do painel",
    "Nenhum nó com alerta vermelho e o workflow publicado",
    [
        {"acao": "No painel, bloco 03, baixe o workflow. No n8n, Create workflow, menu <code>...</code>, Import from File.",
         "detalhe": "O arquivo traz os três agentes e não traz dado nenhum."},
        {"acao": "No nó API do painel, troque <code>NOME_DO_GRUPO</code> no Path.",
         "detalhe": "Nome igual ao de outro grupo derruba a equipe dos dois."},
        {"acao": "Escolha a credencial em Modelo do Atlas, da Vera e do Ciro. Salve e clique em Publish.",
         "detalhe": "Depois copie a Production URL do nó API do painel. A Test URL responde 404 ao painel."},
    ],
    "A URL termina em /webhook/kovan-chat-NOME_DO_GRUPO",
    ambiente="n8n",
))

SLIDES.append(captura_lado(
    "O prompt de sistema de cada agente traz o papel, as regras e a fila",
    "aula08-n8n-atlas.png",
    "Nó Atlas aberto no n8n, com a pergunta e o System Message",
    tabela(["Regra no prompt", "Agente"], [
        ["todo número sai da fila", "os três"],
        ["não recomendar ação", "Atlas"],
        ["só itens dos planos, com área e coluna", "Vera"],
        ["citar todas as áreas que se aplicam", "Vera"],
        ["conferir número a número e dar veredito", "Ciro"],
    ]),
    conclusao="Antes de mudar um prompt, leia os três. A regra de um pressupõe o trabalho do outro.",
))

SLIDES.append(conteudo(
    "Cada item do plano de ação precisa do limiar numérico da coluna que o aciona",
    tabela(["Área", "Item escrito com limiar", "Coluna da fila"], [
        ["Comercial", "valor esperado acima de USD 500 mil: ligação em até 5 dias úteis", "<code>valor_esperado_usd</code>"],
        ["Atendimento", "4 meses ou mais sem compra: contato para verificar chamados", "<code>meses_desde_ultima_compra</code>"],
        ["Pós-vendas", "3 meses ou menos com compra em 12: revisão técnica do parque", "<code>meses_com_compra_nos_ultimos_12</code>"],
    ]),
    contexto="A Vera só recomenda o que está escrito no plano. O plano fica no painel e segue com cada pergunta.",
    conclusao="Plano escrito como intenção vira paráfrase. Plano com limiar vira regra que o Ciro consegue conferir.",
))

SLIDES.append(pratica(
    3, "Passo 5: conectar o painel e escrever os planos", 15,
    "O grupo inteiro", "Uma resposta da equipe com o selo do Ciro",
    "Cada ação cita área, item e coluna, com o valor",
    [
        {"acao": "No bloco 03 do painel, cole a Production URL e clique em Testar conexão.",
         "detalhe": "A equipe leva alguns segundos: são três chamadas ao modelo."},
        {"acao": "No bloco 02, escreva o plano das três áreas, com limiar em cada item.",
         "detalhe": "Os textos da tela são exemplos. O plano do grupo é o que vai para a banca."},
        {"acao": "No bloco 04, clique numa conta da fila e pergunte qual área deve agir.",
         "detalhe": "Leia as três mensagens antes da final. O erro costuma aparecer no Atlas."},
    ],
    "Os três agentes respondem e o Ciro aprova ou corrige com motivo",
    ambiente="painel",
))

SLIDES.append(captura(
    "A bateria fechou em 4 de 4 com o modelo gratuito na demonstração",
    "aula08-bateria.png",
    "Bateria de teste com quatro perguntas aprovadas",
    contexto="Cinco primeiras da fila em ordem, conta fora da fila, compra de 2025 e desconto de 15%.",
    conclusao="A conferência automática aponta onde olhar. O veredito do grupo continua sendo a leitura humana.",
    fonte=DEMO,
))

SLIDES.append(pratica(
    4, "Passos 6 e 7: bateria e comparação com o Jev", 20,
    "O grupo inteiro", "<code>teste_agente.md</code> com o placar e uma mudança",
    "Cada mesa mostra uma reprovação e o que mudou para virar aprovação",
    [
        {"acao": "No laboratório, experimento 03, clique em Rodar as quatro perguntas.",
         "detalhe": "A bateria gasta 12 das 50 requisições do dia no plano gratuito."},
        {"acao": "Para cada reprovação, mude uma coisa só, prompt ou modelo, e rode de novo.",
         "detalhe": "Duas mudanças de uma vez impedem saber qual resolveu."},
        {"acao": "No experimento 02, rode a mesma conta no gratuito e no Jev.",
         "detalhe": "Sem crédito, o Jev devolve erro. Acompanhe então a demonstração do professor."},
    ],
    "Placar registrado e a mudança que virou o veredito",
    ambiente="laboratório",
))

# ---------------------------------------------------------------------------
# 03 A interface do grupo
# ---------------------------------------------------------------------------
SLIDES.append(secao("03", "A interface do grupo", "Antigravity para modificar, GitHub Pages para publicar",
                    ["Clonar e rodar", "Modificar com prompt", "Publicar"]))

SLIDES.append(pratica(
    5, "Passo 8: clonar e rodar no Antigravity", 5,
    "Uma pessoa por grupo", "O painel abrindo em localhost:8000",
    "O painel local aceita a planilha e chega à AUC de 0,814",
    [
        {"acao": "Abra o Antigravity numa pasta vazia e cole o primeiro prompt.",
         "prompt": "Clone o repositório https://github.com/josercf/inteli-pos-2026-2a-eda nesta pasta. Se ele já estiver clonado, rode git pull. Depois abra a pasta frontend, liste os arquivos e explique em uma linha o papel de cada um. Não altere nada ainda."},
        {"acao": "Cole o segundo prompt e abra o endereço que ele devolver.",
         "prompt": "Dentro da pasta frontend, suba um servidor local com python3 -m http.server 8000 e me diga o endereço para abrir no navegador. Deixe o servidor rodando."},
    ],
    "O mesmo painel, agora na pasta do grupo",
    ambiente="Antigravity",
))

SLIDES.append(pratica(
    6, "Passo 9: modificar a interface com prompts", 30,
    "O grupo inteiro", "Pelo menos uma mudança funcionando no localhost",
    "Cada mesa projeta a mudança e mostra o diff",
    [
        {"acao": "Identidade do grupo.",
         "prompt": "Em frontend/index.html, troque o título do cabeçalho para \"Painel de retenção Kovan, grupo NOME_DO_GRUPO\" e coloque o nome dos integrantes no rodapé. Não mexa em modelo.js nem no JSON enviado ao n8n. Mostre o diff antes de salvar."},
        {"acao": "Gráfico das dez contas de maior valor esperado.",
         "prompt": "Acrescente abaixo dos indicadores um gráfico de barras horizontais, em SVG sem biblioteca, com as dez contas de maior valor esperado de resultado.fila. Use só as variáveis de cor de inteli-brand.css."},
        {"acao": "Os prompts de filtro por segmento, exportação em CSV e revisão de segurança estão no guia, passo 9.",
         "detalhe": "Uma mudança por vez, conferida no navegador antes da próxima."},
    ],
    "modelo.js e o JSON enviado ao n8n continuam iguais",
    ambiente="Antigravity",
))

SLIDES.append(conteudo(
    "O GitHub Pages publica a pasta frontend em seis cliques, sem terminal",
    tabela(["Clique", "Onde", "O que fazer"], [
        ["1", "github.com/new", "nome <code>kovan-painel-NOME_DO_GRUPO</code>, Public, Create repository"],
        ["2", "repositório vazio", "link <em>uploading an existing file</em>"],
        ["3", "área de upload", "arrastar os quatro arquivos de <code>frontend</code>, na raiz"],
        ["4", "Commit changes", "mensagem <code>painel do grupo</code>, botão verde"],
        ["5", "Settings, Pages", "<em>Deploy from a branch</em>, <code>main</code>, <code>/ (root)</code>, Save"],
        ["6", "após 1 a 2 minutos", "<em>Your site is live at</em> com a URL do grupo"],
    ], destaque=4),
    conclusao="A planilha, a chave e o endpoint nunca entram no repositório. Ele é público.",
))

SLIDES.append(pratica(
    7, "Passo 10: publicar pelo Antigravity", 15,
    "Uma pessoa por grupo", "A URL do GitHub Pages do grupo",
    "A URL abre em outra máquina, aceita a planilha e conversa com a equipe",
    [
        {"acao": "Alternativa ao caminho pelo navegador. Cole o prompt e confirme cada comando.",
         "prompt": "Publique a pasta frontend no GitHub Pages. Me mostre cada comando antes de rodar. 1) Confira gh auth status. 2) Copie index.html, modelo.js, inteli-brand.css e workflow_n8n.json para uma pasta nova kovan-painel-NOME_DO_GRUPO, fora do repositório clonado. 3) Confira que não há .xlsx, .csv nem chave de API nela. 4) Crie o repositório público com gh repo create --public --source . --push. 5) Ative o Pages pela branch main, pasta raiz, com gh api. 6) Me dê a URL."},
    ],
    "O painel do grupo na internet, com a mudança do passo 9",
    ambiente="Antigravity",
))

# ---------------------------------------------------------------------------
# 04 O contrato entre modelo e agente
# ---------------------------------------------------------------------------
SLIDES.append(secao("04", "O contrato entre modelo e agente", "O nome da coluna também é prompt",
                    ["A leitura errada", "O quiz", "O checkpoint"]))

SLIDES.append(conteudo(
    "Dois modelos leram 0,63 do pico como queda de 63%, e a queda era de 37%",
    tabela(["Etapa", "O que aconteceu"], [
        ["A fila mandava", "<code>queda_contra_pico: 0.63</code>, receita do último ano sobre a do melhor ano"],
        ["gpt-4o-mini e qwen3.8-27b:free escreveram", "&quot;queda de 63% em relação ao pico&quot;"],
        ["O certo", "a conta compra 63% do melhor ano, uma queda de 37%"],
        ["A correção", "a coluna virou <code>receita_12m_como_fracao_do_pico_anual</code> e o prompt explica a leitura"],
    ], destaque=3),
    contexto="O número veio da fila e a regra de origem foi cumprida. O erro estava no nome do campo.",
    conclusao="Com o nome novo e a leitura no prompt, o Ciro com o Jev escreveu &quot;queda de 37%&quot;.",
    fonte=DEMO,
))

SLIDES.append(quiz(
    "Verificação &middot; 5 minutos",
    "De onde deve vir o número?",
    "O Atlas respondeu que a primeira conta comprou USD 3,1 milhões em 2025. A fila não tem esse campo. O que corrigir primeiro?",
    [
        {"texto": "Trocar o modelo gratuito pelo Jev", "certa": False,
         "certo": "", "errado": "Não: um modelo melhor inventa com mais fluência. O defeito é a origem do número."},
        {"texto": "Acrescentar a receita de 2025 à fila enviada", "certa": False,
         "certo": "", "errado": "Não: 2025 está depois do corte, e o campo traria o vazamento de volta pela fila."},
        {"texto": "Reprovar na bateria e reforçar a regra de origem no prompt", "certa": True,
         "certo": "Certo: o número não veio da fila. A bateria precisa pegar isso antes da banca.",
         "errado": ""},
        {"texto": "Aumentar a memória do Atlas para 20 trocas", "certa": False,
         "certo": "", "errado": "Não: memória guarda a conversa, e ela não tem receita de 2025 para lembrar."},
    ],
    {"fichas": [("Conta", "primeira da fila"), ("Campo pedido", "receita 2025"),
                ("Na fila", "ausente")]},
))

SLIDES.append(conteudo(
    "Checkpoint da aula",
    tabela(["Item", "Prova projetada"], [
        ["Painel publicado", "a URL do GitHub Pages aberta no projetor"],
        ["Equipe no n8n do grupo", "uma pergunta respondida pelos três agentes, com o selo do Ciro"],
        ["Planos de ação", "três planos com limiar numérico em cada item"],
        ["Bateria", "o placar e uma reprovação corrigida em <code>teste_agente.md</code>"],
        ["Interface própria", "pelo menos uma mudança do passo 9"],
    ]),
    conclusao="O grupo que trouxer a bateria aprovada sabe como a equipe falha antes de o Comitê perguntar.",
))

SLIDES.append(conteudo(
    "O painel publicado e a equipe de agentes fecham a camada generativa do Artefato 2",
    '        <div class="linha-tempo">\n'
    '          <div class="etapa fragment"><p class="quando">Aula 07</p><h3>Pacote e fila</h3>'
    "<p>O modelo com teste e a fila ordenada por valor esperado.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">Aula 08 &middot; hoje</p><h3>Equipe e painel</h3>'
    "<p>O modelo no navegador, três agentes no n8n e o painel do grupo no GitHub Pages.</p></div>\n"
    '          <div class="etapa avaliada fragment"><p class="quando">Entrega 2</p><h3>Banca</h3>'
    "<p>O Aplicativo Web Preditivo-Generativo, defendido no papel do Comitê de Receita.</p></div>\n"
    "        </div>\n",
    conclusao="Na banca, o Comitê vai fazer à equipe uma pergunta fora da bateria. O grupo que testou sabe como ela falha.",
    por_passos=True,
))

SLIDES.append(conteudo(
    "Referências e nota metodológica",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>Caso e material</h3>'
    "<p>1. Kovan Technologies LATAM: A Definição do Alvo. Business case PL-02-2026, versão v2.</p>"
    f"<p>2. Guia e laboratório da aula, em {SITE}.</p></div>\n"
    '          <div class="concept-card"><h3>Ferramentas</h3>'
    "<p>3. n8n. AI Agent, Webhook e Respond to Webhook. docs.n8n.io.</p>"
    "<p>4. OpenRouter. Modelos, chaves e limites. openrouter.ai/docs.</p>"
    "<p>5. TypeSafe. Jev Router, <code>typesafe/jev-router</code> no OpenRouter.</p></div>\n"
    '          <div class="concept-card"><h3>Métodos citáveis</h3>'
    "<p>6. Yao, S. et al. ReAct: Synergizing Reasoning and Acting in Language Models. ICLR, 2023.</p>"
    "<p>7. Wu, Q. et al. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. 2023.</p></div>\n"
    "        </div>\n",
    conclusao="Todo número do case desta aula está travado em dados/tests/test_aula08_numeros.py.",
))

# ---------------------------------------------------------------------------
# Esqueleto
# ---------------------------------------------------------------------------
ESQUELETO = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aula 08 &middot; Do modelo à equipe de agentes &middot; MBA Inteli x Lenovo</title>

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
