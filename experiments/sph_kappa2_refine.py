"""Refine kappa_2(s) (and kappa_1) on the s grid with many restarts; the level-2 search is seeded from level 1."""
import math, sys, time
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np
from phb.spherical import kappa_r, kappa_row, Hsph, a0
t0 = time.time()
print(f"{'s':>5} {'kappa_0':>10} {'kappa_row':>10} {'kappa_1':>10} {'kappa_2':>10} {'k1-k2':>10}")
for sv in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    k1 = kappa_r(sv, 1, n_starts=40, seed=1)[0]
    k2 = min(kappa_r(sv, 2, n_starts=40, seed=sd)[0] for sd in (1, 2))
    k2 = min(k2, k1)
    print(f"{sv:5.2f} {Hsph(a0(sv)):10.7f} {kappa_row(sv):10.7f} {k1:10.7f} {k2:10.7f} {k1-k2:10.2e}   [{time.time()-t0:.0f}s]", flush=True)
