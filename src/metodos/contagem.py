"""Ordenação por contagem (counting sort).

Custo: O(n + k), onde k = max - min + 1 é a amplitude das chaves.
Memória: um contador por valor possível, ou seja O(k).

É linear e muito rápida quando k é pequeno perto de n. Quando k é
enorme, o vetor de contadores não cabe na memória: por isso a função
se recusa a rodar acima de LIMITE_CONTADORES, e o `escolher` faz a
mesma checagem *antes* de chamá-la.

Aceita negativos: as chaves são deslocadas por `min`.
"""

# 10 milhões de contadores ≈ 80 MB numa lista Python (8 bytes por ponteiro).
LIMITE_CONTADORES = 10_000_000


class FaixaGrandeDemais(MemoryError):
    """Amplitude de chaves grande demais para a contagem."""


def contagem(v, menor=None, maior=None):
    """Devolve uma nova lista ordenada. Não altera `v`.

    `menor`/`maior` são opcionais: se o chamador já os conhece (o
    `ordenar` conhece, porque o `escolher` calculou), evita outra passada.
    """
    if len(v) <= 1:
        return list(v)
    if menor is None:
        menor, maior = min(v), max(v)
    k = maior - menor + 1
    if k > LIMITE_CONTADORES:
        raise FaixaGrandeDemais(
            f"faixa de {k:,} valores exigiria {k:,} contadores "
            f"(limite: {LIMITE_CONTADORES:,})"
        )
    cont = [0] * k
    for x in v:
        cont[x - menor] += 1
    saida = []
    for i, c in enumerate(cont):
        if c:
            saida.extend([i + menor] * c)
    return saida
