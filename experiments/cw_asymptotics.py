"""Constant-weight exponent kappa_CW(delta), kappa_bin = min(kappa_H, kappa_CW), and the gain over M2."""
import sys, time
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
from phb.johnson import kappa_CW, M2
from experiments.asymptotics import kappa_H, mrrw1

deltas = [float(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else \
    [0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.195, 0.22, 0.25, 0.30, 0.35, 0.40]
print(f"{'delta':>6} {'M1':>9} {'M2':>9} {'kappa_H':>9} {'kappa_CW':>9} {'kappa_bin':>9} {'M2-kbin':>9} {'rel%':>6} | {'alpha':>7} {'beta':>9} {'gamma':>9} {'u':>7}")
t0 = time.time()
for d in deltas:
    m1, m2 = mrrw1(d), M2(d)
    kh = kappa_H(d)[0]
    kcw, a, b, g, u = kappa_CW(d)
    kb = min(kh, kcw)
    print(f"{d:6.3f} {m1:9.6f} {m2:9.6f} {kh:9.6f} {kcw:9.6f} {kb:9.6f} {m2-kb:+9.6f} {100*(m2-kb)/m2:6.3f} | {a:7.4f} {b:9.2e} {g:9.2e} {u:7.4f}   [{time.time()-t0:.0f}s]", flush=True)
