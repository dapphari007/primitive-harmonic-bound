"""Fit R_t^2 = const * prod L^{e_L} by full least squares over a reduced dictionary (differences of the five
labels with small constants), round to integers, and verify exactly."""
import sys, json, itertools, math
import numpy as np
from fractions import Fraction
rows = [json.loads(l) for l in open("results/cw2_R_data.jsonl")]
rows = [r for r in rows if r[8] > 1e-14]
names = ["l1", "l2", "l3", "W", "p"]
forms = []
for c in range(-3, 4):
    for a in names: forms.append(((a,), c))
    for a, b in itertools.combinations(names, 2): forms.append(((a, "-" + b), c))
def form_str(f):
    (terms, c) = f
    s = terms[0] + "".join(t if t.startswith("-") else "+" + t for t in terms[1:])
    return f"({s}{c:+d})" if c else f"({s})"
def ev(f, v):
    (terms, c) = f; val = c
    for t in terms: val += -v[t[1:]] if t.startswith("-") else v[t]
    return val
results = {}
for r in (1, 2, 3):
    for t in (1, 2):
        data = [row for row in rows if row[5] == r and row[6] == t]
        V = [dict(zip(names, row[:5])) for row in data]
        y = np.array([math.log(row[8]) for row in data])
        keep = [i for i, f in enumerate(forms) if all(ev(f, v) != 0 for v in V)]
        X = np.array([[math.log(abs(ev(forms[i], v))) for i in keep] for v in V])
        A = np.hstack([np.ones((len(V), 1)), X])
        beta, res, rank, sv = np.linalg.lstsq(A, y, rcond=None)
        expo = beta[1:]; rounded = np.round(expo)
        pred = X @ rounded; c0 = np.mean(y - pred); resid = np.abs(y - pred - c0).max()
        cf = Fraction(math.exp(c0)).limit_denominator(1000)
        terms = " ".join(f"{form_str(forms[keep[k]])}^{int(e)}" for k, e in enumerate(rounded) if e != 0)
        print(f"(r={r},t={t}) rows={len(data)} feats={len(keep)} rank={rank} max|expo-round|={np.abs(expo-rounded).max():.3f} "
              f"verify-resid={resid:.1e}\n    R^2 = {cf} * {terms}")
        results[(r, t)] = (str(cf), [(form_str(forms[keep[k]]), int(e)) for k, e in enumerate(rounded) if e != 0], float(resid))
json.dump({f"{k[0]},{k[1]}": v for k, v in results.items()}, open("results/cw2_R_fit.json", "w"), indent=1)
