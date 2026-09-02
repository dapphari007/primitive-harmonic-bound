"""
Exact (rational) Delsarte LP for A(n, d), via a dense simplex with Bland's rule over Fractions.

    maximise  sum_{i=d}^{n} x_i
    s.t.      -sum_i x_i K_j(i) <= C(n,j)      (j = 1..n)     [ i.e. C(n,j) + sum_i x_i K_j(i) >= 0 ]
              x_i >= 0

The origin (the one-word code) is feasible, so the slack basis starts the simplex.  Krawtchouk
values are exact integers.  Floating-point HiGHS becomes unreliable above n ~ 45 because the
optimal A_i reach ~2^n while the A_0 = 1 constant must still be resolved; exact arithmetic avoids that.
"""
from __future__ import annotations

import math
from fractions import Fraction
from functools import lru_cache


@lru_cache(maxsize=None)
def krawtchouk_int(n: int):
    return [[sum((-1) ** t * math.comb(i, t) * math.comb(n - i, j - t) for t in range(j + 1))
             for i in range(n + 1)] for j in range(n + 1)]


def simplex_max(c, A, b):
    """max c.x s.t. A x <= b, x >= 0, with b >= 0.  Dense tableau, Bland's rule, exact Fractions."""
    m, nv = len(A), len(c)
    # tableau rows: [A | I | b], objective row: [-c | 0 | 0]
    T = [[Fraction(v) for v in A[r]] + [Fraction(int(r == s)) for s in range(m)] + [Fraction(b[r])] for r in range(m)]
    z = [Fraction(-v) for v in c] + [Fraction(0)] * m + [Fraction(0)]
    basis = [nv + r for r in range(m)]
    ncols = nv + m
    while True:
        # Bland: entering = smallest index with negative reduced cost
        enter = next((j for j in range(ncols) if z[j] < 0), None)
        if enter is None:
            break
        # ratio test, ties broken by smallest basis index
        best_r, best_ratio = None, None
        for r in range(m):
            if T[r][enter] > 0:
                ratio = T[r][-1] / T[r][enter]
                if best_ratio is None or ratio < best_ratio or (ratio == best_ratio and basis[r] < basis[best_r]):
                    best_r, best_ratio = r, ratio
        if best_r is None:
            raise RuntimeError("unbounded")
        piv = T[best_r][enter]
        row = [v / piv for v in T[best_r]]
        T[best_r] = row
        for r in range(m):
            if r != best_r and T[r][enter] != 0:
                f = T[r][enter]
                T[r] = [a - f * bb for a, bb in zip(T[r], row)]
        if z[enter] != 0:
            f = z[enter]
            z = [a - f * bb for a, bb in zip(z, row)]
        basis[best_r] = enter
    x = [Fraction(0)] * nv
    for r in range(m):
        if basis[r] < nv:
            x[basis[r]] = T[r][-1]
    return z[-1], x


def exact_delsarte_lp(n: int, d: int) -> Fraction:
    K = krawtchouk_int(n)
    free = list(range(d, n + 1))
    if not free:
        return Fraction(1)
    A = [[-K[j][i] for i in free] for j in range(1, n + 1)]
    b = [math.comb(n, j) for j in range(1, n + 1)]
    c = [1] * len(free)
    val, _ = simplex_max(c, A, b)
    return 1 + val


if __name__ == "__main__":
    import sys, time
    sys.path.insert(0, __file__.rsplit("phb", 1)[0])
    from phb.delsarte_lp import delsarte_lp
    t0 = time.time()
    worst = 0.0
    for n in range(4, 33):
        for d in range(2, n + 1):
            e = exact_delsarte_lp(n, d)
            f = delsarte_lp(n, d)
            worst = max(worst, abs(float(e) - f) / float(e))
    print(f"exact vs HiGHS agree for n<=32, worst relative difference {worst:.2e}  [{time.time()-t0:.1f}s]")
    for n, d in [(23, 7), (24, 8), (46, 3), (48, 4), (50, 6), (64, 3), (64, 12), (64, 22)]:
        t1 = time.time()
        print(f"exact LP({n},{d}) = {float(exact_delsarte_lp(n, d)):.6g}   [{time.time()-t1:.1f}s]")
