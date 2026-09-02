"""CW TEST 1 -- bound (46) vs the exact Johnson-scheme Delsarte LP, all n <= NMAX, 1 <= w < n/2, even d, every (p,q,L)."""
import math, sys, time
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
from phb.johnson import lambda_max, j_plus, log2_Dsum, log2_dp
from phb.johnson_lp import johnson_lp
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 28
t0 = time.time(); pairs = 0; viol = []; beats = 0; margin = math.inf
for n in range(6, NMAX + 1):
    for w in range(2, (n - 1) // 2 + 1):
        N = n - w
        lam = {}
        for p in range(0, w // 2 + 1):
            for q in range(0, N // 2 + 1):
                jp = j_plus(n, w, p, q)
                for L in range(p + q + 1, jp + 1):
                    lam[(p, q, L)] = lambda_max(n, w, p, q, L)
        for d in range(2, 2 * w + 1, 2):
            s = 1 - n * d / (2 * w * N)
            lp = math.log2(johnson_lp(n, w, d)); pairs += 1
            best0 = math.inf; bestk = math.inf
            for (p, q, L), lm in lam.items():
                if lm <= s: continue
                lb = math.log2((1 - s) / (lm - s)) + log2_Dsum(n, p + q, L) - log2_dp(w, p) - log2_dp(N, q)
                margin = min(margin, lb - lp)
                if lb < lp - 1e-9: viol.append((n, w, d, p, q, L, lm, lb, lp))
                if p == 0 and q == 0: best0 = min(best0, lb)
                else: bestk = min(bestk, lb)
            beats += bestk < best0 - 1e-12
    print(f"n={n} done: (n,w,d) triples={pairs}, violations={len(viol)}, (p,q)!=(0,0) beats classical in {beats}, min(log2 bound - log2 LP)={margin:.4f}  [{time.time()-t0:.0f}s]", flush=True)
print("VIOLATIONS:", viol[:10])
