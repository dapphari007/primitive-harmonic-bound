"""
Delsarte LP for constant-weight codes in the Johnson scheme J(n, w), solved exactly.

Relations r = w - |x cap y| (Hamming distance 2r), valencies k_r = C(w,r) C(N,r), N = n - w.
Eigenvalue of the distance-r relation on the j-th Johnson eigenspace (dimension D_j = C(n,j)-C(n,j-1)):
    E_r(j) = sum_{i=0}^{r} (-1)^i C(j,i) C(w-j, r-i) C(N-j, r-i)        (Eberlein polynomial)
Dual eigenvalues Q_j(r) = D_j E_r(j) / k_r.   LP:
    max sum_r A_r,  A_0 = 1,  A_r = 0 for 1 <= r < d/2,  A_r >= 0,  sum_r A_r Q_j(r) >= 0 (j = 1..w).
"""
from __future__ import annotations

import math
from fractions import Fraction
from functools import lru_cache

from .exact_lp import simplex_max


@lru_cache(maxsize=None)
def eberlein(n: int, w: int, r: int, j: int) -> int:
    N = n - w
    return sum((-1) ** i * math.comb(j, i) * math.comb(w - j, r - i) * math.comb(N - j, r - i) for i in range(0, r + 1))


def Dj(n: int, j: int) -> int:
    return math.comb(n, j) - (math.comb(n, j - 1) if j >= 1 else 0)


def johnson_lp(n: int, w: int, d: int) -> Fraction:
    """Exact Delsarte LP bound on A_J(n, w, d) (d even)."""
    assert d % 2 == 0
    N = n - w
    rmin = d // 2
    free = list(range(rmin, w + 1))
    if not free:
        return Fraction(1)
    A, b = [], []
    for j in range(1, w + 1):
        row = []
        for r in free:
            kr = math.comb(w, r) * math.comb(N, r)
            row.append(-Fraction(Dj(n, j) * eberlein(n, w, r, j), kr))
        A.append(row)
        b.append(Fraction(Dj(n, j)))  # Q_j(0) = D_j
    val, _ = simplex_max([1] * len(free), A, b)
    return 1 + val


if __name__ == "__main__":
    # sanity: exact values A(n,d,w): A(8,4,4)=14, A(9,4,4)=18, A(12,6,6)=22, A(24,8,12)=2576 (Golay), A(16,8,8)=30, A(10,4,5)=36
    for n, d, w, known in [(8, 4, 4, 14), (9, 4, 4, 18), (12, 6, 6, 22), (16, 8, 8, 30), (10, 4, 5, 36), (24, 8, 12, 2576), (24, 8, 8, 759)]:
        print(f"LP_J(n={n}, w={w}, d={d}) = {float(johnson_lp(n, w, d)):.4f}   known A(n,d,w) = {known}")
