"""CW CROSSOVER -- block length at which the constant-weight primitive-harmonic certificate (p,q > 0),
transferred to the whole cube by Bassalygo-Elias, first beats the classical constant-weight certificate
(p = q = 0) at fixed delta.  usage: python cw_crossover.py p q n1,n2,...   (delta = p/q; n*p/q must be even)"""
import math, sys, time
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
from phb.johnson import lambda_max, j_plus, log2_Dsum, log2_dp, kappa_CW
from phb.bound import log2_binom
pp = int(sys.argv[1]); qq = int(sys.argv[2]); delta = pp / qq
NS = [int(x) for x in sys.argv[3].split(",")]

def argmin_1d(f, lo, hi, coarse=40):
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

def lb(n, w, d, p, q, L):
    N = n - w
    if not (p + q < L <= j_plus(n, w, p, q)): return math.inf
    s = 1 - n * d / (2 * w * N)
    lam = lambda_max(n, w, p, q, L)
    if lam <= s: return math.inf
    return math.log2((1 - s) / (lam - s)) + log2_Dsum(n, p + q, L) - log2_dp(w, p) - log2_dp(N, q) + n - log2_binom(n, w)

kcw, a_s, b_s, g_s, u_s = kappa_CW(delta, n_starts=12)
print(f"delta={delta}: asymptotic CW optimum alpha*={a_s:.4f} beta*={b_s:.2e} gamma*={g_s:.2e} u*={u_s:.4f}, kappa_CW={kcw:.6f}")
t0 = time.time()
for n in NS:
    d = n * pp // qq
    assert d % 2 == 0 and d * qq == n * pp
    wc = int(a_s * n); wwin = max(5, int(0.15 * wc))
    Lc = int(u_s * n); Lwin = max(6, int(0.6 * Lc))
    # classical: p = q = 0, optimise w and L
    def cl(w):
        return argmin_1d(lambda L: lb(n, w, d, 0, 0, L), 1, min(w, Lc + Lwin))[1]
    w0, b0 = argmin_1d(cl, max(2, wc - wwin), wc + wwin, coarse=24)
    # new: optimise w, p, q, L
    pmax = max(3, int(3 * b_s * n) + 3); qmax = max(2, int(3 * g_s * n) + 2)
    best = (math.inf, None)
    def new(w):
        bw = (math.inf, None)
        for q in range(0, qmax + 1):
            def fp(p):
                L, v = argmin_1d(lambda L: lb(n, w, d, p, q, L), p + q + 1, min(j_plus(n, w, p, q), Lc + Lwin))
                fp.cache[(p, q)] = L
                return v
            fp.cache = {}
            p, v = argmin_1d(fp, 0, pmax, coarse=16)
            if v < bw[0]: bw = (v, (p, q, fp.cache.get((p, q))))
        new.cache[w] = bw[1]
        return bw[0]
    new.cache = {}
    w1, b1 = argmin_1d(new, max(2, wc - wwin), wc + wwin, coarse=16)
    pq = new.cache.get(w1)
    gain = b0 - b1
    print(f"n={n:>7} d={d:>6} | classical: log2={b0:11.3f} rate={b0/n:.6f} w={w0} | new: log2={b1:11.3f} rate={b1/n:.6f} w={w1} (p,q,L)={pq} | gain={gain:+.3f} bits   [{time.time()-t0:.0f}s]", flush=True)
