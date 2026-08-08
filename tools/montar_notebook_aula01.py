# -*- coding: utf-8 -*-
"""
Monta notebooks/aula01_hipoteses.ipynb.

O notebook e escrito por script, e nao a mao, porque o JSON do formato .ipynb
e hostil a edicao manual (escape de aspas e de quebra de linha dentro de cada
celula) e porque o conteudo precisa ser revisado como texto, nao como JSON.

Regra que vale para tudo o que entra aqui: o notebook e publico e o aluno chega
nele antes da aula. Ele carrega o dado, da o dicionario de variaveis e o
registrador do caderno de hipoteses. Ele nao traz nenhuma resposta: nem a
contagem de rupturas, nem o rotulo pronto, nem a tabela que revela a ordem dos
sinais. Descobrir isso e a atividade da tarde.

Uso: python3 tools/montar_notebook_aula01.py
"""

from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "notebooks" / "aula01_hipoteses.ipynb"

URL_PAINEL = (
    "https://raw.githubusercontent.com/josercf/inteli-2026-2-pos-m02/"
    "main/dados/kovan_painel_contas.csv"
)


def md(texto: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": texto.strip("\n").splitlines(True)}


def code(texto: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": texto.strip("\n").splitlines(True),
    }


CELULAS = [
    md(
        """
# Kovan Technologies LATAM: da hipótese à evidência

**Módulo 2, Aula 1 (tarde).** MBA em IA e Dados para Negócios, Inteli x Lenovo.

De manhã seu grupo escreveu um backlog de hipóteses sobre o que explica a
deterioração das contas da Kovan. Esta tarde elas passam pelo dado.

## A regra da casa

**Todo número que entrar no seu caderno vem de código que a IA escreveu e que
você rodou.** Número que a IA cita de cabeça não entra. Não é desconfiança do
modelo: é que ele lê uma amostra do arquivo e completa o resto por
plausibilidade, e plausível não é o mesmo que verdadeiro.

Você não precisa escrever Python. Precisa saber pedir, rodar e conferir.
"""
    ),
    md(
        """
## 1. Carregar o painel

O painel tem 1.187 contas acompanhadas por 14 trimestres, de 2022Q3 a 2025Q4.
É a primeira vez que a operação LATAM tem ERP, CRM e as planilhas de cobertura
das quatro regiões na mesma tabela.
"""
    ),
    code(
        f"""
import pandas as pd

URL = "{URL_PAINEL}"
painel = pd.read_csv(URL)

print(painel.shape)
painel.head()
"""
    ),
    md(
        """
### O dicionário de variáveis

Rode a célula abaixo sempre que precisar lembrar o que uma coluna significa.
Vale a pena ler agora, inteiro: metade das hipóteses que não se sustentam
morrem por confundir duas colunas parecidas.
"""
    ),
    code(
        '''
DICIONARIO = {
    "conta_id": "Identificador da conta corporativa",
    "trimestre": "Trimestre calendário, de 2022Q3 a 2025Q4",
    "segmento": "Estrategico (118 contas), Medio (356), Cauda (713)",
    "regiao": "Brasil, Mexico & Norte LATAM, Cono Sur, Andina & Caribe",
    "am_id": "Account Manager responsável pelo território no trimestre",
    "receita_brl": "Receita faturada no trimestre. Contém registros ausentes",
    "pedidos": "Pedidos distintos faturados no trimestre",
    "linhas_produto_ativas": "Linhas de produto distintas compradas (1 a 6)",
    "valor_medio_pedido_brl": "Receita dividida pelo número de pedidos",
    "recencia_dias": "Dias entre o último pedido faturado e o fim do trimestre",
    "devolucoes_brl": "Devoluções e cancelamentos. Valor negativo",
    "desconto_medio_pct": "Desconto médio concedido no trimestre",
    "oportunidades_abertas": "Oportunidades registradas no CRM no trimestre",
    "oportunidades_perdidas": "Subconjunto das abertas com desfecho perdido",
    "valor_pipeline_brl": "Valor agregado das oportunidades abertas",
    "visitas_registradas": "Visitas do Account Manager. Ausente em parte da base",
    "interacoes_crm": "Interações registradas. Ausente na mesma parte da base",
    "troca_de_am_no_trimestre": "1 indica que o território mudou de responsável",
    "status_conta": "Ativa ou Encerrada",
    "taxonomia_mix": "pre_2023 ou pos_2023",
}

for coluna, descricao in DICIONARIO.items():
    print(f"{coluna:28} {descricao}")
'''
    ),
    md(
        """
---

## 2. Prática 1: o que a IA inventa quando não tem o dado

Antes de qualquer análise, uma calibração de confiança.

**Passo 1.** Abra o painel de IA do Colab e peça, em linguagem natural, sem
nenhuma estrutura:

> analise este arquivo e diga o que há de interessante

**Passo 2.** Agora peça uma coisa que o painel não tem:

> qual a margem média por conta no segmento estratégico?

Anote na célula abaixo o que aconteceu. Se você recebeu um número, procure a
coluna de onde ele saiu.
"""
    ),
    code(
        """
# Quais colunas existem, de verdade?
print(sorted(painel.columns))

# Existe alguma coluna de margem, custo ou lucro?
print([c for c in painel.columns if any(t in c for t in ("margem", "custo", "lucro"))])
"""
    ),
    md(
        """
> **Regra de ouro do dia:** número citado sem célula de origem é número não
> verificado.

Registre em uma frase, aqui mesmo, o que a ferramenta respondeu à pergunta da
margem:

*(escreva aqui)*
"""
    ),
    md(
        """
---

## 3. Prática 2: a mesma pergunta, em quatro níveis de prompt

A pergunta de negócio é a mesma nos quatro: **a queda de receita do segmento
estratégico é uniforme na carteira, ou está concentrada em um subconjunto de
contas?**

O que muda é o que você entrega ao modelo.

| Nível | O que você acrescenta |
|---|---|
| 0 | nada: "analise e diga o que achar" |
| 1 | CREATE: papel, pedido, exemplos, ajustes, formato, extras |
| 2 | estrutura na entrada e na saída: as colunas, o recorte, o formato da tabela |
| 3 | postura adversarial: o que refutaria este achado |

O CREATE é o mesmo que vocês viram de manhã. A diferença aqui é uma restrição
que vale para dado e não vale para texto:

> **use apenas colunas que existem no DataFrame `painel`; se faltar alguma
> informação, diga que falta em vez de estimar.**

**Peça o código, não a resposta.** Cole o prompt do nível 2 no painel de IA e
mande gerar o código na célula abaixo. Rode. O número sai daqui.
"""
    ),
    code(
        """
# Nível 2: peça à IA o código que responde se a queda está concentrada.
# Sugestão de recorte para o prompt: variação de receita entre 2024 e 2025 por
# conta, no segmento estratégico, distribuída em faixas.



"""
    ),
    code(
        """
# Nível 3: agora peça à IA que ataque o próprio achado.
# "Liste três explicações alternativas para este padrão que não sejam
#  deterioração de relacionamento, e diga que coluna do painel testaria cada uma."



"""
    ),
    md(
        """
---

## 4. Prática 3: o caderno de hipóteses

Cada grupo entrega três hipóteses do próprio backlog da manhã, operacionalizadas.

Uma hipótese só está operacionalizada quando você consegue preencher as seis
linhas do registro abaixo. Se você não consegue escrever **como refutar**, o
que você tem ainda é uma opinião.
"""
    ),
    code(
        '''
CADERNO = []


def registrar(enunciado, variaveis, operacao, janela, criterio_de_refutacao,
              prompt, numero_obtido, veredito, observacao=""):
    """Registra uma hipótese testada no caderno do grupo.

    veredito: "Confirmada", "Insuficiente" ou "Contraditada".

    "Insuficiente" não é fracasso: é o resultado honesto quando o painel não
    tem a coluna, a janela ou o número de casos para decidir. Metade das
    hipóteses de um backlog honesto termina assim.
    """
    assert veredito in {"Confirmada", "Insuficiente", "Contraditada"}, veredito
    assert criterio_de_refutacao.strip(), "sem critério de refutação não é hipótese"
    CADERNO.append(
        {
            "hipotese": enunciado,
            "variaveis": variaveis,
            "operacao": operacao,
            "janela": janela,
            "criterio_de_refutacao": criterio_de_refutacao,
            "prompt": prompt,
            "numero_obtido": numero_obtido,
            "veredito": veredito,
            "observacao": observacao,
        }
    )
    print(f"registrada ({len(CADERNO)}): {veredito} - {enunciado[:70]}")


# Exemplo do formato. Apague e escreva as suas.
registrar(
    enunciado="Contas que trocaram de Account Manager no trimestre têm menos "
              "interações registradas no CRM que contas que não trocaram.",
    variaveis="troca_de_am_no_trimestre, interacoes_crm",
    operacao="média de interacoes_crm nos dois grupos",
    janela="2023Q2 a 2025Q4 (antes disso a atividade não era obrigatória)",
    criterio_de_refutacao="se a diferença entre os dois grupos for menor que 10%, "
                          "a hipótese cai",
    prompt="(cole aqui o prompt que gerou o código)",
    numero_obtido="(preencha com o número que saiu do seu código)",
    veredito="Insuficiente",
    observacao="Se ela se confirmar, a leitura muda: queda de atividade no CRM "
               "pode ser troca de responsável, e não conta esfriando.",
)
'''
    ),
    code(
        """
# Hipótese 1 do seu grupo



"""
    ),
    code(
        """
# Hipótese 2 do seu grupo



"""
    ),
    code(
        """
# Hipótese 3 do seu grupo
# Em pelo menos uma das três, use o nível 3: peça à IA que tente derrubar o
# seu próprio achado antes de você fechar o veredito.



"""
    ),
    md(
        """
---

## 4b. Por que as mesas divergem: o mecanismo da ausência

Antes de contar rupturas, uma pergunta que decide a contagem: **por que este
valor está faltando?**

Rubin (1976) separou três mecanismos, e a diferença entre eles não é técnica, é
o que você pode ou não corrigir:

| Mecanismo | O que significa | O que dá para fazer |
|---|---|---|
| Completamente ao acaso | a falta não depende de nada | excluir a linha não enviesa, só perde potência |
| Ao acaso, dado o observado | a falta depende de algo que está na base | corrigir condicionando a esse algo |
| Não ao acaso | a falta depende justamente do que ela esconde | não dá, com o que existe na base |

As células abaixo medem em qual dos três cada ausência do painel se encaixa.
"""
    ),
    code(
        """
# A receita ausente depende do segmento? E do trimestre?
# Se a taxa de ausência for parecida entre grupos, o mecanismo é compatível
# com "completamente ao acaso". Se variar muito, não é.
painel["receita_ausente"] = painel["receita_brl"].isna()

print(painel.groupby("segmento")["receita_ausente"].mean().round(4))
print()
print(painel.groupby("trimestre")["receita_ausente"].mean().round(4).head())
"""
    ),
    code(
        """
# Agora a mesma pergunta para o engajamento comercial.
# Compare o padrão com o da receita: eles contam histórias diferentes.


"""
    ),
    md(
        """
> A conclusão desta célula muda o que você pode afirmar no caderno. Uma ausência
> que depende do segmento ainda é corrigível, porque o segmento está na base.
> Uma que depende do jeito como o cliente compra, não.

---

## 5. Prática 4: o rótulo que não existe

O painel não tem coluna de risco, de propensão nem de churn. Isso não é
esquecimento: é a decisão que está em aberto no case.

**Primeiro, um teste.** Peça à IA:

> crie uma coluna de churn neste dataset

Ela vai criar. Olhe o código que ela gerou e responda: **qual critério ela
escolheu, e ela avisou que estava escolhendo?**

**Depois, o Caminho A.** O rótulo do Caminho A é o único que existe no sistema:
uma conta rompe quando fica dois trimestres consecutivos sem nenhum pedido
faturado. Peça o código, rode, e conte quantas rupturas o segmento estratégico
teve nos 14 trimestres.
"""
    ),
    code(
        """
# Construa o rótulo do Caminho A e conte as rupturas do segmento estratégico.



"""
    ),
    md(
        """
### Antes de fechar

Compare o seu número com o do grupo ao lado. Se derem diferente, o problema não
é de código: é de decisão. Alguma coisa foi tratada de um jeito em uma mesa e de
outro jeito na outra.

Três perguntas para o fechamento:

1. Quantas contas do segmento estratégico romperam? Quantas observações
   conta-trimestre existem no segmento? Que fração isso dá?
2. Se o modelo precisa de quatro trimestres de histórico para calcular as
   variáveis, com quantos eventos você ficaria para treinar?
3. A área comercial consegue conduzir 138 planos de intervenção por trimestre.
   Um modelo que acende esse tanto de vezes por trimestre usa quanto dessa
   capacidade?
"""
    ),
    md(
        """
### Extensão, para quem terminar antes

O case afirma que, com 24 eventos efetivos, a validação não distingue um AUC de
0,71 de um de 0,84. Isso é verificável: a fórmula de Hanley e McNeil (1982) dá o
erro padrão do AUC a partir do número de positivos e de negativos.

Calcule o intervalo de confiança de 95% para 24 eventos e para 176, sobre as
1.652 observações do segmento estratégico, e responda: qual dos dois intervalos
consegue separar 0,71 de 0,84?
"""
    ),
    code(
        """
import math

def erro_padrao_auc(auc, n_pos, n_neg):
    \"\"\"Erro padrão do AUC, Hanley e McNeil (1982).\"\"\"
    q1 = auc / (2 - auc)
    q2 = 2 * auc**2 / (1 + auc)
    num = auc*(1-auc) + (n_pos-1)*(q1 - auc**2) + (n_neg-1)*(q2 - auc**2)
    return math.sqrt(num / (n_pos * n_neg))

# Complete: para cada número de eventos, imprima o intervalo de 95%.


"""
    ),
    code(
        """
# Exporta o caderno do grupo. Anexe o CSV na entrega.
caderno = pd.DataFrame(CADERNO)
caderno.to_csv("caderno_de_hipoteses.csv", index=False)
print(f"{len(caderno)} hipóteses registradas")
caderno[["hipotese", "veredito", "numero_obtido"]]
"""
    ),
    md(
        """
---

## O que fica pronto hoje

O caderno de hipóteses com veredito, e o painel carregado e conferido.

**O que a Aula 2 pega:** se o seu número de rupturas não bateu com o do grupo
ao lado, a causa está nas advertências de qualidade do painel. Elas são o
conteúdo da próxima tarde.

**O que isso alimenta:** o Artefato 1 da semana 5, a Análise de Segmentação
Estratégica e Personas Data-Driven.
"""
    ),
]

NOTEBOOK = {
    "cells": CELULAS,
    "metadata": {
        "colab": {"provenance": [], "toc_visible": True},
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 0,
}


def main() -> None:
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps(NOTEBOOK, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{SAIDA.name}: {len(CELULAS)} celulas")


if __name__ == "__main__":
    main()
