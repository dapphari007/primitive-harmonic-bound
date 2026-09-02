"""Packing exponents gamma_r by hierarchical seeding: the level-r search starts from the level-(r-1) optimum with a
small extra (stabilizer, ambient) pair appended (Prop. 7.3 (2)), plus random restarts.  Reports deficits from lambda_*."""
import math, sys, time
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np
from scipy.optimize import minimize
from phb.spherical import gamma_phi, packing_objective, LAMBDA_STAR, tuple_from_increments
import phb.spherical as S
S.A_MAX = 400.0
rng = np.random.default_rng(7)
t0 = time.time()

def to_z(a, b):
    vals = np.zeros(len(a) + len(b)); vals[0::2] = a; vals[1::2] = b
    asc = vals[::-1]
    return np.log(np.concatenate([[asc[0]], np.diff(asc)]))

def optimise(r, starts, iters=3):
    best = (-math.inf, None)
    def obj(z):
        a, b = tuple_from_increments(z, r)
        v = packing_objective(a, b)
        return 10.0 if not math.isfinite(v) else -v
    for z0 in starts:
        z = z0
        for _ in range(iters):
            res = minimize(obj, z, method="Nelder-Mead", options={"xatol": 1e-11, "fatol": 1e-14, "maxiter": 40000, "maxfev": 80000, "adaptive": True})
            z = res.x
        if -res.fun > best[0]:
            best = (-res.fun, res.x)
    return best

# one-row optimum as the level-0 seed
a_prev, b_prev = np.array([0.1056, 0.0050]), np.array([0.0])  # (a1, a2=0) with b1 -> treat as level 1 with tiny a2
prev = (np.array([0.1056]), np.array([]))
results = {}
for r in range(1, 6):
    starts = []
    pa, pb = prev
    # append a small pair below the previous smallest node, several ratios
    for rho in [0.5, 0.3, 0.15, 0.05, 0.02]:
        small = pa[-1] * rho
        a = np.concatenate([pa, [small * 0.3]]); b = np.concatenate([pb, [small]])
        starts.append(to_z(a, b))
        for _ in range(4):
            starts.append(to_z(a, b) + rng.normal(0, 0.4, 2 * r + 1))
    for _ in range(25):
        starts.append(rng.normal(-2.5, 1.2, 2 * r + 1))
    val, z = optimise(r, starts)
    a, b = tuple_from_increments(z, r)
    G, P = gamma_phi(a, b)
    results[r] = (val, a, b, 2 * G)
    prev = (a, b)
    print(f"level r={r}: gamma_{r} = {val:.8f}   deficit = {LAMBDA_STAR - val:.3e}   s* = 2Gamma = {2*G:.4f}   a={np.array2string(a, precision=5)} b={np.array2string(b, precision=5)}   [{time.time()-t0:.0f}s]", flush=True)
