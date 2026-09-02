"""Figure 6: three-row constant-weight exponent vs the paper's constant-weight exponent (gains vs delta)."""
import json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
rows = json.load(open("results/cw2_kappa_final.json" if os.path.exists("results/cw2_kappa_final.json") else "results/cw2_kappa_grid.json"))
for r in rows:
    r["kappa_CW2"] = r.get("cw2_refined", r["kappa_CW2"]); r["paper_kappa_CW"] = r.get("paper_refined", r["paper_kappa_CW"])
    if "cw2_refined_opt" in r: r["cw2_opt"] = r["cw2_refined_opt"]
d = [r["delta"] for r in rows]
g_slice = [r["paper_gamma0"] - r["kappa_CW2"] for r in rows]
g_paper = [r["paper_kappa_CW"] - r["kappa_CW2"] for r in rows]
g_m2 = [r["M2"] - r["kappa_CW2"] for r in rows]
g_m2_paper = [r["M2"] - r["paper_kappa_CW"] for r in rows]
l3 = [r["cw2_opt"]["ell"][2] for r in rows]
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ax[0].plot(d, g_m2_paper, "s--", color="#888", label=r"paper $\kappa_{CW}$: gain over $M_2$")
ax[0].plot(d, g_m2, "o-", color="#1f77b4", label=r"three-row $\kappa_{CW2}$: gain over $M_2$")
ax[0].plot(d, g_slice, "^-", color="#2ca02c", label=r"$\kappa_{CW2}$ vs its own $\ell_3=0$ slice ($\gamma=0$)")
ax[0].plot(d, g_paper, "d-", color="#d62728", label=r"$\kappa_{CW2}$ vs paper $\kappa_{CW}$ ($\gamma$ optimised)")
ax[0].axhline(0, color="k", lw=0.6)
ax[0].set_yscale("symlog", linthresh=1e-6)
ax[0].set_xlabel(r"$\delta$"); ax[0].set_ylabel("exponent gain (bits per symbol)")
ax[0].set_title("Gains of the three-row constant-weight graph"); ax[0].legend(fontsize=7.5)
ax[1].semilogy(d, l3, "o-", color="#1f77b4")
ax[1].set_xlabel(r"$\delta$"); ax[1].set_ylabel(r"optimal third row $\ell_3=\lambda_3/n$")
ax[1].set_title("Optimal third-row fraction")
plt.tight_layout(); plt.savefig("figures/fig6_cw2.png", dpi=150); print("saved figures/fig6_cw2.png")
