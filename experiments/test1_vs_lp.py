"""
TEST 1 -- soundness stress test of bound (2.3) against the exact Delsarte LP.

Any valid two-point (Delsarte-type) certificate is at least the LP optimum.
The paper says its kernel "produces an ordinary scalar Delsarte certificate",
so for every (n, d, k, L) with lambda > s we must have  bound(2.3) >= LP(n, d).
A single violation would refute the finite-length statement.
"""
from __future__ import annotations

import math
import sys
import time

sys.path.insert(0, __file__.rsplit("experiments", 1)[0])

from phb.bound import perron, log2_sum_binom, log2_mk
from phb.delsarte_lp import delsarte_lp

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 40
TOL = 1e-9

violations = []
rows = []
t0 = time.time()
for n in range(4, NMAX + 1):
    lam = {}
    for k in range(0, n // 2 + 1):
        for L in range(k, n - k + 1):
            lam[(k, L)] = perron(n, k, L)
    for d in range(2, n + 1):
        s = 1.0 - 2.0 * d / n
        lp = math.log2(delsarte_lp(n, d))
        best = {}  # k -> (log2 bound, L)
        for (k, L), lm in lam.items():
            if lm <= s:
                continue
            lb = math.log2((1 - s) / (lm - s)) + log2_sum_binom(n, k, L) - log2_mk(n, k)
            if k not in best or lb < best[k][0]:
                best[k] = (lb, L)
            if lb < lp - TOL:
                violations.append((n, d, k, L, lm, lb, lp))
        b0 = best.get(0, (None, None))
        bk = min(((v[0], k, v[1]) for k, v in best.items() if k >= 1), default=None)
        rows.append((n, d, lp, b0[0], b0[1], bk))
print(f"scanned n = 4..{NMAX} in {time.time()-t0:.1f}s; (n,d) pairs: {len(rows)}")
print(f"violations of bound(2.3) >= LP: {len(violations)}")
for v in violations[:20]:
    n, d, k, L, lm, lb, lp = v
    print(f"  VIOLATION n={n} d={d} k={k} L={L} lambda={lm:.6f} log2bound={lb:.6f} log2LP={lp:.6f}")

# How close does the k>=1 family get to the LP, and does it ever beat k=0 at these lengths?
print("\nn   d   log2 LP   best k=0 (L)        best k>=1 (k,L)     k>=1 beats k=0?")
beats = 0
feasible_k1 = 0
for n, d, lp, b0, L0, bk in rows:
    if bk is None:
        continue
    feasible_k1 += 1
    better = b0 is not None and bk[0] < b0 - 1e-12
    beats += better
    if n in (8, 12, 16, 20, 24, 28, 32, 36, 40) and d in (2, 3, 4, 6, 8, 10, 12):
        print(f"{n:<3} {d:<3} {lp:8.4f}   {b0 if b0 is None else round(b0,4)!s:>8} ({L0})   "
              f"{round(bk[0],4):>8} (k={bk[1]},L={bk[2]})   {'YES' if better else 'no'}")
print(f"\n(n,d) with some feasible k>=1: {feasible_k1};  cases where k>=1 beats k=0: {beats}")
