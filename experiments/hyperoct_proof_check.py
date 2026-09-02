"""PROOF CHECK for the eight closed forms.
(1) Edmonds' four 6j formulas with a spin-1/2 entry, validated against sympy's wigner_6j on all valid triangles.
(2) Symbolic identity:  (|alpha|/n) (f^{alpha-box_r}/f^alpha) (2 j_alpha+1)(2 j_nu+1) {j_beta 1/2 j_nu; j_alpha' J j_alpha}^2
    equals the closed form, as an identity of rational functions of integer a1, a2, b1, b2, k, for all eight moves."""
import sympy as sp
from sympy import Rational as R, sqrt, symbols, simplify
from sympy.physics.wigner import wigner_6j

def edmonds(a, b, c, e, f):
    """{a b c; 1/2 e f}, e = c +- 1/2, f = b +- 1/2  (Edmonds 1957, Table 5, plus 6j symmetries)."""
    s = a + b + c; h = R(1, 2)
    if e == c - h and f == b + h:
        return (-1) ** s * sqrt((s - 2*b) * (s - 2*c + 1) / ((2*b + 1) * (2*b + 2) * (2*c) * (2*c + 1)))
    if e == c - h and f == b - h:
        return (-1) ** s * sqrt((s + 1) * (s - 2*a) / ((2*b) * (2*b + 1) * (2*c) * (2*c + 1)))
    if e == c + h and f == b + h:
        bb, cc = c + h, b + h; ss = a + bb + cc
        return (-1) ** ss * sqrt((ss + 1) * (ss - 2*a) / ((2*bb) * (2*bb + 1) * (2*cc) * (2*cc + 1)))
    if e == c + h and f == b - h:
        bb, cc = c, b; ss = a + bb + cc
        return (-1) ** ss * sqrt((ss - 2*bb) * (ss - 2*cc + 1) / ((2*bb + 1) * (2*bb + 2) * (2*cc) * (2*cc + 1)))
    raise ValueError((a, b, c, e, f))

def tri(x, y, z):
    return abs(x - y) <= z <= x + y and (x + y + z) % 1 == 0

worst = 0; cnt = 0
for twoa in range(0, 11):
    for twob in range(0, 11):
        for twoc in range(0, 11):
            a, b, c = R(twoa, 2), R(twob, 2), R(twoc, 2)
            for e, f in [(c - R(1,2), b + R(1,2)), (c - R(1,2), b - R(1,2)), (c + R(1,2), b + R(1,2)), (c + R(1,2), b - R(1,2))]:
                if e < 0 or f < 0 or not (tri(a, b, c) and tri(a, e, f) and tri(R(1,2), b, f) and tri(R(1,2), e, c)): continue
                w = wigner_6j(a, b, c, R(1,2), e, f); t = edmonds(a, b, c, e, f)
                worst = max(worst, abs(sp.N(t**2 - w**2, 30))); cnt += 1
print(f"(1) Edmonds table vs wigner_6j on {cnt} valid symbols: max |difference of squares| = {worst}")

a1, a2, b1, b2, k = symbols('a1 a2 b1 b2 k', integer=True, positive=True)
n = a1 + a2 + b1 + b2
N = n * (a1 + 1 - a2) * (b1 + 1 - b2)
closed = {
 "a1->b1": (a1 + 1) * (a1 + b2 - k) * (a2 + b1 + 1 - k) / N,
 "a1->b2": (a1 + 1) * (k - a2 - b2) * (a1 + b1 + 1 - k) / N,
 "a2->b1": a2 * (k - a2 - b2 + 1) * (a1 + b1 + 2 - k) / N,
 "a2->b2": a2 * (a2 + b1 - k) * (a1 + b2 + 1 - k) / N,
 "b1->a1": (b1 + 1) * (a2 + b1 - k) * (a1 + b2 + 1 - k) / N,
 "b1->a2": (b1 + 1) * (k - a2 - b2) * (a1 + b1 + 1 - k) / N,
 "b2->a1": b2 * (k - a2 - b2 + 1) * (a1 + b1 + 2 - k) / N,
 "b2->a2": b2 * (a1 + b2 - k) * (a2 + b1 + 1 - k) / N,
}
def fdim(x1, x2):  # dim S^(x1,x2) = C(x1+x2, x2) (x1-x2+1)/(x1+1)
    return sp.binomial(x1 + x2, x2) * (x1 - x2 + 1) / (x1 + 1)
J = n / 2 - k; ja = (a1 - a2) / 2; jb = (b1 - b2) / 2
def pred(move):
    src, dst = move.split("->"); r, rp = int(src[1]), int(dst[1]); h = R(1, 2)
    if src[0] == "a":
        m, after = a1 + a2, ((a1 - 1, a2) if r == 1 else (a1, a2 - 1))
        branch = (m / n) * fdim(*after) / fdim(a1, a2)
        j_src, j_src2 = ja, (ja - h if r == 1 else ja + h)
        j_oth, j_nu = jb, (jb + h if rp == 1 else jb - h)
    else:
        m, after = b1 + b2, ((b1 - 1, b2) if r == 1 else (b1, b2 - 1))
        branch = (m / n) * fdim(*after) / fdim(b1, b2)
        j_src, j_src2 = jb, (jb - h if r == 1 else jb + h)
        j_oth, j_nu = ja, (ja + h if rp == 1 else ja - h)
    # {j_oth 1/2 j_nu ; j_src2 J j_src} = {J j_src2 j_nu ; 1/2 j_oth j_src}   (6j symmetries)
    w = edmonds(J, j_src2, j_nu, j_oth, j_src)
    return branch * (2 * j_src + 1) * (2 * j_nu + 1) * w ** 2
allok = True
for mv, cf in closed.items():
    expr = sp.expand_func(pred(mv))
    diff = simplify(sp.combsimp(expr) - cf)
    diff = simplify(diff.subs({(-1)**(2*a1): 1}))
    ok = (diff == 0)
    allok &= ok
    print(f"(2) {mv}: identity holds symbolically: {ok}" + ("" if ok else f"   residual = {diff}"))
print("ALL EIGHT IDENTITIES PROVED SYMBOLICALLY:", allok)

# (3) the two identities of the paper's Theorem 4.2, now as symbolic identities of rational functions
print("(3) symbolic identities")
def dimV(x1, x2, y1, y2):   # dim V_(alpha,beta) = C(n, |beta|) f^alpha f^beta
    return sp.binomial(x1 + x2 + y1 + y2, y1 + y2) * fdim(x1, x2) * fdim(y1, y2)
# sum-to-one (all eight targets; a target outside the admissible region contributes a formula value that is
# negative or zero there, so the identity is stated as a polynomial identity valid on the interior)
tot = simplify(sum(closed.values()))
print("    sum of the eight coefficients =", tot)
targets = {"a1->b1": (a1-1, a2, b1+1, b2), "a1->b2": (a1-1, a2, b1, b2+1), "a2->b1": (a1, a2-1, b1+1, b2), "a2->b2": (a1, a2-1, b1, b2+1),
           "b1->a1": (a1+1, a2, b1-1, b2), "b1->a2": (a1, a2+1, b1-1, b2), "b2->a1": (a1+1, a2, b1, b2-1), "b2->a2": (a1, a2+1, b1, b2-1)}
rev = {"a1->b1": "b1->a1", "a1->b2": "b2->a1", "a2->b1": "b1->a2", "a2->b2": "b2->a2"}
allrec = True
for mv, rv in rev.items():
    x1, x2, y1, y2 = targets[mv]
    rhs = closed[rv].subs({a1: x1, a2: x2, b1: y1, b2: y2}, simultaneous=True) * dimV(x1, x2, y1, y2)
    lhs = closed[mv] * dimV(a1, a2, b1, b2)
    d = simplify(sp.combsimp(sp.expand_func(lhs - rhs)))
    allrec &= (d == 0)
    print(f"    reciprocity D_lambda p({mv}) = D_lambda' p({rv}):", d == 0)
print("    reciprocity proved symbolically for all four edge types:", allrec)
