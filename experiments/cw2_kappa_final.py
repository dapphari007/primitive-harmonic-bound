"""Refine both sides of the comparison at every grid delta: the paper's kappa_CW (gamma optimised) with extra seeds
near our optimum, and our kappa_CW2 with extra seeds; write results/cw2_kappa_final.json."""
import sys, math, json, time
import numpy as np
sys.path.insert(0, ".")
from scipy.optimize import minimize
from phb.johnson import cw_rate, M2
from phb.cw2_asymptotics import kappa_CW2, F, Lambda, threshold

def paper_side(delta, seeds_ab, n_random=60, seed=1):
    rng = np.random.default_rng(seed)
    def unp(x):
        a = delta / 2 + (0.5 - delta / 2) / (1 + math.exp(-max(-60, min(60, x[0]))))
        b = (a / 2) * math.exp(-abs(x[1])); g = ((1 - a) / 2) * math.exp(-abs(x[2])); return a, b, g
    def obj(x):
        a, b, g = unp(x); v, _ = cw_rate(delta, a, b, g); return 10.0 if (v is None or not math.isfinite(v)) else v
    starts = [np.array([0.0, 6.0, 6.0])]
    for (a, b) in seeds_ab:
        x0 = math.log((a - delta / 2) / (0.5 - delta / 2 - (a - delta / 2)))
        x1 = math.log(a / (2 * b)) if b > 0 else 30.0
        for g in (1e-9, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2):
            starts.append(np.array([x0, x1, math.log((1 - a) / (2 * g))]))
    for _ in range(n_random):
        starts.append(np.array([rng.normal(0, 1.5), rng.uniform(2, 12), rng.uniform(2, 14)]))
    best = (math.inf, None)
    for x0 in starts:
        r = minimize(obj, x0, method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-13, "maxiter": 5000})
        if r.fun < best[0]: best = (r.fun, r.x)
    a, b, g = unp(best[1]); v, u = cw_rate(delta, a, b, g)
    return v, (a, b, g, u)

def z_from(delta, a, b, l3, l2):
    inv = lambda s: math.log(s / (1 - s))
    return np.array([inv((a - delta / 2) / (0.5 - delta / 2)), inv(b / (a / 2)), inv(min(max(l3 / b, 1e-12), 1 - 1e-12)), inv(min(max((l2 - b) / (a - 2 * b), 1e-12), 1 - 1e-12))])

grid = json.load(open("results/cw2_kappa_grid.json"))
out = []
for row in grid:
    d = row["delta"]; t0 = time.time()
    o = row["cw2_opt"]; a_o, b_o, ell_o = o["alpha"], o["beta"], o["ell"]
    a_p, b_p, g_p, u_p = row["paper_opt"]; a_0, b_0, u_0 = row["gamma0_opt"]
    kp, popt = paper_side(d, [(a_o, b_o), (a_p, b_p), (a_0, b_0)])
    kp = min(kp, row["paper_kappa_CW"]); 
    seeds = [z_from(d, a_o, b_o, max(ell_o[2], 1e-12), ell_o[1])] + [z_from(d, a_0, b_0, f * b_0, u_0 * (1 + 0.05 * i)) for f in (1e-6, 1e-4, 1e-2, 0.1, 0.5) for i in range(3)] \
          + [z_from(d, a_p, b_p, f * b_p, u_p) for f in (1e-6, 1e-3, 0.1)]
    k2, ell, a, b, slack = kappa_CW2(d, n_starts=80, seed=3, starts_extra=seeds)
    if k2 > row["kappa_CW2"]:
        k2, ell, a, b, slack = row["kappa_CW2"], tuple(ell_o), a_o, b_o, o["slack"]
    r = dict(row); r.update(paper_refined=kp, paper_refined_opt=list(popt), cw2_refined=k2, cw2_refined_opt=dict(ell=list(ell), alpha=a, beta=b, slack=slack))
    out.append(r)
    print(f"delta={d:.3f}: paper {row['paper_kappa_CW']:.8f} -> refined {kp:.8f} (gamma={popt[2]:.2e}); ours {row['kappa_CW2']:.8f} -> refined {k2:.8f} (l3={ell[2]:.2e}); gain {kp-k2:+.3e}  [{time.time()-t0:.0f}s]", flush=True)
json.dump(out, open("results/cw2_kappa_final.json", "w"), indent=1)
