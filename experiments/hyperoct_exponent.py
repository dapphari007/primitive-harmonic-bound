import sys, time, math; sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
from phb.hyperoct_asymptotics import kappa_2row
from experiments.asymptotics import mrrw2
t0 = time.time()
deltas = [float(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [0.30, 4/13, 0.40, 0.25, 0.20, 0.15, 0.10, 0.35, 0.45, 0.05]
print(f"{'delta':>7} {'M2':>9} {'kappa_H':>9} {'kappa_2row':>10} {'gain':>10} | optimum (u, at, bt, b)", flush=True)
for d in deltas:
    r, (u, at, bt, b), kH, _ = kappa_2row(d, n_starts=12)
    print(f"{d:7.4f} {mrrw2(d):9.6f} {kH:9.6f} {r:10.6f} {kH - r:+10.2e} | u={u:.5f} at={at:.3e} bt={bt:.3e} b={b:.5f}   [{time.time()-t0:.0f}s]", flush=True)
