# ADR-008: a regressão logística da Aula 06 roda em numpy, sem scikit-learn

- **Data:** 12/09/2026
- **Status:** aceita
- **Decisores:** Prof. José Romualdo da Costa Filho

## Contexto

A Aula 06 precisa mostrar o peso de cada variável de entrada, o que exige
ajustar uma regressão logística sobre as sete colunas padronizadas. O acervo não
tinha scikit-learn nas dependências, e a AUC isolada de cada coluna já era
calculada pela estatística de Mann-Whitney com scipy, que já estava presente.

## Decisão

O ajuste roda por Newton-Raphson (IRLS) em cerca de vinte linhas de numpy, em
`dados/analise_aula06.py`. Nenhuma dependência nova entra em
`requirements-dev.txt` por causa desta aula.

## Motivações

- A decisão foi tomada na manhã da aula, com menos de uma hora de margem, e
  acrescentar dependência ao CI naquele momento traria risco sem ganho didático.
- O que a aula precisa mostrar é o coeficiente padronizado e a razão de chances,
  que o ajuste por IRLS entrega diretamente.
- A AUC de uma variável isolada é numericamente igual à estatística de
  Mann-Whitney normalizada, então a régua de comparação entre listas de features
  também dispensa biblioteca de modelagem.

## Riscos conhecidos

- **Implementação própria de método estatístico é código que ninguém revisa.**
  Mitigação: os sete coeficientes, as sete razões de chances e os sete pesos
  relativos estão travados em `dados/tests/test_aula06_numeros.py` contra valor
  transcrito de forma literal.
- **Convergência.** Colunas quase colineares (`freq_meses` e `freq_dias`) tornam
  a matriz de segunda derivada mal condicionada. Mitigação: um ridge de 1e-6, e
  o argumento de `exp` limitado à faixa que ele aguenta.
- **A tarde precisa de mais que isto.** Matriz de confusão, curva ROC, partição
  entre treino e teste e intervalo de confiança da métrica pedem biblioteca.

## Consequências

Positivas:

- O aluno vê o ajuste em vinte linhas legíveis, o que ajuda a entender de onde
  vem o coeficiente, em vez de chamar um método e receber um vetor.
- O acervo continua rodando com pandas, numpy, scipy e pytest.

Negativas:

- A UC2 Aula 2, na tarde do mesmo dia, vai precisar de scikit-learn, e a
  dependência entra ali. Esta ADR será revisitada quando isso acontecer.
- Os números desta aula são medidos sobre a mesma população usada no ajuste, sem
  partição entre treino e teste, e portanto são otimistas. Eles servem de régua
  para comparar duas listas de features, e o material declara isso.

## ADRs relacionadas

- [ADR-007](ADR-007-corte-temporal-separa-observacao-de-rotulo.md), que define a
  janela sobre a qual estas colunas são calculadas.
