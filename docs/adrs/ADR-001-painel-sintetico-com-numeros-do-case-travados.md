# ADR-001: Painel sintético do case, com os números travados por teste

- **Data:** 2026-08-07
- **Status:** Aceita
- **Decisores:** José Romualdo (docente da Trilha de Tecnologia)

## Contexto

O case Kovan (PL-02-2026, v2) descreve com precisão o painel analítico que a
turma vai usar: o Exhibit 3 dá as 20 colunas, as dimensões (1.187 contas por 14
trimestres) e quatro advertências de qualidade. O corpo do case cita dezenas de
números que só fazem sentido se o dado os sustentar: 34 rupturas, prevalência de
2,1%, 192/176/76 episódios nos cortes de 10%, 15% e 25%, captura de 31/29/17
rupturas, desfecho de 56 recuperações, 91 contrações persistentes e 29 rupturas,
e o NRR caindo de 109,0% para 93,0%.

Nada disso existia como arquivo. A nota editorial do próprio case registra o
dataset como "a ser especificado em sessão dedicada, com o insight analítico
embutido descobrível por EDA e não revelado no texto".

As anotações de kickoff apontavam outra direção: como não foi possível usar
dados da Lenovo, o dataset seria substituído por "datasets públicos de mercado",
com o exercício virando transferência de contexto. Há também uma diretriz de
metodologia, herdada do acervo de Graduação, que proíbe dado sintético onde
exista dado aberto real.

## Decisão

Gerar o painel de forma sintética, com a estrutura de episódios escrita conta a
conta de forma explícita, calibrada contra os números impressos no case, e
travada por uma suíte de testes que falha quando qualquer um deles deixa de
fechar.

## Motivações

- **Os números do case são citados em sala.** Um painel público que não os
  sustente obriga a reescrever o case ou a mentir sobre o dado na frente da
  turma. O case v2 foi explicitamente "canonicalizado contra o painel de dados":
  o painel é que precisa obedecer ao case, não o contrário.
- **O insight central precisa ser plantado.** A nota editorial do case prevê um
  achado analítico embutido, descobrível por EDA e não revelado no texto. Numa
  base pública, ou esse padrão não existe, ou existe por acidente, e não há como
  garantir que a turma o encontre em uma tarde. Qual é o achado, com que força
  ele foi plantado e como conduzir a sala até ele estão em
  `docs/notas-do-professor/`, que não é versionado: este arquivo é público e o
  aluno chega nele.
- **As quatro advertências de qualidade são conteúdo de aula.** A Aula 02 inteira
  depende de a receita ausente, as devoluções negativas, a quebra de taxonomia de
  2023 e o engajamento incompleto estarem presentes com magnitude controlada.
- **A diretriz de dado aberto protege contra ilustrar conceito com série
  inventada quando a série real existe.** Aqui não existe série real: nenhuma base
  pública traz painel conta-trimestre de uma operação B2B LATAM com pipeline de
  CRM e rotatividade de território. O risco que a diretriz endereça não se aplica.

## Riscos conhecidos

- **O dado é sintético e a turma vai perceber.** Mitigação: dizer isso na
  primeira aula, em vez de fingir. E introduzir ruído na assinatura plantada:
  uma separação perfeita lê como fabricada, então a assinatura plantada aparece
  com força alta mas não determinística, e o teste que a protege trava a faixa
  nos dois lados (nem separação total, nem sinal fraco demais para ser achado).
- **Números do case que não fecham entre si.** A receita anual do Grupo Talvera
  citada no corpo do texto não bate com a soma dos trimestres do Exhibit 1, e o
  mesmo acontece com o Grupo Andirá. O painel segue o exhibit, que é a fonte mais
  específica, e a divergência fica registrada aqui em vez de ser silenciosamente
  ajustada.
- **Confiança excessiva na suíte de testes.** Mitigação: os testes foram
  verificados contra sete mutações do gerador. Uma delas revelou que o teste do
  Talvera importava a mesma constante que o gerador usava, e passava mesmo com o
  dado alterado; o Exhibit 1 agora está transcrito de forma literal no teste.

## Consequências

- Positivas: o material didático pode citar qualquer número do case sabendo que
  o dado o sustenta; a atividade da tarde tem gabarito verificável; o gerador é
  reutilizável se o case for revisado.
- Negativas: manter o gerador é custo permanente, e qualquer mudança nos números
  do case exige recalibrar e rerodar a suíte.

## ADRs relacionadas

- ADR-002 (Colab com IA integrada como ambiente das práticas)
