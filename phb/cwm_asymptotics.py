r"""
Asymptotics of the m-row layer graphs (general m; m = 3 reproduces phb/cw2_asymptotics.py).

Normalised labels: ell = lambda/n (m entries, sum 1), alpha = w/n, om = eps/n (m-1 entries, sum alpha, padded with 0).
Interlacing: ell_m <= om_{m-1} <= ell_{m-1} <= ... <= om_1 <= ell_1.
    Rtilde_t(r) = prod_{k!=r}|om_t - ell_k| prod_{k!=t, k!=m}|ell_r - om_k| / (prod_{k!=t}|om_t - om_k| prod_{k!=r}|ell_r - ell_k|)
    p_{r->r'}   = (alpha/(1-alpha)) ell_r tautilde^2,
    tautilde    = sum_t sigma_t (om_t/alpha) sqrt(Rtilde_t(r) Rtilde_t(r')),   sigma_t = (-1)^{[r<=t]+[r'<=t]}
    Lambda      = 1 - sum_{r<r'} (sqrt p_{r->r'} - sqrt p_{r'->r})^2
    F           = 1 - H2(alpha) + H(ell) - alpha H(om/alpha),   feasible iff Lambda > 1 - delta/(2 alpha (1-alpha)).
"""
from __future__ import annotations
import math
import numpy as np


def H2(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -x * math.log2(x) - (1 - x) * math.log2(1 - x)


def H(v):
    return -sum(x * math.log2(x) for x in v if x > 0)


def Rtilde(ell, om, r, t, m):
    r0, t0 = r - 1, t - 1
    num = 1.0; den = 1.0
    for k in range(m):
        if k != r0:
            num *= abs(om[t0] - ell[k]); den *= abs(ell[r0] - ell[k])
        if k != t0 and k != m - 1:
            num *= abs(ell[r0] - om[k])
        if k != t0:
            den *= abs(om[t0] - om[k])
    return num / den if den > 0 else float("nan")


def p_inf(ell, alpha, om, r, rp, m):
    tau = 0.0
    for t in range(1, m):
        if om[t - 1] <= 0:
            continue
        s = (-1) ** ((r <= t) + (rp <= t))
        tau += s * (om[t - 1] / alpha) * math.sqrt(Rtilde(ell, om, r, t, m) * Rtilde(ell, om, rp, t, m))
    return (alpha / (1 - alpha)) * ell[r - 1] * tau * tau


def moves(ell, alpha, om, m):
    return {(r, rp): p_inf(ell, alpha, om, r, rp, m) for r in range(1, m + 1) for rp in range(1, m + 1) if r != rp}


def Lambda(ell, alpha, om, m):
    P = moves(ell, alpha, om, m)
    return 1.0 - sum((math.sqrt(P[(r, rp)]) - math.sqrt(P[(rp, r)])) ** 2 for r in range(1, m + 1) for rp in range(r + 1, m + 1))


def threshold(delta, alpha):
    return 1 - delta / (2 * alpha * (1 - alpha))


def F(ell, alpha, om):
    return 1 - H2(alpha) + H(ell) - alpha * H([x / alpha for x in om])


def sig(x):
    x = max(-60.0, min(60.0, x))
    return 1.0 / (1.0 + math.exp(-x))


def unpack(z, delta, m):
    """z has 1 + (m-1) + (m-1) entries: alpha; gaps of om; interlacing fractions of ell_2..ell_m."""
    a = delta / 2 + (0.5 - delta / 2) * sig(z[0])
    u = [math.exp(max(-60.0, min(60.0, z[1 + j]))) for j in range(m - 1)]          # gap weights g_j ~ u_j
    tot = sum((j + 1) * u[j] for j in range(m - 1))
    g = [a * u[j] / tot for j in range(m - 1)]                                       # g_1..g_{m-1}, om_k = sum_{j>=k} g_j
    om = [sum(g[k - 1:]) for k in range(1, m)] + [0.0]
    s = [sig(z[m + j]) for j in range(m - 1)]                                        # fractions for ell_2..ell_m
    ell = [0.0] * m
    ell[m - 1] = om[m - 2] * s[m - 2]
    for k in range(2, m):
        ell[k - 1] = om[k - 1] + (om[k - 2] - om[k - 1]) * s[k - 2]
    ell[0] = 1 - sum(ell[1:])
    return tuple(ell), a, tuple(om[:-1])


def penalised(z, delta, m, pen=50.0):
    ell, a, om = unpack(z, delta, m)
    viol = max(0.0, om[0] - ell[0])
    if viol > 0 or a >= 0.5 - 1e-12:
        return F(ell, a, om) + pen * viol + 1.0 + pen
    omp = tuple(om) + (0.0,)
    # strict interior for the formula's denominators
    if any(omp[k] <= omp[k + 1] + 1e-12 for k in range(m - 1)) or any(ell[k] <= ell[k + 1] + 1e-12 for k in range(m - 1)) or ell[m - 1] <= 1e-14:
        return F(ell, a, om) + pen + 1.0
    g = Lambda(ell, a, omp, m) - threshold(delta, a)
    if not math.isfinite(g):
        return F(ell, a, om) + pen + 1.0
    return F(ell, a, om) + pen * max(0.0, -g)


def kappa_m(delta, m, n_starts=60, seed=0, starts_extra=()):
    from scipy.optimize import minimize
    rng = np.random.default_rng(seed)
    starts = list(starts_extra)
    for _ in range(n_starts):
        z = np.concatenate([[rng.normal(0, 1.5)], rng.uniform(-8, 2, m - 1), rng.uniform(-10, 2, m - 1)])
        starts.append(z)
    best = (math.inf, None)
    for z in starts:
        res = minimize(penalised, z, args=(delta, m), method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-13, "maxiter": 8000})
        if res.fun < best[0]:
            best = (res.fun, res.x)
    z = best[1]
    ell, a, om = unpack(z, delta, m)
    return F(ell, a, om), ell, a, om, Lambda(ell, a, tuple(om) + (0.0,), m) - threshold(delta, a), z


def z_from(delta, a, om, ell, m):
    """Inverse of unpack (for seeding)."""
    inv = lambda s: math.log(min(max(s, 1e-12), 1 - 1e-12) / (1 - min(max(s, 1e-12), 1 - 1e-12)))
    z = [inv((a - delta / 2) / (0.5 - delta / 2))]
    omp = list(om) + [0.0]
    g = [omp[j] - omp[j + 1] for j in range(m - 1)]
    tot = sum((j + 1) * g[j] for j in range(m - 1))
    z += [math.log(max(g[j] / tot, 1e-300)) for j in range(m - 1)]
    s = []
    for k in range(2, m):
        s.append((ell[k - 1] - omp[k - 1]) / max(omp[k - 2] - omp[k - 1], 1e-300))
    s.append(ell[m - 1] / max(omp[m - 2], 1e-300))
    z += [inv(x) for x in s]
    return np.array(z)
