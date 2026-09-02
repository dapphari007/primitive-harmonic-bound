# Posting checklist

## 1. Repository (do first: it fixes the date)
1. Make the GitHub repository public (Settings > Danger zone > Change visibility), or run
   `gh repo edit dapphari007/primitive-harmonic-bound --visibility public --accept-visibility-change-consequences`.
2. Create a release `v1.0` (`gh release create v1.0 --title "v1.0" --notes "Version accompanying the arXiv preprint"`).
3. Archive the release on Zenodo (zenodo.org > GitHub integration > enable the repository > the release is archived
   automatically and receives a DOI). Put the DOI into README.md and CITATION.cff.

## 2. arXiv
- Primary category: math.CO (Combinatorics). Cross-list: cs.IT (Information Theory), math.RT (Representation Theory).
- First submission needs an endorsement for math.CO from an existing arXiv author in that category.
- Upload `paper/main.tex` and `paper/fig5_two_row.png` (single-file submission with one figure; arXiv compiles it).
- Licence: arXiv non-exclusive licence is the usual choice.
- Title: A two-row representation graph improves the primitive-harmonic bound on binary codes
- Abstract: copy from main.tex.
- Comments field: "9 pages, 1 figure. Code and data at https://github.com/dapphari007/primitive-harmonic-bound"
- arXiv requires disclosure of significant generative-AI assistance; the Acknowledgements paragraph does this.

## 3. Journal / conference (after the arXiv posting)
- IEEE Transactions on Information Theory (journal, no submission fee), or Designs, Codes and Cryptography.
- ISIT (conference; deadline usually January) for a short version of Sections 3-4.

## 4. Email to the authors of the OpenAI paper
Send after the arXiv identifier exists. Suggested text:

Subject: Improvement of Theorem 1.1 of "Ten advances" (binary codes) for delta >= 0.235

Dear authors,

I have built the binary analogue of the multi-row spherical hierarchy of Chapter 2 of your paper "Ten advances in
mathematics and theoretical computer science": a representation graph for the hyperoctahedral group whose vertices are
pairs of two-row Young diagrams. Its coordinate-transition coefficients have closed forms (eight rational functions,
proved via Schur-Weyl duality and 6j-symbols with a spin-1/2 entry), and the resulting exponent kappa_2row lies strictly
below your whole-cube exponent kappa_H at every delta. Since your Theorem 1.1 reduces to kappa_H for delta >= 0.2350,
this improves it there; at delta = 0.3 the bound moves from 0.248376 to 0.248150. At the middle level the two-row
graph reproduces the second MRRW bound exactly.

The preprint is at arXiv:XXXX.XXXXX and all code, data and checks are at
https://github.com/dapphari007/primitive-harmonic-bound. I also re-derived your binary, constant-weight and spherical
certificates independently and tested them against exact Delsarte linear programs (no violations in about 2,800 cases);
those checks are in the same repository.

I would be grateful for any comments, and happy to coordinate if you plan to extend your Lean formalisation to this
construction.

With best regards,
Harish K
