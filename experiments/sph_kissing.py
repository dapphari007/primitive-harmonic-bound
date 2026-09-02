"""Kissing-number exponents at s = 1/2 (whole-sphere and cap-optimised) and kappa curves over s."""
import math, sys, time
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np
from phb.spherical import kappa_r, kappa_row, Hsph, a0, BKL
t0 = time.time(); s = 0.5
print("== whole-sphere exponents at s = 1/2 ==")
print(f"classical H_sph(a0(1/2)) = {Hsph(a0(s)):.6f}")
print(f"one-row kappa_row(1/2)   = {kappa_row(s):.6f}")
for r in [1, 2]:
    v, a, b = kappa_r(s, r, n_starts=20)
    print(f"level {r} kappa_{r}(1/2)     = {v:.6f}   a={a.round(5)} b={b.round(5)}   [{time.time()-t0:.0f}s]", flush=True)
print("\n== cap-optimised exponents at s = 1/2: inf_t kappa(t) + 1/2 log2((1-t)/(1-s)) ==")
print(f"classical B_KL(1/2)      = {BKL(s):.6f}")
ts = np.linspace(0.34, 0.5, 33)
vals = [(kappa_row(t) + 0.5 * math.log2((1 - t) / (1 - s)), t) for t in ts]
b = min(vals); print(f"one-row kappa_bar_row(1/2) = {b[0]:.6f} at t = {b[1]:.4f}")
for r in [1, 2]:
    vals = []
    for t in np.linspace(0.36, 0.5, 15):
        vals.append((kappa_r(t, r, n_starts=8)[0] + 0.5 * math.log2((1 - t) / (1 - s)), t))
    b = min(vals); print(f"level {r} kappa_bar_{r}(1/2)   = {b[0]:.6f} at t = {b[1]:.4f}   [{time.time()-t0:.0f}s]", flush=True)
print("\n== kappa curves (whole sphere) ==")
print(f"{'s':>5} {'kappa_0':>9} {'kappa_row':>9} {'kappa_1':>9} {'kappa_2':>9}")
for sv in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    k1 = kappa_r(sv, 1, n_starts=10)[0]; k2 = kappa_r(sv, 2, n_starts=10)[0]
    print(f"{sv:5.2f} {Hsph(a0(sv)):9.6f} {kappa_row(sv):9.6f} {k1:9.6f} {k2:9.6f}   [{time.time()-t0:.0f}s]", flush=True)
