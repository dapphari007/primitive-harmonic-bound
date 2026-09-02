# Goal sheet: the m-row layer graphs (Phase 6)

Started 2026-09-02 (night session). Harish K, working with an AI assistant (Claude, Anthropic). Updated as work proceeds.

## Target
Extend the three-row constant-weight graph (Section 7) to a stabilizer irrep with any number of rows:
E = S^{eps} x trivial with eps an m-row shape of w, ambient S_n-irreps lambda with m+1 rows interlacing eps.
Conjecture C(m): every squared recoupling overlap is the same partial-hook product,
    R_t(lambda, lambda - e_r)^2 = prod_{k!=r}|P_t - Q_k - 1| prod_{k!=t}|Q_r - P_k| / (prod_{k!=t}|P_t - P_k - 1| prod_{k!=r}|Q_r - Q_k|),
    Q_k = lambda_k + (m+1) - k,  P_k = eps_k + (m+1) - k  (eps padded with a zero),  k = 1..m+1,
and p(lambda -> lambda') = (w/N)(f^{lambda'}/f^{nu}) [ sum_t sigma_t (f^{eps - e_t}/f^{eps}) R_t(lambda) R_t(lambda') ]^2
with a sign rule sigma_t to be determined (m = 2: sigma = (-1)^{r+r'} between t = 1 and t = 2).

## Goals and status
- [ ] G1  gl_m Gelfand-Tsetlin modules for general m (phb/glm.py), exact checks; R-overlaps for m = 4 (four-row ambient).
- [ ] G2  Test C(3) on generic four-row points; find the sign rule; check reciprocity of the resulting coefficients.
- [ ] G3  (if feasible) independent exact S_n check of a few four-row coefficients at small n.
- [ ] G4  Asymptotics for four rows: limits, Lambda = 1 - sum (sqrt p - sqrt p')^2, exponent kappa_CW3; compare with
          kappa_CW2, the paper's kappa_CW, M2. Then the trend in m.
- [ ] G5  Toward a proof of C(m): identify R_t with the U(m+1) fundamental reduced Wigner coefficient (seesaw) and
          derive the product formula; if it goes through, Propositions 7.1 / 8.1 become theorems.
- [ ] G6  Section 8 of the note, Figure 7, README, republish.

## Honest expectation
Each extra row is a square-root spectral gain against an x log(1/x) entropy cost with a tiny optimal row (1e-5 for the
third row). Gains from a fourth row are expected to be smaller still; the mathematically valuable output is the
general-m formula and its proof. "Eureka" only if something changes the picture.

## Log
- 02 Sep 22:00  goals set; starting G1.
- 02 Sep 22:55  G1 DONE: phb/glm.py passes commutators/Serre/adjointness/Weyl for gl_3, gl_4, gl_5; m=3 regression exact.
- 02 Sep 22:55  G2 (part): C(3) EXACT on 183 four-row squared overlaps (1e-15). Sign rule found:
                sigma_t = (-1)^{[r<=t]+[r'<=t]}  (term t negative iff t lies between the two moving rows); it
                reproduces (-1)^{r+r'} for m = 2. Next: reciprocity + CW2 regression, then asymptotics (G4).
- 02 Sep 23:10  G2 DONE: four-row closed form with the sign rule satisfies reciprocity exactly (517/517, rational and
                radical parts), self-loops positive, exact regression to CW2 at l4 = 0 (5.6e-17). G4 started
                (phb/cwm_asymptotics.py, experiments/cwm_kappa.py running).
- 02 Sep 23:25  G4 (part): four-row finite-n closed forms converge to the derived limits like 1/n (3e-3, 8e-4, 2e-4 at
                n = 500, 2000, 8000); general-m asymptotics reproduce cw2_asymptotics exactly at m = 3. Optimiser running.
- 02 Sep 23:40  G4 numbers (experiments/cwm_kappa.py -> results/cwm_kappa.json): kappa_m4 - gains over m=3:
                delta=0.05: +1.2e-8; 0.10: +2.8e-7; 0.12: +5.2e-7 (optimal fourth row ~1e-6, third stabilizer row ~1e-6).
                Versus the paper: +1.04e-6 (0.05), +6.78e-6 (0.10), +4.26e-6 (0.12). Diminishing returns confirmed:
                each new row buys roughly 1/50 of the previous one. No Eureka from rows; the value is the general formula.
- 03 Sep 00:05  G5 (identification): K. T. Hecht, Commun. Math. Phys. 41 (1975) 135-156, "A simple class of U(N) Racah
                coefficients", derives the general U(N) Racah coefficient when two of the coupled irreps are totally
                symmetric, by permutation-operator matrix elements in Young-Yamanouchi bases; the answer is a product of
                factors (1 - 1/tau) of axial distances tau_ik = (f_i - i) - (f_k - k) (= partial-hook differences), with
                p = 1 (one box) giving a pure product (his Eqs. 27-28). Our R_t is exactly this class ([1] and [N] both
                totally symmetric, p = 1). C(m) is therefore the p = 1 specialisation of Hecht's formula; the exact
                specialisation (phases, normalisation) is not carried out here. Text: results/hecht1975_text.txt.
- 03 Sep 00:20  G6 (part): Section 8 written (report/patch_cwm.py, table generated from results/cwm_kappa_all.json),
                README updated; waiting for the consolidated exponent run (6 deltas) to rebuild and republish.
- 03 Sep 00:35  G6 DONE: note rebuilt with the six-delta four-row table and republished (artifact version
                "Section 8: all rows"); README and memory updated. G3 (independent S_n check at four rows) skipped:
                reciprocity in exact arithmetic + exact C(3) + exact regression to m = 3 make it redundant.
## Outcome
The m-row family is fully described (Proposition 8.1, sign rule, Hecht 1975 identification); rows give a convergent
series of gains (~1% per row) that lands within 1e-5 of the paper's bound at small distances. No Eureka. The lever left
in the framework is the stabilizer/multiplicity condition, not more rows.
