"""Ordenação por base (radix sort LSD), base 2^BITS.

Custo: O(d · (n + B)), onde B = 2^BITS é o número de baldes e
d = ceil(bits da amplitude / BITS) é o número de passadas.
Estável em cada passada; não compara elementos.

Aceita negativos: as chaves são deslocadas por `min`, o que também
reduz o número de dígitos quando os valores estão longe do zero.
"""

BITS = 8
BASE = 1 << BITS
MASCARA = BASE - 1


def passadas_necessarias(amplitude):
    """Quantas passadas de BITS bits cobrem `amplitude` (max - min)."""
    return max(1, (amplitude.bit_length() + BITS - 1) // BITS)


def base(v, menor=None, maior=None):
    """Devolve uma nova lista ordenada. Não altera `v`.

    `menor`/`maior` são opcionais: se o chamador já os conhece (o
    `ordenar` conhece, porque o `escolher` calculou), evita outra passada.
    """
    if len(v) <= 1:
        return list(v)
    if menor is None:
        menor, maior = min(v), max(v)
    a = [x - menor for x in v]
    d = passadas_necessarias(maior - menor)
    desloc = 0
    for _ in range(d):
        baldes = [[] for _ in range(BASE)]
        for x in a:
            baldes[(x >> desloc) & MASCARA].append(x)
        a = [x for b in baldes for x in b]
        desloc += BITS
    return [x + menor for x in a]
