"""Collect directed squared transition coefficients p(lambda -> lambda') of the binary two-row graph for many
(n, j, a2, b2, k); rational recognition for formula fitting."""
import sys, time, math
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
from phb.hyperoct import transition_coefficients, lr_contains, dim_V
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 9
t0 = time.time()
rows = []
import json
out = open(f"results/hyperoct_coeffs_n{NMAX}.jsonl", "a")
for n in range(6, NMAX + 1):
    for k in range(1, n // 2 + 1):
        for j in range(1, n):
            for a2 in range(0, 3):
                for b2 in range(0, 3):
                    if a2 > (n - j) // 2 or b2 > j // 2: continue
                    if not lr_contains(n, j, a2, b2, k): continue
                    if dim_V(n, j, a2, b2) * n > 1500000: continue
                    try:
                        res, tot = transition_coefficients(n, j, a2, b2, k)
                    except AssertionError as e:
                        print(f"n={n} j={j} a2={a2} b2={b2} k={k}: FAILED {e}", flush=True); continue
                    parts = []
                    for (al, be), p in sorted(res.items(), key=lambda kv: -kv[1]):
                        fr = Fraction(p).limit_denominator(20000)
                        parts.append(f"{al}|{be}: {p:.7f} ~ {fr}")
                        rows.append((n, j, a2, b2, k, al, be, p)); out.write(json.dumps([n, j, a2, b2, k, list(al), list(be), p]) + chr(10)); out.flush()
                    print(f"n={n} j={j} a2={a2} b2={b2} k={k} total={tot:.7f}  " + "  ".join(parts) + f"   [{time.time()-t0:.0f}s]", flush=True)
import pickle
pickle.dump(rows, open("results/hyperoct_coeffs.pkl", "wb"))
print("saved", len(rows), "rows")
