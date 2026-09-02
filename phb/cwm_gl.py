r"""
m-row layer graphs via GL_m recoupling (general m), and the conjectured closed form C(m).

Stabilizer irrep E = S^{eps} x triv with eps an (m-1)-row shape of w; ambient lambda with m rows interlacing eps.
    p(lambda -> lambda') = (w/N) (f^{lambda'}/f^{nu}) tau^2,
    tau = sum_t (f^{eps - e_t}/f^{eps}) R_t(lambda, nu) R_t(lambda', nu),         nu = lambda - e_r,
    R_t = normalised overlap of the two coupling schemes of V_lambda in V_{eps - e_t} (x) C^m (x) Sym^N.
Conjecture C(m):  R_t(lambda, nu)^2 = prod_{k!=r}|P_t-Q_k-1| prod_{k!=t}|Q_r-P_k| / (prod_{k!=t}|P_t-P_k-1| prod_{k!=r}|Q_r-Q_k|),
    Q_k = lambda_k + m - k, P_k = eps_k + m - k (eps padded with zeros), k = 1..m.
"""
from __future__ import annotations

import math
from fractions import Fraction
from functools import lru_cache

import numpy as np

from .glm import GLmIrrep, Tensor, intertwiner, intertwiner_partial


def hook_dim(shape) -> int:
    shape = [x for x in shape if x > 0]
    n = sum(shape)
    conj = [sum(1 for r in shape if r > c) for c in range(shape[0])] if shape else []
    h = 1
    for r, row in enumerate(shape):
        for c in range(row):
            h *= (row - c - 1) + (conj[c] - r - 1) + 1
    return math.factorial(n) // h


def pad(shape, m):
    return tuple(shape) + (0,) * (m - len(shape))


@lru_cache(maxsize=None)
def irrep(hw):
    return GLmIrrep(tuple(hw))


@lru_cache(maxsize=None)
def tensor(hw1, hw2):
    return Tensor(irrep(hw1), irrep(hw2))


def hw_vector(T, wt):
    idx, K = T.hw_vectors(tuple(wt))
    assert K.shape[1] == 1, f"multiplicity {K.shape[1]} for weight {wt}"
    t = np.zeros(T.dim); t[idx] = K[:, 0]
    return t


@lru_cache(maxsize=None)
def full_intertwiner(hw_src, hw1, hw2):
    V = irrep(hw_src); T = tensor(hw1, hw2)
    return intertwiner(V, T, hw_vector(T, hw_src))


def R_overlap(lam, nu, eps, eps_t, N, m):
    """Normalised overlap <A_t | B_nu> for V_lam inside V_{eps_t} (x) C^m (x) Sym^N (all shapes padded to m rows)."""
    lam, nu, eps, eps_t = pad(lam, m), pad(nu, m), pad(eps, m), pad(eps_t, m)
    Cm = pad((1,), m); SymN = pad((N,), m)
    Ve, Vet, VN, Vm = irrep(eps), irrep(eps_t), irrep(SymN), irrep(Cm)
    T_eN = tensor(eps, SymN)
    a_vec = hw_vector(T_eN, lam)
    psi = full_intertwiner(eps, eps_t, Cm)
    A = (psi @ a_vec.reshape(Ve.dim, VN.dim)).reshape(-1)             # in (V_{eps_t} (x) C^m) (x) Sym^N
    T_nm = tensor(nu, Cm)
    b_vec = hw_vector(T_nm, lam).reshape(irrep(nu).dim, Vm.dim)
    T_etN = tensor(eps_t, SymN)
    needed = [i for i in range(irrep(nu).dim) if np.any(b_vec[i] != 0)]
    cols = intertwiner_partial(irrep(nu), T_etN, hw_vector(T_etN, nu), needed)
    B = np.zeros((T_etN.dim, Vm.dim))
    for i in needed:
        B += np.outer(cols[i], b_vec[i])
    B = B.reshape(Vet.dim, VN.dim, Vm.dim).transpose(0, 2, 1).reshape(-1)   # -> (V_{eps_t} (x) C^m) (x) Sym^N
    norm2 = np.kron(np.kron(Vet.norm2, Vm.norm2), VN.norm2)
    ip = float(np.dot(A, norm2 * B)); na = math.sqrt(float(np.dot(A, norm2 * A))); nb = math.sqrt(float(np.dot(B, norm2 * B)))
    return ip / (na * nb)


def valid(shape):
    return all(shape[i] >= shape[i + 1] for i in range(len(shape) - 1)) and shape[-1] >= 0


def products(n, w, lam, lam_p, eps, m):
    """For a move lam -> lam': the products R_t(lam,nu) R_t(lam',nu) for each removable t of eps (signed, with
    consistent conventions across t), plus the branching ratios f^{eps-e_t}/f^eps."""
    N = n - w
    d = [b - a for a, b in zip(pad(lam, m), pad(lam_p, m))]
    r = d.index(-1); nu = list(pad(lam, m)); nu[r] -= 1; nu = tuple(nu)
    out = {}
    for t in range(len(eps)):
        e = list(eps); e[t] -= 1
        if not valid(e):
            continue
        try:
            Rl = R_overlap(lam, nu, eps, tuple(e), N, m)
            Rp = R_overlap(lam_p, nu, eps, tuple(e), N, m)
        except AssertionError:
            continue
        out[t + 1] = (Rl * Rp, Fraction(hook_dim(e), hook_dim(eps)), Rl, Rp)
    return out, r + 1, d.index(1) + 1, nu


def coefficient_numeric(n, w, lam, lam_p, eps, m):
    pr, r, rp, nu = products(n, w, lam, lam_p, eps, m)
    tau = sum(float(ratio) * prod for (prod, ratio, _, _) in pr.values())
    return (w / (n - w)) * float(Fraction(hook_dim(pad(lam_p, m)), hook_dim(nu))) * tau ** 2


# ---------------------------------------------------------------- conjectured closed form C(m)
def partial_hooks(shape, m):
    s = pad(shape, m)
    return [s[k] + m - 1 - k for k in range(m)]


def R2_conj(lam, r, eps, t, m):
    Q = partial_hooks(lam, m); P = partial_hooks(eps, m)
    r0, t0 = r - 1, t - 1
    num = Fraction(1); den = Fraction(1)
    for k in range(m):
        if k != r0:
            num *= abs(P[t0] - Q[k] - 1); den *= abs(Q[r0] - Q[k])
        if k != t0:
            num *= abs(Q[r0] - P[k]); den *= abs(P[t0] - P[k] - 1)
    return num / den


def coefficient_conj(n, w, lam, lam_p, eps, m, sign):
    """Closed-form coefficient with sign(t, r, r') giving the relative sign of term t."""
    N = n - w
    lam, lam_p = pad(lam, m), pad(lam_p, m)
    d = [b - a for a, b in zip(lam, lam_p)]
    r = d.index(-1) + 1; rp = d.index(1) + 1
    nu = list(lam); nu[r - 1] -= 1; nu = tuple(nu)
    tau = 0.0
    for t in range(1, len(eps) + 1):
        e = list(eps); e[t - 1] -= 1
        if not valid(e):
            continue
        ratio = hook_dim(e) / hook_dim(eps)
        tau += sign(t, r, rp) * ratio * math.sqrt(float(R2_conj(lam, r, eps, t, m) * R2_conj(lam_p, rp, eps, t, m)))
    return (w / N) * float(Fraction(hook_dim(lam_p), hook_dim(nu))) * tau ** 2
