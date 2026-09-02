"""Formula mining for the binary two-row transition coefficients.
Hypothesis: each move-type coefficient is a product of small linear forms in (n, j, k, a2, b2) with integer
exponents.  Least squares on logarithms over all data points with p > 0, round to integers, then verify EXACTLY
(as fractions) on every data point, including the p = 0 points (the formula must vanish there)."""
import json, sys, glob, itertools, math
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np

rows = []
for f in glob.glob("results/hyperoct_coeffs_n*.jsonl"):
    for line in open(f):
        n, j, a2, b2, k, al, be, p = json.loads(line)
        rows.append((n, j, a2, b2, k, tuple(al), tuple(be), p))
print("data rows:", len(rows))

def move_type(n, j, a2, b2, al, be):
    alpha = [n - j - a2, a2]; beta = [j - b2, b2]
    al = list(al) + [0, 0]; be = list(be) + [0, 0]
    if sum(be[:3]) == j + 1:  # alpha -> beta
        ra = next(r for r in range(2) if alpha[r] - 1 == al[r] and all(alpha[q] == al[q] for q in range(2) if q != r))
        rb = next(r for r in range(3) if (beta + [0])[r] + 1 == be[r] and all((beta + [0])[q] == be[q] for q in range(3) if q != r))
        return f"a{ra+1}->b{rb+1}"
    else:
        rb = next(r for r in range(2) if beta[r] - 1 == be[r] and all(beta[q] == be[q] for q in range(2) if q != r))
        ra = next(r for r in range(3) if (alpha + [0])[r] + 1 == al[r] and all((alpha + [0])[q] == al[q] for q in range(3) if q != r))
        return f"b{rb+1}->a{ra+1}"

# candidate linear forms  c0 + c1 n + c2 j + c3 k + c4 a2 + c5 b2  with small coefficients
cands = {}
names = ["n", "j", "k", "a2", "b2"]
for coeffs in itertools.product([-2, -1, 0, 1, 2], repeat=5):
    if all(c == 0 for c in coeffs):
        continue
    # keep "reduced" forms: first nonzero coefficient positive
    fnz = next(c for c in coeffs if c != 0)
    if fnz < 0:
        continue
    if sum(abs(c) for c in coeffs) > 4:
        continue
    for c0 in [-3, -2, -1, 0, 1, 2, 3]:
        key = (c0,) + coeffs
        lab = "+".join(([str(c0)] if c0 else []) + [f"{c}{v}" if c != 1 else v for c, v in zip(coeffs, names) if c != 0])
        cands[key] = lab
print("candidate linear forms:", len(cands))
keys = list(cands.keys())

def evalf(key, n, j, k, a2, b2):
    c0, cn, cj, ck, ca, cb = key
    return c0 + cn * n + cj * j + ck * k + ca * a2 + cb * b2

by_type = {}
for r in rows:
    n, j, a2, b2, k, al, be, p = r
    try:
        mt = move_type(n, j, a2, b2, al, be)
    except StopIteration:
        continue
    by_type.setdefault(mt, []).append((n, j, k, a2, b2, p))

for mt, data in sorted(by_type.items()):
    pos = [d for d in data if d[5] > 1e-9]
    if len(pos) < 8:
        print(f"{mt}: only {len(pos)} positive points, skipped"); continue
    # design matrix: columns = candidate forms nonzero on ALL positive points
    usable = [key for key in keys if all(evalf(key, *d[:5]) != 0 for d in pos)]
    A = np.array([[math.log(abs(evalf(key, *d[:5]))) for key in usable] for d in pos])
    y = np.array([math.log(d[5]) for d in pos])
    # sparse-ish solve: orthogonal matching pursuit over the candidate columns
    best = None
    residual = y.copy(); chosen = []
    for _ in range(8):
        corr = A.T @ residual / (np.linalg.norm(A, axis=0) + 1e-12)
        i = int(np.argmax(np.abs(corr)))
        if i in chosen: break
        chosen.append(i)
        sol, *_ = np.linalg.lstsq(A[:, chosen], y, rcond=None)
        residual = y - A[:, chosen] @ sol
        if np.linalg.norm(residual) < 1e-8 * max(1, np.linalg.norm(y)):
            break
    sol, *_ = np.linalg.lstsq(A[:, chosen], y, rcond=None)
    expo = [int(round(x)) for x in sol]
    # exact verification
    def formula(n, j, k, a2, b2):
        val = Fraction(1)
        for i, e in zip(chosen, expo):
            f = evalf(usable[i], n, j, k, a2, b2)
            if e < 0 and f == 0: return None
            val *= Fraction(f) ** e
        return val
    ok = True; bad = 0
    for d in data:
        v = formula(*d[:5])
        target = Fraction(d[5]).limit_denominator(100000)
        if v is None or abs(v - target) > Fraction(1, 10**6):
            ok = False; bad += 1
    terms = " * ".join(f"({cands[usable[i]]})^{e}" if e != 1 else f"({cands[usable[i]]})" for i, e in zip(chosen, expo) if e != 0)
    print(f"{mt}: {len(data)} points ({len(pos)} positive)  residual={np.linalg.norm(residual):.2e}  exact={ok} (bad={bad})\n      p = {terms}")
