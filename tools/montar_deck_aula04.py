# -*- coding: utf-8 -*-
"""Monta aulas/aula04.html.

Gerado, nunca editado a mao: a numeracao de rodape e o fechamento de secao sao
garantidos aqui, e ja se perderam no HTML duas vezes.

Diretiva editorial de 15/08/2026: sem paralelismo negativo, sem antitese
simetrica, sem escalada com dois-pontos. Titulo de slide de conteudo e a
conclusao completa, com o numero dentro. Travado por tools/check_retorica.py.

Todo numero do case que aparece aqui esta travado em
dados/tests/test_aula04_numeros.py, que le o dataset oficial da Lenovo.

Uso: python3 tools/montar_deck_aula04.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from tools import deck_kit  # noqa: E402
from tools.deck_kit import conteudo, figura, pratica, quiz, secao  # noqa: E402

SAIDA = RAIZ / "aulas" / "aula04.html"

deck_kit.configurar("Módulo 2 &middot; Aula 04")
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
    "            <h1>A figura que decide</h1>\n"
    "            <h3>Hipóteses de causa do churn, três filtros para validá-las, e a figura que leva a sobrevivente ao Comitê</h3>\n"
    '            <p class="cover-meta">Módulo 2 &middot; Aula 04 &middot; Trilha de Tecnologia</p>\n'
    '            <p class="cover-meta">29 de agosto de 2026 &middot; 13h00 às 16h00</p>\n'
    "          </div>\n"
    "        </div>\n"
    "      </section>\n"
)

# ---------------------------------------------------------------------------
# 2. Resgate
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A Aula 03 deixou pronto o critério do rótulo: última compra até 08/02/2025 marca a conta",
    '        <div class="stat-tiles">\n'
    '          <div class="stat-tile"><p class="stat-numero">8.282</p><p class="stat-rotulo">contas na carteira</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">1.593</p><p class="stat-rotulo">marcadas como perdidas, 19,2%</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">13</p><p class="stat-rotulo">meses de inatividade que o rótulo exige</p></div>\n'
    '          <div class="stat-tile destaque"><p class="stat-numero">24</p><p class="stat-rotulo">meses que o painel cobre</p></div>\n'
    "        </div>\n"
    '        <p class="linha-contexto">Os dois últimos números juntos definem quem o rótulo alcança, e essa é a primeira pergunta de hoje.</p>\n',
    contexto="Quatro seções do Artefato 1 fecharam em 22/08: carga, qualidade, univariada e bivariada.",
    conclusao="Hoje fecham as três restantes: rótulo, visuais e limitações, e o artefato fica completo para 05/09.",
    fonte="Fonte: datasets_case_modulo2.xlsx; dados/analise_aula03.py.",
))

# ---------------------------------------------------------------------------
# 3. A PBL, sem o perfil das contas
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Duas contas caíram mais de 90% e divergiram",
    '        <table class="tabela-criterios compacta numerica">\n'
    "          <thead><tr><th>Critério</th><th>Conta A</th><th>Conta B</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Segmento e país</td><td>GLOBAL ACCOUNT, Brasil</td><td>GLOBAL ACCOUNT, Brasil</td></tr>\n"
    "            <tr><td>Primeira compra</td><td>abril de 2024</td><td>abril de 2024</td></tr>\n"
    "            <tr><td>Receita no 1º semestre do painel</td><td>USD 270.790</td><td>USD 134.697</td></tr>\n"
    "            <tr><td>Receita no 2º semestre</td><td>USD 2.499</td><td>USD 1.840</td></tr>\n"
    "            <tr><td>Rótulo</td><td>seguiu na base</td><td>perdida</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="Entre 66 contas com queda acima de 70% entre semestres e seis ou mais meses ativos, 63 seguem na base e 3 foram marcadas.",
    conclusao="A hipótese escrita antes do número é a única que pode perder, sem abrir a base.",
    fonte="Fonte: dados/analise_aula04.py, par_da_pbl.",
))

# ---------------------------------------------------------------------------
# 4. Contrato
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Contrato e escopo da tarde",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Item</th><th>O que vale hoje</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Contrato</td><td>Nenhuma figura entra no artefato sem o teste que a sustenta escrito embaixo: intervalo, qui-quadrado ou estratificação, e a população.</td></tr>\n"
    "            <tr><td>Ambiente</td><td>Antigravity, sobre a pasta clonada, com duas skills novas em <code>skills/</code>.</td></tr>\n"
    "            <tr><td>Método</td><td>13h00 às 14h20 e 14h40 às 14h55: três filtros para uma hipótese de causa, e a figura da sobrevivente.</td></tr>\n"
    "            <tr><td>Oficina</td><td>14h55 às 15h45, seções 05, 06 e 07 do Artefato 1. Checkpoint às 15h30.</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
))

# ---------------------------------------------------------------------------
# 5. Divisor
# ---------------------------------------------------------------------------
SLIDES.append(secao("01", "Quem podia ser marcado", "Censura: a população que o rótulo alcança",
                    ["Treze meses de inatividade", "Painel de 24 meses", "Primeira compra até 2025-02"]))

# ---------------------------------------------------------------------------
# 6. As três populações
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "4.534 contas não podem ser marcadas pelo rótulo",
    '        <table class="tabela-criterios compacta numerica">\n'
    "          <thead><tr><th>População</th><th>Contas</th><th>Perdidas</th><th>Prevalência</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Carteira inteira</td><td>8.282</td><td>1.593</td><td>19,2%</td></tr>\n"
    '            <tr class="fragment"><td>Primeira compra até 2025-02 (elegíveis)</td><td>3.748</td><td>1.593</td><td>42,5%</td></tr>\n'
    '            <tr class="fragment"><td>Primeira compra de 2025-03 em diante</td><td>4.534</td><td>0</td><td>0,0%</td></tr>\n'
    "          </tbody>\n"
    "        </table>\n"
    '        <p class="linha-contexto fragment">O rótulo exige treze meses sem compra; quem entrou em março de 2025 teve no máximo doze meses de painel.</p>\n',
    contexto="Censura (Janela Insuficiente): o desfecho pode até existir, mas a janela de observação não teve tempo de alcançar parte das contas.",
    conclusao="Toda hipótese de causa testada na carteira inteira mistura quem não perdeu com quem não teve tempo de perder. Hoje testamos nas 3.748 elegíveis.",
    fonte="Fonte: dados/analise_aula04.py, populacoes.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 7. Perfil de compra por segmento
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A perda vai de 25,4% a 58,1% conforme o segmento",
    '        <table class="tabela-criterios compacta numerica">\n'
    "          <thead><tr><th>Segmento</th><th>Contas</th><th>Prevalência</th><th>Receita</th><th>Dias</th><th>Marcas</th><th>Intervalo</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Setor público</td><td>449</td><td>58,1%</td><td>42.388</td><td>3</td><td>3</td><td>18</td></tr>\n"
    "            <tr><td>Mid market</td><td>1.508</td><td>47,5%</td><td>10.016</td><td>2</td><td>2</td><td>45,5</td></tr>\n"
    "            <tr><td>Small market</td><td>366</td><td>47,3%</td><td>7.692</td><td>2</td><td>1</td><td>20</td></tr>\n"
    "            <tr><td>Grandes contas</td><td>786</td><td>33,5%</td><td>36.926</td><td>4</td><td>3</td><td>24</td></tr>\n"
    "            <tr><td>Contas globais</td><td>568</td><td>28,5%</td><td>56.294</td><td>4</td><td>3</td><td>16</td></tr>\n"
    "            <tr><td>Estratégicas</td><td>71</td><td>25,4%</td><td>125.757</td><td>8</td><td>4</td><td>12</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="3.748 elegíveis; medianas por segmento. É perfil: a causa vem nos filtros seguintes.",
    conclusao="Setor público, com 3 dias e 3 marcas, perde 58,1%, mais que as estratégicas, "
              "com 8 dias, 4 marcas e 25,4%.",
))

# ---------------------------------------------------------------------------
# 8. Prática 1, enquadramento
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    1, "A população elegível e o perfil de compra por segmento", 20,
    "Em grupo, na pasta clonada", "perfil_por_segmento.csv em analises/, com a leitura escrita",
    "Cada mesa diz quantas contas ficaram fora e qual segmento compra menos vezes",
    [
        {"acao": "A skill nova faz o corte de elegibilidade antes de medir.",
         "detalhe": "Confira o primeiro resultado: a prevalência das não elegíveis precisa ser zero. Se não for, o critério do rótulo está errado na sua pasta."},
        {"acao": "Cinco medidas no grão da conta, de três abas diferentes.",
         "detalhe": "Receita e marcas vêm de uma aba cada; dias de compra e intervalo vêm da aba de pedidos. A junção perde contas, e a skill pede o número."},
        {"acao": "A leitura escrita diz o que a tabela não mede.",
         "detalhe": "Intervalo entre compras não existe para quem comprou em um único dia. Canal é constante. Engajamento cobre 1.560 contas elegíveis."},
    ],
    "A mesa apresenta a tabela com as três populações e o perfil dos seis segmentos",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 9. Prática 1, passos
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    1, "Passos 1 e 2, elegibilidade e perfil", 20, "", "", "",
    [
        {"acao": "Peça a elegibilidade.",
         "prompt": "Execute skills/perfil-por-segmento.md, Passo 1, sobre dados/datasets_case_modulo2.xlsx. Traga contas, perdidas e prevalência das três populações.",
         "detalhe": "Confira: 8.282 no total, e as duas partes somam isso."},
        {"acao": "Peça o perfil.",
         "prompt": "Agora o Passo 2 e o Passo 3 da mesma skill: as cinco medidas por segmento, nas elegíveis, e quantas contas ficaram sem intervalo em cada segmento.",
         "detalhe": "Confira: o segmento com maior receita mediana tem mais dias de compra? Se a ordem não fizer sentido, peça o código e leia a junção."},
    ],
    "A tabela traz o tamanho da base em cada linha e a leitura de duas frases por segmento",
    ambiente=AMBIENTE, trilho=False,
    sobrelinha="Prática 1 &middot; um pedido por vez, com conferência entre eles",
))

# ---------------------------------------------------------------------------
# 10. Divisor
# ---------------------------------------------------------------------------
SLIDES.append(secao("02", "A diferença é maior que o ruído", "Intervalo de confiança e qui-quadrado, pela pergunta que respondem",
                    ["Quanto o acaso explica", "Intervalo de Wilson", "Qui-quadrado da tabela"]))

# ---------------------------------------------------------------------------
# 11. A pergunta antes da fórmula
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Uma diferença de 10 pontos entre dois grupos de 30 contas cabe inteira dentro do acaso",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Pergunta</th><th>Ferramenta</th><th>O que ela devolve</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Qual a faixa de valores compatível com esta proporção, dado o tamanho da base?</td><td>Intervalo de confiança de 95% (Wilson)</td><td>Um piso e um teto. Dois intervalos que se cruzam não sustentam diferença.</td></tr>\n"
    "            <tr><td>A distribuição do rótulo entre as categorias desta tabela poderia ser acaso?</td><td>Qui-quadrado de contingência</td><td>Uma estatística, os graus de liberdade e um p. Abaixo de 0,05, o acaso deixa de ser explicação confortável.</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="Nenhuma das duas diz se a diferença importa para o negócio, nem se ela é causa. Elas só eliminam o acaso como explicação.",
    conclusao="O primeiro filtro de uma hipótese é o ruído: diferença que cabe no intervalo não vai para a figura.",
))

# ---------------------------------------------------------------------------
# 12. Figura didática: IC
# ---------------------------------------------------------------------------
SLIDES.append(figura(
    "Com 600 contas por grupo, a mesma diferença de 10 pontos sai do acaso",
    "aula04-ic-didatico.png",
    "Quatro barras horizontais com intervalos de confiança: dois grupos de 30 contas com intervalos que se cruzam, e dois grupos de 600 contas com intervalos separados",
    conclusao="O tamanho da base decide o que a prevalência consegue afirmar; sem base, ela é só adjetivo.",
))

# ---------------------------------------------------------------------------
# 13. Figura real: prevalência por segmento com IC
# ---------------------------------------------------------------------------
SLIDES.append(figura(
    "O setor público perde 58,1% das contas elegíveis",
    "aula04-prevalencia-elegiveis.png",
    "Barras horizontais de prevalência de churn por segmento nas contas elegíveis, com intervalo de confiança de 95% em cada barra e a linha da carteira elegível em 42,5%",
    conclusao="Qui-quadrado de 143,8 com 5 gl: segmento separa o rótulo do acaso.",
    fonte="Fonte: dados/analise_aula04.py, tabela_com_ic(\"segmento\").",
))

# ---------------------------------------------------------------------------
# 14. Três hipóteses do caderno, testadas nas elegíveis
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "A perda cai de 66,4% para 16,1% com mais marcas",
    '        <table class="tabela-criterios compacta numerica">\n'
    "          <thead><tr><th>Hipótese</th><th>Categoria</th><th>Contas</th><th>Prevalência</th><th>IC 95%</th><th>Qui-quadrado</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td rowspan=\"4\">Amplitude de mix</td><td>1 marca</td><td>1.086</td><td>66,4%</td><td>63,5% a 69,1%</td><td rowspan=\"4\">615,4, 3 gl</td></tr>\n"
    "            <tr><td>2 marcas</td><td>915</td><td>51,5%</td><td>48,2% a 54,7%</td></tr>\n"
    "            <tr><td>3 marcas</td><td>640</td><td>34,8%</td><td>31,3% a 38,6%</td></tr>\n"
    "            <tr><td>4 ou mais</td><td>1.107</td><td>16,1%</td><td>14,0% a 18,4%</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="3.748 contas elegíveis. Canal tem valor único e não testa nada; engajamento cobre 1.560 contas.",
    conclusao="Mix passa pelo filtro do ruído; canal é Insuficiente por construção, e engajamento por cobertura.",
    fonte="Fonte: dados/analise_aula04.py, tabela_com_ic.",
))

# ---------------------------------------------------------------------------
# 14b. Os tres andares dos setores, com a mega-conta de licitacao
# ---------------------------------------------------------------------------
# Tabela, e nao a figura de 13 barras: a figura completa tem 490px de altura e
# nao cabe no orcamento vertical de um slide com fecho. Ela vive na secao 6 do
# material de apoio; aqui entra o resumo em tres andares.
SLIDES.append(conteudo(
    "Governo perde 59,7% e quatro setores ficam sem veredito",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Andar</th><th>Setores</th><th>Prevalência</th><th>O que o intervalo autoriza</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Topo</td><td>GOVERNMENT (310) e EDUCATION (189)</td><td>59,7% e 55,6%</td><td>Intervalos acima do de WHOLESALE (34,1%)</td></tr>\n"
    "            <tr><td>Miolo</td><td>Sete setores; o maior: COMMUNICATIONS (1.041)</td><td>34,1% a 46,3%</td><td>Intervalos que se cruzam entre vizinhos</td></tr>\n"
    "            <tr><td>Base pequena</td><td>POWER, UNCLASSIFIED, OIL e INSURANCE</td><td>36,0% a 54,3%</td><td>Menos de 90 contas: veredito Insuficiente</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto='Contas elegíveis, 13 setores do cadastro. <strong class="destaque">Atenção: Setor do cadastro ≠ Segmento do painel.</strong>',
    conclusao="Setores de ciclo longo parecem liderar a inatividade, mas é preciso cuidado com a composição dessa prevalência.",
    fonte="Fonte: dados/analise_aula04.py, perfil_por_setor.",
))

# ---------------------------------------------------------------------------
# 14c. A mega-conta de licitação
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "O perigo do número agregado: licitação lida como churn",
    '        <div class="stat-tiles">\n'
    '          <div class="stat-tile destaque"><p class="stat-numero">65,7%</p><p class="stat-rotulo">da receita perdida elegível na base toda</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">USD 147,3 mi</p><p class="stat-rotulo">em uma única conta</p></div>\n'
    '          <div class="stat-tile"><p class="stat-numero">1</p><p class="stat-rotulo">dia de compra (janeiro/25)</p></div>\n'
    "        </div>\n",
    contexto="A ilusão da alta prevalência no setor de Governo esconde uma única operação atípica.",
    conclusao="Intervir na causa raiz depende de isolar essas anomalias. Prevalência alta com ciclo de licitação por trás pode ser falso positivo em massa.",
    fonte="Fonte: dados/analise_aula04.py, conta_c.",
))

# ---------------------------------------------------------------------------
# 15. Prática 2, enquadramento
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    2, "Uma hipótese do caderno, testada contra o ruído", 20,
    "Em grupo, na pasta clonada", "bivariada.md com a tabela, o intervalo, o qui-quadrado e o veredito",
    "Cada mesa lê o veredito e o intervalo da categoria mais extrema",
    [
        {"acao": "Escolha uma hipótese que a mesa acredita e que pode perder.",
         "detalhe": "Marcas, setor, região ou marca comprada. O critério de refutação vai escrito antes de rodar: qual resultado derruba a hipótese."},
        {"acao": "A skill de bivariada ganhou o Passo 1a, e ele roda primeiro.",
         "detalhe": "Se o agente testar na carteira inteira, a prevalência de 19,2% aparece na tabela. É o sinal de que o corte não foi feito."},
        {"acao": "Veredito em uma de três palavras.",
         "detalhe": "Confirmada, Contraditada ou Insuficiente, como no caderno da Aula 01. Categoria com menos de 30 contas entra marcada."},
    ],
    "A mesa enuncia o veredito e mostra o intervalo da categoria que o sustenta",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 16. Prática 2, passos
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    2, "Passos 1 e 2, a tabela e o teste", 20, "", "", "",
    [
        {"acao": "Peça a tabela com intervalo.",
         "prompt": "Execute skills/bivariada.md, Passos 1a e 2, cruzando churn_label com [sua variável] nas contas elegíveis. Inclua o intervalo de confiança de 95% (Wilson) de cada categoria.",
         "detalhe": "Confira: a soma das contas bate com 3.748? Categoria abaixo de 30 contas marcada?"},
        {"acao": "Peça o qui-quadrado e o veredito.",
         "prompt": "Calcule o qui-quadrado de contingência desta tabela, com graus de liberdade e p. Depois escreva o veredito contra o critério de refutação que eu escrevi.",
         "detalhe": "Confira: o veredito cita o intervalo, e não só o p? Um p pequeno com intervalos que se cruzam nas categorias que importam pede cautela."},
    ],
    "O bivariada.md traz tabela, intervalo, qui-quadrado e o veredito com o critério escrito antes",
    ambiente=AMBIENTE, trilho=False,
    sobrelinha="Prática 2 &middot; um pedido por vez, com conferência entre eles",
))

# ---------------------------------------------------------------------------
# 17. Divisor
# ---------------------------------------------------------------------------
SLIDES.append(secao("03", "A hipótese sobrevive ao controle", "Estratificação por segmento, por frequência e por país",
                    ["Sobrevive", "Desaparece", "Inverte"]))

# ---------------------------------------------------------------------------
# 18. Figura didática: estratificação
# ---------------------------------------------------------------------------
SLIDES.append(figura(
    "Uma diferença de 30 pontos no total pode ser zero dentro de cada estrato",
    "aula04-estratificacao-didatica.png",
    "Barras de prevalência de dois grupos no total e em dois estratos: no total o grupo X perde 65% e o Y 35%; dentro de cada estrato os dois perdem o mesmo",
    conclusao="O segundo filtro é o confundidor: uma associação que some dentro dos estratos era composição, e a variável era proxy do fator de estratificação.",
))

# ---------------------------------------------------------------------------
# 19. Mix sobrevive por segmento
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "O mix se mantém em todos os cinco segmentos",
    '        <table class="tabela-criterios compacta numerica">\n'
    "          <thead><tr><th>Segmento</th><th>1 marca</th><th>Prevalência</th><th>3 ou mais</th><th>Prevalência</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Contas globais</td><td>133</td><td>63,2%</td><td>307</td><td>11,4%</td></tr>\n"
    "            <tr><td>Grandes contas</td><td>196</td><td>66,8%</td><td>413</td><td>14,3%</td></tr>\n"
    "            <tr><td>Mid market</td><td>466</td><td>67,4%</td><td>601</td><td>25,1%</td></tr>\n"
    "            <tr><td>Setor público</td><td>83</td><td>84,3%</td><td>273</td><td>46,9%</td></tr>\n"
    "            <tr><td>Small market</td><td>192</td><td>57,3%</td><td>105</td><td>22,9%</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="Contas elegíveis. Em todos os cinco, o teto de três ou mais marcas fica abaixo do piso de uma marca; estratégicas ficam fora, com poucas contas.",
    conclusao="Controlada por segmento, a hipótese do mix sobrevive, mas falta o fator que o perfil de compra apontou.",
    fonte="Fonte: dados/analise_aula04.py, estratificar(\"marcas\", 1, 3, \"segmento\").",
))

# ---------------------------------------------------------------------------
# 20. Figura real: mix desaparece por frequência
# ---------------------------------------------------------------------------
SLIDES.append(figura(
    "Controlado pela frequência, o mix desaparece",
    "aula04-marcas-por-dias.png",
    "Barras pareadas de prevalência para contas de uma marca e de três ou mais marcas, em quatro faixas de dias de compra, com intervalos de confiança que se cruzam em três das quatro faixas",
    conclusao="Em três das quatro faixas os intervalos se cruzam: 2 dias, 52,5% contra 53,4%; "
              "3 a 5, 21,4% contra 20,3%; 6+, 9,3% contra 5,2%. Na de 1 dia a relação inverte: "
              "81,5% contra 92,5%.",
))

# ---------------------------------------------------------------------------
# 21. Brasil inverte
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Segmento explica 28,2% no Brasil e 12,5% no México",
    '        <table class="tabela-criterios compacta numerica">\n'
    "          <thead><tr><th>Segmento (elegíveis)</th><th>Brasil</th><th>Prevalência</th><th>Outros países</th><th>Prevalência</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Contas globais</td><td>161</td><td>18,6%</td><td>407</td><td>32,4%</td></tr>\n"
    "            <tr><td>Grandes contas</td><td>381</td><td>31,2%</td><td>405</td><td>35,6%</td></tr>\n"
    "            <tr><td>Mid market</td><td>1.168</td><td>48,2%</td><td>340</td><td>45,0%</td></tr>\n"
    "            <tr><td>Setor público</td><td>346</td><td>60,1%</td><td>103</td><td>51,5%</td></tr>\n"
    "            <tr><td>Small market</td><td>73</td><td>72,6%</td><td>293</td><td>41,0%</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    contexto="69,7% das contas elegíveis do Brasil estão em mid market e setor público, contra 28,1% nos outros países.",
    conclusao="A diferença entre países é composição de segmentos, e ela inverte dentro das contas globais.",
    fonte="Fonte: dados/analise_aula04.py, estratificar(\"regiao\", \"BR\", \"outros\", \"segmento\") e composicao_br.",
))

# ---------------------------------------------------------------------------
# 22. Frequência como vazamento
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Um único dia de compra já indica 85,4% de churn",
    '        <table class="tabela-criterios compacta numerica">\n'
    "          <thead><tr><th>Dias de compra</th><th>Contas</th><th>Prevalência</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>1</td><td>1.194</td><td>85,4%</td></tr>\n"
    "            <tr><td>2</td><td>620</td><td>52,3%</td></tr>\n"
    "            <tr><td>3 a 5</td><td>861</td><td>22,0%</td></tr>\n"
    "            <tr><td>6 ou mais</td><td>1.073</td><td>5,6%</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n"
    '        <p class="linha-contexto">Uma conta com um único dia de compra, em 2024, já está a treze meses ou mais sem comprar: a variável conta o desfecho.</p>\n',
    contexto="Qui-quadrado de 1.671,4 com 3 graus de liberdade, o maior da tarde.",
    conclusao="O terceiro filtro é o vazamento: usar uma variável que já é a própria resposta disfarçada (construída com a informação do rótulo).",
    fonte="Fonte: dados/analise_aula04.py, tabela_com_ic(\"faixa_dias\").",
))

# ---------------------------------------------------------------------------
# 23. Quiz
# ---------------------------------------------------------------------------
SLIDES.append(quiz(
    "Verificação",
    "Venda cruzada como retenção?",
    "Uma marca perde 66,4% e quatro ou mais perdem 16,1%, com intervalos que não se cruzam. O diretor comercial propõe uma campanha de venda cruzada para reter. O que você diz?",
    [
        {"texto": "A campanha se sustenta: a diferença passou no teste de ruído.",
         "certa": False, "certo": "",
         "errado": "Passar no ruído elimina o acaso, e só isso. A associação some quando controlada pela frequência de compra."},
        {"texto": "É composição: quem compra mais vezes compra mais marcas.",
         "certa": True,
         "certo": "Em três das quatro faixas de dias de compra, uma marca e três ou mais perdem "
                  "igual; na faixa de 1 dia a relação inverte. O mix é proxy da frequência.",
         "errado": ""},
        {"texto": "Falta o qui-quadrado para decidir, e o p vai responder.",
         "certa": False, "certo": "",
         "errado": "O qui-quadrado já foi calculado, 615,4 com 3 gl. Ele responde sobre o acaso, e a pergunta aqui é sobre confundidor."},
        {"texto": "A hipótese é Insuficiente: a base não tem a variável certa.",
         "certa": False, "certo": "",
         "errado": "A base tem a variável, e ela foi testada. O resultado é Contraditada sob controle, que é um veredito."},
    ],
    {"fichas": [("1 marca", "66,4%"), ("4 ou mais", "16,1%"), ("Sob controle por frequência", '<span class="numerao">cruzam</span>')]},
))

# ---------------------------------------------------------------------------
# 24. Divisor
# ---------------------------------------------------------------------------
SLIDES.append(secao("04", "A figura que decide", "Forma pela pergunta, título como conclusão, teste embaixo",
                    ["Histograma, boxplot, scatterplot", "O número no título", "A linha de capacidade"]))

# ---------------------------------------------------------------------------
# 25. Forma pela pergunta
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Forma da figura pela pergunta",
    '        <table class="tabela-criterios compacta">\n'
    "          <thead><tr><th>Pergunta</th><th>Forma</th><th>O que vai junto</th></tr></thead>\n"
    "          <tbody>\n"
    "            <tr><td>Como a variável se distribui?</td><td>Histograma</td><td>Escala log se assimetria > 3</td></tr>\n"
    "            <tr><td>Onde está a maioria por grupo?</td><td>Boxplot</td><td>Escala e base iguais</td></tr>\n"
    "            <tr><td>Duas variáveis andam juntas?</td><td>Scatterplot</td><td>Nº de pontos e alternativa</td></tr>\n"
    "            <tr><td>Proporção difere por categoria?</td><td>Barras com IC</td><td>Intervalo e qui-quadrado</td></tr>\n"
    "            <tr><td>Duas contas divergem no tempo?</td><td>Séries</td><td>Eixo e corte marcados</td></tr>\n"
    "          </tbody>\n"
    "        </table>\n",
    conclusao="Figura sem teste embaixo é ilustração; com o teste, ela sustenta uma decisão.",
))

# ---------------------------------------------------------------------------
# 26. Figura real: fila por segmento
# ---------------------------------------------------------------------------
SLIDES.append(figura(
    "Cinco segmentos passam de 138 por trimestre",
    "aula04-fila-por-segmento.png",
    "Barras horizontais de contas marcadas como perdidas por segmento nas elegíveis, com a linha de capacidade operacional em 138",
    conclusao="Mid market 716; grandes contas 263; setor público 261; small market 173; contas globais 162.",
    fonte="Fonte: dados/analise_aula04.py, fila_por_segmento.",
))

# ---------------------------------------------------------------------------
# 27. Figura real: o par da PBL
# ---------------------------------------------------------------------------
SLIDES.append(figura(
    "Duas contas se separam no corte do rótulo",
    "aula04-par-pbl.png",
    "Séries mensais de receita de duas contas lado a lado, de abril de 2024 a março de 2026, com a linha do corte do rótulo em fevereiro de 2025",
    conclusao="Conta A voltou a comprar em 2025; Conta B parou em 2024.",
))

# ---------------------------------------------------------------------------
# 28. Prática 3, única
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    3, "A figura da hipótese que sobreviveu", 15,
    "Em grupo, na pasta clonada", "Uma figura em figuras/ e a entrada dela em visuais.md",
    "Cada mesa projeta a figura e lê o título e a linha de teste",
    [
        {"acao": "Reestratifique a hipótese da Prática 2 por um segundo fator.",
         "prompt": "Execute skills/bivariada.md, Passo 4a, sobre a hipótese que testei, estratificando por faixa de dias de compra. Diga se ela sobrevive, desaparece ou inverte.",
         "detalhe": "Se ela desaparecer, a figura é a da estratificação, e o título diz isso."},
        {"acao": "Produza a figura com a skill nova.",
         "prompt": "Execute skills/figura-que-decide.md sobre o resultado: escolha a forma pela pergunta, escreva o título como conclusão com o número, desenhe o intervalo e escreva o teste embaixo.",
         "detalhe": "Confira: o título tem número? A linha embaixo diz a população e o teste?"},
    ],
    "A figura tem título com número, intervalo desenhado e o teste escrito embaixo",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 29. Divisor: oficina
# ---------------------------------------------------------------------------
SLIDES.append(secao("05", "Oficina do Artefato 1", "Seções 05, 06 e 07, das 14h55 às 15h45",
                    ["Rótulo, com a população elegível", "Visuais, com o teste embaixo", "Limitações, a começar pela causa"]))

# ---------------------------------------------------------------------------
# 30. Oficina
# ---------------------------------------------------------------------------
SLIDES.append(pratica(
    4, "Oficina do Artefato 1, seções 05, 06 e 07", 50,
    "Em grupo, três estações de tempo marcado", "A pasta do grupo com as sete seções reexecutáveis",
    "Checkpoint às 15h30: cada mesa mostra a seção mais atrasada",
    [
        {"acao": "Estação 1, 15 minutos: rótulo (seção 05).",
         "detalhe": "O critério recuperado na Aula 03, mais a população que ele consegue marcar e a contagem das 4.534 que ficam fora. Três cortes alternativos com o tamanho da fila."},
        {"acao": "Estação 2, 20 minutos: visuais (seção 06).",
         "detalhe": "Uma figura por segmento da segmentação do grupo, com o teste escrito embaixo. É o insumo que a manhã do Prof. Donaire pede."},
        {"acao": "Estação 3, 15 minutos: limitações (seção 07).",
         "detalhe": "A causa que o dado observacional não fecha, dita com a associação que sobreviveu. O que a base não responde e o dado que faltaria."},
    ],
    "Outra pessoa clona a pasta, coloca o dataset em dados/ e obtém as mesmas figuras",
    ambiente=AMBIENTE,
))

# ---------------------------------------------------------------------------
# 31. Amarração
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "O Artefato 1 fecha hoje com sete seções, e a pergunta da Aula 05 é se um rótulo que não alcança 55% da carteira serve de alvo",
    '        <div class="linha-tempo">\n'
    '          <div class="etapa fragment"><p class="quando">29/08 &middot; hoje</p><h3>Fica pronto</h3>'
    "<p>Rótulo, visuais e limitações, e três filtros para qualquer hipótese de causa.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">Trilha de Negócios</p><h3>Segmentação e personas</h3>'
    "<p>As figuras da seção 06, e a fila real (1.593) vs capacidade (138), sustentam o mapa valor contra risco da manhã.</p></div>\n"
    '          <div class="etapa avaliada fragment"><p class="quando">05/09 &middot; Semana 5</p><h3>Artefato 1 e veredito de alvo</h3>'
    "<p>Entrega binária com feedback cruzado, e o fechamento da recomendação de alvo com número.</p></div>\n"
    '          <div class="etapa fragment"><p class="quando">12/09 &middot; Aula 06</p><h3>Feature engineering</h3>'
    "<p>Recência, frequência e valor, sobre a população elegível, e o vazamento temporal que a frequência de hoje antecipou.</p></div>\n"
    "        </div>\n",
    conclusao="4.534 contas não têm como estar marcadas pelo rótulo entregue. Esse número é metade do argumento do veredito de alvo.",
    por_passos=True,
))

# ---------------------------------------------------------------------------
# 32. Referências
# ---------------------------------------------------------------------------
SLIDES.append(conteudo(
    "Referências e nota metodológica",
    '        <div class="concept-cards">\n'
    '          <div class="concept-card"><h3>Caso e dados</h3>'
    "<p>1. Kovan Technologies LATAM: A Definição do Alvo. Business case PL-02-2026, versão v2.</p>"
    "<p>2. datasets_case_modulo2.xlsx, base oficial recebida em 21/08/2026. Não distribuída por este acervo.</p></div>\n"
    '          <div class="concept-card"><h3>Métodos citáveis</h3>'
    "<p>3. Wilson, E. B. Probable inference. JASA, 1927.</p>"
    "<p>4. Pearson, K. On the criterion. Phil. Magazine, 1900.</p>"
    "<p>5. Simpson, E. H. Interaction in Contingency Tables. JRSS B, 1951.</p>"
    "<p>6. Kaufman, S. et al. Leakage in Data Mining. ACM TKDD, 2012.</p></div>\n"
    '          <div class="concept-card"><h3>O que é nosso</h3>'
    "<p>Os três filtros de causa, o critério de elegibilidade e as duas skills de agente, organizados para este módulo.</p></div>\n"
    "        </div>\n",
    conclusao="Todo número desta aula está travado em dados/tests/test_aula04_numeros.py.",
))

# ---------------------------------------------------------------------------
# Esqueleto
# ---------------------------------------------------------------------------
ESQUELETO = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aula 04 &middot; A figura que decide &middot; MBA Inteli x Lenovo</title>

  <!-- Gerado por tools/montar_deck_aula04.py. Nao editar a mao: a numeracao de
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
