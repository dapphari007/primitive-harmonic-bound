"""Lean finite-n scan (asymptotically guided) of the two-row binary bound vs the paper's one-row (23)."""
import sys, math, time
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
from experiments.hyperoct_finite import two_row_bound
from phb.bound import perron, log2_sum_binom, log2_mk
pp, qq = int(sys.argv[1]), int(sys.argv[2]); delta = pp / qq
NS = [int(x) for x in sys.argv[3].split(",")]
ustar, bstar = float(sys.argv[4]), float(sys.argv[5])      # asymptotic optimum guidance
t0 = time.time()
for n in NS:
    d = n * pp // qq; s = 1 - 2 * d / n
    best1 = (math.inf, None)
    for k in range(max(0, int(0.5 * bstar * n)), int(1.6 * bstar * n) + 4):
        for L in range(int(0.85 * ustar * n), int(1.15 * ustar * n) + 3):
            lam = perron(n, k, L)
            if lam > s:
                v = math.log2((1 - s) / (lam - s)) + log2_sum_binom(n, k, L) - log2_mk(n, k)
                if v < best1[0]: best1 = (v, (k, L))
    k1, L1 = best1[1]
    best2 = (math.inf, None, None)
    for k in range(max(1, k1 - 4), k1 + 8):
        for A in range(0, 2):
            for B in range(0, 4):
                if A == 0 and B == 0: continue
                for jhi in range(L1 - 6, L1 + 10, 2):
                    for width in [3, 8, 20, 60, 150]:
                        jlo = max(k, jhi - width)
                        if jlo >= jhi: continue
                        v, lam = two_row_bound(n, s, k, jlo, jhi, A, B)
                        if v is not None and v < best2[0]: best2 = (v, (k, jlo, jhi, A, B), lam)
    print(f"n={n:>7} d={d:>6} | one-row: {best1[0]:12.3f} rate={best1[0]/n:.6f} (k,L)={best1[1]} | two-row: {best2[0]:12.3f} rate={best2[0]/n:.6f} box={best2[1]} Lambda={best2[2]:.6f} | gain={best1[0]-best2[0]:+.3f}   [{time.time()-t0:.0f}s]", flush=True)
