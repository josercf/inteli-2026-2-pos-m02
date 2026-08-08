# CLAUDE.md

Orientação para o Claude Code neste repositório.

## O que é

Acervo didático da Trilha de Tecnologia do Módulo 2 do MBA em IA e Dados para
Negócios (Inteli x Lenovo, turma 2026.2A). Não é uma aplicação: é um site
estático de decks Reveal.js, notebooks de Colab, materiais do aluno e o gerador
do dataset do case, publicado no GitHub Pages.

Não há bundler nem package manager de JavaScript. A única dependência de
execução é Python, em `.venv` (`requirements-dev.txt`).

## Comandos

```bash
python3 -m http.server 8931                  # preview local (Reveal exige http, nao file://)
.venv/bin/python -m pytest dados/tests -q    # trava os numeros do case
.venv/bin/python tools/check_brand.py        # paleta, tipografia, segmento, emoji
.venv/bin/python tools/check_slides.py       # estouro de 1280x720 e sobreposicao
.venv/bin/python tools/build_site.py         # monta _site/ e confere referencias locais
.venv/bin/python dados/gerar_painel_kovan.py # regera o painel
.venv/bin/python tools/montar_notebook_aula01.py
.venv/bin/python tools/montar_deck_aula01.py    # regera o deck (nao editar o HTML a mao)
.venv/bin/python tools/gerar_figuras_aula01.py  # regera os GIFs de dado
.venv/bin/python tools/gerar_diagramas_svg.py   # regera os diagramas de ciclo
.venv/bin/python tools/medir_ocupacao.py        # faixa morta e ocupacao por slide

# push como josercf (o ssh-agent autentica primeiro como canaldoovidio)
GIT_SSH_COMMAND='ssh -i ~/.ssh/id_ed25519_josercf -o IdentitiesOnly=yes -F /dev/null' git push
```

## Três camadas que precisam ficar coerentes

1. **Planejamento** (raiz): `PLANO_DE_ENSINO.md` e `PLANEJAMENTO_AULA_A_AULA.md`
   são a fonte da verdade para data, título, escopo e entregável. Nenhum deck,
   notebook ou material inventa o que deveria descer daqui.
2. **Metodologia** (skills globais, fora do repositório):
   `~/.claude/skills/inteli-course-design/SKILL.md` e
   `~/.claude/skills/inteli-deck-design/SKILL.md`.
3. **Materiais**: `aulas/`, `notebooks/`, `materiais/`, `dados/`, `index.html`.

## O case e o dataset

Kovan Technologies LATAM. A decisão em aberto é o alvo do modelo: ruptura de
compra (binária, rara, tardia) ou erosão de share of wallet (contínua,
antecipada, sem rótulo no sistema).

`dados/gerar_painel_kovan.py` escreve a estrutura de episódios conta a conta, de
forma explícita, e a calibra contra os números impressos no case.
`dados/tests/test_painel_kovan.py` trava cada um desses números. **Mexeu no
gerador, roda a suíte**: um número que deixa de fechar vira material didático
que cita dado inexistente.

## Armadilhas conhecidas

- **Os testes canônicos rodam sobre `gerar(com_lacunas=False)`.** O painel
  entregue tem receita ausente de propósito. Reconstruir a lacuna por
  interpolação suaviza a queda dentro do episódio e a contagem por corte de
  limiar deixa de fechar: foi assim que dois dos 76 episódios do corte de 25%
  sumiram na primeira versão.
- **Teste que importa a mesma constante que o gerador usa concorda consigo
  mesmo.** O teste do Grupo Talvera passava mesmo com o dado alterado. Valores de
  exhibit ficam transcritos de forma literal no teste.
- **Slide que estoura os 720px não é detectável por `scrollHeight`**: a `section`
  tem altura fixa. Use `tools/check_slides.py`.
- **`aulas/aula01.html` é gerado, não editado.** A fonte é
  `tools/montar_deck_aula01.py`. Editar o HTML direto já custou duas vezes: a
  numeração de rodapé saiu errada ao inserir slides no meio, e uma substituição
  comeu um `</section>`, fazendo o Reveal juntar dois slides sem erro nenhum.
- **Figura é governada pela largura, nunca pela altura.** Com `max-height`, as
  figuras renderizavam entre 0,687 e 0,816 de escala: texto declarado em 16px
  chegava ao projetor com 11px e sobravam 26 a 35% da largura em branco. Elas
  são desenhadas em 1168px e renderizam 1:1.
- **Todo slide de conteúdo fecha com faixa de conclusão.** É o que ocupa o fundo
  do quadro e o que obriga a declarar o "e daí" da página. A faixa e a linha de
  fonte saem juntas dentro de `.fecho`: com `margin-top: auto` só na faixa, a
  linha de fonte caía fora do slide.
- **Título de slide de conteúdo é afirmativo; de prática, quiz e divisor, não.**
  Em quiz, título afirmativo entrega o gabarito. `test_deck_aula01.py` trava os
  dois casos e a lista de registros rejeitados.
- **Diagrama de ciclo é SVG embutido, não `<img>`.** Em `<img>` o fragment do
  Reveal não alcança o interior da figura. As cores vêm do tema, não do arquivo:
  se o SVG trouxesse hex literal, ele entraria no HTML e o `check_brand.py`
  passaria a reprovar o deck.
- **`concept-cards` é uma grade de três colunas.** Para quatro blocos, use o
  modificador `quatro`, senão o quarto fica sozinho com meio slide vazio ao lado.
  O layout passa no validador e mesmo assim lê como erro de montagem.
- **`check_slides.py` é cego a estado pós-interação**: ele nunca clica em nada.
  Responder o quiz e conferir o resultado é verificação manual.
- **`--window-size` de headless não é viewport CSS.** Para medir rolagem
  horizontal, use viewport real do Playwright e compare `scrollWidth` com
  `clientWidth`.
- **`recebidos/` e `docs/notas-do-professor/` nunca são commitados.** O primeiro
  tem o business case, o caderno de exhibits, o deck do Prof. Rafael Donaire e
  material de outro cliente; o segundo tem o gabarito das atividades. O
  repositório é público e o aluno chega nele.
- **`docs/adrs/` é versionado e público.** Nada que revele o achado plantado no
  dataset entra ali: esse conteúdo vive em `docs/notas-do-professor/`.
- **`tools/build_site.py` monta o Pages por allowlist**, não pela pasta inteira.
  Arquivo novo que precisa ir ao ar entra na lista.

## Convenções editoriais

- Português do Brasil com acentuação completa.
- Travessão em dash (U+2014) é proibido. Usar dois-pontos, vírgula, parênteses
  ou hífen.
- Emoji é proibido. A iconografia da marca é o Material Symbols.
- Não expor pesos de avaliação nem fórmulas de nota nos slides.
- Nenhum número do case aparece em material didático sem estar travado por teste.
- Data, título, escopo ou peso que não estiver nos documentos de planejamento
  vira pendência registrada, nunca suposição preenchida.
- Commits em Conventional Commits, escopo pela aula ou pela área:
  `feat(aula01): ...`, `fix(dados): ...`.
