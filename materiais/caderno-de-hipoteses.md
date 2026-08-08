# Caderno de Hipóteses

**Grupo:** _______________  **Data:** 08/08/2026  **Aula 01, Módulo 2**

Este é o entregável de hoje. Ele nasce do backlog que vocês escreveram de manhã
e é a matéria-prima do Artefato 1 da semana 5.

---

## A regra da casa

Todo número que entrar aqui vem de código que a IA escreveu e que vocês rodaram.
Número que a IA cita de cabeça não entra.

Não é desconfiança do modelo. É que ele lê uma amostra do arquivo e completa o
resto por plausibilidade, e plausível não é o mesmo que verdadeiro. Quando a IA
escreve o código, ela também pode errar, mas o erro fica legível: dá para ler a
linha, discordar dela e corrigir.

---

## O que é um registro completo

Uma hipótese só está operacionalizada quando as seis linhas estão preenchidas.
A que costuma faltar é a quarta.

| Campo | O que entra |
|---|---|
| **Enunciado** | A afirmação, clara e mensurável |
| **Variáveis** | Quais colunas do painel carregam o sinal |
| **Operação** | O que se calcula sobre elas, e sobre quais grupos |
| **Janela** | Quais trimestres entram, e por que os outros ficam de fora |
| **Critério de refutação** | Qual resultado derruba a hipótese. Escrito **antes** de rodar |
| **Prompt** | O prompt final que gerou o código |

E, depois de rodar: o número obtido e o veredito.

### Os três vereditos

- **Confirmada.** O número atendeu ao critério e a hipótese se sustenta.
- **Contraditada.** O número atendeu ao critério de refutação. A hipótese caiu.
- **Insuficiente.** O painel não tem a coluna, a janela ou o número de casos
  para decidir.

**Insuficiente não é fracasso.** É o resultado honesto quando o dado não
responde, e vai aparecer no caderno de vocês. Dizer que o dado não responde é
um resultado. Inventar que responde é o que a Kovan já fez uma vez, com o Radar
de Contas: 340 contas sinalizadas, 31 acertos, e o painel abandonado por perda
de confiança em onze meses.

---

## Registro 1

**Enunciado:**

**Variáveis:**

**Operação:**

**Janela:**

**Critério de refutação:**

**Prompt usado:**

```
```

**Número obtido:**

**Veredito:** ( ) Confirmada ( ) Contraditada ( ) Insuficiente

**O que isso muda na recomendação de alvo (Caminho A ou B):**

---

## Registro 2

**Enunciado:**

**Variáveis:**

**Operação:**

**Janela:**

**Critério de refutação:**

**Prompt usado:**

```
```

**Número obtido:**

**Veredito:** ( ) Confirmada ( ) Contraditada ( ) Insuficiente

**O que isso muda na recomendação de alvo (Caminho A ou B):**

---

## Registro 3

Em pelo menos um dos três registros, use a postura adversarial: antes de fechar
o veredito, peça à IA que tente derrubar o seu próprio achado. Anote abaixo o
que ela levantou e o que vocês fizeram com isso.

**Enunciado:**

**Variáveis:**

**Operação:**

**Janela:**

**Critério de refutação:**

**Prompt usado:**

```
```

**Número obtido:**

**Veredito:** ( ) Confirmada ( ) Contraditada ( ) Insuficiente

**O que a IA levantou contra o achado, e o que vocês fizeram com isso:**

---

## Fechamento

**Quantas rupturas o segmento estratégico teve nos 14 trimestres?**

**O número bateu com o do grupo ao lado? Se não, qual decisão foi diferente?**

**Depois de hoje, o grupo está mais perto do Caminho A ou do Caminho B? Qual
número sustenta isso?**

---

## Erros que este caderno existe para evitar

| Erro | Como aparece | O que fazer |
|---|---|---|
| Hipótese que não pode perder | "Existe algum padrão que explica o churn" | Reescrever com uma variável e um corte que decide |
| Número sem origem | Um valor no caderno que ninguém consegue rastrear até uma célula | Rodar de novo e colar o código |
| Confirmação em vez de teste | Todos os vereditos são Confirmada | Testar algo que vocês acreditam e podem perder |
| Correlação lida como causa | "Menos visitas causa churn" | Checar `troca_de_am_no_trimestre`: a atividade cai quando o território troca de responsável, sem a conta ter mudado |
