# -*- coding: utf-8 -*-
"""Monta aulas/aula03.html.

Gerado, nunca editado a mao: a numeracao de rodape e o fechamento de secao sao
garantidos aqui, e ja se perderam no HTML duas vezes.

Diretiva editorial de 15/08/2026: sem paralelismo negativo, sem antitese
simetrica, sem escalada com dois-pontos. Titulo de slide de conteudo e a
conclusao completa, com o numero dentro. Travado por tools/check_retorica.py.

Todo numero do case que aparece aqui esta travado em
dados/tests/test_dataset_oficial.py, que le o dataset oficial da Lenovo.

Uso: python3 tools/montar_deck_aula03.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from tools import deck_kit  # noqa: E402
from tools.deck_kit import conteudo, figura, pratica, quiz, secao  # noqa: E402

SAIDA = RAIZ / "aulas" / "aula03.html"

deck_kit.configurar("Módulo 2 &middot; Aula 03")
deck_kit.reiniciar_paginacao()

AMBIENTE = "Antigravity"

SLIDES: list[str] = []

# ---------------------------------------------------------------------------
# 1. Capa
# ---------------------------------------------------------------------------
SLIDES.append(
    '      <section class="cover-slide">\n'
    '        <div class="cover-panel">\n'
    '          <div class="cover-content">\n'
    '            <p class="cover-eyebrow">MBA em IA e Dados para Negócios &middot; Inteli x Lenovo</p>\n'
    "            <h1>O corte que define o rótulo</h1>\n"
    "            <h3>Análise univariada e bivariada sobre a base oficial, e a regra que ninguém declarou</h3>\n"
    '            <p class="cover-meta">Módulo 2 &middot; Aula 03 &middot; Trilha de Tecnologia</p>\n'
    '            <p class="cover-meta">22 de agosto de 2026 &middot; 13h00 às 16h00</p>\n'
    "          </div>\n"
    "        </div>\n"
    "      </section>\n"
)

# ---------------------------------------------------------------------------
# 2. Resgate: a base mudou
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A base oficial da Lenovo substitui o painel sintético e traz 8.282 contas em 24 meses",
    '        <div class="stat-tiles">\n'
    '          <div class="stat-tile"><p class="stat-numero">8.282</p>'
    '<p class="stat-rotulo">contas na carteira LATAM</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">24</p>'
    '<p class="stat-rotulo">meses, de 2024-04 a 2026-03</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">5</p>'
    '<p class="stat-rotulo">abas, com grãos diferentes entre si</p></div>\n'
    '          <div class="stat-tile destaque"><p class="stat-numero">1.593</p>'
    '<p class="stat-rotulo">contas que a base já marca como perdidas</p></div>\n'
    "        </div>\n"
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>O que a Aula 02 deixou</h3>'
    "<p>A discussão dos dados, sem o registro do tratamento em arquivo.</p></div>\n"
    '          <div class="concept-card"><h3>O que mudou na pergunta</h3>'
    "<p>O rótulo não precisa mais ser construído. Ele veio pronto.</p></div>\n"
    '          <div class="concept-card"><h3>O que a tarde apura</h3>'
    "<p>Qual critério ele usa e o que deixa de fora.</p></div>\n"
    "        </div>\n",
    contexto="O painel das Aulas 01 e 02 tinha 1.187 contas e nenhuma coluna de rótulo.",
    conclusao="O registro de tratamento que ficou pendente fecha hoje, na oficina, sobre a base oficial.",
    fonte="Fonte: datasets_case_modulo2.xlsx.",
))

# ---------------------------------------------------------------------------
# 3. Contrato do dia
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A oficina de hoje fecha quatro das sete seções do Artefato 1",
    '        <div class="concept-cards quatro">\n'
    '          <div class="concept-card"><h3>Contrato do dia</h3>'
    "<p>Toda seção do artefato entra com o número e a figura que a sustentam, "
    "produzidos por código que roda na pasta do grupo.</p></div>\n"
    '          <div class="concept-card"><h3>Ambiente</h3>'
    "<p>Antigravity a tarde inteira, sobre a pasta clonada do repositório da turma. "
    "O dataset chega por fora e fica só na máquina de vocês.</p></div>\n"
    '          <div class="concept-card"><h3>Fecha hoje</h3>'
    "<p>Carga, qualidade, univariada e bivariada.</p></div>\n"
    '          <div class="concept-card"><h3>Vai para a semana</h3>'
    "<p>Rótulo, visuais e limitações.</p></div>\n"
    "        </div>\n",
    contexto="Método das 13h00 às 14h20, intervalo às 14h20, oficina das 14h40 às 15h45.",
    conclusao="O critério de aceite é a reexecução: outra pessoa clona a pasta, roda e obtém os mesmos números.",
))

# ---------------------------------------------------------------------------
# 4. Os dois artefatos da trilha
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A Trilha de Tecnologia entrega dois artefatos avaliados",
    '        <div class="side-by-side">\n'
    "          <div>\n"
    "            <h3>Artefato 1 &middot; Análise Exploratória de Dados</h3>\n"
    "            <p>O código que carrega, limpa e visualiza a base, identificando os padrões "
    "associados ao churn. Entregue como pasta reexecutável.</p>\n"
    "            <p><strong>05/09/2026.</strong> Critério binário, com o foco no feedback. "
    "Alimenta o Customer Segmentation Report da manhã.</p>\n"
    "          </div>\n"
    "          <div>\n"
    "            <h3>Artefato 2 &middot; Aplicativo Web Preditivo-Generativo</h3>\n"
    "            <p>Executa o modelo de churn treinado em Python e consome uma API generativa "
    "para produzir o texto de retenção personalizado.</p>\n"
    "            <p><strong>03/10/2026.</strong> Critério por rubrica, defendido em banca. "
    "Alimenta o Plano de Inteligência de Retenção da manhã.</p>\n"
    "          </div>\n"
    "        </div>\n",
    sobrelinha="O destino da trilha",
    conclusao="A oficina de hoje começa a pasta do Artefato 1, e o critério de aceite é a reexecução.",
))

# ---------------------------------------------------------------------------
# 5. O checklist do Artefato 1
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "O Artefato 1 tem sete seções, e a oficina de hoje fecha quatro",
    '        <div class="embed-tabela">\n'
    "          <table>\n"
    "            <thead><tr><th>Seção</th><th>O que precisa ter</th><th>Quando</th></tr></thead>\n"
    "            <tbody>\n"
    "              <tr><td>01. Carga</td><td>contagem por aba conferida, grão declarado, contas em comum</td><td>hoje</td></tr>\n"
    "              <tr><td>02. Qualidade</td><td>o registro de tratamento, com o custo de cada decisão em linhas</td><td>hoje</td></tr>\n"
    "              <tr><td>03. Univariada</td><td>centro, dispersão e forma, com a leitura escrita de cada figura</td><td>hoje</td></tr>\n"
    "              <tr><td>04. Bivariada</td><td>contingência com o tamanho da base e a explicação alternativa</td><td>hoje</td></tr>\n"
    "              <tr><td>05. Rótulo</td><td>o critério recuperado do dado e três cortes alternativos</td><td>autoestudo</td></tr>\n"
    "              <tr><td>06. Visuais</td><td>as figuras que sustentam a segmentação e as personas da manhã</td><td>autoestudo</td></tr>\n"
    "              <tr><td>07. Limitações</td><td>o que esta base não permite responder</td><td>autoestudo</td></tr>\n"
    "            </tbody>\n"
    "          </table>\n"
    "        </div>\n",
    sobrelinha="Análise Exploratória de Dados &middot; entrega 05/09/2026",
    conclusao="A seção 06 é o item que o checklist da manhã cobra de vocês, então ela tem destinatário e prazo próprios.",
    fonte="O checklist completo está em CHECKLIST-ARTEFATO-1.md, na raiz da pasta clonada.",
))

# ---------------------------------------------------------------------------
# 4. Divisor: a base nova
# ---------------------------------------------------------------------------
SLIDES.append(secao(
    "01", "A base oficial",
    "Cinco abas, cinco grãos, e nenhuma garantia de que elas cruzam",
    condicoes=[
        "Conferir o que chegou antes de perguntar qualquer coisa",
        "Perfilar com a skill que o agente carrega da pasta",
        "Nomear as advertências desta base, que são outras",
    ],
))

# ---------------------------------------------------------------------------
# 5. As cinco abas
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "As cinco abas somam 341.075 linhas em quatro grãos diferentes",
    '        <div class="embed-tabela">\n'
    "          <table>\n"
    "            <thead><tr><th>Aba</th><th>Linhas</th><th>Colunas</th><th>Grão</th><th>Contas</th></tr></thead>\n"
    "            <tbody>\n"
    "              <tr><td>Dataset 1</td><td>24.071</td><td>7</td><td>conta e mês</td><td>8.282</td></tr>\n"
    "              <tr><td>Dataset 2</td><td>19.948</td><td>4</td><td>conta e marca</td><td>8.282</td></tr>\n"
    "              <tr><td>Dataset 3</td><td>80.848</td><td>6</td><td>conta e trimestre</td><td>47.185</td></tr>\n"
    "              <tr><td>Dataset 4</td><td>8.382</td><td>6</td><td>conta</td><td>8.282</td></tr>\n"
    "              <tr><td>raw data</td><td>207.826</td><td>18</td><td>linha de pedido</td><td>8.282</td></tr>\n"
    "            </tbody>\n"
    "          </table>\n"
    "        </div>\n",
    contexto="O painel de receita é mensal. O engajamento comercial é trimestral e cobre 47.185 contas, quase seis vezes o número de contas do painel.",
    conclusao="Duas abas com número de contas diferente não cruzam sozinhas, e a decisão de como cruzá-las é do grupo.",
    fonte="Fonte: datasets_case_modulo2.xlsx.",
))

# ---------------------------------------------------------------------------
# 6. As advertencias desta base
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Quatro advertências de qualidade substituem as do painel sintético",
    '        <div class="concept-cards quatro">\n'
    '          <div class="concept-card"><h3>A chave quase não cruza</h3>'
    "<p>Das 47.185 contas com engajamento comercial, 44.140 não existem no painel. "
    "Só 3.045 das 8.282 contas do painel têm engajamento, ou 36,8%.</p></div>\n"
    '          <div class="concept-card"><h3>O grão temporal difere</h3>'
    "<p>O painel tem 24 períodos mensais no formato 2024-04. O engajamento tem 14 "
    "períodos trimestrais no formato 2023-2, e começa antes do painel.</p></div>\n"
    '          <div class="concept-card"><h3>O cadastro repete conta</h3>'
    "<p>100 identificadores aparecem mais de uma vez, com setor e país divergentes "
    "na mesma conta.</p></div>\n"
    '          <div class="concept-card"><h3>Valores fora do domínio</h3>'
    "<p>25 linhas de receita negativa, 143 zeradas, e 53 participações de marca "
    "ausentes, algumas negativas e algumas somando acima de 1.</p></div>\n"
    "        </div>\n",
    conclusao="Nenhuma dessas quatro estava na base da Aula 02, e cada uma exige uma decisão de tratamento escrita.",
    fonte="Fonte: datasets_case_modulo2.xlsx. Contagens travadas em dados/tests/test_dataset_oficial.py.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 7. Onde estamos no CRISP-DM
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A troca de base devolve o módulo à segunda fase do CRISP-DM",
    '        <div class="processo-fases">\n'
    '          <div class="processo-fase"><span class="num">01</span><h3>Entendimento do negócio</h3>'
    "<p>Aula 01. A decisão de alvo do Comitê.</p></div>\n"
    '          <div class="processo-fase ativa"><span class="num">02</span><h3>Entendimento dos dados</h3>'
    "<p>Hoje. Base nova, perfilamento novo.</p></div>\n"
    '          <div class="processo-fase"><span class="num">03</span><h3>Preparação</h3>'
    "<p>Aula 02, reaplicada à base de hoje.</p></div>\n"
    '          <div class="processo-fase ativa"><span class="num">04</span><h3>Modelagem</h3>'
    "<p>Hoje entra a análise, o modelo fica para a UC2.</p></div>\n"
    '          <div class="processo-fase"><span class="num">05</span><h3>Avaliação</h3>'
    "<p>Aula 05, no veredito de alvo.</p></div>\n"
    '          <div class="processo-fase"><span class="num">06</span><h3>Implantação</h3>'
    "<p>Aulas 07 e 08.</p></div>\n"
    "        </div>\n",
    contexto="O CRISP-DM foi publicado em 1999 e é o mapa que o módulo percorre. As fases não são uma fila: uma base nova devolve o trabalho à fase 2 mesmo que a fase 4 já tenha começado.",
    conclusao="Perfilar a base de hoje custa vinte minutos, e pular esse passo compromete todo número que sair depois.",
    fonte="Fonte: Chapman et al., CRISP-DM 1.0, 1999.",
))

# ---------------------------------------------------------------------------
# 8. Checklist das cinco perguntas
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Cinco perguntas separam a base que chegou da base que você acha que chegou",
    '        <div class="exercise-steps">\n'
    '          <div class="pratica-passo"><span class="num">01</span><div>'
    '<p class="acao">Quantas linhas o agente está vendo? Se não bater com a fonte, o arquivo chegou quebrado.</p></div></div>\n'
    '          <div class="pratica-passo"><span class="num">02</span><div>'
    '<p class="acao">Uma linha representa o quê? Procure a combinação de colunas que não se repete.</p></div></div>\n'
    '          <div class="pratica-passo"><span class="num">03</span><div>'
    '<p class="acao">As chaves cruzam? Junção que perde linha aparece com o número antes de ser usada.</p></div></div>\n'
    '          <div class="pratica-passo"><span class="num">04</span><div>'
    '<p class="acao">Quantos vazios por coluna, e o vazio é zero ou desconhecido? A resposta não está no dado.</p></div></div>\n'
    '          <div class="pratica-passo"><span class="num">05</span><div>'
    '<p class="acao">Existe valor impossível? Receita negativa, participação acima de 1.</p></div></div>\n'
    "        </div>\n",
    sobrelinha="Checklist de perfilamento",
    conclusao="As cinco estão em skills/perfilamento.md, e o agente as executa sozinho.",
))

# ---------------------------------------------------------------------------
# 9. Pratica 1
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    1,
    "O perfilamento das cinco abas, com a skill que o agente carrega sozinho",
    20,
    "Em grupo, na pasta clonada",
    "O arquivo perfil.md, com as advertências ordenadas por linhas afetadas",
    "Cada mesa diz quantas das quatro advertências o agente achou sozinho",
    [
        {"acao": "Clone o repositório e coloque o xlsx em dados/.",
         "prompt": "git clone https://github.com/josercf/inteli-pos-2026-2a-eda.git"},
        {"acao": "Abra a pasta no Antigravity e peça ao agente que resuma as regras da sessão.",
         "detalhe": "Se ele não citar a proibição de preencher lacuna, ele não leu o AGENTS.md."},
        {"acao": "Peça o perfilamento pelo caminho do arquivo, sem colar instrução na conversa.",
         "prompt": "Execute skills/perfilamento.md sobre as cinco abas de dados/datasets_case_modulo2.xlsx."},
        {"acao": "Confira quais das quatro advertências ele achou sozinho, e qual passou."},
    ],
    "A mesa tem o perfil.md em disco e sabe qual advertência o agente deixou passar",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 10. Divisor: univariada
# ---------------------------------------------------------------------------
SLIDES.append(secao(
    "02", "Análise univariada",
    "Uma variável por vez, antes de comparar grupo nenhum",
    condicoes=[
        "Declarar o grão em que a variável está sendo medida",
        "Separar tendência central, dispersão e forma",
        "Escrever, abaixo de cada figura, o que ela não permite concluir",
    ],
))

# ---------------------------------------------------------------------------
# 11. O racional, construido com a turma
# ---------------------------------------------------------------------------
# Sem nenhum numero da base: a turma monta as tres perguntas antes de ver
# qualquer valor, senao a resposta chega antes do criterio.
SLIDES.append(conteudo(
    "Descrever uma variável exige três perguntas, e a terceira quase nunca é feita",
    '        <div class="exercise-steps">\n'
    '          <div class="pratica-passo fragment"><span class="num">01</span><div>'
    '<p class="acao">Onde está o centro?</p>'
    '<p class="detalhe">Média e mediana. Quando as duas divergem por uma ordem de grandeza, '
    "a média deixa de descrever qualquer caso individual.</p></div></div>\n"
    '          <div class="pratica-passo fragment"><span class="num">02</span><div>'
    '<p class="acao">Quanto os casos se afastam do centro?</p>'
    '<p class="detalhe">Desvio padrão e quartis. Um único extremo faz o desvio explodir e '
    "deixar de comparar grupos.</p></div></div>\n"
    '          <div class="pratica-passo fragment"><span class="num">03</span><div>'
    '<p class="acao">Qual o formato da distribuição?</p>'
    '<p class="detalhe">Assimetria e curtose. É a pergunta que diz se as respostas das duas '
    "primeiras valem alguma coisa, e é a que quase nunca aparece no relatório.</p></div></div>\n"
    "        </div>\n",
    contexto="Antes de comparar dois grupos, cada variável precisa ser descrita sozinha. A ordem importa: quem pula para a comparação atribui ao grupo um efeito que era da forma da distribuição.",
    conclusao="A terceira pergunta é a que decide se a média pode ser citada, então ela vem antes e não depois.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 12. O pedido, e como a assimetria sai
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A assimetria sai da média dos cubos dos desvios padronizados",
    '        <div class="side-by-side">\n'
    "          <div>\n"
    "            <h3>O pedido</h3>\n"
    '            <pre class="code-compact"><code>'
    '<span class="hl-dados">Some receita_usd por account_id.</span>\n'
    '<span class="hl-formato">1. média, mediana, desvio, mín, máx\n'
    "2. assimetria e curtose\n"
    "3. histograma, com a escala\n"
    "   declarada na legenda</span>\n"
    '<span class="hl-restricao">Código antes de cada número.</span></code></pre>\n'
    "          </div>\n"
    "          <div>\n"
    "            <h3>De onde vem o número</h3>\n"
    '            <pre class="code-compact"><code>z = (conta - média) / desvio\n'
    "assimetria = média(z³) = 44,5\n"
    "curtose    = média(z⁴) = 2.597</code></pre>\n"
    "            <p>O cubo preserva o sinal e amplifica quem está longe: uma conta a 10 desvios "
    "pesa mil vezes mais que uma a 1 desvio. A maior conta desta carteira está a "
    "<strong>67 desvios</strong> da média.</p>\n"
    "          </div>\n"
    "        </div>\n",
    sobrelinha="Antes de rodar",
    conclusao="Assimetria alta indica média construída por poucos casos, e isso se confere no máximo da coluna.",
))

# ---------------------------------------------------------------------------
# 12. Figura: distribuicao
# ---------------------------------------------------------------------------
SLIDES.append(figura(
    "O 1% de contas do topo concentra 65,1% da receita da carteira",
    "aula03-distribuicao-receita.png",
    "Histograma da receita acumulada por conta em escala logarítmica, com mediana em 18.552 dólares e média em 437.588 dólares",
    conclusao="Os 5% do topo somam 84,4% da receita e os 10% somam 90,6%, com a média 24 vezes acima da mediana.",
))

# ---------------------------------------------------------------------------
# 13. Quiz
# ---------------------------------------------------------------------------
SLIDES.append(quiz(
    "Verificação",
    "Qual número vai para o Comitê?",
    "O Comitê pede a receita típica de uma conta. Qual número você leva?",
    [
        {"texto": "A média da carteira toda, de USD 437.588.",
         "certa": False,
         "certo": "",
         "errado": "Com assimetria de 44,5 a média é puxada pelo topo, e nenhuma conta se parece com ela."},
        {"texto": "A mediana, USD 18.552, com a assimetria.",
         "certa": True,
         "certo": "A mediana descreve a conta do meio, e a assimetria declarada evita comparação com média de outra fonte.",
         "errado": ""},
        {"texto": "A média das contas do topo da carteira.",
         "certa": False,
         "certo": "",
         "errado": "Responde outra pergunta: o Comitê pediu a conta típica, e isso mede concentração."},
        {"texto": "Os dois números, para o Comitê decidir.",
         "certa": False,
         "certo": "",
         "errado": "Sem o critério que os separa, você transfere ao Comitê uma decisão técnica sua."},
    ],
    {"fichas": [
        ("Média", "USD 437.588"),
        ("Mediana", "USD 18.552"),
        ("Assimetria", '<span class="numerao">44,5</span>'),
    ]},
))

# ---------------------------------------------------------------------------
# 14. Pratica 2, enquadramento
# ---------------------------------------------------------------------------
# A pratica vem em dois slides: este enquadra, o proximo tem os passos. Em
# 15/08 a turma leu uma pratica de cinco passos como se fosse um prompt unico.
SLIDES.append(pratica(
    2,
    "A distribuição das variáveis do painel, com a leitura escrita",
    20,
    "Em grupo, na pasta clonada",
    "As figuras em figuras/ e o arquivo univariada.md",
    "Cada mesa lê em voz alta a frase do que a figura não permite concluir",
    [
        {"acao": "São quatro passos, e cada um é um pedido separado ao agente.",
         "detalhe": "Não cole os quatro de uma vez: o agente responde os quatro e você perde o ponto de conferência entre eles."},
        {"acao": "Depois de cada passo, confira antes de seguir.",
         "detalhe": "A lista do que conferir está no slide seguinte, ao lado de cada passo."},
        {"acao": "A entrega é a leitura escrita embaixo de cada figura.",
         "detalhe": "Figura sem as duas frases embaixo não entra na seção de univariada do artefato."},
    ],
    "Cada figura tem duas frases embaixo, e a segunda diz o que ela não sustenta",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 15. Pratica 2, passos 1 e 2
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    2, "Passos 1 e 2, as medidas e a figura", 20, "", "", "",
    [
        {"acao": "Peça as medidas das três variáveis.",
         "prompt": "Execute skills/univariada.md sobre receita_usd, qtd_pedidos e tempo_como_cliente.",
         "detalhe": "Confira: ele somou por conta ou contou linhas? Os dois grãos dão números diferentes."},
        {"acao": "Peça o histograma da receita.",
         "prompt": "Plote o histograma da receita por conta e declare a escala na legenda.",
         "detalhe": "Confira: o máximo do eixo bate com o máximo da tabela do passo 1?"},
    ],
    "As duas saídas estão em arquivo, e o grão está declarado em cada uma",
    ambiente=AMBIENTE, trilho=False,
    sobrelinha="Prática 2 &middot; um pedido por vez, com conferência entre eles",
))

# ---------------------------------------------------------------------------
# 16. Pratica 2, passos 3 e 4
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    2, "Passos 3 e 4, a leitura e o limite", 20, "", "", "",
    [
        {"acao": "Peça a leitura de negócio. Confira se sobrou termo técnico sem explicação.",
         "prompt": "Explique este gráfico sem termo técnico não explicado, e diga em três frases o que olhar nele."},
        {"acao": "Peça o limite da figura. Se ele afirmar causa, refaça o pedido.",
         "prompt": "Escreva o que este gráfico não permite concluir sobre a perda de contas."},
    ],
    "Cada figura tem duas frases embaixo, e a segunda diz o que ela não sustenta",
    ambiente=AMBIENTE, trilho=False,
    sobrelinha="Prática 2 &middot; um pedido por vez, com conferência entre eles",
))

# ---------------------------------------------------------------------------
# 15. Divisor: bivariada
# ---------------------------------------------------------------------------
SLIDES.append(secao(
    "03", "Análise bivariada",
    "Do cruzamento contra o rótulo até o critério que o define",
    condicoes=[
        "Um corte por vez, com o tamanho da base em cada célula",
        "Reconstruir o critério de um rótulo antes de usá-lo",
        "Perguntar, de toda variável que separa bem demais, se ela vazou",
    ],
))

# ---------------------------------------------------------------------------
# 16. As hipoteses, antes do numero
# ---------------------------------------------------------------------------
# A turma formula antes de ver a tabela. Sem isso, a primeira explicacao
# plausivel que aparecer na tela vira a conclusao do grupo.
SLIDES.append(conteudo(
    "Uma prevalência diferente entre segmentos admite pelo menos três explicações",
    '        <div class="exercise-steps">\n'
    '          <div class="pratica-passo fragment"><span class="num">01</span><div>'
    '<p class="acao">Que hipótese explicaria um segmento perder mais contas que outro?</p>'
    '<p class="detalhe">Cada mesa escreve uma. Vale ciclo de compra, vale cobertura comercial, '
    "vale porte da conta.</p></div></div>\n"
    '          <div class="pratica-passo fragment"><span class="num">02</span><div>'
    '<p class="acao">Que evidência nesta base sustentaria a sua hipótese?</p>'
    '<p class="detalhe">Precisa ser uma coluna que existe, não uma que você gostaria que '
    "existisse.</p></div></div>\n"
    '          <div class="pratica-passo fragment"><span class="num">03</span><div>'
    '<p class="acao">Que evidência a derrubaria?</p>'
    '<p class="detalhe">Hipótese que nenhum dado desta base pode derrubar não vai ser testada '
    "hoje, e isso entra na seção de limitações.</p></div></div>\n"
    "        </div>\n",
    contexto="A manhã fechou a segmentação. A tarde mede o churn dentro dela, e a ordem importa: quem vê a tabela antes de formular fica com a primeira explicação plausível que a tabela sugerir.",
    conclusao="As três hipóteses ficam em pé até o fim da aula, e o critério que decide entre elas é a medida.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 16. Tabela de contingencia
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A prevalência de churn na carteira é 19,2%, e ela varia de 13,0% a 31,2% entre segmentos",
    '        <div class="embed-tabela">\n'
    "          <table>\n"
    "            <thead><tr><th>Segmento</th><th>Contas</th><th>Perdidas</th>"
    "<th>Prevalência</th><th>Participação na receita</th></tr></thead>\n"
    "            <tbody>\n"
    "              <tr><td>Setor público</td><td>837</td><td>261</td><td>31,2%</td><td>21,9%</td></tr>\n"
    "              <tr><td>Mid market</td><td>3.134</td><td>716</td><td>22,8%</td><td>10,3%</td></tr>\n"
    "              <tr><td>Estratégicas</td><td>117</td><td>18</td><td>15,4%</td><td>6,3%</td></tr>\n"
    "              <tr><td>Grandes contas</td><td>1.711</td><td>263</td><td>15,4%</td><td>21,9%</td></tr>\n"
    "              <tr><td>Small market</td><td>1.234</td><td>173</td><td>14,0%</td><td>26,7%</td></tr>\n"
    "              <tr><td>Contas globais</td><td>1.249</td><td>162</td><td>13,0%</td><td>12,9%</td></tr>\n"
    "            </tbody>\n"
    "          </table>\n"
    "        </div>\n",
    contexto="Prevalência é a proporção de contas rotuladas como perdidas dentro da categoria. Sem o tamanho da base ao lado, ela engana: 100% de churn em três contas não é achado.",
    conclusao="O setor público reúne a maior prevalência e a segunda maior participação na receita, então ele é o único segmento em que as duas leituras apontam para a mesma prioridade.",
    fonte="Fonte: Dataset 1 e Dataset 4, 8.282 contas. Travado em dados/tests/test_dataset_oficial.py.",
))

# ---------------------------------------------------------------------------
# 17. Figura: prevalencia
# ---------------------------------------------------------------------------
SLIDES.append(figura(
    "Small market concentra 26,7% da receita com a segunda menor prevalência de churn",
    "aula03-prevalencia-segmento.png",
    "Barras horizontais comparando prevalência de churn e participação na receita por segmento",
    conclusao="Prevalência e receita em risco produzem topos diferentes para a mesma fila.",
))

# ---------------------------------------------------------------------------
# 18. Figura: contingencia do rotulo
# ---------------------------------------------------------------------------
SLIDES.append(figura(
    "1.482 contas pararam de comprar até janeiro de 2025 e todas estão rotuladas como perdidas",
    "aula03-contingencia-rotulo.png",
    "Contas por último mês com receita, separadas entre rotuladas como perdidas e rotuladas como ativas",
    conclusao="Fevereiro de 2025 é o único mês com contas dos dois lados, e o corte que os separa não está documentado.",
))

# ---------------------------------------------------------------------------
# 19. O corte diario
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "O corte separa em 08 de fevereiro de 2025, numa granularidade que o painel mensal não expõe",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>O que o painel mensal entrega</h3>'
    "<p>Inatividade de 13 meses marca 1.975 contas e captura 100% das 1.593 perdidas. "
    "Sobram 382 contas que o corte marca e o rótulo não.</p></div>\n"
    '          <div class="concept-card"><h3>Onde estão as 382</h3>'
    "<p>Todas em fevereiro de 2025, o único mês com contas dos dois lados. "
    "São 493 contas nesse mês, 111 perdidas e 382 ativas.</p></div>\n"
    '          <div class="concept-card"><h3>O que a aba de pedidos resolve</h3>'
    "<p>A última compra das perdidas vai até 08/02/2025. A das ativas começa em "
    "10/02/2025. A separação é perfeita no dia.</p></div>\n"
    "        </div>\n",
    contexto="A aba raw data tem 207.826 linhas e a data de cada pedido. Ela não caberia num anexo de conversa, e é por isso que a tarde roda em pasta.",
    conclusao="Quem usou só o agregado mensal chega a treze meses e para em 382 contas sem explicação.",
    fonte="Fonte: aba raw data, data do último pedido por conta. Travado em dados/tests/test_dataset_oficial.py.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 20. Cortes alternativos
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Afrouxar o corte de 13 para 6 meses multiplica a fila de intervenção por 2,6",
    '        <div class="embed-tabela">\n'
    "          <table>\n"
    "            <thead><tr><th>Corte de inatividade</th><th>Contas na fila</th>"
    "<th>Captura do rótulo oficial</th><th>Leitura operacional</th></tr></thead>\n"
    "            <tbody>\n"
    "              <tr><td>6 meses</td><td>5.128</td><td>100%</td><td>Antecipa muito e satura a operação</td></tr>\n"
    "              <tr><td>9 meses</td><td>3.719</td><td>100%</td><td>Fila ainda acima da capacidade</td></tr>\n"
    "              <tr><td>12 meses</td><td>2.716</td><td>100%</td><td>Chega perto do rótulo oficial</td></tr>\n"
    "              <tr><td>13 meses</td><td>1.975</td><td>100%</td><td>É o corte que a base usa</td></tr>\n"
    "            </tbody>\n"
    "          </table>\n"
    "        </div>\n",
    contexto="Todos os cortes capturam 100% das contas que o rótulo oficial marca, porque o rótulo oficial é o mais restritivo dos quatro.",
    conclusao="O corte de 13 meses marca a conta treze meses depois da última compra, quando não sobra intervenção comercial a fazer.",
    fonte="Fonte: Dataset 1, recência contada a partir de 2026-03. Travado em dados/tests/test_dataset_oficial.py.",
))

# ---------------------------------------------------------------------------
# 21. Vazamento
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Nenhuma das 4.494 contas com menos de 17 meses de casa aparece como perdida",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>O que a variável parece ser</h3>'
    "<p>Tempo de casa separa os dois grupos em 17 meses. Num modelo, seria o preditor mais forte da base.</p></div>\n"
    '          <div class="concept-card"><h3>O que ela é</h3>'
    "<p>O rótulo exige treze meses de inatividade. Conta com menos de 17 meses de casa não teve tempo de satisfazer a regra.</p></div>\n"
    '          <div class="concept-card"><h3>O teste que evita isso</h3>'
    "<p>De toda variável que separa bem, pergunte se a informação existiria na hora da decisão.</p></div>\n"
    "        </div>\n",
    sobrelinha="Vazamento de informação",
    contexto="Separação perfeita é sinal de vazamento antes de ser sinal de achado: o modelo funciona no teste e falha em produção.",
    conclusao="A fronteira de 17 meses mede a regra de rotulagem contra a janela do painel.",
    fonte="Fonte: Dataset 1 e Dataset 4.",
))

# ---------------------------------------------------------------------------
# 22. Quiz
# ---------------------------------------------------------------------------
SLIDES.append(quiz(
    "Verificação",
    "O que explica a fronteira de 17 meses?",
    "Nenhuma conta com menos de 17 meses de casa aparece como perdida. Por quê?",
    [
        {"texto": "A amostra de contas novas é pequena demais.",
         "certa": False,
         "certo": "",
         "errado": "São 4.494 contas. Com prevalência de 19,2%, seriam esperadas centenas de casos."},
        {"texto": "Contas novas ainda são mais fiéis à Kovan.",
         "certa": False,
         "certo": "",
         "errado": "Hipótese plausível que esta base não sustenta: a fronteira é limpa demais para ser comportamento."},
        {"texto": "A regra exige inatividade que elas não acumularam.",
         "certa": True,
         "certo": "A fronteira descreve a construção do rótulo, e um modelo com ela aprende a régua em vez do risco.",
         "errado": ""},
        {"texto": "O time comercial prioriza e protege as contas novas.",
         "certa": False,
         "certo": "",
         "errado": "Priorização produziria prevalência menor, e não zero em 4.494 contas."},
    ],
    {"fichas": [
        ("Contas com menos de 17 meses", "4.494"),
        ("Perdidas entre elas", '<span class="numerao">0</span>'),
        ("Prevalência da carteira", "19,2%"),
    ]},
))

# ---------------------------------------------------------------------------
# 23. Pratica 3, enquadramento
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    3,
    "A engenharia reversa do critério do rótulo",
    25,
    "Em grupo, na pasta clonada",
    "A tabela de contingência e o critério recuperado, em bivariada.md",
    "Cada mesa apresenta o critério que recuperou e a evidência que o sustenta",
    [
        {"acao": "São quatro pedidos separados, e o terceiro só faz sentido depois do segundo.",
         "detalhe": "O passo 2 produz um resíduo que o passo 3 resolve. Colar os quatro de uma vez pula o resíduo."},
        {"acao": "Se o grupo não recuperar o critério, isso também é resultado.",
         "detalhe": "O registro nesse caso é critério desconhecido, com o que foi tentado."},
        {"acao": "As hipóteses do bloco anterior continuam em pé.",
         "detalhe": "Ao final, diga qual delas o que você mediu sustenta e qual ele derruba."},
    ],
    "A mesa enuncia o critério do rótulo e mostra a tabela que o sustenta",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 24. Pratica 3, passos 1 e 2
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    3, "Passos 1 e 2, a prevalência e a contingência", 25, "", "", "",
    [
        {"acao": "Peça a prevalência por segmento, com o tamanho da base.",
         "prompt": "No grão da conta, traga contas, contas perdidas, prevalência e participação na receita por segmento_lenovo.",
         "detalhe": "Confira: a soma das contas bate com 8.282? Categoria com menos de 30 contas entra marcada."},
        {"acao": "Peça a contingência do último mês contra o rótulo.",
         "prompt": "Calcule o último período com receita de cada conta e cruze com churn_label. Ache o único mês com contas dos dois lados.",
         "detalhe": "Confira: a soma das células bate com 8.282? Se não bater, ele perdeu contas na agregação."},
    ],
    "As duas tabelas trazem o tamanho da base em cada célula",
    ambiente=AMBIENTE, trilho=False,
    sobrelinha="Prática 3 &middot; um pedido por vez, com conferência entre eles",
))

# ---------------------------------------------------------------------------
# 25. Pratica 3, passos 3 e 4
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    3, "Passos 3 e 4, o grão do pedido e os cortes", 25, "", "", "",
    [
        {"acao": "Desça ao grão do pedido para resolver o resíduo do passo 2.",
         "prompt": "Na raw data, para as contas desse mês, cruze a data do último pedido com churn_label. Existe data que separe sem exceção?",
         "detalhe": "Confira: ele leu as 207.826 linhas? Se resumiu por amostragem, o corte não aparece."},
        {"acao": "Meça o que cortes alternativos fariam com a fila.",
         "prompt": "Construa rótulos com cortes de 6, 9 e 12 meses de inatividade a partir de 2026-03. Traga o tamanho da fila e a receita marcada em cada um.",
         "detalhe": "Confira: a fila cresce quando o corte afrouxa? Se não crescer, a data de referência está errada."},
    ],
    "A mesa escreve o critério do rótulo em uma frase, com a evidência ao lado",
    ambiente=AMBIENTE, trilho=False,
    sobrelinha="Prática 3 &middot; um pedido por vez, com conferência entre eles",
))

# ---------------------------------------------------------------------------
# 24. Divisor: oficina
# ---------------------------------------------------------------------------
SLIDES.append(secao(
    "04", "Oficina do Artefato 1",
    "Quatro estações, uma por seção do checklist",
    condicoes=[
        "Cada seção entra com o número e a figura que a sustentam",
        "Cada decisão de tratamento entra no registro, com o custo em linhas",
        "A pasta precisa reexecutar na máquina de outra pessoa",
    ],
))

# ---------------------------------------------------------------------------
# 26. A skill de limpeza
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A skill calcula o custo das três decisões e para antes de escolher",
    '        <div class="side-by-side">\n'
    "          <div>\n"
    '            <pre class="code-compact"><code># Skill: limpeza de dados\n'
    '<span class="hl-restricao">Não preencha lacuna.\n'
    "Não decida no lugar de quem\n"
    "responde pelo número.</span>\n"
    "## Por advertência\n"
    '<span class="hl-dados">1. Meça o tamanho\n'
    "2. A ausência é condicionada?\n"
    "3. Escolha o indicador\n"
    "4. Calcule sob as três decisões\n"
    '5. Pare e pergunte</span>\n'
    '<span class="hl-formato">## registro-de-tratamento.md</span></code></pre>\n'
    "          </div>\n"
    "          <div>\n"
    '            <div class="concept-cards">\n'
    '              <div class="concept-card"><h3>Excluir</h3>'
    "<p>Assume que o que falta é aleatório.</p></div>\n"
    '              <div class="concept-card"><h3>Imputar</h3>'
    "<p>Inventa variação que não foi observada.</p></div>\n"
    '              <div class="concept-card"><h3>Sinalizar</h3>'
    "<p>Adia a decisão para a análise seguinte.</p></div>\n"
    "            </div>\n"
    "          </div>\n"
    "        </div>\n",
    sobrelinha="skills/limpeza-de-dados.md",
    conclusao="Nada nela é específico da Kovan, e o artefato que ela produz é o registro de tratamento.",
))

# ---------------------------------------------------------------------------
# 26. Oficina
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    4,
    "A oficina fecha quatro das sete seções do artefato",
    55,
    "Em grupo, na pasta clonada",
    "A pasta do grupo, com código, figuras e o registro de tratamento",
    "Às 15h20 as mesas trocam de pasta e executam a skill uma da outra",
    [
        {"acao": "Estação 1, 10 min. Carga: contagem por aba, grão e contas em comum."},
        {"acao": "Estação 2, 25 min. Qualidade: rode a skill e decida cada advertência.",
         "prompt": "Execute skills/limpeza-de-dados.md sobre dados/datasets_case_modulo2.xlsx, uma advertência por vez."},
        {"acao": "Troca de pastas: execute a skill e o registro da mesa ao lado.",
         "detalhe": "Número que não bate indica passo do registro que só fazia sentido para quem escreveu."},
        {"acao": "Estação 3, 10 min. Univariada: aproveite as figuras da Prática 2."},
        {"acao": "Estação 4, 10 min. Bivariada: some um corte por setor à tabela da Prática 3."},
    ],
    "A mesa ao lado executa o registro de vocês e chega aos mesmos números",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 27. Amarracao
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A base tratada de hoje sustenta as figuras da Aula 04 e a segmentação da manhã",
    '        <div class="linha-tempo">\n'
    '          <div class="etapa fragment"><p class="quando">22/08 &middot; hoje</p><h3>Fica pronto</h3>'
    "<p>Quatro seções do Artefato 1 e o critério do rótulo recuperado do dado.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">29/08 &middot; Aula 04</p><h3>Visualização para decidir</h3>'
    "<p>As figuras que vão ao Comitê saem dos números que a pasta do grupo reproduz.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">Manhã de negócios</p><h3>Segmentação e personas</h3>'
    "<p>O relatório da manhã pede as visualizações da EDA, e a seção 06 as entrega.</p></div>\n"
    '          <div class="etapa avaliada fragment"><p class="quando">05/09 &middot; Semana 5</p><h3>Artefato 1</h3>'
    "<p>Análise Exploratória de Dados, entregue como pasta reexecutável.</p></div>\n"
    "        </div>\n",
    conclusao="O rótulo que a base entregou marca a conta treze meses depois da última compra, e essa medida é o insumo do veredito de alvo da Aula 05.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 28. Referencias
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Referências e nota metodológica",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>Caso e dados</h3>'
    "<p>1. Kovan Technologies LATAM: A Definição do Alvo. Business case PL-02-2026, versão v2.</p>"
    "<p>2. datasets_case_modulo2.xlsx, base oficial recebida em 21/08/2026. Não distribuída "
    "por este acervo, por ser dado real de carteira.</p></div>\n"
    '          <div class="concept-card"><h3>Frameworks citáveis</h3>'
    "<p>3. Chapman, P. et al. CRISP-DM 1.0: Step-by-step data mining guide. SPSS, 1999.</p>"
    "<p>4. Tukey, J. W. Exploratory Data Analysis. Addison-Wesley, 1977.</p>"
    "<p>5. Kaufman, S. et al. Leakage in Data Mining. ACM TKDD, 2012.</p></div>\n"
    '          <div class="concept-card"><h3>O que é nosso</h3>'
    "<p>O checklist de cinco perguntas de perfilamento, o checklist de sete seções do "
    "Artefato 1 e as três skills de agente foram organizados para este módulo, sem "
    "seguir padrão publicado.</p></div>\n"
    "        </div>\n",
    conclusao="O critério do rótulo apresentado hoje foi recuperado do próprio dado e está travado por teste, sem depender de documentação da fonte.",
))

# ---------------------------------------------------------------------------
# Esqueleto
# ---------------------------------------------------------------------------
ESQUELETO = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aula 03 &middot; O corte que define o rótulo &middot; MBA Inteli x Lenovo</title>

  <!-- Gerado por tools/montar_deck_aula03.py. Nao editar a mao: a numeracao de
       rodape e o fechamento de secao sao garantidos la, e ja se perderam aqui. -->

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
