"""
Spherical codes: the moving-harmonic (representation-graph) bounds of "Ten Advances", Ch. 2, Sections 4-8.

Finite bounds (Theorem 6.2, eq. (80)):  A(n, s) <= (1-s) / (d_mu (Lambda - s)) * sum_{lambda in Omega} D_lambda,
Lambda = lambda_max of the symmetric weighted adjacency matrix J_Omega, whenever Lambda > s.

One-row path (stabilizer mu = (k), ambient harmonic degrees i = k..L), eq. (73):
    c_i^{(k)} = (i-k+1)(i+k+n-2) / sqrt((i+1)(i+n-2)(2i+n-2)(2i+n)),
    D_i^S = (2i+n-2)/(n-2) * C(i+n-3, i),   d_k^S = C(n+k-2, k) - C(n+k-4, k-2).
Two-row graph (ambient (i, j), i >= k >= j >= 0), directed squared coefficients (81), symmetric
edge weights (79) J = sqrt(p_+ p_-), dimensions D_{i,j} (Section 6.1).
General transition formula (76) with shifted weights (75), for any r (n >= 2r+4).

Asymptotics (Section 7): H_sph(u) = (1+u) log2(1+u) - u log2 u, A(u) = u(1+u), q(u) = sqrt(u(1+u))/(1+2u),
level-r tuples a_1 > b_1 > ... > b_r > a_{r+1} >= 0, residues R_l, Gamma_r = sum R_l q(a_l),
Phi_r = sum H_sph(a_l) - sum H_sph(b_m); kappa_r(s) = inf Phi_r s.t. 2 Gamma_r >= s; cap optimisation (89);
packing exponents gamma_r (93); threshold lambda_* = (1/2) log2(2 pi / e) (96); Chebyshev tuples (106).
"""
from __future__ import annotations

import math
from functools import lru_cache

import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import minimize
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh


# ------------------------------------------------------------------ dimensions
def log2_binom(n: int, k: int) -> float:
    if k < 0 or k > n:
        return -math.inf
    return (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)) / math.log(2)


def DS(n: int, i: int) -> float:
    """dim H_i(R^n) restricted to the sphere, eq. (61)."""
    return (2 * i + n - 2) / (n - 2) * math.comb(i + n - 3, i)


def log2_DS(n: int, i: int) -> float:
    return math.log2((2 * i + n - 2) / (n - 2)) + log2_binom(i + n - 3, i)


def dS(n: int, k: int) -> float:
    """dim H_k(x^perp), eq. (63)."""
    return math.comb(n + k - 2, k) - (math.comb(n + k - 4, k - 2) if k >= 2 else 0)


def log2_dS(n: int, k: int) -> float:
    if k == 0:
        return 0.0
    a = log2_binom(n + k - 2, k)
    b = log2_binom(n + k - 4, k - 2) if k >= 2 else -math.inf
    return a + math.log2(1 - 2.0 ** (b - a)) if b > -math.inf else a


def D2(n: int, i: int, j: int) -> float:
    """dim V_(i,j), Section 6.1 (Weyl formula specialised to two rows)."""
    return ((2 * i + n - 2) * (2 * j + n - 4) * (i - j + 1) * (i + j + n - 3)
            / ((n - 2) * (n - 4) * (i + 1) * (i + n - 3)) * math.comb(i + n - 3, i) * math.comb(j + n - 5, j))


def log2_D2(n: int, i: int, j: int) -> float:
    """log2 dim V_(i,j), overflow-safe."""
    return (math.log2((2 * i + n - 2) * (2 * j + n - 4) * (i - j + 1) * (i + j + n - 3))
            - math.log2((n - 2) * (n - 4) * (i + 1) * (i + n - 3)) + log2_binom(i + n - 3, i) + log2_binom(j + n - 5, j))


# ------------------------------------------------------------------ one-row path
def path_weights(n: int, k: int, L: int) -> np.ndarray:
    i = np.arange(k, L, dtype=float)
    return (i - k + 1) * (i + k + n - 2) / np.sqrt((i + 1) * (i + n - 2) * (2 * i + n - 2) * (2 * i + n))


def lambda_row(n: int, k: int, L: int) -> float:
    if L == k:
        return 0.0
    off = path_weights(n, k, L)
    m = L - k + 1
    return float(eigh_tridiagonal(np.zeros(m), off, eigvals_only=True, select="i", select_range=(m - 1, m - 1))[0])


def log2_bound_row(n: int, s: float, k: int, L: int) -> float | None:
    lam = lambda_row(n, k, L)
    if lam <= s:
        return None
    terms = [log2_DS(n, i) for i in range(k, L + 1)]
    mx = max(terms)
    lsum = mx + math.log2(sum(2.0 ** (t - mx) for t in terms))
    return math.log2((1 - s) / (lam - s)) + lsum - log2_dS(n, k)


# ------------------------------------------------------------------ two-row graph (81)
def p2(n: int, k: int, i: int, j: int):
    """Directed squared coefficients (p_{i,+}, p_{i,-}, p_{j,+}, p_{j,-}) at ambient (i,j), stabilizer (k)."""
    den_i = (i - j + 1) * (i + j + n - 3) * (2 * i + n - 2)
    den_j = (i - j + 1) * (i + j + n - 3) * (2 * j + n - 4)
    pip = (i - k + 1) * (i + k + n - 2) * (i + n - 3) / den_i
    pim = (i - k) * (i + k + n - 3) * (i + 1) / den_i
    pjp = (k - j) * (j + k + n - 3) * (j + n - 4) / den_j
    pjm = j * (k - j + 1) * (j + k + n - 4) / den_j
    return pip, pim, pjp, pjm


def two_row_matrix(n: int, k: int, I: int, J: int):
    """Symmetric weighted adjacency on the box k <= i <= I, 0 <= j <= min(J, k); returns (matrix, vertices)."""
    J = min(J, k)
    verts = [(i, j) for i in range(k, I + 1) for j in range(0, J + 1)]
    idx = {v: a for a, v in enumerate(verts)}
    M = lil_matrix((len(verts), len(verts)))
    for (i, j), a in idx.items():
        pip, pim, pjp, pjm = p2(n, k, i, j)
        if (i + 1, j) in idx:
            w = math.sqrt(pip * p2(n, k, i + 1, j)[1])
            M[a, idx[(i + 1, j)]] = w; M[idx[(i + 1, j)], a] = w
        if (i, j + 1) in idx:
            w = math.sqrt(pjp * p2(n, k, i, j + 1)[3])
            M[a, idx[(i, j + 1)]] = w; M[idx[(i, j + 1)], a] = w
    return M.tocsr(), verts


def lambda_two_row(n: int, k: int, I: int, J: int) -> float:
    M, verts = two_row_matrix(n, k, I, J)
    if M.shape[0] <= 2:
        return float(np.linalg.eigvalsh(M.toarray())[-1])
    return float(eigsh(M, k=1, which="LA", return_eigenvectors=False)[0])


def log2_bound_two_row(n: int, s: float, k: int, I: int, J: int) -> float | None:
    lam = lambda_two_row(n, k, I, J)
    if lam <= s:
        return None
    J = min(J, k)
    terms = [log2_D2(n, i, j) for i in range(k, I + 1) for j in range(0, J + 1)]
    mx = max(terms)
    lsum = mx + math.log2(sum(2.0 ** (t - mx) for t in terms))
    return math.log2((1 - s) / (lam - s)) + lsum - log2_dS(n, k)


def weyl_dim(n: int, r: int, lam) -> float:
    """dim V_lambda for a dominant weight with at most r+1 nonzero rows, eq. (113) (zero-tail specialisation)."""
    lam = list(lam) + [0] * (r + 1 - len(lam))
    val = 1.0
    for i in range(1, r + 2):
        li = lam[i - 1]
        val *= (2 * li + n - 2 * i) / (n - 2 * i)
        val *= math.exp(math.lgamma(li + n - i - r - 2 + 1) - math.lgamma(n - i - r - 2 + 1))
        val *= math.exp(math.lgamma(r + 1 - i + 1) - math.lgamma(li + r + 1 - i + 1))
    for i in range(1, r + 2):
        for j in range(i + 1, r + 2):
            li, lj = lam[i - 1], lam[j - 1]
            val *= (li - lj + j - i) * (li + lj + n - i - j) / ((j - i) * (n - i - j))
    return val


# ------------------------------------------------------------------ general transition formula (76)
def p_general(n: int, r: int, lam: tuple, mu: tuple, ell: int, sign: int) -> float:
    """p_{ell,+/-}(lambda; mu), eq. (76); ell is 1-based; returns 0 if the target weight is not admissible."""
    lam = list(lam) + [0] * (r + 1 - len(lam))
    mu = list(mu) + [0] * (r - len(mu))
    tgt = lam.copy()
    tgt[ell - 1] += sign
    # dominance and interlacing lambda_1 >= mu_1 >= lambda_2 >= ... >= mu_r >= lambda_{r+1} >= 0
    if any(tgt[a] < tgt[a + 1] for a in range(r)) or tgt[-1] < 0:
        return 0.0
    for m in range(r):
        if not (tgt[m] >= mu[m] >= tgt[m + 1]):
            return 0.0
    lh = [lam[a] + n / 2 - (a + 1) for a in range(r + 1)]
    mh = [mu[m] + (n - 1) / 2 - (m + 1) for m in range(r)]
    rho = n / 2 - r - 1
    L = lh[ell - 1]
    num = (L + sign * rho)
    for m in range(r):
        num *= (L + sign * 0.5) ** 2 - mh[m] ** 2
    den = 2 * L
    for q in range(r + 1):
        if q != ell - 1:
            den *= L ** 2 - lh[q] ** 2
    return num / den


# ------------------------------------------------------------------ asymptotics
def Hsph(u: float) -> float:
    if u <= 0:
        return 0.0
    return (1 + u) * math.log2(1 + u) - u * math.log2(u)


def Aq(u: float) -> float:
    return u * (1 + u)


def Ainv(x: float) -> float:
    return (math.sqrt(1 + 4 * x) - 1) / 2


def q(u: float) -> float:
    return math.sqrt(u * (1 + u)) / (1 + 2 * u) if u > 0 else 0.0


def a0(s: float) -> float:
    return ((1 - s * s) ** -0.5 - 1) / 2


def BKL(s: float) -> float:
    """Cap-optimised Kabatianskii-Levenshtein exponent (10)."""
    f = lambda t: Hsph(a0(t)) + 0.5 * math.log2((1 - t) / (1 - s))
    ts = np.linspace(0, s, 4001)
    v = [f(t) for t in ts]
    i = int(np.argmin(v))
    from scipy.optimize import minimize_scalar
    lo, hi = ts[max(i - 1, 0)], ts[min(i + 1, len(ts) - 1)]
    r = minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 1e-12})
    return min(r.fun, v[i])


def residues(xs, ys):
    """R_l = prod_m (x_l - y_m) / prod_{q != l} (x_l - x_q), computed in log space (all positive under strict interlacing)."""
    R = []
    for l, x in enumerate(xs):
        lognum = sum(math.log(abs(x - y)) for y in ys)
        logden = sum(math.log(abs(x - xq)) for qq, xq in enumerate(xs) if qq != l)
        sign = (-1) ** (sum(1 for y in ys if x - y < 0) + sum(1 for qq, xq in enumerate(xs) if qq != l and x - xq < 0))
        R.append(sign * math.exp(lognum - logden))
    return np.array(R)


def gamma_phi(a: np.ndarray, b: np.ndarray):
    """(Gamma_r, Phi_r) for a level-r tuple a (r+1 entries) and b (r entries), eq. (83)."""
    xs = [Aq(v) for v in a]
    ys = [Aq(v) for v in b]
    R = residues(xs, ys)
    G = float(sum(R[l] * q(a[l]) for l in range(len(a))))
    P = float(sum(Hsph(v) for v in a) - sum(Hsph(v) for v in b))
    return G, P


def tuple_from_increments(z: np.ndarray, r: int, zero_tail: bool = False):
    """Strictly interlacing a_1 > b_1 > ... > b_r > a_{r+1} >= 0 from 2r+1 (or 2r) log-increments."""
    vals = []
    cur = 0.0 if zero_tail else math.exp(z[0])
    vals.append(cur)
    for t in (z[1:] if not zero_tail else z):
        cur = cur + math.exp(t)
        vals.append(cur)
    vals = vals[::-1]  # descending: a_1, b_1, a_2, ..., b_r, a_{r+1}
    a = np.array(vals[0::2])
    b = np.array(vals[1::2])
    return a, b


A_MAX = 60.0      # coordinates beyond this are never optimal (the optimising angles are moderate) and only
                  # expose floating-point breakdown of the residues; treat them as infeasible.
MIN_GAP = 1e-7    # minimum relative separation between consecutive interlacing nodes


def valid_tuple(a, b) -> bool:
    seq = np.zeros(len(a) + len(b)); seq[0::2] = a; seq[1::2] = b
    if seq[0] > A_MAX or np.any(~np.isfinite(seq)):
        return False
    gaps = seq[:-1] - seq[1:]
    return bool(np.all(gaps > MIN_GAP * max(1.0, seq[0])))


def packing_objective(a, b):
    if not valid_tuple(a, b):
        return -math.inf
    G, P = gamma_phi(a, b)
    if not (2 * G < 1 - 1e-10):
        return -math.inf
    return 0.5 * math.log2(2 / (1 - 2 * G)) - P


def gamma_r(r: int, n_starts: int = 40, seed: int = 0, zero_tail: bool = False):
    """sup over level-r tuples of the packing objective (93). Returns (value, a, b)."""
    rng = np.random.default_rng(seed)
    dim = 2 * r + (0 if zero_tail else 1)
    best = (-math.inf, None)
    starts = []
    # Chebyshev-type starts at several scales R
    for Rr in [0.3, 1.0, 3.0, 10.0, 30.0]:
        N = r + 1
        xs = [Rr / 2 * (1 + math.cos((2 * l - 1) * math.pi / (2 * N))) for l in range(1, N + 1)]
        ys = [Rr / 2 * (1 + math.cos(m * math.pi / N)) for m in range(1, N)]
        a = np.array([Ainv(x) for x in xs]); b = np.array([Ainv(y) for y in ys])
        vals = np.zeros(2 * r + 1); vals[0::2] = a; vals[1::2] = b
        asc = vals[::-1]
        if zero_tail:
            z = np.log(np.diff(np.concatenate([[0.0], asc[1:]])) + 1e-12)
        else:
            z = np.log(np.concatenate([[asc[0]], np.diff(asc)]) + 1e-12)
        starts.append(z)
    # one-row optimum (a, b) = (0.1056, 0.0050) extended by geometrically small extra nodes
    base = [0.1056, 0.0050]
    extra = [0.0050 * 0.5 ** (m + 1) for m in range(2 * r - 1)]
    asc = np.array(sorted(base + extra))
    if zero_tail:
        starts.append(np.log(np.diff(np.concatenate([[0.0], asc[1:]])) + 1e-12))
    else:
        starts.append(np.log(np.concatenate([[asc[0]], np.diff(asc)]) + 1e-12))
    for _ in range(n_starts):
        starts.append(rng.normal(-2.5, 1.2, dim))
    def obj(z):
        a, b = tuple_from_increments(z, r, zero_tail)
        v = packing_objective(a, b)
        return 10.0 if not math.isfinite(v) else -v
    for z0 in starts:
        res = minimize(obj, z0, method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-13, "maxiter": 20000, "maxfev": 40000})
        if -res.fun > best[0]:
            best = (-res.fun, res.x)
    a, b = tuple_from_increments(best[1], r, zero_tail)
    return best[0], a, b


def kappa_r(s: float, r: int, n_starts: int = 30, seed: int = 0):
    """inf Phi_r subject to 2 Gamma_r >= s over strictly interlacing level-r tuples (r >= 0).
    Shape/scale split: the scaling S_c on quadratic coordinates increases Gamma_r monotonically."""
    rng = np.random.default_rng(seed)
    if r == 0:
        return Hsph(a0(s)), np.array([a0(s)]), np.array([])
    dim = 2 * r  # shape parameters: 2r+1 nodes up to a common scale (the scale is fixed by the constraint)

    def shape(z):
        # quadratic coordinates ascending: x_{r+1} = 1 (scale), then 2r positive increments
        vals = [1.0]
        for t in z:
            vals.append(vals[-1] + math.exp(t))
        return np.array(vals[::-1])  # descending x_1 > y_1 > ... > y_r > x_{r+1}

    def phi_at_boundary(z):
        xy = shape(z)
        if xy[0] / xy[-1] > 1e7 or np.any(np.diff(xy) > -1e-9 * xy[0]):
            return 10.0
        # find c with 2 Gamma = s by bisection on log c
        def G_of(c):
            a = np.array([Ainv(c * v) for v in xy[0::2]]); b = np.array([Ainv(c * v) for v in xy[1::2]])
            return gamma_phi(a, b)
        lo, hi = 1e-8, 1e8
        if 2 * G_of(hi)[0] < s or Ainv(hi * xy[0]) > A_MAX and 2 * G_of(A_MAX * (1 + A_MAX) / xy[0])[0] < s:
            return 10.0
        for _ in range(80):
            mid = math.sqrt(lo * hi)
            if 2 * G_of(mid)[0] >= s:
                hi = mid
            else:
                lo = mid
        a = np.array([Ainv(hi * v) for v in xy[0::2]]); b = np.array([Ainv(hi * v) for v in xy[1::2]])
        if not valid_tuple(a, b):
            return 10.0
        return G_of(hi)[1]

    best = (math.inf, None)
    starts = [rng.normal(-1.0, 1.5, dim) for _ in range(n_starts)]
    for z0 in starts:
        res = minimize(phi_at_boundary, z0, method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-12, "maxiter": 20000, "maxfev": 40000})
        if res.fun < best[0]:
            best = (res.fun, res.x)
    xy = shape(best[1])
    # recover the tuple at the boundary scale
    lo, hi = 1e-8, 1e8
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        a = np.array([Ainv(mid * v) for v in xy[0::2]]); b = np.array([Ainv(mid * v) for v in xy[1::2]])
        if 2 * gamma_phi(a, b)[0] >= s:
            hi = mid
        else:
            lo = mid
    a = np.array([Ainv(hi * v) for v in xy[0::2]]); b = np.array([Ainv(hi * v) for v in xy[1::2]])
    return best[0], a, b


def kappa_row(s: float):
    """One-row optimised rate (90): inf H_sph(a) - H_sph(b) over a > b > 0 with 2 Gamma_row(a,b) >= s."""
    from scipy.optimize import minimize_scalar
    def Bs(a):  # spectral boundary b = B_s(a), Lemma 7.4
        val = 1 + 4 * a * (1 + a) - 2 * s * (1 + 2 * a) * math.sqrt(a * (1 + a))
        return (math.sqrt(max(val, 0.0)) - 1) / 2
    def f(a):
        b = Bs(a)
        if b <= 0 or b >= a:
            return 10.0
        return Hsph(a) - Hsph(b)
    lo = a0(s) * (1 + 1e-9)
    grid = np.geomspace(lo, 50 * lo + 5, 3000)
    v = [f(a) for a in grid]
    i = int(np.argmin(v))
    r = minimize_scalar(f, bounds=(grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]), method="bounded", options={"xatol": 1e-12})
    return min(r.fun, v[i])


LAMBDA_STAR = 0.5 * math.log2(2 * math.pi / math.e)


def chebyshev_tuple(N: int, R: float):
    xs = [R / 2 * (1 + math.cos((2 * l - 1) * math.pi / (2 * N))) for l in range(1, N + 1)]
    ys = [R / 2 * (1 + math.cos(m * math.pi / N)) for m in range(1, N)]
    return np.array([Ainv(x) for x in xs]), np.array([Ainv(y) for y in ys])
