| Método | Aleatório, chaves grandes | Faixa estreita | Quase ordenado | Lista minúscula |
|---|---:|---:|---:|---:|
| Inserção | 1,72 s | 1,93 s | 🏆 **856,1 µs** | 🏆 **2,5 µs** |
| Intercalação | 16,49 ms | 18,97 ms | 4,68 ms | 6,7 µs |
| Rápida | 20,70 ms | 8,17 ms | 20,29 ms | 6,8 µs |
| Híbrida | 17,21 ms | 8,99 ms | 17,24 ms | 2,8 µs |
| Contagem | 💥 recusou | 🏆 **696,8 µs** | 💥 recusou | 40,7 µs |
| Base | 🏆 **5,22 ms** | 1,16 ms | 4,78 ms | 34,4 µs |
| **ordenar** | 5,03 ms | 756,0 µs | 1,11 ms | 2,7 µs |

| Método | Aleatório, chaves grandes | Faixa estreita | Quase ordenado | Lista minúscula | **Pior caso** |
|---|---:|---:|---:|---:|---:|
| Inserção | 329,25× | 2.763,53× | 1,00× | 1,00× | **2.763,53×** |
| Intercalação | 3,16× | 27,22× | 5,47× | 2,72× | **27,22×** |
| Rápida | 3,96× | 11,73× | 23,70× | 2,73× | **23,70×** |
| Híbrida | 3,29× | 12,90× | 20,13× | 1,13× | **20,13×** |
| Contagem | ∞ (recusa) | 1,00× | ∞ (recusa) | 16,47× | **∞** |
| Base | 1,00× | 1,66× | 5,58× | 13,92× | **13,92×** |
| **ordenar** | 0,96× | 1,08× | 1,30× | 1,10× | **1,30×** |

| Cenário | `escolher` decidiu | Melhor fixo | `ordenar` ÷ melhor fixo | Custo do `escolher` | % do tempo do `ordenar` |
|---|---|---|---:|---:|---:|
| Aleatório, chaves grandes | ✅ `base` | `base` | 0,96× | 335,5 µs | 6,7% |
| Faixa estreita | ✅ `contagem` | `contagem` | 1,08× | 325,8 µs | 43,1% |
| Quase ordenado | ✅ `insercao` | `insercao` | 1,30× | 277,4 µs | 24,9% |
| Lista minúscula | ✅ `insercao` | `insercao` | 1,10× | 93 ns | 3,4% |

| Método | Rotacionada (n = 10 000) |
|---|---:|
| `ordenar` (→ `insercao`) | 2,02 s |
| Base | 1,79 ms |
| Intercalação | 4,60 ms |
| Híbrida | 16,82 ms |
