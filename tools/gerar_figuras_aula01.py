# -*- coding: utf-8 -*-
"""
Gera as figuras da Aula 01 em assets/img/.

Tres GIFs animados e dois diagramas SVG. As figuras sao geradas por script, e
nao desenhadas a mao, para que a paleta venha sempre da mesma constante e para
que uma mudanca no case (por exemplo, a serie do Grupo Talvera) se propague sem
alguem precisar lembrar de reabrir um editor de imagem.

As duas series do GIF de contas saem do painel gerado, nao de numeros digitados
aqui: se o gerador do dataset mudar, a figura muda junto ou o teste falha.

Cores: apenas a paleta oficial (brandbook p.66), segmento Exec/Pos.
Tipografia: os GIFs usam DejaVu Sans, que acompanha o matplotlib. As fontes da
marca (Platypi e Manrope) sao webfonts e nao estao instaladas no sistema; num
raster nao ha como consumi-las por token, entao a escolha e uma sans neutra, e
nao uma imitacao. Os SVG usam a pilha de fontes do proprio deck.

Uso: python3 tools/gerar_figuras_aula01.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch  # noqa: E402
from PIL import Image  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "assets" / "img"
sys.path.insert(0, str(RAIZ))

# Paleta oficial (brandbook p.66). Nenhuma cor fora daqui entra numa figura.
ROXO = "#2e2640"
CORAL = "#ff4545"
VERDE_ESCURO = "#066d73"
CINZA_ESCURO = "#b2b6bf"
CINZA_MEDIO = "#caced6"
CINZA_CLARO = "#e6eaeb"
BRANCO = "#ffffff"

FONTE = "DejaVu Sans"

# A figura ocupa a faixa util do slide (1168px de largura) e e renderizada 1:1.
# Antes as figuras eram desenhadas em 1100 a 1150px de largura e o CSS as
# limitava por ALTURA (max-height: 408px), o que impunha fator de escala entre
# 0,687 e 0,816: texto declarado em 16px chegava ao projetor com 11px, abaixo
# do piso de legibilidade que o proprio tema declara, e a figura usava so 65 a
# 74% da largura disponivel. Desenhar na proporcao da faixa resolve os dois de
# uma vez.
LARGURA_FAIXA = 1168
ALTURA_FAIXA = 334
DPI = 100

# Duracao de um quadro, em milissegundos.
QUADRO_MS = 1500
# O ultimo quadro segura mais tempo: e onde esta a leitura, e um loop que passa
# direto por ele nao da tempo de ninguem ler numa projecao.
FINAL_MS = 4500

plt.rcParams["font.family"] = FONTE
plt.rcParams["text.color"] = ROXO
plt.rcParams["axes.labelcolor"] = ROXO
plt.rcParams["xtick.color"] = ROXO
plt.rcParams["ytick.color"] = ROXO
plt.rcParams["xtick.labelsize"] = 15
plt.rcParams["ytick.labelsize"] = 15


def salvar_gif(desenhar, n_quadros: int, destino: Path) -> None:
    """Renderiza quadro a quadro e monta o GIF.

    Nao usa FuncAnimation de proposito. Com ele os artistas da figura sao
    mutados no lugar, o primeiro quadro ja saia com a serie inteira desenhada e
    o titulo, criado vazio antes do tight_layout, ficava cortado fora da figura.
    Alem disso nao havia como dar ao ultimo quadro uma duracao diferente. Aqui
    cada quadro e uma figura inteira, descartada em seguida: mais lento, e sem
    estado compartilhado para vazar de um quadro para o outro.
    """
    quadros = []
    for k in range(n_quadros):
        fig = desenhar(k)
        fig.canvas.draw()
        imagem = Image.frombytes(
            "RGBA", fig.canvas.get_width_height(), bytes(fig.canvas.buffer_rgba())
        ).convert("RGB")
        quadros.append(imagem)
        plt.close(fig)
    duracoes = [QUADRO_MS] * (n_quadros - 1) + [FINAL_MS]
    quadros[0].save(
        destino,
        save_all=True,
        append_images=quadros[1:],
        duration=duracoes,
        loop=0,
    )


def _figura_ciclo():
    # A area util do slide e larga e baixa. Com ylim folgado o desenho ficava
    # numa faixa fina no meio, com metade da figura em branco, e a figura
    # projetada aparecia menor do que precisava.
    fig, ax = plt.subplots(figsize=(LARGURA_FAIXA / DPI, ALTURA_FAIXA / DPI), dpi=DPI)
    fig.patch.set_facecolor(BRANCO)
    ax.set_xlim(-1.80, 1.80)
    ax.set_ylim(-1.00, 1.00)
    ax.set_position([0, 0, 1, 1])
    ax.axis("off")
    return fig, ax


def _desenha_ciclo(ax, itens, pos, arco_cor):
    n = len(itens)
    for i in range(n):
        x1, y1 = pos[i]
        x2, y2 = pos[(i + 1) % n]
        ax.add_patch(
            FancyArrowPatch(
                (x1 * 0.58, y1 * 0.58),
                (x2 * 0.58, y2 * 0.58),
                connectionstyle="arc3,rad=-0.24",
                arrowstyle="-|>",
                mutation_scale=16,
                linewidth=2.0,
                color=arco_cor,
            )
        )


def _posicoes(n, rx=1.26, ry=0.74):
    angulos = [math.pi / 2 - 2 * math.pi * i / n for i in range(n)]
    return [(rx * math.cos(a), ry * math.sin(a)) for a in angulos]


# ---------------------------------------------------------------------------
# 1. CRISP-DM: onde cada encontro do modulo cai no ciclo
# ---------------------------------------------------------------------------

CRISP = [
    ("Entendimento do negócio", "S1"),
    ("Entendimento dos dados", "S1 a S3"),
    ("Preparação dos dados", "S2 e S3"),
    ("Modelagem", "S6"),
    ("Avaliação", "S6 tarde"),
    ("Implantação", "S7 e S8"),
]
CRISP_HOJE = {0, 1}  # fases que a Aula 01 cobre


def gif_crisp_dm(destino: Path) -> None:
    n = len(CRISP)
    pos = _posicoes(n)

    def desenhar(k):
        fig, ax = _figura_ciclo()
        _desenha_ciclo(ax, CRISP, pos, CINZA_ESCURO)
        for i, (nome, encontro) in enumerate(CRISP):
            x, y = pos[i]
            ativo = i == k
            hoje = i in CRISP_HOJE
            ax.add_patch(
                plt.Rectangle(
                    (x - 0.52, y - 0.21), 1.04, 0.42,
                    facecolor=VERDE_ESCURO if ativo else (CINZA_CLARO if hoje else BRANCO),
                    edgecolor=VERDE_ESCURO if hoje else CINZA_MEDIO,
                    linewidth=2.4 if hoje else 1.4,
                    zorder=3,
                )
            )
            ax.text(x, y + 0.05, nome, ha="center", va="center", zorder=4,
                    fontsize=15, color=BRANCO if ativo else ROXO)
            ax.text(x, y - 0.10, encontro, ha="center", va="center", zorder=4,
                    fontsize=13, color=CINZA_CLARO if ativo else ROXO)

        ax.text(0, 0.13, "CRISP-DM", ha="center", va="center",
                fontsize=26, color=ROXO, weight="bold")
        ax.text(0, -0.03, "o ciclo que o módulo percorre inteiro", ha="center",
                va="center", fontsize=15, color=ROXO)
        ax.text(0, -0.20, "hoje: fases 1 e 2" if k in CRISP_HOJE else "",
                ha="center", va="center", fontsize=16, color=VERDE_ESCURO, weight="bold")
        return fig

    salvar_gif(desenhar, n, destino)


# ---------------------------------------------------------------------------
# 2. O ciclo de EDA assistida: o que a IA faz e o que fica com voce
# ---------------------------------------------------------------------------

CICLO = [
    ("Pergunta de negócio", "você"),
    ("Contexto: o schema", "você"),
    ("Prompt com restrição", "você"),
    ("Código", "a IA"),
    ("Execução", "a máquina"),
    ("Verificação e refutação", "você"),
]
# Duas cores, tres rotulos: roxo e o que continua com voce, verde escuro e o
# que nao e voce. A distincao entre "a IA" e "a maquina" fica no rotulo, nao na
# cor, porque cinza escuro sobre branco mede 2,03:1 de contraste (WCAG) e nao
# le numa sala projetada. Onde o texto precisa de menos peso, o caminho e
# reduzir o corpo, nunca clarear a cor.
COR_ATOR = {"você": ROXO, "a IA": VERDE_ESCURO, "a máquina": VERDE_ESCURO}


def gif_ciclo_eda(destino: Path) -> None:
    n = len(CICLO)
    pos = _posicoes(n, rx=1.16)

    def desenhar(k):
        fig, ax = _figura_ciclo()
        _desenha_ciclo(ax, CICLO, pos, CINZA_MEDIO)
        for i, (nome, ator) in enumerate(CICLO):
            x, y = pos[i]
            ativo = i == k
            cor = COR_ATOR[ator]
            ax.add_patch(
                plt.Rectangle(
                    (x - 0.52, y - 0.20), 1.04, 0.40,
                    facecolor=cor if ativo else BRANCO,
                    edgecolor=cor, linewidth=2.0, zorder=3,
                )
            )
            ax.text(x, y + 0.05, nome, ha="center", va="center", zorder=4,
                    fontsize=14.5, color=BRANCO if ativo else ROXO)
            ax.text(x, y - 0.09, ator, ha="center", va="center", zorder=4,
                    fontsize=13, style="italic", color=CINZA_CLARO if ativo else cor)

        ax.text(0, 0.13, "EDA assistida por IA", ha="center", va="center",
                fontsize=24, color=ROXO, weight="bold")
        ax.text(0, -0.03, "quatro dos seis passos continuam com você", ha="center",
                va="center", fontsize=15, color=ROXO)
        ax.text(0, -0.20, "a IA escreve, ela não decide" if CICLO[k][1] == "a IA" else "",
                ha="center", va="center", fontsize=16, color=VERDE_ESCURO, weight="bold")
        return fig

    salvar_gif(desenhar, n, destino)


# ---------------------------------------------------------------------------
# 3. Talvera e Andira: a magnitude da queda nao antecipa o desfecho
# ---------------------------------------------------------------------------


def series_indexadas():
    """Receita das duas contas nomeadas, indexada a 100 no trimestre anterior
    ao inicio do episodio de cada uma.

    Indexar e o que torna as duas comparaveis: elas operam em patamares
    diferentes e os episodios acontecem em anos diferentes. Sem indexar, a
    figura compara tamanho de conta, nao trajetoria.
    """
    from dados.gerar_painel_kovan import ANDIRA_ID, IDX, TALVERA_ID, TRIMESTRES, gerar

    painel = gerar(com_lacunas=False)

    def recorte(conta_id: str, inicio: str, quantos: int):
        i0 = IDX[inicio]
        serie = (
            painel[painel["conta_id"] == conta_id]
            .set_index("trimestre")
            .loc[TRIMESTRES, "receita_brl"]
            .tolist()
        )
        base = serie[i0 - 1]
        return [100.0 * v / base for v in serie[i0 - 1 : i0 - 1 + quantos]]

    # O episodio do Talvera comeca em 2025Q3 (quedas de 19% e 27%) e ele encerra
    # o contrato em janeiro de 2026, ja fora da janela do painel. O do Andira
    # comeca em 2024Q2 (quedas de 35% e 28%) e tem o trimestre de retomada.
    return recorte(TALVERA_ID, "2025Q3", 3), recorte(ANDIRA_ID, "2024Q2", 4)


TITULOS_CONTAS = [
    ("Duas contas do segmento estratégico, no trimestre anterior à queda", ""),
    ("As duas caem. O Andirá cai bem mais.", ""),
    ("As duas seguem caindo. O relatório de receita compara receita.", "qual das duas volta?"),
    ("O Andirá volta acima do patamar anterior. O Talvera encerra o contrato.",
     "a queda maior foi a que se reverteu"),
]


def gif_talvera_andira(destino: Path) -> None:
    talvera, andira = series_indexadas()
    passos = max(len(talvera), len(andira))

    def desenhar(k):
        fig, ax = plt.subplots(figsize=(LARGURA_FAIXA / DPI, ALTURA_FAIXA / DPI), dpi=DPI)
        fig.patch.set_facecolor(BRANCO)
        ax.set_facecolor(BRANCO)
        ax.set_xlim(-0.30, passos - 0.45)
        ax.set_ylim(35, 140)
        ax.set_xticks(range(passos))
        ax.set_xticklabels(["t-1", "t", "t+1", "t+2"][:passos], fontsize=17)
        ax.set_ylabel("receita do trimestre (t-1 = 100)", fontsize=15)
        ax.axhline(100, color=CINZA_MEDIO, linewidth=1.2, zorder=1)
        for lado in ("top", "right"):
            ax.spines[lado].set_visible(False)
        for lado in ("left", "bottom"):
            ax.spines[lado].set_color(CINZA_MEDIO)
        ax.grid(axis="y", color=CINZA_CLARO, linewidth=1)
        ax.set_axisbelow(True)

        titulo, nota = TITULOS_CONTAS[min(k, len(TITULOS_CONTAS) - 1)]
        ax.set_title(titulo, fontsize=18, color=ROXO, loc="left", pad=14)

        for serie, cor, nome in ((talvera, ROXO, "Grupo Talvera"), (andira, VERDE_ESCURO, "Grupo Andirá")):
            ate = min(k + 1, len(serie))
            xs = list(range(ate))
            ax.plot(xs, serie[:ate], color=cor, linewidth=3.2, marker="o",
                    markersize=9, zorder=4)
            # No primeiro quadro as duas partem de 100 e os rotulos ficariam um
            # por cima do outro.
            if xs and k >= 1:
                ax.text(xs[-1] + 0.06, serie[ate - 1], nome, fontsize=17,
                        color=cor, va="center")
        if k == 0:
            ax.text(0.07, 100, "as duas contas partem do mesmo patamar indexado",
                    fontsize=15, color=ROXO, va="center")
        # A serie do Talvera termina antes: ele encerra o contrato em janeiro de
        # 2026, ja fora da janela do painel. Sem esta marca a linha parece ter
        # sido cortada por engano. So no ultimo quadro: no penultimo, a pergunta
        # em aberto e justamente qual das duas volta, e esta nota entrega a
        # resposta antes da hora.
        if k == passos - 1:
            ax.annotate("encerra o contrato\nem janeiro de 2026",
                        xy=(len(talvera) - 1, talvera[-1]),
                        xytext=(len(talvera) - 1.30, talvera[-1] + 21),
                        fontsize=15, color=CORAL, ha="center",
                        arrowprops=dict(arrowstyle="-", color=CORAL, linewidth=1.4))
        if nota:
            ax.text(0.0, 41, nota, fontsize=18, color=CORAL, weight="bold")
        fig.tight_layout()
        return fig

    salvar_gif(desenhar, passos, destino)


# ---------------------------------------------------------------------------
# 4 e 5. Diagramas em SVG
# ---------------------------------------------------------------------------

FONTES_SVG = "Manrope, 'Helvetica Neue', Arial, sans-serif"

ENTRADAS = [
    ("Papel", "analista de revenue analytics", "resposta de consultor genérico"),
    ("Schema", "as 20 colunas, coladas no prompt", "coluna que não existe"),
    ("Recorte", "segmento, janela, agrupamento", "média da base inteira"),
    ("Formato", "a tabela que você espera de volta", "prosa, sem número"),
    ("Restrição", "não estimar o que não existe", "número plausível sem origem"),
]


def svg_structure_in_out(destino: Path) -> None:
    """O que entra num prompt de analise, e o modo de falha de cada ausencia.

    Sem titulo interno: o titulo do slide faz esse trabalho, e dois cabecalhos
    empilhados custavam 100 unidades de altura, que eram exatamente as que
    espremiam o diagrama. Sem barra de conclusao interna: ela virou a faixa de
    conclusao do slide, em HTML, onde o corpo e o do deck e nao o da figura.
    """
    linhas = []
    for i, (rotulo, detalhe, falha) in enumerate(ENTRADAS):
        y = 2 + i * 66
        linhas.append(f"""
  <rect x="0" y="{y}" width="470" height="58" rx="8" fill="{CINZA_CLARO}" stroke="{CINZA_MEDIO}"/>
  <text x="22" y="{y + 30}" font-size="25" font-weight="600" fill="{ROXO}">{rotulo}</text>
  <text x="22" y="{y + 57}" font-size="19" fill="{ROXO}">{detalhe}</text>
  <path d="M 486 {y + 36} L 566 {y + 36}" stroke="{CINZA_ESCURO}" stroke-width="2.5"
        marker-end="url(#seta)"/>
  <rect x="590" y="{y + 16}" width="4" height="40" fill="{CORAL}"/>
  <text x="608" y="{y + 33}" font-size="16" fill="{ROXO}" letter-spacing="0.06em">SEM ISSO</text>
  <text x="608" y="{y + 57}" font-size="22" fill="{ROXO}">{falha}</text>""")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1168 334" width="1168" height="334"
     font-family="{FONTES_SVG}" role="img"
     aria-label="Os cinco elementos de um prompt de análise e o modo de falha de cada ausência">
  <defs>
    <marker id="seta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7"
            orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{CINZA_ESCURO}"/>
    </marker>
  </defs>
  <rect width="1168" height="334" fill="{BRANCO}"/>
  {''.join(linhas)}
</svg>
"""
    destino.write_text(svg, encoding="utf-8")


RAMOS = [
    ("Menos expansão", "contas que cresciam", "cresceram menos", False),
    ("Mais contração", "contas que ficaram", "compraram menos", True),
    ("Mais perda bruta", "contas que", "encerraram contrato", False),
]
FOLHAS = [
    ("A contração se concentra", "em poucas contas", "receita_brl, segmento"),
    ("A cadência de pedidos cai", "antes da receita", "pedidos, recencia_dias"),
    ("A amplitude de mix se", "estreita durante a queda", "linhas_produto_ativas"),
    ("A atividade no CRM cai", "porque o território trocou", "interacoes_crm, troca_de_am"),
]


def svg_arvore_hipoteses(destino: Path) -> None:
    """Decomposicao MECE da pergunta de negocio ate hipoteses testaveis.

    Os ramos que a tarde nao persegue ficam rebaixados (borda cinza), e nao
    apagados: a decomposicao so e MECE se os tres aparecerem. A legenda de
    rodape saiu do SVG e virou a faixa de conclusao do slide.
    """
    partes = []
    for i, (titulo, l1, l2, foco) in enumerate(RAMOS):
        x = 20 + i * 386
        cor = VERDE_ESCURO if foco else CINZA_MEDIO
        partes.append(f"""
  <path d="M 584 110 L 584 134 L {x + 173} 134 L {x + 173} 156" fill="none"
        stroke="{CINZA_ESCURO}" stroke-width="2"/>
  <rect x="{x}" y="156" width="346" height="74" rx="8" fill="{BRANCO}"
        stroke="{cor}" stroke-width="{3.5 if foco else 1.8}"/>
  <text x="{x + 22}" y="184" font-size="21" font-weight="600" fill="{ROXO}">{titulo}</text>
  <text x="{x + 22}" y="208" font-size="16" fill="{ROXO}">{l1}</text>
  <text x="{x + 22}" y="226" font-size="16" fill="{ROXO}">{l2}</text>""")

    for i, (l1, l2, colunas) in enumerate(FOLHAS):
        x = 14 + i * 290
        partes.append(f"""
  <path d="M 579 230 L 579 256 L {x + 133} 256 L {x + 133} 278" fill="none"
        stroke="{VERDE_ESCURO}" stroke-width="2"/>
  <rect x="{x}" y="278" width="266" height="98" rx="8" fill="{CINZA_CLARO}"
        stroke="{CINZA_MEDIO}"/>
  <text x="{x + 18}" y="304" font-size="17" font-weight="600" fill="{ROXO}">{l1}</text>
  <text x="{x + 18}" y="326" font-size="17" font-weight="600" fill="{ROXO}">{l2}</text>
  <rect x="{x + 18}" y="340" width="4" height="22" fill="{VERDE_ESCURO}"/>
  <text x="{x + 32}" y="357" font-size="15" fill="{VERDE_ESCURO}">{colunas}</text>"""
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1168 350" width="1168" height="350"
     font-family="{FONTES_SVG}" role="img"
     aria-label="Árvore de hipóteses decompondo a queda do NRR em três componentes mutuamente exclusivos e quatro hipóteses testáveis">
  <rect width="1168" height="350" fill="{BRANCO}"/>
  <rect x="380" y="8" width="408" height="98" rx="8" fill="{ROXO}"/>
  <text x="406" y="42" font-size="21" font-weight="700" fill="{BRANCO}">Por que o NRR caiu de</text>
  <text x="406" y="70" font-size="21" font-weight="700" fill="{BRANCO}">109% para 93%?</text>
  <text x="406" y="93" font-size="15" fill="{CINZA_CLARO}">a pergunta do Comitê de 3 de março</text>
  {''.join(partes)}
</svg>
"""
    destino.write_text(svg, encoding="utf-8")


# ---------------------------------------------------------------------------

FIGURAS = {
    "aula01-crisp-dm.gif": gif_crisp_dm,
    "aula01-ciclo-eda-ia.gif": gif_ciclo_eda,
    "aula01-talvera-andira.gif": gif_talvera_andira,
    "aula01-structure-in-out.svg": svg_structure_in_out,
    "aula01-arvore-hipoteses.svg": svg_arvore_hipoteses,
}


def main() -> None:
    SAIDA.mkdir(parents=True, exist_ok=True)
    for nome, funcao in FIGURAS.items():
        alvo = SAIDA / nome
        funcao(alvo)
        print(f"{nome}: {alvo.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
