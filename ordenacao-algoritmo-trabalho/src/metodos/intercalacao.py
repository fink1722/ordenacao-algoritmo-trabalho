"""Ordenação por intercalação (merge sort), top-down.

Custo: O(n log n) em todos os casos, memória auxiliar O(n).
Estável.

Otimização: se a última chave da metade esquerda já é <= primeira da
direita, as metades já estão em ordem e a intercalação é pulada.
"""


def _intercalar(esq, dir_):
    if not esq or not dir_ or esq[-1] <= dir_[0]:
        return esq + dir_
    saida = []
    i = j = 0
    ne, nd = len(esq), len(dir_)
    while i < ne and j < nd:
        if esq[i] <= dir_[j]:
            saida.append(esq[i])
            i += 1
        else:
            saida.append(dir_[j])
            j += 1
    saida.extend(esq[i:])
    saida.extend(dir_[j:])
    return saida


def intercalacao(v):
    """Devolve uma nova lista ordenada. Não altera `v`."""
    a = list(v)
    if len(a) <= 1:
        return a
    meio = len(a) // 2
    return _intercalar(intercalacao(a[:meio]), intercalacao(a[meio:]))
