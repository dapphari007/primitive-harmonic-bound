"""
TEST 2 -- rebuild the certificate polynomial from scratch and test its positivity.

For small n, several (k, L), and several amplitude normalisations a, compute
  K(t) = Tr(P_0 P_z),  lambda*(a) = best lambda with (xi - lambda)K positive definite,
and compare lambda*(a) with the Perron eigenvalue lambda of the paper's Jacobi matrix (2.1).
If lambda*(a) >= lambda_(2.1) for the paper's a, the identity (2.2) is at least numerically
consistent; then compare the three bounds  (2.3),  Delsarte f(0)/f^_0,  and the LP.
"""
from __future__ import annotations

import math
import sys

sys.path.insert(0, __file__.rsplit("experiments", 1)[0])

import numpy as np

from phb.bound import perron, log2_bound
from phb.certificate import amplitude_choices, kernel_by_weight, lambda_star, delsarte_bound_from_kernel
from phb.delsarte_lp import delsarte_lp

cases = [(8, 1, 7), (8, 1, 4), (8, 2, 6), (10, 1, 9), (10, 1, 5), (10, 2, 8), (10, 3, 7), (12, 1, 11), (12, 2, 10), (12, 3, 9), (12, 1, 6),
         (8, 0, 3), (10, 0, 4)]
for n, k, L in cases:
    lam21 = perron(n, k, L)
    print(f"\n=== n={n} k={k} L={L}:  lambda(2.1) = {lam21:.6f}")
    for name, a in amplitude_choices(n, k, L).items():
        K = kernel_by_weight(n, k, L, a)
        ls, kh, xkh = lambda_star(n, K)
        ok = ls >= lam21 - 1e-9
        print(f"  {name:<36} lambda* = {ls:.6f}   lambda* >= lambda(2.1): {ok}   K(0)={K[0]:.4f} (m_k={math.comb(n,k)-(math.comb(n,k-1) if k else 0)})")
        if name.startswith("paper"):
            for d in range(2, n + 1):
                s = 1 - 2 * d / n
                b23 = log2_bound(n, d, k, L)
                bdel = delsarte_bound_from_kernel(n, d, K, ls)
                if b23 is None and bdel is None:
                    continue
                lp = delsarte_lp(n, d)
                print(f"      d={d:<2} s={s:+.3f}  (2.3)={'inf' if b23 is None else f'{2**b23:10.3f}'}   "
                      f"Delsarte f(0)/f0={'inf' if bdel is None else f'{bdel:10.3f}'}   LP={lp:10.3f}")
