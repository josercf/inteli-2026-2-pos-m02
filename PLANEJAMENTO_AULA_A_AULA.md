# Planejamento Aula a Aula

Trilha de Tecnologia, Módulo 2, MBA em IA e Dados para Negócios (Inteli x Lenovo).
Fonte da verdade para data, título, escopo e entregável de cada encontro.
Nenhum deck, notebook ou material inventa o que deveria descer daqui.

**Formato do bloco da tarde:** 14h00 às 17h30, com intervalo de 20 minutos.
Sete blocos, nenhum trecho expositivo passando de 15 minutos sem interação
direta da turma.

---

## S1, 08/08/2026: Da hipótese à evidência

**Ementa:** UC1, Aula 1. O framework de EDA: da coleta à pergunta de negócio.

**O que a manhã deixa pronto:** o backlog de hipóteses que os grupos montaram
com o Prof. Rafael Donaire (slide 56), e uma posição preliminar sobre Caminho A
ou Caminho B. A tarde não reapresenta o case: pega o backlog e o submete ao dado.

**Objetivos de aprendizagem:**
1. Distinguir a IA que descreve o dado da IA que escreve o código que mede o dado.
2. Escrever um prompt de análise com a restrição de não preencher lacuna.
3. Operacionalizar uma hipótese até o critério de refutação.
4. Construir o rótulo do Caminho A e medir sua prevalência.

**Regra da casa, anunciada às 14h15 e cobrada até o fim:** todo número que
entrar no caderno vem de código que a IA escreveu e que nós rodamos.

### Agenda em minutos

| Horário | Bloco | Conteúdo |
|---|---|---|
| `14h00 - 14h15` | Resgate e contrato | Cada grupo lê uma hipótese do próprio backlog. As três vão para o quadro. Pergunta disparada: o painel tem 16.618 linhas e nenhuma coluna de risco, como isso vira evidência até as 17h30? |
| `14h15 - 14h30` | Bloco 1 | EDA quando a IA executa. O ciclo pergunta, recorte, medida, refutação. A IA colapsou o custo de executar, não o de decidir o que medir. Enquete: quem já pediu análise de planilha para uma IA e conferiu o número? |
| `14h30 - 14h50` | Prática 1 | Prompt nível 0 sobre o painel, depois o prompt armadilha da margem média, que não existe no dado. Colheita e regra de ouro |
| `14h50 - 15h05` | Bloco 2 | A escada de prompt sobre a mesma pergunta: a queda de receita é uniforme? Níveis 0 a 3. A restrição que vale para dado e não vale para texto |
| `15h05 - 15h25` | Prática 2 | Reescrever no nível 2, pedir o código, rodar no Colab. Subir para o nível 3. Debrief: prompts diferentes deram recortes diferentes sobre a mesma base |
| `15h25 - 15h45` | Intervalo | |
| `15h45 - 16h00` | Bloco 3 | Anatomia do teste falseável: variável, operação, janela, critério de refutação. O que este painel não permite testar |
| `16h00 - 16h30` | Prática 3 | O caderno de hipóteses. Três hipóteses do backlog próprio, com nível 3 obrigatório em pelo menos uma |
| `16h30 - 16h45` | Bloco 4 | O rótulo que não existe. Peça à IA que crie a coluna de churn e leia o critério que ela escolheu sem avisar |
| `16h45 - 17h15` | Prática 4 | Construir o rótulo do Caminho A e contar as rupturas do segmento estratégico. Comparar com a mesa ao lado |
| `17h15 - 17h30` | Amarração | O que fica pronto, o que a Aula 02 pega, o que alimenta o Artefato 1 |

### Verificações do encontro

1. Você pediu a margem média por conta e recebeu um número. O painel não tem
   coluna de margem. O que aconteceu?
2. Qual destas hipóteses está pronta para virar código?
3. Duas mesas contaram rupturas com o mesmo critério e chegaram a números
   diferentes. Qual a explicação mais provável?

### Entregável

Caderno de hipóteses do grupo, com três registros completos e veredito
(Confirmada, Contraditada ou Insuficiente), exportado do notebook.

### Artefatos

- Deck: `aulas/aula01.html`
- Notebook: `notebooks/aula01_hipoteses.ipynb`
- Material do aluno: `materiais/caderno-de-hipoteses.md`
- Condução: `docs/notas-do-professor/aula01.md` (não distribuído)

---

## S2, 15/08/2026: O dado sujo é o case

**Ementa:** UC1, Aula 2. Conceitos de preparação e limpeza de dados.

**Espiral:** a Aula 01 deixou pronto o rótulo do Caminho A e mesas com contagens
de ruptura diferentes entre si. A causa dessa divergência é o conteúdo de hoje.

**Conteúdo:** as quatro advertências de qualidade do Exhibit 3 como matéria, não
como nota de rodapé. Cerca de 1% dos trimestres de conta ativa sem receita
registrada (excluir e imputar produzem séries diferentes); devoluções em coluna
independente e valor negativo; a mudança de taxonomia de 2023, que deixa a
contagem de linhas estruturalmente menor antes de 2023Q1 e fabrica um sinal
falso de erosão em quem não tratar; e o engajamento comercial incompleto, pior
justamente nas contas menores.

**Atividade PBL:** confronto. Metade dos grupos exclui as linhas de receita
ausente, metade imputa. Comparam as duas séries e medem o custo da decisão em
número de rupturas.

**Entregável:** base tratada e o custo numérico de cada decisão de tratamento.

---

## S3, 22/08/2026: O limiar é escolha, não fato

**Ementa:** UC1, Aula 3. Fundamentos de análise univariada e bivariada.

**Espiral:** a Aula 02 deixou pronta a base tratada e a contagem de rupturas
estável entre as mesas.

**Conteúdo:** distribuição de receita e cauda da carteira; prevalência de
ruptura; construção do rótulo de erosão em três cortes de limiar e o efeito de
cada corte no tamanho da fila e na captura de rupturas. Bivariada como a
ferramenta que mostra que o limiar constrói modelos diferentes.

**Atividade PBL:** cada grupo constrói o rótulo nos cortes de 10%, 15% e 25%,
mede quantas rupturas cada corte captura, e depois cruza a ordem em que receita,
mix e cadência se deterioram contra o desfecho do episódio.

**Entregável:** tabela de contingência que sustenta ou derruba as hipóteses do
dia 1. É aqui que o achado central do módulo pode aparecer.

---

## S4, 29/08/2026: Visualização para decidir

**Ementa:** UC1, Aula 4. Conceitos de visualização de dados.

**Conteúdo:** a figura que muda uma decisão contra a figura que ilustra um
texto. Distribuições por segmento, séries lado a lado e o gráfico de valor em
risco por probabilidade com a linha de capacidade operacional desenhada.

**Atividade PBL:** produzir a figura que faz o diretor comercial ver a diferença
entre duas contas que caíram igual e terminaram diferente.

**Entregável:** as figuras do Artefato 1.

---

## S5, 05/09/2026: Entrega 1 e veredito de alvo

**Formato:** primeira metade, entrega e feedback cruzado entre grupos. Segunda
metade, fechamento da recomendação de alvo com número.

**Entregável avaliado:** Artefato 1 de Tecnologia, a Análise Exploratória de
Dados. Entrega binária, com foco em feedback.

---

## S6, 12/09/2026: manhã e tarde com o professor da trilha de Tecnologia

**Manhã, UC2 Aula 1:** feature engineering e metodologias para modelos de
classificação. Recência, frequência e valor; janelas históricas; a variável de
sequência dos sinais; vazamento temporal; o efeito de realimentação do score
sobre a atividade registrada.

**Tarde, UC2 Aula 2:** treinamento e avaliação. Regressão logística, matriz de
confusão, AUC-ROC. O limiar de decisão calibrado pela capacidade operacional, e
não em 0,5. Treinar o Caminho A com os eventos efetivos disponíveis e observar o
intervalo de confiança da métrica.

---

## S7, 19/09/2026: Prototipagem

**Ementa:** UC2, Aula 3. Frameworks de prototipagem de aplicações analíticas.

Do notebook ao aplicativo em Streamlit. A tela que o Account Manager abriria, com
a lista priorizada por valor em risco e a explicação que permite justificar a
priorização internamente.

---

## S8, 26/09/2026: Pipeline integrado

**Ementa:** UC2, Aula 4. Modelo, API generativa e interface no mesmo fluxo.

O aplicativo consome a API generativa e produz o roteiro de intervenção por
conta. Engenharia de prompt com CREATE. Guardrail: o texto gerado não cita
número que não esteja no score. Marcação das contas mantidas fora da intervenção
como grupo de controle.

**Pendência:** chave de API para uso em sala.

---

## S9, 03/10/2026: Entrega 2 e banca

Cada grupo defende o projeto no papel do Comitê de Receita da Kovan LATAM.

**Entregável avaliado:** Artefato 2 de Tecnologia, o Aplicativo Web
Preditivo-Generativo. Avaliação por rubrica.

**Pendência:** rubrica não recebida.
