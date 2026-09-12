# -*- coding: utf-8 -*-
"""Monta aulas/aula06.html.

Gerado, nunca editado a mao: a numeracao de rodape e o fechamento de secao sao
garantidos aqui, e ja se perderam no HTML duas vezes.

Diretiva editorial: sem paralelismo negativo, sem antitese simetrica, sem
escalada com dois-pontos. Titulo de slide de conteudo e a conclusao completa,
com o numero dentro. Travado por tools/check_retorica.py.

Todo numero do case que aparece aqui esta travado em
dados/tests/test_aula06_numeros.py, que le o dataset oficial da Lenovo.

Uso: python3 tools/montar_deck_aula06.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from tools import deck_kit  # noqa: E402
from tools.deck_kit import conteudo, pratica, quiz, secao  # noqa: E402

SAIDA = RAIZ / "aulas" / "aula06.html"

deck_kit.configurar("Módulo 2 &middot; Aula 06")
deck_kit.reiniciar_paginacao()

AMBIENTE = "Gemini"
SLIDES: list[str] = []

# ---------------------------------------------------------------------------
# 1. Capa
# ---------------------------------------------------------------------------
SLIDES.append(
    '      <section class="cover-slide">\n'
    '        <div class="cover-panel">\n'
    '          <div class="cover-content">\n'
    '            <p class="cover-eyebrow">MBA em IA e Dados para Negócios &middot; Inteli x Lenovo</p>\n'
    "            <h1>As variáveis de entrada</h1>\n"
    "            <h3>Recência, frequência e valor sobre uma janela que termina antes do rótulo, e o peso que cada uma recebe no modelo</h3>\n"
    '            <p class="cover-meta">Módulo 2 &middot; Aula 06 &middot; Trilha de Tecnologia</p>\n'
    '            <p class="cover-meta">12 de setembro de 2026 &middot; 09h00 às 12h00</p>\n'
    "          </div>\n"
    "        </div>\n"
    "      </section>\n"
)

# ---------------------------------------------------------------------------
# 2. Resgate
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A Entrega 1 fechou o alvo em 3.748 contas elegíveis",
    '        <div class="stat-tiles">\n'
    '          <div class="stat-tile"><p class="stat-numero">3.748</p><p class="stat-rotulo">contas que o rótulo alcança</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">1.593</p><p class="stat-rotulo">marcadas como perdidas</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">42,5%</p><p class="stat-rotulo">prevalência na população elegível</p></div>\n'
    '          <div class="stat-tile destaque"><p class="stat-numero">13</p><p class="stat-rotulo">meses de inatividade que o rótulo exige</p></div>\n'
    "        </div>\n"
    '        <p class="linha-contexto">O modelo da tarde precisa de uma linha por conta com colunas numéricas. Nenhuma dessas colunas existe no dataset.</p>\n',
    contexto="A Aula 04 recortou quem podia ser marcado; a Entrega 1 fechou o Artefato 1 com sete seções.",
    conclusao="A manhã constrói as colunas de entrada e mede o peso de cada uma. A tarde treina e avalia.",
    fonte="Fonte: datasets_case_modulo2.xlsx; dados/analise_aula06.py.",
))

# ---------------------------------------------------------------------------
# 3. Contrato
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Contrato e escopo da manhã",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Item</th><th>O que vale hoje</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Contrato</td><td>Nenhuma coluna entra na tabela de treino sem a data de corte declarada e sem a medida de quanto ela separa conta perdida de conta mantida.</td></tr>\n"
    "            <tr><td>Ambiente</td><td>Gemini sobre a pasta clonada, com os prompts literais de cada prática nos slides.</td></tr>\n"
    "            <tr><td>Método</td><td>09h00 às 10h20, o corte temporal e as três famílias de variável. 10h35 às 11h20, o peso de cada uma.</td></tr>\n"
    "            <tr><td>Oficina</td><td>11h20 às 11h50, a tabela de features do grupo, reexecutável, com o dicionário de colunas.</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
))

# ---------------------------------------------------------------------------
# 3b. O ambiente: Vertex AI Search com Gemini Pro
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "O ambiente da prática é o Vertex AI Search com Gemini Pro",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Item</th><th>O que usar hoje</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Acesso</td><td>Conta institucional da turma, pelo endereço abaixo. O mesmo link está no portal do módulo.</td></tr>\n"
    "            <tr><td>Modelo</td><td>Gemini Pro, para geração de código e auditoria da própria resposta.</td></tr>\n"
    "            <tr><td>Uso na aula</td><td>As duas práticas rodam ali, com os prompts literais que aparecem nos slides.</td></tr>\n"
    "            <tr><td>Regra</td><td>Todo código gerado passa pelas três perguntas antes de virar coluna da tabela.</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n"
    '        <p class="code-compact"><a href="https://vertexaisearch.cloud.google.com/global/home/cid/168348ee-a260-40fe-b2d0-7dae648342db/r/image-and-video?utm_source=gemini-standard-plus&amp;utm_medium=email&amp;utm_campaign=end-user-welcome&amp;utm_content=get-started">vertexaisearch.cloud.google.com/global/home/cid/168348ee-a260-40fe-b2d0-7dae648342db/r/image-and-video</a></p>\n',
    conclusao="O modelo escreve o código, e a auditoria de vazamento continua sendo trabalho de quem assina a tabela.",
))

# ---------------------------------------------------------------------------
# 4. Divisor: engenharia de feature
# ---------------------------------------------------------------------------
SLIDES.append(secao("01", "Engenharia de feature", "Do evento cru à coluna que o modelo lê",
                    ["O dado chega em evento", "O modelo exige matriz", "A ponte é agregação com data"]))

# ---------------------------------------------------------------------------
# 4b. A definição, em forma de esteira
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "De 207.826 itens de pedido para 3.748 linhas de 7 colunas",
    '        <div class="processo-fases">\n'
    '          <div class="processo-fase fragment"><h4>01. Evento</h4>'
    "<p>Um item de pedido, com data, conta, marca e valor. 207.826 linhas.</p></div>\n"
    '          <div class="processo-fase fragment"><h4>02. Corte</h4>'
    "<p>Fica só o que aconteceu até a data da previsão.</p></div>\n"
    '          <div class="processo-fase fragment"><h4>03. Agregação</h4>'
    "<p>Contar, somar, comparar e datar, sempre por conta.</p></div>\n"
    '          <div class="processo-fase fragment"><h4>04. Coluna</h4>'
    "<p>Cada agregação vira uma coluna com nome e fórmula.</p></div>\n"
    '          <div class="processo-fase fragment"><h4>05. Matriz</h4>'
    "<p>Uma linha por conta elegível. 3.748 por 7.</p></div>\n"
    '          <div class="processo-fase fragment ativa"><h4>06. Escore</h4>'
    "<p>O modelo lê a linha e devolve uma probabilidade.</p></div>\n"
    "        </div>\n",
    contexto="Engenharia de feature é o trabalho de converter o registro de um evento em uma medida por unidade de decisão, dentro de uma janela de tempo declarada.",
    conclusao="A unidade de decisão da Kovan é a conta. Todo dado do case precisa chegar a esse grão antes de virar entrada.",
    fonte="Fonte: dados/analise_aula06.py, do_evento_a_conta.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 4c. O que define um problema de previsão
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Prever exige fixar cinco coisas antes de escrever código",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>O que fixar</th><th>Na Kovan</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Unidade de decisão</td><td>a conta, porque é sobre a conta que o Account Manager age</td></tr>\n"
    "            <tr><td>Instante da previsão</td><td>2025-02, a data de corte</td></tr>\n"
    "            <tr><td>Horizonte</td><td>os 13 meses seguintes, que é o que o rótulo cobre</td></tr>\n"
    "            <tr><td>População</td><td>as 3.748 contas que o rótulo consegue marcar</td></tr>\n"
    "            <tr><td>Uso da saída</td><td>uma lista de 138 contas por ciclo, o limite operacional</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="Sem esses cinco itens fixados, duas pessoas constroem tabelas diferentes a partir do mesmo dataset e nenhuma das duas está errada.",
    conclusao="Os cinco itens vieram das Aulas 03 e 04. A manhã de hoje só constrói as colunas em cima deles.",
))

# ---------------------------------------------------------------------------
# 4d. Dificuldades
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Dificuldades da tabela de features",
    '        <div class="concept-cards quatro">\n'
    '          <div class="concept-card"><h3>Tempo</h3>'
    "<p>A coluna pode ler informação que ainda não existia no instante da previsão. É o vazamento, e é a dificuldade que domina a manhã.</p></div>\n"
    '          <div class="concept-card"><h3>Grão</h3>'
    "<p>O dado chega por item de pedido, por mês e por conta. Agregar do grão errado inventa ou apaga comportamento.</p></div>\n"
    '          <div class="concept-card"><h3>Ausência</h3>'
    "<p>Conta que não comprou não gera linha nenhuma. O silêncio precisa virar número de forma explícita, e é isso que a recência faz.</p></div>\n"
    '          <div class="concept-card"><h3>Escala</h3>'
    "<p>Receita em dólar e contagem de marcas convivem na mesma linha. Comparar peso entre elas exige padronizar antes.</p></div>\n"
    "        </div>\n",
    conclusao="As quatro reaparecem em cada seção de hoje, e a de tempo é a única que estraga o modelo sem dar sinal na métrica.",
))

# ---------------------------------------------------------------------------
# 4e. Técnicas
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Técnicas de construção de coluna",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Técnica</th><th>O que ela produz</th><th>Coluna desta aula</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Agregação</td><td>soma, média ou contagem por conta na janela</td><td><code>valor_obs</code></td></tr>\n"
    "            <tr><td>Contagem distinta</td><td>variedade de um atributo dentro da conta</td><td><code>marcas_obs</code>, <code>freq_dias</code></td></tr>\n"
    "            <tr><td>Recência</td><td>distância em tempo até a data de referência</td><td><code>recencia_corte</code></td></tr>\n"
    "            <tr><td>Janela móvel</td><td>a mesma agregação em recortes de tempo</td><td><code>receita_3m</code></td></tr>\n"
    "            <tr><td>Razão entre janelas</td><td>tendência, sem depender do tamanho da conta</td><td><code>razao_3m</code></td></tr>\n"
    "            <tr><td>Padronização</td><td>escalas diferentes na mesma régua</td><td>entrada da regressão</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="Codificação de categoria e discretização entram na tarde, quando segmento e setor virarem entrada.",
    conclusao="Toda técnica desta lista precisa da data de corte no argumento. Sem ela, qualquer uma delas vaza.",
))

# ---------------------------------------------------------------------------
# 5. Divisor 02
# ---------------------------------------------------------------------------
SLIDES.append(secao("02", "O corte temporal", "A data que separa o que se observa do que se prevê",
                    ["Janela de observação", "Janela do rótulo", "Nada atravessa o corte"]))

# ---------------------------------------------------------------------------
# 5. O painel se parte em dois
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "O rótulo de 13 meses parte o painel de 24 em duas janelas",
    '        <div class="linha-tempo">\n'
    '          <div class="etapa fragment"><p class="quando">2024-04 a 2025-02 &middot; 11 meses</p>'
    "<h3>Janela de observação</h3>"
    "<p>O que a conta fez aqui dentro vira coluna de entrada. Recência, frequência, valor, mix e sequência.</p></div>\n"
    '          <div class="etapa avaliada fragment"><p class="quando">2025-02</p>'
    "<h3>Data de corte</h3>"
    "<p>O instante em que a previsão seria feita na vida real. O que vem depois não existe para o modelo.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">2025-03 a 2026-03 &middot; 13 meses</p>'
    "<h3>Janela do rótulo</h3>"
    "<p>A conta comprou ou não comprou. É a resposta, e resposta não entra como pergunta.</p></div>\n"
    "        </div>\n",
    contexto="A data de corte sai da aritmética do rótulo. O painel termina em 2026-03, o rótulo exige treze meses sem compra, e treze meses antes de 2026-03 é 2025-02.",
    conclusao="Toda coluna construída hoje é calculada com dado até 2025-02, e só com ele.",
    fonte="Fonte: dados/analise_aula06.py, particao_temporal.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 6. O vazamento medido
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A recência do fim do painel repete o rótulo em 89,8%",
    '        <table class="tabela-criterios compacta numerica">\n'
    "          <thead><tr><th>Variável</th><th>Janela usada</th><th>AUC isolada</th></tr></thead>\n"
    "          <tbody>\n"
    '            <tr class="destaque"><td>Recência no fim do painel</td><td>painel inteiro</td><td>0,994</td></tr>\n'
    "            <tr><td>Meses ativos no painel inteiro</td><td>painel inteiro</td><td>0,885</td></tr>\n"
    "            <tr><td>Receita do painel inteiro</td><td>painel inteiro</td><td>0,752</td></tr>\n"
    '            <tr class="fragment"><td>Recência no corte</td><td>observação</td><td>0,772</td></tr>\n'
    "          </tbody>\n"
    "        </table>\n"
    '        <div class="faixa-conclusao clara fragment">\n'
    '          <span class="rotulo">Definições</span>\n'
    "          <p><strong>Recência:</strong> meses entre a última compra e uma data de referência. "
    "<strong>AUC:</strong> chance de a conta perdida pontuar acima da mantida, de 0,5 a 1,0.</p>\n"
    "        </div>\n",
    conclusao="Mudar a referência para 2026-03 faz a coluna copiar o rótulo em 3.366 das 3.748.",
    fonte="Fonte: dados/analise_aula06.py.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 7. Os três testes de vazamento
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Três perguntas reprovam uma coluna antes do treino",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>01. Data</h3>'
    "<p>Algum dado usado no cálculo tem data posterior a 2025-02? Receita total, meses ativos e última compra do painel inteiro reprovam aqui.</p></div>\n"
    '          <div class="concept-card"><h3>02. Definição</h3>'
    "<p>A coluna usa a mesma regra que define o rótulo? Recência com corte em 13 meses é o rótulo escrito com outro nome.</p></div>\n"
    '          <div class="concept-card"><h3>03. Operação</h3>'
    "<p>O valor só é preenchido depois que alguém percebeu o problema? Contato de retenção e desconto emergencial chegam depois do desfecho.</p></div>\n"
    "        </div>\n",
    contexto="As três valem para qualquer coluna, inclusive as que o Gemini sugerir sozinho.",
    conclusao="Coluna que reprova em qualquer uma das três sai da tabela, mesmo com AUC alta. Principalmente com AUC alta.",
))

# ---------------------------------------------------------------------------
# 8. Prática 1
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    1, "Auditar as colunas candidatas com o Gemini", 15,
    "Em dupla, na pasta clonada", "Uma tabela candidatas.md com veredito por coluna",
    "Cada mesa lê em voz alta uma coluna que reprovou e em qual das três perguntas",
    [
        {"acao": "Peça a lista de candidatas ao Gemini, sem pedir código ainda.",
         "prompt": "Sou analista da Kovan LATAM. Tenho um painel mensal por conta de 2024-04 a 2026-03 com receita_usd, qtd_pedidos, segmento e região, mais os pedidos linha a linha com marca e data. O rótulo marca a conta cuja última compra é até 2025-02. Liste 12 colunas candidatas de entrada. Para cada uma, diga a data mais recente que ela usa. Não escreva código.",
         "detalhe": "Peça a data mais recente por coluna: é o que torna o vazamento visível na própria resposta."},
        {"acao": "Aplique as três perguntas na resposta dele.",
         "prompt": "Para cada uma das 12 colunas, responda as três perguntas: usa dado depois de 2025-02? usa a mesma regra do rótulo? só é preenchida depois que alguém percebeu o problema? Marque APROVADA ou REPROVADA e diga em qual pergunta.",
         "detalhe": "Confira à mão duas linhas do veredito. O Gemini aprova coluna vazada quando ela tem nome inocente."},
    ],
    "A dupla nomeia uma coluna que o Gemini sugeriu e que reprovou na pergunta 01",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 9. Divisor 02
# ---------------------------------------------------------------------------
SLIDES.append(secao("03", "Recência, frequência e valor", "Três famílias de variável sobre a janela de observação",
                    ["Há quanto tempo não compra", "Com que regularidade comprava", "Quanto trazia"]))

# ---------------------------------------------------------------------------
# 10. A tabela RFV
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Recência no corte lidera as sete colunas com AUC de 0,772",
    '        <table class="tabela-criterios compacta numerica">\n'
    "          <thead><tr><th>Família</th><th>Coluna</th><th>Como é calculada até 2025-02</th><th>AUC</th></tr></thead>\n"
    "          <tbody>\n"
    '            <tr class="destaque"><td>Recência</td><td>recencia_corte</td><td>meses entre a última compra e 2025-02</td><td>0,772</td></tr>\n'
    "            <tr><td>Frequência</td><td>freq_dias</td><td>dias distintos com pedido</td><td>0,693</td></tr>\n"
    "            <tr><td>Frequência</td><td>freq_meses</td><td>meses distintos com receita</td><td>0,680</td></tr>\n"
    "            <tr><td>Valor</td><td>valor_obs</td><td>soma da receita na janela</td><td>0,618</td></tr>\n"
    "            <tr><td>Mix</td><td>marcas_obs</td><td>marcas distintas compradas</td><td>0,608</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    conclusao="Nenhuma coluna honesta passa de 0,772. Ticket médio e razão dos 3 meses fecham a lista, com 0,540 e 0,567.",
    fonte="Fonte: dados/analise_aula06.py, auc_das_candidatas.",
))

# ---------------------------------------------------------------------------
# 11. A variável de sequência
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Conta sem receita nos 3 meses finais perde em 57,1%",
    '        <table class="tabela-criterios compacta numerica">\n'
    "          <thead><tr><th>Razão entre os dois blocos de 3 meses</th><th>Contas</th><th>Perdidas</th><th>Prevalência</th></tr></thead>\n"
    "          <tbody>\n"
    '            <tr class="destaque"><td>Sem receita nos 3 meses finais</td><td>735</td><td>420</td><td>57,1%</td></tr>\n'
    "            <tr><td>Queda acima de 50%</td><td>218</td><td>37</td><td>17,0%</td></tr>\n"
    "            <tr><td>Queda até 50%</td><td>2.426</td><td>1.088</td><td>44,8%</td></tr>\n"
    "            <tr><td>Estável ou em alta</td><td>369</td><td>48</td><td>13,0%</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n"
    '        <p class="linha-contexto">Quem caiu muito e seguiu comprando ainda estava vivo em 2025-02.</p>\n',
    contexto="Blocos comparados: 2024-12 a 2025-02 contra 2024-09 a 2024-11.",
    conclusao="A razão sozinha vale 0,567 de AUC. O que ela acrescenta é a distinção entre queda e ausência, que a recência não separa.",
    fonte="Fonte: dados/analise_aula06.py, perfil_da_razao.",
))

# ---------------------------------------------------------------------------
# 12. Quiz
# ---------------------------------------------------------------------------
SLIDES.append(quiz(
    "Verificação &middot; 5 minutos",
    "Qual coluna entra na tabela de treino?",
    "Corte em 2025-02. Qual das quatro colunas pode entrar no treino?",
    [
        {"texto": "Receita total no painel inteiro", "certa": False,
         "certo": "", "errado": "Não: a soma inclui a janela do rótulo. Reprova na pergunta 01."},
        {"texto": "Dias com pedido entre 2024-04 e 2025-02", "certa": True,
         "certo": "Certo: fecha em 2025-02, não repete a regra do rótulo e existe antes do desfecho.",
         "errado": ""},
        {"texto": "Meses desde a última compra até 2026-03", "certa": False,
         "certo": "", "errado": "Não: é a coluna de AUC 0,994, que reconstrói o rótulo."},
        {"texto": "Contatos de retenção do Account Manager", "certa": False,
         "certo": "", "errado": "Não: o contato vem depois que alguém percebeu a queda. Reprova na 03."},
    ],
    {"fichas": [("População", "3.748 elegíveis"), ("Prevalência", "42,5%"),
                ("Corte", "2025-02")]},
))

# ---------------------------------------------------------------------------
# 13. Divisor 03
# ---------------------------------------------------------------------------
SLIDES.append(secao("04", "O peso de cada variável", "Quanto cada coluna move a chance de perda",
                    ["Coeficiente padronizado", "Razão de chances", "AUC do conjunto"]))

# ---------------------------------------------------------------------------
# 14. Por que padronizar antes de comparar peso
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Comparar peso exige padronizar antes",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Medida</th><th>O que ela responde</th><th>Cuidado</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Coeficiente bruto</td><td>quanto muda o log-odds por unidade da coluna</td><td>receita em dólar e contagem de marcas não são comparáveis</td></tr>\n"
    "            <tr><td>Coeficiente padronizado</td><td>quanto muda o log-odds por desvio padrão</td><td>é o que permite ordenar as colunas</td></tr>\n"
    "            <tr><td>Razão de chances</td><td>por quanto a chance de perda é multiplicada</td><td>acima de 1,0 empurra para perda, abaixo segura</td></tr>\n"
    "            <tr><td>AUC do conjunto</td><td>o quanto o escore ordena a carteira</td><td>não diz se o limiar está calibrado, que é assunto da tarde</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="As quatro leituras vêm da mesma regressão logística. A diferença está no que cada uma deixa comparar.",
    conclusao="Peso relativo se lê sobre coeficiente padronizado. Coeficiente bruto ordena a escala da coluna, não a importância dela.",
))

# ---------------------------------------------------------------------------
# 15. A tabela de pesos
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Recência responde por 33,1% do peso do modelo",
    '        <table class="tabela-criterios compacta numerica">\n'
    "          <thead><tr><th>Coluna</th><th>Coeficiente padronizado</th><th>Razão de chances</th><th>Peso relativo</th></tr></thead>\n"
    "          <tbody>\n"
    '            <tr class="destaque"><td>recencia_corte</td><td>+0,804</td><td>2,234</td><td>33,1%</td></tr>\n'
    "            <tr><td>freq_meses</td><td>-0,588</td><td>0,555</td><td>24,2%</td></tr>\n"
    "            <tr><td>freq_dias</td><td>-0,554</td><td>0,574</td><td>22,8%</td></tr>\n"
    "            <tr><td>marcas_obs</td><td>-0,159</td><td>0,853</td><td>6,6%</td></tr>\n"
    "            <tr><td>ticket_medio, valor_obs e razao_3m</td><td>+0,129, -0,114 e -0,080</td><td>1,138, 0,892 e 0,923</td><td>13,3%</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="Regressão logística sobre as sete colunas padronizadas, nas 3.748 elegíveis.",
    conclusao="Recência e as duas colunas de frequência somam 80,1% do peso. Valor entra com 10,0%.",
    fonte="Fonte: dados/analise_aula06.py, pesos_do_modelo.",
))

# ---------------------------------------------------------------------------
# 16. A medida de qualidade
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "O conjunto honesto marca 0,794 e o vazado marca 0,995",
    '        <table class="tabela-criterios compacta numerica">\n'
    "          <thead><tr><th>Tabela de features</th><th>Colunas</th><th>AUC do escore</th><th>Serve para decidir?</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Sete colunas fechadas em 2025-02</td><td>7</td><td>0,794</td><td>sim</td></tr>\n"
    '            <tr class="fragment destaque"><td>As mesmas sete, mais a recência do fim do painel</td><td>8</td><td>0,995</td><td>não</td></tr>\n'
    "          </tbody>\n"
    "        </table>\n"
    '        <p class="linha-contexto fragment">A segunda linha sobe 0,201 de AUC e perde todo o valor de decisão: em produção a recência do fim do painel não existe no momento em que o Account Manager precisa da lista.</p>\n',
    contexto="Mesmo dado, mesma população, mesma regressão. A única diferença é uma coluna que atravessa o corte.",
    conclusao="A coluna precisa existir no instante da previsão. O ganho de métrica não entra nessa decisão.",
    fonte="Fonte: dados/analise_aula06.py, qualidade_do_modelo.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 17. Prática 2
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    2, "Construir a tabela de features com o Gemini", 20,
    "Em grupo, na pasta clonada", "features.csv e o dicionário de colunas",
    "Cada mesa mostra a AUC isolada da coluna que criou",
    [
        {"acao": "Gere o código da tabela, com a data de corte no argumento.",
         "prompt": "Escreva uma função em pandas que receba a data de corte como parâmetro e devolva uma linha por conta elegível com as sete colunas da tabela anterior, sem usar dado posterior ao corte."},
        {"acao": "Peça a auditoria do próprio código.",
         "prompt": "Percorra a função e aponte cada trecho que lê dado posterior ao corte. Se não houver, diga qual filtro garante isso em cada coluna.",
         "detalhe": "O erro comum é filtrar o painel e esquecer os pedidos."},
        {"acao": "Meça a AUC de cada coluna e acrescente uma sua. Acima de 0,90, ela vaza.",
         "prompt": "Calcule a AUC isolada de cada coluna por Mann-Whitney. Depois proponha uma oitava coluna que respeite o corte e calcule a AUC dela."},
    ],
    "features.csv reexecutável, com a AUC isolada de cada coluna",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 18. Realimentação
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "O score muda o dado que treina a próxima versão",
    '        <div class="linha-tempo">\n'
    '          <div class="etapa fragment"><p class="quando">Mês 1</p><h3>O modelo aponta</h3>'
    "<p>A lista prioriza 138 contas por valor em risco, dentro da capacidade operacional medida na Aula 04.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">Mês 2</p><h3>O time age</h3>'
    "<p>O Account Manager contata essas 138. Contato registrado, desconto oferecido, oportunidade reaberta.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">Mês 3</p><h3>O dado muda</h3>'
    "<p>Contatos e oportunidades passam a marcar exatamente as contas que o modelo apontou, e não as que estavam em risco.</p></div>\n"
    '          <div class="etapa avaliada fragment"><p class="quando">Próxima versão</p><h3>O treino herda</h3>'
    "<p>Treinar com essas colunas ensina o modelo a reproduzir a lista anterior. A marcação do grupo de controle é o que quebra o ciclo.</p></div>\n"
    "        </div>\n",
    contexto="As colunas de engajamento do Dataset 3 são as candidatas mais expostas a esse efeito.",
    conclusao="Contas mantidas fora da intervenção, marcadas desde o primeiro ciclo, são o único registro do que teria acontecido sem o modelo.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 19. Oficina
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    3, "Oficina: a tabela de features do grupo", 30,
    "Em grupo, três estações de tempo marcado", "A pasta do grupo com features.csv e dicionario.md",
    "Checkpoint às 11h40: cada mesa mostra a coluna de maior peso e a data que ela usa",
    [
        {"acao": "Estação 1, 10 minutos: fechar as sete colunas.",
         "detalhe": "Rodar a função sobre a população elegível e conferir a contagem de 3.748 linhas."},
        {"acao": "Estação 2, 10 minutos: o dicionário de colunas.",
         "detalhe": "Nome, fórmula, data mais recente usada, AUC isolada e o veredito nas três perguntas. Uma linha por coluna."},
        {"acao": "Estação 3, 10 minutos: o peso de cada coluna.",
         "detalhe": "Regressão logística sobre as colunas padronizadas, e a tabela de coeficiente, razão de chances e peso relativo."},
    ],
    "Outra pessoa clona a pasta, roda a função com outra data de corte e obtém outra tabela coerente",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 20. Amarração
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A tabela de hoje é a entrada do modelo da tarde",
    '        <div class="linha-tempo">\n'
    '          <div class="etapa fragment"><p class="quando">Hoje, manhã</p><h3>Fica pronto</h3>'
    "<p>Sete colunas fechadas em 2025-02, o dicionário com a data de cada uma e o peso relativo de cada coluna.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">Hoje, tarde</p><h3>Treinamento e avaliação</h3>'
    "<p>Regressão logística, matriz de confusão e AUC-ROC. O limiar sai da capacidade operacional de 138 contas, não de 0,5.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">Base longa</p><h3>Cinco anos de painel</h3>'
    "<p>A base de 65 meses permite mais de uma data de corte e o histórico de 12 meses que a janela de 11 não comporta.</p></div>\n"
    '          <div class="etapa avaliada fragment"><p class="quando">03/10 &middot; Semana 9</p><h3>Artefato 2 e banca</h3>'
    "<p>O aplicativo preditivo-generativo, defendido no papel do Comitê de Receita.</p></div>\n"
    "        </div>\n",
    conclusao="Uma coluna com AUC de 0,99 na primeira tentativa é o achado mais caro que um grupo pode levar para a banca.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 21. Referências
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Referências e nota metodológica",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>Caso e dados</h3>'
    "<p>1. Kovan Technologies LATAM: A Definição do Alvo. Business case PL-02-2026, versão v2.</p>"
    "<p>2. datasets_case_modulo2.xlsx, base oficial recebida em 21/08/2026. Não distribuída por este acervo.</p></div>\n"
    '          <div class="concept-card"><h3>Métodos citáveis</h3>'
    "<p>3. Kaufman, S. et al. Leakage in Data Mining. ACM TKDD, 2012.</p>"
    "<p>4. Hosmer, D. e Lemeshow, S. Applied Logistic Regression. Wiley, 2013.</p>"
    "<p>5. Mann, H. e Whitney, D. On a Test of Whether One of Two Random Variables is Stochastically Larger. AMS, 1947.</p></div>\n"
    '          <div class="concept-card"><h3>O que é nosso</h3>'
    "<p>O corte em 2025-02, as três perguntas de vazamento e a tabela de sete colunas, organizados para este módulo.</p></div>\n"
    "        </div>\n",
    conclusao="Todo número desta aula está travado em dados/tests/test_aula06_numeros.py.",
))

# ---------------------------------------------------------------------------
# Esqueleto
# ---------------------------------------------------------------------------
ESQUELETO = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aula 06 &middot; As variáveis de entrada &middot; MBA Inteli x Lenovo</title>

  <!-- Gerado por tools/montar_deck_aula06.py. Nao editar a mao: a numeracao de
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
