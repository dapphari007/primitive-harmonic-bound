"""Asymptotic exponent of the binary two-row representation graph.
Normalised coordinates: u = j/n, at = a2/n, bt = b2/n, b = k/n;  A1 = 1-u-at, A2 = at, B1 = u-bt, B2 = bt.
Limiting directed coefficients: p = (row factor) * (X or Y) / N with
    X = (A2+B1-b)(A1+B2-b),  Y = (b-A2-B2)(1-A2-B2-b),  N = (A1-A2)(B1-B2)   (X + Y = N).
Symmetric limiting edge weights and the Perron limit (product-sine Rayleigh quotient on an o(n) box):
    Lambda = 2 [ X (sqrt(A1 B1) + sqrt(A2 B2)) + Y (sqrt(A1 B2) + sqrt(A2 B1)) ] / N.
Ambient dimension exponent  Phi_amb = H2(u) + (1-u) H2(at/(1-u)) + u H2(bt/u);  stabilizer H2(b).
Bound exponent Phi_amb - H2(b) whenever Lambda > s = 1 - 2 delta, inside the admissible region
    at + bt <= b <= min(A1+B2, A2+B1),  at <= (1-u)/2,  bt <= u/2.
At at = bt = 0 this is exactly the paper's whole-cube construction (Lambda = Gamma_H(u, b))."""
import math
import numpy as np
from scipy.optimize import minimize


def H2(x):
    if x <= 0 or x >= 1: return 0.0
    return -x * math.log2(x) - (1 - x) * math.log2(1 - x)


def Lambda(u, at, bt, b):
    A1, A2, B1, B2 = 1 - u - at, at, u - bt, bt
    if min(A1, B1) <= 0 or A1 < A2 or B1 < B2: return -1.0
    N = (A1 - A2) * (B1 - B2)
    if N <= 0: return -1.0
    X = (A2 + B1 - b) * (A1 + B2 - b)
    Y = (b - A2 - B2) * (1 - A2 - B2 - b)
    return 2 * (X * (math.sqrt(A1 * B1) + math.sqrt(A2 * B2)) + Y * (math.sqrt(A1 * B2) + math.sqrt(A2 * B1))) / N


def Phi_amb(u, at, bt):
    return H2(u) + (1 - u) * H2(at / (1 - u)) + u * H2(bt / u)


def admissible(u, at, bt, b):
    A1, A2, B1, B2 = 1 - u - at, at, u - bt, bt
    return (at >= 0 and bt >= 0 and A1 >= A2 and B1 >= B2 and at + bt <= b <= min(A1 + B2, A2 + B1) and b <= 0.5)


def best_b(u, at, bt, s, grid=100):
    """Largest admissible b with Lambda(u,at,bt,b) >= s (Phi decreases in b). None if none."""
    lo, hi = at + bt, min(1 - u - at + bt, at + u - bt, 0.5)
    if hi <= lo: return None
    bs = np.linspace(lo, hi, grid)
    feas = [Lambda(u, at, bt, x) >= s for x in bs]
    if not any(feas): return None
    i = max(i for i, f in enumerate(feas) if f)
    a, c = bs[i], (bs[i + 1] if i + 1 < grid else hi)
    for _ in range(60):
        m = (a + c) / 2
        if Lambda(u, at, bt, m) >= s: a = m
        else: c = m
    return a


def rate(u, at, bt, s):
    b = best_b(u, at, bt, s)
    if b is None: return None, None
    return Phi_amb(u, at, bt) - H2(b), b


def kappa_H(delta):
    """Paper's whole-cube exponent (at = bt = 0), 1-D in u."""
    s = 1 - 2 * delta
    best = (math.inf, None)
    for u in np.concatenate([np.geomspace(1e-4, 0.005, 200), np.linspace(0.005, 0.5, 2000)]):
        r, b = rate(u, 0.0, 0.0, s)
        if r is not None and r < best[0]: best = (r, (u, 0.0, 0.0, b))
    u0 = best[1][0]
    from scipy.optimize import minimize_scalar
    f = lambda u: (rate(u, 0.0, 0.0, s)[0] or 10.0) if 0 < u < 0.5 else 10.0
    res = minimize_scalar(f, bounds=(max(1e-5, u0 * 0.7), min(0.499, u0 * 1.3 + 1e-4)), method="bounded", options={"xatol": 1e-10})
    if res.fun < best[0]: best = (res.fun, (res.x, 0.0, 0.0, best_b(res.x, 0.0, 0.0, s)))
    return best


def kappa_2row(delta, n_starts=40, seed=0):
    """inf over (u, at, bt) of Phi_amb - H2(b_max)."""
    s = 1 - 2 * delta
    rng = np.random.default_rng(seed)
    kH, (u0, _, _, b0) = kappa_H(delta)
    def unpack(z):
        u = 0.5 / (1 + math.exp(-z[0]))
        at = (1 - u) / 2 * math.exp(-abs(z[1]))
        bt = u / 2 * math.exp(-abs(z[2]))
        return u, at, bt
    def obj(z):
        u, at, bt = unpack(z)
        r, b = rate(u, at, bt, s)
        return 10.0 if r is None else r
    starts = []
    u0 = min(max(u0, 0.001), 0.495)
    z0u = math.log(u0 / (0.5 - u0))
    for la in [2, 5, 8]:
        for lb in [2, 5, 8]:
            starts.append(np.array([z0u, la, lb]))
    for _ in range(n_starts):
        starts.append(np.array([z0u + rng.normal(0, 0.5), rng.uniform(1, 12), rng.uniform(1, 12)]))
    best = (math.inf, None)
    for z in starts:
        res = minimize(obj, z, method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-12, "maxiter": 3000})
        if res.fun < best[0]: best = (res.fun, res.x)
    u, at, bt = unpack(best[1]); r, b = rate(u, at, bt, s)
    return r, (u, at, bt, b), kH, (u0, b0)
