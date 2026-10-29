# Calibração das regras do `escolher`

Gerado por `python -m benchmarks.calibrar`. Tempos medianos; o menor de cada linha em negrito.

## A. Tamanho da lista (chaves grandes, aleatórias)

A inserção vence até ~24 elementos (em 32 a híbrida já empata) → `LIMIAR_PEQUENA = 24`. A base só passa a híbrida a partir de ~512, por causa do custo fixo de criar 256 baldes a cada passada → `MIN_BASE = 512`.

| n | insercao | hibrida | intercalacao | rapida | base |
|---:|---:|---:|---:|---:|---:|
| 8 | **1,6 µs** | 1,9 µs | 5,0 µs | 5,3 µs | 100,7 µs |
| 16 | **5,0 µs** | 5,3 µs | 10,9 µs | 11,8 µs | 97,2 µs |
| 24 | **10,1 µs** | 10,2 µs | 19,6 µs | 18,1 µs | 103,4 µs |
| 32 | 17,3 µs | **15,4 µs** | 26,0 µs | 26,0 µs | 113,3 µs |
| 48 | 38,8 µs | **28,8 µs** | 44,6 µs | 43,6 µs | 126,6 µs |
| 64 | 67,6 µs | **38,4 µs** | 61,5 µs | 58,8 µs | 133,1 µs |
| 128 | 237,1 µs | **94,4 µs** | 125,2 µs | 138,3 µs | 168,7 µs |
| 256 | 1,39 ms | **241,4 µs** | 437,0 µs | 431,0 µs | 394,6 µs |
| 512 | 3,97 ms | 569,6 µs | 616,6 µs | 709,1 µs | **386,8 µs** |
| 1024 | 17,58 ms | 1,38 ms | 1,57 ms | 1,75 ms | **675,7 µs** |

## B. Amplitude da faixa (n = 10 000)

A contagem custa O(n + k): enquanto a amplitude k é da ordem de n, ela é a mais rápida; a partir de ~2–3·n a base passa à frente → `FATOR_CONTAGEM = 2`.

| k / n | k | contagem | base | hibrida |
|---:|---:|---:|---:|---:|
| 0,01·n | 100 | **517,3 µs** | 964,3 µs | 8,77 ms |
| 0,1·n | 1.000 | **785,2 µs** | 2,23 ms | 13,23 ms |
| 0,5·n | 5.000 | **1,11 ms** | 1,96 ms | 15,27 ms |
| 1·n | 10.000 | **1,46 ms** | 1,93 ms | 17,08 ms |
| 2·n | 20.000 | 1,75 ms | **1,70 ms** | 16,21 ms |
| 3·n | 30.000 | 2,09 ms | **1,76 ms** | 17,07 ms |
| 5·n | 50.000 | 2,78 ms | **2,07 ms** | 17,15 ms |
| 10·n | 100.000 | 4,13 ms | **2,61 ms** | 17,85 ms |
| 50·n | 500.000 | 14,60 ms | **2,31 ms** | 16,43 ms |

## C. Tamanho das chaves (n = 10 000, log₂ n ≈ 13,3)

A base faz uma passada a cada 8 bits; os métodos por comparação fazem ~log₂ n níveis. Cada passada da base é mais barata que um nível de comparações, então ela aguenta um pouco mais de passadas que log₂ n: vence com folga até 16 passadas (128 bits), empata em 20 e perde a partir de 24 → regra `passadas <= 1,5·log2(n)` (≈ 20 para n = 10 000).

| bits | passadas | base | hibrida | intercalacao | regra escolhe |
|---:|---:|---:|---:|---:|---:|
| 16 | 2 | **1,97 ms** | 19,66 ms | 18,06 ms | base |
| 32 | 4 | **4,73 ms** | 23,92 ms | 17,29 ms | base |
| 64 | 8 | **6,97 ms** | 17,34 ms | 17,37 ms | base |
| 96 | 12 | **10,38 ms** | 17,72 ms | 17,78 ms | base |
| 128 | 16 | **13,24 ms** | 18,91 ms | 17,68 ms | base |
| 160 | 20 | **16,34 ms** | 18,17 ms | 16,75 ms | híbrida |
| 192 | 24 | 21,86 ms | 19,28 ms | **17,35 ms** | híbrida |
| 256 | 32 | 25,93 ms | 17,10 ms | **15,88 ms** | híbrida |

## D. Grau de desordem (n = 10 000, chaves grandes ordenadas + trocas)

Com trocas entre vizinhos, a inserção é imbatível em toda a faixa testada. Com trocas distantes, cada elemento fora do lugar custa O(n) deslocamentos e a inserção perde já com 0,1% de trocas — e o número de descidas NÃO distingue os dois casos (2% de descidas pode ser ótimo ou péssimo para a inserção). Escolhemos `FRACAO_DESCIDAS = 0.05`, que acerta o caso 'vizinhas' e erra o 'distantes' (ver seção de erros no RELATORIO).

| trocas | % trocado | % descidas | insercao | base | intercalacao |
|---:|---:|---:|---:|---:|---:|
| vizinhas | 0,1% | 0,1% | **843,8 µs** | 4,66 ms | 4,49 ms |
| vizinhas | 1,0% | 1,0% | **869,8 µs** | 4,63 ms | 4,40 ms |
| vizinhas | 5,0% | 4,7% | **806,0 µs** | 4,53 ms | 4,50 ms |
| vizinhas | 10,0% | 8,3% | **872,6 µs** | 4,93 ms | 5,31 ms |
| distantes | 0,1% | 0,2% | 6,61 ms | **4,93 ms** | 7,85 ms |
| distantes | 1,0% | 2,0% | 46,71 ms | **4,70 ms** | 10,67 ms |
| distantes | 5,0% | 9,0% | 196,26 ms | **4,55 ms** | 12,20 ms |
| distantes | 10,0% | 16,6% | 415,09 ms | **7,72 ms** | 17,63 ms |

## E. Quanto custa olhar a lista (n = 10 000, aleatória)

Duas passadas com os embutidos `min()` e `max()` (escritos em C) saem mais baratas que uma única passada escrita em Python. E a contagem de descidas com parada antecipada olha só ~10% de uma lista aleatória.

| operação | tempo |
|---:|---:|
| min() + max() embutidos (2 passadas em C) | 280,0 µs |
| 1 laço Python calculando min e max | 397,9 µs |
| contar descidas COM parada antecipada | 44,6 µs |
| contar descidas SEM parada (lista inteira) | 445,8 µs |
| referência: ordenar com a híbrida | 16,76 ms |
