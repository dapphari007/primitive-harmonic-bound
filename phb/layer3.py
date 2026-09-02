r"""
Constant-weight layer with THREE-ROW ambient representations ("CW2").

Setting (paper, Section 3, with the general projection bound Theorem 4.2):
  X = X_w (w-subsets of [n]), G = S_n, stabilizer of a support x: H = S_w x S_N (N = n - w),
  coordinate vector ell_x = sqrt(n/(wN)) (1_x - (w/n) 1) in R^n (unit, orthogonal to 1),
  stabilizer irrep E = E_p(x) (x) triv = S^{(w-p,p)} boxtimes S^{(N)}  (complement degree q = 0),
  ambient irreps S^lambda with c^lambda_{(w-p,p),(N)} = 1  <=>  lambda / (w-p,p) is a horizontal N-strip
      <=>  lambda = (l1, l2, l3) with  l3 <= p <= l2 <= w - p <= l1,  l1 + l2 + l3 = n.
  The paper's path is l3 = 0 (Johnson degrees j = l2, p <= j <= w - p); the extension is l3 > 0.
  Transitions: R^n (x) S^lambda = Ind_{S_{n-1}} Res S^lambda = (+) S^{lambda - box + box} (self-loop lambda -> lambda
  with multiplicity #corners - 1 after removing the trivial summand; ell_x is orthogonal to 1 so that summand is inert).

Numerics: S^lambda realised inside the permutation module M^lambda on ordered set partitions (T1, T2, T3) as the
constituent with the smallest content sum (dominance); E-copy by S_w x S_N class sums; constituent projections of
ell_x (x) v in R^n (x) M^lambda by S_n class sums (contents), exact Lagrange interpolation on the known eigenvalues.
p(lambda -> lambda') = || proj_{lambda'} (ell_x (x) v) ||^2 / ||v||^2.
"""
from __future__ import annotations

import itertools
import math
from functools import lru_cache

import numpy as np


def content(shape) -> int:
    return sum(c - r for r, row in enumerate(shape) for c in range(row))


def content2(shape) -> int:
    return sum((c - r) ** 2 for r, row in enumerate(shape) for c in range(row))


def hook_dim(shape) -> int:
    n = sum(shape)
    shape = [x for x in shape if x > 0]
    conj = [sum(1 for r in shape if r > c) for c in range(shape[0])] if shape else []
    h = 1
    for r, row in enumerate(shape):
        for c in range(row):
            h *= (row - c - 1) + (conj[c] - r - 1) + 1
    return math.factorial(n) // h


def partitions_le_rows(n: int, rows: int):
    out = []
    def rec(rem, maxpart, cur):
        if rem == 0:
            out.append(tuple(cur)); return
        if len(cur) == rows:
            return
        for part in range(min(rem, maxpart), 0, -1):
            rec(rem - part, part, cur + [part])
    rec(n, n, [])
    return out


def admissible(n, w, p, lam) -> bool:
    l = list(lam) + [0, 0, 0]
    l1, l2, l3 = l[:3]
    return l1 + l2 + l3 == n and l1 >= l2 >= l3 >= 0 and l3 <= p <= l2 <= w - p <= l1 and sum(l[3:]) == 0


def box_moves(lam):
    """All lambda' = lambda - box + box (including lambda itself), as 3-row tuples, weakly decreasing, nonneg."""
    l = list(lam) + [0] * (3 - len(lam))
    out = set()
    for r in range(3):
        if l[r] == 0 or (r < 2 and l[r] == l[r + 1] and False):
            pass
        rem = l.copy(); rem[r] -= 1
        if rem[r] < 0 or (r < 2 and rem[r] < rem[r + 1]):
            continue
        for s in range(3):
            add = rem.copy(); add[s] += 1
            if s > 0 and add[s] > add[s - 1]:
                continue
            out.add(tuple(add))
    return sorted(out, reverse=True)


class PermModule3:
    """M^lambda: functions on ordered set partitions (T1, T2, T3) of [n], |Ti| = lambda_i; flat basis by key."""

    def __init__(self, n: int, lam):
        l = list(lam) + [0] * (3 - len(lam))
        self.n = n; self.lam = tuple(l)
        T2s, T3s = [], []
        for T2 in itertools.combinations(range(n), l[1]):
            m2 = sum(1 << e for e in T2)
            rest = [e for e in range(n) if not (m2 >> e) & 1]
            for T3 in itertools.combinations(rest, l[2]):
                m3 = sum(1 << e for e in T3)
                T2s.append(m2); T3s.append(m3)
        self.T2 = np.array(T2s, dtype=np.int64); self.T3 = np.array(T3s, dtype=np.int64)
        self.keys = (self.T2 << n) | self.T3
        order = np.argsort(self.keys)
        self.T2, self.T3, self.keys = self.T2[order], self.T3[order], self.keys[order]
        self.dim = self.keys.size

    def index(self, T2, T3):
        k = (T2.astype(np.int64) << self.n) | T3.astype(np.int64)
        idx = np.searchsorted(self.keys, k)
        assert np.all(self.keys[idx] == k)
        return idx

    @staticmethod
    def apply_perm_mask(mask, sigma):
        out = np.zeros_like(mask)
        for b, sb in enumerate(sigma):
            out |= ((mask >> b) & 1) << int(sb)
        return out

    def perm_src(self, sigma) -> np.ndarray:
        img = self.index(self.apply_perm_mask(self.T2, sigma), self.apply_perm_mask(self.T3, sigma))
        src = np.empty(self.dim, dtype=np.int64); src[img] = np.arange(self.dim)
        return src

    @lru_cache(maxsize=None)
    def transposition_src(self, i, l):
        sigma = np.arange(self.n); sigma[i], sigma[l] = l, i
        return self.perm_src(sigma)

    @lru_cache(maxsize=None)
    def three_cycle_src(self, i, l, m):
        sigma = np.arange(self.n); sigma[i], sigma[l], sigma[m] = l, m, i
        return self.perm_src(sigma)

    def class_sum_2(self, v, subset=None):
        """sum of transpositions (i l) with i, l in subset (default: all)."""
        S = range(self.n) if subset is None else sorted(subset)
        out = np.zeros_like(v)
        for a, i in enumerate(S):
            for l in S[a + 1:]:
                out += v[self.transposition_src(i, l)]
        return out

    def class_sum_3(self, v, subset=None):
        S = range(self.n) if subset is None else sorted(subset)
        out = np.zeros_like(v)
        for i, l, m in itertools.permutations(S, 3):
            if i < l and i < m:
                out += v[self.three_cycle_src(i, l, m)]
        return out


def lagrange_project(op, v, target, others):
    w = v.copy()
    for t in others:
        if abs(t - target) < 1e-9:
            continue
        w = (op(w) - t * w) / (target - t)
    return w


class TensorRM:
    """R^n (x) M^lambda, flat index q * dim + e, S_n acting diagonally."""

    def __init__(self, M: PermModule3):
        self.M = M; self.n = M.n
        self.q = np.repeat(np.arange(self.n), M.dim); self.e = np.tile(np.arange(M.dim), self.n)

    @lru_cache(maxsize=None)
    def transposition_src(self, i, l):
        srcM = self.M.transposition_src(i, l)
        qs = np.arange(self.n); qs[i], qs[l] = l, i
        return qs[self.q] * self.M.dim + srcM[self.e]

    @lru_cache(maxsize=None)
    def three_cycle_src(self, i, l, m):
        srcM = self.M.three_cycle_src(i, l, m)
        sigma = np.arange(self.n); sigma[i], sigma[l], sigma[m] = l, m, i
        inv = np.argsort(sigma)          # src index = sigma^{-1}(q)  (matches the convention of perm_src)
        return inv[self.q] * self.M.dim + srcM[self.e]

    def class_sum_2(self, u):
        out = np.zeros_like(u)
        for i in range(self.n):
            for l in range(i + 1, self.n):
                out += u[self.transposition_src(i, l)]
        return out

    def class_sum_3(self, u):
        out = np.zeros_like(u)
        for i, l, m in itertools.permutations(range(self.n), 3):
            if i < l and i < m:
                out += u[self.three_cycle_src(i, l, m)]
        return out


def project_isotypic(module, v, target_shape, candidates, subset=None, use3=True):
    """Project v onto the S^target isotypic component using contents (and squared contents) over candidates."""
    c1 = sorted({content(nu) for nu in candidates})
    v = lagrange_project(lambda x: module.class_sum_2(x, subset) if subset is not None else module.class_sum_2(x), v, content(target_shape), c1)
    same = [nu for nu in candidates if content(nu) == content(target_shape)]
    if use3 and len({content2(nu) for nu in same}) > 1:
        m = sum(target_shape)
        c2 = sorted({content2(nu) - math.comb(m, 2) for nu in same})
        v = lagrange_project(lambda x: module.class_sum_3(x, subset) if subset is not None else module.class_sum_3(x), v, content2(target_shape) - math.comb(m, 2), c2)
    return v


def raising_matrix(M: PermModule3, src_row: int, dst_row: int):
    """Sparse matrix of the map M^lambda -> M^lambda' moving one element from row src_row to row dst_row (1-based)."""
    import scipy.sparse as sp
    n = M.n; l = list(M.lam)
    l2 = l.copy(); l2[src_row - 1] -= 1; l2[dst_row - 1] += 1
    tgt = PermModule3(n, l2)
    rows, cols = [], []
    T = [None, ~(M.T2 | M.T3) & ((1 << n) - 1), M.T2, M.T3]   # masks of rows 1,2,3
    for c in range(M.dim):
        src = int(T[src_row][c])
        for e in range(n):
            if (src >> e) & 1:
                m2, m3 = int(M.T2[c]), int(M.T3[c])
                if src_row == 2: m2 &= ~(1 << e)
                if src_row == 3: m3 &= ~(1 << e)
                if dst_row == 2: m2 |= (1 << e)
                if dst_row == 3: m3 |= (1 << e)
                rows.append(int(tgt.index(np.array([m2]), np.array([m3]))[0])); cols.append(c)
    return sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(tgt.dim, M.dim))


def specht_project(M: PermModule3, v: np.ndarray) -> np.ndarray:
    """Orthogonal projection onto S^lambda = common kernel of the single-element raising maps (rows 2->1, 3->2, 3->1)."""
    import scipy.sparse as sp
    from scipy.sparse.linalg import lsqr
    l = M.lam
    mats = []
    if l[1] > 0: mats.append(raising_matrix(M, 2, 1))
    if l[2] > 0: mats.append(raising_matrix(M, 3, 2)); mats.append(raising_matrix(M, 3, 1))
    if not mats:
        return v
    Rm = sp.vstack(mats).tocsr()
    # projection onto ker R:  v - R^T y  with y the least-squares solution of R^T y ~ v
    y = lsqr(Rm.T, v, atol=1e-14, btol=1e-14, iter_lim=20000)[0]
    return v - Rm.T @ y


def transition_coefficients(n: int, w: int, p: int, lam, seed: int = 0, verbose: bool = False):
    """All p(lambda -> lambda') for the CW2 graph (complement degree q = 0)."""
    rng = np.random.default_rng(seed)
    lam = tuple(list(lam) + [0] * (3 - len(lam)))
    assert admissible(n, w, p, lam), (n, w, p, lam)
    N = n - w
    M = PermModule3(n, lam)
    v = rng.standard_normal(M.dim)
    # S^lambda inside M^lambda: common kernel of the single-element raising maps (checked by the content test below)
    v = specht_project(M, v)
    res = np.linalg.norm(M.class_sum_2(v) - content(lam) * v) / np.linalg.norm(v)
    assert res < 1e-8, f"Specht projection failed (content residual {res:.2e})"
    # E-copy: S_w-type (w-p, p) on x = {0..w-1}, trivial S_N-type on the complement
    x = list(range(w)); xc = list(range(w, n))
    v = project_isotypic(M, v, (w - p, p), partitions_le_rows(w, w), subset=x)
    if N >= 2:
        v = project_isotypic(M, v, (N,), partitions_le_rows(N, N), subset=xc, use3=False)
    nv2 = float(np.dot(v, v))
    assert nv2 > 1e-12, "E-copy not found"
    # coordinate vector and tensor
    ell = np.array([math.sqrt(n / (w * N)) * ((1 if q < w else 0) - w / n) for q in range(n)])
    T = TensorRM(M)
    u = np.kron(ell, v)
    targets = [t for t in box_moves(lam)]
    result = {}
    total = 0.0
    for tgt in targets:
        wv = project_isotypic(T, u, tgt, targets)
        pval = float(np.dot(wv, wv)) / nv2
        result[tgt] = pval; total += pval
    return result, total, nv2
