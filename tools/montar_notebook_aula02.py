# -*- coding: utf-8 -*-
"""
Monta notebooks/aula02_limpeza.ipynb.

O notebook e escrito por script, e nao a mao, pela mesma razao do gerador da
Aula 1: o JSON do formato .ipynb e hostil a edicao manual e o conteudo precisa
ser revisado como texto.

Este notebook e o plano B declarado da tarde. A pratica corre no painel de IA
do Gemini, com o CSV anexado a conversa; se o upload falhar na conta
corporativa da turma, o grupo abre este notebook no Colab e continua daqui. E
tambem daqui que o grupo exporta o entregavel do dia: a base tratada e a
tabela de custo por decisao.

A celula de carga tenta o caminho local primeiro e cai para a URL bruta do
repositorio no GitHub quando o arquivo local nao existe, que e exatamente o
caso dentro do Colab. A celula da Pratica 4 aplica o mesmo padrao para ler a
skill de limpeza, porque o Colab tambem nao tem o arquivo local.

Uso: python3 tools/montar_notebook_aula02.py
"""

from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "notebooks" / "aula02_limpeza.ipynb"

REPO = "josercf/inteli-2026-2-pos-m02"
URL_PAINEL = f"https://raw.githubusercontent.com/{REPO}/main/dados/kovan_painel_contas.csv"
URL_SKILL = f"https://raw.githubusercontent.com/{REPO}/main/materiais/skill-limpeza-kovan.md"
URL_COLAB = f"https://colab.research.google.com/github/{REPO}/blob/main/notebooks/aula02_limpeza.ipynb"


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
        f"""
[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)]({URL_COLAB})

# Kovan Technologies LATAM: qualidade do dado antes do modelo

**Módulo 2, Aula 2.** MBA em IA e Dados para Negócios, Inteli x Lenovo.

A prática desta tarde roda no painel de IA do Gemini, com o CSV do painel
anexado à conversa. Este notebook é o plano B: se o upload falhar na conta
corporativa da turma, o grupo continua a atividade aqui, com o mesmo painel e
os mesmos quatro exercícios. É também daqui que o grupo exporta o entregável
do dia, ao final da Prática 4.

## A regra da casa

Todo número que entrar na entrega vem de código executado sobre o painel, não
de estimativa do modelo de IA. O Exhibit 3 do case lista quatro advertências
de qualidade sobre este dado. Esta aula mede o efeito de cada uma.
"""
    ),
    md(
        """
## 1. Carregar o painel

O painel tem 1.187 contas acompanhadas por 14 trimestres, de 2022Q3 a 2025Q4.
A célula abaixo tenta o arquivo local primeiro, do jeito que ele existe neste
repositório, e cai para a cópia publicada no GitHub quando o caminho local não
existe, que é o caso ao abrir este notebook no Colab.
"""
    ),
    code(
        f"""
import pandas as pd
from pathlib import Path

CAMINHO_LOCAL_PAINEL = Path("../dados/kovan_painel_contas.csv")
URL_PAINEL = "{URL_PAINEL}"

if CAMINHO_LOCAL_PAINEL.exists():
    painel = pd.read_csv(CAMINHO_LOCAL_PAINEL)
    origem_painel = f"arquivo local ({{CAMINHO_LOCAL_PAINEL}})"
else:
    painel = pd.read_csv(URL_PAINEL)
    origem_painel = "URL bruta do repositório (caminho local ausente, provável Colab)"

ORDEM_SEGMENTOS = ["Estrategico", "Medio", "Cauda"]

print(f"{{painel.shape[0]}} linhas, {{painel.shape[1]}} colunas")
print(f"origem: {{origem_painel}}")
painel.head()
"""
    ),
    md(
        """
---

## 2. Prática 1: perfilamento coluna a coluna

Antes de tratar qualquer coisa, descreva o que existe. Para cada coluna:
tipo, contagem de nulos, mínimo, máximo e número de valores distintos.
"""
    ),
    code(
        """
perfil = pd.DataFrame(
    {
        "tipo": painel.dtypes.astype(str),
        "nulos": painel.isna().sum(),
        "minimo": painel.min(numeric_only=False),
        "maximo": painel.max(numeric_only=False),
        "distintos": painel.nunique(),
    }
)
pd.set_option("display.max_rows", None)
perfil
"""
    ),
    md(
        """
Duas colunas concentram quase toda a contagem de nulos: `receita_brl` e
`visitas_registradas`. A próxima prática mede se essa ausência é uniforme na
carteira ou se ela se concentra em algum grupo de contas.
"""
    ),
    md(
        """
---

## 3. Prática 2: o mecanismo da ausência

`visitas_registradas` falta em parte da base. A pergunta que decide o que dá
para fazer com essa falta: **a taxa de ausência é igual nos três segmentos, ou
varia com o porte da conta?**

Se variar, a ausência não é completamente ao acaso, e o segmento observado é o
que explica boa parte dela.
"""
    ),
    code(
        """
taxa_ausencia_visitas = (
    painel.assign(sem_visita=painel["visitas_registradas"].isna())
    .groupby("segmento")["sem_visita"]
    .mean()
    .reindex(ORDEM_SEGMENTOS)
)

print((taxa_ausencia_visitas * 100).round(1).astype(str) + "%")

esperado = {"Estrategico": 0.2942, "Medio": 0.4990, "Cauda": 0.5317}
for segmento, valor_esperado in esperado.items():
    diferenca = abs(taxa_ausencia_visitas[segmento] - valor_esperado)
    assert diferenca < 0.0001, f"{segmento}: {taxa_ausencia_visitas[segmento]} != {valor_esperado}"
print("conferido: 29,4% no Estratégico, 49,9% no Médio, 53,2% na Cauda")
"""
    ),
    md(
        """
A taxa cresce de forma monotônica com a pulverização da carteira: quanto menor
a conta, maior a chance de a visita não ter sido registrada. Isso torna a
ausência corrigível em parte, porque o segmento que a explica está na própria
base, e ao mesmo tempo perigosa, porque qualquer tratamento que ignore o
segmento distorce a leitura de cobertura comercial de forma diferente em cada
grupo.

---

## 4. Prática 3: o confronto entre dois tratamentos

Duas decisões concorrentes para a mesma ausência:

- **Ausente vira zero.** Trata a falta de registro como zero visitas.
- **Excluir sem registro.** Remove a linha da conta.

As duas funções abaixo aplicam cada decisão, e a tabela final compara a média
de visitas por segmento sob as duas.
"""
    ),
    code(
        """
def ausente_vira_zero(df):
    \"\"\"Preenche a ausência de visitas com zero.\"\"\"
    return df.assign(visitas_tratadas=df["visitas_registradas"].fillna(0))


def excluir_sem_registro(df):
    \"\"\"Remove as linhas sem registro de visita.\"\"\"
    return df.dropna(subset=["visitas_registradas"]).rename(
        columns={"visitas_registradas": "visitas_tratadas"}
    )


media_ausente_zero = (
    ausente_vira_zero(painel).groupby("segmento")["visitas_tratadas"].mean().reindex(ORDEM_SEGMENTOS)
)
media_excluir = (
    excluir_sem_registro(painel).groupby("segmento")["visitas_tratadas"].mean().reindex(ORDEM_SEGMENTOS)
)

comparacao = pd.DataFrame(
    {"ausente_vira_zero": media_ausente_zero, "excluir_sem_registro": media_excluir}
).round(2)
comparacao
"""
    ),
    code(
        """
# Confere a tabela contra os valores travados por dados/tests/test_aula02_numeros.py
esperado_zero = {"Cauda": 2.1012, "Medio": 2.2959, "Estrategico": 2.4479}
esperado_excluir = {"Estrategico": 3.4683, "Cauda": 4.4864, "Medio": 4.5827}

for segmento, valor in esperado_zero.items():
    assert abs(media_ausente_zero[segmento] - valor) < 0.0001, segmento
for segmento, valor in esperado_excluir.items():
    assert abs(media_excluir[segmento] - valor) < 0.0001, segmento

print("conferido: as duas colunas batem com a Prática 3.")
print()
print("Ausente vira zero, do maior para o menor:", list(media_ausente_zero.sort_values(ascending=False).index))
print("Excluir sem registro, do maior para o menor:", list(media_excluir.sort_values(ascending=False).index))
"""
    ),
    md(
        """
O segmento Estratégico tem a maior média de visitas sob "ausente vira zero" e
a menor média sob "excluir sem registro". As duas leituras sustentam
recomendações opostas sobre onde reforçar cobertura comercial, e a diferença
inteira vem da decisão de tratamento, não do dado em si.

---

## 5. Prática 4: aplicar a skill de limpeza preenchida

`materiais/skill-limpeza-kovan.md` registra, para cada advertência do
Exhibit 3, a decisão do grupo, a justificativa e o custo medido no indicador
que a decisão altera. A célula abaixo lê esse arquivo preenchido e aplica os
passos que ele descreve. A conferência da Prática 3 é literal: a média de
visitas por segmento sob a decisão registrada no Passo 3 tem que reproduzir a
coluna correspondente da tabela acima.
"""
    ),
    code(
        f"""
import re

CAMINHO_LOCAL_SKILL = Path("../materiais/skill-limpeza-kovan.md")
URL_SKILL = "{URL_SKILL}"

if CAMINHO_LOCAL_SKILL.exists():
    texto_skill = CAMINHO_LOCAL_SKILL.read_text(encoding="utf-8")
    origem_skill = f"arquivo local ({{CAMINHO_LOCAL_SKILL}})"
else:
    import urllib.request

    with urllib.request.urlopen(URL_SKILL) as resposta:
        texto_skill = resposta.read().decode("utf-8")
    origem_skill = "URL bruta do repositório (caminho local ausente, provável Colab)"

print(f"skill lida de: {{origem_skill}}")


def ler_decisao(texto, numero_passo):
    \"\"\"Extrai a linha 'Decisão do grupo:' de um passo da skill.\"\"\"
    padrao = rf"## Passo {{numero_passo}}:.*?Decisão do grupo:\\s*(.+)"
    encontrado = re.search(padrao, texto, re.DOTALL)
    if not encontrado:
        raise ValueError(f"Passo {{numero_passo}} não encontrado na skill")
    return encontrado.group(1).splitlines()[0].strip()


decisao_passo2 = ler_decisao(texto_skill, 2)
decisao_passo3 = ler_decisao(texto_skill, 3)
decisao_passo4 = ler_decisao(texto_skill, 4)
decisao_passo5 = ler_decisao(texto_skill, 5)

for numero, decisao in enumerate([decisao_passo2, decisao_passo3, decisao_passo4, decisao_passo5], start=2):
    print(f"Passo {{numero}}: {{decisao!r}}")
"""
    ),
    code(
        """
# Passo 2: receita ausente. Indicador sugerido: receita média por linha.
# A soma ignora ausentes nas duas leituras e não muda entre elas: quem muda
# com a decisão é o denominador, por isso o indicador é a média, não a soma.
linhas_afetadas_p2 = int(painel["receita_brl"].isna().sum())

if "EXCLUIR" in decisao_passo2.upper():
    receita_decisao = painel.dropna(subset=["receita_brl"])["receita_brl"].mean()
    receita_alternativa = painel["receita_brl"].fillna(0).mean()
else:
    receita_decisao = painel["receita_brl"].fillna(0).mean()
    receita_alternativa = painel.dropna(subset=["receita_brl"])["receita_brl"].mean()

print(f"linhas afetadas: {linhas_afetadas_p2}")
print(f"receita média por linha, com a decisão: {receita_decisao:,.2f}")
print(f"receita média por linha, com a alternativa: {receita_alternativa:,.2f}")
"""
    ),
    code(
        """
# Passo 3: engajamento comercial. Confere contra a Prática 3.
linhas_afetadas_p3 = int(painel["visitas_registradas"].isna().sum())

if "EXCLUIR" in decisao_passo3.upper():
    tratado_p3 = excluir_sem_registro(painel)
    valor_decisao_geral, valor_alternativa_geral = (
        excluir_sem_registro(painel)["visitas_tratadas"].mean(),
        ausente_vira_zero(painel)["visitas_tratadas"].mean(),
    )
    media_referencia = media_excluir
else:
    tratado_p3 = ausente_vira_zero(painel)
    valor_decisao_geral, valor_alternativa_geral = (
        ausente_vira_zero(painel)["visitas_tratadas"].mean(),
        excluir_sem_registro(painel)["visitas_tratadas"].mean(),
    )
    media_referencia = media_ausente_zero

media_p3_por_segmento = tratado_p3.groupby("segmento")["visitas_tratadas"].mean().reindex(ORDEM_SEGMENTOS)

diferenca_maxima = (media_p3_por_segmento - media_referencia).abs().max()
assert diferenca_maxima < 1e-9, "a skill preenchida não reproduz a Prática 3"

print(f"linhas afetadas: {linhas_afetadas_p3}")
print(f"média geral de visitas, com a decisão: {valor_decisao_geral:.4f}")
print(f"média geral de visitas, com a alternativa: {valor_alternativa_geral:.4f}")
print("conferido: a média por segmento reproduz a Prática 3.")
media_p3_por_segmento.round(2)
"""
    ),
    code(
        """
# Passo 4: mudança de taxonomia em 2023Q1. Indicador sugerido: média de
# linhas de produto por trimestre. A janela comparável começa em 2023Q1.
linhas_afetadas_p4 = int((painel["taxonomia_mix"] == "pre_2023").sum())

media_por_trimestre = painel.groupby("trimestre")["linhas_produto_ativas"].mean()
variacao_janela_comparavel = media_por_trimestre["2025Q4"] / media_por_trimestre["2023Q1"] - 1
variacao_janela_completa = media_por_trimestre["2025Q4"] / media_por_trimestre["2022Q4"] - 1

if "COMPLETA" in decisao_passo4.upper() or "MANTER" in decisao_passo4.upper():
    variacao_decisao, variacao_alternativa = variacao_janela_completa, variacao_janela_comparavel
else:
    variacao_decisao, variacao_alternativa = variacao_janela_comparavel, variacao_janela_completa

print(f"linhas na taxonomia antiga (fora da janela comparável): {linhas_afetadas_p4}")
print(f"média de linhas de produto, 2022Q4: {media_por_trimestre['2022Q4']:.2f}")
print(f"média de linhas de produto, 2023Q1: {media_por_trimestre['2023Q1']:.2f}")
print(f"variação 2023Q1 a 2025Q4, janela comparável: {variacao_janela_comparavel:.1%}")
print(f"variação 2022Q4 a 2025Q4, janela completa: {variacao_janela_completa:.1%}")
"""
    ),
    code(
        """
# Passo 5: devoluções, coluna própria com sinal negativo. Indicador sugerido:
# receita líquida total.
linhas_afetadas_p5 = int((painel["devolucoes_brl"] < 0).sum())

receita_bruta_total = painel["receita_brl"].sum()
devolucoes_total = painel["devolucoes_brl"].sum()
liquida_somando = receita_bruta_total + devolucoes_total
liquida_subtraindo = receita_bruta_total - devolucoes_total

if "SUBTRAIR" in decisao_passo5.upper():
    liquida_decisao, liquida_alternativa = liquida_subtraindo, liquida_somando
else:
    liquida_decisao, liquida_alternativa = liquida_somando, liquida_subtraindo

diferenca_milhoes = abs(liquida_subtraindo - liquida_somando) / 1_000_000

print(f"linhas com devolução registrada: {linhas_afetadas_p5}")
print(f"receita líquida, somando devoluções (sinal como veio): {liquida_somando:,.2f}")
print(f"receita líquida, subtraindo devoluções (dobra o sinal): {liquida_subtraindo:,.2f}")
print(f"diferença entre as duas leituras: R$ {diferenca_milhoes:.1f} milhões")

assert abs(diferenca_milhoes - 217.4) < 0.1, diferenca_milhoes
"""
    ),
    md(
        """
---

## 6. Exportação do entregável

A base tratada, com as decisões dos passos 2, 3 e 5 aplicadas, e a tabela de
custo por decisão: um indicador por passo, o valor sob a decisão registrada,
o valor sob a alternativa descartada e a contagem de linhas que o tratamento
tocou.
"""
    ),
    code(
        """
base_tratada = painel.copy()

if "EXCLUIR" in decisao_passo2.upper():
    base_tratada = base_tratada.dropna(subset=["receita_brl"])
else:
    base_tratada["receita_brl"] = base_tratada["receita_brl"].fillna(0)

if "EXCLUIR" in decisao_passo3.upper():
    base_tratada = base_tratada.dropna(subset=["visitas_registradas"])
else:
    base_tratada["visitas_registradas"] = base_tratada["visitas_registradas"].fillna(0)

base_tratada.to_csv("painel_kovan_tratado.csv", index=False)

tabela_custo = pd.DataFrame(
    [
        {
            "passo": "2. Receita ausente",
            "indicador": "Receita média por linha (BRL)",
            "decisao": decisao_passo2,
            "valor_com_decisao": round(receita_decisao, 2),
            "valor_com_alternativa": round(receita_alternativa, 2),
            "linhas_afetadas": linhas_afetadas_p2,
        },
        {
            "passo": "3. Engajamento comercial",
            "indicador": "Média geral de visitas",
            "decisao": decisao_passo3,
            "valor_com_decisao": round(valor_decisao_geral, 4),
            "valor_com_alternativa": round(valor_alternativa_geral, 4),
            "linhas_afetadas": linhas_afetadas_p3,
        },
        {
            "passo": "4. Mudança de taxonomia",
            "indicador": "Variação de linhas de produto, 2023Q1 a 2025Q4",
            "decisao": decisao_passo4,
            "valor_com_decisao": round(variacao_decisao, 4),
            "valor_com_alternativa": round(variacao_alternativa, 4),
            "linhas_afetadas": linhas_afetadas_p4,
        },
        {
            "passo": "5. Devoluções",
            "indicador": "Receita líquida total (BRL)",
            "decisao": decisao_passo5,
            "valor_com_decisao": round(liquida_decisao, 2),
            "valor_com_alternativa": round(liquida_alternativa, 2),
            "linhas_afetadas": linhas_afetadas_p5,
        },
    ]
)
tabela_custo.to_csv("custo_por_decisao.csv", index=False)

print(f"base tratada: {base_tratada.shape[0]} linhas, {base_tratada.shape[1]} colunas")
print("arquivos gravados: painel_kovan_tratado.csv, custo_por_decisao.csv")
tabela_custo
"""
    ),
    md(
        """
---

## O que fica pronto hoje

A base tratada e a tabela de custo por decisão, prontas para anexar à
entrega. Cada linha da tabela mostra o que a decisão do grupo custou, medido
no indicador que ela altera, ao lado do que a alternativa descartada teria
dado.

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
