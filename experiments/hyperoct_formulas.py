"""Closed forms for the binary two-row transition coefficients.
Each p = sgn * C * (k - r)(n+1-r-k).  (1) find a linear form r(a1,a2,b1,b2) with r in {roots} at every point;
(2) mine |C n| as a product of small linear forms in (a1, a2, b1, b2) by OMP on logs, verify exactly."""
import json, sys, itertools, math
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np, sympy
kk = sympy.symbols('k')
rows = [json.loads(l) for l in open("results/hyperoct_coeffs_n11.jsonl")]
def move_type(n, j, a2, b2, al, be):
    alpha = [n - j - a2, a2]; beta = [j - b2, b2]; al = list(al) + [0, 0]; be = list(be) + [0, 0]
    if sum(be[:3]) == j + 1:
        ra = next(r for r in range(2) if alpha[r] - 1 == al[r] and all(alpha[q] == al[q] for q in range(2) if q != r))
        rb = next(r for r in range(3) if (beta + [0])[r] + 1 == be[r] and all((beta + [0])[q] == be[q] for q in range(3) if q != r))
        return f"a{ra+1}->b{rb+1}"
    rb = next(r for r in range(2) if beta[r] - 1 == be[r] and all(beta[q] == be[q] for q in range(2) if q != r))
    ra = next(r for r in range(3) if (alpha + [0])[r] + 1 == al[r] and all((alpha + [0])[q] == al[q] for q in range(3) if q != r))
    return f"b{rb+1}->a{ra+1}"
groups = {}
for n, j, a2, b2, k, al, be, p in rows:
    try: mt = move_type(n, j, a2, b2, tuple(al), tuple(be))
    except StopIteration: continue
    groups.setdefault((n, j, a2, b2, mt), {})[k] = sympy.Rational(F(p).limit_denominator(400000))
recs = {}
for (n, j, a2, b2, mt), d in sorted(groups.items()):
    if len(d) < 3 or mt.endswith("3"): continue
    pts = sorted(d.items())
    poly = sympy.Poly(sympy.expand(sympy.interpolate(pts[:3], kk)), kk)
    if not all(poly.eval(k) == p for k, p in pts[3:]) or poly.is_zero: continue
    rts = sympy.roots(poly.as_expr(), kk)
    rl = sorted([int(r) for r, m in rts.items() for _ in range(m)])
    if len(rl) != 2: continue
    a1, b1 = n - j - a2, j - b2
    recs.setdefault(mt, []).append(dict(n=n, j=j, a1=a1, a2=a2, b1=b1, b2=b2, C=poly.LC(), roots=rl))
# linear-form candidates in (a1, a2, b1, b2) with constant
lin = []
for c in itertools.product([-1, 0, 1, 2], repeat=4):
    for c0 in range(-2, 4):
        if any(c): lin.append((c0,) + c)
def ev(f, r): return f[0] + f[1]*r['a1'] + f[2]*r['a2'] + f[3]*r['b1'] + f[4]*r['b2']
def lab(f):
    names = ["a1", "a2", "b1", "b2"]; s = ([str(f[0])] if f[0] else []) + [(f"{c}*" if c != 1 else "") + v for c, v in zip(f[1:], names) if c]
    return "+".join(s).replace("+-", "-")
for mt, L in sorted(recs.items()):
    # (1) root linear form
    root_forms = [f for f in lin if all(ev(f, r) in r['roots'] for r in L)]
    root_forms = sorted(root_forms, key=lambda f: sum(abs(x) for x in f))
    # (2) |C n| mining
    y = np.array([math.log(abs(float(r['C'])) * r['n']) for r in L])
    usable = [f for f in lin if all(ev(f, r) > 0 for r in L) and f != (1, 0, 0, 0, 0)]
    A = np.array([[math.log(ev(f, r)) for f in usable] for r in L])
    chosen, resid = [], y.copy()
    for _ in range(6):
        corr = (A.T @ resid) / (np.linalg.norm(A, axis=0) + 1e-12)
        i = int(np.argmax(np.abs(corr)))
        if i in chosen: break
        chosen.append(i); sol, *_ = np.linalg.lstsq(A[:, chosen], y, rcond=None); resid = y - A[:, chosen] @ sol
        if np.linalg.norm(resid) < 1e-9: break
    sol, *_ = np.linalg.lstsq(A[:, chosen], y, rcond=None); ex = [int(round(s)) for s in sol]
    def Cn_formula(r):
        v = F(1)
        for i, e in zip(chosen, ex): v *= F(ev(usable[i], r)) ** e
        return v
    exact = all(Cn_formula(r) == F(abs(r['C']) * r['n']).limit_denominator(10**6) for r in L)
    sign = {float(np.sign(r['C'])) for r in L}
    print(f"{mt}: {len(L)} vertices; root forms: {[lab(f) for f in root_forms[:4]]}; |C|n = {' * '.join(f'({lab(usable[i])})^{e}' if e != 1 else f'({lab(usable[i])})' for i, e in zip(chosen, ex) if e)}  exact={exact}  sign(C)={sign}  resid={np.linalg.norm(resid):.1e}")
