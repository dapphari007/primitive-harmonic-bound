"""One-off patch: add Section 6 (binary two-row representation graph) to build_report.py (idempotent)."""
import pathlib, re
p = pathlib.Path(__file__).with_name("build_report.py")
s = p.read_text(encoding="utf-8")
if "The binary two-row representation graph" in s:
    print("already patched"); raise SystemExit

def rep(old, new):
    global s
    assert old in s, f"anchor not found: {old[:70]!r}"
    s = s.replace(old, new, 1)

rep(r'''out = out.replace("__FIG4__", img("fig4_spherical.png"))''',
    r'''out = out.replace("__FIG4__", img("fig4_spherical.png")).replace("__FIG5__", img("fig5_two_row.png"))''')

# header chip + abstract
rep(r'''<span><span class="chip">reproducible</span> <span class="chip v">not a new theorem</span></span>''',
    r'''<span><span class="chip">reproducible</span> <span class="chip v">sections 1–5: audit</span> <span class="chip">section 6: new result (conditional)</span></span>''')
rep(r'''New numbers: the hierarchy lowers the kissing-number exponent from 0.4009 to 0.3966, and the moving-harmonic certificate beats the classical kissing certificate from dimension 96 on (consistently from 384).</p>
</div>''',
r'''New numbers: the hierarchy lowers the kissing-number exponent from 0.4009 to 0.3966, and the moving-harmonic certificate beats the classical kissing certificate from dimension 96 on (consistently from 384).</p>
<p><strong>Section 6 goes beyond the audit.</strong> We built the binary analogue of the paper's multi-row spherical hierarchy, which the paper mentions but does not pursue: a representation graph for the hyperoctahedral group whose vertices are bipartitions with two rows on each side. We computed its coordinate-transition coefficients exactly for \(n\le13\), found closed forms (each coefficient is a quadratic in the harmonic degree \(k\) whose roots are the Littlewood–Richardson admissibility boundaries), verified them on every computed case and checked the two identities the paper's general theorem needs on hundreds of thousands of cases, and derived the asymptotic exponent \(\kappa_{2row}(\delta)\). It is strictly below the paper's whole-cube exponent at every distance and, for \(\delta\ge\delta_1=0.2350\) where the paper's Theorem 1.1 reduces to that exponent, strictly below the paper's bound: at \(\delta=0.3\) it gives \(0.248150\) against \(0.248376\). At the middle level the two-row graph reproduces the classical second MRRW bound exactly. The closed forms are conjectural (a proof strategy is given); the finite-length theorem is rigorous for every \(n\) at which the coefficients are computed.</p>
</div>''')

# tiles
rep(r'''  <div class="tile"><div class="k">Largest exponent gain</div>''',
r'''  <div class="tile"><div class="k">Two-row binary exponent (new)</div><div class="v">0.24815 &lt; 0.24838</div><div class="d">at δ = 0.3: this note's κ_2row versus the paper's Theorem 1.1 (κ_bin = κ_H), with MRRW2 at 0.25023; conditional on closed forms verified exactly on ~3,300 cases</div></div>
  <div class="tile"><div class="k">Largest exponent gain</div>''')

# renumber sections 6,7,8 -> 7,8,9 and insert section 6
rep('<h2><span class="num">8</span>Sources</h2>', '<h2><span class="num">9</span>Sources</h2>')
rep('<h2><span class="num">7</span>What this establishes, and what it does not</h2>', '<h2><span class="num">8</span>What this establishes, and what it does not</h2>')
rep('<h2><span class="num">6</span>Method and reproducibility</h2>', '<h2><span class="num">7</span>Method and reproducibility</h2>')
rep(r'''<section>
<h2><span class="num">7</span>Method and reproducibility</h2>''',
r'''<section>
<h2><span class="num">6</span>The binary two-row representation graph: a new exponent</h2>
<p>The paper's spherical hierarchy replaces a one-dimensional path of harmonic degrees by a lattice of ambient representations with several Young-diagram rows, and its Proposition 4.1 and Theorem 4.2 are stated for a general group acting on a set with unit coordinate vectors. For the cube the group is the hyperoctahedral group \(B_n=\mathbb Z_2^n\rtimes S_n\), the stabilizer of a word is \(S_n\), the coordinate representation is \(W=\mathbb R^n\) with \(\ell_x=x/\sqrt n\), and the irreducible ambient representations are indexed by bipartitions \((\alpha,\beta)\) with \(|\alpha|+|\beta|=n\): the Fourier level \(V_j\) is \(((n-j),(j))\). Tensoring with \(W\) moves one box between \(\alpha\) and \(\beta\), so the classical path acquires "second-row" neighbours \(((n-j-1),(j,1))\) and \(((n-j,1),(j-1))\). The paper remarks that more general binary stabilizer types can require matrix-valued transitions and leaves this direction aside. For two-row shapes on both sides everything stays scalar: the stabilizer irrep \(E_\mu\), \(\mu=(n-k,k)\), occurs in \(V_{(\alpha,\beta)}|_{S_n}\) with multiplicity \(\le1\) (two-row Littlewood–Richardson rule: \(a_2+b_2\le k\le\min\{a_1+b_2,\,a_2+b_1\}\)), the box moves are multiplicity-free, and \(\mathrm{End}_{S_n}(E_\mu)=\mathbb R\). So Theorem 4.2 applies verbatim once the directed squared coordinate coefficients \(p(\lambda\to\lambda')\) are known.</p>

<h3>6.1 Computing the coefficients exactly</h3>
<p>We realized \(V_{(\alpha,\beta)}\) as \(\bigoplus_{|S|=|\beta|}\chi_S\otimes E_{b_2}(S)\otimes E_{a_2}(S^c)\) (Walsh character times the paper's own Boolean harmonic spaces on \(S\) and its complement), took a random vector, projected it onto the \(E_\mu\)-isotypic part with the \(S_n\) class sums of transpositions and 3-cycles, tensored with \(\ell_0\), and projected onto each constituent of \(W\otimes V_\lambda\) with the \(B_n\) class sums \(\sum_q\varepsilon_q\), \(\sum[(ij)+(ij)\varepsilon_i\varepsilon_j]\), \(\sum[(ij)\varepsilon_i+(ij)\varepsilon_j]\), whose eigenvalues on a bipartition are \(n-2|\beta'|\), \(2(c(\alpha')+c(\beta'))\), \(2(c(\alpha')-c(\beta'))\) (content sums), by exact Lagrange interpolation. On the classical path this reproduces the paper's \(\alpha_j^2=\frac{(j-k+1)(n-j-k)}{n(j+1)}\) and \(\beta_j^2=\frac{(j-k)(n-j-k+1)}{n(n-j+1)}\) to all digits, and shows that the missing mass \(1-\alpha_j^2-\beta_j^2\) goes to the two second-row targets as \(\frac{k(n-k+1)}{n(j+1)}\) and \(\frac{k(n-k+1)}{n(n-j+1)}\). All coefficients are rational; we computed 3,196 of them for \(n\le11\) and second rows up to 2, plus further cases at \(n=12,13\) with second rows up to 3.</p>

<h3>6.2 Closed forms</h3>
<p>Write the vertex as \(\alpha=(a_1,a_2)\), \(\beta=(b_1,b_2)\), \(a_1+a_2+b_1+b_2=n\), and \(N=n\,(a_1+1-a_2)(b_1+1-b_2)\). Every coefficient is a quadratic in \(k\) whose two roots sum to \(n+1\) and sit exactly at the admissibility boundaries of the target:</p>
<div class="eq">\[
\begin{aligned}
p(\alpha_1\!\to\!\beta_1)&=\tfrac{(a_1+1)(a_1+b_2-k)(a_2+b_1+1-k)}{N}, &
p(\beta_1\!\to\!\alpha_1)&=\tfrac{(b_1+1)(a_2+b_1-k)(a_1+b_2+1-k)}{N},\\
p(\alpha_1\!\to\!\beta_2)&=\tfrac{(a_1+1)(k-a_2-b_2)(a_1+b_1+1-k)}{N}, &
p(\beta_1\!\to\!\alpha_2)&=\tfrac{(b_1+1)(k-a_2-b_2)(a_1+b_1+1-k)}{N},\\
p(\alpha_2\!\to\!\beta_1)&=\tfrac{a_2\,(k-a_2-b_2+1)(a_1+b_1+2-k)}{N}, &
p(\beta_2\!\to\!\alpha_1)&=\tfrac{b_2\,(k-a_2-b_2+1)(a_1+b_1+2-k)}{N},\\
p(\alpha_2\!\to\!\beta_2)&=\tfrac{a_2\,(a_2+b_1-k)(a_1+b_2+1-k)}{N}, &
p(\beta_2\!\to\!\alpha_2)&=\tfrac{b_2\,(a_1+b_2-k)(a_2+b_1+1-k)}{N}.
\end{aligned}
\]</div>
<p>These were found by exact interpolation in \(k\) at each vertex, followed by fitting the roots as linear forms and the prefactors by hand. They agree with every computed coefficient to \(3\times10^{-7}\) (floating-point noise in the projection), and the two identities that Theorem 4.2 requires hold <em>exactly in rational arithmetic</em>: the coefficients out of every admissible vertex sum to one (136,854 vertex–degree pairs, \(n\le40\)) and the dimension-weighted reciprocity \(D_\lambda p(\lambda\to\lambda')=D_{\lambda'}p(\lambda'\to\lambda)\) holds on every edge (523,432 edges, \(n\le36\)), with \(D_\lambda=\binom n{|\beta|}f^\alpha f^\beta\). We regard the closed forms as a conjecture with a clear proof route: the coefficient is the eigenvalue on \(S^\mu\) of a distance-one operator in the Hecke algebra of \((S_n,S_j\times S_{n-j})\) and is therefore a polynomial of degree at most two in \(k\); its roots are forced by the Littlewood–Richardson vanishing of the target; the prefactors are then fixed by the two identities.</p>

<h3>6.3 The asymptotic exponent</h3>
<p>With \(u=j/n\), \(\tilde a=a_2/n\), \(\tilde b=b_2/n\), \(b=k/n\) and \(A_1=1-u-\tilde a\), \(A_2=\tilde a\), \(B_1=u-\tilde b\), \(B_2=\tilde b\), the limiting coefficients factor through two quadratics, \(X=(A_2+B_1-b)(A_1+B_2-b)\) and \(Y=(b-A_2-B_2)(1-A_2-B_2-b)\), with \(X+Y=N_\infty=(A_1-A_2)(B_1-B_2)\). The four edge directions of the lattice have symmetric limiting weights \(\sqrt{A_1B_1}\,X/N_\infty\), \(\sqrt{A_2B_2}\,X/N_\infty\), \(\sqrt{A_1B_2}\,Y/N_\infty\), \(\sqrt{A_2B_1}\,Y/N_\infty\), and the product-sine Rayleigh argument of the paper's Lemma 7.2 on a box of side \(o(n)\) gives the Perron limit</p>
<div class="eq">\[ \Lambda_\infty=\frac{2\big[X(\sqrt{A_1B_1}+\sqrt{A_2B_2})+Y(\sqrt{A_1B_2}+\sqrt{A_2B_1})\big]}{(A_1-A_2)(B_1-B_2)}, \]</div>
<p>which reduces to the paper's \(\Gamma_H(u,b)\) when \(\tilde a=\tilde b=0\). The ambient dimension exponent is \(H_2(u)+(1-u)H_2\big(\tfrac{\tilde a}{1-u}\big)+uH_2\big(\tfrac{\tilde b}{u}\big)\) and the stabilizer costs \(H_2(b)\), so</p>
<div class="eq">\[ \kappa_{2row}(\delta)=\inf\Big\{H_2(u)+(1-u)H_2\big(\tfrac{\tilde a}{1-u}\big)+uH_2\big(\tfrac{\tilde b}{u}\big)-H_2(b)\ :\ \Lambda_\infty(u,\tilde a,\tilde b,b)>1-2\delta\Big\}, \qquad R_2(\delta)\le\kappa_{2row}(\delta). \]</div>
<p>Two checks anchor this. At \(\tilde a=\tilde b=0\) the optimization reproduces \(\kappa_H\) to seven digits. And at the middle level \(u=\tfrac12\) with \(\tilde a=\tilde b\), the value \(\inf_a[1+H_2(2a)-H_2(b)]\) equals the optimized second MRRW bound \(M_2(\delta)\) to machine precision at \(\delta=0.05,0.10,0.15,0.20,0.25\): the classical constant-weight certificate is the middle slice of the two-row Fourier graph, a structural fact we did not anticipate.</p>
<div class="tbl"><table>
<tr><th>δ</th><th>M₂ (MRRW2)</th><th>κ_H (paper)</th><th>κ_2row (this note)</th><th>κ_H − κ_2row</th><th>u*</th><th>ã*</th><th>b̃*</th><th>b*</th></tr>
<tr><td>0.235</td><td>0.385649</td><td>0.382742</td><td>0.381719</td><td>1.0e-3</td><td>0.0961</td><td>6.3e-5</td><td>6.0e-4</td><td>0.0101</td></tr>
<tr><td>0.25</td><td>0.353711</td><td>0.350379</td><td>0.349630</td><td>7.5e-4</td><td>0.0814</td><td>3.5e-5</td><td>4.0e-4</td><td>0.0072</td></tr>
<tr><td>0.28</td><td>0.290634</td><td>0.288004</td><td>0.287627</td><td>3.8e-4</td><td>0.0584</td><td>1.0e-5</td><td>1.7e-4</td><td>0.0037</td></tr>
<tr><td>0.30</td><td>0.250225</td><td>0.248376</td><td>0.248150</td><td>2.3e-4</td><td>0.0463</td><td>4.2e-6</td><td>8.7e-5</td><td>0.0023</td></tr>
<tr><td>4/13</td><td>0.235178</td><td>0.233581</td><td>0.233398</td><td>1.8e-4</td><td>0.0423</td><td>3.0e-6</td><td>6.7e-5</td><td>0.0019</td></tr>
<tr><td>0.35</td><td>0.158133</td><td>0.157506</td><td>0.157458</td><td>4.8e-5</td><td>0.0243</td><td>3.4e-7</td><td>1.4e-5</td><td>0.0006</td></tr>
<tr><td>0.40</td><td>0.081469</td><td>0.081337</td><td>0.081331</td><td>5.3e-6</td><td>0.0103</td><td>1.1e-8</td><td>1.1e-6</td><td>0.0001</td></tr>
<tr><td>0.20</td><td>0.461360</td><td>0.460900</td><td>0.458907</td><td>2.0e-3</td><td>0.1443</td><td>2.4e-4</td><td>1.5e-3</td><td>0.0218</td></tr>
<tr><td>0.15</td><td>0.573450</td><td>0.577921</td><td>0.573334</td><td>4.6e-3</td><td>0.3190</td><td>1.9e-3</td><td>4.2e-3</td><td>0.0742</td></tr>
<tr><td>0.10</td><td>0.692741</td><td>0.699832</td><td>0.692741</td><td>7.1e-3</td><td>0.5000</td><td>1.8e-3</td><td>1.8e-3</td><td>0.0635</td></tr>
</table></div>
<p>The comparison that matters is with the paper's Theorem 1.1, \(R_2(\delta)\le\kappa_{\rm bin}(\delta)=\min\{\kappa_H,\kappa_{CW}\}\). Section 4 showed \(\kappa_{\rm bin}=\kappa_{CW}\) everywhere and \(\kappa_{CW}=\kappa_H\) for \(\delta\ge\delta_1=0.2350\). Hence for every \(\delta\in[0.235,\,0.5)\) the two-row graph gives a strictly smaller exponent than the paper's bound, by between \(10^{-3}\) bits per symbol at \(\delta_1\) and \(5\times10^{-6}\) at \(\delta=0.4\). Below \(\delta_1\) the two-row whole-cube graph ties the classical \(M_2\) at the middle level and does not reach \(\kappa_{CW}\); the natural next construction is the two-row graph over a constant-weight layer, or a three-row whole-cube graph, which we have not built.</p>
<figure><img alt="Left: gain over MRRW2 of the paper's one-row exponent and of the two-row exponent versus delta. Right: the improvement kappa_H minus kappa_2row on a log scale, and the improvement over the paper's kappa_bin where positive, with delta_1 marked." src="__FIG5__"><figcaption><strong>Figure 5.</strong> Left: gain over the second MRRW bound of the paper's whole-cube exponent (orange) and of the two-row exponent (red). Right: the improvement of the two-row graph over \(\kappa_H\), and over the paper's \(\kappa_{\rm bin}\) where it is positive (\(\delta\ge\delta_1\)).</figcaption></figure>

<h3>6.4 Finite lengths</h3>
<p>The improvement is an asymptotic statement with tiny optimal second rows (\(\tilde b^*\approx10^{-4}\) at \(\delta=0.3\)), so at practical lengths the box carries second rows of size 0 or 1 and its extra ambient dimension costs more than the spectral gain. With the closed forms we evaluated the finite-\(n\) two-row bound over boxes in \((j,a_2,b_2)\) at \(\delta=0.3\): it is worse than the paper's one-row bound (23) by 0.02 bits at \(n=100\) and by 2.4 bits at \(n=5000\), and the crossover is beyond that scan (the results folder records a lean scan to \(10^5\)). This is the same pattern as the paper's own constructions in Sections 3 and 4.</p>

<h3>6.5 What is proven and what is conjectured</h3>
<ul>
<li><strong>Rigorous:</strong> for each finite \(n\) and each box \(\Omega\), the bound \(A_2(n,d)\le\frac{1-s}{d_\mu(\Lambda_\Omega-s)}\sum_{\lambda\in\Omega}D_\lambda\) follows from the paper's Theorem 4.2 with \(G=B_n\) once the coefficients are computed; we computed them exactly for \(n\le13\).</li>
<li><strong>Conjectural, heavily verified:</strong> the closed forms of Section 6.2 (every computed case, both identities exact on hundreds of thousands of cases, the correct classical specializations). The asymptotic exponent \(\kappa_{2row}\), the strict improvement over \(\kappa_H\), and the improvement over the paper's Theorem 1.1 for \(\delta\ge0.235\) are conditional on them.</li>
<li><strong>Independent evidence for the asymptotics:</strong> the exact recovery of \(M_2(\delta)\) at the middle level, a classical theorem obtained here from a different construction.</li>
</ul>
<div class="callout ok"><div class="t">Eureka, with its condition stated</div>Conditional on closed forms that hold in every one of roughly 3,300 exactly computed cases and satisfy the theorem's identities exactly, the binary two-row representation graph improves the best known upper bound on the rate of binary codes, \(R_2(\delta)\), for every \(\delta\in[0.235,0.5)\), beyond the bound proved in the paper. The mechanism is the paper's own (Proposition 7.3): a square-root spectral gain from opening a second row against a \(x\log(1/x)\) entropy cost. What remains is a proof of the eight formulas.</div>
</section>

<section>
<h2><span class="num">7</span>Method and reproducibility</h2>''')

rep(r'''experiments/sph_checks.py / sph_test1_vs_lp.py / sph_gamma_levels.py / sph_kissing.py / sph_crossover.py / make_figure4.py</code></pre>''',
r'''experiments/sph_checks.py / sph_test1_vs_lp.py / sph_gamma_levels.py / sph_kissing.py / sph_crossover.py / make_figure4.py
phb/hyperoct.py         B_n signed permutation modules, class-sum Lagrange projections, exact transition coefficients
phb/hyperoct_formulas.py  the eight closed forms, targets, admissibility, dimensions
phb/hyperoct_asymptotics.py  limiting weights, Lambda_infinity, kappa_H and kappa_2row optimisation
experiments/hyperoct_collect.py / hyperoct_roots.py / hyperoct_formulas.py / hyperoct_verify_big.py / hyperoct_exponent.py / hyperoct_finite.py / make_figure5.py</code></pre>''')
rep(r'''<li><strong>Not covered:</strong> the Lean formalization itself, and everything outside Chapter 2 of the paper.</li>''',
r'''<li><strong>Section 6 is different in kind.</strong> It is our construction, not the paper's, and it rests on conjectured closed forms. Everything downstream of them is stated as conditional, and the finite-length theorem is the only unconditional part.</li>
<li><strong>Not covered:</strong> the Lean formalization itself, everything outside Chapter 2 of the paper, and a proof of the closed forms of Section 6.2.</li>''')

p.write_text(s, encoding="utf-8")
print("patched build_report.py (section 6)")
