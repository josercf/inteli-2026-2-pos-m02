# -*- coding: utf-8 -*-
"""Monta aulas/aula07.html.

Gerado, nunca editado a mao: a numeracao de rodape e o fechamento de secao sao
garantidos aqui, e ja se perderam no HTML duas vezes.

Diretiva editorial: sem paralelismo negativo, sem antitese simetrica, sem
escalada com dois-pontos. Titulo de slide de conteudo e a conclusao completa,
com o numero dentro. Travado por tools/check_retorica.py.

Todo numero do case que aparece aqui sai de dados/analise_aula07.py, que importa
o proprio pacote que a turma roda, e esta travado em
dados/tests/test_aula07_numeros.py.

Uso: python3 tools/montar_deck_aula07.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from tools import deck_kit  # noqa: E402
from tools.deck_kit import conteudo, pratica, quiz, secao  # noqa: E402

SAIDA = RAIZ / "aulas" / "aula07.html"

deck_kit.configurar("Módulo 2 &middot; Aula 07")
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
    "            <h1>Do script à tela</h1>\n"
    "            <h3>O modelo exportado do Gemini vira pacote com teste, e a fila que o Account Manager abre revela qual critério de ordenação vale dinheiro</h3>\n"
    '            <p class="cover-meta">Módulo 2 &middot; Aula 07 &middot; Trilha de Tecnologia</p>\n'
    '            <p class="cover-meta">26 de setembro de 2026 &middot; 13h00 às 16h00</p>\n'
    "          </div>\n"
    "        </div>\n"
    "      </section>\n"
)

# ---------------------------------------------------------------------------
# 2. Resgate
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A Aula 06 fechou 11 colunas e o Gemini devolveu 94 linhas",
    '        <div class="stat-tiles">\n'
    '          <div class="stat-tile"><p class="stat-numero">11</p><p class="stat-rotulo">colunas de entrada, fechadas em 2024-03</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">4.708</p><p class="stat-rotulo">contas elegíveis</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">94</p><p class="stat-rotulo">linhas do script exportado</p></div>\n'
    '          <div class="stat-tile destaque"><p class="stat-numero">0</p><p class="stat-rotulo">testes que o script trouxe</p></div>\n'
    "        </div>\n"
    '        <p class="linha-contexto">O script treina, prevê e imprime. Ele funciona, e é um bom ponto de partida. Ele não é um produto.</p>\n',
    contexto="A manhã da Aula 06 construiu a tabela de features e mediu o peso de cada coluna. O grupo exportou o modelo do Gemini.",
    conclusao="A tarde de hoje transforma o script em pacote com teste e em uma tela que alguém abre.",
    fonte="Fonte: dados/analise_aula07.py.",
))

# ---------------------------------------------------------------------------
# 3. Contrato
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Contrato e escopo da tarde",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Item</th><th>O que vale hoje</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Contrato</td><td>Nada entra no aplicativo sem teste que possa falhar. Número que a tela mostra e código que ninguém consegue reexecutar não contam.</td></tr>\n"
    "            <tr><td>Ambiente</td><td>Antigravity sobre a pasta clonada. O aplicativo vive em <code>app/</code>, ao lado das análises.</td></tr>\n"
    "            <tr><td>Método</td><td>13h00 às 14h20, do script ao pacote. 14h40 às 15h20, o critério da fila.</td></tr>\n"
    "            <tr><td>Oficina</td><td>15h20 às 15h50, a tela do grupo rodando. Checkpoint às 15h40.</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
))

# ---------------------------------------------------------------------------
# 4. Divisor 01
# ---------------------------------------------------------------------------
SLIDES.append(secao("01", "O script que veio do Gemini", "O que ele resolve e onde ele para",
                    ["Treina e prevê", "Inventa o próprio alvo", "Custa meio segundo por conta"]))

# ---------------------------------------------------------------------------
# 5. O que o script faz e onde para
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "As 94 linhas resolvem três coisas e param em três",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>O script resolve</th><th>O script para em</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Monta oito colunas a partir da linha de pedido</td><td>Inventa o próprio alvo, com corte em 2022-06-30</td></tr>\n"
    "            <tr><td>Treina um HistGradientBoosting e prevê</td><td>Reprocessa 492.393 linhas a cada consulta</td></tr>\n"
    "            <tr><td>Devolve a probabilidade de uma conta</td><td>Devolve probabilidade, e não a lista de trabalho</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n"
    '        <p class="linha-contexto">Os três da direita são o roteiro da tarde. Nenhum deles é erro de quem escreveu: são o que separa um script que responde de um aplicativo que alguém opera.</p>\n',
    contexto="O código foi lido linha a linha antes desta aula, e roda sobre a base longa sem alteração.",
    conclusao="Refatorar aqui é trabalho de engenharia, e é o que o Artefato 2 avalia.",
))

# ---------------------------------------------------------------------------
# 6. O alvo inventado
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Um alvo próprio impede comparar com tudo que veio antes",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Item</th><th>No script exportado</th><th>No case</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Data de corte</td><td>2022-06-30</td><td>07/03/2024</td></tr>\n"
    "            <tr><td>Definição de perda</td><td>sem compra até 2024-12-31</td><td><code>churn_label</code> do painel</td></tr>\n"
    '            <tr class="fragment"><td>População avaliada</td><td>toda conta com histórico</td><td>as 4.708 elegíveis</td></tr>\n'
    "          </tbody>\n"
    "        </table>\n"
    '        <p class="linha-contexto fragment">O alvo do script é defensável em abstrato. O problema é que ele não é o alvo que o Comitê aprovou, e a Entrega 1 inteira foi construída sobre o outro.</p>\n',
    contexto="As duas definições produzem populações e prevalências diferentes.",
    conclusao="Modelo avaliado contra outro rótulo não se compara com nada que a turma produziu até aqui.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 7. O custo por consulta
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A tabela sai de 219 segundos para 0,6 com o cache",
    '        <table class="tabela-criterios compacta numerica">\n'
    "          <thead><tr><th>Etapa</th><th>No script</th><th>No pacote</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Ler as cinco abas do xlsx</td><td>a cada execução</td><td>uma vez, com cache em disco</td></tr>\n"
    "            <tr><td>Converter data e valor</td><td>a cada consulta, nas 492.393 linhas</td><td>uma vez, na carga</td></tr>\n"
    "            <tr><td>Calcular a cadência</td><td>laço Python por conta</td><td>vetorizado</td></tr>\n"
    '            <tr class="destaque"><td>Montar a tabela de 4.708 contas</td><td>219 segundos</td><td>0,6 segundo</td></tr>\n'
    "            <tr><td>Treinar</td><td>a cada chamada</td><td>uma vez, gravado em joblib</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="Medido na mesma máquina, sobre a mesma base de 492.393 linhas de pedido.",
    conclusao="Meio segundo por conta parece pouco até a tela pedir 138 de uma vez. Aí vira um minuto de espera por clique.",
    fonte="Fonte: dados/analise_aula07.py, custo_de_carga.",
))

# ---------------------------------------------------------------------------
# 8. Prática 1
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    1, "Auditar o script exportado no Antigravity", 20,
    "Em grupo, na pasta clonada", "auditoria.md com um achado por linha, e o trecho citado",
    "Cada mesa lê um achado que não está nesta lista de três",
    [
        {"acao": "Peça a leitura crítica, sem deixar o agente reescrever nada ainda.",
         "prompt": "Leia churn_model.py inteiro. Liste cada ponto em que ele usa dado posterior à data de corte, cada ponto em que recalcula algo que já foi calculado, e cada ponto em que uma decisão de negócio está escrita no meio do código. Cite a linha. Não reescreva.",
         "detalhe": "Não deixe reescrever antes de listar. O agente conserta e a mesa perde o achado."},
        {"acao": "Confira dois achados à mão, na base.",
         "detalhe": "Um achado que ninguém verificou vale zero na banca. Escolha os dois mais caros e rode o número."},
    ],
    "A mesa tem um achado verificado que não estava na lista do professor",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 9. Divisor 02
# ---------------------------------------------------------------------------
SLIDES.append(secao("02", "De script para pacote", "O que muda quando outra pessoa precisa rodar",
                    ["Módulo com responsabilidade", "Teste que pode falhar", "Modelo gravado em disco"]))

# ---------------------------------------------------------------------------
# 10. A estrutura
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Cinco módulos, um assunto cada",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Módulo</th><th>Responsabilidade</th><th>O que ele não faz</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td><code>dados.py</code></td><td>ler as cinco abas, com cache</td><td>não limpa nem decide nada</td></tr>\n"
    "            <tr><td><code>rotulo.py</code></td><td>o alvo do case e a população elegível</td><td>não inventa critério</td></tr>\n"
    "            <tr><td><code>features.py</code></td><td>as 11 colunas, com o corte no argumento</td><td>não lê nada depois do corte</td></tr>\n"
    "            <tr><td><code>modelo.py</code></td><td>treinar, gravar, escore fora da amostra</td><td>não escolhe limiar</td></tr>\n"
    "            <tr><td><code>lista.py</code></td><td>da probabilidade para a fila do ciclo</td><td>não treina nada</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="A tela importa os cinco e não calcula nada por conta própria.",
    conclusao="A pergunta que separa um módulo do outro é quem precisa mudar quando o negócio muda de ideia.",
))

# ---------------------------------------------------------------------------
# 11. Antes e depois
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "O que mudou do script para o pacote",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Defeito</th><th>O que foi feito</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Alvo próprio, corte fixo no código</td><td>o <code>churn_label</code> do case, corte no argumento</td></tr>\n"
    "            <tr><td>Cadência conta a conta, tudo reprocessado</td><td>vetorizado, com cache em disco</td></tr>\n"
    "            <tr><td>Treina a cada chamada, e avalia dentro da amostra</td><td>modelo em <code>joblib</code>, escore fora da amostra em 5 dobras</td></tr>\n"
    "            <tr><td>Probabilidade solta</td><td>a fila do ciclo, limiar pela capacidade</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="As oito colunas do Gemini ficaram, e três de erosão entraram.",
    conclusao="AUC de 0,8249 fora da amostra, sobre as 4.708 elegíveis.",
    fonte="Fonte: dados/analise_aula07.py.",
))

# ---------------------------------------------------------------------------
# 12. O teste que trava o vazamento
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Um teste de dez linhas fecha o vazamento da tabela inteira",
    '        <pre class="code-compact"><code>def test_a_compra_posterior_ao_corte_nao_muda_nada():\n'
    "    ped = _pedidos_de_brinquedo()\n"
    "    completo = features.construir(ped, CORTE)\n"
    "    truncado = features.construir(ped[ped.billing_dt &lt;= CORTE], CORTE)\n"
    "    pd.testing.assert_frame_equal(completo, truncado)</code></pre>\n"
    '        <p class="linha-contexto">Apagar tudo que aconteceu depois do corte não pode mudar nenhuma coluna de nenhuma conta. Uma coluna que lê a janela do rótulo muda de valor assim que essa janela some da entrada.</p>\n',
    contexto="O mesmo teste roda duas vezes: sobre cinco pedidos de brinquedo e sobre as 4.708 contas reais.",
    conclusao="Foi visto falhando. Trocar a comparação da data faz a recência da conta de teste cair de 241 para 0.",
))

# ---------------------------------------------------------------------------
# 13. Os defeitos que os testes acharam
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Escrever os testes encontrou dois defeitos e um engano meu",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>O que apareceu</th><th>Como apareceu</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>A fila estourava com valor infinito</td><td>receita anualizada dividida por tempo de casa igual a zero</td></tr>\n"
    "            <tr><td>Oito contas em primeiro lugar</td><td><code>rank</code> com empate, e fila de trabalho não tem oito primeiros</td></tr>\n"
    '            <tr class="destaque"><td>O teste da razão estava errado</td><td>a conta de teste tinha base de comparação, e o 0,0 estava certo</td></tr>\n'
    "          </tbody>\n"
    "        </table>\n"
    '        <p class="linha-contexto">O terceiro é o mais útil de todos. O teste reprovou, eu conferi o dado, e quem estava errado era o teste. Isso está escrito na docstring dele.</p>\n',
    conclusao="Teste que nunca falhou não é prova de que o código está certo. Pode ser prova de que ele não testa nada.",
))

# ---------------------------------------------------------------------------
# 14. Prática 2
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    2, "Rodar o treino e a suíte na pasta do grupo", 20,
    "Em grupo, na pasta clonada", "A saída de python -m app.treinar e de pytest, coladas em execucao.md",
    "Cada mesa mostra a AUC fora da amostra e o número de testes que passaram",
    [
        {"acao": "Treine e grave o modelo.",
         "prompt": "Rode python -m app.treinar e cole a saída. Se algum número divergir do que está no README, aponte qual e investigue antes de seguir.",
         "detalhe": "Divergência aqui quase sempre é base diferente ou cache velho."},
        {"acao": "Rode a suíte e quebre um teste de propósito.",
         "prompt": "Rode pytest app/tests -q. Depois altere features.py para usar o painel inteiro no lugar do histórico até o corte, rode de novo e mostre qual teste reprova.",
         "detalhe": "Reverta a alteração depois. O objetivo é ver a rede pegar."},
    ],
    "A mesa viu o teste de vazamento reprovar e voltou ao verde",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 15. Divisor 03
# ---------------------------------------------------------------------------
SLIDES.append(secao("03", "O critério da fila", "Duas ordenações da mesma carteira",
                    ["Por probabilidade", "Por valor esperado", "A conta que muda de lugar"]))

# ---------------------------------------------------------------------------
# 16. O achado
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A fila com 85,5% de precisão alcança 0,01% da receita em risco",
    '        <table class="tabela-criterios compacta numerica">\n'
    "          <thead><tr><th>Ordenação da fila de 138</th><th>Acertos</th><th>Precisão</th><th>Receita alcançada</th><th>Do risco</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Por probabilidade de perda</td><td>118</td><td>85,5%</td><td>USD 2.641</td><td>0,01%</td></tr>\n"
    '            <tr class="destaque fragment"><td>Por valor esperado</td><td>41</td><td>29,7%</td><td>USD 25.242.093</td><td>68,4%</td></tr>\n'
    "          </tbody>\n"
    "        </table>\n"
    '        <p class="linha-contexto fragment">As contas de escore mais alto são compras únicas de 2021. A receita delas nos 12 meses antes do corte é zero, porque elas já tinham ido embora.</p>\n',
    contexto="Mesmo modelo, mesma fila de 138, muda só o critério. O risco total é de USD 36.903.303, nas 2.456 contas perdidas.",
    conclusao="Valor esperado é o escore multiplicado pela receita dos 12 meses anteriores. Uma multiplicação reordena a carteira inteira.",
    fonte="Fonte: dados/analise_aula07.py, filas.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 17. A Conta D
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A Conta D sai de 3.024º para 1º ao trocar o critério",
    '        <table class="tabela-criterios compacta numerica">\n'
    "          <thead><tr><th>Critério</th><th>Conta D</th><th>Conta E</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Escore do modelo</td><td>0,448</td><td>0,820</td></tr>\n"
    "            <tr><td>Receita nos 12 meses até o corte</td><td>USD 4.642.422</td><td>USD 0</td></tr>\n"
    "            <tr><td>Posição por probabilidade</td><td>3.024º</td><td>910º</td></tr>\n"
    '            <tr class="destaque"><td>Posição por valor esperado</td><td>1º</td><td>4.085º</td></tr>\n'
    "          </tbody>\n"
    "          </tbody>\n"
    "        </table>\n"
    '        <p class="linha-contexto">A Conta D é a que a Aula 06 apresentou: a perda mais cara da carteira, invisível para o escore. Acrescentar colunas de erosão moveu ela de 3.254º para 3.024º. Trocar o critério moveu para 1º.</p>\n',
    conclusao="O ponto cego não era da tabela de features. Era da pergunta que a lista respondia.",
    fonte="Fonte: dados/analise_aula07.py, par_de_contas.",
))

# ---------------------------------------------------------------------------
# 18. Quiz
# ---------------------------------------------------------------------------
SLIDES.append(quiz(
    "Verificação &middot; 5 minutos",
    "Qual mudança recupera mais receita?",
    "A fila de 138 alcança 0,01% da receita em risco. O que muda mais esse número?",
    [
        {"texto": "Trocar a regressão pelo XGBoost bem ajustado", "certa": False,
         "certo": "", "errado": "Não: a AUC subiria alguns pontos e a ordem por probabilidade continuaria a mesma."},
        {"texto": "Ordenar a fila por escore vezes receita", "certa": True,
         "certo": "Certo: a mesma fila de 138 passa a alcançar 68,4% do risco, com precisão menor.",
         "errado": ""},
        {"texto": "Dobrar a capacidade para 276 contas", "certa": False,
         "certo": "", "errado": "Não: mais contas do mesmo tipo. O topo da lista continua sendo compra única de 2021."},
        {"texto": "Acrescentar colunas de erosão de receita", "certa": False,
         "certo": "", "errado": "Não: já foram acrescentadas, e a Conta D andou de 3.254º para 3.024º."},
    ],
    {"fichas": [("Fila", "138 contas"), ("Risco total", "USD 36,9 mi"),
                ("Precisão hoje", "85,5%")]},
))

# ---------------------------------------------------------------------------
# 19. Divisor 04
# ---------------------------------------------------------------------------
SLIDES.append(secao("04", "A tela", "O que o Account Manager abre na segunda de manhã",
                    ["A fila do ciclo", "A conta aberta", "O que a tela não sabe"]))

# ---------------------------------------------------------------------------
# 20. A tela
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A tela mostra a fila, a conta e o que ela não sabe",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>A fila</h3>'
    "<p>As 138 do ciclo, com escore, receita em risco e valor esperado. O critério de ordenação é um botão, e os cartões de precisão e de receita alcançada mudam junto.</p></div>\n"
    '          <div class="concept-card"><h3>A conta</h3>'
    "<p>As compras mês a mês até o corte, as 11 colunas de entrada e as duas posições. É o que o Account Manager precisa para justificar a ligação internamente.</p></div>\n"
    '          <div class="concept-card"><h3>O rodapé</h3>'
    "<p>As quatro coisas que a tela não sabe, escritas na própria tela. Limitação que só existe no relatório não chega a quem decide.</p></div>\n"
    "        </div>\n",
    contexto="Streamlit, carregando o modelo gravado. A tela não treina nada e abre em menos de um segundo.",
    conclusao="Um aviso aparece quando a conta tem valor alto e escore baixo, que é exatamente o caso da Conta D.",
))

# ---------------------------------------------------------------------------
# 21. O que a tela não sabe
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Quatro limitações ficam escritas na própria tela",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Limitação</th><th>Consequência para quem usa</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>O escore mede parada de compra</td><td>conta que encolhe e continua comprando não aparece</td></tr>\n"
    "            <tr><td>Engajamento cobre 33,8% das contas antes do corte</td><td>contato comercial não entra como coluna</td></tr>\n"
    "            <tr><td>Valor em risco é a receita dos 12 meses anteriores</td><td>conta parada há mais de um ano vale zero por construção</td></tr>\n"
    "            <tr><td>Nenhuma coluna usa dado posterior ao corte</td><td>verificado em teste, e não prometido em texto</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="A Conta D não tem nenhuma linha de engajamento até o corte. O sinal que a salvaria não está em aba nenhuma da base.",
    conclusao="Estas quatro entram na seção de limitações do Artefato 2, com o número ao lado de cada uma.",
))

# ---------------------------------------------------------------------------
# 22. Oficina
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    3, "Oficina: a tela do grupo no ar", 30,
    "Em grupo, três estações de tempo marcado", "A tela rodando na máquina do grupo, com o critério de ordenação funcionando",
    "Checkpoint às 15h40: cada mesa projeta a própria tela e troca o critério ao vivo",
    [
        {"acao": "Estação 1, 10 minutos: treinar e abrir.",
         "detalhe": "python -m app.treinar e depois streamlit run. Se a tela demorar mais de dois segundos para abrir, ela está treinando na abertura."},
        {"acao": "Estação 2, 10 minutos: o botão de critério.",
         "detalhe": "Trocar a ordenação e conferir que os cartões de precisão e de receita alcançada mudam junto. Anotar os dois pares de números."},
        {"acao": "Estação 3, 10 minutos: o rodapé de limitações.",
         "detalhe": "Escrever as quatro limitações do grupo com o número ao lado. Limitação sem número é opinião."},
    ],
    "Outra pessoa clona a pasta, roda os dois comandos e vê a mesma fila",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 23. Amarração
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A tela de hoje é metade do Artefato 2",
    '        <div class="linha-tempo">\n'
    '          <div class="etapa fragment"><p class="quando">26/09 &middot; hoje</p><h3>Fica pronto</h3>'
    "<p>O pacote com teste, o modelo gravado e a tela com os dois critérios de fila.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">Pendente</p><h3>A camada generativa</h3>'
    "<p>O roteiro de intervenção por conta, com o guardrail de não citar número fora do escore. Depende da chave de API.</p></div>\n"
    '          <div class="etapa avaliada fragment"><p class="quando">03/10 &middot; Semana 9</p><h3>Entrega 2 e banca</h3>'
    "<p>Defesa no papel do Comitê de Receita, com a limitação declarada junto com o número.</p></div>\n"
    "        </div>\n",
    conclusao="O grupo que levar a fila por probabilidade sem a comparação de receita vai ser perguntado por que gastou o ciclo com contas que já tinham ido embora.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 24. Referências
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Referências e nota metodológica",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>Caso e dados</h3>'
    "<p>1. Kovan Technologies LATAM: A Definição do Alvo. Business case PL-02-2026, versão v2.</p>"
    "<p>2. datasets_case_modulo2_5yrs.xlsx, base longa de 65 meses. Não distribuída por este acervo.</p></div>\n"
    '          <div class="concept-card"><h3>Métodos citáveis</h3>'
    "<p>3. Ke, G. et al. LightGBM. NeurIPS, 2017. A família do HistGradientBoosting.</p>"
    "<p>4. Breiman, L. Random Forests. Machine Learning, 2001. A importância por permutação.</p>"
    "<p>5. Sculley, D. et al. Hidden Technical Debt in Machine Learning Systems. NeurIPS, 2015.</p></div>\n"
    '          <div class="concept-card"><h3>O que é nosso</h3>'
    "<p>A comparação entre as duas ordenações da fila e as quatro limitações declaradas, organizadas para este módulo.</p></div>\n"
    "        </div>\n",
    conclusao="Todo número desta aula está travado em dados/tests/test_aula07_numeros.py.",
))

# ---------------------------------------------------------------------------
# Esqueleto
# ---------------------------------------------------------------------------
ESQUELETO = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aula 07 &middot; Do script à tela &middot; MBA Inteli x Lenovo</title>

  <!-- Gerado por tools/montar_deck_aula07.py. Nao editar a mao. -->

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
