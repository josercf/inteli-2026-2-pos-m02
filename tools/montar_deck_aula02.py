# -*- coding: utf-8 -*-
"""Monta aulas/aula02.html.

Gerado, nunca editado a mao: a numeracao de rodape e o fechamento de secao sao
garantidos aqui, e ja se perderam no HTML duas vezes.

Diretiva editorial de 15/08/2026: sem paralelismo negativo, sem antitese
simetrica, sem escalada com dois-pontos. Titulo de slide de conteudo e a
conclusao completa, com o numero dentro. Travado por tools/check_retorica.py.

Todo numero do case que aparece aqui esta travado em
dados/tests/test_aula02_numeros.py ou em dados/tests/test_painel_kovan.py.

Uso: python3 tools/montar_deck_aula02.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from tools import deck_kit  # noqa: E402
from tools.deck_kit import conteudo, figura, pratica, quiz, secao  # noqa: E402

SAIDA = RAIZ / "aulas" / "aula02.html"

deck_kit.configurar("Módulo 2 &middot; Aula 02")
deck_kit.reiniciar_paginacao()

# ---------------------------------------------------------------------------
# Os slides
# ---------------------------------------------------------------------------

SLIDES: list[str] = []

# 1. Capa
SLIDES.append(
    '      <section class="cover-slide">\n'
    '        <div class="cover-panel">\n'
    '          <div class="cover-content">\n'
    '            <p class="cover-eyebrow">MBA em IA e Dados para Negócios &middot; Inteli x Lenovo</p>\n'
    "            <h1>O dado sujo é o case</h1>\n"
    "            <h3>Preparação e limpeza de dados, e o custo numérico de cada decisão de tratamento</h3>\n"
    '            <p class="cover-meta">Módulo 2 &middot; Aula 02 &middot; Trilha de Tecnologia</p>\n'
    '            <p class="cover-meta">15 de agosto de 2026 &middot; 14h00 às 17h30</p>\n'
    "          </div>\n"
    "        </div>\n"
    "      </section>\n"
)

# 2. Resgate da Aula 01
SLIDES.append(conteudo(
    "Três mesas aplicaram o mesmo critério de ruptura e chegaram a contagens diferentes de 34",
    '        <div class="stat-tiles">\n'
    '          <div class="stat-tile"><p class="stat-numero">34</p>'
    '<p class="stat-rotulo">rupturas no segmento estratégico, referência</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">1.652</p>'
    '<p class="stat-rotulo">observações conta-trimestre no segmento</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">160</p>'
    '<p class="stat-rotulo">linhas do painel sem receita registrada</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">0</p>'
    '<p class="stat-rotulo">decisões de tratamento escritas por alguma mesa</p></div>\n'
    "        </div>\n"
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>O critério aplicado</h3>'
    "<p>Zero pedidos faturados em dois trimestres consecutivos.</p></div>\n"
    '          <div class="concept-card"><h3>A pergunta de abertura</h3>'
    "<p>O que cada mesa fez com as linhas sem receita registrada?</p></div>\n"
    '          <div class="concept-card"><h3>O que sobrou da Aula 01</h3>'
    "<p>Três contagens, nenhuma com o tratamento que a produziu.</p></div>\n"
    "        </div>\n",
    conclusao="A divergência entra hoje como insumo, e a tarde mede quanto cada decisão de tratamento vale em número.",
    fonte="Fonte: painel Kovan, 16.618 registros conta-trimestre e 1.187 contas. Contagem de ruptura construída na Aula 01.",
))

# 3. Contrato do dia e entregavel
SLIDES.append(conteudo(
    "O entregável do dia exige uma decisão declarada para cada uma das quatro advertências do Exhibit 3",
    '        <div class="concept-cards quatro">\n'
    '          <div class="concept-card"><h3>Receita ausente</h3>'
    "<p>160 linhas sem <code>receita_brl</code>, 14 delas no segmento estratégico.</p></div>\n"
    '          <div class="concept-card"><h3>Engajamento ausente</h3>'
    "<p>8.280 linhas sem <code>visitas_registradas</code> nem <code>interacoes_crm</code>.</p></div>\n"
    '          <div class="concept-card"><h3>Quebra de taxonomia</h3>'
    "<p><code>linhas_produto_ativas</code> muda de régua em 2023Q1, com salto de 98,5%.</p></div>\n"
    '          <div class="concept-card"><h3>Sinal das devoluções</h3>'
    "<p><code>devolucoes_brl</code> tem 15.999 valores negativos e nenhum positivo.</p></div>\n"
    "        </div>\n",
    contexto="Até 17h30: a base tratada, o custo numérico de cada decisão e a skill em Markdown que reproduz os dois quando executada.",
    conclusao="Advertência sem decisão registrada conta como decisão de manter o dado como veio, e entra no registro com esse nome.",
    rotulo_conclusao="Entrega",
    fonte="Fonte: Exhibit 3 do Caderno Kovan PL-02-2026 v2, medido sobre as 16.618 linhas entregues.",
))

# 4. Divisor: qualidade de dado
SLIDES.append(secao(
    "Bloco 1 de 4",
    "Qualidade de dado",
    "Onde a limpeza mora dentro da análise exploratória, e o vocabulário que nomeia cada defeito.",
    ["A base foi perfilada?", "O defeito tem nome?", "A decisão está escrita?"],
))

# 5. Onde a limpeza mora dentro da EDA
SLIDES.append(conteudo(
    "As decisões de preparação determinam os números que a análise exploratória produz",
    '        <div class="linha-tempo">\n'
    '          <div class="etapa"><p class="quando">Passo 1</p><h3>Perfilar</h3>'
    "<p>Quais colunas existem, quantos valores faltam e onde a lacuna se concentra.</p></div>\n"
    '          <div class="etapa"><p class="quando">Passo 2</p><h3>Decidir</h3>'
    "<p>O que fazer com cada defeito, escrito antes de recalcular qualquer indicador.</p></div>\n"
    '          <div class="etapa"><p class="quando">Passo 3</p><h3>Medir</h3>'
    "<p>O indicador recalculado sob cada alternativa de tratamento, no mesmo código.</p></div>\n"
    '          <div class="etapa avaliada"><p class="quando">Passo 4</p><h3>Registrar</h3>'
    "<p>O arquivo que outra pessoa executa e obtém o mesmo número.</p></div>\n"
    "        </div>\n",
    contexto="O ciclo de seis passos da EDA assistida ficou na Aula 01. O recorte de hoje é o que acontece antes da primeira estatística.",
    conclusao="A análise exploratória da Aula 03 recebe o resultado destes quatro passos, junto com todo defeito que eles deixarem passar.",
))

# 6. As seis dimensoes de qualidade
SLIDES.append(conteudo(
    "Seis dimensões descrevem a qualidade de uma base: completude, validade, consistência, unicidade, acurácia e temporalidade",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>Completude</h3>'
    "<p>160 linhas sem receita e 8.280 sem engajamento.</p></div>\n"
    '          <div class="concept-card"><h3>Validade</h3>'
    "<p>devolucoes_brl chega com sinal negativo.</p></div>\n"
    '          <div class="concept-card"><h3>Consistência</h3>'
    "<p>taxonomia_mix muda de régua em 2023Q1.</p></div>\n"
    '          <div class="concept-card"><h3>Unicidade</h3>'
    "<p>16.618 linhas, 1.187 contas, sem duplicata.</p></div>\n"
    '          <div class="concept-card"><h3>Acurácia</h3>'
    "<p>Visita ausente do CRM contra visita que não ocorreu.</p></div>\n"
    '          <div class="concept-card"><h3>Temporalidade</h3>'
    "<p>Janela de 2022Q3 a 2025Q4, em duas réguas de mix.</p></div>\n"
    "        </div>\n",
    conclusao="Quatro das seis dimensões têm defeito documentado neste painel.",
))

# 7. Pratica 1
SLIDES.append(pratica(
    1, "Perfil de qualidade do painel", 20,
    "Em grupo, uma tela por grupo",
    "A lista de defeitos que a IA apontou sozinha, e o que ela deixou passar",
    "Aos 14 minutos, as quatro advertências em voz alta",
    [
        {"acao": "Suba o painel no Gemini e peça o perfil coluna a coluna.",
         "prompt": "Perfile este CSV coluna a coluna: tipo, valores ausentes, valores distintos, mínimo e máximo. Devolva o código que produziu cada número."},
        {"acao": "Acrescente a restrição contra preenchimento.",
         "prompt": "Não preencha nenhuma lacuna e não estime nenhum valor. Se faltar informação para responder, diga que falta."},
        {"acao": "Marque quais defeitos ela apontou por conta própria.",
         "detalhe": "São quatro no Exhibit 3. Anote quantos apareceram sem você citar."},
        {"acao": "Confira um número do perfil rodando a contagem você mesmo.",
         "detalhe": "Comece pela contagem de linhas sem receita registrada."},
    ],
    "O grupo sabe qual advertência a IA deixou passar.",
    ambiente="Gemini",
))

# 8. Divisor: as quatro advertencias
SLIDES.append(secao(
    "Bloco 2 de 4",
    "As quatro advertências do Exhibit 3",
    "Os quatro defeitos medidos sobre as 16.618 linhas que a turma recebeu.",
    ["Quantas linhas atinge", "Onde se concentra", "Qual indicador move"],
))

# 9. Advertencia 1: receita ausente
SLIDES.append(conteudo(
    "160 linhas do painel não têm receita registrada, e todas pertencem a contas ativas",
    '        <div class="stat-tiles">\n'
    '          <div class="stat-tile"><p class="stat-numero">160</p>'
    '<p class="stat-rotulo">linhas sem receita_brl, de 16.618</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">Ativa</p>'
    '<p class="stat-rotulo">status de conta das 160, sem exceção</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">14</p>'
    '<p class="stat-rotulo">dessas linhas no segmento estratégico</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">160</p>'
    '<p class="stat-rotulo">linhas sem valor_medio_pedido_brl</p></div>\n'
    "        </div>\n"
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>Onde a lacuna cai</h3>'
    "<p>Nos 14 trimestres, sempre em conta ativa.</p></div>\n"
    '          <div class="concept-card"><h3>O que ela arrasta</h3>'
    "<p>O valor médio do pedido some nas mesmas 160 linhas.</p></div>\n"
    '          <div class="concept-card"><h3>O que ela exige</h3>'
    "<p>Nomear o mecanismo antes de escolher o tratamento.</p></div>\n"
    "        </div>\n",
    sobrelinha="Advertência 1 de 4",
    conclusao="Descartar a linha remove trimestre de conta que seguia comprando.",
    fonte="Fonte: painel Kovan, colunas receita_brl e valor_medio_pedido_brl.",
))

# 10. Figura: mapa de ausencia
SLIDES.append(figura(
    "A ausência se concentra em quatro colunas e varia com o segmento",
    "aula02-mapa-ausencia.png",
    "Matriz da taxa de ausência por coluna e por segmento no painel de contas da Kovan",
    conclusao="Taxa de ausência que muda com uma coluna observada indica ausência condicionada.",
))

# 11. Advertencia 2: engajamento ausente
SLIDES.append(conteudo(
    "A ausência de registro de engajamento varia de 29,4% a 53,2% entre segmentos",
    '        <div class="concept-cards quatro">\n'
    '          <div class="concept-card"><h3>Estratégico</h3>'
    "<p>29,4% das linhas sem visita nem interação registrada.</p></div>\n"
    '          <div class="concept-card"><h3>Médio</h3><p>49,9%.</p></div>\n'
    '          <div class="concept-card"><h3>Cauda</h3><p>53,2%.</p></div>\n'
    '          <div class="concept-card"><h3>Total</h3>'
    "<p>8.280 das 16.618 linhas do painel.</p></div>\n"
    "        </div>\n",
    sobrelinha="Advertência 2 de 4",
    contexto="As colunas visitas_registradas e interacoes_crm faltam sempre nas mesmas linhas, de modo que a lacuna cobre o registro de atividade comercial inteiro.",
    conclusao="A taxa de ausência acompanha o segmento, de modo que preencher a lacuna com zero desloca mais as contas de cauda do que as estratégicas.",
    fonte="Fonte: painel Kovan, 16.618 registros conta-trimestre. Exhibit 3, advertência 2 de 4.",
))

# 12. Figura: quebra de taxonomia
SLIDES.append(conteudo(
    "A média de linhas de produto sobe 98,5% em 2023Q1 sem nenhuma transação nova",
    # O PNG mede 1168x420 e traz 16px de branco puro no topo e 19px na base,
    # medidos pixel a pixel. Esta e a unica figura do deck cuja altura nao cabe
    # com folga: sem cortar essa borda, o slide fecha a 12px do limite de 720px
    # e o CI, que renderiza com outra fonte, reprova por alguns pixels.
    #
    # O corte vem de uma moldura com overflow, e nao de margem negativa na
    # propria figura: margem negativa move a caixa da imagem por cima da faixa
    # de conclusao, e o check_slides.py reprova como sobreposicao, com razao.
    # A moldura tambem preserva a regra da figura: 1168px de largura, 1:1, o
    # corpo declarado na figura e o corpo projetado.
    # Altura = 420 natural - 14 cortados no topo - 16 cortados na base.
    '        <div class="figura-moldura" style="height: 390px; overflow: hidden">\n'
    '          <img class="figura" style="margin-top: -14px"'
    ' src="../assets/img/aula02-quebra-taxonomia.png"'
    ' alt="Série trimestral da média de linhas de produto ativas, com o corte de taxonomia de 2023Q1 marcado">\n'
    "        </div>\n",
    conclusao="A erosão real de mix é a queda de 30,4%, e a janela inteira registra alta de 38%.",
    conclusao_clara=True,
))

# 13. Advertencia 4: sinal das devolucoes
SLIDES.append(conteudo(
    "As devoluções chegam com sinal negativo, e inverter esse sinal desloca R$ 217,4 milhões da receita líquida",
    '        <table class="tabela-criterios">\n'
    "          <thead><tr><th>Operação</th><th>Código</th><th>Receita líquida do painel</th></tr></thead>\n"
    "          <tbody>\n"
    '            <tr class="fragment"><td>Somar a coluna</td>'
    "<td><code>receita_brl + devolucoes_brl</code></td>"
    '<td class="vence">R$ 8,298 bi</td></tr>\n'
    '            <tr class="fragment"><td>Subtrair a coluna</td>'
    "<td><code>receita_brl - devolucoes_brl</code></td>"
    "<td>R$ 8,515 bi</td></tr>\n"
    '            <tr class="decisiva fragment"><td>Diferença entre as duas leituras</td>'
    "<td>duas vezes a soma das devoluções</td>"
    "<td>R$ 217,4 milhões</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    sobrelinha="Advertência 4 de 4",
    contexto="A coluna devolucoes_brl traz 15.999 valores negativos, 619 zeros e nenhum valor positivo.",
    conclusao="Um sinal trocado em uma linha de código move 2,59% da receita do painel.",
    por_passos=True,
    fonte="Fonte: painel Kovan, receita bruta de R$ 8,406 bi. Exhibit 3, advertência 4 de 4.",
))

# 14. Quiz 1
SLIDES.append(quiz(
    "Verificação &middot; questão 1",
    "A média de linhas de produto",
    "A média de linhas de produto passou de 1,85 para 3,67 entre 2022Q4 e 2023Q1. O que aconteceu com a carteira?",
    [
        {"texto": "As contas passaram a contratar mais linhas de produto", "certa": False,
         "certo": "Correto.",
         "errado": "Nenhuma transação acompanha o salto. O volume de pedidos segue a mesma série nos dois trimestres."},
        {"texto": "A régua de contagem mudou e o mix ficou igual", "certa": True,
         "certo": "A coluna taxonomia_mix vale pre_2023 em 2022Q3 e 2022Q4, e pos_2023 nos doze trimestres seguintes. O salto é da régua.",
         "errado": "Procure a coluna que muda de valor exatamente entre 2022Q4 e 2023Q1."},
        {"texto": "O painel perdeu as contas de menor mix no trimestre", "certa": False,
         "certo": "Correto.",
         "errado": "O painel tem as mesmas 1.187 contas ao longo dos 14 trimestres."},
        {"texto": "Houve erro de carga no fechamento de 2023Q1", "certa": False,
         "certo": "Correto.",
         "errado": "A mudança está documentada no Exhibit 3, e vale para todos os trimestres seguintes."},
    ],
    {"fichas": [
        ("A média por trimestre", "linhas_produto_ativas"),
        ("O salto", '<span class="numerao">+98,5%</span>'),
        ("A coluna taxonomia_mix", "pre_2023 em 2022Q3 e 2022Q4"),
    ]},
))

# 15. Pratica 2
SLIDES.append(pratica(
    2, "O mecanismo da ausência", 20,
    "Em grupo, uma tela por grupo",
    "A taxa de ausência de engajamento por segmento, com o código",
    "Aos 14 minutos, comparação das taxas entre as mesas",
    [
        {"acao": "Peça a taxa de ausência de visitas por segmento.",
         "prompt": "Calcule a proporção de linhas com visitas_registradas ausente, por segmento. Devolva o código pandas e a tabela."},
        {"acao": "Compare as três taxas entre si.",
         "detalhe": "Taxas iguais entre segmentos indicariam ausência aleatória."},
        {"acao": "Teste se a ausência depende de outra coluna observada.",
         "prompt": "A ausência de visitas_registradas depende de status_conta ou de trimestre? Mostre a tabela e o código."},
        {"acao": "Escreva uma frase dizendo de que coluna a ausência depende.",
         "detalhe": "A frase vai para a skill de limpeza do grupo, na Prática 4."},
    ],
    "O grupo sabe de que coluna a ausência depende.",
    ambiente="Gemini",
))

# 16. MCAR, MAR e MNAR
SLIDES.append(conteudo(
    "O engajamento ausente segue o mecanismo MAR: a ausência depende do segmento",
    '        <table class="tabela-criterios">\n'
    "          <thead><tr><th>Mecanismo</th><th>Do que a ausência depende</th>"
    "<th>Consequência</th></tr></thead>\n"
    "          <tbody>\n"
    '            <tr class="fragment"><td>MCAR, completamente ao acaso</td>'
    "<td>De nada registrado na base</td>"
    "<td>Excluir preserva a média e reduz a amostra</td></tr>\n"
    '            <tr class="decisiva fragment"><td>MAR, ao acaso dado o observado</td>'
    "<td>De coluna observada, o segmento</td>"
    '<td class="vence">Excluir enviesa a média; condicionar ao segmento corrige</td></tr>\n'
    '            <tr class="fragment"><td>MNAR, não ao acaso</td>'
    "<td>De informação fora da base</td>"
    "<td>Nenhuma correção com as colunas disponíveis</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    sobrelinha="Taxonomia de Rubin, 1976",
    conclusao="A escolha do tratamento depende do mecanismo, e o segmento é coluna presente no painel.",
    por_passos=True,
    fonte="Fonte: painel Kovan. Rubin, Biometrika, 1976.",
))

# 17. Divisor: a decisao de tratamento
SLIDES.append(secao(
    "Bloco 3 de 4",
    "A decisão de tratamento",
    "Três alternativas, o que cada uma assume sobre a lacuna e como se mede o que ela custa.",
    ["O que a lacuna representa", "Qual indicador ela move", "Quanto ela move"],
))

# 18. Excluir, imputar, sinalizar
SLIDES.append(conteudo(
    "Excluir, imputar e sinalizar assumem coisas diferentes sobre o que a lacuna representa",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card fragment"><h3>Excluir</h3>'
    "<p>Assume que a linha ausente não carrega informação sobre o fenômeno medido.</p>"
    '<p class="fonte-nota">Custo: a amostra encolhe, e o viés entra quando a ausência depende do segmento</p></div>\n'
    '          <div class="concept-card fragment"><h3>Imputar</h3>'
    "<p>Assume um valor para a lacuna e passa a tratar esse valor como observado.</p>"
    '<p class="fonte-nota">Custo: zero, mediana da conta e média do segmento produzem três séries distintas</p></div>\n'
    '          <div class="concept-card fragment"><h3>Sinalizar</h3>'
    "<p>Mantém a linha e acrescenta uma coluna que marca o registro como ausente.</p>"
    '<p class="fonte-nota">Custo: a coluna nova precisa entrar em toda análise seguinte</p></div>\n'
    "        </div>\n",
    contexto="As três alternativas são defensáveis, e nenhuma delas devolve a informação que o sistema não registrou.",
    conclusao="A escolha entre as três precisa estar escrita ao lado do número que ela produziu, com o custo medido junto.",
    por_passos=True,
))

# 19. Como se mede o custo de uma decisao
SLIDES.append(conteudo(
    "O custo de uma decisão de tratamento se mede recalculando o indicador sob cada alternativa",
    '        <div class="concept-cards quatro">\n'
    '          <div class="concept-card"><h3>01 Escolher o indicador</h3>'
    "<p>O número que vai para a recomendação, com o recorte declarado.</p></div>\n"
    '          <div class="concept-card"><h3>02 Recalcular</h3>'
    "<p>O mesmo código, trocando apenas a linha que aplica o tratamento.</p></div>\n"
    '          <div class="concept-card"><h3>03 Registrar a diferença</h3>'
    "<p>Em ponto percentual, em contagem de eventos ou em posição no ranking.</p></div>\n"
    '          <div class="concept-card"><h3>04 Declarar a escolha</h3>'
    "<p>Qual alternativa entra no entregável, e o que ela assume sobre a lacuna.</p></div>\n"
    "        </div>\n",
    contexto="A diferença medida é o custo. Argumento sobre qual tratamento é melhor, sem o recálculo, fica fora do registro.",
    conclusao="A Prática 3 aplica os quatro passos às visitas médias por segmento, com metade da sala em cada alternativa.",
))

# 20. Pratica 3, o confronto
SLIDES.append(pratica(
    3, "O custo da decisão de tratamento", 30,
    "Trios, metade da sala em cada tratamento",
    "Visitas médias por segmento, nos três segmentos",
    "Os dois quadros no projetor, lado a lado",
    [
        {"acao": "Mesas 1 e 2: preencher a ausência de visitas com zero",
         "prompt": "Trate visitas_registradas ausente como 0 e calcule a média por segmento. Mostre o código."},
        {"acao": "Mesas 3 e 4: excluir as linhas sem registro de visita",
         "prompt": "Descarte as linhas em que visitas_registradas está ausente e calcule a média por segmento. Mostre o código."},
        {"acao": "Escrever os três números no quadro da sua metade",
         "detalhe": "Cauda, Médio e Estratégico, com duas casas decimais."},
        {"acao": "Defender a leitura para a outra metade",
         "detalhe": "Qual recomendação sobre cobertura comercial o seu número sustenta?"},
    ],
    "Cada metade consegue dizer qual decisão de tratamento produziu o seu número.",
    ambiente="Gemini",
))

# 21. Figura: a inversao dos segmentos
SLIDES.append(figura(
    "O tratamento da lacuna leva o segmento estratégico da maior à menor média de visitas",
    "aula02-inversao-segmentos.png",
    "Dois painéis com as visitas médias por segmento sob cada tratamento da lacuna, e a ordem dos segmentos destacada",
    conclusao="O que decide entre as duas leituras é o mecanismo de ausência medido na Prática 2.",
))

# 22. Quiz 2
SLIDES.append(quiz(
    "Verificação &middot; questão 2",
    "As duas ordens",
    "As duas mesas mediram visitas por segmento na mesma base. Por que as ordens divergiram?",
    [
        {"texto": "O Gemini devolveu médias diferentes no mesmo pedido", "certa": False,
         "certo": "Correto.",
         "errado": "O modelo escreveu o código, e quem rodou foi cada mesa, sobre o mesmo arquivo."},
        {"texto": "Uma das mesas rodou o cálculo num recorte menor", "certa": False,
         "certo": "Correto.",
         "errado": "As duas rodaram sobre os 14 trimestres, sem filtro de janela."},
        {"texto": "Cada mesa tratou de um jeito a linha sem visita", "certa": True,
         "certo": "Com a ausência valendo zero, o estratégico tem a maior média dos três. Excluindo as linhas ausentes, tem a menor.",
         "errado": "Pense no que cada mesa fez com as 8.280 linhas em que a visita não está registrada."},
        {"texto": "A base mudou entre a execução de uma mesa e a outra", "certa": False,
         "certo": "Correto.",
         "errado": "O arquivo é o mesmo, carregado da mesma URL no começo da tarde."},
    ],
    {"fichas": [
        ("O arquivo", "o mesmo nas duas mesas"),
        ("O que divergiu", '<span class="numerao">a ordem</span>'),
        ("A coluna", "visitas_registradas"),
    ]},
))

# 23. Divisor: registrar a decisao
SLIDES.append(secao(
    "Bloco 4 de 4",
    "Registrar a decisão",
    "O arquivo que outra pessoa executa na semana que vem e obtém o mesmo número.",
    ["O que foi feito", "Por que foi feito", "Que número saiu"],
))

# 24. O criterio que separa os dois ambientes
SLIDES.append(conteudo(
    "Cinco critérios separam os dois ambientes, e o entregável exige reexecução por terceiro",
    '        <table class="tabela-criterios">\n'
    "          <thead><tr><th>Critério</th><th>Gemini</th><th>Antigravity</th></tr></thead>\n"
    "          <tbody>\n"
    '            <tr class="fragment"><td>Unidade de trabalho</td>'
    "<td>Mensagem numa conversa</td><td>Arquivo numa pasta</td></tr>\n"
    '            <tr class="fragment"><td>Instalação</td>'
    '<td class="vence">Nenhuma</td><td>Aplicativo desktop com login</td></tr>\n'
    '            <tr class="fragment"><td>Ciclo de resposta</td>'
    '<td class="vence">Segundos</td><td>Minutos, com plano e execução</td></tr>\n'
    '            <tr class="fragment"><td>O que sobra ao fechar</td>'
    '<td>Histórico de conversa</td><td class="vence">Script, base tratada e log</td></tr>\n'
    '            <tr class="decisiva fragment"><td>Reexecutável por terceiro</td>'
    '<td>Ausente</td><td class="vence">Disponível</td></tr>\n'
    "          </tbody>\n"
    "        </table>\n",
    conclusao="O critério é a persistência do trabalho, e a skill em Markdown carrega a última linha entre os dois.",
    por_passos=True,
))

# 25. Anatomia da skill em Markdown
SLIDES.append(conteudo(
    "A skill de limpeza registra, para cada advertência, a decisão tomada e o custo medido",
    '        <div class="side-by-side">\n'
    "          <div>\n"
    '            <pre class="code-compact"><code># Skill: limpeza do painel Kovan\n'
    "## Entrada\n"
    "kovan_painel_contas.csv, 16.618 linhas\n"
    "## Decisões, uma por advertência\n"
    "- receita_brl ausente, 160 linhas\n"
    "    tratamento:\n"
    "    custo medido:\n"
    "- visitas_registradas, 8.280 linhas\n"
    "- taxonomia_mix, quebra em 2023Q1\n"
    "- devolucoes_brl, sinal negativo\n"
    "## Saída\n"
    "base tratada e tabela de custos</code></pre>\n"
    "          </div>\n"
    "          <div>\n"
    '            <p class="sobrelinha">Três seções obrigatórias</p>\n'
    "            <p><strong>Entrada</strong> nomeia o arquivo e a contagem de linhas que o agente deve encontrar.</p>\n"
    "            <p><strong>Decisões</strong> traz uma linha por advertência, com o tratamento e o número que ele produziu.</p>\n"
    "            <p><strong>Saída</strong> declara o que a execução precisa deixar em disco.</p>\n"
    '            <p class="fonte-nota">Markdown puro: entra nos dois ambientes.</p>\n'
    "          </div>\n"
    "        </div>\n",
    conclusao="A omissão de uma advertência equivale a manter o dado como veio.",
))

# 26. Pratica 4
SLIDES.append(pratica(
    4, "A skill de limpeza do grupo", 30,
    "Em grupo, um arquivo por grupo",
    "A skill preenchida, com as quatro decisões e o custo medido de cada uma",
    "Aos 20 minutos, conferir o número contra o da Prática 3",
    [
        {"acao": "Abra o esqueleto e preencha uma linha por advertência.",
         "detalhe": "Receita ausente, engajamento ausente, quebra de taxonomia e sinal das devoluções."},
        {"acao": "Escreva o custo medido ao lado de cada decisão.",
         "detalhe": "Número, unidade e o recorte sobre o qual foi medido."},
        {"acao": "Cole o arquivo inteiro na conversa e rode contra a base crua.",
         "prompt": "Siga este arquivo passo a passo sobre o CSV anexado. Devolva o código e a tabela de custos."},
        {"acao": "Confira as visitas médias por segmento contra as da Prática 3.",
         "detalhe": "Divergência indica que a skill descreve um tratamento diferente do que o grupo aplicou."},
    ],
    "A skill executada por quem não a escreveu devolve os mesmos números que o grupo apresentou na Prática 3.",
    ambiente="Gemini",
))

# 27. Amarracao
SLIDES.append(conteudo(
    "A base tratada de hoje sustenta a análise bivariada da Aula 03 e o Artefato 1",
    '        <div class="linha-tempo">\n'
    '          <div class="etapa fragment"><p class="quando">15/08 &middot; hoje</p><h3>Fica pronto</h3>'
    "<p>Base tratada, o custo das quatro decisões e a skill em Markdown que reproduz os dois.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">22/08 &middot; Aula 03</p><h3>Análise univariada e bivariada</h3>'
    "<p>Distribuições, relações entre colunas e o rótulo de erosão em três cortes de limiar, sobre a base tratada hoje.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">Aula 04</p><h3>Visualização para decidir</h3>'
    "<p>Os quadros que vão ao Comitê saem dos números que a skill do grupo reproduz.</p></div>\n"
    '          <div class="etapa avaliada fragment"><p class="quando">Semana 5 &middot; 05/09</p><h3>Artefato 1</h3>'
    "<p>Análise Exploratória de Dados, com o registro de tratamento anexado.</p></div>\n"
    "        </div>\n",
    conclusao="A Aula 03 recebe a base com as decisões escritas, de modo que uma divergência de número entre grupos passa a ter onde ser localizada.",
    por_passos=True,
))

# 28. Referencias
SLIDES.append(conteudo(
    "Referências e nota metodológica",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>Caso e dados</h3>'
    "<p>1. Kovan Technologies LATAM: A Definição do Alvo. Business case PL-02-2026, versão v2. "
    "As quatro advertências de qualidade estão no Exhibit 3.</p></div>\n"
    '          <div class="concept-card"><h3>Método</h3>'
    "<p>2. Rubin. Inference and missing data, Biometrika, 1976. &nbsp; 3. Little e Rubin. "
    "Statistical Analysis with Missing Data, Wiley, 2019.</p>"
    "<p>4. Wirth e Hipp. CRISP-DM, 2000. &nbsp; 5. Tukey. Exploratory Data Analysis, 1977.</p></div>\n"
    '          <div class="concept-card"><h3>Decisões do módulo</h3>'
    "<p>6. ADR-003: Gemini como ambiente das práticas, Antigravity como demonstração.</p>"
    "<p>7. ADR-004: a skill de agente em Markdown como artefato do aluno.</p></div>\n"
    "        </div>\n",
    conclusao="As seis dimensões de qualidade foram organizadas neste módulo a partir da literatura de data quality, sem seguir um padrão publicado. "
              "Cada número citado hoje é reproduzível por dados/tests/test_aula02_numeros.py.",
    rotulo_conclusao="Nota metodológica",
    conclusao_clara=True,
))

# 29. Encerramento
SLIDES.append(
    '      <section class="end-slide">\n'
    '        <div class="accent-bar"></div>\n'
    '        <p class="secao-numero">Módulo 2 &middot; Aula 02 &middot; encerramento</p>\n'
    "        <h1>Próximo encontro: 22/08</h1>\n"
    "        <h3>Prof. José Romualdo da Costa Filho &middot; MBA em IA e Dados para Negócios</h3>\n"
    "      </section>\n"
)


ESQUELETO = """<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aula 02 &middot; O dado sujo é o case &middot; MBA Inteli x Lenovo</title>

  <!-- Gerado por tools/montar_deck_aula02.py. Nao editar a mao: a numeracao de
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
