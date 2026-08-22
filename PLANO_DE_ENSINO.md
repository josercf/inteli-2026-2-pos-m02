# Plano de Ensino

## Módulo 2: Inteligência de Mercado e Modelagem Preditiva para Crescimento

**Curso:** MBA em IA e Dados para Negócios (Inteli x Lenovo)
**Turma:** 2026.2A, aproximadamente 20 alunos em três grupos formados no Módulo 1
**Trilha deste acervo:** Tecnologia (bloco da tarde)
**Professor:** José Romualdo da Costa Filho
**Trilha de Negócios (bloco da manhã):** Prof. Rafael Donaire
**Case integrador:** Kovan Technologies LATAM, referência PL-02-2026

---

## 1. O formato do sábado

O módulo é presencial, aos sábados, e cada encontro tem duas metades que se
alimentam:

| Turno | Horário | Responsável | Papel |
|---|---|---|---|
| Manhã | 09h00 às 12h30 | Rafael Donaire | Inteligência de mercado, comportamento do consumidor, construção de hipóteses |
| Tarde | 14h00 às 17h30 | José Romualdo | Trabalho com dados para validar ou derrubar as hipóteses levantadas de manhã |

A integração é o diferencial do presencial e não é decorativa: o roteiro da
tarde parte do que a manhã produziu. Na Aula 01, por exemplo, a manhã fecha com
os grupos montando um backlog de hipóteses (slide 56 do deck do Rafael), e a
tarde começa pegando esse backlog.

---

## 2. Calendário

Nove encontros, de 08/08/2026 a 03/10/2026. Em 12/09 o professor da tarde
conduz também a manhã.

| # | Data | Manhã | Tarde | Marco |
|---|---|---|---|---|
| S1 | 08/08 | Negócios | **UC1.1** Da hipótese à evidência | |
| S2 | 15/08 | Negócios | **UC1.2** Preparação e limpeza | |
| S3 | 22/08 | Negócios | **UC1.3** Univariada e bivariada | |
| S4 | 29/08 | Negócios | **UC1.4** Visualização para decidir | |
| S5 | 05/09 | Negócios | Entrega 1 e veredito de alvo | **Artefato 1** |
| S6 | 12/09 | **UC2.1** Feature engineering | **UC2.2** Treino e avaliação | |
| S7 | 19/09 | Negócios | **UC2.3** Prototipagem | |
| S8 | 26/09 | Negócios | **UC2.4** Pipeline ML mais GenAI mais UI | |
| S9 | 03/10 | Negócios | Entrega 2 e banca | **Artefato 2** |

Notas de calendário:

- 07/09 é feriado e cai numa segunda-feira: não conflita com nenhum encontro.
- A ementa oficial prevê 10 semanas com a semana 6 livre e aulas remotas. O
  formato real da turma Lenovo é presencial em 9 sábados corridos. Onde os dois
  divergem, **este documento segue o calendário real**, e a divergência fica
  registrada aqui em vez de ser silenciada.

---

## 3. Unidades curriculares (ementa oficial da Trilha de Tecnologia)

### UC1: Fundamentos de Análise Exploratória de Dados

| Aula | Título da ementa | Encontro |
|---|---|---|
| 1 | O Framework de EDA: da coleta à pergunta de negócio | S1 tarde |
| 2 | Conceitos de preparação e limpeza de dados (nulos, outliers) | S2 tarde |
| 3 | Fundamentos de análise univariada e bivariada | S3 tarde |
| 4 | Conceitos de visualização de dados | S4 tarde |

### UC2: Modelagem Preditiva e Prototipagem de Aplicações de IA

| Aula | Título da ementa | Encontro |
|---|---|---|
| 1 | Feature engineering e metodologias para modelos de classificação | S6 manhã |
| 2 | Treinamento e avaliação (regressão logística, AUC-ROC) | S6 tarde |
| 3 | Introdução a frameworks de prototipagem de aplicações analíticas | S7 tarde |
| 4 | Arquitetura de pipeline integrado: modelo, API generativa e interface | S8 tarde |

---

## 4. Entregas avaliadas

| Marco | Artefato de Tecnologia | Critério |
|---|---|---|
| Semana 5 (05/09) | Análise Exploratória de Dados: código que carrega, limpa e visualiza o painel, identificando os padrões associados ao churn | Binária: entregou ou não entregou. O foco é o feedback |
| Semana 9 (03/10) | Aplicativo Web Preditivo-Generativo: executa o modelo de churn treinado em Python e consome uma API generativa para produzir o texto de retenção personalizado | Rubrica |

A rubrica da entrega final tem como base os critérios do Módulo 2 do semestre
anterior. **Pendência aberta:** esse documento ainda não foi recebido, e por
isso a rubrica não está transcrita aqui. Nenhum peso é estimado ou inferido.

Os artefatos da Trilha de Negócios, entregues nos mesmos marcos, são a Análise
de Segmentação Estratégica com Personas Data-Driven (semana 5) e o Plano de
Intervenção Preditiva com Business Case de ROI (semana 10). O trabalho da tarde
alimenta os dois: a segmentação da manhã precisa da EDA da tarde, e o ROI da
manhã precisa dos números do modelo da tarde.

---

## 5. O case: Kovan Technologies LATAM

A Kovan é uma operação LATAM de computing corporativo. O NRR do segmento
estratégico caiu de 109% para 93% em quatro trimestres, e a decomposição
mostrou que a deterioração não está onde a operação a procurava: veio de contas
que continuam na base e compram menos, não de contratos encerrados.

O Comitê de Receita já decidiu construir um modelo de propensão. O que está em
aberto, e é o que os grupos precisam fechar, é **o que exatamente o modelo deve
prever**:

- **Caminho A, Sinal de Ruptura.** Alvo binário e verificável, derivável do
  sistema. 34 eventos observados em 14 trimestres, 24 efetivos para treino,
  6 a 10 contas sinalizadas por trimestre. Dispara tarde.
- **Caminho B, Erosão Silenciosa.** Alvo contínuo e construído. 176 episódios
  observados, dos quais 31,8% se resolveram sozinhos e 51,7% seguiram
  contraindo sem romper. 120 a 190 contas sinalizadas por trimestre contra um
  teto operacional de 138 planos de intervenção.

Há uma janela única de publicação no CRM, em setembro de 2026, e uma equipe de
seis pessoas por 26 semanas: dá para construir um modelo, não dois.

### O dataset

**A partir da Aula 03, a base é `dados/datasets_case_modulo2.xlsx`**, o dataset
oficial da Lenovo recebido em 21/08/2026: cinco abas, 8.282 contas, 24 meses de
2024-04 a 2026-03, e 207.826 linhas de pedido. Ele **não é versionado**, porque
é dado real de carteira LATAM e este repositório é público. A justificativa da
troca está em `docs/adrs/ADR-005`, e a distribuição à turma acontece pelo
repositório de clone `github.com/josercf/inteli-pos-2026-2a-eda`, que traz a
estrutura e as skills sem o dado.

A base oficial **tem** uma coluna `churn_label`, o que muda a pergunta do
módulo. Ela é constante por conta e determinada pelo último mês de compra, com
corte em 08/02/2025. O Caminho A deixa de ser construção de rótulo e passa a ser
auditoria de um rótulo existente; o Caminho B segue em aberto.

As Aulas 01 e 02 rodaram sobre `dados/kovan_painel_contas.csv`, gerado por
`dados/gerar_painel_kovan.py`: 1.187 contas por 14 trimestres, 16.618 registros,
20 colunas, conforme o Exhibit 3 do Caderno de Exhibits. O painel sintético
permanece no repositório como registro dessas duas aulas, sem ser reapresentado
(`docs/adrs/ADR-001`).

O painel é sintético, com os números do case travados por teste, e traz de
propósito as quatro advertências de qualidade do exhibit. A justificativa
completa dessa escolha, incluindo a divergência com a orientação inicial de
usar bases públicas, está em `docs/adrs/ADR-001`.

O painel **não tem coluna de risco, de propensão nem de rótulo**. Isso é
conteúdo, não lacuna: a decisão de alvo é o case.

---

## 6. Matriz de rastreabilidade

| Encontro | Competência técnica da ementa | Momento do case | Entregável do dia |
|---|---|---|---|
| S1 | EDA: da coleta à pergunta de negócio | O painel não tem rótulo | Caderno de hipóteses com veredito |
| S2 | Preparação e limpeza (nulos, outliers) | As quatro advertências do Exhibit 3 | Base tratada e o custo de cada decisão |
| S3 | Análise univariada e bivariada | O critério do `churn_label` não está documentado | Quatro seções do Artefato 1 |
| S4 | Visualização de dados | Talvera e Andirá caíram igual e terminaram diferente | Figuras do Artefato 1 |
| S5 | Consolidação | O Comitê de 3 de março | Recomendação de alvo |
| S6m | Feature engineering | A suspeita não testada de Otávio Rangel | Matriz de features com corte temporal |
| S6t | Métricas de avaliação, matriz de confusão, AUC-ROC | O argumento de Priscila Nakamura | Modelo e matriz de confusão em reais |
| S7 | Prototipagem de aplicações analíticas | O Radar de Contas morreu por desuso | App com lista priorizada |
| S8 | Pipeline integrado e engenharia de prompt | O grupo de controle de Cláudia Meireles | Artefato 2 técnico |
| S9 | Comunicação executiva | Banca no papel do Comitê de Receita | Defesa por rubrica |

---

## 7. Ferramentas

- **Antigravity**, para todas as práticas a partir da Aula 03, sobre a pasta
  clonada do repositório da turma. A turma não escreve Python do zero: escreve
  prompts, lê o código gerado e roda. O entregável é a pasta que sobra. A
  decisão está em `docs/adrs/ADR-006`, que emenda a ADR-003 e a ADR-002.
- **Google Colab com IA integrada** permanece como ambiente de execução de
  código descrito na `docs/adrs/ADR-002`, usado nas Aulas 01 e 02.
- **Streamlit** para o protótipo da UC2, com o Colab como ambiente de treino.
- O ambiente institucional da turma é Microsoft, e cada tarde reserva uma faixa
  curta para mostrar como o mesmo passo se faria em Copilot no trabalho deles.
  A aula não depende desse ambiente.

**Pendência aberta:** chave de API generativa para a aula de 26/09.

---

## 8. Pendências de planejamento

Registradas em vez de preenchidas por suposição:

1. Decks das aulas 2 a 9 da Trilha de Negócios. Só a Aula 01 foi recebida.
2. Rubrica da entrega final.
3. Autoestudos por semana. A ementa não os lista.
4. A décima aula com professor convidado que a ementa cita, e que o calendário
   de nove sábados não acomoda.
5. Chave de API para uso em sala.
