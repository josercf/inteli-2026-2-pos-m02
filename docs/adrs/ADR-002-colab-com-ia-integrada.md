# ADR-002: Colab com IA integrada como ambiente das práticas

- **Data:** 2026-08-07
- **Status:** Aceita
- **Decisores:** José Romualdo (docente da Trilha de Tecnologia)

## Contexto

A turma Lenovo é heterogênea, de estagiários a diretores, com pouca
familiaridade com ferramentas técnicas e ambiente institucional Microsoft
(provavelmente Copilot). A ementa da Trilha de Tecnologia exige EDA, modelagem e
prototipagem, e a orientação do módulo é que a análise seja conduzida com IA
generativa e engenharia de prompt, não escrevendo Python do zero.

Três ambientes foram considerados: Colab com IA integrada; chat externo
(ChatGPT, Claude ou Copilot) somado ao Colab; e o Copilot corporativo da Lenovo
como ferramenta principal.

## Decisão

Usar o Google Colab com a IA integrada como ambiente único das práticas. O
Copilot do ambiente deles entra como ponte comentada, não como dependência da
aula.

## Motivações

- **O atrito de copiar e colar entre janelas é onde turmas pouco técnicas
  travam.** No Colab, pedir o código e executá-lo acontecem na mesma tela.
- **A regra pedagógica do módulo exige execução.** A tese da primeira aula é que
  número que sai do modelo não vale e número que sai de código executado vale.
  Isso só é praticável se rodar código for barato.
- **O Copilot corporativo não é testável a tempo.** Não há confirmação de que a
  conta corporativa aceita upload de CSV nem de que gera e executa Python, e a
  primeira aula é no dia seguinte a esta decisão. Apostar a aula em ambiente que
  não controlamos é risco sem contrapartida.

## Riscos conhecidos

- **Exige conta Google.** Mitigação: quem não tiver trabalha em dupla, o que
  também é aceitável pedagogicamente.
- **Sai do ambiente institucional da turma.** Mitigação: cada tarde reserva uma
  faixa curta mostrando como o mesmo passo seria feito em Copilot no trabalho
  deles. A transferência é objetivo declarado do módulo.
- **Dependência de rede na sala.** Mitigação: o notebook carrega o painel de uma
  URL pública, e o plano B (CSV local por pendrive) está registrado nas notas de
  condução, para ser anunciado no começo da aula e não no meio da prática.

## Consequências

- Positivas: uma ferramenta só, sem instalação, com IA e execução na mesma tela.
- Negativas: o aprendizado não transfere literalmente para a stack deles, e a
  ponte precisa ser feita de forma explícita em cada aula.

## ADRs relacionadas

- ADR-001 (painel sintético com os números do case travados)
- ADR-003 (Gemini como ambiente das práticas e Antigravity como demonstração),
  que emenda esta a partir da Aula 02: as práticas passam a rodar em Gemini e o
  Colab fica como plano B declarado
