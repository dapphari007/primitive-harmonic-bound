"""SPHERICAL TRANSCRIPTION CHECKS.
(a) classical path (k=0): eigenvalues of J_{0,L} = roots of the Gegenbauer polynomial C^{(n-2)/2}_{L+1}
(b) two-row coefficients (81) = general formula (76) at r = 1
(c) full-graph normalisation (77): sum of directed squared coefficients = 1 (r = 1, 2, 3)
(d) dimension reciprocity (78) with the Weyl formula (113), and D_{i,j} = (113) at r = 1
(e) classical packing exponent gamma_0 = 0.5990 (Kabatianskii-Levenshtein), B_KL(1/2) = 0.4014 (kissing)
(f) Chebyshev construction: bound (109) tends to lambda_* = (1/2) log2(2 pi / e)
"""
import math, sys
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np
from scipy.special import roots_gegenbauer
from scipy.linalg import eigh_tridiagonal
from phb.spherical import (path_weights, p2, p_general, weyl_dim, D2, DS, dS, Hsph, a0, BKL, gamma_phi,
                           chebyshev_tuple, packing_objective, LAMBDA_STAR, Ainv, gamma_r)

print("(a) classical harmonic path vs Gegenbauer roots")
for n, L in [(3, 6), (5, 10), (8, 12), (24, 20), (50, 30)]:
    off = path_weights(n, 0, L)
    ev = eigh_tridiagonal(np.zeros(L + 1), off, eigvals_only=True)
    roots, _ = roots_gegenbauer(L + 1, (n - 2) / 2)
    print(f"   n={n:>3} L={L:>2}: max|eig - root| = {np.max(np.abs(np.sort(ev) - np.sort(roots))):.2e}")

print("(b) two-row (81) vs general (76), r=1")
rng = np.random.default_rng(1)
worst = 0.0
for _ in range(200):
    n = int(rng.integers(6, 40)); k = int(rng.integers(0, 12)); i = k + int(rng.integers(0, 15)); j = int(rng.integers(0, k + 1))
    pip, pim, pjp, pjm = p2(n, k, i, j)
    g = [p_general(n, 1, (i, j), (k,), 1, +1), p_general(n, 1, (i, j), (k,), 1, -1),
         p_general(n, 1, (i, j), (k,), 2, +1), p_general(n, 1, (i, j), (k,), 2, -1)]
    worst = max(worst, max(abs(a - b) for a, b in zip([pip, pim, pjp, pjm], g)))
print(f"   max |(81) - (76)| over 200 random (n,k,i,j): {worst:.2e}")

print("(c) full-graph normalisation (77) and (d) reciprocity (78) with Weyl dimensions (113)")
for r in [1, 2, 3]:
    worst77 = 0.0; worst78 = 0.0; worstD = 0.0
    for _ in range(150):
        n = int(rng.integers(2 * r + 4, 2 * r + 30))
        # random interlacing lambda_1 >= mu_1 >= lambda_2 >= ... >= mu_r >= lambda_{r+1} >= 0
        seq = np.sort(rng.integers(0, 14, size=2 * r + 1))[::-1]
        lam = tuple(int(x) for x in seq[0::2]); mu = tuple(int(x) for x in seq[1::2])
        tot = 0.0
        for ell in range(1, r + 2):
            for sign in (+1, -1):
                p = p_general(n, r, lam, mu, ell, sign)
                tot += p
                if p > 0:
                    tgt = list(lam); tgt[ell - 1] += sign
                    pb = p_general(n, r, tuple(tgt), mu, ell, -sign)
                    worst78 = max(worst78, abs(weyl_dim(n, r, lam) * p - weyl_dim(n, r, tgt) * pb) / max(1.0, weyl_dim(n, r, lam) * p))
        worst77 = max(worst77, abs(tot - 1))
        if r == 1:
            worstD = max(worstD, abs(weyl_dim(n, 1, lam) - D2(n, lam[0], lam[1])) / D2(n, lam[0], lam[1]))
    print(f"   r={r}: max|sum p - 1| = {worst77:.2e}   max rel. violation of (78) = {worst78:.2e}" + (f"   max rel |D2 - Weyl| = {worstD:.2e}" if r == 1 else ""))

print("(e) classical exponents")
from scipy.optimize import minimize_scalar
g0 = lambda s: 0.5 * math.log2(2 / (1 - s)) - Hsph(a0(s))
r0 = minimize_scalar(lambda s: -g0(s), bounds=(0.01, 0.99), method="bounded", options={"xatol": 1e-12})
print(f"   gamma_0 = sup_s [1/2 log2(2/(1-s)) - H_sph(a0(s))] = {-r0.fun:.6f} at s = {r0.x:.5f}   (KL 1978 packing exponent: 0.5990)")
print(f"   B_KL(1/2) = {BKL(0.5):.6f}   (KL kissing-number exponent: 0.4014)")
print(f"   H_sph(a0(1/2)) (whole-sphere, no cap) = {Hsph(a0(0.5)):.6f}")
print(f"   lambda_* = (1/2) log2(2 pi / e) = {LAMBDA_STAR:.9f}")

print("(f) Chebyshev construction (106)-(109)")
for N, R in [(2, 1), (4, 4), (8, 16), (16, 64), (32, 256), (64, 1024), (128, 4096)]:
    a, b = chebyshev_tuple(N, R)
    G, P = gamma_phi(a, b)
    val = packing_objective(a, b)
    ZR = 2 / math.pi * math.asin(1 / math.sqrt(4 * R + 1))
    bound109 = 0.5 * math.log2(2 / ZR) - 0.5 * Hsph(Ainv(R))
    print(f"   N={N:>3} R={R:>5}: 2Gamma={2*G:.6f}  Phi={P:.6f}  packing objective={val:.6f}  (109) limit N->inf: {bound109:.6f}   deficit from lambda_*: {LAMBDA_STAR-val:.2e}")

print("(g) recurrence (67)-(68) by quadrature: multiplication by t on the copy of H_k(x^perp) inside H_i(R^n)")
# In the separated form (65) the S^{n-1} inner products reduce to 1-D integrals with weight (1-t^2)^{k+(n-3)/2}
# over t = <x,u>; the orthonormal radial polynomials are Gegenbauer with eta = k + (n-2)/2.
from scipy.special import eval_gegenbauer, roots_jacobi
worst = 0.0
for n in [3, 4, 6, 9, 15]:
    for k in [0, 1, 2, 3]:
        eta = k + (n - 2) / 2
        # Gauss-Jacobi nodes for weight (1-t^2)^{eta-1/2}
        tq, wq = roots_jacobi(60, eta - 0.5, eta - 0.5)
        def pnorm(j):
            v = eval_gegenbauer(j, eta, tq) if eta > 0 else np.cos(j * np.arccos(tq))
            return v / math.sqrt(np.sum(wq * v * v))
        for i in range(k, k + 6):
            j = i - k
            a_meas = np.sum(wq * tq * pnorm(j + 1) * pnorm(j))
            b_meas = np.sum(wq * tq * pnorm(j - 1) * pnorm(j)) if j >= 1 else 0.0
            a_paper = math.sqrt((i - k + 1) * (i + k + n - 2) / ((2 * i + n - 2) * (2 * i + n)))
            b_paper = math.sqrt((i - k) * (i + k + n - 3) / ((2 * i + n - 4) * (2 * i + n - 2))) if j >= 1 else 0.0
            worst = max(worst, abs(abs(a_meas) - a_paper), abs(abs(b_meas) - b_paper))
print(f"   max |measured - (68)| over n in {{3,4,6,9,15}}, k <= 3, i <= k+5: {worst:.2e}")
