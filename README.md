# A two-row representation graph improves the primitive-harmonic bound on binary codes

Code, data and checks for the paper of the same title (Harish K, 2026; `paper/main.tex`, `paper/main.pdf`).

**Main result.** The primitive-harmonic (moving-subspace) method of OpenAI's *Ten Advances in Mathematics and
Theoretical Computer Science* (Aug 2026, Chapter 2) gave the first improvement since 1977 of the MRRW upper bound on
the rate of binary codes. Its binary certificates use representations of the hyperoctahedral group B_n indexed by
pairs of one-row Young diagrams. This repository builds the analogue with pairs of **two-row** diagrams, proves the
closed forms of its coordinate-transition coefficients (eight rational functions; Schur-Weyl duality and 6j-symbols
with a spin-1/2 entry), and derives the exponent kappa_2row(delta), which lies strictly below the paper's whole-cube
exponent at every delta and therefore improves the paper's Theorem 1.1 for every delta >= 0.2350 (at delta = 0.3:
0.248150 against 0.248376, with MRRW at 0.250225). A second part treats constant-weight layers with any number of
ambient rows (closed forms as products of partial-hook differences, verified exactly on every computed case), and a
third part is an independent numerical verification of the paper's certificates against exact Delsarte linear programs.

Research note with all details and figures: `report/beyond-mrrw-audit.html` (build with `python report/build_report.py`).

Disclosure: the computations, the discovery of the closed forms and a first draft of the text were carried out with the
assistance of an AI system (Claude, Anthropic); the author takes full responsibility for the results and proofs.

## How to reproduce the main numbers
```
pip install numpy scipy sympy mpmath matplotlib
python experiments/hyperoct_proof_check.py      # Theorem 3.1: 6j table, the eight identities, sum rule, reciprocity
python experiments/hyperoct_exponent.py         # Table 1: kappa_2row(delta) vs kappa_H and M2
python experiments/cw2_sign.py                  # Section 5 (three rows): closed form vs exact S_n coefficients
python experiments/cwm_test.py 16               # Section 5 (four rows): conjecture C(3) and the sign rule
```
Raw outputs of every run are in `results/`.

## Layout

| path | what |
|---|---|
| `phb/bound.py` | Jacobi matrix (22), Perron eigenvalue, bound (23) in log space |
| `phb/delsarte_lp.py` | Delsarte LP via HiGHS (reliable for n ≤ 40) |
| `phb/exact_lp.py` | exact rational simplex for the Delsarte LP (n ≤ 64 and beyond) |
| `phb/certificate.py` | from-scratch construction of the moving-primitive-subspace kernel K(t); Krawtchouk transform; λ*(a) |
| `experiments/test1_vs_lp.py` | Test 1: bound ≥ LP for all (n,d,k,L), n ≤ 40 |
| `experiments/test1_exact.py` | Test 1 with the exact LP, n = 41..64 |
| `experiments/test2_certificate.py` | Test 2: λ*(a) vs λ, Delsarte sharpening, small n |
| `experiments/asymptotics.py` | κ_H(δ), MRRW1, MRRW2, the δ = 4/13 witness |
| `experiments/crossover.py` | finite-length crossover scans (`python experiments/crossover.py p q m1,m2,...`) |
| `experiments/make_figures.py` | Figures 1–2 |
| `phb/johnson.py` | constant-weight bound (46), associated Hahn coefficients, Ĵ, Λ (6), κ_CW (8) |
| `phb/johnson_lp.py` | exact Delsarte LP for the Johnson scheme |
| `phb/johnson_certificate.py` | explicit Johnson-layer reconstruction, measured coefficients, kernel, λ* |
| `experiments/cw_*.py`, `make_figure3.py` | constant-weight tests, exponent, crossover, Figure 3 |
| `phb/spherical.py` | spherical one-row/two-row/general representation-graph bounds (73), (76), (81), Weyl dims (113), hierarchy asymptotics, kappa_r, gamma_r |
| `phb/spherical_lp.py` | degree-capped Delsarte-Goethals-Seidel LP |
| `experiments/sph_*.py`, `make_figure4.py` | spherical checks, LP test, packing levels, kissing exponents, crossover, Figure 4 |
| `phb/hyperoct.py` | hyperoctahedral (B_n) two-row representation graph: exact transition coefficients by class-sum projection |
| `phb/hyperoct_formulas.py` | the eight conjectured closed forms (verified exactly on all computed cases) |
| `phb/hyperoct_asymptotics.py` | limiting weights, Perron limit, kappa_2row optimisation |
| `experiments/hyperoct_*.py`, `make_figure5.py` | collection, formula mining, verification, exponent table, finite-n scans, Figure 5 |
| `phb/layer3.py` | three-row constant-weight (CW2) graph: exact S_n transition coefficients on a Johnson layer (permutation modules, Specht projections, explicit E-copy) |
| `phb/gl3.py` | gl_3 Gelfand-Tsetlin modules (checked exactly), invariant form, tensor products, highest-weight vectors, intertwiners |
| `phb/cw2_gl3.py` | CW2 coefficients via GL_3 recoupling (p = (w/N)(f^lam'/f^nu) tau^2) |
| `phb/cw2_formulas.py` | Proposition 7.1: closed form of every CW2 coefficient (partial-hook products, sign (-1)^(r+r')) |
| `phb/cw2_asymptotics.py` | limits, Lambda_CW2 = 1 - sum (sqrt p - sqrt p')^2, threshold, exponent optimisation kappa_CW2 |
| `experiments/layer3_*.py`, `cw2_*.py`, `make_figure6.py` | data collection, formula mining and verification, sign rule, exponent grid and refinement, Figure 6 |
| `phb/glm.py` | gl_m Gelfand-Tsetlin modules for any m (commutators, Serre, adjointness, Weyl dims checked for m <= 5) |
| `phb/cwm_gl.py` | m-row layer graphs: general recoupling overlaps and the closed form C(m) with the sign rule |
| `phb/cwm_asymptotics.py` | m-row limits, Lambda, exponent kappa_m |
| `experiments/cwm_test.py`, `cwm_kappa.py` | four-row verification of C(3) and sign rule; four-row exponent |
| `GOALS.md` | goal sheet and log of the night session (Phase 6) |
| `results/` | raw outputs of every run |

## Requirements

Python 3.12, numpy, scipy, mpmath, matplotlib (PyMuPDF only for extracting the source PDFs).

## Headline results

* 0 violations of bound ≥ exact Delsarte LP optimum over all (n, d) with 4 ≤ n ≤ 64 and every feasible (k, L).
* In the from-scratch reconstruction, the best positive-definite λ equals the Perron eigenvalue of (22) to 6 decimals
  in all 13 configurations tested; a multi-start optimizer cannot improve the paper's amplitude normalization.
* κ_H(δ) < MRRW1(δ) for all δ; κ_H(δ) < MRRW2(δ) exactly for δ > δ₀ = 0.19504.
* Finite-length crossover (new certificate beats classical): n = 30 (δ = 1/10), n = 160 (δ = 1/4, isolated wins from 20),
  n = 1105 (δ = 4/13, isolated wins from 468).
* Replacing trace Cauchy–Schwarz by the exact constant Krawtchouk coefficient of K tightens (23) by 2–7 % at n ≤ 12.

Constant-weight (Johnson-layer) construction, paper Section 3:
* classical Johnson matrix reproduces the exact distance spectrum (1e-16); identity (50) and the β=γ=0 → M2 reduction hold to 1e-16;
* 0 violations of bound (46) ≥ exact Johnson-scheme LP over 1,090 (n,w,d) triples, n ≤ 30, every admissible (p,q,L);
* measured associated Hahn coefficients from an explicit construction match (36)-(37) to 1e-16 (11 (p,q) pairs); λ* = λ_max(Ĵ) in 21 configurations;
* κ_CW(δ) < M2(δ) for all δ (gain 1e-6 at δ=0.02 ... 3.3e-3 at δ≈0.25); κ_CW ≤ κ_H everywhere, strictly below δ₁ = 0.2350.

Spherical codes and sphere packing, paper Sections 4-8:
* all transcription identities hold to 1e-14 (Gegenbauer roots, (81)=(76), (77) sum-to-one, (78) reciprocity with Weyl (113), recurrence (68) by quadrature);
* 0 violations of the one-row/two-row bounds vs the spherical LP in 64 (n, s) cases; classical limits reproduce KL 1978 (0.5990 packing, 0.4009 kissing);
* independent optimization of the hierarchy reproduces the paper's Figure 4 deficits from λ* = ½ log2(2π/e): 5.3e-3, 1.5e-3, 2.0e-4, 1.5e-5, 1.7e-6 (classical, one-row, levels 1-3);
* kissing-number exponent upper bound lowered from 0.4009 (KL) to 0.3966 (level 1; cap reduction no longer helps); finite-n crossover at s = 1/2: n = 96 (first), consistent from n = 384.

NEW (Section 6 of the note, Theorems 6.1-6.2, PROVED): the binary two-row representation graph gives
kappa_2row(delta) < kappa_H(delta) for all delta and beats the paper's Theorem 1.1 for delta >= 0.235
(e.g. delta = 0.3: 0.248150 vs paper 0.248376 vs MRRW2 0.250225). At the middle level u = 1/2 the two-row graph
reproduces MRRW2 exactly. Closed forms: `phb/hyperoct_formulas.py`; data: `results/hyperoct_coeffs_n11.jsonl`.
Proof of the coefficient formulas: each coefficient = (branching ratio) x (2 j_alpha+1)(2 j_nu+1) x (6j-symbol with a
spin-1/2 entry)^2 by Schur-Weyl duality; `experiments/hyperoct_proof_check.py` validates Edmonds' 6j table against exact
values and proves the eight identities, the sum rule and the dimension reciprocity symbolically (results/hyperoct_proof_check.txt).

NEW (Section 7 of the note, Proposition 7.1, verified): the paper's constant-weight construction with the ambient
S_n-irreps allowed THREE rows (E = S^{(w-p,p)} x trivial, vertices = three-row shapes interlacing (w-p,p); this is the
largest multiplicity-free extension, since a two-row S_N part on top of three-row shapes has LR multiplicity 2).
Coefficients: exact S_n numerics for n <= 12 (`results/layer3_coeffs_n12.jsonl`), reduced by Schur-Weyl duality to GL_3
recoupling overlaps and then to the closed form R_t^2 = prod_{k!=r}|P_t-Q_k-1| prod_{k!=t}|Q_r-P_k| /
(prod_{k!=t}|P_t-P_k-1| prod_{k!=r}|Q_r-Q_k|) with partial hooks Q = lambda + (2,1,0), P = (w-p+2, p+1, 0); the coefficient
is (w/N)(f^lam'/f^nu) [ratio_1 R_1 R_1' + (-1)^(r+r') ratio_2 R_2 R_2']^2 (Biedenharn-Louck fundamental-Wigner structure).
Verified: all 366 exact S_n coefficients (2e-14), 1,458 GL_3 overlaps (6e-15), 25 random cases n <= 29 (6e-16),
reciprocity exact in rational arithmetic (364/364), self-loop sum rule (6e-14). Exponent kappa_CW2 (`results/cw2_kappa_final.json`):
beats the paper's kappa_CW for delta <= 0.12 by at most 6.5e-6 bits (delta = 0.1: 0.6925510 vs 0.6925575) and loses to it
from delta = 0.15 on (the paper's gamma > 0 S_N part wins there); beats its own gamma = 0 slice at every delta. Not a Eureka:
a new closed form and a sixth-decimal improvement at small distances.

NEW (Section 8 of the note, Proposition 8.1, verified at four rows): the same construction with an (m-1)-row stabilizer
shape and m-row ambient shapes, for any m. The partial-hook formula holds with k over m rows, and the recoupling sum has
m-1 terms with signs sigma_t = (-1)^([r<=t]+[r'<=t]) (negative iff row t lies between the moving rows). Verified at m = 4:
183 squared overlaps exact (1e-15), reciprocity exact 517/517, exact regression to m = 3. Identified with Hecht (1975,
CMP 41, 135) U(N) Racah coefficients with two totally symmetric irreps (axial distances = partial-hook differences).
Exponent (`results/cwm_kappa_all.json`): the fourth row adds +1.3e-10 (delta .02), +1.2e-8 (.05), +2.8e-7 (.10),
+5.2e-7 (.12) over three rows, about 1% of the third row's gain; rows are a convergent series with a tiny sum.
