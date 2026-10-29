"""Desenha resultados/grafico.png a partir de resultados/medicoes.csv.

Quatro painéis (um por cenário), barras horizontais em escala log.
Métodos fixos em cinza, o `ordenar` em azul.

Uso isolado:  python -m benchmarks.grafico
"""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

from .medicao import formatar  # noqa: E402

PASTA = Path(__file__).resolve().parent.parent / "resultados"

CENARIOS = [
    ("aleatorio", "Aleatório, chaves grandes", "n = 10 000 · faixa ±10¹²"),
    ("estreita", "Faixa estreita", "n = 10 000 · valores em [−50, 50]"),
    ("quase", "Quase ordenado", "n = 10 000 · 1% de trocas vizinhas"),
    ("minuscula", "Lista minúscula", "n = 10 · tempo por lista"),
]
ORDEM = ["ordenar", "insercao", "intercalacao", "rapida", "hibrida", "contagem", "base"]
ROTULOS = {
    "ordenar": "ordenar",
    "insercao": "Inserção",
    "intercalacao": "Intercalação",
    "rapida": "Rápida",
    "hibrida": "Híbrida",
    "contagem": "Contagem",
    "base": "Base",
}

AZUL = "#2a78d6"
CINZA = "#b9b8b0"
TEXTO = "#1f1f1e"
TEXTO_2 = "#6b6a63"
FUNDO = "#ffffff"
GRADE = "#ecebe6"


def _fmt(s):
    return formatar(s, casas=None if s >= 1 else 1)


def _eixo(s, _):
    if s >= 1:
        return f"{s:g} s"
    if s >= 1e-3:
        return f"{s * 1e3:g} ms"
    return f"{s * 1e6:g} µs"


def desenhar(csv_path=PASTA / "medicoes.csv", saida=PASTA / "grafico.png"):
    dados = {}
    with open(csv_path, encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            dados[linha["cenario"], linha["metodo"]] = float(linha["segundos"]) if linha["segundos"] else None

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig, eixos = plt.subplots(2, 2, figsize=(12, 8.2), dpi=160, facecolor=FUNDO)
    fig.subplots_adjust(left=0.1, right=0.96, top=0.80, bottom=0.06, hspace=0.5, wspace=0.42)

    for ax, (chave, titulo, sub) in zip(eixos.flat, CENARIOS):
        ax.set_facecolor(FUNDO)
        valores = [dados.get((chave, m)) for m in ORDEM]
        validos = [v for v in valores if v is not None]
        lo, hi = min(validos), max(validos)
        y = list(range(len(ORDEM)))[::-1]
        melhor_fixo = min(v for m, v in zip(ORDEM, valores) if v is not None and m != "ordenar")

        for yi, m, v in zip(y, ORDEM, valores):
            if v is None:
                ax.text(lo / 1.6, yi, "recusou: faixa grande demais para os contadores",
                        va="center", ha="left", color=TEXTO_2, fontsize=8.5, style="italic")
                continue
            cor = AZUL if m == "ordenar" else CINZA
            ax.barh(yi, v - lo / 2, height=0.62, color=cor, left=lo / 2, zorder=2)
            peso = "bold" if (m == "ordenar" or v == melhor_fixo) else "normal"
            marca = "  ★ melhor fixo" if v == melhor_fixo else ""
            ax.text(v * 1.12, yi, _fmt(v) + marca, va="center", ha="left",
                    color=TEXTO, fontsize=8.5, fontweight=peso)

        ax.set_xscale("log")
        ax.set_xlim(lo / 2, hi * 12)
        ax.set_yticks(y)
        ax.set_yticklabels([ROTULOS[m] for m in ORDEM], color=TEXTO)
        for lbl, m in zip(ax.get_yticklabels(), ORDEM):
            if m == "ordenar":
                lbl.set_fontweight("bold")
                lbl.set_color(AZUL)
        ax.xaxis.set_major_formatter(FuncFormatter(_eixo))
        ax.tick_params(axis="x", colors=TEXTO_2, labelsize=8, length=0)
        ax.tick_params(axis="y", length=0)
        ax.tick_params(axis="x", which="minor", length=0)
        ax.grid(axis="x", color=GRADE, linewidth=0.8, zorder=0)
        ax.grid(axis="x", which="minor", visible=False)
        for lado in ("top", "right", "bottom", "left"):
            ax.spines[lado].set_visible(False)
        ax.set_title(titulo, loc="left", fontsize=12, fontweight="bold", color=TEXTO, pad=18)
        ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=8.5, color=TEXTO_2)

    fig.text(0.1, 0.945, "ordenar × os seis métodos fixos", fontsize=16, fontweight="bold", color=TEXTO)
    fig.text(0.1, 0.905, "Tempo mediano por lista (escala logarítmica — menor é melhor). "
             "Em azul, o ordenador adaptativo; em cinza, cada método fixo.",
             fontsize=9.5, color=TEXTO_2)
    fig.savefig(saida, facecolor=FUNDO)
    plt.close(fig)


if __name__ == "__main__":
    desenhar()
