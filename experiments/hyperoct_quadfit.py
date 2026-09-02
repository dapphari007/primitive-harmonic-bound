"""For each (n, j, a2, b2, move), fit p(k) by an exact quadratic in k through the data; report the quadratic's
coefficients as fractions and check extra points."""
import json, glob, sys
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
rows = []
for f in sorted(set(glob.glob("results/hyperoct_coeffs_n11.jsonl"))):
    for line in open(f):
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
    groups.setdefault((n, j, a2, b2, mt), {})[k] = F(p).limit_denominator(200000)
def quad_through(pts):
    (k0, p0), (k1, p1), (k2, p2) = pts[:3]
    # Lagrange -> coefficients c0 + c1 k + c2 k^2
    import sympy
    kk = sympy.symbols('k')
    poly = sympy.interpolate([(k0, sympy.Rational(p0.numerator, p0.denominator)), (k1, sympy.Rational(p1.numerator, p1.denominator)), (k2, sympy.Rational(p2.numerator, p2.denominator))], kk)
    return sympy.Poly(sympy.expand(poly), kk)
import sympy
kk = sympy.symbols('k')
print("groups with >= 4 k-values (fit quadratic on 3, check the rest):")
for key, d in sorted(groups.items()):
    if len(d) >= 4:
        pts = sorted(d.items())
        poly = quad_through(pts)
        ok = all(poly.eval(k) == sympy.Rational(p.numerator, p.denominator) for k, p in pts[3:])
        n, j, a2, b2, mt = key
        print(f"n={n} j={j} a2={a2} b2={b2} {mt:7s}: k-values {[k for k,_ in pts]}  quadratic ok={ok}   p(k) = {sympy.factor(poly.as_expr())}")
