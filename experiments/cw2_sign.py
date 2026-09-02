"""Determine the relative sign of the two recoupling terms and validate the closed form against exact S_n data."""
import sys, json, itertools, math
sys.path.insert(0, ".")
from phb.cw2_gl3 import R_overlap, cw2_coefficient
from phb.cw2_formulas import cw2_coefficient_formula, R2, valid_shape
rows = [json.loads(l) for l in open("results/layer3_coeffs_n12.jsonl")]
signs = {}
for n, w, p, lam, tgt, pv, fr in rows:
    if tuple(lam) == tuple(tgt) or pv < 1e-12: continue
    N = n - w; d = [b - a for a, b in zip(lam, tgt)]; r = d.index(-1) + 1; rp = d.index(1) + 1
    nu = list(lam); nu[r - 1] -= 1
    eps = (w - p, p); prods = {}
    for t in (1, 2):
        eps_t = list(eps); eps_t[t - 1] -= 1
        if not valid_shape(eps_t): continue
        try:
            prods[t] = R_overlap(tuple(lam), tuple(nu), eps, tuple(eps_t), N) * R_overlap(tuple(tgt), tuple(nu), eps, tuple(eps_t), N)
        except AssertionError:
            pass
    if len(prods) == 2 and abs(prods[1]) > 1e-9 and abs(prods[2]) > 1e-9:
        s = math.copysign(1, prods[1] * prods[2])
        signs.setdefault((r, rp), set()).add(int(s))
print("relative sign sigma_2/sigma_1 per move type (r -> r'):", signs)
# validate closed form with sigma = -1 and +1
for sigma in (-1, +1):
    worst = 0.0; ok = 0; tot = 0
    for n, w, p, lam, tgt, pv, fr in rows:
        if tuple(lam) == tuple(tgt) or pv < 1e-12: continue
        v = cw2_coefficient_formula(n, w, p, lam, tgt, sigma); e = abs(v - pv); worst = max(worst, e); ok += e < 1e-9; tot += 1
    print(f"closed form (sigma={sigma:+d}) vs exact S_n data: {ok}/{tot} within 1e-9, max err {worst:.2e}")
# also R2 formula vs gl3 numerics on the mined data
data = [json.loads(l) for l in open("results/cw2_R_data.jsonl")]
worst = max(abs(float(R2((l1, l2, l3), r, (W, p), t)) - R2v) for l1, l2, l3, W, p, r, t, R, R2v in data)
print(f"R^2 closed form vs gl3 numerics on {len(data)} points: max err {worst:.2e}")
