# ADR-005: o dataset oficial da Lenovo substitui o painel sintético

- **Data:** 2026-08-22
- **Status:** Aceita
- **Decisores:** José Romualdo (docente da Trilha de Tecnologia)

> **Esta ADR emenda a ADR-001**, que escolheu gerar um painel sintético com os
> números do case travados por teste. A motivação daquela decisão era a ausência
> de base real. Essa ausência acabou.

## Contexto

O dataset oficial da Kovan chegou em 21/08/2026, como
`datasets_case_modulo2.xlsx`, com cinco abas e 24 MB. Três fatos tornam a troca
inevitável e um quarto a torna urgente.

O painel sintético cobria 1.187 contas em 14 trimestres, com colunas em
português e sem coluna de rótulo. A base oficial cobre 8.282 contas em 24 meses,
com colunas em inglês, cinco grãos diferentes e uma coluna `churn_label`
preenchida. Nenhuma análise feita sobre um transfere para o outro.

A turma reclamou da qualidade do painel sintético durante a Aula 02. A
reclamação é procedente no ponto que importa: as advertências plantadas eram
conhecidas de antemão pelo docente, e a sala percebeu isso.

Os artefatos avaliados da Semana 5 e da Semana 9 precisam rodar sobre a base que
a Lenovo reconhece como sua. Um Artefato 1 construído sobre dado sintético não
serve de insumo ao Artefato 2 nem à banca.

A urgência: a Aula 03 é em 22/08, e ela é a primeira depois da chegada da base.

## Decisão

A base oficial passa a ser a única a partir da Aula 03. A substituição é
declarada em sala, no primeiro bloco, e o painel sintético permanece no
repositório apenas como registro das Aulas 01 e 02.

O arquivo **não é versionado**. Ele contém receita conta a conta de uma carteira
LATAM real, e este repositório é público e publica no GitHub Pages. Ele entra no
`.gitignore` e chega à turma pelo mesmo canal em que o docente o recebeu.

## Motivações

- **O achado central sobrevive à troca, e melhora.** O eixo previsto para a
  Aula 03 era o limiar do rótulo como escolha. Na base oficial, o `churn_label`
  é constante por conta e inteiramente determinado pelo último mês de compra,
  com separação perfeita em 08/02/2025. A aula deixa de construir um rótulo
  hipotético e passa a auditar um rótulo real que ninguém documentou.
- **As advertências de qualidade da base oficial não foram plantadas.** A chave
  do engajamento comercial cruza com 36,8% do painel, o grão temporal difere
  entre abas, o cadastro repete 100 contas com setor divergente. Nada disso foi
  desenhado para a aula, e é exatamente por isso que ensina.
- **A troca é o conteúdo, e não um contratempo.** A `skill-limpeza-kovan.md` que
  cada grupo escreveu na Aula 02 prometia portabilidade. Executá-la contra uma
  base que ela nunca viu é o teste que a ADR-004 previu e que não tinha como
  acontecer enquanto a base fosse a mesma.

## Riscos conhecidos

- **A narrativa do case cita números do painel sintético.** O business case fala
  em 1.187 contas, 34 rupturas e segmentos Estratégico, Médio e Cauda. A base
  oficial tem 8.282 contas e seis segmentos em inglês. Mitigação: a
  correspondência mais forte foi verificada e registrada, `STRATEGIC ACCOUNT`
  tem 117 contas contra as 118 do case. Onde os dois divergirem, a base oficial
  prevalece e a divergência entra nas notas de condução.
- **As Aulas 01 e 02 ficam sobre uma base aposentada.** Mitigação aceita: elas
  já aconteceram, e reescrevê-las custaria mais do que vale. O material delas
  permanece no ar com o painel sintético, e a Aula 03 declara a troca.
- **O dataset fora do repositório cria um passo de distribuição.** Mitigação: o
  repositório de clone da turma (ADR-006) traz a estrutura, a skill e o
  `dados/LEIA-ME.md` dizendo onde o arquivo entra, com `.gitignore` que impede
  o aluno de commitá-lo por engano.
- **A suíte de testes fica dependente de um arquivo ausente.**
  `dados/tests/test_dataset_oficial.py` é pulado por inteiro quando o xlsx não
  está presente, e a ausência aparece como skip. Quem clona o acervo público não
  vê a suíte vermelha por não ter um arquivo que não deveria ter.

## Consequências

- Positivas: os artefatos avaliados passam a rodar sobre dado que a Lenovo
  reconhece; o achado da aula é real e verificável pela turma; a reclamação
  sobre a base sintética recebe uma resposta que é conteúdo.
- Negativas: o acervo passa a ter duas bases e duas nomenclaturas de segmento,
  e todo material novo precisa dizer qual delas está usando. Os testes do painel
  sintético continuam rodando e travando números que nenhuma aula futura cita.

## ADRs relacionadas

- ADR-001 (painel sintético com os números do case travados), emendada por esta
- ADR-004 (a skill de agente em Markdown como artefato do aluno)
- ADR-006 (Antigravity como ambiente único e o repositório de clone)
