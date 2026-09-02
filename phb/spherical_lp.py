"""
Delsarte-Goethals-Seidel LP for spherical codes A(n, s), degree-capped, with discretised sign constraint.

f(t) = sum_{m=0}^{N} f_m P_m(t),  P_m = Gegenbauer C_m^{(n-2)/2} normalised by P_m(1) = 1,
f_m >= 0, f_0 = 1, f(t) <= 0 on [-1, s]   =>   A(n, s) <= f(1).
The constraint is imposed on a fine grid, so the value is a (slightly optimistic) lower bound on the true
degree-N LP value; that is exactly what a necessary-condition test needs.  The max of the optimal f over a
much finer grid is returned as a diagnostic.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import linprog


def gegenbauer_normalised(n: int, N: int, t: np.ndarray) -> np.ndarray:
    """P_m(t) for m = 0..N, shape (N+1, len(t))."""
    t = np.asarray(t, dtype=float)
    P = np.zeros((N + 1, t.size))
    P[0] = 1.0
    if N >= 1:
        P[1] = t
    for m in range(1, N):
        P[m + 1] = ((2 * m + n - 2) * t * P[m] - m * P[m - 1]) / (m + n - 2)
    return P


def spherical_lp(n: int, s: float, N: int, grid: int = 3000):
    """Returns (bound f(1), coefficients f_m, max violation of f on a 20x finer grid)."""
    # Chebyshev-distributed points on [-1, s] plus endpoints
    th = np.linspace(0, np.pi, grid)
    t = -1 + (s + 1) * (1 - np.cos(th)) / 2
    P = gegenbauer_normalised(n, N, t)
    # variables f_1..f_N ; minimise sum f_m ; constraints sum_{m>=1} f_m P_m(t_j) <= -1
    c = np.ones(N)
    A_ub = P[1:].T
    b_ub = -np.ones(t.size)
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None)] * N, method="highs")
    if res.status != 0:
        raise RuntimeError(res.message)
    f = np.concatenate([[1.0], res.x])
    tf = np.linspace(-1, s, 20 * grid)
    viol = float(np.max(gegenbauer_normalised(n, N, tf).T @ f))
    return 1.0 + res.fun, f, viol


if __name__ == "__main__":
    # kissing numbers: A(3,1/2)=12 (LP 13.16), A(4,1/2)=24 (LP 25.56), A(8,1/2)=240, A(24,1/2)=196560
    for n, N, known in [(3, 30, 12), (4, 30, 24), (8, 30, 240), (24, 30, 196560)]:
        v, f, viol = spherical_lp(n, 0.5, N)
        print(f"LP_sph(n={n}, s=1/2, deg<={N}) = {v:.4f}  (known A = {known}; max f on fine grid = {viol:.2e})")
