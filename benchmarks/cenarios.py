"""Geradores dos cenários de medição. Todos são determinísticos (semente fixa)."""

import random

N = 10_000  # tamanho das listas nos cenários grandes
N_MINUSCULA = 10  # tamanho da lista minúscula
QTD_MINUSCULAS = 2_000  # quantas listas minúsculas medir de uma vez
SEMENTE = 2026


def aleatorio_chaves_grandes(n=N, semente=SEMENTE):
    """n inteiros uniformes em [-10^12, 10^12] — faixa ~2·10^12, com negativos."""
    r = random.Random(semente)
    return [r.randint(-(10**12), 10**12) for _ in range(n)]


def faixa_estreita(n=N, semente=SEMENTE):
    """n inteiros em [-50, 50] — só 101 valores possíveis, muitas repetições."""
    r = random.Random(semente)
    return [r.randint(-50, 50) for _ in range(n)]


def quase_ordenado(n=N, semente=SEMENTE, fracao=0.01):
    """Chaves grandes já ordenadas, com 1% de trocas entre vizinhos."""
    r = random.Random(semente)
    v = sorted(r.randint(-(10**12), 10**12) for _ in range(n))
    for _ in range(int(n * fracao)):
        i = r.randrange(n - 1)
        v[i], v[i + 1] = v[i + 1], v[i]
    return v


def listas_minusculas(qtd=QTD_MINUSCULAS, n=N_MINUSCULA, semente=SEMENTE):
    """`qtd` listas de `n` inteiros em [-1000, 1000]."""
    r = random.Random(semente)
    return [[r.randint(-1000, 1000) for _ in range(n)] for _ in range(qtd)]


def rotacionada(n=N):
    """Lista ordenada 'girada' pela metade: [n/2 .. n-1, 0 .. n/2-1].
    Só UMA descida, mas metade dos elementos está longe do lugar.
    É o cenário em que o `escolher` erra."""
    return list(range(n // 2, n)) + list(range(n // 2))


# nome -> (rótulo, lista de entradas a ordenar)
# Os cenários grandes têm uma única entrada; o minúsculo tem várias.
def todos():
    return {
        "aleatorio": ("Aleatório, chaves grandes", [aleatorio_chaves_grandes()]),
        "estreita": ("Faixa estreita", [faixa_estreita()]),
        "quase": ("Quase ordenado", [quase_ordenado()]),
        "minuscula": ("Lista minúscula", listas_minusculas()),
    }
