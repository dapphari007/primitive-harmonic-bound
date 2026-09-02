r"""
Closed forms for the CW2 (three-row constant-weight) representation-graph coefficients.

Labels: lambda = (l1, l2, l3) three-row shape of n, eps = (W, p) two-row shape of w (W = w - p), N = n - w.
Partial hooks: Q_k = l_k + 3 - k,  P_k = eps_k + 3 - k with eps_3 = 0 (so P = (W+2, p+1, 0)).
Squared recoupling overlap (mined from GL_3 numerics; exact on 948 generic points):
    R_t(lambda, nu)^2 = prod_{k != r} |P_t - Q_k - 1| prod_{k != t} |Q_r - P_k|
                        / ( prod_{k != t} |P_t - P_k - 1| prod_{k != r} |Q_r - Q_k| ),
    where nu = lambda - e_r and eps'_t = eps - e_t.
Coefficient of the move lambda -> lambda' = lambda - e_r + e_{r'}:
    p = (w/N) (f^{lambda'} / f^{nu}) tau^2,
    tau = sum_{t=1,2} (f^{eps'_t}/f^{eps}) sigma_t sqrt(R_t(lambda,nu)^2 R_t(lambda',nu)^2),
with relative sign sigma = (-1)^(r + r') (determined in experiments/cw2_sign.py: -1 for adjacent rows, +1 for 1 <-> 3).
"""
from __future__ import annotations
import math
from fractions import Fraction


def partial_hooks(shape, m=3):
    shape = tuple(shape) + (0,) * (m - len(shape))
    return [shape[k] + m - 1 - k for k in range(m)]


def R2(lam, r, eps, t):
    """R_t(lambda, lambda - e_r)^2 (exact Fraction); r, t are 1-based rows."""
    Q = partial_hooks(lam); P = partial_hooks(eps)
    r0, t0 = r - 1, t - 1
    num = Fraction(1); den = Fraction(1)
    for k in range(3):
        if k != r0:
            num *= abs(P[t0] - Q[k] - 1); den *= abs(Q[r0] - Q[k])
        if k != t0:
            num *= abs(Q[r0] - P[k]); den *= abs(P[t0] - P[k] - 1)
    return num / den


def dim_ratio_add(nu, r):
    """f^{nu + e_r} / f^{nu} for shapes with <= 3 rows (r 1-based)."""
    lam = list(nu); lam[r - 1] += 1
    Q = partial_hooks(lam); n = sum(lam)
    val = Fraction(n, Q[r - 1])
    for k in range(3):
        if k != r - 1:
            val *= Fraction(Q[r - 1] - Q[k], Q[r - 1] - Q[k] - 1)
    return val


def dim_ratio_remove(eps, t):
    """f^{eps - e_t} / f^{eps} for a two-row shape eps = (a, b) (t 1-based)."""
    a, b = eps
    if t == 1:
        return Fraction((a - b) * (a + 1), (a + b) * (a - b + 1))
    return Fraction((a - b + 2) * b, (a + b) * (a - b + 1))


def valid_shape(s):
    return all(s[i] >= s[i + 1] for i in range(len(s) - 1)) and s[-1] >= 0


def cw2_coefficient_formula(n, w, p, lam, lam_p, sigma=None):
    """p(lambda -> lambda') from the closed form; sigma = relative sign of the t=2 term, default (-1)^(r+r')."""
    N = n - w
    lam = tuple(lam); lam_p = tuple(lam_p)
    d = [b - a for a, b in zip(lam, lam_p)]
    r = d.index(-1) + 1; rp = d.index(1) + 1
    nu = list(lam); nu[r - 1] -= 1; nu = tuple(nu)
    if sigma is None:
        sigma = (-1) ** (r + rp)
    eps = (w - p, p)
    tau = 0.0
    for t in (1, 2):
        eps_t = list(eps); eps_t[t - 1] -= 1
        if not valid_shape(eps_t):
            continue
        term = float(dim_ratio_remove(eps, t)) * math.sqrt(float(R2(lam, r, eps, t) * R2(lam_p, rp, eps, t)))
        tau += term if t == 1 else sigma * term
    return (w / N) * float(dim_ratio_add(nu, rp)) * tau ** 2
