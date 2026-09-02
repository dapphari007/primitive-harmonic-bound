r"""
gl_m irreducible representations (any m) in the Gelfand-Tsetlin basis, invariant inner product, tensor products,
highest-weight vectors and (partial) intertwiners.  Generalises phb/gl3.py; used for the m-row layer graphs.

GT pattern for highest weight (hw_1 >= ... >= hw_m): rows R_m = hw, R_{m-1}, ..., R_1 with betweenness
    R_{k+1}[i] >= R_k[i] >= R_{k+1}[i+1].
Weight: w_k = sum(R_k) - sum(R_{k-1}).  Generators (Molev, Thm 2.3), l_{ki} = m_{ki} - i + 1:
    E_{k,k+1} xi = - sum_i [ prod_{j<=k+1} (l_{ki} - l_{k+1,j}) / prod_{j != i} (l_{ki} - l_{kj}) ] xi_{+delta_{ki}}
    E_{k+1,k} xi =   sum_i [ prod_{j<=k-1} (l_{ki} - l_{k-1,j}) / prod_{j != i} (l_{ki} - l_{kj}) ] xi_{-delta_{ki}}
Basis not orthonormal; the invariant form is diagonal, propagated from the highest-weight vector by adjointness.
`check()` verifies the sl_2 commutators, the Serre relations, adjointness and the Weyl dimension.
"""
from __future__ import annotations

import math
import numpy as np
import scipy.sparse as sp


class GLmIrrep:
    def __init__(self, hw):
        hw = tuple(int(x) for x in hw)
        m = len(hw)
        assert all(hw[i] >= hw[i + 1] for i in range(m - 1)) and hw[-1] >= 0
        self.hw, self.m = hw, m
        pats = []
        def rec(k, rows):
            # rows: dict k -> tuple; generate row k-1 from row k
            if k == 1:
                pats.append(tuple(rows[j] for j in range(1, m)))
                return
            upper = rows[k]
            def gen(i, cur):
                if i == k - 1:
                    rows[k - 1] = tuple(cur); rec(k - 1, rows); return
                for x in range(upper[i + 1], upper[i] + 1):
                    gen(i + 1, cur + [x])
            gen(0, [])
        rec(m, {m: hw})
        self.pats = pats
        self.index = {p: i for i, p in enumerate(pats)}
        self.dim = len(pats)
        W = np.zeros((self.dim, m), dtype=np.int64)
        for i, p in enumerate(pats):
            rows = self._rows(p)
            prev = 0
            for k in range(1, m + 1):
                s = sum(rows[k]); W[i, k - 1] = s - prev; prev = s
        self.weights = W
        self.E = {}
        for k in range(1, m):
            self.E[(k, k + 1)] = self._build(k, k + 1)
            self.E[(k + 1, k)] = self._build(k + 1, k)
        self.hw_index = self.index[tuple(tuple(hw[:k]) for k in range(1, m))]
        self.norm2 = self._norms()

    def _rows(self, p):
        rows = {k: p[k - 1] for k in range(1, self.m)}
        rows[self.m] = self.hw
        return rows

    def _l(self, rows):
        return {k: [rows[k][i] - i for i in range(k)] for k in range(1, self.m + 1)}

    def _build(self, k, kp):
        M = sp.lil_matrix((self.dim, self.dim))
        for col, p in enumerate(self.pats):
            rows = self._rows(p); l = self._l(rows)
            if kp == k + 1:      # raising E_{k,k+1}: +1 on an entry of row k
                for i in range(k):
                    lki = l[k][i]
                    num = 1.0
                    for j in range(k + 1):
                        num *= (lki - l[k + 1][j])
                    den = 1.0
                    for j in range(k):
                        if j != i:
                            den *= (lki - l[k][j])
                    if den == 0 or num == 0:
                        continue
                    q = list(rows[k]); q[i] += 1
                    newp = tuple(tuple(q) if kk == k else p[kk - 1] for kk in range(1, self.m))
                    if newp in self.index:
                        M[self.index[newp], col] += -num / den
            else:                 # lowering E_{kk+1,kk}, kk = kp: -1 on an entry of row kk
                kk = kp
                for i in range(kk):
                    lki = l[kk][i]
                    num = 1.0
                    for j in range(kk - 1):
                        num *= (lki - l[kk - 1][j])
                    den = 1.0
                    for j in range(kk):
                        if j != i:
                            den *= (lki - l[kk][j])
                    if den == 0 or num == 0:
                        continue
                    q = list(rows[kk]); q[i] -= 1
                    newp = tuple(tuple(q) if kk2 == kk else p[kk2 - 1] for kk2 in range(1, self.m))
                    if newp in self.index:
                        M[self.index[newp], col] += num / den
        return M.tocsr()

    def _norms(self):
        g = np.full(self.dim, np.nan); g[self.hw_index] = 1.0
        frontier = [self.hw_index]
        while frontier:
            new = []
            for src in frontier:
                for k in range(1, self.m):
                    L = self.E[(k + 1, k)]; R = self.E[(k, k + 1)]
                    col = L[:, src]
                    for tgt in col.nonzero()[0]:
                        if np.isnan(g[tgt]):
                            g[tgt] = g[src] * R[src, tgt] / L[tgt, src]
                            new.append(tgt)
            frontier = new
        assert not np.isnan(g).any(), "norm propagation incomplete"
        assert np.all(g > 0), "non-positive norms"
        return g

    def weyl_dim(self):
        m = self.m; l = [self.hw[i] - i for i in range(m)]
        num = 1; den = 1
        for i in range(m):
            for j in range(i + 1, m):
                num *= (l[i] - l[j]); den *= (j - i)
        return num // den

    def check(self):
        E = self.E; m = self.m
        H = [sp.diags(self.weights[:, k].astype(float)) for k in range(m)]
        out = dict(dim=self.dim, weyl=self.weyl_dim(), comm=0.0, serre=0.0, adj=0.0)
        G = sp.diags(self.norm2)
        for k in range(1, m):
            c = E[(k, k + 1)] @ E[(k + 1, k)] - E[(k + 1, k)] @ E[(k, k + 1)] - (H[k - 1] - H[k])
            out["comm"] = max(out["comm"], abs(c).max() if c.nnz else 0.0)
            a = G @ E[(k + 1, k)] - E[(k, k + 1)].T @ G
            out["adj"] = max(out["adj"], abs(a).max() if a.nnz else 0.0)
        for k in range(1, m - 1):
            E13 = E[(k, k + 1)] @ E[(k + 1, k + 2)] - E[(k + 1, k + 2)] @ E[(k, k + 1)]
            s1 = E13 @ E[(k + 1, k + 2)] - E[(k + 1, k + 2)] @ E13
            s2 = E[(k, k + 1)] @ E13 - E13 @ E[(k, k + 1)]
            out["serre"] = max(out["serre"], abs(s1).max() if s1.nnz else 0.0, abs(s2).max() if s2.nnz else 0.0)
        return out


class Tensor:
    """V (x) W with product basis, generators E (x) 1 + 1 (x) E, product form."""

    def __init__(self, V, W):
        self.V, self.W = V, W
        self.m = V.m
        self.dim = V.dim * W.dim
        self.weights = (V.weights[:, None, :] + W.weights[None, :, :]).reshape(-1, self.m)
        self.norm2 = np.kron(V.norm2, W.norm2)
        IV, IW = sp.identity(V.dim), sp.identity(W.dim)
        self.E = {k: sp.kron(V.E[k], IW) + sp.kron(IV, W.E[k]) for k in V.E}

    def hw_vectors(self, wt):
        idx = np.where((self.weights == np.array(wt)).all(axis=1))[0]
        if idx.size == 0:
            return idx, np.zeros((0, 0))
        As = sp.vstack([self.E[(k, k + 1)][:, idx] for k in range(1, self.m)]).tocsr()
        rows = np.unique(As.nonzero()[0])
        A = As[rows].toarray() if rows.size else np.zeros((1, idx.size))
        u, s, vt = np.linalg.svd(A)
        rank = int((s > 1e-9 * max(1.0, s.max() if s.size else 1.0)).sum())
        K = vt[rank:].T
        return idx, K


def height(w, m):
    return sum((m - k) * w[k - 1] for k in range(1, m + 1))


def intertwiner_partial(V: GLmIrrep, T: Tensor, t_hw: np.ndarray, needed):
    """Columns Phi[:, i] of the intertwiner V -> T for the basis indices in `needed` (and all of higher weight)."""
    m = V.m
    hw = V.hw_index
    cols_done = {hw: np.asarray(t_hw, dtype=float)}
    needed = set(needed)
    if needed <= cols_done.keys():
        return cols_done
    need_ht = min(height(V.weights[i], m) for i in needed)
    for wgt in sorted(set(map(tuple, V.weights)), key=lambda w: -height(w, m)):
        if height(wgt, m) < need_ht:
            break
        cols = [i for i in range(V.dim) if tuple(V.weights[i]) == wgt and i not in cols_done]
        if not cols:
            continue
        rows_A, rows_b = [], []
        for k in range(1, m):
            L = V.E[(k + 1, k)]; LT = T.E[(k + 1, k)]
            for j in list(cols_done.keys()):
                colL = L[:, j].toarray().ravel()
                if not np.any(colL[cols]):
                    continue
                rhs = LT @ cols_done[j]
                for i in np.where(colL != 0)[0]:
                    if i in cols_done:
                        rhs = rhs - colL[i] * cols_done[i]
                rows_A.append(colL[cols]); rows_b.append(rhs)
        if not rows_A:
            raise RuntimeError(f"cannot reach weight {wgt}")
        A = np.array(rows_A); B = np.array(rows_b)
        X, *_ = np.linalg.lstsq(A, B, rcond=None)
        for ci, i in enumerate(cols):
            cols_done[i] = X[ci]
        if needed <= cols_done.keys():
            break
    return cols_done


def intertwiner(V: GLmIrrep, T: Tensor, t_hw: np.ndarray):
    cols = intertwiner_partial(V, T, t_hw, range(V.dim))
    Phi = np.zeros((T.dim, V.dim))
    for i, c in cols.items():
        Phi[:, i] = c
    return Phi
