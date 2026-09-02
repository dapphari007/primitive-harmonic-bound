"""kappa_CW2(delta) (three-row constant-weight graph, S_N part trivial) vs the paper's kappa_CW (gamma optimised),
its gamma = 0 restriction, M2, and the two-row binary graph exponent."""
import sys, math, time, json
sys.path.insert(0, ".")
from phb.cw2_asymptotics import kappa_CW2, kappa_CW2_tworow
from phb.johnson import kappa_CW, M2, cw_rate
from phb.hyperoct_asymptotics import kappa_2row, kappa_H
deltas = [float(x) for x in sys.argv[1:]] or [0.05, 0.10, 0.15, 0.20, 0.235]
out = []
for d in deltas:
    t0 = time.time()
    k2, ell, a, b, slack = kappa_CW2(d)
    k2r, ell_r, a_r, b_r, _ = kappa_CW2_tworow(d)
    kcw, acw, bcw, gcw, ucw = kappa_CW(d)
    m2 = M2(d)
    row = dict(delta=d, kappa_CW2=k2, ell=ell, alpha=a, beta=b, slack=slack, kappa_CW2_l3eq0=k2r, kappa_CW_paper=kcw,
               paper_opt=(acw, bcw, gcw, ucw), M2=m2)
    print(f"delta={d}: kappa_CW2={k2:.7f} (ell={tuple(round(x,5) for x in ell)}, alpha={a:.5f}, beta={b:.5f}, slack={slack:.1e})"
          f"\n   l3=0 restriction {k2r:.7f} | paper kappa_CW {kcw:.7f} (alpha={acw:.5f} beta={bcw:.5f} gamma={gcw:.5f} u={ucw:.5f}) | M2 {m2:.7f}"
          f"\n   gain vs paper: {kcw - k2:+.3e}   [{time.time()-t0:.0f}s]", flush=True)
    out.append(row)
json.dump(out, open("results/cw2_kappa.json", "a"), indent=1)
