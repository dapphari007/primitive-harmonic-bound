# Posting checklist

## 1. Repository and archive — DONE
- Public: https://github.com/dapphari007/primitive-harmonic-bound (MIT licence, topics set).
- Zenodo, 2026-09-05: version DOI 10.5281/zenodo.22363307, **concept DOI 10.5281/zenodo.22363306** (cite this one; it
  always resolves to the newest version). Both are in README.md and CITATION.cff. Every future GitHub release is
  archived automatically under the same concept DOI.

## 2. arXiv — your steps, in order

Everything below needs your identity and your login, so it has to be done by you. The files are ready.

**a. Register.** https://arxiv.org/user/register — real name `Harish K`, affiliation `Independent researcher`.

**b. Start the submission.** https://arxiv.org/submit
   - Licence: keep the default `arXiv.org perpetual, non-exclusive license`.
   - Primary category: `math.CO` (Combinatorics). Cross-lists: `cs.IT` (Information Theory) and `math.RT`
     (Representation Theory).

**c. Get the endorsement code.** A new account without an academic email is not yet allowed to post to math.CO, so at
   this point arXiv shows a six-character endorsement code and a link of the form
   `https://arxiv.org/auth/endorse?x=CODE`. Copy them, then send **Email 1** in `EMAILS.md` to one researcher who posts
   to math.CO or cs.IT. When they enter the code, the block disappears. Endorsement is not a review and commits the
   endorser to nothing.

**d. Upload two files** (as separate files, not a folder or an archive):
   - `paper/main.tex`
   - `paper/fig5_two_row.png`
   arXiv compiles them itself. Check the generated PDF preview: 9 pages, one figure on page 5 or 6.

**e. Metadata.**
   - Title: `A two-row representation graph improves the primitive-harmonic bound on binary codes`
   - Authors: `Harish K`
   - Comments: `9 pages, 1 figure. Code, data and machine-checked identities: https://github.com/dapphari007/primitive-harmonic-bound (DOI 10.5281/zenodo.22363306)`
   - Abstract: paste the plain-text version at the bottom of this file (the LaTeX abstract contains \cite commands,
     which the metadata field does not accept).
   - MSC classes (optional): `94B65, 05E10, 20C30`. ACM class (optional): `E.4`.

**f. Submit.** Submissions made before 14:00 US Eastern on a working day are normally announced the following evening.
   You get an identifier of the form `arXiv:2609.XXXXX`.

**g. After it is live:** put the arXiv identifier into README.md and CITATION.cff, and send **Email 2** in `EMAILS.md`.

## 3. Journal or conference (after arXiv, optional)
- IEEE Transactions on Information Theory, or Designs, Codes and Cryptography. Neither charges a submission fee.
- ISIT for a short version of Sections 3 and 4 (deadline usually in January).

## 4. Before you post — worth doing
Read Section 3.3 of the PDF until you can explain the three steps in your own words, and if you can, have one
mathematician read that section. The Zenodo DOI already fixes the date, so a few days spent on this cost you nothing.

---

## Plain-text abstract for the arXiv metadata field

The primitive-harmonic (moving-subspace) method introduced in OpenAI's "Ten advances in mathematics and theoretical
computer science" (2026) gave the first improvement since 1977 of the McEliece-Rodemich-Rumsey-Welch upper bound on the
rate R_2(delta) of binary codes. Its binary certificates use representations of the hyperoctahedral group B_n indexed by
pairs of one-row Young diagrams. We build the analogue with pairs of two-row diagrams, compute its coordinate-transition
coefficients in closed form (eight rational functions whose roots are the Littlewood-Richardson admissibility
boundaries), and prove them by Schur-Weyl duality together with the recoupling of three SU(2) spins with a spin-1/2
entry. The resulting explicit exponent kappa_2row(delta) satisfies R_2(delta) <= kappa_2row(delta) for all delta in
(0,1/2) and lies strictly below the whole-cube exponent of that paper at every delta; since the paper's Theorem 1.1
reduces to the whole-cube exponent for delta >= 0.2350, the bound is improved there. At delta = 0.3 it moves from
0.248376 to 0.248150. At the middle level the new exponent reproduces the classical second MRRW bound exactly. We also
describe the analogous extension inside a constant-weight layer to ambient shapes with any number of rows, give its
coefficients in closed form as products of partial-hook differences (identified with Hecht's class of U(N) Racah
coefficients and verified exactly on every computed case), and show that the gains from additional rows form a
convergent series of rapidly decreasing terms. All computations are reproducible from the accompanying repository.
