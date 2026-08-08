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
    fig, ax = plt.subplots(figsize=(10, 4.9), dpi=115)
    fig.patch.set_facecolor(BRANCO)
    ax.set_xlim(-1.66, 1.66)
    ax.set_ylim(-1.06, 1.06)
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


def _posicoes(n, rx=1.14, ry=0.80):
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
                    (x - 0.46, y - 0.20), 0.92, 0.40,
                    facecolor=VERDE_ESCURO if ativo else (CINZA_CLARO if hoje else BRANCO),
                    edgecolor=VERDE_ESCURO if hoje else CINZA_MEDIO,
                    linewidth=2.4 if hoje else 1.4,
                    zorder=3,
                )
            )
            ax.text(x, y + 0.05, nome, ha="center", va="center", zorder=4,
                    fontsize=10.5, color=BRANCO if ativo else ROXO)
            ax.text(x, y - 0.10, encontro, ha="center", va="center", zorder=4,
                    fontsize=9.5, color=CINZA_CLARO if ativo else ROXO)

        ax.text(0, 0.13, "CRISP-DM", ha="center", va="center",
                fontsize=19, color=ROXO, weight="bold")
        ax.text(0, -0.03, "o ciclo que o módulo percorre inteiro", ha="center",
                va="center", fontsize=10.5, color=ROXO)
        ax.text(0, -0.20, "hoje: fases 1 e 2" if k in CRISP_HOJE else "",
                ha="center", va="center", fontsize=12, color=VERDE_ESCURO, weight="bold")
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
                    (x - 0.44, y - 0.19), 0.88, 0.38,
                    facecolor=cor if ativo else BRANCO,
                    edgecolor=cor, linewidth=2.0, zorder=3,
                )
            )
            ax.text(x, y + 0.05, nome, ha="center", va="center", zorder=4,
                    fontsize=10, color=BRANCO if ativo else ROXO)
            ax.text(x, y - 0.09, ator, ha="center", va="center", zorder=4,
                    fontsize=9.5, style="italic", color=CINZA_CLARO if ativo else cor)

        ax.text(0, 0.13, "EDA assistida por IA", ha="center", va="center",
                fontsize=17, color=ROXO, weight="bold")
        ax.text(0, -0.03, "quatro dos seis passos continuam com você", ha="center",
                va="center", fontsize=10.5, color=ROXO)
        ax.text(0, -0.20, "a IA escreve, ela não decide" if CICLO[k][1] == "a IA" else "",
                ha="center", va="center", fontsize=12, color=VERDE_ESCURO, weight="bold")
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
        fig, ax = plt.subplots(figsize=(10, 5.4), dpi=110)
        fig.patch.set_facecolor(BRANCO)
        ax.set_facecolor(BRANCO)
        ax.set_xlim(-0.30, passos - 0.45)
        ax.set_ylim(35, 140)
        ax.set_xticks(range(passos))
        ax.set_xticklabels(["t-1", "t", "t+1", "t+2"][:passos], fontsize=12)
        ax.set_ylabel("receita do trimestre (t-1 = 100)", fontsize=11)
        ax.axhline(100, color=CINZA_MEDIO, linewidth=1.2, zorder=1)
        for lado in ("top", "right"):
            ax.spines[lado].set_visible(False)
        for lado in ("left", "bottom"):
            ax.spines[lado].set_color(CINZA_MEDIO)
        ax.grid(axis="y", color=CINZA_CLARO, linewidth=1)
        ax.set_axisbelow(True)

        titulo, nota = TITULOS_CONTAS[min(k, len(TITULOS_CONTAS) - 1)]
        ax.set_title(titulo, fontsize=13.5, color=ROXO, loc="left", pad=16)

        for serie, cor, nome in ((talvera, ROXO, "Grupo Talvera"), (andira, VERDE_ESCURO, "Grupo Andirá")):
            ate = min(k + 1, len(serie))
            xs = list(range(ate))
            ax.plot(xs, serie[:ate], color=cor, linewidth=3.2, marker="o",
                    markersize=9, zorder=4)
            # No primeiro quadro as duas partem de 100 e os rotulos ficariam um
            # por cima do outro.
            if xs and k >= 1:
                ax.text(xs[-1] + 0.07, serie[ate - 1], nome, fontsize=12,
                        color=cor, va="center")
        if k == 0:
            ax.text(0.07, 100, "as duas contas partem do mesmo patamar indexado",
                    fontsize=11, color=ROXO, va="center")
        # A serie do Talvera termina antes: ele encerra o contrato em janeiro de
        # 2026, ja fora da janela do painel. Sem esta marca a linha parece ter
        # sido cortada por engano. So no ultimo quadro: no penultimo, a pergunta
        # em aberto e justamente qual das duas volta, e esta nota entrega a
        # resposta antes da hora.
        if k == passos - 1:
            ax.annotate("encerra o contrato\nem janeiro de 2026",
                        xy=(len(talvera) - 1, talvera[-1]),
                        xytext=(len(talvera) - 1.30, talvera[-1] + 21),
                        fontsize=11, color=CORAL, ha="center",
                        arrowprops=dict(arrowstyle="-", color=CORAL, linewidth=1.4))
        if nota:
            ax.text(0.0, 41, nota, fontsize=13, color=CORAL, weight="bold")
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
    """O que entra num prompt de analise, e o modo de falha de cada ausencia."""
    linhas = []
    for i, (rotulo, detalhe, falha) in enumerate(ENTRADAS):
        y = 122 + i * 72
        linhas.append(f"""
  <rect x="40" y="{y}" width="340" height="58" rx="8" fill="{CINZA_CLARO}" stroke="{CINZA_MEDIO}"/>
  <text x="58" y="{y + 25}" font-size="19" font-weight="600" fill="{ROXO}">{rotulo}</text>
  <text x="58" y="{y + 46}" font-size="15" fill="{ROXO}">{detalhe}</text>
  <path d="M 392 {y + 29} L 470 {y + 29}" stroke="{CINZA_ESCURO}" stroke-width="2"
        marker-end="url(#seta)"/>
  <text x="486" y="{y + 35}" font-size="16" fill="{CORAL}">sem isso: {falha}</text>""")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1060 552" width="1060" height="552"
     font-family="{FONTES_SVG}" role="img"
     aria-label="Os cinco elementos de um prompt de análise e o modo de falha de cada ausência">
  <defs>
    <marker id="seta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7"
            orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{CINZA_ESCURO}"/>
    </marker>
  </defs>
  <rect width="1060" height="552" fill="{BRANCO}"/>
  <text x="40" y="48" font-size="27" font-weight="700" fill="{ROXO}">Estrutura na entrada, estrutura na saída</text>
  <text x="40" y="80" font-size="16" fill="{ROXO}">Cada ausência tem um modo de falha próprio, e todos chegam com cara de resposta boa.</text>
  <rect x="40" y="100" width="980" height="4" fill="{VERDE_ESCURO}"/>
  {''.join(linhas)}
  <rect x="40" y="492" width="980" height="44" rx="8" fill="{VERDE_ESCURO}"/>
  <text x="58" y="520" font-size="17" fill="{BRANCO}">O que se pede de volta é o código, nunca o resultado: número citado de cabeça não tem origem para conferir.</text>
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
    """Decomposicao MECE da pergunta de negocio ate hipoteses testaveis."""
    partes = []
    for i, (titulo, l1, l2, foco) in enumerate(RAMOS):
        x = 55 + i * 325
        cor = VERDE_ESCURO if foco else CINZA_MEDIO
        partes.append(f"""
  <path d="M 530 142 L 530 172 L {x + 133} 172 L {x + 133} 200" fill="none"
        stroke="{CINZA_ESCURO}" stroke-width="2"/>
  <rect x="{x}" y="200" width="266" height="80" rx="8" fill="{BRANCO}"
        stroke="{cor}" stroke-width="{3 if foco else 1.6}"/>
  <text x="{x + 20}" y="230" font-size="19" font-weight="600" fill="{ROXO}">{titulo}</text>
  <text x="{x + 20}" y="252" font-size="14" fill="{ROXO}">{l1}</text>
  <text x="{x + 20}" y="270" font-size="14" fill="{ROXO}">{l2}</text>""")

    for i, (l1, l2, colunas) in enumerate(FOLHAS):
        x = 48 + i * 246
        partes.append(f"""
  <path d="M 513 280 L 513 320 L {x + 108} 320 L {x + 108} 348" fill="none"
        stroke="{VERDE_ESCURO}" stroke-width="2"/>
  <rect x="{x}" y="348" width="216" height="104" rx="8" fill="{CINZA_CLARO}"
        stroke="{CINZA_MEDIO}"/>
  <text x="{x + 16}" y="376" font-size="15" font-weight="600" fill="{ROXO}">{l1}</text>
  <text x="{x + 16}" y="396" font-size="15" font-weight="600" fill="{ROXO}">{l2}</text>
  <text x="{x + 16}" y="428" font-size="12.5" fill="{VERDE_ESCURO}">{colunas}</text>""")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1060 500" width="1060" height="500"
     font-family="{FONTES_SVG}" role="img"
     aria-label="Árvore de hipóteses decompondo a queda do NRR em três componentes mutuamente exclusivos e quatro hipóteses testáveis">
  <rect width="1060" height="500" fill="{BRANCO}"/>
  <rect x="320" y="26" width="420" height="116" rx="8" fill="{ROXO}"/>
  <text x="348" y="62" font-size="20" font-weight="700" fill="{BRANCO}">Por que o NRR caiu de</text>
  <text x="348" y="90" font-size="20" font-weight="700" fill="{BRANCO}">109% para 93%?</text>
  <text x="348" y="120" font-size="14" fill="{CINZA_CLARO}">a pergunta que o Comitê faz em 3 de março</text>
  {''.join(partes)}
  <text x="48" y="480" font-size="13" fill="{ROXO}">Os três ramos são mutuamente exclusivos e cobrem o indicador inteiro. As folhas são o que a tarde consegue testar, e cada uma nomeia a coluna que a testa.</text>
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
