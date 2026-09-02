r"""
Multi-row binary representation graph for the hyperoctahedral group B_n = Z_2^n x S_n.

Ambient irreducible B_n-representations are indexed by bipartitions (alpha, beta), |alpha| + |beta| = n.
Model (Young):  V_(alpha,beta) = (+)_{S subset [n], |S| = |beta|}  chi_S (x) S^beta(S) (x) S^alpha(S^c),
where chi_S is the Walsh character on the cube (sign flips act by prod_{q in S} eps_q) and the Specht
modules of two-row shapes are the Boolean harmonic spaces  S^(m-p,p)(A) = E_p(A) = ker(lowering map).
We work with two-row shapes  alpha = (n-j-a2, a2),  beta = (j-b2, b2)  and write the vertex as (j, a2, b2).

Stabilizer of the base point (the all-zero word) is S_n; the stabilizer representation is E_mu with
mu = (n-k, k) (the paper's primitive space E_k).  Coordinate representation W = R^n (signed permutations),
coordinate vector ell_0 = (1,...,1)/sqrt n.  Tensoring with W moves one box between alpha and beta.

The directed squared coordinate coefficient  p(lambda -> lambda')  = || proj_{V_lambda'} (ell_0 (x) v) ||^2 / ||v||^2
for any nonzero v in the E_mu-isotypic part of V_lambda (Prop. 4.1 / Theorem 4.2 of the paper, with G = B_n).

Numerics: vectors in the signed permutation module M(n; j, b2, a2) with basis (S, P, Q), P subset S, |P| = b2,
Q subset S^c, |Q| = a2, stored as flat arrays over sorted integer keys.  Projections use central elements:
  Y2 = sum_{i<j} (ij)  (S_n transposition class sum; eigenvalue = content sum c(mu) on S^mu),
  Y3 = sum 3-cycles     (eigenvalue = sum of squared contents - C(n,2)),
  Z1 = sum_q eps_q      (diagonal on W (x) M: separates |beta'| = j +- 1),
  Z2 = sum_{i<j} [(ij) + (ij) eps_i eps_j]   -> acts as 2 (c(alpha') + c(beta')),
  Z3 = sum_{i<j} [(ij) eps_i + (ij) eps_j]   -> acts as 2 (c(alpha') - c(beta')),
with Krylov / Lagrange eigen-splitting.
"""
from __future__ import annotations

import itertools
import math
from functools import lru_cache

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import cg


def popcount(a: np.ndarray) -> np.ndarray:
    a = a.astype(np.int64)
    c = np.zeros_like(a)
    for b in range(a.max().bit_length() if a.size else 0):
        c += (a >> b) & 1
    return c


def content(shape) -> int:
    return sum(c - r for r, row in enumerate(shape) for c in range(row))


def content2(shape) -> int:
    return sum((c - r) ** 2 for r, row in enumerate(shape) for c in range(row))


def f_two_row(m: int, a: int) -> int:
    """dim S^(m-a, a) = C(m,a) - C(m,a-1)."""
    return math.comb(m, a) - (math.comb(m, a - 1) if a >= 1 else 0)


def dim_V(n: int, j: int, a2: int, b2: int) -> int:
    return math.comb(n, j) * f_two_row(j, b2) * f_two_row(n - j, a2)


class SignedModule:
    """Flat basis of M(n; j, b2, a2): keys encode (S, P, Q) bitmasks."""

    def __init__(self, n: int, j: int, b2: int, a2: int):
        self.n, self.j, self.b2, self.a2 = n, j, b2, a2
        S_list, P_list, Q_list = [], [], []
        for S in itertools.combinations(range(n), j):
            Smask = sum(1 << e for e in S)
            comp = [e for e in range(n) if not (Smask >> e) & 1]
            for P in itertools.combinations(S, b2):
                Pmask = sum(1 << e for e in P)
                for Q in itertools.combinations(comp, a2):
                    Qmask = sum(1 << e for e in Q)
                    S_list.append(Smask); P_list.append(Pmask); Q_list.append(Qmask)
        self.S = np.array(S_list, dtype=np.int64); self.P = np.array(P_list, dtype=np.int64); self.Q = np.array(Q_list, dtype=np.int64)
        self.keys = self._key(self.S, self.P, self.Q)
        order = np.argsort(self.keys)
        self.S, self.P, self.Q, self.keys = self.S[order], self.P[order], self.Q[order], self.keys[order]
        self.dim = self.keys.size

    def _key(self, S, P, Q):
        return (S.astype(np.int64) << (2 * self.n)) | (P.astype(np.int64) << self.n) | Q.astype(np.int64)

    def index(self, S, P, Q):
        k = self._key(S, P, Q)
        idx = np.searchsorted(self.keys, k)
        assert np.all(self.keys[idx] == k)
        return idx

    # ---- permutation action (no signs): sigma given as array new_pos[old_pos]
    @staticmethod
    def apply_perm_mask(mask: np.ndarray, sigma: np.ndarray) -> np.ndarray:
        out = np.zeros_like(mask)
        for b, sb in enumerate(sigma):
            out |= ((mask >> b) & 1) << int(sb)
        return out

    def perm_index(self, sigma: np.ndarray) -> np.ndarray:
        """Index array: (sigma v)[i] = v[src[i]] where basis element i = sigma(basis element src[i])."""
        # image of each basis element under sigma
        Si = self.apply_perm_mask(self.S, sigma); Pi = self.apply_perm_mask(self.P, sigma); Qi = self.apply_perm_mask(self.Q, sigma)
        img = self.index(Si, Pi, Qi)
        src = np.empty(self.dim, dtype=np.int64)
        src[img] = np.arange(self.dim)
        return src

    @lru_cache(maxsize=None)
    def transposition_src(self, i: int, l: int) -> np.ndarray:
        sigma = np.arange(self.n); sigma[i], sigma[l] = l, i
        return self.perm_index(sigma)

    @lru_cache(maxsize=None)
    def three_cycle_src(self, i: int, l: int, m: int) -> np.ndarray:
        sigma = np.arange(self.n); sigma[i], sigma[l], sigma[m] = l, m, i
        return self.perm_index(sigma)

    # ---- S_n class sums on M
    def Y2(self, v: np.ndarray) -> np.ndarray:
        out = np.zeros_like(v)
        for i in range(self.n):
            for l in range(i + 1, self.n):
                out += v[self.transposition_src(i, l)]
        return out

    def Y3(self, v: np.ndarray) -> np.ndarray:
        out = np.zeros_like(v)
        for i, l, m in itertools.permutations(range(self.n), 3):
            if i < l and i < m:
                out += v[self.three_cycle_src(i, l, m)]
        return out

    # ---- harmonic (Specht) projection: kernel of the lowering maps in P (within S) and Q (within S^c)
    def lowering_matrix(self, which: str) -> sp.csr_matrix:
        """Sparse matrix of the lowering map d: M(b2 or a2) -> M(b2-1 or a2-1) in the corresponding index."""
        n = self.n
        if which == "P":
            tgt = SignedModule(n, self.j, self.b2 - 1, self.a2)
            rows, cols = [], []
            for c in range(self.dim):
                Pm = int(self.P[c])
                for e in range(n):
                    if (Pm >> e) & 1:
                        rows.append(int(tgt.index(np.array([self.S[c]]), np.array([Pm & ~(1 << e)]), np.array([self.Q[c]]))[0])); cols.append(c)
        else:
            tgt = SignedModule(n, self.j, self.b2, self.a2 - 1)
            rows, cols = [], []
            for c in range(self.dim):
                Qm = int(self.Q[c])
                for e in range(n):
                    if (Qm >> e) & 1:
                        rows.append(int(tgt.index(np.array([self.S[c]]), np.array([self.P[c]]), np.array([Qm & ~(1 << e)]))[0])); cols.append(c)
        return sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(tgt.dim, self.dim))

    def harmonic_project(self, v: np.ndarray) -> np.ndarray:
        for which, deg in (("P", self.b2), ("Q", self.a2)):
            if deg == 0:
                continue
            d = self.lowering_matrix(which)
            A = d @ d.T
            y, info = cg(A, d @ v, rtol=1e-12, maxiter=5000)
            assert info == 0
            v = v - d.T @ y
        return v


def krylov_split(op, v: np.ndarray, tol: float = 1e-9, maxdim: int = 400):
    """Split v into eigen-components of the (diagonalisable, real-spectrum) operator op via its Krylov space.
    Returns list of (eigenvalue, component)."""
    nv = np.linalg.norm(v)
    if nv < 1e-14:
        return []
    Q = [v / nv]
    H = np.zeros((maxdim + 1, maxdim))
    for m in range(maxdim):
        w = op(Q[m])
        for i in range(len(Q)):
            H[i, m] = np.dot(Q[i], w); w = w - H[i, m] * Q[i]
        for i in range(len(Q)):  # re-orthogonalise
            c = np.dot(Q[i], w); w = w - c * Q[i]; H[i, m] += c
        hn = np.linalg.norm(w)
        if hn < tol * nv:
            break
        H[m + 1, m] = hn
        Q.append(w / hn)
    else:
        raise RuntimeError("Krylov space larger than maxdim; increase maxdim")
    k = len(Q)
    Hk = H[:k, :k]
    theta = np.linalg.eigvals(Hk).real
    # cluster eigenvalues
    theta = np.sort(theta); clusters = []
    for t in theta:
        if clusters and abs(t - clusters[-1][-1]) < 1e-6 * max(1.0, abs(t)):
            clusters[-1].append(t)
        else:
            clusters.append([t])
    thetas = [float(np.mean(c)) for c in clusters]
    comps = []
    for i, ti in enumerate(thetas):
        w = v.copy()
        for l, tl in enumerate(thetas):
            if l != i:
                w = (op(w) - tl * w) / (ti - tl)
        comps.append((ti, w))
    return comps


class TensorWM:
    """W (x) M with flat index (q, e) -> q * dimM + e; group actions with signs."""

    def __init__(self, M: SignedModule):
        self.M = M; self.n = M.n
        self.q = np.repeat(np.arange(self.n), M.dim)
        self.e = np.tile(np.arange(M.dim), self.n)
        self.S = M.S[self.e]
        self.Stilde = self.S ^ (1 << self.q)   # effective sign set of e_q (x) chi_S

    @lru_cache(maxsize=None)
    def transposition_src(self, i: int, l: int) -> np.ndarray:
        srcM = self.M.transposition_src(i, l)
        # q maps under (i l) too: element (q, e) = (il) applied to (q', e') with q' = (il) q, e' = srcM[e]
        qsrc = np.arange(self.n); qsrc[i], qsrc[l] = l, i
        return qsrc[self.q] * self.M.dim + srcM[self.e]

    def Z2(self, u: np.ndarray) -> np.ndarray:
        out = np.zeros_like(u)
        for i in range(self.n):
            for l in range(i + 1, self.n):
                same = (((self.Stilde >> i) & 1) == ((self.Stilde >> l) & 1))
                out += 2.0 * same * u[self.transposition_src(i, l)]
        return out

    def Z3(self, u: np.ndarray) -> np.ndarray:
        out = np.zeros_like(u)
        for i in range(self.n):
            for l in range(i + 1, self.n):
                bi = (self.Stilde >> i) & 1; bl = (self.Stilde >> l) & 1
                w = np.where(bi == bl, np.where(bi == 1, -2.0, 2.0), 0.0)
                out += w * u[self.transposition_src(i, l)]
        return out


def constituents(n: int, j: int, a2: int, b2: int):
    """Bipartitions reachable by moving one box; returns dict name -> (alpha', beta') with only weakly-decreasing shapes."""
    alpha = [n - j - a2, a2]; beta = [j - b2, b2]
    out = {}
    def ok(sh): return all(sh[i] >= sh[i + 1] for i in range(len(sh) - 1)) and all(x >= 0 for x in sh)
    # alpha -> beta
    for ra in range(2):
        for rb in range(3):
            a = alpha.copy(); b = beta + [0]
            a[ra] -= 1; b[rb] += 1
            if ok(a) and ok(b):
                out[(f"a{ra+1}->b{rb+1}")] = (tuple(a), tuple(b))
    for rb in range(2):
        for ra in range(3):
            a = alpha + [0]; b = beta.copy()
            b[rb] -= 1; a[ra] += 1
            if ok(a) and ok(b):
                out[(f"b{rb+1}->a{ra+1}")] = (tuple(a), tuple(b))
    return out


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


def lagrange_project(op, v: np.ndarray, target: float, others: list) -> np.ndarray:
    """Component of v in the target-eigenspace of op, given the list of all other possible eigenvalues."""
    w = v.copy()
    for t in others:
        if abs(t - target) < 1e-9:
            continue
        w = (op(w) - t * w) / (target - t)
    return w


def transition_coefficients(n: int, j: int, a2: int, b2: int, k: int, seed: int = 0, verbose: bool = False):
    """All directed squared coefficients p(lambda -> lambda') for lambda = (j, a2, b2), stabilizer mu = (n-k, k),
    by exact Lagrange projection onto known central-character eigenvalues."""
    rng = np.random.default_rng(seed)
    M = SignedModule(n, j, b2, a2)
    v = rng.standard_normal(M.dim)
    v = M.harmonic_project(v)                       # now in V_lambda (up to CG tolerance)
    mu = (n - k, k)
    # S_n-isotypic projection onto S^mu: candidates are all partitions of n with <= 4 rows
    cands = partitions_le_rows(n, 4)
    c1 = sorted({content(nu) for nu in cands})
    v = lagrange_project(M.Y2, v, content(mu), c1)
    same = [nu for nu in cands if content(nu) == content(mu)]
    c2 = sorted({content2(nu) - math.comb(n, 2) for nu in same})
    if len(c2) > 1:
        v = lagrange_project(M.Y3, v, content2(mu) - math.comb(n, 2), c2)
    amb = [nu for nu in same if content2(nu) == content2(mu) and nu != mu]
    if amb and verbose:
        print("   WARNING: content-ambiguous partitions", amb)
    nv2 = float(np.dot(v, v))
    assert nv2 > 1e-10, "E_mu not found in V_lambda"
    T = TensorWM(M)
    u = np.tile(v, n) / math.sqrt(n)
    inS = ((M.S[T.e] >> T.q) & 1).astype(bool)
    cons = constituents(n, j, a2, b2)
    result = {}
    total = 0.0
    for block, mask in (("beta+1", ~inS), ("beta-1", inS)):
        ub = np.where(mask, u, 0.0)
        blk = [(al, be) for (al, be) in cons.values() if (sum(be) == j + 1) == (block == "beta+1")]
        z2 = sorted({2 * (content(al) + content(be)) for al, be in blk})
        for (al, be) in blk:
            t2 = 2 * (content(al) + content(be)); t3 = 2 * (content(al) - content(be))
            w = lagrange_project(T.Z2, ub, t2, z2)
            z3 = sorted({2 * (content(a) - content(b)) for a, b in blk if 2 * (content(a) + content(b)) == t2})
            w = lagrange_project(T.Z3, w, t3, z3)
            p = float(np.dot(w, w)) / nv2
            result[(al, be)] = p
            total += p
    return result, total


def lr_contains(n: int, j: int, a2: int, b2: int, k: int) -> bool:
    """Does V_(alpha,beta) restricted to S_n contain S^(n-k,k)?  Two-row LR rule: a2+b2 <= k <= min(a1+b2, a2+b1)."""
    a1, b1 = n - j - a2, j - b2
    return a2 + b2 <= k <= min(a1 + b2, a2 + b1) and a1 >= a2 and b1 >= b2 and k <= n // 2
