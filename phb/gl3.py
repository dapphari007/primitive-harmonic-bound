r"""
gl_3 irreducible representations in the Gelfand-Tsetlin basis, invariant inner product, tensor products,
highest-weight vectors and intertwiners.  Used to compute the CW2 (three-row constant-weight) coefficients via
Schur-Weyl duality in modules of dimension O(n^2).

GT pattern for highest weight (a, b, c):  rows  (a, b, c) / (m12, m22) / (m11)  with betweenness
    a >= m12 >= b >= m22 >= c,   m12 >= m11 >= m22.
Weight (eigenvalues of E_11, E_22, E_33):  (m11, m12 + m22 - m11, a + b + c - m12 - m22).
Generator action (Molev, "Gelfand-Tsetlin bases for classical Lie algebras", Thm 2.3), l_{ki} = m_{ki} - i + 1:
    E_{k,k+1} xi = - sum_i [ prod_{j=1}^{k+1} (l_{ki} - l_{k+1,j}) / prod_{j != i} (l_{ki} - l_{kj}) ] xi_{+delta_{ki}}
    E_{k+1,k} xi =   sum_i [ prod_{j=1}^{k-1} (l_{ki} - l_{k-1,j}) / prod_{j != i} (l_{ki} - l_{kj}) ] xi_{-delta_{ki}}
(the basis is not orthonormal; the invariant form is diagonal with norms obtained by the adjointness
E_{k+1,k}^* = E_{k,k+1}, propagated from the highest-weight vector).  All conventions are checked numerically
(commutation relations, Weyl dimension, adjointness) in `check()`.
"""
from __future__ import annotations

import itertools
import math
from functools import lru_cache

import numpy as np
import scipy.sparse as sp


class GL3Irrep:
    def __init__(self, hw):
        a, b, c = hw
        assert a >= b >= c >= 0
        self.hw = (a, b, c)
        pats = []
        for m12 in range(b, a + 1):
            for m22 in range(c, b + 1):
                for m11 in range(m22, m12 + 1):
                    pats.append((m12, m22, m11))
        self.pats = pats
        self.index = {p: i for i, p in enumerate(pats)}
        self.dim = len(pats)
        self.weights = np.array([(m11, m12 + m22 - m11, a + b + c - m12 - m22) for (m12, m22, m11) in pats])
        self.E = {}
        for (k, kp) in [(1, 2), (2, 1), (2, 3), (3, 2)]:
            self.E[(k, kp)] = self._build(k, kp)
        # diagonal invariant form
        self.norm2 = self._norms()

    def _l(self, p):
        """l_{ki} arrays: row 3 = hw, row 2 = (m12, m22), row 1 = (m11); l_{ki} = m_{ki} - i + 1."""
        a, b, c = self.hw; m12, m22, m11 = p
        return {3: [a - 0, b - 1, c - 2], 2: [m12 - 0, m22 - 1], 1: [m11 - 0]}

    def _build(self, k, kp):
        M = sp.lil_matrix((self.dim, self.dim))
        for col, p in enumerate(self.pats):
            l = self._l(p)
            m12, m22, m11 = p
            if kp == k + 1:      # raising E_{k,k+1}: adds 1 to an entry of row k
                for i in range(k):
                    lki = l[k][i]
                    num = 1.0
                    for j in range(k + 1):
                        num *= (lki - l[k + 1][j])
                    den = 1.0
                    for j in range(k):
                        if j != i:
                            den *= (lki - l[k][j])
                    if den == 0:
                        continue
                    coef = -num / den
                    q = list(p)
                    if k == 1: q[2] += 1
                    else: q[i] += 1
                    q = tuple(q)
                    if q in self.index and coef != 0:
                        M[self.index[q], col] += coef
            else:                 # lowering E_{kk+1, kk} with kk = kp: subtracts 1 from an entry of row kk
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
                    if den == 0:
                        continue
                    coef = num / den
                    q = list(p)
                    if kk == 1: q[2] -= 1
                    else: q[i] -= 1
                    q = tuple(q)
                    if q in self.index and coef != 0:
                        M[self.index[q], col] += coef
        return M.tocsr()

    def _norms(self):
        """||xi||^2 from <E_{k+1,k} xi, xi'> = <xi, E_{k,k+1} xi'> and ||xi_hw||^2 = 1."""
        a, b, c = self.hw
        hw = self.index[(a, b, a)]
        g = np.full(self.dim, np.nan); g[hw] = 1.0
        # BFS by lowering
        frontier = [hw]
        while frontier:
            new = []
            for src in frontier:
                for (k, kp) in [(2, 1), (3, 2)]:
                    L = self.E[(k, kp)]; R = self.E[(kp, k)]
                    col = L[:, src]
                    for tgt in col.nonzero()[0]:
                        if np.isnan(g[tgt]):
                            # g_tgt * L[tgt, src] = g_src * R[src, tgt]
                            g[tgt] = g[src] * R[src, tgt] / L[tgt, src]
                            new.append(tgt)
            frontier = new
        assert not np.isnan(g).any(), "norm propagation incomplete"
        assert np.all(g > 0), "non-positive norms: convention error"
        return g

    def check(self):
        E = self.E
        H1 = sp.diags(self.weights[:, 0].astype(float)); H2 = sp.diags(self.weights[:, 1].astype(float)); H3 = sp.diags(self.weights[:, 2].astype(float))
        c1 = (E[(1,2)] @ E[(2,1)] - E[(2,1)] @ E[(1,2)] - (H1 - H2))
        c2 = (E[(2,3)] @ E[(3,2)] - E[(3,2)] @ E[(2,3)] - (H2 - H3))
        # adjointness with the diagonal form G: G L = R^T G  for L = E_{k+1,k}, R = E_{k,k+1}
        G = sp.diags(self.norm2)
        adj1 = G @ E[(2,1)] - E[(1,2)].T @ G
        adj2 = G @ E[(3,2)] - E[(2,3)].T @ G
        a, b, c = self.hw
        weyl = (a - b + 1) * (b - c + 1) * (a - c + 2) // 2
        return dict(comm12=abs(c1).max(), comm23=abs(c2).max(), adj1=abs(adj1).max(), adj2=abs(adj2).max(), dim=self.dim, weyl=weyl)


class Tensor:
    """V (x) W with product basis, generators E (x) 1 + 1 (x) E, product form."""

    def __init__(self, V: GL3Irrep, W: GL3Irrep):
        self.V, self.W = V, W
        self.dim = V.dim * W.dim
        self.weights = (V.weights[:, None, :] + W.weights[None, :, :]).reshape(-1, 3)
        self.norm2 = np.kron(V.norm2, W.norm2)
        IV, IW = sp.identity(V.dim), sp.identity(W.dim)
        self.E = {k: sp.kron(V.E[k], IW) + sp.kron(IV, W.E[k]) for k in V.E}

    def hw_vectors(self, wt):
        """Basis of highest-weight vectors of weight wt (kernel of E12, E23 on the weight space)."""
        idx = np.where((self.weights == np.array(wt)).all(axis=1))[0]
        if idx.size == 0:
            return idx, np.zeros((0, 0))
        As = sp.vstack([self.E[(1, 2)][:, idx], self.E[(2, 3)][:, idx]]).tocsr()
        rows = np.unique(As.nonzero()[0])
        A = As[rows].toarray() if rows.size else np.zeros((1, idx.size))
        # kernel via SVD (restricted to the nonzero rows: the weight-space equations only)
        u, s, vt = np.linalg.svd(A)
        rank = int((s > 1e-9 * max(1.0, s.max() if s.size else 1.0)).sum())
        K = vt[rank:].T
        return idx, K

    def inner(self, x, y):
        return float(np.dot(x, self.norm2 * y))


def intertwiner(V: GL3Irrep, T: Tensor, t_hw: np.ndarray):
    """Extend v_hw -> t_hw to the full intertwiner Phi: V -> T (matrix T.dim x V.dim) by propagating lowering
    equations weight space by weight space (least squares on each weight space)."""
    a, b, c = V.hw
    Phi = np.zeros((T.dim, V.dim))
    hw = V.index[(a, b, a)]
    Phi[:, hw] = t_hw
    done = np.zeros(V.dim, bool); done[hw] = True
    # order weights by height (sum of positive-root coefficients)  -> process from highest downward
    heights = (V.weights[:, 0] * 2 + V.weights[:, 1])
    order = np.argsort(-heights)
    remaining = set(range(V.dim)) - {hw}
    for wgt in sorted(set(map(tuple, V.weights)), key=lambda w: -(2 * w[0] + w[1])):
        cols = [i for i in range(V.dim) if tuple(V.weights[i]) == wgt and not done[i]]
        if not cols:
            continue
        # equations: for each lowering op L and each done source j:  Phi[:, cols] @ L[cols, j] = (L_T @ Phi[:, j]) - Phi[:, done_other] @ L[done_other, j]
        rows_A, rows_b = [], []
        for (k, kp) in [(2, 1), (3, 2)]:
            L = V.E[(k, kp)]; LT = T.E[(k, kp)]
            for j in np.where(done)[0]:
                colL = L[:, j].toarray().ravel()
                if not np.any(colL[cols]):
                    continue
                rhs = LT @ Phi[:, j]
                for i in np.where(colL != 0)[0]:
                    if done[i]:
                        rhs = rhs - colL[i] * Phi[:, i]
                rows_A.append(colL[cols]); rows_b.append(rhs)
        if not rows_A:
            raise RuntimeError(f"cannot reach weight {wgt}")
        A = np.array(rows_A)               # (#eq, #cols)
        B = np.array(rows_b)               # (#eq, T.dim)
        X, *_ = np.linalg.lstsq(A, B, rcond=None)   # (#cols, T.dim)
        Phi[:, cols] = X.T
        for i in cols:
            done[i] = True
    return Phi


def intertwiner_partial(V: GL3Irrep, T: "Tensor", t_hw: np.ndarray, needed):
    """Columns Phi[:, i] of the intertwiner V -> T for the basis indices i in `needed` only (and for every basis
    vector of higher weight), by the same weight-space propagation as `intertwiner`.  Returns a dict i -> column."""
    a, b, c = V.hw
    hw = V.index[(a, b, a)]
    cols_done = {hw: np.asarray(t_hw, dtype=float)}
    needed = set(needed)
    if needed <= cols_done.keys():
        return cols_done
    ht = lambda w: 2 * w[0] + w[1]
    need_ht = min(ht(V.weights[i]) for i in needed)
    for wgt in sorted(set(map(tuple, V.weights)), key=lambda w: -ht(w)):
        if ht(wgt) < need_ht:
            break
        cols = [i for i in range(V.dim) if tuple(V.weights[i]) == wgt and i not in cols_done]
        if not cols:
            continue
        rows_A, rows_b = [], []
        for (k, kp) in [(2, 1), (3, 2)]:
            L = V.E[(k, kp)]; LT = T.E[(k, kp)]
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
