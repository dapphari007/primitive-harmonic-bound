"""G1/G2: check the gl_m modules, regress m=3 against cw2_gl3, test conjecture C(3) (four-row ambient) and find the
sign rule.  Usage: python experiments/cwm_test.py [nmax]"""
import sys, json, time, itertools, math, random
sys.path.insert(0, ".")
from fractions import Fraction
from phb.glm import GLmIrrep
from phb.cwm_gl import R_overlap, products, R2_conj, hook_dim, pad, valid
from phb.cw2_gl3 import R_overlap as R_overlap3

t0 = time.time()
# ---- module checks
for hw in [(2, 1, 0), (3, 1, 0), (2, 1, 0, 0), (3, 2, 1, 0), (4, 2, 1, 0), (5, 3, 1, 0), (3, 1, 0, 0, 0)]:
    V = GLmIrrep(hw); c = V.check()
    print(f"gl_{len(hw)} hw={hw}: dim {c['dim']} weyl {c['weyl']} comm {c['comm']:.1e} serre {c['serre']:.1e} adj {c['adj']:.1e} min norm2 {V.norm2.min():.3g}")

# ---- m = 3 regression vs cw2_gl3
worst = 0.0
for (lam, W, p) in [((10, 5, 1), 5, 2), ((9, 4, 2), 5, 3), ((11, 6, 2), 6, 3)]:
    for r in (1, 2, 3):
        for t in (1, 2):
            nu = list(lam); nu[r - 1] -= 1; eps = (W, p); e = list(eps); e[t - 1] -= 1
            if not valid(nu) or not valid(e): continue
            N = sum(lam) - W - p
            try:
                a = abs(R_overlap3(tuple(lam), tuple(nu), eps, tuple(e), N)); b = abs(R_overlap(lam, tuple(nu), eps, tuple(e), N, 3))
            except AssertionError:
                continue
            worst = max(worst, abs(a - b))
print(f"m=3 regression vs cw2_gl3: max |diff| = {worst:.2e}  [{time.time()-t0:.0f}s]")

# ---- m = 4: conjecture C(3) on generic four-row points
nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 16
rows = []; worst = 0.0; cnt = 0
sign_obs = {}
for l4 in range(0, 2):
    for pp in range(l4 + 1, l4 + 3):
        for l3 in range(pp + 1, pp + 3):
            for p in range(l3 + 1, l3 + 3):
                for l2 in range(p + 1, p + 3):
                    for W in range(l2 + 1, l2 + 3):
                        for l1 in range(W + 1, W + 3):
                            lam = (l1, l2, l3, l4); n = sum(lam); eps = (W, p, pp); w = sum(eps); N = n - w
                            if n > nmax or N < 1: continue
                            for r in range(1, 5):
                                nu = list(lam); nu[r - 1] -= 1
                                if not valid(nu): continue
                                for t in range(1, 4):
                                    e = list(eps); e[t - 1] -= 1
                                    if not valid(e): continue
                                    try:
                                        R = R_overlap(lam, tuple(nu), eps, tuple(e), N, 4)
                                    except AssertionError:
                                        continue
                                    conj = float(R2_conj(lam, r, eps, t, 4))
                                    err = abs(R * R - conj); worst = max(worst, err); cnt += 1
                                    rows.append([l1, l2, l3, l4, W, p, pp, r, t, R, R * R, conj])
                            # sign rule: products for all moves
                            for r in range(1, 5):
                                for rp in range(1, 5):
                                    if r == rp: continue
                                    tgt = list(lam); tgt[r - 1] -= 1; tgt[rp - 1] += 1
                                    if not valid(tgt): continue
                                    try:
                                        pr, _, _, _ = products(n, w, lam, tuple(tgt), eps, 4)
                                    except AssertionError:
                                        continue
                                    ts = sorted(pr)
                                    if len(ts) >= 2 and all(abs(pr[t][0]) > 1e-9 for t in ts):
                                        rel = tuple((t, int(math.copysign(1, pr[t][0] * pr[ts[0]][0]))) for t in ts)
                                        sign_obs.setdefault((r, rp), set()).add(rel)
    print(f"l4={l4} done: {cnt} overlaps, worst |R^2 - conj| = {worst:.2e}  [{time.time()-t0:.0f}s]", flush=True)
json.dump(rows, open("results/cwm4_R_data.json", "w"))
print(f"C(3) test: {cnt} squared overlaps, max |R^2 - conjecture| = {worst:.2e}")
print("relative signs per move (r -> r'): (t, sign relative to the smallest t):")
for k in sorted(sign_obs):
    print("  ", k, sorted(sign_obs[k]))
