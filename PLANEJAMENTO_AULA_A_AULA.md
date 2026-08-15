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
| `14h15 - 14h30` | Bloco 1 | EDA quando a IA executa. **CRISP-DM** como mapa do módulo e o **ciclo de EDA assistida**: quatro dos seis passos continuam com você. Enquete: quem já pediu análise de planilha para uma IA e conferiu o número? |
| `14h30 - 14h50` | Prática 1 | Prompt nível 0 sobre o painel, depois o prompt armadilha da margem média, que não existe no dado. Colheita e regra de ouro |
| `14h50 - 15h05` | Bloco 2 | A escada de prompt sobre a mesma pergunta: a queda de receita é uniforme? Níveis 0 a 3, com o prompt real lado a lado. **Estrutura na entrada, estrutura na saída**: os cinco elementos e o modo de falha de cada ausência |
| `15h05 - 15h25` | Prática 2 | Reescrever no nível 2, pedir o código, rodar no Colab. Subir para o nível 3. Debrief: prompts diferentes deram recortes diferentes sobre a mesma base |
| `15h25 - 15h45` | Intervalo | |
| `15h45 - 16h00` | Bloco 3 | Anatomia do teste falseável: variável, operação, janela, critério de refutação. **Árvore de hipóteses MECE**, da pergunta do Comitê até a coluna que testa cada folha. O que este painel não permite testar |
| `16h00 - 16h30` | Prática 3 | O caderno de hipóteses. Três hipóteses do backlog próprio, com nível 3 obrigatório em pelo menos uma |
| `16h30 - 16h45` | Bloco 4 | O rótulo que não existe. **Cinco critérios para escolher o alvo**, aplicados a A e B. Talvera e Andirá: a magnitude da queda não antecipa o desfecho. Peça à IA que crie a coluna de churn e leia o critério que ela escolheu sem avisar |
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

### Frameworks apresentados

CRISP-DM (Wirth e Hipp, 2000); o ciclo de EDA assistida por IA (construção do
módulo); estrutura na entrada e na saída, complementando o CREATE que a manhã
apresenta; árvore de hipóteses MECE (Conn e Sarrazin, McKinsey); e os cinco
critérios de escolha de alvo (construção do módulo, a partir das restrições do
case). O que é citável e o que é nosso está separado no slide de referências.

### Artefatos

- Deck: `aulas/aula01.html`, 32 slides, com três GIFs e dois diagramas.
  Gerado por `tools/montar_deck_aula01.py`, não editado à mão
- Figuras: `tools/gerar_figuras_aula01.py`, desenhadas em 1168px e renderizadas 1:1
- Notebook: `notebooks/aula01_hipoteses.ipynb`
- Material de apoio: `materiais/aula01-material-de-apoio.html`, sete seções com
  as contas que a projeção não comporta (derivação do intervalo do AUC,
  mecanismos de ausência aplicados coluna a coluna, prompts completos)
- Material do aluno: `materiais/caderno-de-hipoteses.md`
- Condução: `docs/notas-do-professor/aula01.md` (não distribuído)

---

## S2, 15/08/2026: O dado sujo é o case

**Ementa:** UC1, Aula 2. Conceitos de preparação e limpeza de dados.

**Espiral:** a Aula 01 deixou pronto o rótulo do Caminho A e mesas com contagens
de ruptura diferentes entre si. A causa dessa divergência é o conteúdo de hoje.

**Conteúdo:** as quatro advertências de qualidade do Exhibit 3 tratadas como
matéria da aula. As 160 linhas de trimestre de conta ativa sem receita
registrada; as 8.280 linhas de engajamento comercial ausente, concentradas nas
contas menores; a mudança de taxonomia de 2023Q1, que faz a média de linhas de
produto saltar de 1,85 para 3,67 e esconde a queda de 30,4% que vem depois; e
`devolucoes_brl` em coluna independente, com sinal negativo.

**Objetivos de aprendizagem:**
1. Perfilar uma base desconhecida com IA, sem aceitar lacuna preenchida.
2. Distinguir ausência aleatória de ausência enviesada, e nomear o mecanismo.
3. Medir o custo de uma decisão de tratamento em vez de argumentar sobre ela.
4. Registrar o tratamento num artefato reexecutável e portátil entre agentes.

**Contrato do dia, anunciado às 14h00 e cobrado até o fim:** toda decisão de
tratamento entra escrita, com o custo medido.

**Ambiente:** as quatro práticas rodam em Gemini, o Antigravity aparece em
demonstração projetada da máquina do professor, e o Colab da Aula 01 fica como
plano B declarado no começo da aula (ADR-003).

### Agenda em minutos

| Horário | Bloco | Conteúdo |
|---|---|---|
| `14h00 - 14h15` | Resgate e contrato | As contagens de ruptura da Aula 01 vão para o quadro. O número certo é 34. Pergunta disparada: o que cada mesa fez com as linhas em que a receita não está registrada? Contrato do dia: toda decisão de tratamento entra escrita, com o custo medido |
| `14h15 - 14h30` | Bloco 1 | Onde a limpeza mora dentro da EDA. As **seis dimensões de qualidade de dado** (completude, validade, consistência, unicidade, acurácia, temporalidade) como checklist nomeável. Enquete: quem já recebeu base de outra área e usou sem perfilar? |
| `14h30 - 14h50` | Prática 1, Gemini | Perfilamento cego. Subir o painel e pedir o perfil de qualidade coluna a coluna, com a restrição de não preencher lacuna. Colheita: quantas das quatro advertências a IA achou sozinha, e qual ela perdeu |
| `14h50 - 15h05` | Bloco 2 | As quatro advertências do Exhibit 3 com os números na tela |
| `15h05 - 15h25` | Prática 2, Gemini | Mecanismo de ausência. A ausência do engajamento é aleatória? Medem por segmento e encontram 29,4% contra 53,2%. **MCAR, MAR e MNAR** entram como vocabulário na sequência da medição, nomeando o que a turma acabou de observar |
| `15h25 - 15h45` | Intervalo | |
| `15h45 - 16h00` | Bloco 3 | Excluir, imputar ou sinalizar. Cada uma das três decisões assume uma coisa diferente sobre o mundo. Como se mede o custo de uma decisão de tratamento |
| `16h00 - 16h30` | Prática 3, confronto | Metade dos grupos trata `visitas_registradas` ausente como zero, metade exclui. Cada metade calcula visitas médias por segmento e defende a leitura. Os dois quadros vão lado a lado e a ordem dos segmentos inverte |
| `16h30 - 16h45` | Bloco 4 | A **skill de agente** como formato: arquivo Markdown com o fluxo sistemático. Anatomia e por que ela resolve o problema de abertura. Demonstração projetada no Antigravity, com o mesmo arquivo lido por um agente que trabalha sobre pasta |
| `16h45 - 17h15` | Prática 4 | Preenchem a `skill-limpeza-kovan.md` a partir do esqueleto, colam no Gemini e rodam contra a base crua. Critério de aceite: o número tem que bater com o da Prática 3 |
| `17h15 - 17h30` | Amarração | O que fica pronto, o que a Aula 03 pega, o que alimenta o Artefato 1 |

### Verificações do encontro

1. Duas mesas mediram visitas por segmento na mesma base e chegaram a ordens
   opostas. Qual explicação é a mais provável?
2. A média de linhas de produto passou de 1,85 para 3,67 entre 2022Q4 e 2023Q1.
   O que aconteceu com a carteira?
3. Qual destas decisões de tratamento pode ser reproduzida por outra pessoa na
   semana que vem?

### Entregável

Base tratada, o custo numérico de cada decisão de tratamento, e a
`skill-limpeza-kovan.md` preenchida, que produz os dois quando executada.

"Base tratada" exige uma decisão declarada para cada uma das quatro
advertências: o que foi feito com as 160 linhas de receita ausente, com as 8.280
de engajamento ausente, com a quebra de taxonomia de 2023Q1 e com o sinal de
`devolucoes_brl`. A Prática 3 aprofunda uma dessas quatro e o entregável
responde pelas quatro. Omissão conta como decisão de manter o dado como veio, e
o esqueleto da skill tem uma linha obrigatória para cada advertência.

### Frameworks apresentados

Seis dimensões de qualidade de dado (organizadas neste módulo a partir da
literatura de data quality, sem seguir padrão publicado); a taxonomia de
mecanismos de ausência MCAR, MAR e MNAR (Rubin, Biometrika, 1976; Little e
Rubin, Wiley, 2019); as três decisões de tratamento (excluir, imputar,
sinalizar) com o custo medido em cada caso; e a skill de agente em Markdown como
formato de registro do fluxo. O que é citável e o que é nosso está separado no
slide de referências.

### Artefatos

- Deck: `aulas/aula02.html`, com três figuras. Gerado por
  `tools/montar_deck_aula02.py`, não editado à mão
- Figuras: `tools/gerar_figuras_aula02.py`, desenhadas em 1168px e renderizadas
  1:1 (inversão dos segmentos, quebra de taxonomia, mapa de ausência)
- Notebook: `notebooks/aula02_limpeza.ipynb`, plano B do upload no Gemini e
  lugar de exportar o entregável
- Material de apoio: `materiais/aula02-material-de-apoio.html`, com MCAR, MAR e
  MNAR aplicados coluna a coluna, o efeito da taxonomia trimestre a trimestre,
  os prompts completos e o código de cada tratamento
- Material do aluno: `materiais/skill-limpeza-kovan.md`, esqueleto preenchido na
  Prática 4
- Condução: `docs/notas-do-professor/aula02.md` (não distribuído)

### Divergência registrada

O planejamento original prescrevia, para a S2, que metade dos grupos excluísse
as linhas de receita ausente e metade as imputasse, comparando as duas séries e
medindo o custo da decisão em número de rupturas.

Essa atividade foi medida contra o CSV entregue e ficou fraca. São 14 linhas de
receita ausente no segmento estratégico. O custo em contagem de rupturas fica em
168 contra 169, e em episódios de erosão o intervalo inteiro vai de 74 a 76 no
corte de 25%. Duas metades da sala apresentariam números praticamente iguais.

A forma do PBL foi mantida: metade exclui, metade imputa, ambas medem o custo e
entregam a base tratada. A coluna do confronto passou de `receita_brl` para
`visitas_registradas`, onde a ordem dos segmentos inverte entre os dois
tratamentos. A receita ausente permanece na aula como Prática 2, o mecanismo de
ausência, que é onde a espiral da Aula 01 aterrissa.

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
