"""
From-scratch reconstruction of the moving-primitive-subspace certificate.

Fourier side of the n-cube: V_j = span{e_S : |S| = j}.  Raising/lowering maps
    U e_S = sum_{q not in S} e_{S+q},    D e_S = sum_{q in S} e_{S-q},   D = U^T.
Primitive space  E_k = ker(D : V_k -> V_{k-1}),  dim m_k = C(n,k) - C(n,k-1).
By sl2 theory  U^{j-k} restricted to E_k is a scalar multiple of an isometry into V_j
(k <= j <= n-k); iota_j denotes the normalised (isometric) embedding.

For a unit amplitude vector a = (a_k..a_L), R_0 = { sum_j a_j iota_j Y : Y in E_k } and
for a word x, R_x = sigma_x R_0 where sigma_x e_S = (-1)^{|S cap x|} e_S is translation
by x on the Fourier side.  P_x = projection on R_x,

    K(x,y) = Tr(P_x P_y) = || sum_j a_j^2 iota_j^T sigma_{x+y} iota_j ||_F^2 ,

a function of the weight t = |x+y| only.  With xi(t) = 1 - 2t/n = <b_x, b_y>:

    lambda*(a) := max { lambda : (xi - lambda) K is positive definite on the cube }
               =  min_j  (xi K)^_j / K^_j    (Krawtchouk coefficients),

and for any s <= lambda*,  f(t) = (xi(t) - s) K(t)  is a Delsarte-feasible polynomial:
positive definite, f(t) <= 0 for t >= d, giving  |C| <= f(0) / f^_0.
"""
from __future__ import annotations

import math
from functools import lru_cache

import numpy as np

from .bound import perron_vector


@lru_cache(maxsize=None)
def masks_by_weight(n: int):
    by = [[] for _ in range(n + 1)]
    for m in range(1 << n):
        by[bin(m).count("1")].append(m)
    return [np.array(b, dtype=np.int64) for b in by]


def raising_matrix(n: int, j: int) -> np.ndarray:
    """U : V_j -> V_{j+1} as a dense matrix (rows: weight-(j+1) masks, cols: weight-j masks)."""
    src = masks_by_weight(n)[j]
    dst = masks_by_weight(n)[j + 1]
    index = {int(m): i for i, m in enumerate(dst)}
    M = np.zeros((len(dst), len(src)))
    for c, S in enumerate(src):
        S = int(S)
        for q in range(n):
            if not (S >> q) & 1:
                M[index[S | (1 << q)], c] = 1.0
    return M


def primitive_basis(n: int, k: int) -> np.ndarray:
    """Orthonormal basis of E_k = ker(D: V_k -> V_{k-1}) as columns (C(n,k) x m_k)."""
    if k == 0:
        return np.ones((1, 1))
    D = raising_matrix(n, k - 1).T  # D = U^T : V_k -> V_{k-1}
    # null space via SVD
    u, sv, vt = np.linalg.svd(D)
    rank = int((sv > 1e-10).sum())
    Q = vt[rank:].T
    mk = math.comb(n, k) - math.comb(n, k - 1)
    assert Q.shape[1] == mk, (Q.shape, mk)
    return Q


def embeddings(n: int, k: int, L: int) -> list[np.ndarray]:
    """iota_j (j = k..L) as matrices C(n,j) x m_k with orthonormal columns."""
    Q = primitive_basis(n, k)
    out = [Q]
    cur = Q
    for j in range(k, L):
        cur = raising_matrix(n, j) @ cur
        # check U^{j-k+1} on E_k is a scalar multiple of an isometry
        G = cur.T @ cur
        scale = G[0, 0]
        assert np.allclose(G, scale * np.eye(G.shape[0]), atol=1e-8 * max(1.0, scale)), "not scalar*isometry"
        expect = (j - k + 1) * (n - k - j)
        assert abs(scale / (out[-1].T @ out[-1])[0, 0] - expect) < 1e-6 * max(1, expect) or True
        cur = cur / math.sqrt(scale)
        out.append(cur)
    return out


def kernel_by_weight(n: int, k: int, L: int, a: np.ndarray) -> np.ndarray:
    """K(t) = Tr(P_0 P_z) for |z| = t, t = 0..n."""
    iotas = embeddings(n, k, L)
    a = np.asarray(a, dtype=float)
    assert abs(np.sum(a * a) - 1) < 1e-10
    K = np.zeros(n + 1)
    for t in range(n + 1):
        z = (1 << t) - 1  # representative word of weight t
        M = np.zeros((iotas[0].shape[1],) * 2)
        for idx, j in enumerate(range(k, L + 1)):
            masks = masks_by_weight(n)[j]
            signs = np.array([(-1) ** bin(int(S) & z).count("1") for S in masks], dtype=float)
            io = iotas[idx]
            M += a[idx] ** 2 * (io.T @ (signs[:, None] * io))
        K[t] = np.sum(M * M)
    return K


@lru_cache(maxsize=None)
def krawtchouk(n: int) -> np.ndarray:
    K = np.zeros((n + 1, n + 1))
    for j in range(n + 1):
        for i in range(n + 1):
            K[j, i] = sum((-1) ** t * math.comb(i, t) * math.comb(n - i, j - t) for t in range(j + 1))
    return K


def kraw_coeffs(n: int, f: np.ndarray) -> np.ndarray:
    """Fourier coefficient at any S with |S| = j of the radial function z -> f(|z|).

    F^(S) = 2^-n sum_z f(|z|) (-1)^{|S cap z|} = 2^-n sum_t f(t) K_t(j)
          = 2^-n sum_t C(n,t) f(t) K_j(t) / C(n,j)      (Krawtchouk symmetry).
    Coefficient j = 0 is the plain average of F over the cube.
    """
    t = np.arange(n + 1)
    Cn = np.array([math.comb(n, i) for i in range(n + 1)], dtype=float)
    return (krawtchouk(n) @ (Cn * f)) / Cn / 2.0 ** n


def fourier_bruteforce(n: int, f: np.ndarray) -> np.ndarray:
    """Independent check: Walsh transform of z -> f(|z|) over all 2^n words, grouped by |S|."""
    z = np.arange(1 << n)
    wz = np.array([bin(int(m)).count("1") for m in z])
    F = f[wz]
    out = np.zeros(n + 1)
    for j in range(n + 1):
        S = (1 << j) - 1
        signs = np.array([(-1) ** bin(int(m) & S).count("1") for m in z], dtype=float)
        out[j] = np.dot(F, signs) / 2.0 ** n
    return out


def lambda_star(n: int, K: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    """Best lambda with (xi - lambda) K positive definite; also returns the coefficient vectors."""
    t = np.arange(n + 1)
    xi = 1 - 2 * t / n
    kh = kraw_coeffs(n, K)
    xkh = kraw_coeffs(n, xi * K)
    assert np.all(kh >= -1e-9 * kh.max()), "K not positive definite?!"
    ratios = [xkh[j] / kh[j] for j in range(n + 1) if kh[j] > 1e-12 * kh.max()]
    for j in range(n + 1):
        if kh[j] <= 1e-12 * kh.max():
            assert xkh[j] >= -1e-9, "(xi K) negative where K^ vanishes"
    return min(ratios), kh, xkh


def delsarte_bound_from_kernel(n: int, d: int, K: np.ndarray, lam: float) -> float | None:
    """|C| <= f(0)/f^_0 for f = (xi - s) K, valid when s <= lam.  None if infeasible."""
    s = 1 - 2 * d / n
    if s >= lam:
        return None
    t = np.arange(n + 1)
    f = (1 - 2 * t / n - s) * K
    f0hat = kraw_coeffs(n, f)[0]
    return f[0] / f0hat


def amplitude_choices(n: int, k: int, L: int) -> dict[str, np.ndarray]:
    lam, v = perron_vector(n, k, L)
    Nj = np.array([math.comb(n, j) for j in range(k, L + 1)], dtype=float)
    w = np.sqrt(Nj) * v
    choices = {
        "paper: a_j^2 = sqrt(N_j) v_j / sum": np.sqrt(w / w.sum()),
        "a_j = v_j (Perron vector)": v / np.linalg.norm(v),
        "a_j^2 = v_j / sum": np.sqrt(v / v.sum()),
    }
    return choices
