"""Ordenação por inserção.

Custo: O(n + I), onde I é o número de inversões da lista.
- Melhor caso (já ordenada): O(n)
- Pior caso (invertida):     O(n²)

É imbatível em listas minúsculas (quase nenhum overhead) e em listas
quase ordenadas, onde cada elemento anda poucas posições.
"""


def insercao(v):
    """Devolve uma nova lista ordenada. Não altera `v`."""
    a = list(v)
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x
    return a
