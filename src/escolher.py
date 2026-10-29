"""O escolhedor: olha a lista e devolve o nome do método mais adequado.

Regras, em ordem (a primeira que casar decide):

  1. n <= LIMIAR_PEQUENA                         -> "insercao"
  2. poucas descidas (v[i] > v[i+1])             -> "insercao"
  3. faixa estreita: k <= FATOR_CONTAGEM * n     -> "contagem"
     (e k <= LIMITE_CONTADORES, para não estourar a memória)
  4. n >= MIN_BASE e passadas <= 1,5·log2(n)     -> "base"
  5. caso contrário                              -> "hibrida"

Custo: a regra 2 percorre a lista em Python, mas PARA CEDO assim que
encontra descidas demais (numa lista aleatória ela olha só ~10% dos
elementos). A regra 3 precisa de min e max: usamos os embutidos min()
e max(), que são duas passadas, mas em C, mais rápidas que uma única
passada em Python (medido em `benchmarks/calibrar.py`).

Todas as constantes vieram de `python -m benchmarks.calibrar`.
"""

import math

from .metodos.base import passadas_necessarias
from .metodos.contagem import LIMITE_CONTADORES

LIMIAR_PEQUENA = 24  # até aqui a inserção vence (overhead mínimo)
FRACAO_DESCIDAS = 0.05  # até 5% de descidas = "quase ordenada"
FATOR_CONTAGEM = 2  # contagem vence a base enquanto k <= ~2n
MIN_BASE = 512  # abaixo disso os 256 baldes da base custam caro
FATOR_PASSADAS = 1.5  # base vence enquanto passadas <= ~1,5·log2(n)


def contar_descidas(v, limite):
    """Conta posições com v[i] > v[i+1], parando assim que passar de `limite`."""
    descidas = 0
    anterior = v[0]
    for x in v:
        if x < anterior:
            descidas += 1
            if descidas > limite:
                return descidas
        anterior = x
    return descidas


def escolher(v):
    """Devolve o nome do método: 'insercao', 'contagem', 'base' ou 'hibrida'."""
    return analisar(v)[0]


def analisar(v):
    """Como `escolher`, mas devolve também o que foi descoberto sobre a
    lista ({"menor": ..., "maior": ...}), para o `ordenar` reaproveitar."""
    n = len(v)

    # Regra 1: lista minúscula
    if n <= LIMIAR_PEQUENA:
        return "insercao", {}

    # Regra 2: quase ordenada (para cedo se não for)
    limite = int(n * FRACAO_DESCIDAS)
    if contar_descidas(v, limite) <= limite:
        return "insercao", {}

    # Regra 3: faixa estreita — e checagem de memória ANTES de chamar a contagem
    menor, maior = min(v), max(v)
    k = maior - menor + 1
    extremos = {"menor": menor, "maior": maior}
    if k <= FATOR_CONTAGEM * n and k <= LIMITE_CONTADORES:
        return "contagem", extremos

    # Regra 4: base, se o número de passadas não passar de ~1,5·log2(n)
    if n >= MIN_BASE and passadas_necessarias(k - 1) <= FATOR_PASSADAS * math.log2(n):
        return "base", extremos

    # Regra 5: o caso geral
    return "hibrida", {}
