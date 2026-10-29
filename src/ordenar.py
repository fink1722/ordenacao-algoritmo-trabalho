"""Ordenação adaptativa: escolhe o método e executa."""

from .escolher import analisar
from .metodos import METODOS


def ordenar(v):
    """Devolve uma nova lista ordenada usando o método indicado por `escolher`.

    O que o escolhedor já descobriu sobre a lista (menor e maior valor)
    é repassado à contagem e à base, que assim não percorrem a lista
    de novo só para calcular os extremos.
    """
    metodo, extremos = analisar(v)
    return METODOS[metodo](v, **extremos)
