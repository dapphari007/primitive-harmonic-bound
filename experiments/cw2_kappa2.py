"""Robust comparison over a delta grid: paper's kappa_CW (gamma optimised) and gamma=0 restriction, our kappa_CW2
(three rows, seeded from the paper's gamma=0 optimum and random starts), M2."""
import sys, math, time, json
import numpy as np
sys.path.insert(0, ".")
from scipy.optimize import minimize
from phb.johnson import kappa_CW, M2, cw_rate
from phb.cw2_asymptotics import kappa_CW2, unpack, penalised, F, Lambda, threshold

def kappa_CW_gamma0(delta, n_starts=40, seed=0):
    rng = np.random.default_rng(seed)
    def unp(x):
        a = delta / 2 + (0.5 - delta / 2) / (1 + math.exp(-x[0])); b = (a / 2) * math.exp(-abs(x[1])); return a, b
    def obj(x):
        a, b = unp(x); v, _ = cw_rate(delta, a, b, 0.0); return 10.0 if v is None else v
    best = (math.inf, None)
    starts = [np.array([0.0, 6.0])] + [np.array([rng.normal(0, 1.5), rng.uniform(2, 10)]) for _ in range(n_starts)]
    for x0 in starts:
        r = minimize(obj, x0, method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-13, "maxiter": 4000})
        if r.fun < best[0]: best = (r.fun, r.x)
    a, b = unp(best[1]); v, u = cw_rate(delta, a, b, 0.0)
    return v, a, b, u

def z_from(delta, a, b, l3, l2):
    inv = lambda s: math.log(s / (1 - s))
    z0 = inv((a - delta / 2) / (0.5 - delta / 2)); z1 = inv(b / (a / 2)); z2 = inv(min(max(l3 / b, 1e-12), 1 - 1e-12)); z3 = inv(min(max((l2 - b) / (a - 2 * b), 1e-12), 1 - 1e-12))
    return np.array([z0, z1, z2, z3])

deltas = [float(x) for x in sys.argv[1:]] or [0.02, 0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.22, 0.235]
rows = []
for d in deltas:
    t0 = time.time()
    kcw, acw, bcw, gcw, ucw = kappa_CW(d)
    k0, a0, b0, u0 = kappa_CW_gamma0(d)
    seeds = [z_from(d, a0, b0, l3, u0 * f) for l3 in (1e-7 * b0, 1e-3 * b0, 0.05 * b0, 0.3 * b0, 0.8 * b0) for f in (1.0, 1.1, 1.3)]
    k2, ell, a, b, slack = kappa_CW2(d, n_starts=40, starts_extra=seeds)
    m2 = M2(d)
    row = dict(delta=d, paper_kappa_CW=kcw, paper_opt=[acw, bcw, gcw, ucw], paper_gamma0=k0, gamma0_opt=[a0, b0, u0],
               kappa_CW2=k2, cw2_opt=dict(ell=list(ell), alpha=a, beta=b, slack=slack), M2=m2)
    rows.append(row)
    print(f"delta={d:.3f}: M2 {m2:.7f} | paper kappa_CW {kcw:.7f} (gamma={gcw:.2e}) | paper gamma=0 {k0:.7f} | ours kappa_CW2 {k2:.7f} "
          f"(l3={ell[2]:.2e}, l2={ell[1]:.5f}, alpha={a:.5f}, beta={b:.5f}, slack={slack:.0e})\n"
          f"      gain vs gamma=0 slice {k0-k2:+.3e} | gain vs paper best {kcw-k2:+.3e}   [{time.time()-t0:.0f}s]", flush=True)
json.dump(rows, open("results/cw2_kappa_grid.json", "w"), indent=1)
