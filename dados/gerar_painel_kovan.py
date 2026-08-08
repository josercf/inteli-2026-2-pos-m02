# -*- coding: utf-8 -*-
"""
Gerador do painel analitico de contas da Kovan Technologies LATAM (Exhibit 3).

Produz dados/kovan_painel_contas.csv: 1.187 contas x 14 trimestres (2022Q3 a
2025Q4) = 16.618 registros, com as 20 colunas do dicionario de variaveis.

Os numeros canonicos do case (Case_Modulo2_Lenovo_Kovan_v2 e o Caderno de
Exhibits) nao sao aproximados por sorteio: a estrutura de episodios e escrita
conta a conta, de forma explicita, e os valores monetarios sao calibrados sobre
ela. dados/tests/test_painel_kovan.py trava cada um desses numeros.

Alvos travados no segmento estrategico (118 contas, 1.652 observacoes):

- 34 rupturas dentro da janela (prevalencia de 2,1% em nivel conta-trimestre)
- 192 episodios de erosao ao corte de 10%, 176 ao de 15%, 76 ao de 25%
- que capturam, respectivamente, 31, 29 e 17 das 34 rupturas
- dos 176 episodios do corte de 15%: 56 recuperam (31,8%), 91 seguem
  contraindo sem romper (51,7%) e 29 terminam em ruptura (16,5%)
- NRR do cohort: 109,0% em 2024 e 93,0% em 2025 (Exhibit 2)

O insight plantado, que o texto do case nao revela e que a EDA precisa
descobrir: a magnitude da queda nao separa o episodio reversivel do
irreversivel; a ORDEM em que os sinais se deterioram separa. No episodio
irreversivel a amplitude de mix estreita antes de a receita cair, e a cadencia
de pedidos se deteriora junto. No reversivel a receita cai primeiro e o mix
nao estreita (e o caso do Grupo Andira, o contraexemplo do case).

As quatro advertencias de qualidade do Exhibit 3 sao injetadas por ultimo, de
proposito: quem nao tratar a receita ausente encontra uma contagem de rupturas
diferente de 34, que e exatamente o conteudo da segunda aula.

Uso: python3 dados/gerar_painel_kovan.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260808
RAIZ = Path(__file__).resolve().parent
SAIDA = RAIZ / "kovan_painel_contas.csv"

# ---------------------------------------------------------------------------
# Grade do painel
# ---------------------------------------------------------------------------

TRIMESTRES = [
    f"{ano}Q{q}"
    for ano in range(2022, 2026)
    for q in range(1, 5)
    if not (ano == 2022 and q < 3)
]
assert len(TRIMESTRES) == 14
IDX = {t: i for i, t in enumerate(TRIMESTRES)}
ANO_DO_TRIMESTRE = [int(t[:4]) for t in TRIMESTRES]
N_T = len(TRIMESTRES)

I_TAXONOMIA_NOVA = IDX["2023Q1"]  # advertencia 3 do Exhibit 3
I_ATIVIDADE_OBRIGATORIA = IDX["2023Q2"]  # 11 trimestres uteis de atividade

N_CONTAS = 1187
SEGMENTOS = {"Estrategico": 118, "Medio": 356, "Cauda": 713}
assert sum(SEGMENTOS.values()) == N_CONTAS

REGIOES = ["Brasil", "Mexico & Norte LATAM", "Cono Sur", "Andina & Caribe"]
PESO_REGIAO = [0.42, 0.24, 0.20, 0.14]
N_TERRITORIOS = 46

# Alvos do Exhibit 2, em R$ milhoes
NRR_BASE_2023 = 1296.8
NRR_TOTAL_2024 = 1412.9
NRR_TOTAL_2025 = 1313.8
RUPTURAS_2024 = 14
RUPTURAS_2025 = 11

# ---------------------------------------------------------------------------
# Plano de episodios do segmento estrategico
# ---------------------------------------------------------------------------
#
# A classe de magnitude e definida pelas duas quedas trimestre a trimestre:
#   "10_15"   -> as duas ficam em [10%, 15%)
#   "15_25"   -> as duas passam de 15%, mas nao as duas passam de 25%
#   "25_mais" -> as duas passam de 25%
#
# A contagem por corte cai direto dessas classes:
#   corte 10% -> 16 + 100 + 76 = 192
#   corte 15% ->      100 + 76 = 176
#   corte 25% ->            76 =  76

RUPTURAS_TOTAIS = 34
RUPTURA_COM_EPISODIO = {"25_mais": 17, "15_25": 12, "10_15": 2}
RUPTURA_SEM_EPISODIO = 3
assert sum(RUPTURA_COM_EPISODIO.values()) + RUPTURA_SEM_EPISODIO == RUPTURAS_TOTAIS

# Episodios em contas que sobrevivem a janela. A classe de magnitude e
# distribuida entre recuperados e persistentes na mesma proporcao, de proposito:
# a magnitude nao pode separar os dois grupos, so a ordem dos sinais separa.
# O Grupo Talvera entra aqui como um persistente da classe 15_25 (ele encerra o
# contrato em janeiro de 2026, fora da janela do painel, e por isso nao e uma
# das 34 rupturas).
DESFECHO_SOBREVIVENTE = {
    ("recupera", "25_mais"): 22,
    ("recupera", "15_25"): 34,
    ("persiste", "25_mais"): 37,
    ("persiste", "15_25"): 54,
    ("recupera", "10_15"): 5,
    ("persiste", "10_15"): 9,
}

# Com que frequencia o mix estreita antes de a receita cair, por desfecho.
# A assinatura nao pode ser perfeita: 100% contra 0% le como dado fabricado e
# entrega o achado antes de a turma procurar por ele. O que o case sustenta e
# uma suspeita forte e nao testada de Otavio Rangel, nao uma regra deterministica.
P_MIX_LIDERA = {"irreversivel": 0.86, "reversivel": 0.13}

FAIXA_QUEDA = {
    "10_15": (0.102, 0.146),
    "15_25": (0.154, 0.244),
    "25_mais": (0.256, 0.42),
}

# ---------------------------------------------------------------------------
# Contas nomeadas pelo case, com trajetoria fixada pelos exhibits
# ---------------------------------------------------------------------------

TALVERA_ID = "ACC-00720"
TALVERA_AM = "AM-41"
TALVERA = {
    "2024Q3": dict(receita=9_239_623.49, pedidos=14, linhas=6, recencia=9),
    "2024Q4": dict(receita=9_245_926.85, pedidos=14, linhas=6, recencia=25),
    "2025Q1": dict(receita=9_006_362.75, pedidos=25, linhas=5, recencia=20),
    "2025Q2": dict(receita=7_925_599.22, pedidos=15, linhas=4, recencia=23),
    "2025Q3": dict(receita=6_419_735.37, pedidos=12, linhas=3, recencia=25),
    "2025Q4": dict(receita=4_686_406.82, pedidos=7, linhas=2, recencia=19),
}

ANDIRA_ID = "ACC-00311"
ANDIRA_PATAMAR = 13_850_000.0
ANDIRA_RETOMADA = 17_020_000.0

NOMEADAS = (TALVERA_ID, ANDIRA_ID)


@dataclass
class Episodio:
    inicio: int
    classe: str
    desfecho: str  # "recupera" | "persiste" | "rompe"
    quedas: tuple[float, float] = (0.0, 0.0)
    lidera_mix: bool = False


@dataclass
class Conta:
    conta_id: str
    segmento: str
    regiao: str
    territorio: str
    patamar: float
    ciclo: int
    fase: int
    semente: int
    tendencia: float = 1.0
    episodios: list[Episodio] = field(default_factory=list)
    rompe_em: int | None = None
    tem_engajamento: bool = True


# ---------------------------------------------------------------------------
# Plano
# ---------------------------------------------------------------------------


def _sorteia_quedas(rng: np.random.Generator, classe: str) -> tuple[float, float]:
    lo, hi = FAIXA_QUEDA[classe]
    if classe == "15_25" and rng.random() < 0.35:
        # Uma das duas pode passar de 25%: o corte de 25% exige as duas.
        forte = float(rng.uniform(0.256, 0.34))
        fraca = float(rng.uniform(0.154, 0.244))
        return (forte, fraca) if rng.random() < 0.5 else (fraca, forte)
    return (float(rng.uniform(lo, hi)), float(rng.uniform(lo, hi)))


# Gerador dedicado a assinatura de mix. Sortear isso no mesmo gerador que
# monta o plano deslocaria todo o fluxo aleatorio seguinte e mudaria as
# contagens canonicas de episodio e de desfecho.
_RNG_MIX = np.random.default_rng(SEED + 31)


def _lidera_mix(rng: np.random.Generator, desfecho: str) -> bool:
    """O mix estreita antes de a receita cair neste episodio?"""
    chave = "reversivel" if desfecho == "recupera" else "irreversivel"
    return bool(_RNG_MIX.random() < P_MIX_LIDERA[chave])


def _janelas_livres(ocupado: list[bool], duracao: int) -> list[int]:
    return [
        i
        for i in range(1, N_T - duracao + 1)
        if not any(ocupado[i : i + duracao])
    ]


def _monta_contas(rng: np.random.Generator) -> list[Conta]:
    ids = [f"ACC-{i:05d}" for i in range(1, N_CONTAS + 1)]
    for fixo in NOMEADAS:
        ids.remove(fixo)
    rng.shuffle(ids)
    ids = [TALVERA_ID, ANDIRA_ID] + ids

    contas: list[Conta] = []
    i = 0
    for segmento, quantidade in SEGMENTOS.items():
        for _ in range(quantidade):
            conta_id = ids[i]
            regiao = str(rng.choice(REGIOES, p=PESO_REGIAO))
            territorio = f"AM-{int(rng.integers(1, N_TERRITORIOS + 1)):02d}"
            if conta_id == TALVERA_ID:
                regiao, territorio = "Brasil", TALVERA_AM
            if segmento == "Estrategico":
                patamar = float(rng.lognormal(math.log(2_200_000), 0.62))
            elif segmento == "Medio":
                patamar = float(rng.lognormal(math.log(260_000), 0.50))
            else:
                patamar = float(rng.lognormal(math.log(52_000), 0.55))
            contas.append(
                Conta(
                    conta_id=conta_id,
                    segmento=segmento,
                    regiao=regiao,
                    territorio=territorio,
                    patamar=patamar,
                    ciclo=int(rng.integers(12, 17)),
                    fase=int(rng.integers(0, 16)),
                    semente=SEED + 1000 + i,
                    # Tendencia propria da conta, constante ao longo da janela.
                    # E o que produz a expansao que o Exhibit 2 decompoe: sem
                    # contas crescendo, o NRR de 109% em 2024 nao existe.
                    # Constante por conta de proposito: uma tendencia com ruido
                    # trimestral criaria episodios de erosao por acaso.
                    tendencia=float(np.clip(rng.normal(1.021, 0.028), 0.970, 1.075)),
                    tem_engajamento=bool(
                        rng.random() < (0.90 if segmento == "Estrategico" else 0.62)
                    ),
                )
            )
            i += 1
    return contas


def _planeja_estrategicas(rng: np.random.Generator, contas: list[Conta]) -> None:
    estrategicas = [c for c in contas if c.segmento == "Estrategico"]
    talvera = next(c for c in estrategicas if c.conta_id == TALVERA_ID)
    andira = next(c for c in estrategicas if c.conta_id == ANDIRA_ID)

    # Trajetorias fixadas pelos exhibits. O Talvera segue contraindo ate o fim
    # da janela (persistente 15_25); o Andira recupera sem estreitar o mix.
    talvera.episodios = [
        Episodio(IDX["2025Q3"], "15_25", "persiste", (0.19, 0.27), lidera_mix=True)
    ]
    andira.episodios = [
        Episodio(IDX["2024Q2"], "25_mais", "recupera", (0.35, 0.28), lidera_mix=False)
    ]

    disponiveis = [c for c in estrategicas if c.conta_id not in NOMEADAS]
    rng.shuffle(disponiveis)

    # --- as 34 rupturas ----------------------------------------------------
    plano: list[str] = []
    for classe, quantidade in RUPTURA_COM_EPISODIO.items():
        plano += [classe] * quantidade
    plano += ["sem_episodio"] * RUPTURA_SEM_EPISODIO
    anos = [2024] * RUPTURAS_2024 + [2025] * RUPTURAS_2025 + [2023] * 7 + [2022] * 2
    assert len(plano) == len(anos) == RUPTURAS_TOTAIS
    rng.shuffle(plano)
    rng.shuffle(anos)

    rompem: list[Conta] = []
    for classe, ano in zip(plano, anos):
        conta = disponiveis.pop()
        rompem.append(conta)
        candidatos = [
            i
            for i, a in enumerate(ANO_DO_TRIMESTRE)
            if a == ano and 4 <= i <= N_T - 2
        ]
        if not candidatos:
            candidatos = [max(4, N_T - 2)]
        zera = int(rng.choice(candidatos))
        conta.rompe_em = zera
        if classe != "sem_episodio":
            conta.episodios = [
                Episodio(
                    inicio=max(1, zera - 3),
                    classe=classe,
                    desfecho="rompe",
                    quedas=_sorteia_quedas(rng, classe),
                    lidera_mix=_lidera_mix(rng, "rompe"),
                )
            ]

    # --- episodios das contas que sobrevivem -------------------------------
    sobreviventes = disponiveis + [talvera, andira]
    assert len(sobreviventes) == 118 - RUPTURAS_TOTAIS

    pendentes: list[tuple[str, str]] = []
    for (desfecho, classe), quantidade in DESFECHO_SOBREVIVENTE.items():
        n = quantidade
        if (desfecho, classe) == ("recupera", "25_mais"):
            n -= 1  # o Andira
        if (desfecho, classe) == ("persiste", "15_25"):
            n -= 1  # o Talvera
        pendentes += [(desfecho, classe)] * n
    rng.shuffle(pendentes)

    # Alocacao deliberada, nao por tentativa: um episodio ocupa cinco
    # trimestres (duas quedas mais a resolucao do desfecho), e a janela de 14
    # so comporta dois por conta se o primeiro ficar na metade inicial e o
    # segundo na final. Sortear a posicao livremente deixa episodios sem lugar.
    livres = [c for c in sobreviventes if c.conta_id not in NOMEADAS]
    rng.shuffle(livres)
    capacidade = 2 * len(livres)
    if len(pendentes) > capacidade:
        raise RuntimeError(f"{len(pendentes)} episodios para {capacidade} vagas")
    com_dois = len(pendentes) - len(livres)  # quantas contas recebem dois

    INICIO_CEDO = [1, 2, 3, 4]
    for posicao, conta in enumerate(livres):
        quantos = 2 if posicao < com_dois else 1
        if quantos == 2:
            i1 = int(rng.choice(INICIO_CEDO))
            i2 = int(rng.integers(i1 + 5, N_T - 4))
            inicios = [i1, i2]
        else:
            inicios = [int(rng.integers(1, N_T - 4))]
        for inicio in inicios:
            if not pendentes:
                break
            desfecho, classe = pendentes.pop(0)
            conta.episodios.append(
                Episodio(
                    inicio=inicio,
                    classe=classe,
                    desfecho=desfecho,
                    quedas=_sorteia_quedas(rng, classe),
                    # O insight: o episodio que nao se reverte quase sempre
                    # comeca pelo estreitamento de mix, e o que se reverte quase
                    # nunca. "Quase" e o que faz o achado precisar de evidencia.
                    lidera_mix=_lidera_mix(rng, desfecho),
                )
            )
    if pendentes:
        raise RuntimeError(f"sobraram {len(pendentes)} episodios sem janela livre")


def _planeja_demais(rng: np.random.Generator, contas: list[Conta]) -> None:
    """Medio e Cauda: sustentam a media de 82 episodios por trimestre na base."""
    intensidade = np.linspace(0.55, 1.60, N_T)
    for conta in (c for c in contas if c.segmento != "Estrategico"):
        ocupado = [False] * N_T
        for inicio in range(1, N_T - 2):
            if ocupado[inicio]:
                continue
            if rng.random() >= 0.086 * intensidade[inicio]:
                continue
            classe = str(rng.choice(["10_15", "15_25", "25_mais"], p=[0.22, 0.50, 0.28]))
            desfecho = str(rng.choice(["recupera", "persiste"], p=[0.33, 0.67]))
            conta.episodios.append(
                Episodio(
                    inicio=inicio,
                    classe=classe,
                    desfecho=desfecho,
                    quedas=_sorteia_quedas(rng, classe),
                    lidera_mix=_lidera_mix(rng, desfecho),
                )
            )
            for k in range(inicio, min(inicio + 5, N_T)):
                ocupado[k] = True
        if rng.random() < 0.055:
            conta.rompe_em = int(rng.integers(4, N_T - 1))


# ---------------------------------------------------------------------------
# Series
# ---------------------------------------------------------------------------

# Ruido e ciclo baixos de proposito no estrategico: com amplitude maior, duas
# quedas consecutivas acontecem por acaso e as contagens exatas por corte
# deixam de fechar.
AMPLITUDE_CICLO = 0.07
SIGMA_RUIDO = 0.018


# Quantos trimestres a contracao segue depois do episodio, no desfecho
# persistente. O case exige que a contracao dure pelo menos quatro trimestres
# ("uma tendencia com inercia mensuravel"), nao que a conta entre em espiral:
# um declinio sem fim consumiria a receita do segmento e derrubaria o NRR muito
# abaixo dos 93% do Exhibit 2.
CAUDA_PERSISTENTE = 4


def _serie(conta: Conta, crescimento: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(receita, linhas de mix, indice de cadencia). Deterministica por conta."""
    rng = np.random.default_rng(conta.semente)
    receita = np.zeros(N_T)
    mix_max = {"Estrategico": 6, "Medio": 5, "Cauda": 3}[conta.segmento]
    mix = np.full(N_T, float(mix_max))
    cadencia = np.ones(N_T)

    # Deriva combinada: tendencia propria da conta mais o crescimento comum do
    # segmento, que a calibracao ajusta para o NRR bater com o Exhibit 2.
    deriva = np.array([conta.tendencia ** i * crescimento[i] for i in range(N_T)])

    def passo(k: int) -> float:
        """Fator de deriva de um trimestre para o seguinte."""
        return float(deriva[k] / deriva[k - 1]) if k > 0 else 1.0

    for i in range(N_T):
        ciclo = 1.0 + AMPLITUDE_CICLO * math.sin(
            2 * math.pi * ((i + conta.fase) % conta.ciclo) / conta.ciclo
        )
        receita[i] = conta.patamar * ciclo * float(rng.normal(1.0, SIGMA_RUIDO)) * deriva[i]

    for ep in sorted(conta.episodios, key=lambda e: e.inicio):
        i0 = ep.inicio
        if i0 + 1 >= N_T:
            continue
        base = receita[i0 - 1] if i0 > 0 else receita[0]
        q1, q2 = ep.quedas
        # As duas quedas sao gravadas direto sobre a serie, sem deriva: e o que
        # torna a contagem por corte de limiar exata.
        receita[i0] = base * (1 - q1)
        receita[i0 + 1] = receita[i0] * (1 - q2)

        # --- amplitude de mix ---------------------------------------------
        # Niveis absolutos, nunca decrementos acumulados: com dois episodios na
        # mesma conta, decremento sobre a cauda leva o mix de toda a base a 1.
        nivel = mix[i0 - 2] if i0 >= 2 else float(mix_max)
        if ep.lidera_mix:
            # Assinatura do irreversivel: o mix estreita um trimestre ANTES de
            # a receita cair, e a cadencia se deteriora junto com a receita.
            if i0 - 1 >= 0:
                mix[i0 - 1] = max(1.0, nivel - 1)
            mix[i0] = max(1.0, nivel - 2)
            fim = min(i0 + 2 + CAUDA_PERSISTENTE, N_T)
            mix[i0 + 1 : fim] = max(1.0, nivel - 3)
            mix[fim:] = max(1.0, nivel - 2)
            cadencia[i0:] *= 0.72
            cadencia[i0 + 1 :] *= 0.82
        else:
            # Reversivel: a receita cai e o mix segue intacto.
            cadencia[i0 : i0 + 2] *= 0.94

        # --- desfecho ------------------------------------------------------
        if ep.desfecho == "recupera":
            alvo = base * float(rng.uniform(1.02, 1.16))
            for k in range(i0 + 2, N_T):
                receita[k] = (
                    alvo * passo(k)
                    if k == i0 + 2
                    else receita[k - 1] * float(rng.normal(1.0, 0.018)) * passo(k)
                )
            cadencia[i0 + 2 :] = 1.0
        elif ep.desfecho == "persiste":
            fim = min(i0 + 2 + CAUDA_PERSISTENTE, N_T)
            for k in range(i0 + 2, fim):
                receita[k] = receita[k - 1] * (1 - float(rng.uniform(0.02, 0.05))) * passo(k)
            for k in range(fim, N_T):
                receita[k] = receita[k - 1] * float(rng.normal(1.0, 0.018)) * passo(k)
        else:  # rompe: a queda continua, sempre abaixo de 25% ao trimestre,
            # para nao criar um segundo episodio no corte de 25%.
            for k in range(i0 + 2, N_T):
                receita[k] = receita[k - 1] * (1 - float(rng.uniform(0.12, 0.22))) * passo(k)
                mix[k] = max(1.0, mix[k - 1] - 1)

    if conta.rompe_em is not None:
        receita[conta.rompe_em :] = 0.0
        mix[conta.rompe_em :] = 0.0
        cadencia[conta.rompe_em :] = 0.0

    return np.maximum(receita, 0.0), mix, cadencia


def _fixa_nomeadas(conta: Conta, receita, mix, cadencia):
    """Sobrescreve o que os exhibits fixam valor a valor."""
    if conta.conta_id == TALVERA_ID:
        rng = np.random.default_rng(SEED + 77)
        for i in range(IDX["2024Q3"]):
            receita[i] = TALVERA["2024Q3"]["receita"] * float(rng.normal(1.0, 0.03))
            mix[i] = 6
        for trimestre, v in TALVERA.items():
            i = IDX[trimestre]
            receita[i] = v["receita"]
            mix[i] = v["linhas"]
        cadencia[IDX["2025Q2"] :] *= 0.75
    elif conta.conta_id == ANDIRA_ID:
        i2 = IDX["2024Q2"]
        for i in range(i2):
            receita[i] = ANDIRA_PATAMAR * (1 + 0.015 * ((i % 3) - 1))
        receita[i2] = ANDIRA_PATAMAR * 0.65
        receita[i2 + 1] = receita[i2] * 0.72
        receita[IDX["2024Q4"]] = ANDIRA_RETOMADA
        for i in range(IDX["2025Q1"], N_T):
            receita[i] = receita[i - 1] * 1.008
        mix[:] = 6  # o contraexemplo: nunca estreitou o mix
    return receita, mix, cadencia


def _vetor_crescimento(r24: float, r25: float) -> np.ndarray:
    """Crescimento comum do segmento, composto trimestre a trimestre.

    Composto, e nao um degrau por ano, de proposito: um degrau faria a receita
    de toda a carteira saltar no primeiro trimestre do ano, o que apareceria
    na EDA como um artefato sem nenhuma leitura de negocio.
    """
    taxas = np.zeros(N_T)
    for i, ano in enumerate(ANO_DO_TRIMESTRE):
        if ano == 2024:
            taxas[i] = r24
        elif ano == 2025:
            taxas[i] = r25
    return np.cumprod(1.0 + taxas)


def _somas_anuais(contas: list[Conta], crescimento: np.ndarray) -> dict:
    """Soma da receita do segmento estrategico por ano, separando as nomeadas."""
    out = {"nomeadas": {2023: 0.0, 2024: 0.0, 2025: 0.0},
           "outras": {2023: 0.0, 2024: 0.0, 2025: 0.0}}
    for conta in contas:
        if conta.segmento != "Estrategico":
            continue
        receita, mix, cad = _serie(conta, crescimento)
        receita, mix, cad = _fixa_nomeadas(conta, receita, mix, cad)
        chave = "nomeadas" if conta.conta_id in NOMEADAS else "outras"
        for i, ano in enumerate(ANO_DO_TRIMESTRE):
            if ano in out[chave]:
                out[chave][ano] += receita[i]
    return out


def _totais(contas, r24: float, r25: float) -> tuple[float, float, float]:
    """Receita anual do segmento estrategico, ja com a escala aplicada."""
    s = _somas_anuais(contas, _vetor_crescimento(r24, r25))
    # As duas contas nomeadas tem valores fixados pelos exhibits e nao podem
    # ser escaladas: a escala recai sobre as outras 116.
    escala = (NRR_BASE_2023 * 1e6 - s["nomeadas"][2023]) / s["outras"][2023]
    t = {
        ano: (s["nomeadas"][ano] + escala * s["outras"][ano]) / 1e6
        for ano in (2023, 2024, 2025)
    }
    return t[2024], t[2025], escala


def _bisseccao(f, alvo: float, lo: float, hi: float, passos: int = 34) -> float:
    """Busca a taxa que leva f ao alvo. f precisa ser monotona crescente."""
    for _ in range(passos):
        meio = (lo + hi) / 2
        if f(meio) < alvo:
            lo = meio
        else:
            hi = meio
    return (lo + hi) / 2


def _calibra(contas: list[Conta]) -> tuple[np.ndarray, float]:
    """Acha (crescimento, escala) que fazem o NRR bater com o Exhibit 2.

    Duas buscas encadeadas, nao um ponto fixo multiplicativo: o total de 2024
    depende so da taxa de 2024, e o de 2025 depende das duas. Com a taxa de
    2024 ja fixada, a de 2025 fica com um alvo unidimensional e monotono.
    """
    r24 = _bisseccao(lambda r: _totais(contas, r, 0.0)[0], NRR_TOTAL_2024, -0.20, 0.30)
    r25 = _bisseccao(lambda r: _totais(contas, r24, r)[1], NRR_TOTAL_2025, -0.30, 0.25)
    _, _, escala = _totais(contas, r24, r25)
    return _vetor_crescimento(r24, r25), escala


# ---------------------------------------------------------------------------
# Painel
# ---------------------------------------------------------------------------


def gerar(com_lacunas: bool = True) -> pd.DataFrame:
    """Monta o painel.

    `com_lacunas=False` devolve a estrutura canonica, antes de injetar a
    receita ausente. E o que os testes usam para conferir as contagens do case:
    reconstruir a lacuna por interpolacao mudaria as quedas dentro do episodio
    e a contagem por corte de limiar deixaria de fechar. O painel entregue ao
    aluno e sempre o `com_lacunas=True`.
    """
    global _RNG_MIX
    _RNG_MIX = np.random.default_rng(SEED + 31)
    rng = np.random.default_rng(SEED)
    contas = _monta_contas(rng)
    _planeja_estrategicas(rng, contas)
    _planeja_demais(rng, contas)
    crescimento, escala = _calibra(contas)

    # Troca de Account Manager: 11 dos 46 territorios trocam em 2025 (23,9%).
    rng_troca = np.random.default_rng(SEED + 7)
    territorios = sorted({c.territorio for c in contas})
    trocas: set[tuple[str, int]] = set()
    i_2025 = [i for i, a in enumerate(ANO_DO_TRIMESTRE) if a == 2025]
    i_antes = [i for i, a in enumerate(ANO_DO_TRIMESTRE) if a < 2025]
    for t in rng_troca.choice(territorios, size=11, replace=False):
        trocas.add((str(t), int(rng_troca.choice(i_2025))))
    for t in rng_troca.choice(territorios, size=9, replace=False):
        trocas.add((str(t), int(rng_troca.choice(i_antes))))

    linhas = []
    for conta in contas:
        receita, mix, cadencia = _serie(conta, crescimento)
        receita, mix, cadencia = _fixa_nomeadas(conta, receita, mix, cadencia)
        if conta.conta_id not in NOMEADAS:
            receita = receita * escala

        rng_col = np.random.default_rng(conta.semente + 500_000)
        base_pedidos = {"Estrategico": 14, "Medio": 7, "Cauda": 4}[conta.segmento]

        for i, trimestre in enumerate(TRIMESTRES):
            rompida = conta.rompe_em is not None and i >= conta.rompe_em
            r = 0.0 if rompida else float(receita[i])
            pedidos = (
                0
                if rompida
                else max(1, int(round(base_pedidos * float(cadencia[i]) * float(rng_col.normal(1.0, 0.16)))))
            )
            linhas_mix = 0 if rompida else int(mix[i])
            # Advertencia 3: ate 2022Q4 as tres linhas de infraestrutura eram
            # registradas como uma so.
            if i < I_TAXONOMIA_NOVA and linhas_mix > 0:
                linhas_mix = max(1, linhas_mix - 2)

            recencia = 92 if rompida else int(
                np.clip(rng_col.normal(22, 8) / max(float(cadencia[i]), 0.3), 1, 92)
            )
            if conta.conta_id == TALVERA_ID and trimestre in TALVERA:
                pedidos = TALVERA[trimestre]["pedidos"]
                recencia = TALVERA[trimestre]["recencia"]

            valor_medio = (r / pedidos) if pedidos else 0.0
            tem_atividade = conta.tem_engajamento and i >= I_ATIVIDADE_OBRIGATORIA
            troca = 1 if (conta.territorio, i) in trocas else 0
            visitas = interacoes = None
            if tem_atividade:
                visitas = max(0, int(rng_col.normal(6 * float(cadencia[i]), 2)))
                interacoes = max(0, int(rng_col.normal(18 * float(cadencia[i]), 5)))
                if troca:
                    # A atividade cai por troca de responsavel, nao por
                    # deterioracao da conta: o confundidor que o case aponta.
                    visitas = int(visitas * 0.35)
                    interacoes = int(interacoes * 0.40)

            oportunidades = max(0, int(rng_col.normal(3 * float(cadencia[i]), 1.4)))
            perdidas = int(rng_col.binomial(oportunidades, 0.34)) if oportunidades else 0

            linhas.append(
                {
                    "conta_id": conta.conta_id,
                    "trimestre": trimestre,
                    "segmento": conta.segmento,
                    "regiao": conta.regiao,
                    "am_id": conta.territorio,
                    "receita_brl": round(r, 2),
                    "pedidos": pedidos,
                    "linhas_produto_ativas": linhas_mix,
                    "valor_medio_pedido_brl": round(valor_medio, 2),
                    "recencia_dias": recencia,
                    # Advertencia 2: coluna independente da receita, em valor
                    # negativo, que precisa de tratamento explicito.
                    "devolucoes_brl": -round(abs(float(rng_col.normal(0.012, 0.009))) * r, 2),
                    "desconto_medio_pct": round(float(np.clip(rng_col.normal(7.5, 3.1), 0, 28)), 2),
                    "oportunidades_abertas": oportunidades,
                    "oportunidades_perdidas": perdidas,
                    "valor_pipeline_brl": round(max(0.0, float(rng_col.normal(0.45, 0.18))) * r, 2),
                    "visitas_registradas": visitas,
                    "interacoes_crm": interacoes,
                    "troca_de_am_no_trimestre": troca,
                    "status_conta": "Encerrada" if rompida else "Ativa",
                    "taxonomia_mix": "pre_2023" if i < I_TAXONOMIA_NOVA else "pos_2023",
                }
            )

    painel = pd.DataFrame(linhas)

    # Advertencia 1: cerca de 1% dos trimestres com conta ativa nao tem receita
    # registrada, por atraso no fechamento contabil. Injetada por ultimo, de
    # proposito: a estrutura canonica ja esta pronta, e quem nao tratar a
    # lacuna encontra uma contagem de rupturas diferente de 34.
    if com_lacunas:
        rng_falha = np.random.default_rng(SEED + 11)
        ativos = painel.index[painel["status_conta"] == "Ativa"].to_numpy()
        faltantes = rng_falha.choice(
            ativos, size=int(round(0.010 * len(ativos))), replace=False
        )
        painel.loc[faltantes, "receita_brl"] = np.nan
        painel.loc[faltantes, "valor_medio_pedido_brl"] = np.nan

    return painel


def main() -> None:
    painel = gerar()
    painel.to_csv(SAIDA, index=False, encoding="utf-8")
    print(f"{SAIDA.name}: {len(painel)} linhas x {painel.shape[1]} colunas")


if __name__ == "__main__":
    main()
