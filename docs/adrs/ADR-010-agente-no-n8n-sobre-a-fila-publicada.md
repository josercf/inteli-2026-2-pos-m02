# ADR-010: o modelo roda no navegador e uma equipe de três agentes no n8n responde sobre a fila

- **Data:** 03/10/2026
- **Status:** aceita (revisada no mesmo dia; ver Histórico)
- **Decisores:** Prof. José Romualdo da Costa Filho

## Contexto

A UC2 Aula 4 pede o pipeline integrado: modelo, API generativa e interface. A
pendência registrada na S8 era a chave de API para uso em sala. A turma tem
acesso ao n8n do Inteli (inteli.app.n8n.cloud) e pode criar chave gratuita no
OpenRouter.

A Aula 08 é invertida: os alunos trabalham a partir de um guia e o professor
circula. Isso exige um caminho sem instalação e sem passo que dependa do
ambiente Python de cada máquina.

## Decisão

O painel (`painel/index.html` e `painel/modelo.js`) lê a planilha original do
case no navegador, monta seis colunas por conta com histórico até 2024-02,
treina uma regressão logística com escore fora da amostra e ordena a fila por
valor esperado. A fila segue, a cada pergunta, para um workflow fixo do n8n
(`painel/workflow_n8n.json`) com três agentes em sequência: Atlas (analista),
Vera (estrategista, aplica os planos de ação das áreas) e Ciro (revisor). O
modelo de linguagem é escolhido no painel, com um modelo `:free` do OpenRouter
como padrão e o Jev Router da TypeSafe como opção.

## Motivações

- Nenhuma instalação: a planilha entra como chegou e o arquivo do workflow não
  carrega dado, então serve a todos os grupos.
- A planilha não sai do navegador. Ao n8n vão só as 138 contas da fila, com
  identificador anonimizado e as colunas que a tela mostra.
- A divisão em três agentes torna visível onde a resposta errou: no número
  (Atlas), na ação (Vera) ou na conferência (Ciro).
- O mesmo cálculo existe em Python (`dados/analise_aula08.py`), e
  `tools/tests/test_painel_modelo.py` compara os dois conta a conta.
- A chave gratuita resolve a pendência sem custo e sem a chave passar por
  arquivo ou repositório: ela fica numa credencial do n8n de cada aluno.

## Riscos conhecidos

- **URL pública do webhook.** Quem tem o endereço consulta a equipe do grupo.
  Mitigação: o endpoint não entra no repositório publicado; cada pessoa cola no
  painel e ele fica no navegador dela.
- **Limite do plano gratuito.** 20 requisições por minuto e 50 por dia por
  conta, e cada pergunta usa três. Mitigação: uma chave por aluno e a bateria
  dimensionada em 12 requisições.
- **O Jev cobra por uso.** Com chave sem crédito ele devolve erro. Mitigação:
  o padrão é gratuito, e a comparação com o Jev é demonstrada pelo professor.
- **Modelo gratuito sai do catálogo.** Mitigação: o identificador é um campo do
  painel, e o guia ensina a reconhecer o sufixo `:free`.
- **A base curta de 24 meses não tem histórico antes do corte.** Mitigação:
  `modelo.js` reconhece a base pela primeira data e devolve mensagem que
  explica qual arquivo usar.
- **Fila inteira no prompt de três agentes.** São cerca de 17 mil tokens por
  chamada. Aceito para 138 contas; uma fila maior pediria ferramenta de
  consulta em vez de contexto.

## Consequências

Positivas: o aluno vai do arquivo original ao painel publicado no GitHub Pages
sem instalar nada, e o grupo modifica a cópia em `frontend/` do repositório de
prática. O nome de coluna que dois modelos leram errado
(`queda_contra_pico`) virou `receita_12m_como_fracao_do_pico_anual`.

Negativas: o modelo do navegador é uma regressão logística de seis colunas, mais
simples que o pacote da Aula 07 (AUC 0,814 contra 0,825). A Aula 07 continua
sendo a referência de engenharia.

## Histórico

A primeira versão desta ADR, no mesmo dia, publicava a fila calculada em Python
(`app.publicar`) embutida num nó Code do n8n, com um único agente. Ela foi
substituída porque exigia rodar o modelo localmente antes de cada uso, o que
não se sustenta numa aula invertida.

## ADRs relacionadas

- ADR-005: o dataset oficial e a base que não é versionada.
- ADR-008: a regressão logística por IRLS, que o painel reproduz em JavaScript.
- ADR-009: o aplicativo da Aula 07 no repositório de prática.
