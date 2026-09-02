"""G4: kappa_m(delta) for m = 3 (regression vs kappa_CW2) and m = 4 (four-row ambient), seeded from the m=3 optimum."""
import sys, json, math, time
import numpy as np
sys.path.insert(0, ".")
from phb.cwm_asymptotics import kappa_m, z_from, unpack, F, Lambda, threshold
final = {r["delta"]: r for r in json.load(open("results/cw2_kappa_final.json"))}
deltas = [float(x) for x in sys.argv[1:]] or [0.05, 0.10, 0.12]
out = []
for d in deltas:
    t0 = time.time()
    r3 = final[d]; o = r3["cw2_refined_opt"]; ell3 = o["ell"]; a3 = o["alpha"]; b3 = o["beta"]
    # m = 3 regression (seeded + random)
    seeds3 = [z_from(d, a3, (a3 - b3, b3), ell3, 3)]
    k3, ell, a, om, slack, z3 = kappa_m(d, 3, n_starts=30, starts_extra=seeds3)
    # m = 4 seeded from the m = 3 optimum with a tiny fourth row and tiny third stabilizer row
    seeds4 = []
    for f_om in (1e-6, 1e-4, 1e-2, 0.1, 0.5):
        for f_l in (1e-3, 0.1, 0.5, 0.9):
            om3 = f_om * b3; l4 = f_l * om3
            om4 = (a3 - b3 - om3, b3, om3)
            ell4 = (ell3[0], ell3[1], ell3[2] - l4 * 0.0, l4)
            ell4 = (1 - ell4[1] - ell4[2] - ell4[3], ell4[1], ell4[2], ell4[3])
            try:
                seeds4.append(z_from(d, a3, om4, ell4, 4))
            except Exception:
                pass
    k4, ell4o, a4, om4o, slack4, z4 = kappa_m(d, 4, n_starts=40, starts_extra=seeds4)
    row = dict(delta=d, kappa_CW2_ref=r3["cw2_refined"], kappa_m3=k3, m3_opt=dict(ell=list(ell), alpha=a, om=list(om), slack=slack),
               kappa_m4=k4, m4_opt=dict(ell=list(ell4o), alpha=a4, om=list(om4o), slack=slack4), paper=r3["paper_refined"], M2=r3["M2"])
    out.append(row)
    print(f"delta={d}: m=3 {k3:.8f} (ref {r3['cw2_refined']:.8f}) | m=4 {k4:.8f} (ell={tuple(round(x,6) for x in ell4o)}, alpha={a4:.5f}, om={tuple(round(x,6) for x in om4o)}, slack={slack4:.0e})"
          f"\n   gain m4 vs m3 {k3-k4:+.3e} | m4 vs paper {r3['paper_refined']-k4:+.3e}   [{time.time()-t0:.0f}s]", flush=True)
    json.dump(out, open(__import__("os").environ.get("CWM_OUT", "results/cwm_kappa.json"), "w"), indent=1)
