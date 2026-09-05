# Ready-to-send emails

Two emails, in the order you send them. Replace the CAPITALISED placeholders. Nothing else needs editing.

---

## Email 1 — endorsement request (send first, after arXiv gives you a code)

You only get the endorsement code after you register on arXiv and begin a submission to math.CO. Send this to a
researcher who posts regularly to math.CO (combinatorics) or cs.IT (information theory): a professor in your city's
university mathematics or electrical-engineering department, a coding-theory author whose papers you have read, or a
former teacher. One is enough. Endorsement means only "this person's submission looks like genuine research"; it is
not a peer review and carries no responsibility for the contents.

**Subject:** arXiv endorsement request for math.CO — improvement of the MRRW bound on binary codes

Dear Professor SURNAME,

I am an independent researcher and I would like to post my first preprint to arXiv, in math.CO. New submitters need an
endorsement, and arXiv suggests asking someone who publishes in the same area, which is why I am writing to you.

The paper improves the best known upper bound on the rate of binary error-correcting codes. In August 2026 OpenAI's
"Ten advances in mathematics and theoretical computer science" gave the first improvement since 1977 of the
McEliece-Rodemich-Rumsey-Welch bound, using a moving-subspace (primitive-harmonic) method whose binary certificates are
built from hyperoctahedral representations indexed by pairs of one-row Young diagrams. I build the analogue for pairs
of two-row diagrams, prove closed forms for its transition coefficients using Schur-Weyl duality and 6j-symbols with a
spin-1/2 entry, and obtain an exponent that is strictly smaller than theirs for every relative distance above
delta = 0.235. At delta = 0.3 the upper bound moves from 0.248376 to 0.248150.

Everything is public and checkable:

  Manuscript (9 pages): https://github.com/dapphari007/primitive-harmonic-bound/releases/download/v1.1/main.pdf
  Code, data and verification scripts: https://github.com/dapphari007/primitive-harmonic-bound
  Archived with a DOI: https://doi.org/10.5281/zenodo.22363306

If you are willing, the endorsement code is CODE and the link is https://arxiv.org/auth/endorse?x=CODE

I would of course also be grateful for any comment on the proof itself, though I understand that endorsement does not
imply any review.

With thanks and best regards,
Harish K
Arwin@kaaspro.com

---

## Email 2 — to the authors of the OpenAI paper (send only after the preprint is live)

Find the contact address on the front matter of the paper (cdn.openai.com/pdf/ten-proofs-oai.pdf). If no address is
given, open an issue on https://github.com/openai/ten-proofs instead and paste the same text; that is public and
timestamped, which works in your favour.

**Subject:** Improvement of Theorem 1.1 (binary codes) for delta >= 0.235

Dear authors,

I have built the binary analogue of the multi-row spherical hierarchy of Chapter 2 of "Ten advances in mathematics and
theoretical computer science": a representation graph for the hyperoctahedral group whose vertices are pairs of two-row
Young diagrams, rather than the one-row pairs used in your binary certificates.

Its coordinate-transition coefficients have closed forms, proved by Schur-Weyl duality together with the recoupling of
three SU(2) spins and Edmonds' closed form for 6j-symbols with a spin-1/2 entry; the resulting exponent kappa_2row is
strictly below your whole-cube exponent kappa_H at every delta. Since your Theorem 1.1 reduces to kappa_H for
delta >= delta_1 = 0.2350, this improves the bound there. At delta = 0.3 the value moves from 0.248376 to 0.248150,
with MRRW2 at 0.250225. At the middle level the two-row graph reproduces the second MRRW bound exactly, which is an
independent check on the whole reduction.

  Preprint: arXiv:ARXIV_ID
  Code, data and machine-checked identities: https://github.com/dapphari007/primitive-harmonic-bound
  Archived: https://doi.org/10.5281/zenodo.22363306

Before building on your construction I re-derived your binary, constant-weight and spherical certificates from scratch
and tested them against exact Delsarte linear programs: no violations in roughly 2,800 cases, and your asymptotic
numbers reproduce. Those checks are in the same repository.

I would be grateful for any comments, and I would be glad to coordinate if you plan to extend the Lean formalisation to
this construction.

With best regards,
Harish K
Arwin@kaaspro.com
