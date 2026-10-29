"""Mede os seis métodos fixos e o `ordenar` nos quatro cenários.

Uso (na raiz do repositório):

    python -m benchmarks.medir

Gera em resultados/:
    medicoes.csv   tempos brutos (segundos por lista)
    tabelas.md     tabelas prontas para colar no RELATORIO.md
    grafico.png    gráfico dos quatro cenários
"""

import csv
import platform
import sys
from pathlib import Path

from src import METODOS, escolher, ordenar
from src.metodos.contagem import FaixaGrandeDemais

from . import cenarios
from .medicao import br, formatar, medir_intercalado

PASTA = Path(__file__).resolve().parent.parent / "resultados"
RODADAS = 9  # mediana de 9 rodadas intercaladas
RODADAS_LENTAS = 3  # para quem passa de 0,5 s por rodada

FUNCOES = {**METODOS, "ordenar": ordenar}
NOMES = {
    "insercao": "Inserção",
    "intercalacao": "Intercalação",
    "rapida": "Rápida",
    "hibrida": "Híbrida",
    "contagem": "Contagem",
    "base": "Base",
    "ordenar": "**ordenar**",
}


def medir_cenario(funcoes, entradas, com_escolher=True):
    """Confere a correção de cada função e mede todas de forma intercalada.
    Devolve {nome: segundos por lista}, com None para quem recusou."""
    aceitas, tempos = {}, {}
    for nome, f in funcoes.items():
        try:
            saida = f(entradas[0])
        except FaixaGrandeDemais:
            tempos[nome] = None
            continue
        assert saida == sorted(entradas[0]), f"{nome} ordenou errado!"
        aceitas[nome] = f
    if com_escolher:
        aceitas["escolher"] = escolher
    tempos.update(medir_intercalado(aceitas, entradas, RODADAS, RODADAS_LENTAS))
    return tempos


def main():
    PASTA.mkdir(exist_ok=True)
    todos = cenarios.todos()
    tempos = {}  # (cenario, metodo) -> segundos | None
    escolhas = {}  # cenario -> (metodo escolhido, custo do escolher)

    print(f"Python {platform.python_version()} · {platform.system()} {platform.machine()}\n")
    for chave, (rotulo, entradas) in todos.items():
        print(f"▸ {rotulo}")
        medidos = medir_cenario(FUNCOES, entradas)
        custo = medidos.pop("escolher")
        for nome in FUNCOES:
            t = medidos[nome]
            tempos[chave, nome] = t
            print(f"    {nome:<13} {formatar(t) if t is not None else 'recusou (faixa grande demais)'}")
        escolhido = escolher(entradas[0])
        escolhas[chave] = (escolhido, custo)
        print(f"    escolher → {escolhido} (custo {formatar(custo)})\n")

    # Cenário extra: onde o escolher erra
    rot = [cenarios.rotacionada()]
    print("▸ Rotacionada (cenário de erro)")
    erro = medir_cenario({n: FUNCOES[n] for n in ("ordenar", "base", "intercalacao", "hibrida")},
                         rot, com_escolher=False)
    for nome, t in erro.items():
        print(f"    {nome:<13} {formatar(t)}")
    erro_escolha = escolher(rot[0])
    print(f"    escolher → {erro_escolha}\n")

    salvar_csv(tempos, escolhas, erro)
    salvar_tabelas(todos, tempos, escolhas, erro, erro_escolha)

    from .grafico import desenhar

    desenhar(PASTA / "medicoes.csv", PASTA / "grafico.png")
    print(f"Resultados salvos em {PASTA}")


def salvar_csv(tempos, escolhas, erro):
    with open(PASTA / "medicoes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cenario", "metodo", "segundos"])
        for (cen, met), t in tempos.items():
            w.writerow([cen, met, "" if t is None else f"{t:.9f}"])
        for cen, (_, custo) in escolhas.items():
            w.writerow([cen, "escolher", f"{custo:.9f}"])
        for met, t in erro.items():
            w.writerow(["rotacionada", met, f"{t:.9f}"])


def salvar_tabelas(todos, tempos, escolhas, erro, erro_escolha):
    chaves = list(todos)
    linhas = []

    # Tabela principal: métodos nas linhas, cenários nas colunas
    cab = "| Método | " + " | ".join(todos[c][0] for c in chaves) + " |"
    linhas += [cab, "|---|" + "---:|" * len(chaves)]
    vencedor = {
        c: min((t, m) for (cc, m), t in tempos.items() if cc == c and t is not None and m != "ordenar")[1]
        for c in chaves
    }
    for nome in FUNCOES:
        celulas = []
        for c in chaves:
            t = tempos[c, nome]
            if t is None:
                celulas.append("💥 recusou")
            elif nome == vencedor[c]:
                celulas.append(f"🏆 **{formatar(t)}**")
            else:
                celulas.append(formatar(t))
        linhas.append(f"| {NOMES[nome]} | " + " | ".join(celulas) + " |")

    # Tabela relativa: tempo ÷ melhor fixo do cenário, e o pior caso de cada um
    linhas += ["", "| Método | " + " | ".join(todos[c][0] for c in chaves) + " | **Pior caso** |",
               "|---|" + "---:|" * (len(chaves) + 1)]
    for nome in FUNCOES:
        razoes = []
        for c in chaves:
            t = tempos[c, nome]
            razoes.append(float("inf") if t is None else t / tempos[c, vencedor[c]])
        celulas = ["∞ (recusa)" if r == float("inf") else f"{br(r)}×" for r in razoes]
        pior = max(razoes)
        pior_txt = "∞" if pior == float("inf") else f"{br(pior)}×"
        linhas.append(f"| {NOMES[nome]} | " + " | ".join(celulas) + f" | **{pior_txt}** |")

    # Tabela do escolher
    linhas += ["", "| Cenário | `escolher` decidiu | Melhor fixo | `ordenar` ÷ melhor fixo | Custo do `escolher` | % do tempo do `ordenar` |",
               "|---|---|---|---:|---:|---:|"]
    for c in chaves:
        esc, custo = escolhas[c]
        melhor = vencedor[c]
        razao = tempos[c, "ordenar"] / tempos[c, melhor]
        pct = 100 * custo / tempos[c, "ordenar"]
        # acerto = o método escolhido fica a até 5% do melhor fixo (empate técnico conta)
        acerto = "✅" if tempos[c, esc] <= 1.05 * tempos[c, melhor] else "⚠️"
        linhas.append(
            f"| {todos[c][0]} | {acerto} `{esc}` | `{melhor}` | {br(razao)}× | {formatar(custo)} | {br(pct, 1)}% |"
        )

    # Tabela do erro
    linhas += ["", "| Método | Rotacionada (n = 10 000) |", "|---|---:|"]
    for nome, t in erro.items():
        rot = f"`ordenar` (→ `{erro_escolha}`)" if nome == "ordenar" else NOMES[nome]
        linhas.append(f"| {rot} | {formatar(t)} |")

    (PASTA / "tabelas.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
