"""Testes de correção dos seis métodos e do `ordenar`.

Cada função é testada contra os casos de borda pedidos no enunciado
(vazia, um elemento, todos iguais, já ordenada, invertida, negativos)
e contra listas aleatórias, comparando com o `sorted` do Python.
"""

import random

import pytest

from src import METODOS, ordenar
from src.metodos.contagem import LIMITE_CONTADORES, FaixaGrandeDemais, contagem

FUNCOES = {**METODOS, "ordenar": ordenar}

CASOS_DE_BORDA = {
    "vazia": [],
    "um_elemento": [42],
    "dois_elementos": [2, 1],
    "todos_iguais": [7] * 100,
    "ja_ordenada": list(range(200)),
    "invertida": list(range(200, 0, -1)),
    "negativos": [-5, 3, -1, 0, -100, 99, -5, 2],
    "so_negativos": list(range(-1, -150, -1)),
    "zeros_e_negativos": [0, -1, 0, -1, 0],
    "chaves_grandes": [10**15, -(10**15), 0, 10**12, -1],
}


@pytest.mark.parametrize("nome_caso", CASOS_DE_BORDA)
@pytest.mark.parametrize("nome_funcao", FUNCOES)
def test_casos_de_borda(nome_funcao, nome_caso):
    entrada = CASOS_DE_BORDA[nome_caso]
    if nome_funcao == "contagem" and nome_caso == "chaves_grandes":
        with pytest.raises(FaixaGrandeDemais):  # recusa em vez de estourar a memória
            contagem(entrada)
        return
    assert FUNCOES[nome_funcao](entrada) == sorted(entrada)


@pytest.mark.parametrize("nome_funcao", FUNCOES)
@pytest.mark.parametrize("n", [3, 17, 33, 100, 500, 2000])
def test_aleatorios(nome_funcao, n):
    rng = random.Random(n)
    for faixa in (10, 10_000, 10**12):
        entrada = [rng.randint(-faixa, faixa) for _ in range(n)]
        if nome_funcao == "contagem" and 2 * faixa + 1 > LIMITE_CONTADORES:
            continue  # a contagem se recusa (testado à parte)
        assert FUNCOES[nome_funcao](entrada) == sorted(entrada)


@pytest.mark.parametrize("nome_funcao", FUNCOES)
def test_nao_altera_a_entrada(nome_funcao):
    entrada = [5, -2, 9, 0, 5, 1] * 20
    copia = list(entrada)
    FUNCOES[nome_funcao](entrada)
    assert entrada == copia


@pytest.mark.parametrize("nome_funcao", FUNCOES)
def test_lista_grande_invertida_sem_estourar_recursao(nome_funcao):
    if nome_funcao == "insercao":
        pytest.skip("O(n²) — lento demais para este tamanho, não é bug")
    entrada = list(range(20_000, 0, -1))
    assert FUNCOES[nome_funcao](entrada) == sorted(entrada)


def test_contagem_recusa_faixa_gigante():
    with pytest.raises(FaixaGrandeDemais):
        contagem([0, LIMITE_CONTADORES * 10])


def test_ordenar_nao_estoura_com_faixa_gigante():
    entrada = [10**18, -(10**18)] * 50 + list(range(100))
    assert ordenar(entrada) == sorted(entrada)
