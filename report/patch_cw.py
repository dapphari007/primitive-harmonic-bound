"""One-off patch: add the plain-language and constant-weight sections to build_report.py (idempotent)."""
import pathlib
p = pathlib.Path(__file__).with_name("build_report.py")
s = p.read_text(encoding="utf-8")
if "IN PLAIN WORDS" in s:
    print("already patched"); raise SystemExit

def rep(old, new):
    global s
    assert old in s, f"anchor not found: {old[:70]!r}"
    s = s.replace(old, new, 1)

rep(r'''out = HTML.replace("__FIG1__", img("fig1_exponents.png")).replace("__FIG2__", img("fig2_finite_n.png"))''',
    r'''out = HTML.replace("__FIG1__", img("fig1_exponents.png")).replace("__FIG2__", img("fig2_finite_n.png")).replace("__FIG3__", img("fig3_cw_exponent.png"))
out = out.replace("__CWCROSS__", (ROOT / "report" / "cw_crossover_paragraph.html").read_text(encoding="utf-8") if (ROOT / "report" / "cw_crossover_paragraph.html").exists() else "")''')

rep(r'''and replacing the paper's trace Cauchy–Schwarz step by the exact constant Krawtchouk coefficient of the kernel tightens the finite-length bound by 2–7% at short lengths without changing the exponent.</p>
</div>''',
r'''and replacing the paper's trace Cauchy–Schwarz step by the exact constant Krawtchouk coefficient of the kernel tightens the finite-length bound by 2–7% at short lengths without changing the exponent.</p>
<p>The same audit was then applied to the paper's constant-weight (Johnson-layer) construction, which supplies the improvement below \(\delta_0\). Its associated Hahn recurrence coefficients, measured from an explicit construction of the tensor-product harmonic spaces, agree with the paper's formulas to \(10^{-16}\); its finite bound never falls below the exact Johnson-scheme LP in 1,090 cases; and its exponent \(\kappa_{CW}\) is below \(M_2\) at every distance, though by margins as small as \(10^{-6}\) bits per symbol at \(\delta=0.02\). Unexpectedly, \(\kappa_{CW}\le\kappa_H\) everywhere: the constant-weight family contains the whole-cube bound as its middle-layer boundary and is strictly better below \(\delta_1=0.2350\).</p>
</div>''')

rep(r'''<section>
<h2><span class="num">AT A GLANCE</span>What the numbers say</h2>''',
r'''<section>
<h2><span class="num">IN PLAIN WORDS</span>What this is about, with small examples</h2>
<p><strong>The problem.</strong> A binary code is a list of words of \(n\) bits in which any two words differ in at least \(d\) positions, so that a few flipped bits can never turn one word into another. With 8-bit words and \(d=2\) you can keep 128 words (all words with an even number of ones); with \(d=4\) only 16 survive. For long words with \(d\) a fixed fraction \(\delta\) of \(n\), the count grows like \(2^{Rn}\), and nobody knows the largest possible growth rate \(R\). Gilbert and Varshamov showed how large it can at least be; McEliece, Rodemich, Rumsey and Welch (MRRW) showed in 1977 how large it can at most be. That ceiling had not moved in 49 years.</p>
<p><strong>How ceilings are proved.</strong> Attach a "spotlight" (a vector in a big space) to every word. The overlap of two spotlights depends only on how far apart the words are. Choose the spotlights so that overlaps between distinct codewords are always non-positive, while the total overlap of all spotlights together can never be negative. Then the only way the sum can be non-negative is if there are few words: that is the ceiling. The classical proof uses one spotlight per word. The new idea is to give every word a whole <em>bundle</em> of spotlights, exponentially many, all moving rigidly with the word. A bundle has a large "size" (its dimension) but, in the precise sense the proof needs, bundles overlap no more than single spotlights do, so the ceiling drops.</p>
<p><strong>What we did.</strong> Three things a careful referee would do with a calculator. First, we re-computed the paper's own worked example and got its numbers to every printed digit. Second, we used a known "best possible spotlight ceiling" (the Delsarte linear program, which can be computed exactly for short words) as a lie detector: no spotlight argument can beat it, so if the new formula ever did, the formula would be wrong. In 2,749 length-and-distance cases it never did. Third, we rebuilt the bundles ourselves from scratch, with no help from the paper's proof, and measured directly whether the overlap sums are positive. They are, and the weighting the paper uses is exactly the best possible one.</p>
<p><strong>What we added.</strong> Numbers the paper does not state. For example, at distance 4/13 the new ceiling only beats the old one for words longer than about 1,100 bits; at distance 1/10 it already wins at 30 bits. The whole-cube version beats the strongest classical ceiling only for \(\delta\) above 0.195; below that, the paper's constant-weight version is needed, and there the improvement is real but tiny (a millionth of a bit per symbol at \(\delta=0.02\)).</p>
<p><strong>On the word "Eureka".</strong> We reserve it for a genuinely new mathematical fact: a theorem, or a number in a published table that we can move. Nothing in this note qualifies; it is verification and quantification of someone else's theorem, done carefully. We say so plainly rather than dress it up.</p>
</section>

<section>
<h2><span class="num">AT A GLANCE</span>What the numbers say</h2>''')

rep(r'''<div class="tile"><div class="k">LP soundness test</div><div class="v">__TOTAL_VIOL__ / __TOTAL_PAIRS__</div><div class="d">violations of bound ≥ Delsarte LP optimum, every d for 4 ≤ n ≤ 56 and n = 60, 64, every feasible (k, L)</div></div>''',
r'''<div class="tile"><div class="k">LP soundness tests</div><div class="v">0 / 2,749</div><div class="d">violations of bound ≥ exact Delsarte LP: __TOTAL_PAIRS__ Hamming cases (every d, 4 ≤ n ≤ 56 and n = 60, 64) plus 1,090 Johnson-layer cases (n ≤ 30)</div></div>''')
rep(r'''<div class="tile"><div class="k">Largest exponent gain</div>''',
r'''<div class="tile"><div class="k">Hahn coefficients, rebuilt</div><div class="v">10⁻¹⁶</div><div class="d">agreement between the paper's associated Hahn formulas (36)–(37) and coefficients measured from an explicit construction, 11 (p, q) pairs</div></div>
  <div class="tile"><div class="k">Layers vs whole cube</div><div class="v">δ₁ = 0.2350</div><div class="d">below δ₁ the constant-weight exponent κ_CW is strictly below κ_H; above it the optimal layer is the middle one and the two coincide</div></div>
  <div class="tile"><div class="k">Largest exponent gain</div>''')

rep('<h2><span class="num">4</span>Method and reproducibility</h2>', '<h2><span class="num">5</span>Method and reproducibility</h2>')
rep('<h2><span class="num">5</span>What this establishes, and what it does not</h2>', '<h2><span class="num">6</span>What this establishes, and what it does not</h2>')
rep('<h2><span class="num">6</span>Sources</h2>', '<h2><span class="num">7</span>Sources</h2>')

rep(r'''<section>
<h2><span class="num">5</span>Method and reproducibility</h2>''',
r'''<section>
<h2><span class="num">4</span>The constant-weight construction</h2>
<p>Below \(\delta_0\) the whole-cube certificate loses to \(M_2\), and the paper's Section 3 supplies a second construction. Restrict the code to words of weight \(w=\alpha n\) (Bassalygo–Elias costs \(1-H_2(\alpha)\) in the exponent), and to a word \(x\) attach the tensor product \(E_p(x)\otimes E_q(x^c)\) of Boolean harmonic spaces of degrees \(p\) and \(q\) on its support and complement. Each Johnson degree \(j\) with \(p+q\le j\le j_+=\min\{w,\,w-p+q,\,N+p-q\}\) contains exactly one copy (Lemma 3.1), and multiplication by the distance coordinate acts on these copies through an <em>associated Hahn recurrence</em> with explicit coefficients \(b^{p,q}_j,c^{p,q}_j\) (eqs. (35)–(37)). The symmetric Johnson matrix \(\widehat J\) has diagonal \((b^{p,q}_j)^2/b^0_j\) and off-diagonal \((c^{p,q}_j)^2/c^0_j\), and Theorem 3.4 gives, for even \(d\) and \(s=1-nd/(2wN)\),</p>
<div class="eq">\[ A_J(n,w,d)\;\le\;\frac{1-s}{\lambda-s}\cdot\frac{\sum_{j=p+q}^{L}\big(\binom nj-\binom n{j-1}\big)}{\big(\binom wp-\binom w{p-1}\big)\big(\binom Nq-\binom N{q-1}\big)},\qquad \lambda=\lambda_{\max}(\widehat J)>s. \tag{46} \]</div>
<p>Asymptotically the threshold is the explicit function \(\Lambda_{\alpha,\beta,\gamma}(u)\) of eq. (6) and the exponent is \(\kappa_{CW}(\delta)\), an infimum over four parameters \((\alpha,\beta,\gamma,u)\) (eq. (8)); \(\beta=\gamma=0\) recovers the classical objective \(F_\delta\) exactly (eq. (50)).</p>

<h3>4.1 Transcription checks</h3>
<ul>
<li>For \(p=q=0\) and the full Johnson path \(L=w\), the spectrum of \(\widehat J\) must be the set of distance coordinates \(\{1-nr/(wN): r=0..w\}\). It is, to \(9\times10^{-16}\), for \((n,w)\) up to \((41,20)\).</li>
<li>Identity (50), \(1-\Lambda_{\alpha,0,0}(u)=(A-U)/(A(1+2\sqrt U))\), holds to \(8\times10^{-16}\) on a 400-point grid.</li>
<li>Minimizing the \(\beta=\gamma=0\) rate over \(\alpha\) reproduces \(M_2(\delta)\) to \(3\times10^{-16}\) at four distances.</li>
</ul>

<h3>4.2 Soundness against the exact Johnson-scheme LP</h3>
<p>The Delsarte LP for constant-weight codes uses the Eberlein eigenvalues \(E_r(j)=\sum_i(-1)^i\binom ji\binom{w-j}{r-i}\binom{N-j}{r-i}\); we solve it exactly (rational simplex) and checked it against seven known values, including the Golay-derived \(A(24,8,12)=2576\) and \(A(24,8,8)=759\). Across all \(6\le n\le30\), \(2\le w<n/2\), even \(d\), and every admissible \((p,q,L)\): <strong>1,090 triples, zero violations</strong> of (46) ≥ LP.</p>

<h3>4.3 The certificate rebuilt from first principles</h3>
<p>For \((n,w)=(10,4)\) and \((12,5)\) we built functions on the \(w\)-subsets, the Johnson eigenspaces, the harmonic spaces \(E_p(x)\), \(E_q(x^c)\), and an equivariant map from their tensor product into each Johnson degree (Schur's lemma makes any nonzero equivariant image the unique copy; we verified it is a scalar multiple of an isometry). We then <em>measured</em> the diagonal and neighboring-degree coefficients of multiplication by the distance coordinate and compared with (36)–(37).</p>
<div class="tbl"><table>
<tr><th>(n, w)</th><th>(p, q)</th><th>degrees</th><th>max |b_meas − b(37)|</th><th>max |c_meas − c(37)|</th><th>L</th><th>λ_max(Ĵ)</th><th>λ* (positivity)</th></tr>
<tr><td>(10, 4)</td><td>(0, 0)</td><td>0..4</td><td>6.9e-16</td><td>2.8e-16</td><td>2</td><td>0.583333</td><td class="win">0.583333</td></tr>
<tr><td>(10, 4)</td><td>(1, 0)</td><td>1..3</td><td>3.1e-16</td><td>2.2e-16</td><td>3</td><td>0.659751</td><td class="win">0.659751</td></tr>
<tr><td>(10, 4)</td><td>(0, 1)</td><td>1..4</td><td>3.5e-16</td><td>2.2e-16</td><td>4</td><td>0.550037</td><td class="win">0.550037</td></tr>
<tr><td>(10, 4)</td><td>(1, 1)</td><td>2..4</td><td>2.2e-16</td><td>1.9e-16</td><td>4</td><td>0.356657</td><td class="win">0.356657</td></tr>
<tr><td>(10, 4)</td><td>(1, 2)</td><td>3..4</td><td>6.9e-17</td><td>8.3e-17</td><td>4</td><td>0.101860</td><td class="win">0.101860</td></tr>
<tr><td>(12, 5)</td><td>(1, 1)</td><td>2..5</td><td>5.0e-16</td><td>2.2e-16</td><td>5</td><td>0.442547</td><td class="win">0.442547</td></tr>
<tr><td>(12, 5)</td><td>(2, 1)</td><td>3..4</td><td>8.3e-17</td><td>2.8e-17</td><td>4</td><td>0.252435</td><td class="win">0.252435</td></tr>
<tr><td>(12, 5)</td><td>(2, 2)</td><td>4..5</td><td>8.3e-17</td><td>5.6e-17</td><td>5</td><td>0.116547</td><td class="win">0.116547</td></tr>
</table></div>
<p>Every measured coefficient matches the paper's formula to machine precision, in all eleven \((p,q)\) pairs tested, and in all 21 retained-degree choices the best positive-definite \(\lambda^*\) (computed through the Eberlein transform of the reconstructed kernel) equals \(\lambda_{\max}(\widehat J)\) to six decimals. As in the whole-cube case, the Delsarte polynomial \((t-s)K\) tightens (46) by a few percent at these lengths (e.g. 218.8 → 163.4 for \(n=12,w=5,d=4\) at \(p=q=0,L=2\)).</p>

<h3>4.4 The constant-weight exponent</h3>
<p>We minimized (8) numerically: for fixed \((\alpha,\beta,\gamma)\) the smallest admissible \(u\) with \(\Lambda>1-\delta/(2\alpha(1-\alpha))\) is found by bisection, and the remaining three parameters by multi-start Nelder–Mead (25 starts, including the classical minimizer).</p>
<div class="tbl"><table>
<tr><th>δ</th><th>M₂</th><th>κ_H</th><th>κ_CW</th><th>M₂ − κ_CW</th><th>relative</th><th>α*</th><th>β*</th><th>γ*</th><th>u*</th></tr>
<tr><td>0.02</td><td>0.917985</td><td>0.918531</td><td>0.917983</td><td>1.3e-6</td><td>0.0001%</td><td>0.0104</td><td>1.0e-6</td><td>~0</td><td>0.0001</td></tr>
<tr><td>0.05</td><td>0.825137</td><td>0.827872</td><td>0.825115</td><td>2.2e-5</td><td>0.003%</td><td>0.028</td><td>1.7e-5</td><td>5e-7</td><td>0.0008</td></tr>
<tr><td>0.10</td><td>0.692741</td><td>0.699832</td><td>0.692557</td><td>1.8e-4</td><td>0.026%</td><td>0.0649</td><td>1.7e-4</td><td>1.2e-5</td><td>0.0044</td></tr>
<tr><td>0.14</td><td>0.596611</td><td>0.601957</td><td>0.596084</td><td>5.3e-4</td><td>0.088%</td><td>0.1064</td><td>5.4e-4</td><td>6.4e-5</td><td>0.0116</td></tr>
<tr><td>0.18</td><td>0.505544</td><td>0.507027</td><td>0.504356</td><td>1.2e-3</td><td>0.235%</td><td>0.1710</td><td>1.3e-3</td><td>2.7e-4</td><td>0.0270</td></tr>
<tr><td>0.195</td><td>0.472335</td><td>0.472339</td><td>0.470788</td><td>1.5e-3</td><td>0.328%</td><td>0.2073</td><td>1.8e-3</td><td>4.6e-4</td><td>0.0368</td></tr>
<tr><td>0.22</td><td>0.417875</td><td>0.415810</td><td>0.415554</td><td>2.3e-3</td><td>0.555%</td><td>0.3049</td><td>2.6e-3</td><td>1.1e-3</td><td>0.0622</td></tr>
<tr><td>0.25</td><td>0.353711</td><td>0.350379</td><td>0.350379</td><td>3.3e-3</td><td>0.942%</td><td>0.5000</td><td>2.0e-3</td><td>2.0e-3</td><td>0.0758</td></tr>
<tr><td>0.30</td><td>0.250225</td><td>0.248376</td><td>0.248376</td><td>1.8e-3</td><td>0.739%</td><td>0.5000</td><td>7.9e-4</td><td>7.9e-4</td><td>0.0451</td></tr>
<tr><td>0.40</td><td>0.081469</td><td>0.081337</td><td>0.081337</td><td>1.3e-4</td><td>0.162%</td><td>0.5000</td><td>4.9e-5</td><td>4.9e-5</td><td>0.0103</td></tr>
</table></div>
<p>Three conclusions. First, \(\kappa_{CW}<M_2\) at every distance, as Theorem 3.8 asserts, but the margin below \(\delta\approx0.1\) is minute: about \(10^{-6}\) bits per symbol at \(\delta=0.02\) and \(1.8\times10^{-4}\) at \(\delta=0.1\). The optimal harmonic degrees are correspondingly tiny (\(\beta^*\approx10^{-6}\) to \(10^{-3}\)), which is the \(2\varepsilon\log_2(1/\varepsilon)\) mechanism of Proposition 3.7 operating at its natural scale. Second, and not stated in the paper, \(\kappa_{CW}\le\kappa_H\) for all \(\delta\): the constant-weight family contains the whole-cube bound as its \(\alpha\to1/2\), \(\beta=\gamma\) boundary, so \(\kappa_{\rm bin}=\kappa_{CW}\) and the minimum in Theorem 3.8 is never attained by the whole-cube term alone. The optimal layer weight \(\alpha^*\) increases continuously with \(\delta\) and reaches the middle layer at \(\delta_1=0.2350\) (by bisection; \(\alpha^*=0.472\) at \(\delta=0.235\), \(0.500\) at \(0.240\)); above \(\delta_1\) the two exponents coincide. Third, the total gain over \(M_2\) peaks at \(3.3\times10^{-3}\) bits per symbol near \(\delta=0.255\), about one percent of the bound, and decays on both sides.</p>
<figure><img alt="Left: gain of the constant-weight exponent over MRRW2 versus delta on a logarithmic scale, with delta_0 and delta_1 marked. Right: the gap kappa_H minus kappa_CW, positive below delta_1 and zero above." src="__FIG3__"><figcaption><strong>Figure 3.</strong> Left: the improvement \(M_2-\kappa_{CW}\) on a logarithmic scale; it spans six orders of magnitude across the distance range. Right: \(\kappa_H-\kappa_{CW}\), the advantage of choosing a non-middle layer, which vanishes at \(\delta_1=0.2350\).</figcaption></figure>
__CWCROSS__
</section>

<section>
<h2><span class="num">5</span>Method and reproducibility</h2>''')

rep(r'''experiments/make_figures.py      Figures 1-2                results/*.txt   raw outputs of every run</code></pre>''',
r'''experiments/make_figures.py      Figures 1-2                results/*.txt   raw outputs of every run
phb/johnson.py          constant-weight bound (46): associated Hahn coefficients (35)-(37), Jhat (43)-(44), Lambda (6), kappa_CW (8)
phb/johnson_lp.py       exact Delsarte LP for the Johnson scheme (Eberlein eigenvalues)
phb/johnson_certificate.py  explicit Johnson eigenspaces, E_p (x) E_q, equivariant embeddings, measured b_j, c_j, kernel, lambda*
experiments/cw_test1_vs_lp.py / cw_test2_certificate.py / cw_asymptotics.py / cw_crossover.py / make_figure3.py</code></pre>''')

rep(r'''<li><strong>Not covered:</strong> the constant-weight (Johnson-layer) construction that supplies the improvement for \(\delta<\delta_0\), the spherical hierarchy, and the sphere-packing consequence. Their finite-length spectral thresholds are given in the paper (equation (6)) and could be audited the same way.</li>''',
r'''<li><strong>The constant-weight audit is the strongest evidence here.</strong> Its recurrence coefficients are not eigenvalues of a matrix we copied; they were measured from an explicit representation-theoretic construction and agree with the paper's closed forms to \(10^{-16}\), and the resulting kernels pass the positivity test independently.</li>
<li><strong>New from this note:</strong> \(\delta_0=0.19504\), \(\delta_1=0.2350\), the observation \(\kappa_{CW}\le\kappa_H\) (so \(\kappa_{\rm bin}=\kappa_{CW}\)), the size of the gains at every distance, the finite-length crossover lengths, and the Krawtchouk sharpening of (23) and (46).</li>
<li><strong>Not covered:</strong> the spherical-code hierarchy and its sphere-packing consequence (Sections 4–8 of the paper). The same harness applies to its representation graphs.</li>''')

p.write_text(s, encoding="utf-8")
print("patched build_report.py")
