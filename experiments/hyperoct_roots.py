"""For each (vertex, move): exact quadratic in k -> leading coefficient C and roots; then fit each root as an
integer linear form in (n, j, a2, b2) and the leading coefficient as a ratio of products of linear forms."""
import json, glob, sys, itertools, math
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import sympy
kk = sympy.symbols('k')
rows = []
for line in open("results/hyperoct_coeffs_n11.jsonl"):
    n, j, a2, b2, k, al, be, p = json.loads(line); rows.append((n, j, a2, b2, k, tuple(al), tuple(be), p))
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
    try: mt = move_type(n, j, a2, b2, al, be)
    except StopIteration: continue
    groups.setdefault((n, j, a2, b2, mt), {})[k] = sympy.Rational(F(p).limit_denominator(400000))
recs = {}  # move -> list of (n, j, a2, b2, C, roots)
for (n, j, a2, b2, mt), d in sorted(groups.items()):
    if len(d) < 3 or mt.endswith("3"): continue
    pts = sorted(d.items())
    poly = sympy.Poly(sympy.expand(sympy.interpolate(pts[:3], kk)), kk)
    if not all(poly.eval(k) == p for k, p in pts[3:]): 
        print("NOT QUADRATIC:", (n, j, a2, b2, mt)); continue
    if poly.is_zero: continue
    C = poly.LC(); roots = sympy.roots(poly.as_expr(), kk)
    rts = sorted([r for r, m in roots.items() for _ in range(m)])
    if len(rts) != 2 or not all(r.is_Integer for r in rts):
        print("odd roots:", (n, j, a2, b2, mt), poly.as_expr()); continue
    recs.setdefault(mt, []).append((n, j, a2, b2, C, int(rts[0]), int(rts[1])))
import numpy as np
print("move       #pts  root sum = n+1 ?   root fits (r = c0 + c1 n + c2 j + c3 a2 + c4 b2)")
for mt, L in sorted(recs.items()):
    A = np.array([[1, n, j, a2, b2] for n, j, a2, b2, C, r1, r2 in L], float)
    sums_ok = all(r1 + r2 == n + 1 for n, j, a2, b2, C, r1, r2 in L)
    # fit the smaller root and the larger root separately
    out = []
    for which in (5, 6):
        y = np.array([row[which] for row in L], float)
        sol, res, rk, sv = np.linalg.lstsq(A, y, rcond=None)
        sol_r = np.round(sol).astype(int)
        exact = np.all(A @ sol_r == y)
        out.append(f"{'r_min' if which == 5 else 'r_max'} = {sol_r.tolist()} exact={exact}")
    print(f"{mt:8s} {len(L):4d}  sum=n+1: {sums_ok}   " + " | ".join(out))
    # leading coefficient: try C = +-1/(n * D) with D a product of small linear forms; print C*n as fraction per point for inspection
    samples = [(n, j, a2, b2, sympy.nsimplify(C * n)) for n, j, a2, b2, C, r1, r2 in L][:14]
    print("      C*n samples (n,j,a2,b2 -> C*n):", ", ".join(f"({n},{j},{a2},{b2})->{c}" for n, j, a2, b2, c in samples))
