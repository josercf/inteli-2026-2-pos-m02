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

## S3, 22/08/2026: O corte que define o rótulo

**Ementa:** UC1, Aula 3. Fundamentos de análise univariada e bivariada.

**Horário:** 13h00 às 16h00, combinado com a turma, com folga até 16h30. O
intervalo de 20 minutos é preservado.

**Espiral:** a Aula 02 terminou na discussão dos dados em Gemini e **não chegou
a construir a skill de limpeza com a turma**, que era a Prática 4 dela. O dataset
oficial da Lenovo chegou em 21/08 e substitui o painel sintético (ADR-005). A
Aula 03 fecha as duas pendências: perfila a base nova e usa a skill de limpeza
já pronta no repositório, com o tempo de aula gasto em explicar e demonstrar em
vez de preencher esqueleto.

**Conteúdo:** distribuição de receita e a cauda da carteira; prevalência de
churn por segmento e por setor; tabela de contingência como forma bivariada para
alvo binário; a engenharia reversa do critério que define o `churn_label`; e o
teste de vazamento aplicado a variável que separa bem demais.

**O achado do dia:** o `churn_label` é constante por conta e inteiramente
determinado pelo último mês de compra. Contas que pararam até 2025-01 estão
todas marcadas como perdidas, contas que compraram de 2025-03 em diante não
estão, e fevereiro de 2025 é o único mês com contas dos dois lados. No grão do
pedido a separação é perfeita: até 08/02/2025 marca, a partir de 10/02/2025 não
marca. O rótulo é uma regra de recência de treze meses que a fonte não declarou.

**Objetivos de aprendizagem:**
1. Descrever uma variável pelo que sua distribuição responde, separando
   tendência central, dispersão e forma.
2. Ler uma tabela de contingência e dizer o que ela sustenta e o que não.
3. Reconstruir, a partir do dado, o critério que define um rótulo entregue
   pronto.
4. Medir o efeito de um limiar alternativo sobre o tamanho da fila de
   intervenção.

**Contrato do dia, anunciado às 13h00 e cobrado até o fim:** toda seção do
artefato entra com o número e a figura que a sustentam, produzidos por código
que roda na pasta do grupo.

**Ambiente:** Antigravity a tarde inteira, sobre a pasta clonada de
`github.com/josercf/inteli-pos-2026-2a-eda` (ADR-006). O dataset não é
versionado e chega por uma planilha no Drive, com o caminho no slide da Prática
1 e no README do repositório. Sem plano B de ambiente declarado: a mitigação é o
`analise_referencia.py` dentro da pasta.

### Agenda em minutos

| Horário | Bloco | Conteúdo |
|---|---|---|
| `13h00 - 13h15` | Resgate e contrato | A base oficial: cinco abas, 8.282 contas, 24 meses, e um `churn_label` que a anterior não tinha. Clone do repositório, dataset na pasta, Antigravity aberto. Contrato do dia |
| `13h15 - 13h35` | Bloco 1 e Prática 1 | Onde a troca de base nos coloca no CRISP-DM. O checklist de cinco perguntas antes de perguntar. As quatro dimensões de qualidade violadas na base. Prática: clonar, colocar o dataset e perfilar com `skills/perfilamento.md` |
| `13h35 - 13h55` | Bloco 2 e Prática 2 | Univariada construída antes do número: as três perguntas em lista, e uma figura por pergunta (centro, dispersão, forma). Depois o pedido a executar e a fórmula da assimetria. Só então a distribuição da Kovan |
| `13h55 - 14h20` | Bloco 3 e Prática 3 | O limite da univariada. Hipóteses formuladas antes da tabela. Bivariada: prevalência por segmento contra participação na receita. A contingência do último mês por rótulo, e a engenharia reversa do corte no grão do pedido |
| `14h20 - 14h40` | Intervalo | |
| `14h40 - 15h45` | Oficina do Artefato 1 | Dez minutos de demonstração da skill de limpeza, depois quatro estações de 55 minutos. A estação 2 fecha com a troca de pastas entre mesas |
| `15h45 - 16h00` | Amarração | O que fica pronto, o que a Aula 04 pega, o que a manhã do Prof. Donaire recebe |

### Verificações do encontro

1. A receita média por conta é USD 437.588 e a mediana é USD 18.552. Qual das
   duas vai para o Comitê, e por quê?
2. Nenhuma das 4.494 contas com menos de 17 meses de casa aparece como perdida.
   Qual a explicação mais provável?
3. Duas mesas mediram prevalência de churn no mesmo segmento e chegaram a
   números diferentes. O que checar primeiro?

### Entregável

Quatro das sete seções do Artefato 1 de Tecnologia, entregues como pasta
reexecutável: carga, qualidade, univariada e bivariada. As três restantes
(rótulo, visuais e limitações) vão para o autoestudo da semana, e o checklist
marca essa divisão de forma explícita.

O critério de aceite é a reexecução: outra pessoa clona a pasta do grupo, coloca
o dataset em `dados/` e obtém os mesmos números do relatório.

### Frameworks apresentados

CRISP-DM (Chapman et al., 1999) como recap, situando a univariada e a bivariada
dentro da fase de entendimento dos dados e mostrando que base nova devolve o
trabalho à fase 2; estatística descritiva univariada com tendência central,
dispersão e forma (assimetria e curtose); tabela de contingência e prevalência
condicional como forma bivariada para alvo binário; vazamento de informação
(Kaufman et al., ACM TKDD, 2012) como teste obrigatório de variável que separa
bem demais; e o limite da correlação como evidência de causa. O checklist de
cinco perguntas de perfilamento, o checklist de sete seções do Artefato 1 e as
três skills de agente foram organizados para este módulo, sem seguir padrão
publicado.

### Artefatos

- Repositório de clone: `github.com/josercf/inteli-pos-2026-2a-eda`, com
  `AGENTS.md`, `skills/`, o checklist e o `analise_referencia.py`
- Deck: `aulas/aula03.html`, com três figuras. Gerado por
  `tools/montar_deck_aula03.py`, não editado à mão
- Figuras: `tools/gerar_figuras_aula03.py`, desenhadas em 1168px e renderizadas
  1:1 (distribuição de receita, contingência do rótulo, prevalência por segmento)
- Números: `dados/analise_aula03.py`, travado por
  `dados/tests/test_dataset_oficial.py`
- Figuras didáticas: três distribuições sintéticas com semente fixa
  (tendência central, dispersão, forma), para o conceito chegar antes do número
- Material de apoio: `materiais/aula03-material-de-apoio.html`
- Material do aluno: `materiais/checklist-artefato-1-tecnologia.md`
- Condução: `docs/notas-do-professor/aula03.md` (não distribuído)

### Pendências abertas ao fim da S3

Registradas em 22/08/2026, depois da aula, para não virarem suposição na S4.

1. **Como a tarde correu de fato não está registrado.** Falta saber quantos
   grupos chegaram ao corte de 08/02/2025 e quantos pararam no resíduo de 382
   contas. A resposta muda o que a Aula 04 pode assumir como sabido, e é o
   insumo da espiral de abertura dela.
2. **As notas de condução e o material de apoio descrevem a estrutura anterior.**
   `docs/notas-do-professor/aula03.md` fala em estação 2 de vinte minutos e
   checkpoint às 15h30, quando a oficina virou 55 minutos com a troca de pastas.
   `materiais/aula03-material-de-apoio.html` descreve as práticas como slide
   único e não menciona as figuras de conceito da univariada.
3. **O compartilhamento da planilha no Drive não foi verificado.** O link está
   num slide publicado no GitHub Pages e no README de um repositório público. Se
   estiver como "qualquer pessoa com o link", a base real de carteira LATAM ficou
   acessível a partir de página aberta, o que contraria a ADR-005. Restringir ao
   domínio do Inteli não afeta quem já clonou.
4. **Dois slides abaixo da folga de 40px:** o checklist com 15px e o das cinco
   abas com 4px. Passam no limite real, e são os primeiros a estourar se algum
   texto crescer (ver a armadilha de folga no `CLAUDE.md`).

### Divergência registrada

O planejamento original prescrevia, para a S3, construir o rótulo de erosão em
cortes de 10%, 15% e 25% de queda de receita, medir quantas rupturas cada corte
captura, e cruzar a ordem em que receita, mix e cadência se deterioram contra o
desfecho do episódio. O entregável previsto era a tabela de contingência que
sustenta ou derruba as hipóteses do dia 1.

Duas mudanças o inviabilizaram. O painel sintético, onde os episódios de erosão
foram construídos, foi substituído pela base oficial (ADR-005), que não tem
coluna de mix comparável nem cadência trimestral alinhada ao painel de receita.
E a base oficial entrega um `churn_label` pronto, o que muda a pergunta de "qual
rótulo construir" para "que critério esse rótulo usa".

O que foi mantido: a tabela de contingência como entregável, o exercício de
limiar (agora sobre cortes de inatividade de 6, 9, 12 e 13 meses, com fila de
5.128, 3.719, 2.716 e 1.975 contas) e a amarração com as hipóteses do dia 1.

O que foi acrescentado: 65 minutos de oficina de construção do Artefato 1,
combinados com o Prof. Rafael Donaire para as Aulas 03 e 04, e o título mudou de
"O limiar é escolha, não fato", que é paralelismo negativo reprovado por
`tools/check_retorica.py`.

---

## S4, 29/08/2026: A figura que decide

**Ementa:** UC1, Aula 4. Conceitos de visualização de dados.

**Horário:** 13h00 às 16h00, folga até 16h30, intervalo 14h20 às 14h40.

**Espiral:** a Aula 03 deixou pronto o critério do rótulo; a maioria dos grupos
chegou ao corte de 08/02/2025. A Aula 04 assume o critério como sabido e parte
dele para a população que ele alcança.

**Conteúdo:** censura e população elegível; perfil de compra por segmento; IC
de Wilson e qui-quadrado; estratificação com os três desfechos; frequência
como vazamento; forma da figura pela pergunta, título como conclusão, teste
embaixo.

**O achado do dia:** 4.534 das 8.282 contas fizeram a primeira compra depois de
2025-02 e não têm como estar marcadas; entre as 3.748 elegíveis a prevalência é
42,5%. A hipótese do mix sobrevive ao controle por segmento e desaparece sob
controle por frequência de compra.

**Objetivos de aprendizagem:**
1. Restringir a população de teste à que pode exibir o desfecho e medir o
   efeito da restrição sobre a prevalência.
2. Ler um intervalo de confiança de proporção (Wilson) e um teste qui-quadrado
   como resposta à pergunta "a diferença é maior que o ruído?".
3. Estratificar uma associação por um terceiro fator e declarar se ela
   sobrevive, desaparece ou inverte.
4. Escolher a forma da figura (histograma, boxplot, scatterplot, série, barras
   com IC) pela pergunta que ela responde, e escrever o título como conclusão
   com o número dentro.

**Contrato do dia:** nenhuma figura entra no artefato sem o teste escrito
embaixo.

**Ambiente:** Antigravity, pasta clonada, duas skills novas.

### Agenda em minutos

| Horário | Bloco | Conteúdo |
|---|---|---|
| `13h00 - 13h15` | Resgate e contrato | O critério do rótulo como sabido. A PBL apresentada sem o perfil das contas; cada mesa escreve três hipóteses. Contrato: nenhuma figura entra no artefato sem o teste que a sustenta escrito embaixo |
| `13h15 - 13h40` | Bloco 1 e Prática 1 | Quem podia ser marcado: censura, a tabela das três populações. O perfil de compra por segmento (receita mediana, dias de compra, marcas, intervalo mediano entre compras, marca dominante) em tabela única. Prática 1: construir elegíveis e perfil por segmento com `skills/perfil-por-segmento.md` |
| `13h40 - 14h05` | Bloco 2 e Prática 2 | A diferença é maior que o ruído: IC de Wilson e qui-quadrado, cada um apresentado pela pergunta que responde, com figura didática (duas proporções cujos IC se cruzam, duas cujos IC não se cruzam) antes de qualquer número da base. Prática 2: cada mesa testa uma hipótese do caderno nas elegíveis (marcas, setor, região, marca comprada) e registra o veredito |
| `14h05 - 14h20` | Bloco 3 e quiz | A hipótese sobrevive ao controle: estratificação de marcas por segmento (sobrevive), de marcas por dias de compra (desaparece), de BR por segmento (inverte). Frequência de compra como vazamento. Quiz de verificação |
| `14h20 - 14h40` | Intervalo | |
| `14h40 - 14h55` | Bloco 4 e Prática 3 | A figura que decide: forma escolhida pela pergunta; título como conclusão; IC desenhado; linha de capacidade (138 planos) no gráfico de valor em risco. Prática 3: reestratificar a hipótese da mesa e produzir a figura com `skills/figura-que-decide.md` |
| `14h55 - 15h45` | Oficina do Artefato 1 | Seções 05 (rótulo, com a população elegível acrescentada), 06 (uma figura por segmento com o teste embaixo) e 07 (limitações, a começar pela causa que o dado observacional não fecha). Checkpoint às 15h30. Elástica até 16h15 |
| `15h45 - 16h00` | Amarração | O que fica pronto para a Entrega 1 de 05/09; o que a manhã do Prof. Donaire recebe (figuras da seção 06 com IC); a pergunta da Aula 05: um rótulo que não consegue marcar 55% da carteira serve de alvo? |

### Verificações do encontro

1. A prevalência da carteira é 19,2% e a das elegíveis é 42,5%. Qual vai para a
   figura do Comitê, e o que muda no tamanho da fila?
2. Contas de uma marca perdem 66,4% e de quatro ou mais perdem 16,1%, com IC que
   não se cruzam. Isso autoriza recomendar venda cruzada como retenção?
3. Duas mesas estratificaram a mesma hipótese por fatores diferentes e chegaram
   a vereditos opostos. Qual das duas está certa?

### Entregável

Três das sete seções do Artefato 1, em pasta reexecutável: rótulo (05), visuais
(06) e limitações (07). Com as quatro da Aula 03, o artefato fica completo para
a Entrega 1 de 05/09. Critério de aceite inalterado: outra pessoa clona, coloca
o dataset em `dados/`, executa e obtém as mesmas figuras e os mesmos números.

### Frameworks apresentados

IC de Wilson (Wilson, 1927); qui-quadrado de contingência (Pearson, 1900);
estratificação e paradoxo de Simpson (Simpson, 1951); vazamento (Kaufman et
al., 2012); censura como conceito de análise de sobrevivência, apresentado sem
o ferramental. Os três filtros, a elegibilidade e as skills são organização do
módulo, sem padrão publicado.

### Artefatos

| Artefato | Caminho | Observação |
|---|---|---|
| Números | `dados/analise_aula04.py` | elegíveis, perfil por segmento, IC, qui-quadrado, estratificações, par da PBL. `scipy` entra em `requirements-dev.txt` |
| Testes | `dados/tests/test_aula04_numeros.py`, `tools/tests/test_figuras_aula04.py`, `tools/tests/test_skills_aula04.py`, `tools/tests/test_deck_aula04.py`, `tools/tests/test_material_aula04.py` | cada número do deck transcrito literal; pulado quando o xlsx não existe |
| Figuras | `tools/gerar_figuras_aula04.py` | seis figuras: `aula04-ic-didatico`, `aula04-estratificacao-didatica`, `aula04-prevalencia-elegiveis`, `aula04-marcas-por-dias`, `aula04-par-pbl`, `aula04-fila-por-segmento`. 1168px, 1:1 |
| Deck | `tools/montar_deck_aula04.py` gerando `aulas/aula04.html` | 32 slides; não editado à mão |
| Material de apoio | `materiais/aula04-material-de-apoio.html` | explica IC, qui-quadrado e estratificação em prosa, com a leitura de negócio de cada teste |
| Skills | `inteli-pos-2026-2a-eda/skills/perfil-por-segmento.md`, `figura-que-decide.md`; `bivariada.md` ganha passo de elegibilidade e de estratificação | em duplicata com `materiais/` no acervo, como as anteriores |
| Repositório de clone | `AGENTS.md` e `CHECKLIST-ARTEFATO-1.md` | a seção 05 ganha "a população que o rótulo consegue marcar"; a 06 ganha "o teste escrito embaixo de cada figura" |
| Checklist no acervo | `materiais/checklist-artefato-1-tecnologia.md` | mesma mudança |
| Condução | `docs/notas-do-professor/aula04.md` | gabarito das estratificações e dos `account_id` da PBL; não distribuído |
| Planejamento | `PLANEJAMENTO_AULA_A_AULA.md`, seção S4 | reescrita no formato da S3, com divergência registrada |
| Portal e site | `index.html`, `tools/build_site.py` | card da Aula 04 e allowlist |

### Pendências abertas ao fim da S4

Registradas em 22/08/2026, antes da aula, para não virarem suposição na
condução.

1. **A oficina com o Prof. Donaire ainda não está confirmada para 29/08.** Este
   planejamento assume que os 50 minutos previstos se mantêm, com elasticidade
   até 16h15.
2. **O que os cadernos de hipóteses da Aula 01 registraram não está no
   repositório.** O veredito de cada hipótese testada em mesa depende desse
   registro, e ele precisa ser recuperado antes da condução.

### Divergência registrada

O planejamento original previa, para a S4, um gráfico de valor em risco por
probabilidade com a linha de capacidade operacional desenhada. A probabilidade
por conta só existe depois do modelo (UC2), então o gráfico entra com a
receita da conta no eixo e a linha de capacidade desenhada, sem probabilidade.
A PBL original falava em "ordem de deterioração" (receita, mix, cadência), que
o painel sintético tinha e a base oficial não tem alinhado; o par da PBL passa
a ser escolhido pela queda de receita entre semestres.

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
