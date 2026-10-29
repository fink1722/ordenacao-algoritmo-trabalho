"""Ordenação híbrida: quicksort com pivô aleatório + inserção.

O quicksort divide a lista até as partes ficarem pequenas
(<= LIMIAR_INSERCAO elementos). Essas partes são deixadas como estão;
no final, uma única passada de inserção sobre a lista inteira termina
o trabalho. Como cada elemento já está a no máximo LIMIAR posições do
seu lugar final, essa passada custa O(n · LIMIAR).

O limiar 16 fica abaixo do ponto em que a inserção pura deixa de vencer
(~24, ver tabela A de resultados/calibracao.md).
"""

from .rapida import _gerador, particionar3

LIMIAR_INSERCAO = 16


def _quick_ate_limiar(a, ini, fim, rng):
    while fim - ini + 1 > LIMIAR_INSERCAO:
        lt, gt = particionar3(a, ini, fim, rng)
        if lt - ini < fim - gt:
            _quick_ate_limiar(a, ini, lt - 1, rng)
            ini = gt + 1
        else:
            _quick_ate_limiar(a, gt + 1, fim, rng)
            fim = lt - 1


def _insercao_no_lugar(a):
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x


def hibrida(v, semente=None):
    """Devolve uma nova lista ordenada. Não altera `v`."""
    a = list(v)
    _quick_ate_limiar(a, 0, len(a) - 1, _gerador(semente))
    _insercao_no_lugar(a)
    return a
