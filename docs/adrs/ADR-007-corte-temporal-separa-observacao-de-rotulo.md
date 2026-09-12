# ADR-007: o corte temporal em 2025-02 separa observação de rótulo

- **Data:** 12/09/2026
- **Status:** aceita
- **Decisores:** Prof. José Romualdo da Costa Filho

## Contexto

A partir da Aula 06 o acervo deixa de descrever a carteira e passa a construir
as colunas de entrada de um modelo de classificação. O rótulo recuperado na
Aula 03 marca a conta cuja última compra aconteceu até 08/02/2025, o que
equivale a treze meses de inatividade contados do fim do painel, em 2026-03.

Até a Aula 05, toda medida do acervo foi calculada sobre o painel inteiro, de
2024-04 a 2026-03, e isso estava correto: análise exploratória descreve o que
aconteceu. Manter esse hábito na construção de features produz colunas que leem
o mesmo período que define o alvo, e o modelo passa a receber a resposta junto
com a pergunta.

## Decisão

O painel é particionado em 2025-02. Features são calculadas apenas com dado de
2024-04 a 2025-02 (11 meses) e o alvo é determinado apenas com dado de 2025-03 a
2026-03 (13 meses).

## Motivações

- A data não é escolha de conveniência: treze meses antes de 2026-03 cai em
  2025-02, e qualquer outro corte faria a janela de features invadir a janela do
  alvo ou descartaria meses observáveis sem contrapartida.
- As duas janelas somam os 24 meses do painel, sem buraco e sem sobreposição.
- O corte representa o instante em que a previsão seria feita na operação. Uma
  coluna que não existe naquele instante não pode entrar no modelo, qualquer que
  seja o ganho de métrica que ela traga.
- A diferença é mensurável e vira conteúdo de aula. A recência lida no fim do
  painel entrega AUC de 0,994 e reproduz o rótulo em 89,8% das contas; a mesma
  fórmula lida no corte entrega 0,772. O escore conjunto sai de 0,794 para 0,995
  quando a coluna vazada entra.

## Riscos conhecidos

- **A janela de observação fica curta.** Com 11 meses não cabe feature de
  histórico de 12 meses nem comparação ano contra ano. Mitigação: a base longa
  de 65 meses, recebida em 12/09/2026, permite reposicionar o corte deixando
  anos de histórico atrás dele. Enquanto ela não é migrada, a limitação fica
  declarada no material.
- **O corte é único.** Um só par de janelas produz um só exemplo por conta.
  Mitigação: com a base longa, vários cortes sobre a mesma carteira, o que
  também permite verificar se o peso das variáveis é estável no tempo.
- **A regra pode ser burlada sem má intenção.** Alguém filtra o painel mensal
  pelo corte e esquece a tabela de pedidos. Mitigação: o teste em
  `dados/tests/test_aula06_numeros.py` recalcula as sete colunas sobre um painel
  truncado no corte e exige que nenhum valor mude em nenhuma das 3.748 linhas.
  Esse teste foi visto falhando: incluir `recencia_fim` na lista verificada
  produz 3.748 diferenças.

## Consequências

Positivas:

- Toda coluna de entrada do módulo passa a ter data de corte declarada, e a
  auditoria de vazamento vira verificação mecânica em vez de leitura atenta.
- O grupo recebe uma função parametrizada pela data de corte, que é o que
  permite reexecutar o pipeline sobre a base longa sem reescrever o código.

Negativas:

- Os números da Aula 04 e da Aula 06 não são comparáveis de forma direta: a
  primeira mede a carteira inteira do painel, a segunda mede a janela de
  observação. Quem cruzar as duas tabelas sem notar isso encontra divergência
  onde não há erro.
- A prevalência de 42,5% da população elegível continua sendo a base de
  comparação, e ela não é a prevalência da carteira (19,2%).

## ADRs relacionadas

- [ADR-005](ADR-005-dataset-oficial-substitui-painel-sintetico.md), que trouxe o
  dataset oficial de onde saem as duas janelas.
