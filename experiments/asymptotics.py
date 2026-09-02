"""
Asymptotic exponent of the whole-cube primitive-harmonic bound, (2.4):

    Lambda(a,b) = 2 (a(1-a) - b(1-b)) / sqrt(a(1-a)),  0 < b < a <= 1/2
    Lambda(a,b) > 1 - 2 delta   ==>   R2(delta) <= H2(a) - H2(b)

    kappa_H(delta) := inf { H2(a) - H2(b) : Lambda(a,b) >= 1 - 2 delta }

compared with MRRW1(delta) = H2(1/2 - sqrt(delta(1-delta))) and the optimised
second MRRW bound M2(delta) = min_{0<=u<=1-2delta} [1 + g(u^2) - g(u^2 + 2 delta u + 2 delta)],
g(z) = H2((1 - sqrt(1-z))/2).   Also checks the rational witness (2.5) at delta = 4/13.
"""
from __future__ import annotations

from fractions import Fraction

import mpmath as mp
import numpy as np
from scipy.optimize import minimize_scalar

mp.mp.dps = 40


def H2(x):
    if x <= 0 or x >= 1:
        return 0.0
    return float(-x * np.log2(x) - (1 - x) * np.log2(1 - x))


def mrrw1(delta):
    return H2(0.5 - np.sqrt(delta * (1 - delta)))


def g(z):
    return H2((1 - np.sqrt(max(0.0, 1 - z))) / 2)


def mrrw2(delta):
    f = lambda u: 1 + g(u * u) - g(u * u + 2 * delta * u + 2 * delta)
    us = np.linspace(0, 1 - 2 * delta, 4001)
    vals = [f(u) for u in us]
    i = int(np.argmin(vals))
    lo, hi = us[max(i - 1, 0)], us[min(i + 1, len(us) - 1)]
    if hi > lo:
        r = minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 1e-12})
        return min(r.fun, vals[i])
    return vals[i]


def a_min(b, delta):
    """Smallest a with Lambda(a,b) = 1-2delta; None if it would need a > 1/2."""
    B = b * (1 - b)
    c = 1 - 2 * delta
    sqrtA = (c + np.sqrt(c * c + 16 * B)) / 4
    A = sqrtA * sqrtA
    if A > 0.25 + 1e-15:
        return None
    return (1 - np.sqrt(max(0.0, 1 - 4 * A))) / 2


def kappa_H(delta):
    """inf_b H2(a_min(b)) - H2(b).  Returns (value, a, b)."""
    def obj(b):
        a = a_min(b, delta)
        if a is None:
            return 10.0
        return H2(a) - H2(b)
    # b ranges over (0, b_max) where a_min(b_max) = 1/2
    bs = np.logspace(-9, np.log10(0.5), 3000)
    vals = np.array([obj(b) for b in bs])
    i = int(np.argmin(vals))
    lo, hi = bs[max(i - 1, 0)], bs[min(i + 1, len(bs) - 1)]
    r = minimize_scalar(obj, bounds=(lo, hi), method="bounded", options={"xatol": 1e-14})
    b = r.x if r.fun < vals[i] else bs[i]
    return obj(b), a_min(b, delta), b


if __name__ == "__main__":
    # ---- the rational witness of Section 2.4 ----
    delta, a, b = Fraction(4, 13), Fraction(1, 25), Fraction(1, 1500)
    A, B = a * (1 - a), b * (1 - b)
    margin = 4 * (A - B) ** 2 - (Fraction(5, 13)) ** 2 * A
    print("delta=4/13, a=1/25, b=1/1500")
    print(f"  spectral margin 4(A-B)^2 - (5/13)^2 A = {margin}   (paper: 3182386369/213890625000000)")
    print(f"  match: {margin == Fraction(3182386369, 213890625000000)}")
    Lam = 2 * float(A - B) / float(A) ** 0.5
    print(f"  Lambda(a,b) = {Lam:.9f}  vs  1-2delta = 5/13 = {5/13:.9f}   ->  Lambda > 1-2delta: {Lam > 5/13}")
    with mp.workdps(40):
        h = lambda x: -x * mp.log(x, 2) - (1 - x) * mp.log(1 - x, 2)
        val = h(mp.mpf(1) / 25) - h(mp.mpf(1) / 1500)
        m1 = h(mp.mpf(1) / 26)
        print(f"  H2(1/25) - H2(1/1500) = {mp.nstr(val, 12)}   < 469/2000 = 0.2345 : {val < mp.mpf(469)/2000}")
        print(f"  MRRW1(4/13) = H2(1/26) = {mp.nstr(m1, 12)}")
    print(f"  M2(4/13) (optimised second MRRW) = {mrrw2(4/13):.9f}")
    v, aa, bb = kappa_H(4 / 13)
    print(f"  optimised kappa_H(4/13) = {v:.9f} at a={aa:.6f}, b={bb:.3e}")

    # ---- table across delta ----
    print("\n delta    MRRW1      MRRW2      kappa_H    kH<MRRW1  kH<MRRW2   a_opt     b_opt")
    for delta in [0.02, 0.05, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.273, 0.30, 4/13, 0.35, 0.40, 0.45, 0.49]:
        m1, m2 = mrrw1(delta), mrrw2(delta)
        v, aa, bb = kappa_H(delta)
        print(f" {delta:<7.4f} {m1:.6f}   {m2:.6f}   {v:.6f}   {str(v < m1 - 1e-9):<8}  {str(v < m2 - 1e-9):<8}  {aa:.5f}   {bb:.2e}")
