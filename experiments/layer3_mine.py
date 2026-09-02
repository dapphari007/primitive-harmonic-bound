"""Structured mining of CW2 off-diagonal coefficients as products of linear forms in (l1, l2, l3, w, p)."""
import json, sys, itertools, math
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np
rows = [json.loads(l) for l in open("results/layer3_coeffs_n12.jsonl")]
def mtype(lam, tgt):
    d = [t - s for s, t in zip(lam, tgt)]
    if all(x == 0 for x in d): return "self"
    r = d.index(-1) + 1; s = d.index(1) + 1
    return f"{r}->{s}"
data = {}
for n, w, p, lam, tgt, pv, fr in rows:
    mt = mtype(lam, tgt)
    if mt == "self": continue
    data.setdefault(mt, []).append((n, w, p, lam[0], lam[1], lam[2], F(fr)))
# candidate linear forms: c0 + c1 l1 + c2 l2 + c3 l3 + c4 w + c5 p, coefficients in {-1,0,1}, at most 3 nonzero, c0 in -3..3
cands = []
for c in itertools.product([-1, 0, 1], repeat=5):
    nz = sum(1 for x in c if x); 
    if nz == 0 or nz > 3: continue
    if next(x for x in c if x) < 0: continue
    for c0 in range(-3, 4):
        cands.append((c0,) + c)
def ev(f, r): return f[0] + f[1]*r[3] + f[2]*r[4] + f[3]*r[5] + f[4]*r[1] + f[5]*r[2]
def lab(f):
    names = ["l1", "l2", "l3", "w", "p"]
    s = ([str(f[0])] if f[0] else []) + [("-" if c == -1 else "") + v for c, v in zip(f[1:], names) if c]
    return "(" + "+".join(s).replace("+-", "-") + ")"
print("candidates:", len(cands))
for mt, L in sorted(data.items()):
    pos = [r for r in L if r[6] > 0]
    zero = [r for r in L if r[6] == 0]
    usable = [f for f in cands if all(ev(f, r) > 0 for r in pos)]
    y = np.array([math.log(float(r[6])) for r in pos])
    A = np.array([[math.log(ev(f, r)) for f in usable] for r in pos])
    # greedy OMP with re-fitting, up to 9 factors
    chosen, resid = [], y.copy()
    for _ in range(9):
        corr = (A.T @ resid) / (np.linalg.norm(A, axis=0) + 1e-12)
        i = int(np.argmax(np.abs(corr)))
        if i in chosen: break
        chosen.append(i); sol, *_ = np.linalg.lstsq(A[:, chosen], y, rcond=None); resid = y - A[:, chosen] @ sol
        if np.linalg.norm(resid) < 1e-9: break
    sol, *_ = np.linalg.lstsq(A[:, chosen], y, rcond=None); ex = [int(round(s)) for s in sol]
    # exact check with a rational constant fitted from the first point
    def prod(r):
        v = F(1)
        for i, e in zip(chosen, ex): v *= F(ev(usable[i], r)) ** e
        return v
    const = pos[0][6] / prod(pos[0])
    exact = all(const * prod(r) == r[6] for r in pos)
    print(f"{mt}: {len(L)} points ({len(pos)} positive, {len(zero)} zero) resid={np.linalg.norm(resid):.1e} exact={exact}  const={const}")
    print("     p =", const, "*", " * ".join(f"{lab(usable[i])}^{e}" if e != 1 else lab(usable[i]) for i, e in zip(chosen, ex) if e))
