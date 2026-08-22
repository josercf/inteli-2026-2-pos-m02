# ADR-006: Antigravity como ambiente único, sobre um repositório de clone

- **Data:** 2026-08-22
- **Status:** Aceita
- **Decisores:** José Romualdo (docente da Trilha de Tecnologia)

> **Esta ADR emenda a ADR-003**, que colocou as práticas no Gemini e reservou ao
> Antigravity uma faixa de demonstração projetada. O risco que sustentava aquela
> divisão era a instalação em máquina corporativa, registrado lá como **não
> verificado**.

## Contexto

O risco de instalação foi resolvido entre a Aula 02 e a Aula 03: os grupos
instalaram o Antigravity e rodaram na própria máquina. A ADR-003 previa
explicitamente que instalação funcionando entraria como bônus, e ela funcionou
para a turma inteira.

Três exigências da Aula 03 apontam para o mesmo ambiente:

| Exigência do dia | Gemini | Antigravity |
|---|---|---|
| Ler as 207.826 linhas da aba de pedidos | Não cabe em anexo | Roda local |
| Executar a skill do grupo sem colar em conversa | Colagem manual | Lê da pasta |
| Produzir o Artefato 1, que é código que roda | Histórico de conversa | Pasta com script e figura |

A terceira é decisiva. O Artefato 1 de Tecnologia está definido no plano de
ensino como "código que carrega, limpa e visualiza o painel". Uma tarde inteira
de conversa não produz esse artefato.

A primeira também: o corte que define o `churn_label` só é recuperável no grão
do pedido (ADR-005), e essa aba tem 37,6 MB em CSV.

## Decisão

As quatro práticas e a oficina da Aula 03 rodam em Antigravity. Não há segundo
ambiente declarado.

Os grupos clonam `github.com/josercf/inteli-pos-2026-2a-eda`, que traz um
`AGENTS.md` na raiz com as regras da sessão, três skills em `skills/`, o
checklist do artefato e a pasta `dados/` vazia. O dataset entra por fora
(ADR-005).

## Motivações

- **O setup deixa de custar tempo de aula.** Clonar e abrir a pasta substitui o
  ritual de colar skill em conversa, que na Aula 02 consumiu minutos de cada
  prática e produziu estado divergente entre as mesas.
- **O `AGENTS.md` carrega as regras sem que o aluno as repita.** A proibição de
  preencher lacuna, a exigência de mostrar o código antes do número e a regra de
  salvar o que produzir passam a valer desde o primeiro prompt, para todos.
- **Um ambiente só elimina a troca de contexto.** A ADR-003 aceitou duas
  ferramentas porque a comparação entre elas era o conteúdo do bloco das 16h30.
  Esse conteúdo já foi dado.

## Riscos conhecidos

- **Mesa travada não tem para onde ir.** A decisão do docente foi ambiente
  único, sem plano B declarado, para não dividir a atenção da sala. Mitigação
  que não custa tempo de aula: a pasta traz `analise_referencia.py`, que produz
  os números do dia quando executado. Mesa travada roda o script e continua;
  mesa destravada nunca abre o arquivo.
- **O ciclo do agente é de minutos, não de segundos.** Mitigação: os blocos
  foram dimensionados para isso. As práticas curtas têm 20 a 25 minutos, contra
  os 15 do formato anterior, e a oficina tem 65.
- **O aluno pode commitar o dataset por engano.** Mitigação: o `.gitignore` do
  repositório de clone bloqueia `.csv`, `.xlsx` e `.parquet` dentro de `dados/`,
  e o `dados/LEIA-ME.md` diz por que.
- **O repositório é público e leva o nome da turma.** Ele não contém dado, nome
  de aluno nem material de terceiro. Contém estrutura, skills e checklist.

## Consequências

- Positivas: o entregável do dia é uma pasta reexecutável, que é literalmente o
  formato do Artefato 1; a aba de pedidos entra na aula; o setup cai para um
  clone.
- Negativas: a aula passa a depender de uma instalação por máquina, sem
  alternativa declarada em sala. O `analise_referencia.py` reduz o custo de uma
  mesa parada, e não elimina.

## ADRs relacionadas

- ADR-002 (Colab com IA integrada como ambiente das práticas)
- ADR-003 (Gemini nas práticas e Antigravity em demonstração), emendada por esta
- ADR-004 (a skill de agente em Markdown como artefato do aluno)
- ADR-005 (o dataset oficial substitui o painel sintético)
