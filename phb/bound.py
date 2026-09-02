"""
Primitive-harmonic linear-programming bound for binary codes.

Transcribed from "How the Ideas Came Together", Chapter 2 (Sections 2.2-2.4).

For length n, primitive degree k (0 <= k), and retained degree L (k <= L <= n-k):

  * Jacobi matrix J (size L-k+1, indices j = k..L, zero diagonal) with
        J[j, j+1] = J[j+1, j] = c_j = (j-k+1)(n-j-k) / ( n * sqrt((j+1)(n-j)) )      (2.1)
  * lambda = Perron (largest) eigenvalue of J
  * D   = sum_{j=k}^{L} C(n, j)            ambient dimension
  * m_k = C(n, k) - C(n, k-1)              primitive multiplicity
  * s   = 1 - 2d/n                          max normalised inner product at distance >= d

  If lambda > s:   |C| <= (1-s)/(lambda-s) * D / m_k                                 (2.3)

At k = 0 the entries reduce to sqrt((j+1)(n-j))/n, the classical normalised
Krawtchouk recurrence, and the bound is the classical Levenshtein/MRRW-type bound.
"""
from __future__ import annotations

import math
from functools import lru_cache

import numpy as np
from scipy.linalg import eigh_tridiagonal


def jacobi_offdiag(n: int, k: int, L: int) -> np.ndarray:
    """Off-diagonal entries c_j, j = k..L-1, of the Jacobi matrix (2.1)."""
    if not (0 <= k <= L <= n - k):
        raise ValueError(f"need 0 <= k <= L <= n-k, got n={n} k={k} L={L}")
    j = np.arange(k, L, dtype=np.float64)
    num = (j - k + 1.0) * (n - j - k)
    den = n * np.sqrt((j + 1.0) * (n - j))
    return num / den


def perron(n: int, k: int, L: int) -> float:
    """Largest eigenvalue of the symmetric tridiagonal Jacobi matrix (2.1)."""
    size = L - k + 1
    if size == 1:
        return 0.0
    off = jacobi_offdiag(n, k, L)
    diag = np.zeros(size)
    w = eigh_tridiagonal(diag, off, eigvals_only=True, select="i", select_range=(size - 1, size - 1))
    return float(w[0])


def perron_vector(n: int, k: int, L: int) -> tuple[float, np.ndarray]:
    """Perron eigenvalue and positive unit eigenvector of (2.1)."""
    size = L - k + 1
    off = jacobi_offdiag(n, k, L)
    diag = np.zeros(size)
    w, v = eigh_tridiagonal(diag, off, select="i", select_range=(size - 1, size - 1))
    vec = v[:, 0]
    if vec.sum() < 0:
        vec = -vec
    return float(w[0]), vec


@lru_cache(maxsize=None)
def log2_binom(n: int, j: int) -> float:
    if j < 0 or j > n:
        return -math.inf
    return (math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1)) / math.log(2)


def log2_sum_binom(n: int, lo: int, hi: int) -> float:
    """log2 of sum_{j=lo}^{hi} C(n,j), computed stably."""
    terms = [log2_binom(n, j) for j in range(lo, hi + 1)]
    m = max(terms)
    return m + math.log2(sum(2.0 ** (t - m) for t in terms))


def log2_mk(n: int, k: int) -> float:
    """log2 of m_k = C(n,k) - C(n,k-1) (k >= 1); m_0 = 1."""
    if k == 0:
        return 0.0
    a = log2_binom(n, k)
    b = log2_binom(n, k - 1)
    return a + math.log2(1.0 - 2.0 ** (b - a))


def log2_bound(n: int, d: int, k: int, L: int) -> float | None:
    """log2 of the bound (2.3); None if the spectral condition lambda > s fails."""
    s = 1.0 - 2.0 * d / n
    lam = perron(n, k, L)
    if lam <= s:
        return None
    return math.log2((1.0 - s) / (lam - s)) + log2_sum_binom(n, k, L) - log2_mk(n, k)


def bound(n: int, d: int, k: int, L: int) -> float | None:
    """The bound (2.3) itself (float); None if infeasible.  Use log2_bound for large n."""
    lb = log2_bound(n, d, k, L)
    return None if lb is None else 2.0 ** lb


def best_bound(n: int, d: int, k: int) -> tuple[float | None, int | None]:
    """Minimise (2.3) over L for fixed (n, d, k). Returns (log2 bound, best L)."""
    best, bestL = None, None
    for L in range(k, n - k + 1):
        lb = log2_bound(n, d, k, L)
        if lb is not None and (best is None or lb < best):
            best, bestL = lb, L
    return best, bestL


if __name__ == "__main__":
    # The worked example of Section 2.2: n = 8, k = 1, L = 7, even-weight code d = 2.
    n, k, L, d = 8, 1, 7, 2
    lam = perron(n, k, L)
    print(f"n={n} k={k} L={L}: Perron eigenvalue = {lam:.6f}   (paper: 0.569289)")
    print(f"bound (2.3) for d={d}: {bound(n, d, k, L):.3f}   (paper: 261.843)")
    # The 'wrong' recurrence of Section 2.2: c~_j = sqrt((j-k+1)(n-j-k))/n
    j = np.arange(k, L, dtype=float)
    off_wrong = np.sqrt((j - k + 1) * (n - j - k)) / n
    w = eigh_tridiagonal(np.zeros(L - k + 1), off_wrong, eigvals_only=True)
    lam_wrong = w[-1]
    s = 1 - 2 * d / n
    D = sum(math.comb(n, jj) for jj in range(k, L + 1))
    mk = math.comb(n, k) - math.comb(n, k - 1)
    print(f"wrong recurrence: Perron = {lam_wrong:.6f} (paper: 3/4), bound = {(1-s)/(lam_wrong-s)*D/mk:.4f} (paper: 508/7 = {508/7:.4f})")
