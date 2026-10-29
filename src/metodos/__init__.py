"""Os seis métodos de ordenação do semestre.

Todos têm a mesma assinatura: recebem uma lista de inteiros e devolvem
uma NOVA lista ordenada, sem alterar a original.
"""

from .base import base
from .contagem import contagem
from .hibrida import hibrida
from .insercao import insercao
from .intercalacao import intercalacao
from .rapida import rapida

METODOS = {
    "insercao": insercao,
    "intercalacao": intercalacao,
    "rapida": rapida,
    "hibrida": hibrida,
    "contagem": contagem,
    "base": base,
}

__all__ = ["METODOS", *METODOS]
