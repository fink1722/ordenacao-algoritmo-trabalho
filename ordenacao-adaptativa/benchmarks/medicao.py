"""Cronômetro comum: mediana de várias rodadas intercaladas, por entrada."""

import random
import time


def medir_intercalado(funcoes, entradas, rodadas, rodadas_lentas, limite_lento=0.5):
    """Mede várias funções nas mesmas entradas, de forma INTERCALADA.

    Em cada rodada, todas as funções rodam uma vez, em ordem embaralhada.
    Assim, variações da máquina (turbo, cache, outro processo) atingem
    todas igualmente, em vez de favorecer quem foi medido por último.
    Funções lentas (> `limite_lento` s por rodada) participam só das
    primeiras `rodadas_lentas` rodadas. Devolve {nome: mediana em s}.
    """
    amostras = {nome: [] for nome in funcoes}
    ordem = list(funcoes)
    sorteio = random.Random(0)
    lentas = set()
    for r in range(rodadas):
        sorteio.shuffle(ordem)
        for nome in ordem:
            if nome in lentas and r >= rodadas_lentas:
                continue
            f = funcoes[nome]
            ini = time.perf_counter()
            for v in entradas:
                f(v)
            total = time.perf_counter() - ini
            amostras[nome].append(total / len(entradas))
            if total > limite_lento:
                lentas.add(nome)
    return {nome: sorted(a)[len(a) // 2] for nome, a in amostras.items()}


def br(numero, casas=2):
    """Número no formato brasileiro: 2655.57 -> '2.655,57'."""
    txt = f"{numero:,.{casas}f}"
    return txt.replace(",", "_").replace(".", ",").replace("_", ".")


def formatar(segundos, casas=None):
    """Formata um tempo com a unidade mais legível, com vírgula decimal."""
    if segundos is None:
        return "—"
    if segundos >= 1:
        return f"{br(segundos, 2 if casas is None else casas)} s"
    if segundos >= 1e-3:
        return f"{br(segundos * 1e3, 2 if casas is None else casas)} ms"
    if segundos >= 1e-6:
        return f"{br(segundos * 1e6, 1 if casas is None else casas)} µs"
    return f"{br(segundos * 1e9, 0)} ns"
