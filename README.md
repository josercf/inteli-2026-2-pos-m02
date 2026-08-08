# Módulo 2 · Inteligência de Mercado e Modelagem Preditiva

Acervo didático da **Trilha de Tecnologia** do Módulo 2 do MBA em IA e Dados
para Negócios do Inteli, turma Lenovo 2026.2A.

O módulo é presencial, aos sábados. A manhã é de Negócios, com o Prof. Rafael
Donaire; a tarde é de Tecnologia, com o Prof. José Romualdo. O que a manhã
levanta como hipótese, a tarde submete ao dado.

Site publicado: <https://josercf.github.io/inteli-2026-2-pos-m02/>

## O que tem aqui

| Caminho | Conteúdo |
|---|---|
| `PLANO_DE_ENSINO.md` | Calendário, unidades curriculares, entregas e o case |
| `PLANEJAMENTO_AULA_A_AULA.md` | Roteiro minuto a minuto de cada encontro |
| `aulas/aulaNN.html` | Deck Reveal.js, um por aula |
| `notebooks/` | Laboratório da tarde, feito para o Google Colab |
| `materiais/` | O que o aluno preenche e entrega |
| `dados/` | Gerador, testes e o painel de contas da Kovan |
| `assets/` | Tema Inteli do segmento Exec, scripts e Reveal.js vendorizado |
| `tools/` | Validadores de marca e de layout, e o build do site |
| `docs/adrs/` | Decisões não triviais, com contexto e riscos |

Reveal.js está vendorizado em `assets/vendor/` de propósito: a aula precisa
rodar sem depender da rede da sala.

O material de condução (notas com gabarito e perguntas socráticas) não está no
repositório: ele revela as respostas das atividades e fica com o professor.

## O case

**Kovan Technologies LATAM.** O Net Revenue Retention do segmento estratégico
caiu de 109% para 93% em quatro trimestres. A decomposição do indicador mostrou
que a deterioração não veio de contratos encerrados: veio de contas que
continuam na base e compram menos.

O Comitê de Receita já decidiu construir um modelo de propensão. O que está em
aberto, e é o que os grupos precisam fechar, é o que exatamente ele deve prever:
a **ruptura de compra**, alvo binário e verificável que dispara tarde, ou a
**erosão de share of wallet**, alvo contínuo e antecipado que precisa ser
inventado e produz uma fila maior que a capacidade de resposta da área comercial.

## O painel de dados

`dados/kovan_painel_contas.csv`: 1.187 contas por 14 trimestres (2022Q3 a
2025Q4), 16.618 registros, 20 colunas, conforme o Exhibit 3 do Caderno de
Exhibits.

O painel **não tem coluna de risco, de propensão nem de rótulo**. Isso não é
lacuna: é a decisão em aberto do case.

Ele é sintético e traz de propósito as quatro advertências de qualidade do
exhibit (receita ausente, devoluções em coluna independente, quebra de taxonomia
em 2023 e engajamento comercial incompleto). A justificativa está em
`docs/adrs/ADR-001`.

## Rodar localmente

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
python3 -m http.server 8931     # servir por http: file:// muda o comportamento do Reveal
open http://localhost:8931/
```

Exportar um deck em PDF: abrir a URL com `?print-pdf` e usar o botão injetado
por `assets/js/inteli-print.js`. **O PDF exportado revela a resposta dos
quizzes**, então não distribuí-lo antes da aula.

## Regenerar e validar

```sh
python dados/gerar_painel_kovan.py           # regera o painel
python -m pytest dados/tests -q              # trava os numeros do case
python tools/check_brand.py                  # paleta, tipografia e iconografia
python tools/check_slides.py                 # estouro de slide e sobreposicao
python tools/build_site.py                   # monta _site/ e confere as referencias
python tools/montar_notebook_aula01.py       # regera o notebook da aula 01
```

`tools/build_site.py` monta o site a partir de uma **allowlist**, não da pasta
inteira: o diretório de trabalho tem material do programa e de outros clientes
que não pode ir para um site público, e uma allowlist erra para o lado de deixar
de publicar.

Passar nos validadores não é o mesmo que o slide estar bom: eles medem o estado
inicial da página e são cegos a fonte pequena demais para projeção, a figura
espremida e ao estado depois de o quiz ser respondido. Tirar screenshot continua
sendo parte do fluxo.
