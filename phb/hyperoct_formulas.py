"""
Conjectured closed forms for the directed squared coordinate coefficients of the binary TWO-ROW
representation graph (hyperoctahedral group B_n, stabilizer S_n, stabilizer irrep mu = (n-k, k)).

Vertex lambda = (alpha, beta) = ((a1, a2), (b1, b2)),  a1 + a2 + b1 + b2 = n,  a1 >= a2, b1 >= b2.
Moves: a box leaves row r of one partition and joins row r' of the other.  With
    N = n (a1 + 1 - a2)(b1 + 1 - b2):
    p(a1->b1) = (a1+1) (a1+b2-k)(a2+b1+1-k) / N          p(b1->a1) = (b1+1) (a2+b1-k)(a1+b2+1-k) / N
    p(a1->b2) = (a1+1) (k-a2-b2)(a1+b1+1-k) / N          p(b1->a2) = (b1+1) (k-a2-b2)(a1+b1+1-k) / N
    p(a2->b1) =   a2   (k-a2-b2+1)(a1+b1+2-k) / N        p(b2->a1) =   b2   (k-a2-b2+1)(a1+b1+2-k) / N
    p(a2->b2) =   a2   (a2+b1-k)(a1+b2+1-k) / N          p(b2->a2) =   b2   (a1+b2-k)(a2+b1+1-k) / N
Every root pair sums to n+1.  Found by exact numerical computation (experiments/hyperoct_collect.py) and
formula mining (experiments/hyperoct_roots.py, hyperoct_formulas.py); verified on all n <= 11 data.
"""
from __future__ import annotations

import math
from fractions import Fraction

MOVES = ["a1->b1", "a1->b2", "a2->b1", "a2->b2", "b1->a1", "b1->a2", "b2->a1", "b2->a2"]


def p_formula(move: str, a1, a2, b1, b2, k):
    n = a1 + a2 + b1 + b2
    N = n * (a1 + 1 - a2) * (b1 + 1 - b2)
    if move == "a1->b1": num = (a1 + 1) * (a1 + b2 - k) * (a2 + b1 + 1 - k)
    elif move == "a1->b2": num = (a1 + 1) * (k - a2 - b2) * (a1 + b1 + 1 - k)
    elif move == "a2->b1": num = a2 * (k - a2 - b2 + 1) * (a1 + b1 + 2 - k)
    elif move == "a2->b2": num = a2 * (a2 + b1 - k) * (a1 + b2 + 1 - k)
    elif move == "b1->a1": num = (b1 + 1) * (a2 + b1 - k) * (a1 + b2 + 1 - k)
    elif move == "b1->a2": num = (b1 + 1) * (k - a2 - b2) * (a1 + b1 + 1 - k)
    elif move == "b2->a1": num = b2 * (k - a2 - b2 + 1) * (a1 + b1 + 2 - k)
    elif move == "b2->a2": num = b2 * (a1 + b2 - k) * (a2 + b1 + 1 - k)
    else: raise ValueError(move)
    return Fraction(num, N) if isinstance(a1, int) else num / N


def target(move: str, a1, a2, b1, b2):
    a = [a1, a2, 0]; b = [b1, b2, 0]
    src, dst = move.split("->")
    if src[0] == "a":
        a[int(src[1]) - 1] -= 1; b[int(dst[1]) - 1] += 1
    else:
        b[int(src[1]) - 1] -= 1; a[int(dst[1]) - 1] += 1
    return tuple(a), tuple(b)


def admissible(a1, a2, b1, b2, k) -> bool:
    """Two-row shapes containing S^(n-k,k): a2+b2 <= k <= min(a1+b2, a2+b1)."""
    return a1 >= a2 >= 0 and b1 >= b2 >= 0 and a2 + b2 <= k <= min(a1 + b2, a2 + b1)


def dim_V(a1, a2, b1, b2) -> int:
    n = a1 + a2 + b1 + b2
    f = lambda m, a: math.comb(m, a) - (math.comb(m, a - 1) if a >= 1 else 0)
    return math.comb(n, b1 + b2) * f(a1 + a2, a2) * f(b1 + b2, b2)


def reverse(move: str) -> str:
    src, dst = move.split("->")
    return f"{dst}->{src}"
