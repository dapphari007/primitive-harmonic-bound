"""Figure 5: the binary two-row exponent kappa_2row versus the paper's kappa_H / kappa_bin and MRRW2."""
import re, sys, pathlib, math
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = pathlib.Path(__file__).resolve().parents[1]
rows = []
for line in (ROOT / "results" / "hyperoct_exponent_table.txt").read_text().splitlines():
    m = re.match(r"\s*([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([+-][0-9.e+-]+)", line)
    if m: rows.append([float(m.group(i)) for i in range(1, 6)])
A = np.array(sorted(rows)); d, M2, kH, k2, gain = A.T
# kappa_CW from the fine constant-weight table (for the comparison with the paper's kappa_bin)
cw = {}
for line in (ROOT / "results" / "cw_asymptotics_fine.txt").read_text().splitlines():
    m = re.match(r"\s*([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)", line)
    if m: cw[round(float(m.group(1)), 4)] = float(m.group(5))
fig, ax = plt.subplots(1, 2, figsize=(12, 4.4))
ax[0].plot(d, M2 - kH, "o-", ms=3, color="tab:orange", label=r"paper: $M_2-\kappa_H$")
ax[0].plot(d, M2 - k2, "s-", ms=3, color="tab:red", label=r"this note: $M_2-\kappa_{2row}$")
ax[0].axvline(0.2350, color="0.5", ls=":", label=r"$\delta_1$ (above: paper's $\kappa_{bin}=\kappa_H$)")
ax[0].axhline(0, color="k", lw=.6)
ax[0].set_xlabel(r"relative distance $\delta$"); ax[0].set_ylabel("gain over MRRW2 (bits / symbol)")
ax[0].set_title("Whole-cube exponents: one-row vs two-row graph"); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
ax[1].semilogy(d, gain, "s-", ms=3, color="tab:red", label=r"$\kappa_H-\kappa_{2row}$")
kb = np.array([min(kH[i], cw.get(round(float(d[i]), 4), kH[i])) for i in range(len(d))])
g2 = kb - k2; g2m = np.where((g2 > 0) & (d >= 0.2349), g2, np.nan)
ax[1].semilogy(d, g2m, "^--", ms=4, color="tab:purple", label=r"$\kappa_{bin}-\kappa_{2row}$ (paper" + "\'" + r"s Theorem 1.1), $\delta\geq\delta_1$")
ax[1].axvline(0.2350, color="0.5", ls=":")
ax[1].set_xlabel(r"relative distance $\delta$"); ax[1].set_ylabel("improvement (bits / symbol)")
ax[1].set_title("Improvement of the two-row graph"); ax[1].legend(fontsize=8); ax[1].grid(alpha=.3, which="both")
fig.tight_layout(); fig.savefig(ROOT / "figures" / "fig5_two_row.png", dpi=150)
print("fig5 written", len(rows))
