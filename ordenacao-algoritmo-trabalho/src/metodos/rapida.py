"""Ordenação rápida (quicksort) com pivô aleatório.

Custo esperado: O(n log n). Pior caso O(n²), mas com pivô aleatório
nenhuma entrada específica o provoca de forma sistemática.

Usa partição em três vias (< pivô | = pivô | > pivô), para que listas
com muitas chaves repetidas (ou todas iguais) não degenerem.
A recursão vai sempre para o lado menor, e o lado maior é tratado no
laço; assim a pilha fica O(log n).
"""

import random


def _gerador(semente):
    """Sem semente usa o gerador global (criar um Random novo custa ~15 µs,
    o que pesa em listas pequenas); com semente, um gerador reprodutível."""
    return random if semente is None else random.Random(semente)


def particionar3(a, ini, fim, rng):
    """Particiona a[ini..fim] em três faixas. Devolve (lt, gt):
    a[ini..lt-1] < p,  a[lt..gt] == p,  a[gt+1..fim] > p."""
    p = a[rng.randint(ini, fim)]
    lt, i, gt = ini, ini, fim
    while i <= gt:
        x = a[i]
        if x < p:
            a[lt], a[i] = x, a[lt]
            lt += 1
            i += 1
        elif x > p:
            a[gt], a[i] = x, a[gt]
            gt -= 1
        else:
            i += 1
    return lt, gt


def _rapida(a, ini, fim, rng):
    while ini < fim:
        lt, gt = particionar3(a, ini, fim, rng)
        if lt - ini < fim - gt:
            _rapida(a, ini, lt - 1, rng)
            ini = gt + 1
        else:
            _rapida(a, gt + 1, fim, rng)
            fim = lt - 1


def rapida(v, semente=None):
    """Devolve uma nova lista ordenada. Não altera `v`."""
    a = list(v)
    _rapida(a, 0, len(a) - 1, _gerador(semente))
    return a
