# Skill de limpeza do painel Kovan: versão de referência

Procedimento completo de tratamento do arquivo `kovan_painel_contas.csv`, com
as quatro decisões já tomadas e justificadas. Serve como referência de
qualidade e como ponto de partida para adaptação.

Onde colar: no início de uma conversa no Gemini, nas instruções personalizadas
de um Gem, ou na pasta do projeto, para um agente que trabalha sobre arquivos
encontrar.

Vocabulário usado aqui: **linha** é um trimestre de uma conta; **coluna** é um
campo, como `receita_brl`; **valor ausente** é célula vazia no arquivo;
**imputar** é preencher célula vazia com um número estimado; **segmento**
classifica a conta em Estratégico, Médio ou Cauda; **pandas** é a biblioteca de
Python usada para ler e agregar a tabela.

## Regra de conduta, válida para toda a execução

1. Não estime, não interpole e não complete valor ausente. Célula vazia
   permanece vazia, com uma coluna de marcação ao lado.
2. Mostre o código que produziu cada número antes de apresentar esse número.
3. A cada tratamento, imprima a contagem de linhas afetadas.
4. Toda média de engajamento sai reportada por segmento.
5. Todo indicador sai acompanhado da contagem de linhas que entrou no cálculo.

## Passo 0: carregar e perfilar

```python
import pandas as pd
df = pd.read_csv("kovan_painel_contas.csv")
print(len(df), df["conta_id"].nunique(), sorted(df["trimestre"].unique()))
print(df.isna().sum())
```

Imprima, por coluna: tipo, contagem de vazios, mínimo, máximo e número de
valores distintos. Nenhum tratamento nesta etapa.

## Passo 1: receita ausente

Colunas `receita_brl` e `valor_medio_pedido_brl`, 160 linhas vazias nas duas ao
mesmo tempo, todas em conta com `status_conta == "Ativa"`.

```python
df["receita_ausente"] = df["receita_brl"].isna()
print(df["receita_ausente"].sum(), df.loc[df["receita_ausente"], "status_conta"].unique())
```

**Decisão: sinalizar a linha e excluí-la do cálculo de qualquer indicador que
use receita.** A lacuna registra atraso no fechamento contábil de uma conta que
segue comprando. Imputar zero converteria esse atraso na afirmação de que a
conta comprou R$ 0,00 no trimestre, o que aparece na série como uma queda
brusca e alimenta o alarme de ruptura com um episódio inexistente.

Aplicação: em cada agregação de receita, use `df[~df["receita_ausente"]]` e
imprima ao lado do resultado a contagem de linhas deixadas de fora.

## Passo 2: engajamento ausente, com teste de mecanismo

Colunas `visitas_registradas` e `interacoes_crm`, 8.280 linhas vazias nas duas
ao mesmo tempo. Meça a taxa de ausência por segmento antes de decidir qualquer
coisa: é esse teste que separa lacuna espalhada ao acaso de lacuna concentrada
em um grupo.

```python
df["engaj_ausente"] = df["visitas_registradas"].isna()
print((df.groupby("segmento")["engaj_ausente"].mean() * 100).round(1))
```

Resultado: Estratégico 29,4%, Médio 49,9%, Cauda 53,2%. A taxa acompanha o
segmento, então a ausência carrega informação sobre a própria conta.

**Decisão: manter a lacuna como lacuna, sem preencher com zero, e reportar toda
média de engajamento condicionada ao segmento.**

```python
base = df.dropna(subset=["visitas_registradas"])
print(base.groupby("segmento")["visitas_registradas"].mean().round(2))
print(len(df) - len(base), "linhas fora do cálculo")
```

Custo da alternativa descartada, medido com o mesmo código e uma linha trocada
(`df.assign(v=df["visitas_registradas"].fillna(0))`): com zero, o Estratégico
tem a maior média dos três segmentos, 2,45. Excluindo as linhas vazias, ele tem
a menor, 3,47. A ordem dos três segmentos inverte entre os dois tratamentos, e
cada ordem sustenta uma recomendação oposta sobre cobertura comercial.

## Passo 3: quebra de taxonomia em 2023Q1

```python
print(df.groupby("taxonomia_mix")["trimestre"].unique())
m = df.groupby("trimestre")["linhas_produto_ativas"].mean()
print(m[["2022Q4", "2023Q1", "2025Q4"]].round(2))
```

A coluna `taxonomia_mix` vale `pre_2023` apenas em 2022Q3 e 2022Q4. A média de
linhas de produto por conta sobe de 1,85 em 2022Q4 para 3,67 em 2023Q1, um
salto de 98,5% em um trimestre, sem contrapartida transacional. O salto vem da
recontagem de categorias.

**Decisão: nunca comparar contagem de linhas de produto através do corte de
2023Q1. A janela de análise começa em 2023Q1.**

```python
janela = df[df["taxonomia_mix"] == "pos_2023"]
print(len(df) - len(janela), "linhas fora da janela comparável")
```

Dentro dessa janela, a média cai 30,4% de 2023Q1 a 2025Q4, e essa queda é
erosão de mix real. Quem compara 2022Q4 contra 2025Q4 obtém +38,1% e conclui
que a carteira ampliou mix, com o sinal da erosão invertido.

## Passo 4: devoluções

```python
d = df["devolucoes_brl"]
print(int((d > 0).sum()), int((d < 0).sum()), int((d == 0).sum()))
df["receita_liquida_brl"] = df["receita_brl"] + d
```

A coluna traz 15.999 valores negativos, 619 zeros e nenhum positivo. O sinal
negativo já está no dado.

**Decisão: somar `devolucoes_brl` à receita.** Subtrair aplica o sinal duas
vezes e infla a receita líquida total em R$ 217.401.151,62, 2,59% do total.

## Passo 5: saída

Grave `kovan_painel_tratado.csv` com todas as colunas originais mais
`receita_ausente`, `engaj_ausente` e `receita_liquida_brl`. Nenhuma célula
vazia do arquivo original foi preenchida. Imprima a tabela final com o
indicador de cada passo, o valor sob a decisão adotada e o valor sob a
alternativa descartada.

## Passo 6: verificação final

Quem executar este arquivo corretamente obtém os valores abaixo. Um valor que
não bate indica erro de execução no passo correspondente.

| Medida | Valor esperado |
|---|---|
| Linhas com `receita_brl` vazia | 160 |
| `status_conta` distinto dessas linhas | apenas `Ativa` |
| Dessas, no segmento Estratégico | 14 |
| Linhas com `visitas_registradas` vazia | 8.280 |
| Linhas com `interacoes_crm` vazia | 8.280 |
| Taxa de ausência de engajamento, Estratégico | 29,4% |
| Taxa de ausência de engajamento, Médio | 49,9% |
| Taxa de ausência de engajamento, Cauda | 53,2% |
| Visitas médias excluindo vazias: Estratégico | 3,47 |
| Visitas médias excluindo vazias: Cauda | 4,49 |
| Visitas médias excluindo vazias: Médio | 4,58 |
| Visitas médias com zero: Cauda, Médio, Estratégico | 2,10 / 2,30 / 2,45 |
| Trimestres com `taxonomia_mix == "pre_2023"` | 2022Q3 e 2022Q4 |
| Média de `linhas_produto_ativas` em 2022Q4 | 1,85 |
| Média de `linhas_produto_ativas` em 2023Q1 | 3,67 |
| Média de `linhas_produto_ativas` em 2025Q4 | 2,55 |
| Salto de 2022Q4 para 2023Q1 | +98,5% |
| Variação de 2023Q1 a 2025Q4 | -30,4% |
| `devolucoes_brl` positivas, negativas, zeros | 0 / 15.999 / 619 |
| Receita bruta total | R$ 8.406.227.803,71 |
| Receita líquida somando devoluções | R$ 8.297.527.227,90 |
| Receita líquida subtraindo devoluções | R$ 8.514.928.379,52 |
| Diferença entre as duas | R$ 217.401.151,62 |

## O que esta skill não faz

Ela trata este painel. Os nomes de coluna, os quatro defeitos e os limiares de
verificação valem para `kovan_painel_contas.csv` e precisam ser trocados para
qualquer outra base.

Ela também não cobre: detecção de valores extremos, deduplicação de contas,
validação de faixa por coluna, conciliação com sistema de origem e qualquer
modelagem preditiva. Uma decisão de tratamento fora dos quatro passos acima
continua exigindo registro escrito, com o custo medido em número, no mesmo
formato usado aqui.
