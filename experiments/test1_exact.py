"""TEST 1 (extended) -- bound (23) vs the EXACT rational Delsarte LP for 41 <= n <= 64 (HiGHS is unreliable there)."""
import math, sys, time
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
from phb.bound import perron, log2_sum_binom, log2_mk
from phb.exact_lp import exact_delsarte_lp
ns = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else list(range(41, 57)) + [60, 64]
t0 = time.time(); total = 0; viol = []; beats = 0; minratio = math.inf
for n in ns:
    lam = {(k, L): perron(n, k, L) for k in range(0, n // 2 + 1) for L in range(k, n - k + 1)}
    for d in range(2, n + 1):
        s = 1 - 2 * d / n
        lp = math.log2(exact_delsarte_lp(n, d)); total += 1
        best0, bestk = math.inf, math.inf
        for (k, L), lm in lam.items():
            if lm <= s: continue
            lb = math.log2((1 - s) / (lm - s)) + log2_sum_binom(n, k, L) - log2_mk(n, k)
            if lb < lp - 1e-9: viol.append((n, d, k, L, lm, lb, lp))
            minratio = min(minratio, lb - lp)
            if k == 0: best0 = min(best0, lb)
            else: bestk = min(bestk, lb)
        beats += bestk < best0 - 1e-12
    print(f"n={n} done, cumulative (n,d) pairs={total}, violations={len(viol)}, k>=1 beats k=0 in {beats} pairs, min(log2 bound - log2 LP)={minratio:.4f}  [{time.time()-t0:.0f}s]", flush=True)
print("VIOLATIONS:", viol[:10])
