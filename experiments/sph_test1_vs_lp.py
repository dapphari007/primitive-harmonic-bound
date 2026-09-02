"""SPH TEST 1 -- one-row (73) and two-row (81) finite bounds vs the degree-capped spherical Delsarte LP.
A moving-projection certificate is a scalar polynomial of degree <= 2*I_max in <x,y>, so it can never beat the
LP over polynomials of degree <= N when N >= 2*I_max + 1.  Any violation would refute the finite theorem."""
import math, sys, time
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np
from phb.spherical import log2_bound_row, log2_bound_two_row
from phb.spherical_lp import spherical_lp
KMAX, LMAX, IMAX, JMAX = 8, 24, 20, 4
N = 2 * max(LMAX, IMAX) + 2
t0 = time.time(); cases = 0; viol = []; wins_row = 0; wins_two = 0
known = {(3, 0.5): 12, (4, 0.5): 24, (8, 0.5): 240, (24, 0.5): 196560, (8, 0.0): 16, (5, 0.0): 10}
for n in [5, 6, 7, 8, 10, 12, 16, 24]:
    for s in [-0.3, -0.1, 0.0, 0.2, 0.35, 0.5, 0.65, 0.8]:
        lp, f, vio = spherical_lp(n, s, N)
        llp = math.log2(lp); cases += 1
        best0 = min((log2_bound_row(n, s, 0, L) or math.inf) for L in range(1, LMAX + 1))
        bestrow = math.inf; arg_row = None
        for k in range(1, KMAX + 1):
            for L in range(k + 1, LMAX + 1):
                v = log2_bound_row(n, s, k, L)
                if v is not None:
                    if v < llp - 1e-7: viol.append(("row", n, s, k, L, v, llp))
                    if v < bestrow: bestrow, arg_row = v, (k, L)
        besttwo = math.inf; arg_two = None
        if n >= 6:
            for k in range(1, KMAX + 1):
                for I in range(k + 1, IMAX + 1):
                    for J in range(1, min(JMAX, k) + 1):
                        v = log2_bound_two_row(n, s, k, I, J)
                        if v is not None:
                            if v < llp - 1e-7: viol.append(("two", n, s, k, I, J, v, llp))
                            if v < besttwo: besttwo, arg_two = v, (k, I, J)
        wins_row += bestrow < best0 - 1e-12; wins_two += besttwo < min(best0, bestrow) - 1e-12
        kn = known.get((n, s))
        print(f"n={n:>2} s={s:+.2f} | LP(deg<={N})={lp:12.3f} | classical k=0: {2**best0:12.3f} | one-row: {2**bestrow:12.3f} {arg_row} | two-row: {'-' if besttwo==math.inf else f'{2**besttwo:12.3f}'} {arg_two}"
              + (f" | known A={kn}" if kn else "") + f"   [{time.time()-t0:.0f}s]", flush=True)
print(f"\ncases={cases}, violations={len(viol)}, one-row beats classical in {wins_row}, two-row beats both in {wins_two}")
print("VIOLATIONS:", viol[:10])
