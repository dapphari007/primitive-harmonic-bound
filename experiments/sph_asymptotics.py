"""Spherical hierarchy asymptotics: packing exponents gamma_r (93), kissing exponents at s = 1/2,
kappa_r(s) curves, strict hierarchy, deficits from lambda_* (reproduces the paper's Figure 4 numbers)."""
import math, sys, time
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np
from phb.spherical import (gamma_r, kappa_r, kappa_row, Hsph, a0, BKL, LAMBDA_STAR, gamma_phi)
t0 = time.time()
print(f"lambda_* = {LAMBDA_STAR:.9f}")
print("\n== sphere-packing exponents gamma_r = sup_tuples [1/2 log2(2/(1-2Gamma_r)) - Phi_r] ==")
from scipy.optimize import minimize_scalar
g0 = lambda s: 0.5 * math.log2(2 / (1 - s)) - Hsph(a0(s))
r0 = minimize_scalar(lambda s: -g0(s), bounds=(0.01, 0.99), method="bounded", options={"xatol": 1e-12})
print(f"classical (KL):  gamma_0 = {-r0.fun:.7f}   deficit = {LAMBDA_STAR + r0.fun:.3e}   at s = {r0.x:.4f}")
# one-row: tuples (a, b) with a2 = 0 (level-1 with zero terminal coordinate)
from scipy.optimize import minimize
def one_row_obj(z):
    b = math.exp(z[0]); a = b + math.exp(z[1])
    G, P = gamma_phi(np.array([a, 0.0]), np.array([b]))
    return 10.0 if 2 * G >= 1 else -(0.5 * math.log2(2 / (1 - 2 * G)) - P)
best = min((minimize(one_row_obj, x0, method="Nelder-Mead", options={"xatol":1e-10,"fatol":1e-13,"maxiter":20000}) for x0 in
            [np.array([-3.0, -1.0]), np.array([-2.0, -2.0]), np.array([-1.0, 0.0]), np.array([-4.0, -0.5])]), key=lambda r: r.fun)
b = math.exp(best.x[0]); a = b + math.exp(best.x[1]); G, P = gamma_phi(np.array([a, 0.0]), np.array([b]))
print(f"one-row:         gamma_row = {-best.fun:.7f}   deficit = {LAMBDA_STAR + best.fun:.3e}   at s = 2Gamma = {2*G:.4f} (a={a:.4f}, b={b:.5f})")
for r in [1, 2, 3, 4]:
    v, a, bb = gamma_r(r, n_starts=30)
    G, P = gamma_phi(a, bb)
    print(f"level r={r}:       gamma_{r} = {v:.7f}   deficit = {LAMBDA_STAR - v:.3e}   at s = 2Gamma = {2*G:.4f}   a={np.round(a,4)} b={np.round(bb,4)}   [{time.time()-t0:.0f}s]", flush=True)

print("\n== kissing-number exponents at s = 1/2 (whole-sphere kappa_r and cap-optimised kappa_bar_r) ==")
s = 0.5
print(f"classical: H_sph(a0(1/2)) = {Hsph(a0(s)):.6f}   B_KL(1/2) = {BKL(s):.6f}")
kr = kappa_row(s); print(f"one-row:   kappa_row(1/2) = {kr:.6f}")
vals = {}
for r in [1, 2, 3]:
    v, a, bb = kappa_r(s, r, n_starts=24)
    vals[r] = v
    print(f"level {r}:   kappa_{r}(1/2) = {v:.6f}   a={np.round(a,4)} b={np.round(bb,4)}   [{time.time()-t0:.0f}s]", flush=True)
# cap-optimised: inf_t kappa_r(t) + 1/2 log2((1-t)/(1-s)); scan t
for r in [1, 2]:
    ts = np.linspace(0.30, 0.5, 21)
    best = min((kappa_r(t, r, n_starts=10)[0] + 0.5 * math.log2((1 - t) / (1 - s)), t) for t in ts)
    print(f"cap-optimised level {r}: kappa_bar_{r}(1/2) = {best[0]:.6f} at t = {best[1]:.3f}   [{time.time()-t0:.0f}s]", flush=True)
ts = np.linspace(0.30, 0.5, 41)
best = min((kappa_row(t) + 0.5 * math.log2((1 - t) / (1 - s)), t) for t in ts)
print(f"cap-optimised one-row:  kappa_bar_row(1/2) = {best[0]:.6f} at t = {best[1]:.3f}")

print("\n== kappa curves (whole sphere) ==")
print(f"{'s':>5} {'kappa_0':>9} {'kappa_row':>9} {'kappa_1':>9} {'kappa_2':>9}")
for s in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    k1 = kappa_r(s, 1, n_starts=12)[0]; k2 = kappa_r(s, 2, n_starts=12)[0]
    print(f"{s:5.2f} {Hsph(a0(s)):9.6f} {kappa_row(s):9.6f} {k1:9.6f} {k2:9.6f}   [{time.time()-t0:.0f}s]", flush=True)
