"""Finite-n binary TWO-ROW representation-graph bound (Theorem 4.2 of the paper with G = B_n), using the
numerically computed transition coefficients, versus the paper's one-row bound (23) and the exact Delsarte LP.

Vertex set Omega = {(j, a2, b2): jlo <= j <= jhi, a2 <= A, b2 <= B, LR-admissible for mu = (n-k, k)}.
Symmetric edge weight sqrt(p(l->l') p(l'->l)); Lambda = lambda_max; bound = (1-s)/(d_mu (Lambda-s)) sum D_lambda.
usage: python hyperoct_bound.py n [A B]"""
import sys, math, time, itertools
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np
from phb.hyperoct import transition_coefficients, lr_contains, dim_V, f_two_row
from phb.exact_lp import exact_delsarte_lp
from phb.bound import perron, log2_sum_binom, log2_mk

n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
A = int(sys.argv[2]) if len(sys.argv) > 2 else 1
B = int(sys.argv[3]) if len(sys.argv) > 3 else 1
t0 = time.time()
cache = {}
def coeffs(j, a2, b2, k):
    key = (j, a2, b2, k)
    if key not in cache:
        res, tot = transition_coefficients(n, j, a2, b2, k)
        assert abs(tot - 1) < 1e-6, tot
        d = {}
        for (al, be), p in res.items():
            if al == "?": continue
            al = list(al) + [0, 0]; be = list(be) + [0, 0]
            if al[2] or be[2]: continue          # three-row targets never contain E_mu
            d[(sum(be[:2]), al[1], be[1])] = p     # target vertex (j', a2', b2')
        cache[key] = d
    return cache[key]

print(f"n={n}, second rows up to A={A}, B={B}")
print(f"{'d':>3} {'log2 LP':>9} | {'one-row (23) best':>18} {'(k,L)':>7} | {'two-row best':>13} {'(k, j-range, A, B)':>20} {'Lambda':>8} | {'gain bits':>9}")
for d in range(2, n + 1):
    s = 1 - 2 * d / n
    lp = math.log2(exact_delsarte_lp(n, d))
    # paper's one-row bound (23), best over k, L
    best1 = (math.inf, None)
    for k in range(0, n // 2 + 1):
        for L in range(k + 1, n - k + 1):
            lam = perron(n, k, L)
            if lam > s:
                v = math.log2((1 - s) / (lam - s)) + log2_sum_binom(n, k, L) - log2_mk(n, k)
                if v < best1[0]: best1 = (v, (k, L))
    # two-row graph, best over k and j-window
    best2 = (math.inf, None, None)
    for k in range(1, n // 2 + 1):
        verts_all = [(j, a2, b2) for j in range(0, n + 1) for a2 in range(A + 1) for b2 in range(B + 1)
                     if lr_contains(n, j, a2, b2, k) and a2 <= (n - j) // 2 and b2 <= j // 2]
        js = sorted({v[0] for v in verts_all})
        for jlo in js:
            for jhi in js:
                if jhi < jlo: continue
                verts = [v for v in verts_all if jlo <= v[0] <= jhi]
                if len(verts) < 2: continue
                idx = {v: i for i, v in enumerate(verts)}
                J = np.zeros((len(verts), len(verts)))
                for v in verts:
                    for w, p in coeffs(*v, k).items():
                        if w in idx:
                            q = coeffs(*w, k).get(v, 0.0)
                            J[idx[v], idx[w]] = math.sqrt(max(p, 0) * max(q, 0))
                lam = float(np.linalg.eigvalsh(J)[-1])
                if lam > s:
                    Dsum = sum(dim_V(n, *v) for v in verts)
                    val = math.log2((1 - s) / (lam - s)) + math.log2(Dsum) - math.log2(f_two_row(n, k))
                    if val < best2[0]: best2 = (val, (k, jlo, jhi, A, B), lam)
    gain = best1[0] - best2[0] if math.isfinite(best2[0]) else float("nan")
    print(f"{d:>3} {lp:9.4f} | {best1[0]:18.4f} {str(best1[1]):>7} | {best2[0]:13.4f} {str(best2[1]):>20} {best2[2] if best2[2] else float('nan'):8.4f} | {gain:+9.4f}   [{time.time()-t0:.0f}s]", flush=True)
