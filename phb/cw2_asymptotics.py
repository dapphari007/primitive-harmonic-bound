r"""
Asymptotics of the CW2 (three-row constant-weight) representation graph.

Normalised labels: ell = (l1, l2, l3) = lambda/n (sum 1), alpha = w/n, beta = p/n, omega = eps/n = (alpha-beta, beta, 0).
Admissible (interlacing eps < lambda):  l3 <= beta <= l2 <= alpha - beta <= l1.
Limits of the closed forms (phb/cw2_formulas.py):
    Rbar_t(ell, r) = prod_{k!=r} |om_t - l_k| prod_{k!=t} |l_r - om_k| / (prod_{k!=t} |om_t - om_k| prod_{k!=r} |l_r - l_k|)
    tau(r, r')     = ((alpha-beta)/alpha) sqrt(Rbar_1(r) Rbar_1(r')) + (-1)^{r+r'} (beta/alpha) sqrt(Rbar_2(r) Rbar_2(r'))
    p_{r->r'}      = (alpha/(1-alpha)) tau(r,r')^2 / l_{r'}   (= (alpha/(1-alpha)) l_r tautilde^2 with the factor l_r l_r' of tau^2 cancelled)
    p_loop         = 1 - sum_{r != r'} p_{r->r'}
    Lambda         = p_loop + sum_{r != r'} sqrt(p_{r->r'} p_{r'->r}) = 1 - sum_{r<r'} (sqrt p_{r->r'} - sqrt p_{r'->r})^2
Bound exponent (binary codes via Bassalygo-Elias, S_N part trivial):
    F = 1 - H2(alpha) + H(ell) - alpha H2(beta/alpha)   whenever  Lambda(ell; alpha, beta) > 1 - delta / (2 alpha (1 - alpha)).
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


def Rtilde(ell, om, r, t):
    """Rbar_t(ell, r) with the factor |l_r - om_3| = l_r removed (so Rbar = l_r * Rtilde; smooth at l_r = 0)."""
    r0, t0 = r - 1, t - 1
    num = 1.0; den = 1.0
    for k in range(3):
        if k != r0:
            num *= abs(om[t0] - ell[k]); den *= abs(ell[r0] - ell[k])
        if k != t0 and k != 2:
            num *= abs(ell[r0] - om[k])
        if k != t0:
            den *= abs(om[t0] - om[k])
    return num / den if den > 0 else float("nan")


def Rbar(ell, om, r, t):
    return ell[r - 1] * Rtilde(ell, om, r, t)


def p_inf(ell, alpha, beta, r, rp):
    """Limit of p(lambda -> lambda - e_r + e_r'):  (alpha/(1-alpha)) l_r tautilde^2,
    tautilde = ((alpha-beta)/alpha) sqrt(Rt_1(r) Rt_1(r')) + (-1)^(r+r') (beta/alpha) sqrt(Rt_2(r) Rt_2(r'))."""
    om = (alpha - beta, beta, 0.0)
    tau = ((alpha - beta) / alpha) * math.sqrt(Rtilde(ell, om, r, 1) * Rtilde(ell, om, rp, 1))
    if beta > 0:
        tau += ((-1) ** (r + rp)) * (beta / alpha) * math.sqrt(Rtilde(ell, om, r, 2) * Rtilde(ell, om, rp, 2))
    return (alpha / (1 - alpha)) * ell[r - 1] * tau * tau


def admissible(ell, alpha, beta, tol=0.0):
    l1, l2, l3 = ell
    return (l3 >= -tol and beta >= l3 - tol and l2 >= beta - tol and alpha - beta >= l2 - tol and l1 >= alpha - beta - tol
            and l1 >= l2 >= l3 and beta >= 0)


def moves(ell, alpha, beta):
    P = {}
    for r in (1, 2, 3):
        for rp in (1, 2, 3):
            if r != rp:
                P[(r, rp)] = p_inf(ell, alpha, beta, r, rp)
    return P


def Lambda(ell, alpha, beta):
    P = moves(ell, alpha, beta)
    return 1.0 - sum((math.sqrt(P[(r, rp)]) - math.sqrt(P[(rp, r)])) ** 2 for r in (1, 2, 3) for rp in (1, 2, 3) if r < rp)


def threshold(delta, alpha):
    return 1 - delta / (2 * alpha * (1 - alpha))


def F(ell, alpha, beta):
    return 1 - H2(alpha) + H(ell) - alpha * H2(beta / alpha)


def sig(x):
    x = max(-60.0, min(60.0, x))
    return 1.0 / (1.0 + math.exp(-x))


def unpack(z, delta):
    a = delta / 2 + (0.5 - delta / 2) * sig(z[0])        # alpha in (delta/2, 1/2)
    b = (a / 2) * sig(z[1])                              # beta in (0, alpha/2)
    l3 = b * sig(z[2])                                   # l3 in (0, beta)
    l2 = b + (a - 2 * b) * sig(z[3])                     # l2 in (beta, alpha - beta)
    l1 = 1 - l2 - l3
    return (l1, l2, l3), a, b


def penalised(z, delta, pen=50.0):
    ell, a, b = unpack(z, delta)
    viol = max(0.0, (a - b) - ell[0])                    # need l1 >= alpha - beta
    if viol > 0:
        return F(ell, a, b) + pen * viol + 1.0
    if not (b < a / 2 - 1e-9 and ell[2] < b - 1e-12 and b < ell[1] < a - b - 1e-12 and a < 0.5 - 1e-12):
        return F(ell, a, b) + pen + 1.0
    g = Lambda(ell, a, b) - threshold(delta, a)
    if not math.isfinite(g):
        return F(ell, a, b) + pen + 1.0
    return F(ell, a, b) + pen * max(0.0, -g)


def kappa_CW2(delta, n_starts=60, seed=0, starts_extra=()):
    """inf of F subject to Lambda >= threshold, over alpha, beta, ell (three rows). Returns (value, ell, alpha, beta, Lambda-thr)."""
    from scipy.optimize import minimize
    rng = np.random.default_rng(seed)
    starts = list(starts_extra)
    for _ in range(n_starts):
        starts.append(np.array([rng.normal(0, 1.5), rng.uniform(-6, 0), rng.uniform(-8, 1), rng.uniform(-6, 2)]))
    best = (math.inf, None)
    for z in starts:
        res = minimize(penalised, z, args=(delta,), method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-13, "maxiter": 6000})
        if res.fun < best[0]:
            best = (res.fun, res.x)
    z = best[1]
    # polish with the explicit constraint
    def _g(z):
        ell_, a_, b_ = unpack(z, delta)
        v = Lambda(ell_, a_, b_) - threshold(delta, a_)
        return v if math.isfinite(v) else -1.0
    cons = [{"type": "ineq", "fun": _g},
            {"type": "ineq", "fun": lambda z: unpack(z, delta)[0][0] - (unpack(z, delta)[1] - unpack(z, delta)[2])}]
    try:
        res = minimize(lambda z: F(*unpack(z, delta)), z, method="SLSQP", constraints=cons, options={"ftol": 1e-14, "maxiter": 500})
        if res.success and all(c["fun"](res.x) >= -1e-10 for c in cons) and res.fun < best[0]:
            z = res.x
    except Exception:
        pass
    ell, a, b = unpack(z, delta)
    return F(ell, a, b), ell, a, b, Lambda(ell, a, b) - threshold(delta, a)


def kappa_CW2_tworow(delta, n_starts=60, seed=0):
    """Same optimisation restricted to l3 = 0 (must reproduce the paper's constant-weight exponent at gamma = 0)."""
    from scipy.optimize import minimize
    rng = np.random.default_rng(seed)
    def obj(z):
        zz = np.array([z[0], z[1], -60.0, z[2]])
        return penalised(zz, delta)
    best = (math.inf, None)
    for _ in range(n_starts):
        z0 = np.array([rng.normal(0, 1.5), rng.uniform(-6, 0), rng.uniform(-6, 2)])
        res = minimize(obj, z0, method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-13, "maxiter": 6000})
        if res.fun < best[0]:
            best = (res.fun, res.x)
    zz = np.array([best[1][0], best[1][1], -60.0, best[1][2]])
    ell, a, b = unpack(zz, delta)
    return F(ell, a, b), ell, a, b, Lambda(ell, a, b) - threshold(delta, a)
