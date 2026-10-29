"""Experimentos que deram origem às constantes do `escolher`.

Uso (na raiz do repositório):

    python -m benchmarks.calibrar

Gera resultados/calibracao.md com cinco tabelas:
  A. tamanho da lista       -> LIMIAR_PEQUENA e MIN_BASE
  B. amplitude da faixa     -> FATOR_CONTAGEM
  C. tamanho das chaves     -> regra "passadas da base <= log2(n)"
  D. grau de desordem       -> FRACAO_DESCIDAS
  E. custo de olhar a lista -> por que min()+max() e não um laço único
"""

import math
import random
from pathlib import Path

from src.escolher import contar_descidas
from src.metodos import METODOS
from src.metodos.base import passadas_necessarias

from .medicao import br, formatar, medir_intercalado

PASTA = Path(__file__).resolve().parent.parent / "resultados"
R = random.Random(7)
RODADAS = 5


def tabela(titulo, explicacao, cab, linhas, saida):
    saida.append(f"## {titulo}\n\n{explicacao}\n")
    saida.append("| " + " | ".join(cab) + " |")
    saida.append("|" + "---:|" * len(cab))
    for ln in linhas:
        saida.append("| " + " | ".join(ln) + " |")
    saida.append("")
    print(f"\n{titulo}")
    for ln in linhas:
        print("   ", " · ".join(ln))


def destacar(tempos):
    """Formata os tempos, com o menor em negrito."""
    menor = min(tempos.values())
    return {m: (f"**{formatar(t)}**" if t == menor else formatar(t)) for m, t in tempos.items()}


def exp_tamanho(saida):
    metodos = ["insercao", "hibrida", "intercalacao", "rapida", "base"]
    linhas = []
    for n in [8, 16, 24, 32, 48, 64, 128, 256, 512, 1024]:
        qtd = max(5, 4000 // n)
        entradas = [[R.randint(-(10**12), 10**12) for _ in range(n)] for _ in range(qtd)]
        t = destacar(medir_intercalado({m: METODOS[m] for m in metodos}, entradas, RODADAS, RODADAS))
        linhas.append([str(n)] + [t[m] for m in metodos])
    tabela("A. Tamanho da lista (chaves grandes, aleatórias)",
           "A inserção vence até ~24 elementos (em 32 a híbrida já empata) → `LIMIAR_PEQUENA = 24`. "
           "A base só passa a híbrida a partir de ~512, por causa do custo fixo de criar 256 baldes "
           "a cada passada → `MIN_BASE = 512`.",
           ["n"] + metodos, linhas, saida)


def exp_faixa(saida):
    n = 10_000
    metodos = ["contagem", "base", "hibrida"]
    linhas = []
    for fator in [0.01, 0.1, 0.5, 1, 2, 3, 5, 10, 50]:
        k = max(2, int(fator * n))
        entradas = [[R.randrange(k) for _ in range(n)]]
        t = destacar(medir_intercalado({m: METODOS[m] for m in metodos}, entradas, RODADAS, RODADAS))
        linhas.append([br(fator, 2).rstrip("0").rstrip(",") + "·n", f"{k:,}".replace(",", ".")] + [t[m] for m in metodos])
    tabela("B. Amplitude da faixa (n = 10 000)",
           "A contagem custa O(n + k): enquanto a amplitude k é da ordem de n, ela é a mais rápida; "
           "a partir de ~2–3·n a base passa à frente → `FATOR_CONTAGEM = 2`.",
           ["k / n", "k"] + metodos, linhas, saida)


def exp_bits(saida):
    n = 10_000
    metodos = ["base", "hibrida", "intercalacao"]
    linhas = []
    for bits in [16, 32, 64, 96, 128, 160, 192, 256]:
        entradas = [[R.getrandbits(bits) for _ in range(n)]]
        t = destacar(medir_intercalado({m: METODOS[m] for m in metodos}, entradas, RODADAS, RODADAS))
        d = passadas_necessarias((1 << bits) - 1)
        regra = "base" if d <= 1.5 * math.log2(n) else "híbrida"
        linhas.append([str(bits), str(d)] + [t[m] for m in metodos] + [regra])
    tabela(f"C. Tamanho das chaves (n = 10 000, log₂ n ≈ {br(math.log2(n), 1)})",
           "A base faz uma passada a cada 8 bits; os métodos por comparação fazem ~log₂ n níveis. "
           "Cada passada da base é mais barata que um nível de comparações, então ela aguenta "
           "um pouco mais de passadas que log₂ n: vence com folga até 16 passadas (128 bits), empata em 20 e perde a partir de 24 "
           "→ regra `passadas <= 1,5·log2(n)` (≈ 20 para n = 10 000).",
           ["bits", "passadas"] + metodos + ["regra escolhe"], linhas, saida)


def exp_desordem(saida):
    n = 10_000
    metodos = ["insercao", "base", "intercalacao"]
    linhas = []
    for tipo in ["vizinhas", "distantes"]:
        for frac in [0.001, 0.01, 0.05, 0.1]:
            v = sorted(R.randint(-(10**12), 10**12) for _ in range(n))
            for _ in range(int(frac * n)):
                i = R.randrange(n - 1)
                j = i + 1 if tipo == "vizinhas" else R.randrange(n)
                v[i], v[j] = v[j], v[i]
            desc = contar_descidas(v, n)
            t = destacar(medir_intercalado({m: METODOS[m] for m in metodos}, [v], 3, 3))
            linhas.append([tipo, br(100 * frac, 1) + "%", br(100 * desc / n, 1) + "%"] + [t[m] for m in metodos])
    tabela("D. Grau de desordem (n = 10 000, chaves grandes ordenadas + trocas)",
           "Com trocas entre vizinhos, a inserção é imbatível em toda a faixa testada. "
           "Com trocas distantes, cada elemento fora do lugar custa O(n) deslocamentos e a inserção "
           "perde já com 0,1% de trocas — e o número de descidas NÃO distingue os dois casos "
           "(2% de descidas pode ser ótimo ou péssimo para a inserção). "
           "Escolhemos `FRACAO_DESCIDAS = 0.05`, que acerta o caso 'vizinhas' e erra o 'distantes' "
           "(ver seção de erros no RELATORIO).",
           ["trocas", "% trocado", "% descidas"] + metodos, linhas, saida)


def exp_custo(saida):
    n = 10_000
    v = [R.randint(-(10**12), 10**12) for _ in range(n)]

    def min_max_embutidos(v):
        return min(v), max(v)

    def laco_unico_python(v):
        mn = mx = v[0]
        for x in v:
            if x < mn:
                mn = x
            elif x > mx:
                mx = x
        return mn, mx

    def descidas_com_parada(v):
        return contar_descidas(v, int(len(v) * 0.05))

    def descidas_sem_parada(v):
        return contar_descidas(v, len(v))

    def ordenar_hibrida(v):
        return METODOS["hibrida"](v)

    fs = {
        "min() + max() embutidos (2 passadas em C)": min_max_embutidos,
        "1 laço Python calculando min e max": laco_unico_python,
        "contar descidas COM parada antecipada": descidas_com_parada,
        "contar descidas SEM parada (lista inteira)": descidas_sem_parada,
        "referência: ordenar com a híbrida": ordenar_hibrida,
    }
    t = medir_intercalado(fs, [v], 9, 9)
    linhas = [[nome, formatar(s)] for nome, s in t.items()]
    tabela("E. Quanto custa olhar a lista (n = 10 000, aleatória)",
           "Duas passadas com os embutidos `min()` e `max()` (escritos em C) saem mais baratas que uma "
           "única passada escrita em Python. E a contagem de descidas com parada antecipada olha só "
           "~10% de uma lista aleatória.",
           ["operação", "tempo"], linhas, saida)


def main():
    PASTA.mkdir(exist_ok=True)
    saida = ["# Calibração das regras do `escolher`", "",
             "Gerado por `python -m benchmarks.calibrar`. Tempos medianos; o menor de cada linha em negrito.", ""]
    for exp in (exp_tamanho, exp_faixa, exp_bits, exp_desordem, exp_custo):
        exp(saida)
    (PASTA / "calibracao.md").write_text("\n".join(saida), encoding="utf-8")
    print(f"\nSalvo em {PASTA / 'calibracao.md'}")


if __name__ == "__main__":
    main()
