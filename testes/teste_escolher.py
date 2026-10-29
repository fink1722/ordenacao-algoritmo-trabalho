"""Testes das regras do `escolher`."""

import random

from src.escolher import LIMIAR_PEQUENA, escolher
from src.metodos.contagem import LIMITE_CONTADORES

rng = random.Random(0)


def test_vazia_e_um_elemento():
    assert escolher([]) == "insercao"
    assert escolher([1]) == "insercao"


def test_lista_minuscula_usa_insercao():
    v = [rng.randint(-(10**12), 10**12) for _ in range(LIMIAR_PEQUENA)]
    assert escolher(v) == "insercao"


def test_ja_ordenada_usa_insercao():
    assert escolher(list(range(10_000))) == "insercao"


def test_todos_iguais_usa_insercao():
    # zero descidas: a inserção faz uma passada e termina
    assert escolher([3] * 1000) == "insercao"


def test_quase_ordenada_usa_insercao():
    v = list(range(10_000))
    for _ in range(100):
        i = rng.randrange(len(v) - 1)
        v[i], v[i + 1] = v[i + 1], v[i]
    assert escolher(v) == "insercao"


def test_invertida_nao_usa_insercao():
    assert escolher(list(range(10_000, 0, -1))) != "insercao"


def test_faixa_estreita_usa_contagem():
    v = [rng.randint(-50, 50) for _ in range(10_000)]
    assert escolher(v) == "contagem"


def test_faixa_gigante_nunca_usa_contagem():
    # prevê o estouro de memória antes de chamar a contagem
    v = [rng.randint(0, LIMITE_CONTADORES * 100) for _ in range(LIMITE_CONTADORES // 10)]
    assert escolher(v) != "contagem"


def test_chaves_grandes_usa_base():
    v = [rng.randint(-(10**12), 10**12) for _ in range(10_000)]
    assert escolher(v) == "base"


def test_chaves_enormes_usa_hibrida():
    # 512 bits = 64 passadas da base, bem mais que log2(10 000) ≈ 13
    v = [rng.getrandbits(512) for _ in range(10_000)]
    assert escolher(v) == "hibrida"


def test_tamanho_medio_usa_hibrida():
    # 33..255 elementos: grande demais para inserção, pequeno para a base
    v = [rng.randint(-(10**12), 10**12) for _ in range(100)]
    assert escolher(v) == "hibrida"
