r"""
From-scratch reconstruction of the constant-weight certificate for small n.

Functions on X_w (w-subsets of [n]).  Johnson harmonic spaces V_j^J are the eigenspaces of the
Johnson graph (|x cap y| = w-1) with eigenvalue (w-j)(N-j) - j.  For a base support x, the
attached space E_x^{p,q} = E_p(x) (x) E_q(x^c) of Boolean harmonics is mapped equivariantly into
functions on X_w by
    (T Y)(y) = sum_{P subset y cap x, |P| = p} sum_{Q subset y \ x, |Q| = q} Y(P, Q),
and phi_{j,x} Y := normalised projection of T Y onto V_j^J (Schur: a scalar multiple of an isometry
on each admissible degree j_- <= j <= j_+).  We then MEASURE the recurrence coefficients
    b_j = <phi_j Y, t(x,.) phi_j Y>,   c_j = <phi_{j+1} Y, t(x,.) phi_j Y>
and compare with the paper's associated Hahn formulas (36)-(37).  Finally we build the Perron-weighted
projection P_x, the kernel K(r) = tr(P_x P_y) and the best positive-definite lambda*.
"""
from __future__ import annotations

import itertools
import math

import numpy as np

from .johnson import hahn_bc, perron_vector, j_plus
from .johnson_lp import eberlein, Dj


def subsets(items, k):
    return [frozenset(c) for c in itertools.combinations(items, k)]


class JohnsonLayer:
    def __init__(self, n: int, w: int):
        self.n, self.w, self.N = n, w, n - w
        self.X = subsets(range(n), w)
        self.index = {S: i for i, S in enumerate(self.X)}
        M = len(self.X)
        # distance matrix r(x,y) = w - |x cap y|
        masks = np.array([sum(1 << e for e in S) for S in self.X], dtype=np.int64)
        inter = np.zeros((M, M), dtype=np.int64)
        for i in range(M):
            inter[i] = np.array([bin(int(masks[i] & m)).count("1") for m in masks])
        self.r = w - inter
        A1 = (self.r == 1).astype(float)
        ev, U = np.linalg.eigh(A1)
        self.proj = {}
        for j in range(w + 1):
            theta = (w - j) * (self.N - j) - j
            sel = np.abs(ev - theta) < 1e-6
            assert sel.sum() == Dj(n, j), (j, sel.sum(), Dj(n, j))
            Uj = U[:, sel]
            self.proj[j] = Uj @ Uj.T
        self.x = frozenset(range(w))
        self.t = 1 - n * self.r[self.index[self.x]] / (w * self.N)   # t(x, .) as a vector on X_w

    def harmonic_space(self, ground, p):
        """Orthonormal basis of E_p(ground): functions on p-subsets with vanishing lowering map."""
        ground = sorted(ground)
        if p == 0:
            return [frozenset()], np.ones((1, 1))
        Sp = subsets(ground, p)
        Sm = subsets(ground, p - 1)
        idx_m = {S: i for i, S in enumerate(Sm)}
        Dm = np.zeros((len(Sm), len(Sp)))
        for c, S in enumerate(Sp):
            for e in S:
                Dm[idx_m[S - {e}], c] = 1.0
        u, sv, vt = np.linalg.svd(Dm)
        rank = int((sv > 1e-10).sum())
        Q = vt[rank:].T
        assert Q.shape[1] == math.comb(len(ground), p) - math.comb(len(ground), p - 1)
        return Sp, Q

    def attached_space(self, p, q):
        """Basis Y_ab = f_a (x) g_b of E_x^{p,q}, returned as the matrix T (X_w x dim) applying T to each basis vector."""
        Sp, Qp = self.harmonic_space(self.x, p)
        Sq, Qq = self.harmonic_space(set(range(self.n)) - self.x, q)
        idx_p = {S: i for i, S in enumerate(Sp)}
        idx_q = {S: i for i, S in enumerate(Sq)}
        # T maps a function on pairs (P,Q) to a function on X_w
        Tm = np.zeros((len(self.X), len(Sp) * len(Sq)))
        for yi, y in enumerate(self.X):
            inx = sorted(y & self.x)
            outx = sorted(y - self.x)
            if len(inx) < p or len(outx) < q:
                continue
            for P in itertools.combinations(inx, p):
                for Q in itertools.combinations(outx, q):
                    Tm[yi, idx_p[frozenset(P)] * len(Sq) + idx_q[frozenset(Q)]] += 1.0
        basis = np.kron(Qp, Qq)   # columns: orthonormal basis of E_p (x) E_q
        return Tm @ basis        # X_w x d_{p,q}

    def embeddings(self, p, q, L):
        """phi_j for j = p+q..L as matrices X_w x d_{p,q} with orthonormal columns, signs per (38).

        The equivariant images T_r Y := 1[r(x,y) = r] * (T Y) (r = 0..w) all lie in the E^{p,q}-isotypic
        part; by Lemma 3.1 / Schur, any nonzero projection onto V_j^J is the unique copy, up to scale."""
        TY = self.attached_space(p, q)
        d = TY.shape[1]
        rx = self.r[self.index[self.x]]
        phis = {}
        for j in range(p + q, L + 1):
            best = None
            for r in range(self.w + 1):
                Pj = self.proj[j] @ ((rx == r)[:, None] * TY)
                G = Pj.T @ Pj
                if best is None or G[0, 0] > best[1]:
                    best = (Pj, G[0, 0], G)
            Pj, scale, G = best
            assert scale > 1e-10, f"projection of T(E^{p,q}) onto V_{j} vanishes for every r"
            assert np.allclose(G, scale * np.eye(d), atol=1e-8 * scale), "not scalar*isometry (Schur violated?)"
            phis[j] = Pj / math.sqrt(scale)
        # orientation (38): make <phi_{j+1} Y, t phi_j Y> > 0
        for j in range(p + q, L):
            c = np.sum(phis[j + 1] * (self.t[:, None] * phis[j])) / d
            if c < 0:
                phis[j + 1] = -phis[j + 1]
        return phis

    def measured_coefficients(self, p, q, L):
        phis = self.embeddings(p, q, L)
        d = next(iter(phis.values())).shape[1]
        out = {}
        for j in range(p + q, L + 1):
            Bm = phis[j].T @ (self.t[:, None] * phis[j])
            assert np.allclose(Bm, Bm[0, 0] * np.eye(d), atol=1e-8), "b_j not scalar"
            cval = None
            if j < L:
                Cm = phis[j + 1].T @ (self.t[:, None] * phis[j])
                assert np.allclose(Cm, Cm[0, 0] * np.eye(d), atol=1e-8), "c_j not scalar"
                cval = Cm[0, 0]
            out[j] = (Bm[0, 0], cval)
        return out, phis

    def kernel(self, p, q, L):
        """K(r) = tr(P_x P_y) for the Perron-weighted amplitudes, r = 0..w; plus lambda_max(Jhat)."""
        lam, v = perron_vector(self.n, self.w, p, q, L)
        js = list(range(p + q, L + 1))
        omega = np.array([math.sqrt(Dj(self.n, j)) * v[i] for i, j in enumerate(js)])
        a = np.sqrt(omega / omega.sum())
        _, phis = self.measured_coefficients(p, q, L)
        Psi = sum(a[i] * phis[j] for i, j in enumerate(js))      # X_w x d
        # P_y for y = g x: permute coordinates.  K depends only on r, so use representatives.
        K = np.zeros(self.w + 1)
        d = Psi.shape[1]
        for r in range(self.w + 1):
            y = frozenset(list(range(r, self.w)) + list(range(self.w, self.w + r)))  # |x cap y| = w - r
            # permutation g with g(x) = y: map elements of x to elements of y, complement to complement
            g = {}
            xs, ys = sorted(self.x), sorted(y)
            for e, f in zip(xs, ys): g[e] = f
            xc, yc = sorted(set(range(self.n)) - self.x), sorted(set(range(self.n)) - y)
            for e, f in zip(xc, yc): g[e] = f
            perm = np.array([self.index[frozenset(g[e] for e in S)] for S in self.X])
            Psi_y = np.zeros_like(Psi)
            Psi_y[perm] = Psi
            M = Psi.T @ Psi_y
            K[r] = np.sum(M * M)
        assert abs(K[0] - d) < 1e-8
        return K, lam

    def scheme_eigs(self, F):
        """Eigenvalue of the Bose-Mesner element sum_r F(r) A_r on V_j: sum_r F(r) E_r(j)."""
        return np.array([sum(F[r] * eberlein(self.n, self.w, r, j) for r in range(self.w + 1)) for j in range(self.w + 1)])

    def lambda_star(self, K):
        tr = np.array([1 - self.n * r / (self.w * self.N) for r in range(self.w + 1)])
        kh = self.scheme_eigs(K)
        tkh = self.scheme_eigs(tr * K)
        assert np.all(kh >= -1e-9 * kh.max()), "K not positive definite"
        ratios = [tkh[j] / kh[j] for j in range(self.w + 1) if kh[j] > 1e-10 * kh.max()]
        return min(ratios)

    def delsarte_bound(self, K, d, lam):
        """A_J <= f(0)/f^_0 with f(r) = (t(r) - s) K(r), valid when s <= lam."""
        s = 1 - self.n * d / (2 * self.w * self.N)
        if s >= lam:
            return None
        tr = np.array([1 - self.n * r / (self.w * self.N) for r in range(self.w + 1)])
        f = (tr - s) * K
        kr = np.array([math.comb(self.w, r) * math.comb(self.N, r) for r in range(self.w + 1)], float)
        f0hat = np.dot(kr, f) / kr.sum()
        return f[0] / f0hat
