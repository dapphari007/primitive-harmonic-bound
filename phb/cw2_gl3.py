r"""
CW2 coefficients via Schur-Weyl duality in gl_3 modules.

For an off-diagonal move lambda -> lambda' = lambda - box_r + box_r', with nu = lambda - box_r, eps = (w-p, p),
eps'_t in {(w-p-1, p), (w-p, p-1)}:
    p(lambda -> lambda') = w f^{lambda'} tau^2 / (N f^nu),
    tau = sum_t (f^{eps'_t} / f^eps) R_t(lambda, nu) R_t(lambda', nu),
    R_t(lambda, nu) = normalised overlap of two gl_3 coupling schemes for V_lambda inside V_{eps'_t} (x) C^3 (x) Sym^N:
        A_t : V_lambda -> V_eps (x) Sym^N -> (V_{eps'_t} (x) C^3) (x) Sym^N,
        B_nu: V_lambda -> V_nu (x) C^3 -> (V_{eps'_t} (x) Sym^N) (x) C^3  (factors reordered).
Derivation: reduction of the S_n computation through Frobenius reciprocity, the orthogonality of ell_x to the
all-ones vector (which removes the complement slots), and the identification of multiplicity spaces with
gl_3 intertwiner spaces (three-row shapes).  Validated against exact S_n numerics in experiments/cw2_validate.py.
"""
from __future__ import annotations

import math
from functools import lru_cache

import numpy as np

from .gl3 import GL3Irrep, Tensor, intertwiner, intertwiner_partial


def hook_dim(shape) -> int:
    shape = [x for x in shape if x > 0]
    n = sum(shape)
    conj = [sum(1 for r in shape if r > c) for c in range(shape[0])] if shape else []
    h = 1
    for r, row in enumerate(shape):
        for c in range(row):
            h *= (row - c - 1) + (conj[c] - r - 1) + 1
    return math.factorial(n) // h


@lru_cache(maxsize=None)
def irrep(hw):
    return GL3Irrep(tuple(hw))


@lru_cache(maxsize=None)
def tensor(hw1, hw2):
    return Tensor(irrep(hw1), irrep(hw2))


def hw_vector(T: Tensor, wt):
    idx, K = T.hw_vectors(tuple(wt))
    assert K.shape[1] == 1, f"multiplicity {K.shape[1]} for weight {wt}"
    t = np.zeros(T.dim); t[idx] = K[:, 0]
    return t


@lru_cache(maxsize=None)
def full_intertwiner(hw_src, hw1, hw2):
    """Phi: V_{hw_src} -> V_{hw1} (x) V_{hw2} as a dense matrix (unique up to sign)."""
    V = irrep(hw_src); T = tensor(hw1, hw2)
    return intertwiner(V, T, hw_vector(T, hw_src))


def reorder_last_two(vec, d1, d2, d3):
    """(V1 (x) V2) (x) V3 -> (V1 (x) V3) (x) V2 index permutation."""
    return vec.reshape(d1, d2, d3).transpose(0, 2, 1).reshape(-1)


def R_overlap(lam, nu, eps, eps_t, N):
    """Normalised overlap <A_t | B_nu> for V_lam inside V_{eps_t} (x) C3 (x) Sym^N."""
    C3 = (1, 0, 0); SymN = (N, 0, 0)
    eps = tuple(eps) + (0,) * (3 - len(eps)); eps_t = tuple(eps_t) + (0,) * (3 - len(eps_t))
    Ve, Vet, VN, V3 = irrep(eps), irrep(eps_t), irrep(SymN), irrep(C3)
    # scheme A: hw vector of weight lam in V_eps (x) Sym^N, then (psi_t (x) id)
    T_eN = tensor(eps, SymN)
    a_vec = hw_vector(T_eN, lam)                                   # in V_eps (x) Sym^N
    psi = full_intertwiner(eps, eps_t, C3)                         # V_eps -> V_{eps_t} (x) C3
    A = (psi @ a_vec.reshape(Ve.dim, VN.dim)).reshape(-1)          # in (V_{eps_t} (x) C3) (x) Sym^N
    # scheme B: hw vector of weight lam in V_nu (x) C3 = sum_i x_i (x) e_i, then Phi_nu on the few x_i, reorder
    T_n3 = tensor(nu, C3)
    b_vec = hw_vector(T_n3, lam).reshape(irrep(nu).dim, V3.dim)   # rows: GT basis of V_nu, cols: e_i
    T_etN = tensor(eps_t, SymN)
    needed = [i for i in range(irrep(nu).dim) if np.any(b_vec[i] != 0)]
    cols = intertwiner_partial(irrep(nu), T_etN, hw_vector(T_etN, nu), needed)
    B = np.zeros((T_etN.dim, V3.dim))
    for i in needed:
        B += np.outer(cols[i], b_vec[i])
    B = reorder_last_two(B.reshape(-1), Vet.dim, VN.dim, V3.dim)   # -> (V_{eps_t} (x) C3) (x) Sym^N
    norm2 = np.kron(np.kron(Vet.norm2, V3.norm2), VN.norm2)
    ip = float(np.dot(A, norm2 * B)); na = math.sqrt(float(np.dot(A, norm2 * A))); nb = math.sqrt(float(np.dot(B, norm2 * B)))
    return ip / (na * nb)


def cw2_coefficient(n, w, p, lam, lam_p):
    """p(lambda -> lambda') for an off-diagonal move of the CW2 graph (complement degree q = 0)."""
    N = n - w
    lam = tuple(lam); lam_p = tuple(lam_p)
    d = [b - a for a, b in zip(lam, lam_p)]
    r = d.index(-1); nu = list(lam); nu[r] -= 1; nu = tuple(nu)
    eps = (w - p, p)
    tau = 0.0
    for eps_t in [(w - p - 1, p), (w - p, p - 1)]:
        if eps_t[0] < eps_t[1] or eps_t[1] < 0:
            continue
        # eps_t must sit in V_nu (x) ... : the hw vectors must exist; skip if the coupling is impossible
        try:
            Rl = R_overlap(lam, nu, eps, eps_t, N)
            Rp = R_overlap(lam_p, nu, eps, eps_t, N)
        except AssertionError:
            continue
        tau += (hook_dim(eps_t) / hook_dim(eps)) * Rl * Rp
    return w * hook_dim(lam_p) * tau ** 2 / (N * hook_dim(nu))
