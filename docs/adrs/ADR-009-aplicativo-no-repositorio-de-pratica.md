# ADR-009: o aplicativo da Aula 07 vive no repositório de prática, e o acervo lê os números dele

- **Data:** 12/09/2026
- **Status:** aceita
- **Decisores:** Prof. José Romualdo da Costa Filho

## Contexto

A Aula 07 entrega um modelo de predição e uma interface. Isso é código de
aplicação, com dependência de scikit-learn, joblib e Streamlit, e com um modelo
treinado em disco. O acervo até aqui só tinha scripts de análise e geradores de
deck.

Duas coisas precisavam de lugar: o aplicativo em si, e os números que o deck
cita sobre ele.

## Decisão

O aplicativo vive em `app/` dentro do repositório de prática
(`inteli-pos-2026-2a-eda`), que a turma já clonou. O acervo não copia esse
código: `dados/analise_aula07.py` importa o pacote `app` do repositório irmão e
lê os números dele.

## Motivações

- O aluno já tem o repositório de prática clonado e o Antigravity aberto nele.
  Um terceiro repositório seria mais um passo de configuração numa tarde de três
  horas.
- O número do slide precisa descrever o que roda na tela. Reimplementar a conta
  no acervo faria os dois divergirem na primeira correção aplicada de um lado
  só, e o deck passaria a citar um aplicativo que não existe.
- O repositório de prática já é o lugar declarado do trabalho do grupo
  (ADR-006).

## Riscos conhecidos

- **O acervo passa a depender de um diretório irmão.** Mitigação:
  `dados/analise_aula07.py` levanta `PraticaAusente` com a mensagem do que
  fazer, e `dados/tests/test_aula07_numeros.py` pula quando o irmão não está
  presente. O CI não mede estes números, e isso está declarado no arquivo de
  teste.
- **Os dois artefatos se misturam.** O Artefato 1 é a análise e o Artefato 2 é o
  aplicativo, e agora os dois moram juntos. Mitigação: `app/` é uma pasta
  isolada, com testes próprios, e o `CHECKLIST-ARTEFATO-1.md` continua na raiz.
- **Dado real e nota de aluno num repositório público.** Ao preparar este commit,
  `git add -A` levou ao stage a planilha de avaliação da banca e
  `dados/raw_data_tratada.csv.gz`: o `.gitignore` cobria `dados/*.csv` mas não a
  extensão `.gz`, e não cobria a raiz. As duas brechas foram fechadas. Vale
  conferir o histórico antes de qualquer publicação.

## Consequências

Positivas:

- O deck da Aula 07 cita números que saem do código que o aluno executa, e a
  suíte do acervo falha se os dois divergirem.
- O grupo recebe um pacote de referência com teste, e não um script solto.

Negativas:

- Rodar a suíte completa do acervo passa a exigir o repositório irmão e a base
  longa para cobrir a Aula 07. Sem eles, 42 testes pulam em silêncio, e pular
  não é passar.
- A dependência é por caminho de sistema de arquivos, e quebra se alguém clonar
  o repositório de prática com outro nome.

## ADRs relacionadas

- [ADR-006](ADR-006-antigravity-como-ambiente-unico.md), que fixou o repositório
  de prática como ambiente de trabalho da turma.
- [ADR-007](ADR-007-corte-temporal-separa-observacao-de-rotulo.md), que define o
  corte que o aplicativo usa.
