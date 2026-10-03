# ADR-010: o agente da Aula 08 roda no n8n e consulta a fila publicada em lote

- **Data:** 03/10/2026
- **Status:** aceita
- **Decisores:** Prof. José Romualdo da Costa Filho

## Contexto

A UC2 Aula 4 pede o pipeline integrado: modelo, API generativa e interface. A
pendência registrada na S8 era a chave de API para uso em sala. A turma tem
acesso ao n8n do Inteli (inteli.app.n8n.cloud), e o workspace já tem uma
credencial OpenRouter.

O modelo da Aula 07 é scikit-learn, treinado na máquina do grupo. O n8n não
executa Python com scikit-learn.

## Decisão

O grupo publica o resultado do modelo, e não o modelo: `python -m app.publicar`
grava a fila do ciclo (138 contas, por valor esperado) e um workflow do n8n com
essa fila embutida num nó Code. O mesmo workflow expõe a fila por Webhook e liga
um AI Agent, com modelo do OpenRouter, a essa URL como ferramenta.

Um terceiro gatilho, `POST /webhook/kovan-chat-<grupo>`, atende o painel web
(`painel/index.html` no acervo, copiado em `frontend/` no repositório de
prática). O painel envia a pergunta, as linhas da planilha e os planos de ação
de Comercial, Atendimento e Pós-vendas, e o agente responde apoiado só nesse
material. A turma usa o painel publicado primeiro e depois adapta a própria
cópia.

## Motivações

- O escore só muda quando a base muda, uma vez por ciclo. Inferência em lote
  atende o caso sem servidor de modelo.
- Um arquivo de importação elimina a montagem do workflow à mão, que numa aula
  de duas horas consumiria o tempo da bateria de teste.
- O agente consulta a mesma URL que qualquer outro sistema usaria, então o
  número que ele cita é auditável contra a API.
- A credencial OpenRouter do workspace resolve a pendência da chave sem que a
  chave passe por arquivo, prompt ou repositório.

## Riscos conhecidos

- **URL pública.** O Webhook e o chat ficam abertos para quem tiver o link.
  Mitigação: só saem identificador anonimizado e os campos que a tela da Aula 07
  já mostrava, com a lista travada em `app/tests/test_publicar.py`. O deck
  declara que um uso real pediria autenticação.
- **Dado real em serviço externo.** A fila é derivada da base real. Mitigação:
  nenhum pedido, nome ou cadastro sai; o n8n é o tenant do Inteli.
- **Colisão de URL entre grupos.** O caminho do webhook leva o nome do grupo,
  passado em `--grupo`.
- **Versão de nó.** O arquivo declara `typeVersion` dos nós de IA. Uma
  atualização do n8n pode pedir revisão; o script de captura importa o arquivo
  real e falha se o n8n recusar.
- **A planilha inteira vai no prompt.** O painel limita a 300 linhas por
  pergunta. A fila do ciclo tem 138.
- **A mesma pergunta pode indicar áreas diferentes** quando duas se aplicam.
  Observado na demonstração com a Conta D; o deck ensina a ordenar as áreas no
  plano.

## Consequências

Positivas: a camada generativa do Artefato 2 sai pronta para teste, e a regra
"todo número sai da ferramenta" é verificável na aba Executions.

Negativas: a fila no n8n envelhece até alguém rodar `app.publicar` de novo, e a
reimportação substitui o workflow do grupo.

## ADRs relacionadas

- ADR-009: o aplicativo vive no repositório de prática.
