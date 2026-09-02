"""Figure 4 (spherical): (a) deficits lambda_* - gamma by certificate family; (b) gaps between kappa levels; (c) kissing crossover."""
import re, sys, pathlib, math
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
RES = ROOT / "results"
NL = chr(10)
txt = NL.join((RES / f).read_text() for f in ["sph_asymptotics.txt", "sph_gamma_levels.txt", "sph_kissing.txt"] if (RES / f).exists())
ktxt = (RES / "sph_kappa2_refine.txt").read_text() if (RES / "sph_kappa2_refine.txt").exists() and "0.90" in (RES / "sph_kappa2_refine.txt").read_text() else txt
LAM = 0.5 * math.log2(2 * math.pi / math.e)

fam, defi, sopt = [], [], []
pats = [("classical" + NL + "(KL)", r"classical \(KL\):\s+gamma_0 = ([0-9.]+)\s+deficit = ([0-9.e+-]+)\s+at s = ([0-9.]+)"),
        ("one-row", r"gamma_row = ([0-9.]+)\s+deficit = ([0-9.e+-]+)\s+at s = 2Gamma = ([0-9.]+)")]
for r in range(1, 6):
    pats.append((f"level {r}", rf"level r={r}: gamma_{r} = ([0-9.]+)\s+deficit = ([0-9.e+-]+)\s+s\* = 2Gamma = ([0-9.]+)"))
for lab, pat in pats:
    m = re.search(pat, txt)
    if m:
        fam.append(lab); defi.append(float(m.group(2))); sopt.append(float(m.group(3)))

fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
cols = ["0.6", "tab:blue", "tab:green", "tab:pink", "tab:purple", "tab:red", "tab:brown"]
ax[0].bar(range(len(fam)), defi, color=cols[:len(fam)])
ax[0].set_yscale("log"); ax[0].set_xticks(range(len(fam))); ax[0].set_xticklabels(fam, fontsize=8)
ymin = min(defi) / 20
for i, (d, s) in enumerate(zip(defi, sopt)):
    if d / ymin > 30:
        ax[0].text(i, d * 0.55, f"{d:.1e}" + NL + f"s*={s:.3f}", ha="center", va="top", fontsize=7, color="white", fontweight="bold")
    else:
        ax[0].text(i, d * 1.6, f"{d:.1e}" + NL + f"s*={s:.3f}", ha="center", va="bottom", fontsize=7, color="black")
ax[0].set_ylim(bottom=ymin)
ax[0].set_ylim(top=max(defi) * 2.5, bottom=min(defi) / 20)
ax[0].set_ylabel(r"deficit $\lambda_* - \gamma$ (bits / dimension)")
ax[0].set_title(r"Sphere packing: distance to $\lambda_*=\frac{1}{2}\log_2\frac{2\pi}{e}$")
ax[0].grid(alpha=.3, axis="y")

rows = []
for line in ktxt.splitlines():
    m = re.match(r"\s*([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s*([0-9.e+-]*)\s*(\[|$)", line)
    if m and 0 < float(m.group(1)) < 1:
        rows.append([float(m.group(i)) for i in range(1, 6)])
if rows:
    A = np.array(rows); s, k0, kr, k1, k2 = A.T
    ax[1].plot(s, k0 - k1, "o-", ms=3, color="0.5", label=r"classical $\kappa_0-\kappa_1$")
    ax[1].plot(s, kr - k1, "s-", ms=3, color="tab:blue", label=r"one-row $\kappa_{row}-\kappa_1$")
    g12 = np.array(k1 - k2, float); g12[g12 < 1e-8] = np.nan
    ax[1].plot(s, g12, "v-", ms=3, color="tab:red", label=r"level 1 $\kappa_1-\kappa_2$ (below $10^{-8}$ not drawn)")
    ax[1].set_yscale("log")
    ax[1].set_xlabel("inner product s"); ax[1].set_ylabel("gap in whole-sphere exponent (bits / dimension)")
    ax[1].set_title("Spherical-code exponents: gaps between levels")
    ax[1].legend(fontsize=8); ax[1].grid(alpha=.3, which="both")

cr = []
for f in ["sph_crossover_kissing_part1.txt", "sph_crossover_kissing_part2.txt"]:
    if (RES / f).exists():
        for line in (RES / f).read_text().splitlines():
            m = re.match(r"\s*(\d+)\s*\|\s*([0-9.]+)\s+([0-9.]+)\s+\d+\s*\|\s*([0-9.]+)\s+([0-9.]+).*\|\s*([0-9.]+)\s+([0-9.]+).*\|\s*([+-][0-9.]+)\s+([+-][0-9.]+)", line)
            if m:
                cr.append([float(m.group(i)) for i in (1, 2, 4, 6, 8, 9)])
if cr:
    C = np.array(sorted(cr)); n, b0, b1, b2, g1, g2 = C.T
    ax[2].semilogx(n, b0 / n, "o-", ms=3, color="0.5", label="classical path (k = 0)")
    ax[2].semilogx(n, b1 / n, "s-", ms=3, color="tab:blue", label="one-row (best k, L)")
    ax[2].semilogx(n, b2 / n, "^-", ms=3, color="tab:green", label="two-row (best k, I, J)")
    ax[2].axhline(0.401414, color="0.5", ls="--", lw=.8, label=r"classical limit 0.4014")
    ax[2].axhline(0.396626, color="tab:blue", ls="--", lw=.8, label=r"level-1 limit 0.3966")
    ax[2].set_xlabel("dimension n"); ax[2].set_ylabel(r"$\log_2(\mathrm{bound})/n$ at $s=1/2$")
    ax[2].set_title("Kissing-number certificates at finite n")
    ax[2].legend(fontsize=7); ax[2].grid(alpha=.3)

fig.tight_layout(); fig.savefig(ROOT / "figures" / "fig4_spherical.png", dpi=150)
print("fig4 written:", len(fam), "families,", len(rows), "kappa rows,", len(cr), "crossover rows")
