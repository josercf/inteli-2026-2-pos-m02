# -*- coding: utf-8 -*-
"""
Monta aulas/aula01.html.

O deck passou a ser gerado, e nao editado a mao, depois da revisao de
diagramacao. Duas razoes concretas, as duas por defeito observado:

1. A numeracao de rodape era mantida na unha. Ao inserir sete slides no meio do
   deck, ela saiu errada; ao corrigir o slide de referencias, uma substituicao
   comeu um `</section>` e o Reveal juntou dois slides sem nenhum erro aparecer.
   Aqui a numeracao e o fechamento de secao sao garantidos por construcao.

2. A estrutura de faixas (sobrelinha, titulo, corpo, faixa de conclusao, fonte)
   so vale se for igual em todo slide. Como funcao, ela e igual; como HTML
   repetido 32 vezes, ela diverge.

Convencao de titulo, fixada na revisao:

- Slide de conteudo leva titulo afirmativo: declara o achado que a exposicao
  prova. Sem metafora, sem pergunta retorica, sem inversao.
- Slide de pratica, de quiz e divisor NAO leva titulo afirmativo. Num quiz, o
  titulo afirmativo entrega o gabarito. Nesses, a funcao vai na sobrelinha e o
  h2 nomeia a tarefa ou o objeto.

Uso: python3 tools/montar_deck_aula01.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from tools import deck_kit  # noqa: E402
from tools.deck_kit import conteudo, figura, figura_embutida, pratica, quiz, secao  # noqa: E402

SAIDA = RAIZ / "aulas" / "aula01.html"

deck_kit.configurar("Módulo 2 &middot; Aula 01")
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
    "            <h1>Da hipótese à evidência</h1>\n"
    "            <h3>Análise exploratória assistida por IA e definição do alvo de um modelo de churn</h3>\n"
    '            <p class="cover-meta">Módulo 2 &middot; Aula 01 &middot; Trilha de Tecnologia</p>\n'
    '            <p class="cover-meta">08 de agosto de 2026 &middot; 14h00 às 17h30</p>\n'
    "          </div>\n"
    "        </div>\n"
    "      </section>\n"
)

# 2. Programacao
SLIDES.append(conteudo(
    "Sequência da tarde, das 14h00 às 17h30",
    '        <div class="linha-tempo">\n'
    '          <div class="etapa"><p class="quando">14h00 &middot; 30 min</p><h3>Regra de evidência</h3>'
    "<p>O que separa a IA que descreve o dado da que escreve o código que o mede.</p></div>\n"
    '          <div class="etapa"><p class="quando">14h30 &middot; 55 min</p><h3>Especificação de prompt</h3>'
    "<p>Quatro níveis sobre a mesma pergunta de negócio, e o que falha em cada ausência.</p></div>\n"
    '          <div class="etapa"><p class="quando">15h45 &middot; 45 min</p><h3>Teste falseável</h3>'
    "<p>Variável, operação, janela e critério de refutação. O caderno de hipóteses do grupo.</p></div>\n"
    '          <div class="etapa avaliada"><p class="quando">16h30 &middot; 60 min</p><h3>Definição do alvo</h3>'
    "<p>O rótulo do Caminho A construído e contado sobre o painel.</p></div>\n"
    "        </div>\n",
    contexto="Quatro blocos, duas práticas em Colab e três verificações. Cada bloco fecha com um registro no caderno do grupo.",
    conclusao="Intervalo das 15h25 às 15h45. O caderno de hipóteses é a entrega de hoje.",
    rotulo_conclusao="Entrega",
))

# 3. Resgate da manha
SLIDES.append(conteudo(
    "A manhã produziu hipóteses; o painel não contém a variável que as testaria",
    '        <div class="stat-tiles">\n'
    '          <div class="stat-tile"><p class="stat-numero">16.618</p><p class="stat-rotulo">linhas no painel de contas</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">20</p><p class="stat-rotulo">colunas disponíveis</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">0</p><p class="stat-rotulo">colunas de risco, propensão ou churn</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">3h30</p><p class="stat-rotulo">até o fechamento</p></div>\n'
    "        </div>\n"
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>Produzido pela manhã</h3>'
    "<p>Backlog de hipóteses e posição preliminar sobre Caminho A ou B.</p></div>\n"
    '          <div class="concept-card"><h3>Ausente no dado</h3>'
    "<p>Nenhuma coluna de risco. Sem custo, nenhuma margem derivável.</p></div>\n"
    '          <div class="concept-card"><h3>Exigido até 17h30</h3>'
    "<p>Cada hipótese com número, célula de origem e veredito.</p></div>\n"
    "        </div>\n",
    conclusao="A hipótese formulada em linguagem de negócio precisa virar coluna, operação e corte antes de qualquer código.",
    fonte="Fonte: painel analítico de contas, Exhibit 3 do Caderno Kovan PL-02-2026 v2.",
))

# 4. Divisor: criterio de aceitacao
SLIDES.append(secao(
    "Bloco 1 de 4",
    "Critério de aceitação de evidência",
    "Todo número registrado no caderno vem de código executado sobre o painel, e o código fica disponível para leitura.",
    ["O número existe numa célula", "A célula é reexecutável", "O código pode ser contestado"],
))

# 5. Duas maquinas
SLIDES.append(conteudo(
    "A IA que descreve devolve número sem origem; a que escreve código devolve número auditável",
    '        <table class="tabela-criterios">\n'
    "          <thead><tr><th>Dimensão</th><th>Descrever o dado</th><th>Escrever o código que mede</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Origem do número</td><td>amostra do arquivo, completada por plausibilidade</td>"
    '<td class="vence">execução sobre as 16.618 linhas</td></tr>\n'
    "            <tr><td>O que volta</td><td>um valor</td>"
    '<td class="vence">um valor e o código que o produziu</td></tr>\n'
    '            <tr class="decisiva"><td>Rastreabilidade</td><td>nenhuma</td>'
    '<td class="vence">célula reexecutável</td></tr>\n'
    "            <tr><td>Modo de falha</td><td>número plausível para coluna inexistente</td>"
    '<td class="vence">erro de lógica visível no código</td></tr>\n'
    "          </tbody>\n"
    "        </table>\n",
    conclusao="As duas respondem em segundos. Só uma pode ser contestada por quem recebe o número.",
))

# 5b. Por que a IA erra em tabela: mecanismo, e nao opiniao
SLIDES.append(conteudo(
    "O erro em tabela vem da arquitetura, não da falta de capacidade do modelo",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card fragment"><h3>Tokenização linear</h3>'
    "<p>A tabela entra como sequência de texto. A relação entre linha e coluna não sobrevive à serialização.</p>"
    '<p class="fonte-nota">O erro cresce com o número de colunas</p></div>\n'
    '          <div class="concept-card fragment"><h3>Janela de contexto</h3>'
    "<p>16.618 linhas não cabem no contexto. O modelo lê uma amostra e responde sobre o arquivo inteiro.</p>"
    '<p class="fonte-nota">A resposta não distingue o que ele leu do que completou</p></div>\n'
    '          <div class="concept-card fragment"><h3>Cálculo implícito</h3>'
    "<p>Somar dezesseis mil valores por previsão do próximo token não é uma operação aritmética.</p>"
    '<p class="fonte-nota">A saída tem a forma de um cálculo e não passou por um</p></div>\n'
    "        </div>\n",
    conclusao="Nenhum dos três se resolve com um modelo maior. A saída é separar leitura de computação.",
    por_passos=True,
    fonte="Fontes: The Structural Challenge, 2026; TaCube, EMNLP 2022.",
))

# 5c. Os numeros do benchmark
SLIDES.append(conteudo(
    "Nenhum modelo isolado atinge erro baixo o bastante para uso não supervisionado",
    '        <div class="stat-tiles">\n'
    '          <div class="stat-tile"><p class="stat-numero">82,4%</p><p class="stat-rotulo">melhor modelo em planilhas financeiras, cerca de 1 erro a cada 6 perguntas</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">48,6%</p><p class="stat-rotulo">média de todos os modelos na maior planilha do benchmark</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">29%</p><p class="stat-rotulo">acerto exato pedindo a resposta direto ao modelo</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">58%</p><p class="stat-rotulo">acerto exato pedindo que ele gere e execute o código</p></div>\n'
    "        </div>\n"
    '        <div class="side-by-side">\n'
    "          <div>\n"
    '            <p class="sobrelinha">Os dois primeiros</p>\n'
    "            <p>A queda acompanha o tamanho da planilha e é consistente entre dez configurações "
    "de três fornecedores. É limite de arquitetura, não fraqueza de um modelo.</p>\n"
    "          </div>\n"
    "          <div>\n"
    '            <p class="sobrelinha">Os dois últimos</p>\n'
    "            <p>A mesma pergunta, ao mesmo modelo, dobra de acerto quando muda de pedir o número "
    "para pedir o código. Sem os erros de escala, chega a 80%.</p>\n"
    "          </div>\n"
    "        </div>\n",
    conclusao="Dobrar o acerto não exigiu trocar de modelo. Exigiu trocar o que se pede a ele.",
    fonte="Fontes: FinSheet-Bench, arXiv 2026 (24 arquivos, 10 configurações de modelo); Pándy, Lakatos e Hajdu, IEEE INES 2025.",
))

# 6. CRISP-DM
SLIDES.append(figura_embutida(
    "As fases 1 e 2 do CRISP-DM consomem 6 das 26 semanas do projeto",
    "aula01-crisp-dm.svg",
    conclusao="As duas primeiras fases não são preâmbulo do projeto: são 23% da janela que a Kovan tem para entregar o modelo.",
    fonte="Fonte: cronograma do projeto Kovan, 26 semanas, Exhibit 5. CRISP-DM conforme Wirth e Hipp (2000).",
))

# 7. Custo por etapa
SLIDES.append(conteudo(
    "A IA reduziu o custo de executar, não o de decidir o que medir",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>1. Pergunta</h3><p>Decidir o que medir e sobre qual recorte.</p>'
    '<p class="fonte-nota">Permanece com o analista</p></div>\n'
    '          <div class="concept-card"><h3>2. Recorte e medida</h3><p>Escrever o código e executá-lo sobre a base inteira.</p>'
    '<p class="fonte-nota">Transferido à ferramenta</p></div>\n'
    '          <div class="concept-card"><h3>3. Refutação</h3><p>Decidir se o número derruba a hipótese.</p>'
    '<p class="fonte-nota">Permanece com o analista</p></div>\n'
    "        </div>\n",
    contexto="De três etapas, uma foi automatizada. O gargalo saiu da execução e foi para a formulação.",
    conclusao="Pergunta mal formulada agora é respondida rápido e errado, e chega com a mesma aparência de uma resposta boa.",
))

# 8. Ciclo de EDA assistida
SLIDES.append(figura_embutida(
    "Quatro dos seis passos da EDA assistida permanecem com o analista",
    "aula01-ciclo-eda-ia.svg",
    conclusao="Decidir o que medir e decidir se o número derruba a hipótese não são delegáveis.",
))

# 9. Pratica 1
SLIDES.append(pratica(
    1, "Pedido sem estrutura sobre o painel Kovan", 20,
    "Individual, no notebook da aula",
    "O número que a IA devolveu e a coluna de origem dele, ou a constatação de que ela não existe",
    "Aos 12 minutos, colheita em voz alta",
    [
        {"acao": "Abra o notebook no Colab e rode a célula que carrega o painel.",
         "detalhe": "1.187 contas por 14 trimestres."},
        {"acao": "Peça uma análise sem nenhuma estrutura.",
         "prompt": "analise este arquivo e diga o que há de interessante"},
        {"acao": "Agora peça um número que o painel não tem.",
         "prompt": "qual a margem média por conta no segmento estratégico?"},
        {"acao": "Se recebeu um número, encontre a coluna de onde ele saiu.",
         "detalhe": "Se não encontrar, anote isso: é o resultado da prática."},
    ],
    "Você consegue apontar a célula que produziu o número, ou provar que ela não existe."
))

# 10. Regra de ouro
SLIDES.append(secao(
    "Regra da casa",
    "Todo número apresentado precisa ter uma célula de origem",
    "Sem a célula, o número não foi verificado. Foi apenas recebido.",
    ["Qual célula produziu este número?", "Quais colunas ela leu?", "Que filtro estava aplicado?"],
))

# 11. Quiz 1
SLIDES.append(quiz(
    "Verificação &middot; questão 1",
    "Margem média em painel sem coluna de margem",
    "Você pediu a margem média por conta e recebeu R$ 412 mil. O que aconteceu?",
    [
        {"texto": "Ele derivou a margem a partir de receita e do desconto médio", "certa": False,
         "certo": "Correto.",
         "errado": "Não existe: nenhuma combinação das 20 colunas produz margem sem dado de custo."},
        {"texto": "Ele completou um número plausível, sem origem em coluna", "certa": True,
         "certo": "O modelo completou por plausibilidade. Ele não distingue lembrar de calcular: o número tem a forma certa e origem nenhuma.",
         "errado": "Reveja: o painel não traz custo nem margem em nenhuma das 20 colunas."},
        {"texto": "Ele leu um arquivo diferente daquele que foi carregado", "certa": False,
         "certo": "Correto.",
         "errado": "O painel foi carregado por inteiro na célula anterior."},
        {"texto": "Foi erro de cálculo, e some quando se pede novamente", "certa": False,
         "certo": "Correto.",
         "errado": "Um erro de cálculo pressupõe que houve cálculo. Não houve."},
    ],
    {"fichas": [
        ("Você pediu", "margem média por conta"),
        ("Você recebeu", '<span class="numerao">R$ 412 mil</span>'),
        ("O painel tem", "20 colunas, nenhuma de custo nem de margem"),
    ]},
))

# 12. Divisor: niveis de prompt
SLIDES.append(secao(
    "Bloco 2 de 4",
    "Níveis de especificação de prompt",
    "A mesma pergunta de negócio em quatro formulações, e o que muda no que volta.",
))

# 13. Os quatro niveis
SLIDES.append(conteudo(
    "Cada nível acrescenta uma restrição e reduz o espaço de resposta do modelo",
    '        <div class="concept-cards quatro">\n'
    '          <div class="concept-card fragment"><h3>Nível 0</h3><p>Sem estrutura. Pedido em linguagem natural, sem recorte.</p>'
    '<p class="fonte-nota">Volta: resumo de colunas e três observações genéricas</p></div>\n'
    '          <div class="concept-card fragment"><h3>Nível 1</h3><p>CREATE: papel, pedido, exemplos, ajustes, formato e extras.</p>'
    '<p class="fonte-nota">Volta: prosa estruturada, ainda sem recorte</p></div>\n'
    '          <div class="concept-card fragment"><h3>Nível 2</h3><p>Estrutura na entrada e na saída: colunas, recorte e formato da tabela.</p>'
    '<p class="fonte-nota">Volta: código pandas, faixas de variação por conta</p></div>\n'
    '          <div class="concept-card fragment"><h3>Nível 3</h3><p>Postura adversarial: o que refutaria o achado.</p>'
    '<p class="fonte-nota">Volta: o código e as explicações que o derrubam</p></div>\n'
    "        </div>\n",
    sobrelinha="Pergunta de negócio: a queda de receita é uniforme na carteira?",
    conclusao="O nível 2 é o piso para qualquer pedido que precise produzir um número.",
    por_passos=True,
))

# 14. Nivel 0 contra nivel 2
SLIDES.append(conteudo(
    "O nível 0 devolve descrição; o nível 2 devolve o código que produz o número",
    '        <div class="par-prompt">\n'
    "          <div>\n"
    "            <h3>Nível 0</h3>\n"
    '            <pre class="code-compact"><code>analise este arquivo e diga\no que há de interessante</code></pre>\n'
    "            <p>Volta um resumo de colunas e três observações genéricas. Descrição não é análise.</p>\n"
    "          </div>\n"
    "          <div>\n"
    "            <h3>Nível 2</h3>\n"
    '            <pre class="code-compact"><code><span class="hl-persona">Você é analista de revenue\nanalytics da Kovan LATAM.</span>\n'
    '<span class="hl-dados">Use o DataFrame `painel`, colunas:\nconta_id, trimestre, segmento,\nreceita_brl, status_conta.</span>\n'
    '<span class="hl-formato">Devolva o código pandas que compara\n2025 contra 2024 no segmento\nestratégico, por conta, em faixas\nde variação.</span>\n'
    '<span class="hl-restricao">Se faltar informação, diga que\nfalta. Não estime.</span></code></pre>\n'
    "          </div>\n"
    "        </div>\n"
    '        <div class="hl-legenda">\n'
    '          <span class="lg-persona">papel</span>\n'
    '          <span class="lg-dados">dados disponíveis</span>\n'
    '          <span class="lg-formato">recorte e formato de saída</span>\n'
    '          <span class="lg-restricao">restrição contra estimativa</span>\n'
    "        </div>\n",
    conclusao="O recorte que produz o número foi decisão sua, e está escrito onde qualquer um pode discordar dele.",
))

# 15. Estrutura na entrada e na saida
SLIDES.append(figura(
    "A ausência de cada elemento produz um modo de falha próprio",
    "aula01-structure-in-out.svg",
    "Os cinco elementos de um prompt de análise e o modo de falha associado a cada ausência",
    conclusao="Nenhuma dessas falhas chega com cara de erro. Todas chegam com cara de resposta boa.",
))

# 16. A restricao que so vale para dado
SLIDES.append(conteudo(
    "Completar a lacuna é serviço em texto e é defeito em análise",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>01 Schema</h3>'
    '<p class="fonte-nota">Use apenas colunas que existem no DataFrame `painel`.</p>'
    "<p>Bloqueia: coluna que não existe.</p></div>\n"
    '          <div class="concept-card"><h3>02 Restrição</h3>'
    '<p class="fonte-nota">Se faltar informação para responder, diga que falta, em vez de estimar.</p>'
    "<p>Bloqueia: número plausível sem origem.</p></div>\n"
    '          <div class="concept-card"><h3>03 Formato</h3>'
    '<p class="fonte-nota">Devolva o código, não o resultado.</p>'
    "<p>Bloqueia: resultado sem célula que o produza.</p></div>\n"
    "        </div>\n",
    contexto="Em texto, preencher a lacuna é o serviço contratado. Em análise, é o defeito.",
    conclusao="As três cláusulas entram em todo prompt de análise a partir de agora.",
))

# 17. Pratica 2
SLIDES.append(pratica(
    2, "Concentração da queda no segmento estratégico", 20,
    "Em duplas, uma tela por dupla",
    "Um recorte numérico e três explicações alternativas, cada uma com a coluna que a testaria",
    "Aos 14 minutos, comparar o recorte com a mesa ao lado",
    [
        {"acao": "Escreva o prompt de nível 2 para a pergunta do bloco.",
         "detalhe": "A queda de receita do segmento estratégico está concentrada ou é uniforme?"},
        {"acao": "Peça o código, não o número. Rode no notebook.",
         "detalhe": "O número sai da execução."},
        {"acao": "Suba para o nível 3.",
         "prompt": "liste três explicações alternativas para este padrão e a coluna que testaria cada uma"},
        {"acao": "Compare o seu recorte com o da mesa ao lado.",
         "detalhe": "Se os números divergirem, o que mudou não foi o dado."},
    ],
    "O recorte está escrito no prompt, e o número saiu de uma célula que você rodou."
))

# 18. Intervalo
SLIDES.append(secao(
    "Intervalo",
    "15h25 às 15h45",
    "Na volta: anatomia do teste falseável, árvore de hipóteses e o caderno do grupo.",
))

# 19. Anatomia do teste falseavel
SLIDES.append(conteudo(
    "Uma hipótese só é testável se especifica variável, operação, janela e critério de refutação",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card fragment"><h3>Variável</h3><p>Qual coluna do painel carrega o sinal.</p>'
    '<p class="fonte-nota">receita_brl, linhas_produto_ativas</p></div>\n'
    '          <div class="concept-card fragment"><h3>Operação</h3><p>O que se calcula sobre ela, e sobre quais grupos.</p>'
    '<p class="fonte-nota">mediana por segmento, dois grupos</p></div>\n'
    '          <div class="concept-card fragment"><h3>Janela</h3><p>Quais trimestres entram, e por que os outros ficam de fora.</p>'
    '<p class="fonte-nota">2023Q2 a 2025Q4, onze trimestres</p></div>\n'
    "        </div>\n",
    conclusao="Critério de refutação: qual resultado derruba a hipótese, escrito antes de rodar. Sem esta linha, a análise vira busca por confirmação.",
    por_passos=True,
    rotulo_conclusao="O quarto",
))

# 20. Arvore de hipoteses
SLIDES.append(figura(
    "Só o componente de contração gera hipóteses testáveis nesta base",
    "aula01-arvore-hipoteses.svg",
    "Árvore que decompõe a queda do NRR em três componentes mutuamente exclusivos e quatro hipóteses testáveis",
    conclusao="Cada folha nasce de um ramo do indicador e nomeia a coluna que a testa.",
    fonte="Fonte: decomposição do NRR do segmento estratégico, Exhibit 2 do Caderno Kovan.",
))

# 21. O que o painel nao permite testar
SLIDES.append(conteudo(
    "Rentabilidade, engajamento e efeito de intervenção não são testáveis com estas 20 colunas",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card fragment"><h3>Rentabilidade</h3><p>Não há custo nem margem. Nenhuma hipótese sobre lucro por conta é testável.</p>'
    '<p class="fonte-nota">coluna ausente: custo, margem</p></div>\n'
    '          <div class="concept-card fragment"><h3>Engajamento completo</h3><p>Visitas e interações existem para parte da base, e a cobertura não é uniforme entre segmentos.</p>'
    '<p class="fonte-nota">cobertura parcial: visitas_registradas</p></div>\n'
    '          <div class="concept-card fragment"><h3>Efeito da intervenção</h3><p>Não há registro de quem recebeu plano de intervenção.</p>'
    '<p class="fonte-nota">coluna ausente: plano_intervencao</p></div>\n'
    "        </div>\n",
    conclusao="Insuficiente é um veredito legítimo e vai aparecer no caderno. Dizer que o dado não responde é resultado; inventar que responde é o que a Kovan já fez uma vez, com o Radar de Contas.",
    por_passos=True,
))

# 21b. Mecanismos de ausencia
SLIDES.append(conteudo(
    "A ausência tem mecanismo, e o mecanismo decide se dá para corrigir",
    '        <table class="tabela-criterios">\n'
    "          <thead><tr><th>Mecanismo</th><th>Onde aparece no painel</th><th>O que fazer</th></tr></thead>\n"
    "          <tbody>\n"
    '            <tr class="fragment"><td>Completamente ao acaso</td>'
    "<td>receita não registrada por atraso no fechamento contábil, cerca de 1% dos trimestres</td>"
    '<td class="vence">excluir a linha não enviesa, só perde potência</td></tr>\n'
    '            <tr class="fragment"><td>Ao acaso, dado o observado</td>'
    "<td>engajamento comercial ausente, e a cobertura é pior nas contas menores</td>"
    "<td>corrigível condicionando ao segmento, que está na base</td></tr>\n"
    '            <tr class="decisiva fragment"><td>Não ao acaso</td>'
    "<td>contas que compram por portal de procurement registram menos atividade comercial</td>"
    "<td>não corrigível com o que existe na base</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    conclusao="Taxonomia de Rubin. Tratar os três casos da mesma forma foi a decisão que separou a contagem das mesas.",
    por_passos=True,
    fonte="Fonte: advertências de qualidade do Exhibit 3. Taxonomia conforme Rubin, Inference and missing data, Biometrika, 1976.",
))

# 22. Pratica 3
SLIDES.append(pratica(
    3, "Caderno de hipóteses do grupo", 30,
    "Em grupo, um caderno por grupo",
    "Três hipóteses com as seis linhas preenchidas e veredito",
    "Aos 20 minutos, checar se algum veredito é Insuficiente",
    [
        {"acao": "Pegue três hipóteses do backlog que o grupo escreveu de manhã."},
        {"acao": "Preencha as seis linhas do registro para cada uma.",
         "prompt": "hipótese · variável · operação · janela · critério de refutação · veredito"},
        {"acao": "Em pelo menos uma, peça à IA que derrube o seu próprio achado.",
         "detalhe": "Antes de fechar o veredito, não depois."},
        {"acao": "Exporte o caderno.",
         "detalhe": "Entrega de hoje e matéria-prima do Artefato 1."},
    ],
    "As três hipóteses têm critério de refutação escrito antes de rodar, e ao menos um veredito não é Confirmada."
))

# 23. Quiz 2
SLIDES.append(quiz(
    "Verificação &middot; questão 2",
    "Hipótese pronta para virar código",
    "Qual destas hipóteses pode ser testada sobre o painel e pode perder?",
    [
        {"texto": "Clientes insatisfeitos com o atendimento deixam a Kovan mais cedo", "certa": False,
         "certo": "Correto.",
         "errado": "Não tem variável nem janela, e nenhum resultado a derrubaria."},
        {"texto": "A concorrência ficou mais agressiva nas contas que saíram em 2025 e 2024", "certa": False,
         "certo": "Correto.",
         "errado": "O painel não registra concorrência. Sem coluna, não há teste."},
        {"texto": "Existe no painel algum padrão capaz de explicar o churn das contas", "certa": False,
         "certo": "Correto.",
         "errado": "Confirma-se sempre: qualquer resultado cabe nela. Uma hipótese que não pode perder não informa nada."},
        {"texto": "Contas que estreitam o mix antes da receita rompem mais", "certa": True,
         "certo": "Tem variável, grupos comparados, janela declarada e um corte que decide. Dá para rodar e dá para perder.",
         "errado": "Volte e procure a que traz variável, janela e um número que decide."},
    ],
    {"fichas": [
        ("O painel oferece", "20 colunas, 14 trimestres"),
        ("As hipóteses", "vieram do backlog que os grupos escreveram de manhã"),
        ("A janela", "14 trimestres, de 2022Q3 a 2025Q4"),
    ]},
))

# 24. Divisor: definicao do alvo
SLIDES.append(secao(
    "Bloco 4 de 4",
    "Definição do alvo do modelo",
    "Nenhuma das 20 colunas do painel identifica quem está em risco. A decisão é o que o modelo deve prever.",
))

# 25. Dois alvos
SLIDES.append(conteudo(
    "O rótulo do Caminho A existe no sistema; o do Caminho B precisa ser construído",
    '        <div class="side-by-side">\n'
    "          <div>\n"
    '            <p class="sobrelinha">Caminho A &middot; Sinal de ruptura</p>\n'
    "            <p>Binário e verificável, derivável hoje à tarde.</p>\n"
    '            <code class="prompt-literal">pedidos == 0 em 2 trimestres consecutivos</code>\n'
    '            <p class="fonte-nota">A regra sai pronta do ERP. Não há o que negociar.</p>\n'
    "          </div>\n"
    "          <div>\n"
    '            <p class="sobrelinha">Caminho B &middot; Erosão silenciosa</p>\n'
    "            <p>Contínuo e construído. Alguém precisa decidir o que conta como contração relevante.</p>\n"
    '            <code class="prompt-literal">contração relevante = ?\n  queda de 10% em 2 trimestres\n  queda de 15% em 2 trimestres\n  queda de 25% em 2 trimestres</code>\n'
    '            <p class="fonte-nota">Cada corte constrói um modelo diferente.</p>\n'
    "          </div>\n"
    "        </div>\n",
    conclusao="Trocar o limiar do Caminho B muda a população-alvo antes do primeiro treinamento. A escolha do rótulo é decisão de negócio, não de modelagem.",
))

# 26. Cinco criterios
SLIDES.append(conteudo(
    "Nenhum dos dois caminhos vence nos cinco critérios",
    '        <table class="tabela-criterios">\n'
    "          <thead><tr><th>Critério</th><th>A pergunta que ele faz</th>"
    "<th>Caminho A &middot; ruptura</th><th>Caminho B &middot; erosão</th></tr></thead>\n"
    "          <tbody>\n"
    '            <tr class="fragment"><td>Observabilidade</td>'
            "<td>o rótulo existe no sistema?</td>"
    '<td class="vence">existe</td><td>precisa ser construído</td></tr>\n'
    '            <tr class="decisiva"><td>Prevalência</td><td>há eventos suficientes para treinar?</td>'
    '<td>34 eventos, 24 efetivos</td><td class="vence">176 episódios</td></tr>\n'
    '            <tr class="fragment"><td>Antecedência</td>'
            "<td>o sinal acende a tempo de agir?</td>"
    '<td>depois da decisão do cliente</td><td class="vence">com o relacionamento aberto</td></tr>\n'
    '            <tr class="fragment"><td>Acionabilidade</td>'
            "<td>a fila cabe na capacidade?</td>"
    '<td>6 a 10 por trimestre</td><td class="vence">120 a 190, teto de 138</td></tr>\n'
    '            <tr class="fragment"><td>Verificabilidade</td>'
            "<td>dá para auditar se acertou?</td>"
    '<td class="vence">direta</td><td>depende do limiar escolhido</td></tr>\n'
    "          </tbody>\n"
    "        </table>\n",
    contexto="O Caminho A vence em observabilidade e verificabilidade; o Caminho B, nos outros três.",
    conclusao="A decisão não é qual caminho é melhor, é qual critério a Kovan aceita perder.",
    por_passos=True,
    fonte="Fonte: Exhibits 2 a 5, Caderno Kovan PL-02-2026 v2. Os cinco critérios são construção deste módulo, não framework publicado.",
))

# 27. Talvera e Andira
SLIDES.append(figura(
    "A magnitude da queda não distingue a conta que retorna da que não retorna",
    "aula01-talvera-andira.gif",
    "Receita indexada de duas contas do segmento estratégico ao longo do episódio de contração",
    conclusao="As duas caíram e a que caiu mais foi a que voltou. Se a magnitude não separa, o que separa? É o conteúdo da Aula 03.",
    rotulo_conclusao="Em aberto",
    fonte="Fonte: painel analítico de contas, séries indexadas ao trimestre anterior ao episódio.",
))

# 27b. Quantos eventos decidem
SLIDES.append(figura(
    "Com 24 eventos, a validação não distingue um modelo bom de um ruim",
    "aula01-incerteza-auc.gif",
    "Curva da metade do intervalo de confiança de 95% do AUC contra o número de eventos positivos",
    conclusao="Ao fim de 26 semanas e R$ 1,842 milhão, a Kovan não saberia se o modelo funciona.",
    fonte="Fontes: Hanley e McNeil, Radiology, 1982. Minus et al., Journal of Clinical Epidemiology, 2025: o viés do AUC é dirigido pelo número de eventos, não pela taxa.",
))

# 28. Pratica 4
SLIDES.append(pratica(
    4, "Construção do rótulo do Caminho A", 30,
    "Em duplas na mesma mesa",
    "O número de rupturas do segmento estratégico, com o critério declarado",
    "Aos 20 minutos, comparar com a mesa ao lado",
    [
        {"acao": "Peça o rótulo à IA e leia o código que ela gerou.",
         "prompt": "crie uma coluna de churn neste dataset"},
        {"acao": "Identifique o critério que ela escolheu.",
         "detalhe": "Ela avisou que estava escolhendo?"},
        {"acao": "Construa o rótulo do Caminho A e conte as rupturas.",
         "detalhe": "Zero pedidos faturados em dois trimestres consecutivos, segmento estratégico."},
        {"acao": "Compare o número com a mesa ao lado.",
         "detalhe": "Se der diferente, o problema é de decisão, não de código."},
    ],
    "O número tem um critério declarado ao lado, e a divergência com a mesa vizinha está localizada."
))

# 29. Quiz 3
SLIDES.append(quiz(
    "Verificação &middot; questão 3",
    "Divergência entre contagens de ruptura",
    "Duas mesas contaram rupturas com o mesmo critério e chegaram a números diferentes. Qual a explicação mais provável?",
    [
        {"texto": "Uma das mesas carregou um arquivo diferente do painel oficial da Kovan", "certa": False,
         "certo": "Correto.",
         "errado": "O painel é o mesmo arquivo, carregado da mesma URL."},
        {"texto": "A IA alucinou o resultado da contagem em uma das duas mesas", "certa": False,
         "certo": "Correto.",
         "errado": "O modelo escreveu o código, mas quem rodou foi você, sobre a base inteira."},
        {"texto": "Cada mesa tratou de um jeito o trimestre sem receita", "certa": True,
         "certo": "Trimestre sem receita registrada não é trimestre sem compra. Excluir a linha e imputar o valor produzem séries diferentes, e a contagem muda junto.",
         "errado": "Pense no que cada mesa fez com as linhas em que a receita não está registrada."},
        {"texto": "É diferença de arredondamento e não altera a leitura", "certa": False,
         "certo": "Correto.",
         "errado": "Contagem de eventos raros não depende de arredondamento."},
    ],
    {"fichas": [
        ("As duas mesas", "rodaram o mesmo critério sobre o mesmo arquivo"),
        ("O painel tem", "14 trimestres e 20 colunas"),
        ("A diferença", "está numa decisão de tratamento, não no código"),
    ]},
))

# 30. Amarracao
SLIDES.append(conteudo(
    "Encadeamento entre a entrega de hoje, a Aula 02 e o Artefato 1",
    '        <div class="linha-tempo">\n'
    '          <div class="etapa fragment"><p class="quando">08/08 &middot; hoje</p><h3>Fica pronto</h3>'
    "<p>Caderno de hipóteses com veredito, painel carregado e conferido, e a contagem de rupturas do Caminho A.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">15/08 &middot; manhã</p><h3>Continua com o Rafael</h3>'
    "<p>A discussão de alvo volta pelo lado de negócio, com a recomendação que o Comitê precisa assinar.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">15/08 &middot; tarde</p><h3>Trata o dado</h3>'
    "<p>As quatro advertências de qualidade do painel. Foi uma delas que separou a contagem das mesas hoje.</p></div>\n"
    '          <div class="etapa avaliada fragment"><p class="quando">Semana 5 &middot; 05/09</p><h3>Artefato 1</h3>'
    "<p>Análise Exploratória de Dados, com a segmentação que a trilha de Negócios entrega no mesmo marco.</p></div>\n"
    "        </div>\n",
    conclusao="A divergência de contagem de hoje não é erro de ninguém: é o insumo da aula de qualidade de dado em 15/08.",
    por_passos=True,
))

# 31. Referencias
SLIDES.append(conteudo(
    "Referências e nota metodológica",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>Caso e dados</h3>'
    "<p>1. Kovan Technologies LATAM: A Definição do Alvo. Business case PL-02-2026, versão v2, e Caderno de Exhibits 1 a 5.</p></div>\n"
    '          <div class="concept-card"><h3>Método</h3>'
    "<p>2. Wirth e Hipp. CRISP-DM, 2000. &nbsp; 3. Tukey. Exploratory Data Analysis, 1977.</p>"
    "<p>4. Conn e Sarrazin. Issue Tree e MECE, McKinsey, 2019. &nbsp; 5. Courtney, Kirkland e "
    "Viguerie. Strategy Under Uncertainty, HBR, 1997.</p></div>\n"
    '          <div class="concept-card"><h3>Continuidade no programa</h3>'
    "<p>6. Donaire, R. Inteligência de Mercado e Modelagem Preditiva. Aula 01, manhã, 08/08/2026. Estrutura CREATE e vieses do HIPPO.</p></div>\n"
    "        </div>\n",
    conclusao="O ciclo de EDA assistida e os cinco critérios de escolha de alvo são construção deste módulo, não framework publicado.",
    rotulo_conclusao="Nota metodológica",
    conclusao_clara=True,
))

# 32. Encerramento
SLIDES.append(
    '      <section class="end-slide">\n'
    '        <div class="accent-bar"></div>\n'
    '        <p class="secao-numero">Módulo 2 &middot; Aula 01 &middot; encerramento</p>\n'
    "        <h1>Próximo encontro: 15/08</h1>\n"
    "        <h3>Prof. José Romualdo da Costa Filho &middot; MBA em IA e Dados para Negócios</h3>\n"
    "      </section>\n"
)


ESQUELETO = """<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aula 01 &middot; Da hipótese à evidência &middot; MBA Inteli x Lenovo</title>

  <!-- Gerado por tools/montar_deck_aula01.py. Nao editar a mao: a numeracao de
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
