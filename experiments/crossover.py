"""
CROSSOVER LENGTH -- at which block length n does the primitive-harmonic certificate (k >= 1)
first give a smaller bound than the classical k = 0 (Levenshtein / first-MRRW-type) certificate?

The paper proves the asymptotic separation but explicitly says it "does not claim an
improvement for short block lengths".  Here we quantify it for delta = d/n fixed.

usage:  python crossover.py p q m1,m2,...      (delta = p/q, n = q*m)
"""
from __future__ import annotations

import math
import sys
import time

sys.path.insert(0, __file__.rsplit("experiments", 1)[0])

from phb.bound import perron, log2_sum_binom, log2_mk

p = int(sys.argv[1]) if len(sys.argv) > 2 else 4
q = int(sys.argv[2]) if len(sys.argv) > 2 else 13
delta = p / q
MULTS = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else \
    [50, 100, 200, 300, 400, 500, 600, 800, 1000, 1500, 2000]


def lb(n, s, k, L):
    if not (k <= L <= n - k):
        return math.inf
    lam = perron(n, k, L)
    if lam <= s:
        return math.inf
    return math.log2((1 - s) / (lam - s)) + log2_sum_binom(n, k, L) - log2_mk(n, k)


def argmin_1d(f, lo, hi, coarse=40):
    """Coarse-to-fine integer minimisation of f on [lo, hi] (f may be +inf on a left interval)."""
    lo, hi = int(lo), int(hi)
    step = max(1, (hi - lo) // coarse)
    best_x, best_v = None, math.inf
    for x in range(lo, hi + 1, step):
        v = f(x)
        if v < best_v:
            best_x, best_v = x, v
    if best_x is None:
        return None, math.inf
    while step > 1:
        step = max(1, step // 4)
        for x in range(max(lo, best_x - 4 * step), min(hi, best_x + 4 * step) + 1, step):
            v = f(x)
            if v < best_v:
                best_x, best_v = x, v
    return best_x, best_v


def best_for_k(n, s, k, Llo, Lhi):
    return argmin_1d(lambda L: lb(n, s, k, L), max(k, Llo), min(n - k, Lhi))


print(f"delta = {p}/{q} = {delta:.6f}")
print(f"{'n':>7} {'d':>6} | {'k=0 log2':>10} {'rate':>8} {'L0':>6} | {'k>=1 log2':>10} {'rate':>8} {'k':>5} {'L':>6} | {'gain(bits)':>10}")
t0 = time.time()
first_cross = None
for m in MULTS:
    n, d = q * m, p * m
    s = 1 - 2 * d / n
    a0 = 0.5 - math.sqrt(delta * (1 - delta))
    L_c = int(a0 * n)
    win = max(12, int(0.02 * n))
    L0, b0 = best_for_k(n, s, 0, L_c - win, L_c + win)
    kmax = max(4, int(0.006 * n) + 3)

    def g(k):
        L, v = best_for_k(n, s, k, L_c - win, L_c + 2 * win)
        g.cache[k] = L
        return v
    g.cache = {}
    kbest, bk = argmin_1d(g, 1, kmax, coarse=30)
    Lk = g.cache.get(kbest)
    gain = b0 - bk if (math.isfinite(b0) and math.isfinite(bk)) else None
    if gain is not None and gain > 0 and first_cross is None:
        first_cross = n
    print(f"{n:>7} {d:>6} | {b0:10.3f} {b0/n:8.5f} {L0!s:>6} | {bk:10.3f} {bk/n if math.isfinite(bk) else float('nan'):8.5f} {kbest!s:>5} {Lk!s:>6} | "
          f"{'' if gain is None else f'{gain:10.3f}'}   [{time.time()-t0:.0f}s]", flush=True)
print(f"\nfirst n in the scan where k>=1 beats k=0: {first_cross}")
