"""Mine closed forms R_t^2 = const * prod L_k^{e_k} over a dictionary of linear forms, per (r, t) class."""
import sys, json, itertools, math
import numpy as np
sys.path.insert(0, ".")

rows = [json.loads(l) for l in open("results/cw2_R_data.jsonl")]
print("rows", len(rows))

def variables(l1, l2, l3, W, p):
    N = l1 + l2 + l3 - W - p
    return dict(l1=l1, l2=l2, l3=l3, W=W, p=p, N=N, w=W + p, n=l1 + l2 + l3)

names = ["l1", "l2", "l3", "W", "p", "N", "w", "n"]
forms = []
for c in range(-4, 5):
    for a in names:
        forms.append(((a,), c))
    for a, b in itertools.combinations(names, 2):
        forms.append(((a, "-" + b), c))
def form_str(f):
    (terms, c) = f
    s = terms[0] + "".join(t if t.startswith("-") else "+" + t for t in terms[1:])
    return f"({s}{c:+d})" if c else f"({s})"
def eval_form(f, v):
    (terms, c) = f
    val = c
    for t in terms:
        val += -v[t[1:]] if t.startswith("-") else v[t]
    return val

def omp(X, y, maxk=14, tol=1e-9):
    n, m = X.shape
    S = []
    ones = np.ones((n, 1))
    def fit(S):
        A = np.hstack([ones, X[:, S]]) if S else ones
        beta, *_ = np.linalg.lstsq(A, y, rcond=None)
        return beta, y - A @ beta
    beta, res = fit(S)
    while len(S) < maxk and np.sqrt(np.mean(res ** 2)) > tol:
        Xc = X - X.mean(axis=0)
        corr = np.abs(Xc.T @ res) / (np.linalg.norm(Xc, axis=0) + 1e-300)
        corr[S] = -1
        k = int(np.argmax(corr)); S.append(k)
        beta, res = fit(S)
    return S, beta, res

for r in (1, 2, 3):
    for t in (1, 2):
        data = [row for row in rows if row[5] == r and row[6] == t and row[8] > 1e-14]
        if len(data) < 30:
            print(f"(r={r},t={t}): only {len(data)} rows, skipped"); continue
        V = [variables(*row[:5]) for row in data]
        y = np.array([math.log(row[8]) for row in data])
        keep = [i for i, f in enumerate(forms) if all(eval_form(f, v) != 0 for v in V)]
        X = np.array([[math.log(abs(eval_form(forms[i], v))) for i in keep] for v in V])
        S, beta, res = omp(X, y)
        expo = beta[1:]
        rounded = np.round(expo)
        # refit with integer exponents, constant only
        pred = X[:, S] @ rounded
        c0 = np.mean(y - pred); res_int = y - pred - c0
        const = math.exp(c0)
        from fractions import Fraction
        cf = Fraction(const).limit_denominator(1000)
        terms = " ".join(f"{form_str(forms[keep[k]])}^{int(e)}" for k, e in zip(S, rounded) if e != 0)
        print(f"(r={r},t={t}) rows={len(data)} omp-rms={np.sqrt(np.mean(res**2)):.1e} int-max-res={np.abs(res_int).max():.1e} "
              f"max|expo-round|={np.abs(expo-rounded).max():.3f}\n    R^2 = {cf} * {terms}")
