"""Collect CW2 transition coefficients p(lambda -> lambda') for all admissible (n, w, p, lambda), n <= NMAX."""
import sys, time, json, math
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
from fractions import Fraction
from phb.layer3 import transition_coefficients, admissible, hook_dim
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12
out = open(f"results/layer3_coeffs_n{NMAX}.jsonl", "a")
t0 = time.time(); cnt = 0
for n in range(6, NMAX + 1):
    for w in range(2, (n - 1) // 2 + 1):
        for p in range(0, w // 2 + 1):
            for l3 in range(0, p + 1):
                for l2 in range(max(p, l3), w - p + 1):
                    l1 = n - l2 - l3
                    lam = (l1, l2, l3)
                    if not admissible(n, w, p, lam): continue
                    if n * math.factorial(n) // (math.factorial(l1) * math.factorial(l2) * math.factorial(l3)) > 2_500_000: continue
                    try:
                        res, tot, _ = transition_coefficients(n, w, p, lam)
                    except AssertionError as e:
                        print(f"n={n} w={w} p={p} lam={lam}: FAILED {e}", flush=True); continue
                    assert abs(tot - 1) < 1e-6, (n, w, p, lam, tot)
                    for tgt, pv in res.items():
                        out.write(json.dumps([n, w, p, list(lam), list(tgt), pv, str(Fraction(pv).limit_denominator(2_000_000))]) + chr(10))
                    out.flush(); cnt += 1
                    print(f"n={n} w={w} p={p} lam={lam}: total={tot:.9f}  " + "  ".join(f"{t}:{v:.6f}" for t, v in sorted(res.items(), reverse=True) if v > 1e-9) + f"   [{time.time()-t0:.0f}s]", flush=True)
print("DONE vertices:", cnt)
