"""
Delsarte linear-programming bound for binary codes A(n, d).

    maximise   sum_{i=0}^{n} A_i
    subject to A_0 = 1,  A_i = 0 (1 <= i < d),  A_i >= 0,
               sum_i A_i K_j(i) >= 0   for j = 1..n,

where K_j(i) = sum_t (-1)^t C(i,t) C(n-i, j-t) is the Krawtchouk polynomial.
Krawtchouk values are exact integers; the LP is solved with HiGHS (scipy).
"""
from __future__ import annotations

import math
from functools import lru_cache

import numpy as np
from scipy.optimize import linprog


@lru_cache(maxsize=None)
def krawtchouk_table(n: int) -> np.ndarray:
    """K[j, i] = K_j(i) for 0 <= j, i <= n as float64 (exact for n <= ~50)."""
    K = np.zeros((n + 1, n + 1))
    for j in range(n + 1):
        for i in range(n + 1):
            K[j, i] = sum((-1) ** t * math.comb(i, t) * math.comb(n - i, j - t) for t in range(0, j + 1))
    return K


def delsarte_lp(n: int, d: int) -> float:
    """Delsarte LP upper bound on A(n, d) (float)."""
    K = krawtchouk_table(n)
    free = [i for i in range(d, n + 1)]  # A_0 = 1 fixed; A_1..A_{d-1} = 0
    m = len(free)
    if m == 0:
        return 1.0
    # variables x = A_free.  maximise sum x  ->  minimise -sum x
    c = -np.ones(m)
    # constraints: -(K[j,0] + sum_i x_i K[j,i]) <= 0  for j = 1..n
    # Row j is divided by C(n,j) = K_j(0) so every coefficient has modulus <= 1 (numerical scaling);
    # the trivial bounds A_i <= C(n,i) are added so HiGHS never reports 'unbounded' on round-off.
    rows = np.array([math.comb(n, j) for j in range(1, n + 1)], dtype=float)
    A_ub = -K[1:, free] / rows[:, None]
    b_ub = K[1:, 0] / rows
    bnds = [(0, float(math.comb(n, i))) for i in free]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bnds, method="highs")
    if res.status != 0:
        raise RuntimeError(f"LP failed for n={n} d={d}: {res.message}")
    return 1.0 - res.fun


if __name__ == "__main__":
    # sanity: known exact values A(7,3)=16 (Hamming), A(8,4)=16, A(23,7)=4096 (Golay), A(24,8)=4096
    for n, d, expect in [(7, 3, 16), (8, 4, 16), (8, 2, 128), (23, 7, 4096), (24, 8, 4096), (16, 6, 256)]:
        print(f"LP({n},{d}) = {delsarte_lp(n, d):.4f}   known A = {expect}")
