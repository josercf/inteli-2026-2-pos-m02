# Skill de limpeza: painel de contas Kovan

Instruções de tratamento do painel `kovan_painel_contas.csv`. Este arquivo é
lido por um agente antes de qualquer análise: cole-o no início de uma conversa
no Gemini, ou deixe-o na pasta do projeto para um agente que trabalha sobre
arquivos encontrar.

Preenchido pelo grupo: ____________________   Data: ____ / ____ / 2026

## Objetivo

Produzir a base tratada do painel Kovan, com uma decisão registrada para cada
advertência do Exhibit 3 e com o custo de cada decisão medido em número.

## Regras que valem para toda a execução

1. Não estime, não interpole e não complete nenhum valor ausente que não
   esteja na base. Quando a informação não existir, registre que ela não
   existe.
2. Mostre o código que produziu cada número antes de apresentar esse número.
3. Ao aplicar qualquer tratamento, imprima a contagem de linhas afetadas.
4. Cada passo abaixo termina com duas medidas separadas: a contagem de linhas
   que o tratamento toca, como registro do tamanho da intervenção, e o custo
   medido no indicador que a decisão altera, recalculado sob a alternativa
   escolhida e sob a alternativa descartada.

## Passo 1: perfilamento

Para cada coluna do painel, informe tipo, contagem de nulos, mínimo, máximo e
número de valores distintos. Não trate nada ainda.

## Passo 2: receita ausente (`receita_brl`, `valor_medio_pedido_brl`)

Situação na base: contas ativas com linhas sem receita registrada, por atraso
de fechamento contábil.

Decisão do grupo: PREENCHER

Justificativa em uma frase: ______________________________________________

Linhas afetadas por este tratamento: ______________________________________

Custo medido
  Indicador afetado (sugestão: receita líquida total): ____________________
  Valor do indicador com a decisão acima: __________________________________
  Valor do indicador com a alternativa descartada: _________________________

## Passo 3: engajamento comercial (`visitas_registradas`, `interacoes_crm`)

Situação na base: linhas sem registro de visita nem de interação. A taxa de
ausência varia por segmento.

Decisão do grupo: PREENCHER

Justificativa em uma frase: ______________________________________________

Linhas afetadas por este tratamento: ______________________________________

Custo medido
  Indicador afetado (sugestão: média de visitas por segmento): ____________
  Valor do indicador com a decisão acima: __________________________________
  Valor do indicador com a alternativa descartada: _________________________

## Passo 4: mudança de taxonomia (`taxonomia_mix`, `linhas_produto_ativas`)

Situação na base: a taxonomia de mix muda em 2023Q1. A contagem de linhas de
produto antes desse trimestre e depois dele usa categorias diferentes.

Decisão do grupo: PREENCHER

Justificativa em uma frase: ______________________________________________

Linhas afetadas por este tratamento: ______________________________________

Custo medido
  Indicador afetado (sugestão: média de linhas de produto por trimestre): _
  Valor do indicador com a decisão acima: __________________________________
  Valor do indicador com a alternativa descartada: _________________________

## Passo 5: devoluções (`devolucoes_brl`)

Situação na base: a coluna registra devolução em separado da receita e chega
com sinal negativo.

Decisão do grupo: PREENCHER

Justificativa em uma frase: ______________________________________________

Linhas afetadas por este tratamento: ______________________________________

Custo medido
  Indicador afetado (sugestão: contagem de rupturas): ______________________
  Valor do indicador com a decisão acima: __________________________________
  Valor do indicador com a alternativa descartada: _________________________

## Passo 6: saída

Grave a base tratada. Imprima uma tabela com o indicador de cada um dos
passos 2 a 5, com o valor sob a decisão escolhida e o valor sob a alternativa
descartada lado a lado, e com a contagem de linhas afetadas como coluna
adicional.

## Critério de aceite

Execute este arquivo contra a base crua. Os indicadores da tabela do Passo 6
reproduzem os números que o grupo apresentou na Prática 3. Um valor que não
bate marca uma diferença entre o que este arquivo descreve e o que a mesa
decidiu fazer, e o passo correspondente precisa ser reescrito até fechar.
