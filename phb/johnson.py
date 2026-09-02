"""
Constant-weight (Johnson-layer) primitive-harmonic bound.

Transcribed from "Ten Advances", Chapter 2, Section 3 (Theorem 3.4, eqs. (35)-(37), (43)-(46)), and
the asymptotic threshold (6)-(8) with Lemma 3.5 / Theorem 3.6.

Parameters: n, w (1 <= w < n/2), N = n - w, harmonic degrees 0 <= p <= w/2 on the support and
0 <= q <= N/2 on the complement, retained Johnson degrees j = p+q .. L with
    p + q < L <= min{ w, w - p + q, N + p - q }.
Associated Hahn parameters (35):
    j1 = w/2 - p,  j2 = N/2 - q,  jj = n/2 - j,  m0 = n/2 - w,  S = j1 + j2,  Dl = j2 - j1.
(36)-(37):
    mu_j  = (m0/2) (j2(j2+1) - j1(j1+1)) / (jj(jj+1))
    nu_j  = sqrt((jj^2 - m0^2)(jj^2 - Dl^2)((S+1)^2 - jj^2)) / (2 jj sqrt((2jj-1)(2jj+1)))
    b_j^{p,q} = (n mu_j - m0^2)/(wN),      c_j^{p,q} = n nu_j/(wN)
Symmetric Johnson matrix (43)-(44), indices j = p+q..L:
    Jhat[j,j]   = (b_j^{p,q})^2 / b_j^0   (j >= 1; 0 if j = 0)
    Jhat[j,j+1] = (c_j^{p,q})^2 / c_j^0
Theorem 3.4 (46): for even d with 2 <= d <= 2w, s = 1 - n d /(2 w N), lambda = lambda_max(Jhat):
    if lambda > s:  A_J(n,w,d) <= (1-s)/(lambda-s) * sum_{j=p+q}^{L} D_j / ( d_p(w) d_q(N) ),
    D_j = C(n,j) - C(n,j-1),  d_p(w) = C(w,p) - C(w,p-1).
Bassalygo-Elias (29):  A_2(n,d) <= 2^n / C(n,w) * A_J(n,w,d).
"""
from __future__ import annotations

import math

import numpy as np
from scipy.linalg import eigh_tridiagonal

from .bound import log2_binom


def hahn_bc(n: int, w: int, p: int, q: int, j: int) -> tuple[float, float]:
    """(b_j^{p,q}, c_j^{p,q}) from (35)-(37). c_j is meaningful for j < j_plus only."""
    N = n - w
    j1 = w / 2 - p
    j2 = N / 2 - q
    jj = n / 2 - j
    m0 = n / 2 - w
    S = j1 + j2
    Dl = j2 - j1
    mu = (m0 / 2) * (j2 * (j2 + 1) - j1 * (j1 + 1)) / (jj * (jj + 1))
    rad = (jj * jj - m0 * m0) * (jj * jj - Dl * Dl) * ((S + 1) ** 2 - jj * jj)
    if rad <= 0 or 2 * jj - 1 <= 0:
        nu = 0.0
    else:
        nu = math.sqrt(rad) / (2 * jj * math.sqrt((2 * jj - 1) * (2 * jj + 1)))
    b = (n * mu - m0 * m0) / (w * N)
    c = n * nu / (w * N)
    return b, c


def j_plus(n: int, w: int, p: int, q: int) -> int:
    return min(w, w - p + q, n - w + p - q)


def jhat(n: int, w: int, p: int, q: int, L: int) -> tuple[np.ndarray, np.ndarray]:
    """Diagonal and off-diagonal of the symmetric Johnson matrix (43)-(44) on degrees p+q..L."""
    jm = p + q
    if not (1 <= w < n / 2 and 0 <= p <= w / 2 and 0 <= q <= (n - w) / 2 and jm < L <= j_plus(n, w, p, q)):
        raise ValueError(f"bad parameters n={n} w={w} p={p} q={q} L={L}")
    diag = np.zeros(L - jm + 1)
    off = np.zeros(L - jm)
    for idx, j in enumerate(range(jm, L + 1)):
        b, c = hahn_bc(n, w, p, q, j)
        b0, c0 = hahn_bc(n, w, 0, 0, j)
        diag[idx] = 0.0 if j == 0 else b * b / b0
        if j < L:
            off[idx] = c * c / c0
    return diag, off


def lambda_max(n: int, w: int, p: int, q: int, L: int) -> float:
    diag, off = jhat(n, w, p, q, L)
    if diag.size == 1:
        return float(diag[0])
    return float(eigh_tridiagonal(diag, off, eigvals_only=True, select="i", select_range=(diag.size - 1, diag.size - 1))[0])


def perron_vector(n: int, w: int, p: int, q: int, L: int):
    diag, off = jhat(n, w, p, q, L)
    wv, v = eigh_tridiagonal(diag, off, select="i", select_range=(diag.size - 1, diag.size - 1))
    vec = v[:, 0]
    if vec.sum() < 0:
        vec = -vec
    return float(wv[0]), vec


def log2_Dsum(n: int, jm: int, L: int) -> float:
    """log2 sum_{j=jm}^{L} (C(n,j) - C(n,j-1)) = log2 (C(n,L) - C(n,jm-1))  (telescoping)."""
    a = log2_binom(n, L)
    b = log2_binom(n, jm - 1) if jm >= 1 else -math.inf
    return a + math.log2(1.0 - 2.0 ** (b - a)) if b > -math.inf else a


def log2_dp(m: int, p: int) -> float:
    if p == 0:
        return 0.0
    a = log2_binom(m, p)
    b = log2_binom(m, p - 1)
    return a + math.log2(1.0 - 2.0 ** (b - a))


def log2_bound_J(n: int, w: int, d: int, p: int, q: int, L: int) -> float | None:
    """log2 of the constant-weight bound (46); None if infeasible (lambda <= s)."""
    if d % 2 or not (2 <= d <= 2 * w):
        raise ValueError("d must be even with 2 <= d <= 2w")
    N = n - w
    s = 1.0 - n * d / (2.0 * w * N)
    lam = lambda_max(n, w, p, q, L)
    if lam <= s:
        return None
    return math.log2((1 - s) / (lam - s)) + log2_Dsum(n, p + q, L) - log2_dp(w, p) - log2_dp(N, q)


def log2_bound_BE(n: int, w: int, d: int, p: int, q: int, L: int) -> float | None:
    """Bassalygo-Elias transfer of (46) to unrestricted codes: log2 A_2(n,d) bound."""
    lb = log2_bound_J(n, w, d, p, q, L)
    return None if lb is None else lb + n - log2_binom(n, w)


# ----------------------------------------------------------------------------------------------
# Asymptotics: (6)-(8)
# ----------------------------------------------------------------------------------------------
def H2(x: float) -> float:
    if x <= 0 or x >= 1:
        return 0.0
    return float(-x * math.log2(x) - (1 - x) * math.log2(1 - x))


def Lambda(alpha: float, beta: float, gamma: float, u: float) -> float:
    z = 1 - 2 * u
    m = 1 - 2 * alpha
    zeta = 1 - 2 * beta - 2 * gamma
    xi = 1 - 2 * alpha + 2 * beta - 2 * gamma
    z2, m2 = z * z, m * m
    B = (zeta * xi - m * z2) ** 2 / (z2 * (1 - m2) * (1 - z2))
    C2 = (z2 - xi * xi) * (zeta * zeta - z2) / (z2 * (1 - m2) * math.sqrt(1 - z2))
    return B + C2


def cw_threshold(delta: float, alpha: float) -> float:
    return 1 - delta / (2 * alpha * (1 - alpha))


def u_range(alpha, beta, gamma):
    return beta + gamma, min(alpha, alpha - beta + gamma, 1 - alpha + beta - gamma)


def u_min(delta, alpha, beta, gamma, grid=400):
    """Smallest u in the admissible range with Lambda(u) > threshold; None if infeasible."""
    lo, hi = u_range(alpha, beta, gamma)
    if not (hi > lo):
        return None
    thr = cw_threshold(delta, alpha)
    us = np.linspace(lo, hi, grid + 2)[1:-1]
    feas = [Lambda(alpha, beta, gamma, u) > thr for u in us]
    if not any(feas):
        return None
    i = feas.index(True)
    a = us[i - 1] if i > 0 else lo
    b = us[i]
    for _ in range(60):
        mid = (a + b) / 2
        if Lambda(alpha, beta, gamma, mid) > thr:
            b = mid
        else:
            a = mid
    return b


def cw_rate(delta, alpha, beta, gamma):
    u = u_min(delta, alpha, beta, gamma)
    if u is None:
        return None, None
    val = 1 - H2(alpha) + H2(u) - alpha * H2(beta / alpha) - (1 - alpha) * H2(gamma / (1 - alpha))
    return val, u


def kappa_CW(delta: float, n_starts: int = 24, seed: int = 0):
    """Numerically minimise (8). Returns (value, alpha, beta, gamma, u)."""
    from scipy.optimize import minimize
    rng = np.random.default_rng(seed)

    def unpack(x):
        a = delta / 2 + (0.5 - delta / 2) / (1 + math.exp(-x[0]))   # alpha in (delta/2, 1/2)
        b = (a / 2) * math.exp(-abs(x[1]))                          # beta in (0, alpha/2]
        g = ((1 - a) / 2) * math.exp(-abs(x[2]))                    # gamma in (0, (1-alpha)/2]
        return a, b, g

    def obj(x):
        a, b, g = unpack(x)
        val, _ = cw_rate(delta, a, b, g)
        return 10.0 if val is None else val

    best = (math.inf, None)
    # classical starting point: beta=gamma=0 minimiser of M2 (u along the spectral boundary)
    starts = [np.array([0.0, 6.0, 6.0])]
    for _ in range(n_starts):
        starts.append(np.array([rng.normal(0, 1.5), rng.uniform(2, 9), rng.uniform(2, 9)]))
    for x0 in starts:
        r = minimize(obj, x0, method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-12, "maxiter": 4000})
        if r.fun < best[0]:
            best = (r.fun, r.x)
    a, b, g = unpack(best[1])
    val, u = cw_rate(delta, a, b, g)
    return val, a, b, g, u


def M2(delta: float) -> float:
    from scipy.optimize import minimize_scalar
    g = lambda z: H2((1 - math.sqrt(max(0.0, 1 - z))) / 2)
    f = lambda t: 1 + g(t * t) - g(t * t + 2 * delta * t + 2 * delta)
    ts = np.linspace(0, 1 - 2 * delta, 4001)
    vals = [f(t) for t in ts]
    i = int(np.argmin(vals))
    lo, hi = ts[max(i - 1, 0)], ts[min(i + 1, len(ts) - 1)]
    if hi > lo:
        r = minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 1e-12})
        return min(r.fun, vals[i])
    return vals[i]
