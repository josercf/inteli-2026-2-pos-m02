# ADR-011: o recap conjunto sintetiza o material de Negócios sem republicá-lo, e não introduz número novo

- **Data:** 09/10/2026
- **Status:** aceita
- **Decisores:** Prof. José Romualdo da Costa Filho, com a programação da aula combinada com o Prof. Rafael Donaire

## Contexto

A Aula 09 fecha o módulo em encontro conjunto das duas trilhas, com quatro
blocos: recap (material de Negócios e de Tecnologia), tira-dúvidas,
finalização dos artefatos e apresentação. O recap de Negócios depende dos
decks do Prof. Rafael Donaire, recebidos em PDF em 08/10/2026.

Duas restrições já existiam no acervo. Este repositório é público, e o deck
de Negócios é material do professor, que fica em `recebidos/` e nunca é
commitado. E nenhum número do case aparece em material didático sem estar
travado por teste.

## Decisão

O deck da Aula 09 sintetiza os conceitos da trilha de Negócios em slides
próprios, citando o professor e as fontes originais (Courtney et al., Spoor,
Kotler, caso HubSpot da HBS, BCG), sem copiar slide, imagem ou texto corrido do
material recebido; os PDFs ficam em `recebidos/negocios/`. E a aula não calcula
número novo: todo número com cara de dado do case vem de uma aula anterior e
aponta, em `tools/tests/test_deck_aula09.py`, para o teste que o trava.

## Motivações

- O recap precisa estar no deck público, porque a turma revisa por ele durante
  a finalização; o material do professor de Negócios continua sendo dele.
- As fontes originais são citáveis e públicas, e o aluno pode chegar nelas sem
  o deck de Negócios.
- Recap é onde um número reaparece com uma casa trocada sem ninguém
  recalcular. A trava aponta para o teste original em vez de recalcular, e um
  número sem trava reprova a suíte.

## Riscos conhecidos e mitigações

- **A síntese pode divergir do que o Prof. Rafael ensinou.** Mitigação: cada
  slide de Negócios cita a aula de origem na linha de fonte, para que o Prof.
  Rafael confira a síntese contra o próprio material.
- **Número ilustrativo confundido com dado do case** (por exemplo, a hipótese
  "reduzir 15%" da aula 1 de Negócios). Mitigação: esses números ficam numa
  lista separada no teste, com o motivo ao lado.
- **Data, horário dos blocos e tempo por grupo não foram definidos.**
  Mitigação: o deck sai sem eles e a pendência fica no planejamento, como na
  Aula 08.

## Consequências

- Positivas: o recap das duas trilhas fica num só lugar, público, e cada número
  dele é rastreável até o teste que o trava.
- Negativas: a síntese de Negócios é mais curta que o material original, e o
  deck não mostra as figuras do professor. Quem quiser o original recorre ao
  material distribuído por ele.

## ADRs relacionadas

- ADR-001 e ADR-005, sobre números do case travados por teste e dado que não é
  versionado.
- ADR-010, sobre o aplicativo que a apresentação demonstra.
