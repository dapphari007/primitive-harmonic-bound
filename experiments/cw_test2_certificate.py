"""
CW TEST 2 -- explicit reconstruction of the constant-weight certificate for small n.
(a) measured recurrence coefficients b_j, c_j of multiplication by t(x,.) on the copies of
    E_x^{p,q} = E_p(x) (x) E_q(x^c) inside the Johnson spaces, vs the paper's (36)-(37);
(b) lambda*_J (best positive-definite lambda of (t - lambda) K) vs lambda_max(Jhat);
(c) bound (46) vs the Delsarte-Johnson bound f(0)/f^_0 vs the exact Johnson LP.
"""
import math, sys, time
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np
from phb.johnson_certificate import JohnsonLayer
from phb.johnson import hahn_bc, j_plus, lambda_max, log2_bound_J
from phb.johnson_lp import johnson_lp

cases = {(10, 4): [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2), (2, 1), (1, 2), (2, 2), (0, 3), (1, 3)],
         (12, 5): [(0, 0), (1, 1), (2, 1), (1, 2), (2, 2), (2, 3)]}
for (n, w), pqs in cases.items():
    t0 = time.time()
    JL = JohnsonLayer(n, w)
    print(f"\n##### n={n} w={w} (|X_w|={len(JL.X)}, built in {time.time()-t0:.1f}s)")
    for p, q in pqs:
        jp = j_plus(n, w, p, q)
        if p + q >= jp:
            print(f"  (p,q)=({p},{q}): j_- = {p+q} >= j_+ = {jp}, no admissible degrees"); continue
        L = jp
        meas, _ = JL.measured_coefficients(p, q, L)
        worst_b = worst_c = 0.0
        for j in range(p + q, L + 1):
            b, c = hahn_bc(n, w, p, q, j)
            bm, cm = meas[j]
            worst_b = max(worst_b, abs(bm - b))
            if cm is not None:
                worst_c = max(worst_c, abs(cm - c))
        print(f"  (p,q)=({p},{q}) degrees {p+q}..{L}: max|b_meas-b(37)| = {worst_b:.2e}, max|c_meas-c(37)| = {worst_c:.2e}")
        # positivity test for several retained-degree choices
        for Lr in sorted({jp, max(p + q + 1, (p + q + jp) // 2), min(jp, p + q + 2)}):
            if Lr <= p + q: continue
            K, lam = JL.kernel(p, q, Lr)
            ls = JL.lambda_star(K)
            flag = "OK " if ls >= lam - 1e-9 else "!! "
            line = f"      L={Lr}: lambda_max(Jhat)={lam:.6f}  lambda*={ls:.6f}  {flag}"
            # bounds for each even d
            parts = []
            for d in range(2, 2 * w + 1, 2):
                lb = log2_bound_J(n, w, d, p, q, Lr)
                bd = JL.delsarte_bound(K, d, ls)
                if lb is None and bd is None: continue
                lp = float(johnson_lp(n, w, d))
                parts.append(f"d={d}: (46)={'inf' if lb is None else f'{2**lb:.2f}'} Dels={'inf' if bd is None else f'{bd:.2f}'} LP={lp:.2f}")
            print(line + ("\n         " + " | ".join(parts) if parts else ""))
