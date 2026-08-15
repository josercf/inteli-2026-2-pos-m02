# ADR-003: Gemini como ambiente das práticas e Antigravity como demonstração

- **Data:** 2026-08-15
- **Status:** Aceita
- **Decisores:** José Romualdo (docente da Trilha de Tecnologia)

> **Esta ADR emenda a ADR-002**, que escolheu o Colab com IA integrada como
> ambiente único das práticas. A ADR-002 continua válida no que diz respeito ao
> Colab como ambiente de execução de código e como plano B. O que muda é o
> ambiente em que as práticas do dia acontecem.

## Contexto

A Aula 02 precisa ensinar a diferença entre uma análise conduzida em conversa e
um tratamento registrado em arquivo. O critério que separa os dois ambientes
candidatos é a persistência do trabalho: o que sobra depois que a sessão fecha e
o que outra pessoa consegue reexecutar.

| Critério | Gemini | Antigravity |
|---|---|---|
| Unidade de trabalho | Mensagem numa conversa | Arquivo numa pasta |
| Instalação | Nenhuma | Aplicativo desktop com login |
| Ciclo de resposta | Segundos | Minutos, com plano e execução |
| O que sobra ao fechar | Histórico de conversa | Script, base tratada, log de execução |
| Reexecutável por terceiro | Não | Sim |

As duas primeiras linhas favorecem o Gemini numa sala com 20 pessoas e 3h30 de
bloco. As três últimas são requisito do entregável do dia, que é uma base
tratada auditável.

O Colab com IA integrada, escolhido na ADR-002, atende ao requisito de executar
código na mesma tela. Ele não demonstra um agente que trabalha sobre uma pasta,
que é o comportamento que a Prática 4 precisa mostrar.

A divergência observada na Aula 01 sustenta a mudança: as mesas conduziram
tratamentos ad hoc em conversa e nenhuma delas ficou com registro do que fez.

## Decisão

As quatro práticas da Aula 02 rodam em Gemini. O Antigravity entra em uma faixa
de 10 a 15 minutos, projetada da máquina do professor. O Colab permanece como
plano B declarado no começo da aula, com o notebook do dia já carregado.

## Motivações

- **A comparação entre os dois ambientes é conteúdo da aula.** A turma precisa
  ver o mesmo arquivo Markdown sendo lido nos dois runtimes para entender o que a
  portabilidade significa.
- **O Gemini não exige instalação.** Numa sala de 20 pessoas com máquina
  corporativa, cada passo de instalação custa minutos de bloco e produz
  divergência de estado entre as mesas.
- **O entregável exige registro reexecutável.** O Antigravity mostra o
  comportamento de um agente que abre uma pasta, escreve script e deixa log, que
  é o formato que o aluno leva para o trabalho (ADR-004).

## Riscos conhecidos

- **Instalação do Antigravity em máquina corporativa.** Este risco permanece
  **não verificado** até a data desta ADR. Mitigação: o desenho da aula não
  depende dele. As quatro práticas rodam em Gemini, e o Antigravity aparece
  apenas em demonstração projetada da máquina do professor. Instalação que
  funcione para algum grupo entra como bônus nas notas de condução.
- **Upload de CSV no Gemini pela conta corporativa.** Risco **verificado e
  descartado em 15/08/2026**: o upload do CSV de 1,8 MB foi testado na conta
  corporativa Inteli (Edu, Pro) e funcionou. Mitigação mantida por precaução de
  rede na sala: o notebook do dia fica pronto no Colab, anunciado no começo da
  aula e não no meio da prática.
- **Duas ferramentas na mesma tarde.** Mitigação: o Antigravity ocupa uma faixa
  única de 10 a 15 minutos, sem exigir ação da turma.

## Consequências

- Positivas: o entregável do dia passa a ter um formato reexecutável, a
  diferença entre análise conversacional e tratamento registrado aparece
  demonstrada na tela, e nenhuma prática depende de instalação.
- Negativas: a turma passa a ver duas ferramentas em uma tarde, o que contraria a
  motivação de redução de atrito que sustentou a ADR-002. O atrito é aceito
  porque a comparação entre as duas é o conteúdo do bloco das 16h30. O Colab, que
  era o ambiente único, passa a ocupar o papel de plano B, e as notas de condução
  precisam manter os dois caminhos atualizados.

## ADRs relacionadas

- ADR-001 (painel sintético com os números do case travados)
- ADR-002 (Colab com IA integrada como ambiente das práticas), emendada por esta
- ADR-004 (a skill de agente em Markdown como artefato do aluno)
