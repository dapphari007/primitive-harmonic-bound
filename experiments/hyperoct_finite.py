"""Finite-n two-row binary bound from the closed-form coefficients (box Omega in (j, a2, b2)), versus the
paper's one-row bound (23), at fixed delta.  usage: python hyperoct_finite.py p q n1,n2,..."""
import sys, math, time
sys.path.insert(0, __file__.rsplit("experiments", 1)[0])
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh
from phb.hyperoct_formulas import p_formula, target, admissible, MOVES
from phb.bound import perron, log2_sum_binom, log2_mk, log2_binom


def log2_f(m, a):
    if a == 0: return 0.0
    x = log2_binom(m, a); y = log2_binom(m, a - 1)
    return x + math.log2(1 - 2.0 ** (y - x))

def log2_dim(n, j, a2, b2):
    return log2_binom(n, j) + log2_f(n - j, a2) + log2_f(j, b2)

def two_row_bound(n, s, k, jlo, jhi, A, B):
    verts = [(j, a2, b2) for j in range(jlo, jhi + 1) for a2 in range(A + 1) for b2 in range(B + 1)
             if admissible(n - j - a2, a2, j - b2, b2, k)]
    if len(verts) < 2: return None, None
    idx = {v: i for i, v in enumerate(verts)}
    M = lil_matrix((len(verts), len(verts)))
    for (j, a2, b2), i in idx.items():
        a1, b1 = n - j - a2, j - b2
        for mv in MOVES:
            ta, tb = target(mv, a1, a2, b1, b2)
            if ta[2] or tb[2] or ta[0] < ta[1] or tb[0] < tb[1]: continue
            w = (tb[0] + tb[1], ta[1], tb[1])
            if w in idx and idx[w] > i:
                p = float(p_formula(mv, a1, a2, b1, b2, k))
                rev = {"a1->b1": "b1->a1", "a1->b2": "b2->a1", "a2->b1": "b1->a2", "a2->b2": "b2->a2",
                       "b1->a1": "a1->b1", "b1->a2": "a2->b1", "b2->a1": "a1->b2", "b2->a2": "a2->b2"}[mv]
                q = float(p_formula(rev, ta[0], ta[1], tb[0], tb[1], k))
                if p > 0 and q > 0:
                    M[i, idx[w]] = math.sqrt(p * q); M[idx[w], i] = math.sqrt(p * q)
    M = M.tocsr()
    lam = float(eigsh(M, k=1, which="LA", return_eigenvectors=False)[0]) if M.shape[0] > 2 else float(np.linalg.eigvalsh(M.toarray())[-1])
    if lam <= s: return None, lam
    terms = [log2_dim(n, *v) for v in verts]; mx = max(terms)
    lsum = mx + math.log2(sum(2.0 ** (t - mx) for t in terms))
    return math.log2((1 - s) / (lam - s)) + lsum - log2_mk(n, k), lam

def main():
  pp, qq = int(sys.argv[1]), int(sys.argv[2]); delta = pp / qq
  NS = [int(x) for x in sys.argv[3].split(",")]
  t0 = time.time()
  print(f"delta = {delta}")
  for n in NS:
      d = n * pp // qq
      s = 1 - 2 * d / n
      # paper's one-row (23): best over k, L near the asymptotic optimum
      best1 = (math.inf, None)
      for k in range(0, max(6, int(0.01 * n) + 6)):
          for L in range(k + 1, min(n - k, int(0.12 * n) + 20) + 1):
              lam = perron(n, k, L)
              if lam > s:
                  v = math.log2((1 - s) / (lam - s)) + log2_sum_binom(n, k, L) - log2_mk(n, k)
                  if v < best1[0]: best1 = (v, (k, L))
      k1, L1 = best1[1]
      # two-row boxes: k around k1, j-window around [.., L1], small second rows
      best2 = (math.inf, None, None)
      for k in range(max(1, k1 - 3), k1 + 6):
          for A in range(0, 3):
              for B in range(0, 4):
                  if A == 0 and B == 0: continue
                  for jhi in range(max(k + 2, L1 - 8), L1 + 12):
                      for jlo in [k, max(k, jhi - 40), max(k, jhi - 12), max(k, jhi - 4)]:
                          if jlo >= jhi: continue
                          v, lam = two_row_bound(n, s, k, jlo, jhi, A, B)
                          if v is not None and v < best2[0]: best2 = (v, (k, jlo, jhi, A, B), lam)
      gain = best1[0] - best2[0]
      print(f"n={n:>6} d={d:>5} | one-row (23): {best1[0]:11.3f} rate={best1[0]/n:.6f} (k,L)={best1[1]} | two-row: {best2[0]:11.3f} rate={best2[0]/n:.6f} box={best2[1]} Lambda={best2[2]:.5f} | gain={gain:+.3f} bits   [{time.time()-t0:.0f}s]", flush=True)

if __name__ == "__main__":
    main()
