"""Figure 3: constant-weight exponent gains, parsed from results/cw_asymptotics_fine.txt."""
import re, sys, pathlib
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
rows = []
for line in (ROOT / "results" / "cw_asymptotics_fine.txt").read_text().splitlines():
    m = re.match(r"\s*([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([+-][0-9.]+)", line)
    if m:
        rows.append([float(x) for x in m.groups()])
A = np.array(rows)
d, M1, M2, kH, kCW, kbin, gain = A.T
keep = d <= 0.451          # beyond this the gains (< 1e-5) sit at the optimizer's noise floor
d, M1, M2, kH, kCW = d[keep], M1[keep], M2[keep], kH[keep], kCW[keep]
def pos(x):
    x = np.array(x, float); x[x <= 0] = np.nan; return x
fig, ax = plt.subplots(1, 2, figsize=(12, 4.4))
ax[0].semilogy(d, pos(M2 - kCW), "o-", ms=3, color="tab:red", label=r"$M_2-\kappa_{CW}$")
ax[0].semilogy(d, pos(M2 - kH), "s--", ms=3, color="tab:orange", label=r"$M_2-\kappa_H$ (only where positive)")
ax[0].axvline(0.19504, color="0.4", ls=":", label=r"$\delta_0=0.19504$")
ax[0].axvline(0.2350, color="tab:blue", ls=":", label=r"$\delta_1=0.2350$")
ax[0].set_xlabel(r"relative distance $\delta$"); ax[0].set_ylabel("gain in exponent (bits / symbol)")
ax[0].set_title("Improvement over the second MRRW bound"); ax[0].grid(alpha=.3, which="both"); ax[0].legend(fontsize=8)
ax[1].semilogy(d, pos(kH - kCW), "o-", ms=3, color="tab:blue", label=r"$\kappa_H-\kappa_{CW}$ (zero for $\delta\geq\delta_1$, not drawn)")
ax[1].axvline(0.2350, color="tab:blue", ls=":", label=r"$\delta_1=0.2350$")
ax[1].set_xlabel(r"relative distance $\delta$"); ax[1].set_ylabel(r"$\kappa_H-\kappa_{CW}$")
ax[1].set_title("Advantage of a non-middle layer"); ax[1].grid(alpha=.3, which="both"); ax[1].legend(fontsize=8)
fig.tight_layout(); fig.savefig(ROOT / "figures" / "fig3_cw_exponent.png", dpi=150)
print("wrote fig3 with", len(rows), "points")
