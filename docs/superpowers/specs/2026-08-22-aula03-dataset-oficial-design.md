# Aula 03: o corte que define o rótulo

- **Data:** 2026-08-22
- **Status:** Aprovado em conversa, implementação em curso
- **Decisores:** José Romualdo (docente da Trilha de Tecnologia)

## Contexto

A S3 estava planejada em quatro linhas: univariada e bivariada sobre o painel
sintético, com construção do rótulo de erosão em três cortes de limiar. Quatro
fatos mudaram o desenho entre 15/08 e 22/08:

1. O dataset oficial da Lenovo chegou em 21/08 (`dados/datasets_case_modulo2.xlsx`,
   cinco abas, 24 MB).
2. A turma reclamou da qualidade do painel sintético durante a Aula 02.
3. O Prof. Rafael Donaire e o docente da tarde combinaram dedicar parte das
   Aulas 03 e 04 à construção dos artefatos da Semana 5.
4. O horário mudou: 13h00 às 16h00, com folga até 16h30.

## Decisão

A Aula 03 apresenta o dataset oficial como substituição declarada, roda a tarde
inteira em Antigravity sobre um repositório de clone, e reserva o bloco final
para a construção do Artefato 1 de Tecnologia.

## O achado que organiza a aula

O `churn_label` do dataset oficial é constante por conta e inteiramente
determinado pelo último mês com receita:

| Último mês com receita | churn=0 | churn=1 |
|---|---|---|
| 2024-04 a 2025-01 | 0 | 1.482 |
| 2025-02 | 382 | 111 |
| 2025-03 a 2026-03 | 6.307 | 0 |

O rótulo entregue pronto é uma regra de inatividade com corte em torno de
fevereiro de 2025, que ninguém declarou. A aula faz a engenharia reversa desse
corte e mede o que cortes alternativos fariam com o tamanho da fila.

Segundo fato da mesma natureza: nenhuma das 4.494 contas com menos de 17 meses
de casa aparece como perdida.

## Eixo, reformulado

O Caminho A deixa de ser construção e vira auditoria de um rótulo existente. O
Caminho B continua em aberto, com argumento mais forte: o rótulo oficial só
marca conta que parou de comprar há mais de treze meses.

## Agenda

| Horário | Bloco |
|---|---|
| 13h00 - 13h15 | Resgate e contrato |
| 13h15 - 13h35 | Bloco 1 e Prática 1: CRISP-DM e a skill da Aula 02 contra a base nova |
| 13h35 - 13h55 | Bloco 2 e Prática 2: univariada |
| 13h55 - 14h20 | Bloco 3 e Prática 3: bivariada e a engenharia reversa do rótulo |
| 14h20 - 14h40 | Intervalo |
| 14h40 - 15h45 | Oficina do Artefato 1, elástica até 16h15 |
| 15h45 - 16h00 | Amarração |

## Ambiente

Antigravity na tarde inteira. Os grupos clonam
`github.com/josercf/inteli-pos-2026-2a-eda`, que traz `AGENTS.md`, as skills e a
pasta `dados/` vazia. Os CSVs chegam pelo canal da turma, fora do repositório,
porque são dado real de carteira LATAM e o acervo é público.

Sem plano B de ambiente, por decisão do docente. A mitigação que não custa tempo
de aula é o `analise_referencia.py` na pasta do dia: mesa travada executa e
continua com os números certos.

## Checklist do Artefato 1 de Tecnologia

Sete seções, espelhando a forma do checklist do Prof. Donaire, com a sexta
desenhada para alimentar a segmentação e as personas da manhã:

1. CARGA, 2. QUALIDADE, 3. UNIVARIADA, 4. BIVARIADA, 5. RÓTULO, 6. VISUAIS,
7. LIMITAÇÕES.

Em 65 minutos de oficina fecham quatro (carga, qualidade, univariada,
bivariada). Rótulo, visuais e limitações vão para o autoestudo da semana, e o
checklist marca essa divisão de forma explícita.

## Entregáveis

1. Repositório `github.com/josercf/inteli-pos-2026-2a-eda`
2. `dados/analise_aula03.py` e `dados/tests/test_dataset_oficial.py`
3. `tools/montar_deck_aula03.py` e `aulas/aula03.html`
4. `tools/gerar_figuras_aula03.py`
5. `materiais/aula03-material-de-apoio.html`
6. `materiais/checklist-artefato-1-tecnologia.md`
7. `docs/notas-do-professor/aula03.md`
8. ADR-005 (dataset oficial) e ADR-006 (Antigravity como ambiente único)
9. Seção S3 do `PLANEJAMENTO_AULA_A_AULA.md` e seção 5 do `PLANO_DE_ENSINO.md`
10. `.gitignore` do xlsx e allowlist do `tools/build_site.py`

## Restrições herdadas

- Nenhum número em slide sem teste que o trave.
- Sem paralelismo, sem em dash, sem emoji. Título de conteúdo é afirmativo, de
  prática e quiz não é.
- O painel sintético permanece no repositório para as Aulas 01 e 02, sem ser
  reapresentado.
