"""Verify the closed forms at n = 12, 13 with second rows up to 3 (previously untested a2 = 3 / b2 = 3)."""
import sys, time, math, json
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
from phb.hyperoct import transition_coefficients, lr_contains, dim_V
from phb.hyperoct_formulas import p_formula, target, MOVES
t0 = time.time(); worst = 0.0; cnt = 0
out = open("results/hyperoct_verify_big.jsonl", "a")
for n in [12, 13]:
    for j in range(2, n - 1):
        for a2 in range(0, 4):
            for b2 in range(0, 4):
                if a2 > (n - j) // 2 or b2 > j // 2 or (a2 < 3 and b2 < 3): continue
                if dim_V(n, j, a2, b2) * n > 3_000_000: continue
                a1, b1 = n - j - a2, j - b2
                for k in range(a2 + b2, min(a1 + b2, a2 + b1) + 1):
                    if k > n // 2: continue
                    res, tot = transition_coefficients(n, j, a2, b2, k)
                    for mv in MOVES:
                        ta, tb = target(mv, a1, a2, b1, b2)
                        if ta[2] or tb[2] or ta[0] < ta[1] or tb[0] < tb[1]: continue
                        val = float(p_formula(mv, a1, a2, b1, b2, k))
                        got = res.get((ta[:2], tb[:2]), res.get(((ta[0], ta[1], 0), (tb[0], tb[1], 0)), None))
                        if got is None:
                            got = 0.0
                            for (al, be), p in res.items():
                                if tuple(al)[:2] == ta[:2] and tuple(be)[:2] == tb[:2]: got = p
                        err = abs(val - got); worst = max(worst, err); cnt += 1
                        out.write(json.dumps([n, j, a2, b2, k, mv, val, got]) + chr(10)); out.flush()
                    print(f"n={n} j={j} a2={a2} b2={b2} k={k}: total={tot:.8f}  worst so far={worst:.2e}  checked={cnt}  [{time.time()-t0:.0f}s]", flush=True)
print("DONE worst =", worst, "checked =", cnt)
