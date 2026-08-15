# ADR-004: A skill de agente em Markdown como artefato do aluno

- **Data:** 2026-08-15
- **Status:** Aceita
- **Decisores:** José Romualdo (docente da Trilha de Tecnologia)

## Contexto

O briefing do módulo pede competência transferível: o que a turma pratica na
sala precisa continuar funcionando na segunda-feira, no ambiente de trabalho
deles, onde nem o Gemini nem o Antigravity necessariamente estarão disponíveis.

Três formatos de artefato foram considerados para o entregável da Aula 02:

| Formato | O que sobra ao fechar a sessão | Roda em outro agente |
|---|---|---|
| Prompt salvo no histórico | Texto vinculado à ferramenta e à conversa | Por cópia manual, sem estrutura |
| Notebook exportado | Código executável, preso a Python e ao runtime | Sim, com ambiente Python |
| Arquivo Markdown de instrução | Fluxo declarado em texto estruturado | Sim, em qualquer agente que leia arquivo |

A Aula 01 mostrou o custo de não ter artefato: as mesas conduziram tratamentos
ad hoc em conversa, chegaram a contagens de ruptura diferentes entre si e
nenhuma delas ficou com registro do que fez.

## Decisão

O artefato que o aluno leva da Aula 02 é um arquivo Markdown descrevendo o fluxo
sistemático de tratamento da base: entrada, decisões por advertência, saída e
critério de aceite. O esqueleto é `materiais/skill-limpeza-kovan.md`, preenchido
na Prática 4.

## Motivações

- **A portabilidade entre runtimes é o requisito principal.** O mesmo arquivo é
  colado como instrução no Gemini e lido pelo agente do Antigravity na
  demonstração projetada, o que torna a transferência verificável dentro da aula.
- **O formato obriga a declarar a decisão.** O esqueleto tem uma linha
  obrigatória para cada uma das quatro advertências de qualidade, de modo que
  omitir uma decisão fica visível no artefato.
- **Markdown é legível por pessoa e por agente.** O aluno consegue revisar o
  fluxo sem executar nada, e a revisão em grupo acontece sobre o mesmo texto que
  a ferramenta consome.
- **O critério de aceite fica dentro do artefato.** A skill declara o número que
  a execução precisa reproduzir, o que permite conferir o resultado sem depender
  de memória da sessão.

## Riscos conhecidos

- **O formato de arquivo de instrução varia entre agentes.** Alguns esperam
  cabeçalho YAML, outros um nome de arquivo específico, outros uma pasta
  reservada. Mitigação: o esqueleto usa Markdown puro, sem sintaxe proprietária,
  e o material de apoio registra onde cada agente espera encontrar o arquivo.
- **Texto em linguagem natural admite ambiguidade na execução.** Mitigação: cada
  decisão do esqueleto exige a coluna afetada, o tratamento aplicado e o número
  que ele produz, o que dá um critério de aceite objetivo.
- **O aluno pode preencher o arquivo sem executá-lo.** Mitigação: a Prática 4 tem
  como critério de aceite que o número produzido pela skill bata com o da Prática
  3, o que exige a execução dentro do bloco.

## Consequências

- Positivas: o entregável do dia passa a ser reexecutável por outra pessoa, a
  divergência entre mesas fica rastreável até a decisão que a causou, e o aluno
  sai com um arquivo que funciona no agente do trabalho dele.
- Negativas: preencher o arquivo consome 30 minutos de bloco que poderiam ir para
  análise, e manter o esqueleto atualizado passa a ser trabalho recorrente do
  acervo conforme os agentes mudam de convenção.

## ADRs relacionadas

- ADR-002 (Colab com IA integrada como ambiente das práticas)
- ADR-003 (Gemini como ambiente das práticas e Antigravity como demonstração)
