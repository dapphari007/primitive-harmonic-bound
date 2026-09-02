"""Figures for the research note."""
import sys, math
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from experiments.asymptotics import kappa_H, mrrw1, mrrw2, H2

# ---------- Figure 1: asymptotic exponents ----------
ds = np.linspace(0.005, 0.495, 200)
m1 = np.array([mrrw1(d) for d in ds]); m2 = np.array([mrrw2(d) for d in ds]); kh = np.array([kappa_H(d)[0] for d in ds])
gv = np.array([1 - H2(d) for d in ds])
fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
ax[0].plot(ds, gv, color="0.6", ls="--", label="Gilbert–Varshamov (lower)")
ax[0].plot(ds, m1, color="tab:blue", label="MRRW1")
ax[0].plot(ds, m2, color="tab:orange", label="MRRW2 (optimised)")
ax[0].plot(ds, kh, color="tab:red", lw=1.4, label=r"$\kappa_H(\delta)$  whole-cube, k>0")
ax[0].set_xlabel(r"relative distance $\delta$"); ax[0].set_ylabel("rate exponent"); ax[0].set_title("Asymptotic upper bounds on $R_2(\delta)$")
ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
ax[1].plot(ds, m1 - kh, color="tab:blue", label=r"MRRW1 $-\ \kappa_H$")
ax[1].plot(ds, m2 - kh, color="tab:orange", label=r"MRRW2 $-\ \kappa_H$")
ax[1].axhline(0, color="k", lw=.6); ax[1].axvline(0.19504, color="tab:red", ls=":", label=r"$\delta_0=0.19504$")
ax[1].set_xlabel(r"relative distance $\delta$"); ax[1].set_ylabel("gain in exponent"); ax[1].set_title("Gain of the primitive-harmonic exponent")
ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig("figures/fig1_exponents.png", dpi=150)

# ---------- Figure 2: finite-n crossover ----------
from phb.bound import perron, log2_sum_binom, log2_mk
def lb(n, s, k, L):
    if not (k <= L <= n - k): return math.inf
    lam = perron(n, k, L)
    if lam <= s: return math.inf
    return math.log2((1 - s) / (lam - s)) + log2_sum_binom(n, k, L) - log2_mk(n, k)
def argmin_1d(f, lo, hi, coarse=40):
    lo, hi = int(lo), int(hi); step = max(1, (hi - lo) // coarse); bx, bv = None, math.inf
    for x in range(lo, hi + 1, step):
        v = f(x)
        if v < bv: bx, bv = x, v
    if bx is None: return None, math.inf
    while step > 1:
        step = max(1, step // 4)
        for x in range(max(lo, bx - 4 * step), min(hi, bx + 4 * step) + 1, step):
            v = f(x)
            if v < bv: bx, bv = x, v
    return bx, bv
def series(p, q, mults):
    out = []
    delta = p / q
    for m in mults:
        n, d = q * m, p * m; s = 1 - 2 * d / n
        a0 = .5 - math.sqrt(delta * (1 - delta)); Lc = int(a0 * n); win = max(12, int(.02 * n))
        _, b0 = argmin_1d(lambda L: lb(n, s, 0, L), Lc - win, Lc + win)
        kmax = max(4, int(.006 * n) + 3)
        _, bk = argmin_1d(lambda k: argmin_1d(lambda L: lb(n, s, k, L), max(k, Lc - win), Lc + 2 * win)[1], 1, kmax, coarse=30)
        out.append((n, b0 / n, bk / n))
    return np.array(out)
fig, ax = plt.subplots(1, 3, figsize=(14, 4.3))
for a, (p, q, mults, lab) in zip(ax, [(1, 10, [3,4,5,6,8,10,15,20,30,50,100,200,500,1000,2000], "δ = 1/10"),
                                     (1, 4, [5,10,20,30,40,50,60,80,100,150,200,300,500,1000,2000,4000], "δ = 1/4"),
                                     (4, 13, [2,3,4,6,8,10,15,20,30,36,40,50,60,80,100,150,200,300,500,1000,2000], "δ = 4/13")]):
    S = series(p, q, mults); delta = p / q
    a.semilogx(S[:, 0], S[:, 1], "o-", ms=3, color="tab:blue", label="classical certificate (k = 0)")
    a.semilogx(S[:, 0], S[:, 2], "s-", ms=3, color="tab:red", label="primitive-harmonic (best k ≥ 1)")
    a.axhline(mrrw1(delta), color="tab:blue", ls="--", lw=.8, label="MRRW1 limit")
    a.axhline(mrrw2(delta), color="tab:orange", ls="--", lw=.8, label="MRRW2 limit")
    a.axhline(kappa_H(delta)[0], color="tab:red", ls="--", lw=.8, label=r"$\kappa_H$ limit")
    a.set_title(f"finite-length rate of the bound, {lab}"); a.set_xlabel("block length n"); a.set_ylabel("log2(bound)/n"); a.grid(alpha=.3)
    a.legend(fontsize=7)
fig.tight_layout(); fig.savefig("figures/fig2_finite_n.png", dpi=150)
print("figures written")
