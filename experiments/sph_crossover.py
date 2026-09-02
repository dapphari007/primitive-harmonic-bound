"""KISSING-NUMBER CROSSOVER -- at s = 1/2, the dimension n at which the one-row / two-row moving-harmonic
certificates first beat the classical harmonic-path (Levenshtein/KL-type) certificate.
usage: python sph_crossover.py n1,n2,...   (default list)"""
import math, sys, time
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
from phb.spherical import log2_bound_row, log2_bound_two_row, a0
s = 0.5
NS = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [24, 32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1024, 1536, 2048, 3072, 4096]

def argmin_1d(f, lo, hi, coarse=30):
    lo, hi = int(lo), int(hi)
    if hi < lo: return None, math.inf
    step = max(1, (hi - lo) // coarse); bx, bv = None, math.inf
    for x in range(lo, hi + 1, step):
        v = f(x)
        if v < bv: bx, bv = x, v
    if bx is None: return None, math.inf
    while step > 1:
        step = max(1, step // 4)
        for x in range(max(lo, bx - 4 * step), min(hi, bx + 4 * step) + 1, step):
            v = f(x)
            if v < bv: bx, bv = x, v
    return bx, bv

t0 = time.time()
print(f"{'n':>6} | {'classical log2':>14} {'rate':>8} {'L0':>5} | {'one-row log2':>13} {'rate':>8} {'(k,L)':>10} | {'two-row log2':>13} {'rate':>8} {'(k,I,J)':>12} | {'gain row':>9} {'gain two':>9}")
for n in NS:
    Lc = int(a0(s) * n) + 2; Lmax = 3 * Lc + 10
    L0, b0 = argmin_1d(lambda L: (log2_bound_row(n, s, 0, L) or math.inf), 1, Lmax)
    kmax = max(4, int(0.03 * n) + 4)
    def row_k(k):
        L, v = argmin_1d(lambda L: (log2_bound_row(n, s, k, L) if L > k else None) or math.inf, k + 1, Lmax)
        row_k.cache[k] = L; return v
    row_k.cache = {}
    k1, b1 = argmin_1d(row_k, 1, kmax, coarse=20)
    def two_k(k):
        best = (math.inf, None)
        for J in range(1, min(k, 4) + 1):
            I, v = argmin_1d(lambda I: (log2_bound_two_row(n, s, k, I, J) if I > k else None) or math.inf, k + 1, Lmax, coarse=20)
            if v < best[0]: best = (v, (I, J))
        two_k.cache[k] = best[1]; return best[0]
    two_k.cache = {}
    k2, b2 = argmin_1d(two_k, 1, kmax, coarse=12)
    IJ = two_k.cache.get(k2)
    print(f"{n:>6} | {b0:14.3f} {b0/n:8.5f} {L0:>5} | {b1:13.3f} {b1/n:8.5f} {str((k1, row_k.cache.get(k1))):>10} | {b2:13.3f} {b2/n:8.5f} {str((k2,)+tuple(IJ or ())):>12} | {b0-b1:+9.3f} {b0-b2:+9.3f}   [{time.time()-t0:.0f}s]", flush=True)
