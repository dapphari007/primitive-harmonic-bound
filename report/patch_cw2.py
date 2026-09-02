"""One-off patch: add Section 7 (three-row constant-weight graph) to build_report.py (idempotent)."""
import pathlib
p = pathlib.Path(__file__).with_name("build_report.py")
s = p.read_text(encoding="utf-8")
if "Proposition 7.1" in s:
    print("already patched"); raise SystemExit

def rep(old, new):
    global s
    assert old in s, f"anchor not found: {old[:90]!r}"
    s = s.replace(old, new, 1)

# ---- header chip
rep(r'''<span class="chip">section 6: new theorem</span></span>''',
    r'''<span class="chip">section 6: new theorem</span> <span class="chip">section 7: new closed form</span></span>''')

# ---- abstract: add a paragraph after the Section 6 paragraph
rep(r'''resting only on the paper's general projection bound, Schur–Weyl duality, and Edmonds' table of 6j-symbols.</p>''',
    r'''resting only on the paper's general projection bound, Schur–Weyl duality, and Edmonds' table of 6j-symbols.</p>
<p><strong>Section 7 opens a third row inside a constant-weight layer.</strong> The paper's layer construction (Section 3) lives on two-row ambient shapes; we let the ambient shapes have three rows, which is the largest multiplicity-free extension of that construction. We computed the coordinate-transition coefficients exactly for \(n\le12\), reduced them by Schur–Weyl duality to \(GL_3\) recoupling coefficients, and found and verified a closed form: each coefficient is the square of a two-term sum of square roots of ratios of products of partial-hook differences, the structure of the classical \(U(3)\) fundamental Wigner coefficients. The resulting exponent \(\kappa_{CW2}\) improves the paper's constant-weight exponent \(\kappa_{CW}\) for small distances (__CW2_DRANGE__) by at most __CW2_MAXGAIN__ bits, and loses to it beyond, where the paper's second Young-subgroup parameter matters and cannot be combined with a third row. This is a new formula and a small new number, not a breakthrough; we say so.</p>''')

# ---- tile
rep(r'''<div class="tile"><div class="k">Largest exponent gain</div>''',
    r'''<div class="tile"><div class="k">Three-row layer graph (new)</div><div class="v">__CW2_TILE__</div><div class="d">closed form for all coefficients (partial-hook products, verified on every computed case); exponent κ_CW2 below the paper's κ_CW for δ ≲ __CW2_DCROSS__, above it beyond</div></div>
  <div class="tile"><div class="k">Largest exponent gain</div>''')

# ---- renumber sections 7,8,9 -> 8,9,10
rep('<h2><span class="num">9</span>Sources</h2>', '<h2><span class="num">10</span>Sources</h2>')
rep('<h2><span class="num">8</span>What this establishes, and what it does not</h2>', '<h2><span class="num">9</span>What this establishes, and what it does not</h2>')
rep('<h2><span class="num">7</span>Method and reproducibility</h2>', '<h2><span class="num">8</span>Method and reproducibility</h2>')

# ---- Section 7
SECTION7 = r'''<section>
<h2><span class="num">7</span>The three-row constant-weight graph: a closed form and a small gain</h2>
<p>Section 6 improved the paper's bound for \(\delta\ge\delta_1=0.2350\), where the paper's best exponent is its whole-cube exponent. Below \(\delta_1\) the paper's best is the constant-weight exponent \(\kappa_{CW}\) of its Section 3, built on a layer \(\{x:|x|=w\}\) with the Young subgroup \(H=S_w\times S_{n-w}\), a stabilizer irrep \(E=S^{(w-p,p)}\boxtimes S^{(N-q,q)}\) (\(N=n-w\)), and ambient \(S_n\)-irreps \(S^{(n-j,j)}\) with two rows. We asked the natural question: what happens when the ambient shapes are allowed three rows?</p>

<h3>7.1 The construction and why three rows is the limit</h3>
<p>Take \(E=S^{(w-p,p)}\boxtimes\mathbf 1_{S_N}\). By Pieri's rule \(\mathrm{Hom}_H(E,S^\lambda)\) is at most one-dimensional and is nonzero exactly when \(\lambda/(w-p,p)\) is a horizontal strip, i.e. when \(\lambda=(\lambda_1,\lambda_2,\lambda_3)\) has at most three rows and interlaces \(\varepsilon=(w-p,p)\): \(\lambda_3\le p\le\lambda_2\le w-p\le\lambda_1\). So the paper's Theorem 4.2 applies with vertex set the interlacing three-row shapes, and the coordinate operator (the centred indicator of a coordinate, restricted to the layer) moves one box from a row \(r\) to a row \(r'\) or leaves \(\lambda\) fixed. At \(\lambda_3=0\) and \(q=0\) this is exactly the paper's construction; we verified that our coefficients reproduce its associated Hahn coefficients (35)–(37) there. Three rows is as far as this goes: with a second two-row factor \(S^{(N-q,q)}\), \(q>0\), the Littlewood–Richardson multiplicity of a three-row \(\lambda\) can be two (\(c^{(3,2,1)}_{(2,1),(2,1)}=2\)), so the paper's multiplicity-one hypothesis fails and the two extensions, a third ambient row and a nontrivial \(S_N\)-part, cannot be combined.</p>

<h3>7.2 Exact coefficients and their reduction to \(GL_3\)</h3>
<p>We computed the directed squared coefficients \(p(\lambda\to\lambda')\) exactly for \(n\le12\) by building the permutation modules of three-row shapes on the layer, projecting onto Specht modules through the kernels of the raising maps, and evaluating the coordinate operator on an explicit \(E\)-copy (812 coefficients at 179 vertices; every out-degree sums to one to \(10^{-9}\)). Unlike Section 6, blind interpolation failed: these numbers are not products of linear forms. The reason is structural. Frobenius reciprocity and the orthogonality of the centred indicator to the all-ones vector reduce a move \(\lambda\to\lambda'=\lambda-\square_r+\square_{r'}\), with \(\nu=\lambda-\square_r\), to</p>
<div class="eq">\[p(\lambda\to\lambda')=\frac wN\,\frac{f^{\lambda'}}{f^{\nu}}\,\tau^2,\qquad \tau=\sum_{t=1,2}\frac{f^{\varepsilon-\square_t}}{f^{\varepsilon}}\,R_t(\lambda,\nu)\,R_t(\lambda',\nu),\]</div>
<p>where \(R_t(\lambda,\nu)\) is the cosine of the angle between two coupling schemes of \(V_\lambda\) inside \(V_{\varepsilon-\square_t}\otimes\mathbb C^3\otimes\mathrm{Sym}^N\mathbb C^3\): one through \(V_\varepsilon\otimes\mathrm{Sym}^N\), the other through \(V_\nu\otimes\mathbb C^3\). Schur–Weyl duality turns three-row Specht modules into \(GL_3\)-modules, and the multiplicity spaces into intertwiner spaces. We implemented the \(GL_3\) modules in the Gelfand–Tsetlin basis (checked: commutation relations, adjointness, Weyl dimensions, all exact), propagated the intertwiners from highest-weight vectors, and recovered all 366 off-diagonal exact coefficients to \(2\times10^{-14}\). A coefficient is thus the square of a sum of two recoupling terms, which is why it is not a rational function of the labels.</p>

<h3>7.3 Closed form: Proposition 7.1</h3>
<p>Each squared recoupling cosine is rational, and on generic interior points it is a product of linear forms. Write partial hooks \(Q=(\lambda_1+2,\lambda_2+1,\lambda_3)\) for the three-row label and \(P=(w-p+2,\,p+1,\,0)\) for \(\varepsilon\) regarded as a three-row shape with an empty third row. Then, for \(\nu=\lambda-\square_r\) and \(t\in\{1,2\}\),</p>
<div class="eq">\[R_t(\lambda,\nu)^2=\frac{\prod_{k\ne r}|P_t-Q_k-1|\;\prod_{k\ne t}|Q_r-P_k|}{\prod_{k\ne t}|P_t-P_k-1|\;\prod_{k\ne r}|Q_r-Q_k|}\qquad(k\in\{1,2,3\}),\]</div>
<p>and the two terms of \(\tau\) combine with the relative sign \((-1)^{r+r'}\) (opposite signs for moves between adjacent rows, equal signs for moves between rows 1 and 3), with \(f^{\varepsilon-\square_1}/f^{\varepsilon}=\frac{(a-b)(a+1)}{(a+b)(a-b+1)}\) and \(f^{\varepsilon-\square_2}/f^{\varepsilon}=\frac{(a-b+2)\,b}{(a+b)(a-b+1)}\) for \(\varepsilon=(a,b)\), and \(f^{\nu+\square_{r'}}/f^{\nu}=\frac n{Q_{r'}}\prod_{k\ne r'}\frac{Q_{r'}-Q_k}{Q_{r'}-Q_k-1}\) with \(Q\) the partial hooks of \(\lambda'\).</p>
<p><strong>Proposition 7.1</strong> (closed form, verified). <em>With these ingredients, \(p(\lambda\to\lambda')=\frac wN\frac{f^{\lambda'}}{f^\nu}\Big[\frac{f^{\varepsilon-\square_1}}{f^\varepsilon}R_1(\lambda,\nu)R_1(\lambda',\nu)+(-1)^{r+r'}\frac{f^{\varepsilon-\square_2}}{f^\varepsilon}R_2(\lambda,\nu)R_2(\lambda',\nu)\Big]^2\) with \(R_t\ge0\) the square roots above, and \(p(\lambda\to\lambda)=1-\sum_{\lambda'\ne\lambda}p(\lambda\to\lambda')\).</em></p>
<p>Status. The reduction to \(\tau\) is derived (the same standard facts as in Section 6, with \(GL_3\) in place of \(SU(2)\)), and the formula for \(R_t^2\) was found by fitting on 1,458 generic points computed in the \(GL_3\) modules and is exact on all of them (to \(6\times10^{-15}\)). It has the form of the Biedenharn–Louck pattern-calculus expression for the reduced Wigner coefficients of the fundamental representation of \(U(3)\), which is what a seesaw duality between \(V_\varepsilon\otimes\mathrm{Sym}^N\) and the branching \(U(3)\downarrow U(2)\) predicts; we have not reproduced that derivation line by line, so we state a verified proposition rather than a theorem. The evidence leaves no realistic room for error: all 366 off-diagonal exact coefficients for \(n\le12\) (\(2\times10^{-14}\)), 25 random cases up to \(n=29\) against the independent \(GL_3\) computation (\(6\times10^{-16}\)), the self-loop sum rule at all 179 vertices (\(6\times10^{-14}\)), and the dimension-weighted reciprocity \(f^\lambda p(\lambda\to\lambda')=f^{\lambda'}p(\lambda'\to\lambda)\), which holds <em>exactly in rational arithmetic</em>, separately for the rational and the radical part of the square, on 364 of 364 random cases.</p>

<h3>7.4 Asymptotics and the exponent</h3>
<p>With \(\ell=\lambda/n\), \(\alpha=w/n\), \(\beta=p/n\), \(\omega=(\alpha-\beta,\beta,0)\), the limits are \(p_{r\to r'}=\frac{\alpha}{1-\alpha}\,\ell_r\,\tilde\tau(r,r')^2\) with \(\tilde\tau=\frac{\alpha-\beta}\alpha\sqrt{\tilde R_1(r)\tilde R_1(r')}+(-1)^{r+r'}\frac\beta\alpha\sqrt{\tilde R_2(r)\tilde R_2(r')}\), where \(\tilde R_t(r)\) is the degree-zero limit of \(R_t^2/\ell_r\) (the factor \(\ell_r\) is the vanishing partial hook of the empty third row of \(\varepsilon\); cancelling it makes the boundary \(\ell_3=0\) regular: a move into an empty third row keeps order-one mass, as \(p(a_1\to b_2)\) did in Section 6). The Perron limit of the symmetrised coefficient matrix is the row sum including the self-loop, which takes the striking form</p>
<div class="eq">\[\Lambda_{CW2}(\ell;\alpha,\beta)=1-\sum_{r<r'}\big(\sqrt{p_{r\to r'}}-\sqrt{p_{r'\to r}}\big)^2 .\]</div>
<p>The bound on binary codes is then, by Bassalygo–Elias and the paper's Theorem 4.2 with the box argument of Theorem 6.2, \(R_2(\delta)\le\kappa_{CW2}(\delta)=\inf\{1-H_2(\alpha)+H(\ell)-\alpha H_2(\beta/\alpha)\}\) over admissible \((\alpha,\beta,\ell)\) with \(\Lambda_{CW2}>1-\delta/(2\alpha(1-\alpha))\), the threshold being the normalised Johnson eigenvalue at distance \(d\). Two checks anchor the limit: the finite-\(n\) closed forms converge to it like \(1/n\), and on the slice \(\ell_3=0\) it equals the paper's \(\Lambda\) of (6) to twelve digits and reproduces the paper's rate function to fifteen.</p>
<table><thead><tr><th>δ</th><th>M₂</th><th>paper κ_CW (γ*)</th><th>paper's slice γ = 0</th><th>κ_CW2 (ℓ₃*)</th><th>gain vs slice</th><th>gain vs paper</th></tr></thead><tbody>
__CW2TABLE__
</tbody></table>
<figure><img alt="Left: gains over M2 of the paper's constant-weight exponent and of the three-row exponent, and the gains of the three-row exponent over its own two-row slice and over the paper's exponent, versus delta on a symmetric log scale. Right: the optimal third-row fraction versus delta." src="__FIG6__"><figcaption><strong>Figure 6.</strong> Left: what the third row buys. Gains over \(M_2\) of the paper's \(\kappa_{CW}\) (grey) and of \(\kappa_{CW2}\) (blue); the gain of \(\kappa_{CW2}\) over its own two-row slice (green, always positive) and over the paper's \(\gamma\)-optimised \(\kappa_{CW}\) (red, positive only at small \(\delta\)). Right: the optimal third-row fraction \(\ell_3^*\).</figcaption></figure>
<p>__CW2_TEXT__</p>

<h3>7.5 Assessment</h3>
<ul>
<li><strong>New:</strong> the closed form of Proposition 7.1, the first explicit description of a moving-subspace graph beyond two-row shapes, and the identity \(\Lambda=1-\sum(\sqrt{p}-\sqrt{p'})^2\), which says that the spectral quantity the method needs is one minus the total "irreversibility" of the coefficient matrix.</li>
<li><strong>Small:</strong> the exponent gain over the paper's \(\kappa_{CW}\) is at most __CW2_MAXGAIN__ bits and exists only for __CW2_DRANGE__; beyond that the paper's \(\gamma>0\) construction is better, and the two cannot be combined (Section 7.1). The gain over the two-row slice with \(\gamma=0\) is larger and present at every distance, which is the clean statement of what a third row buys.</li>
<li><strong>Together with Section 6:</strong> the best exponent now known to us is \(\kappa_{CW2}\) for __CW2_DRANGE__, the paper's \(\kappa_{CW}\) in between, and \(\kappa_{2row}\) for \(\delta\ge\delta_1\).</li>
</ul>
<div class="callout"><div class="t">Not a Eureka</div>A new closed form and a new, verified, very small number. We would only use the word for an improvement that changes the picture; this one changes the sixth decimal.</div>
</section>

<section>
<h2><span class="num">8</span>Method and reproducibility</h2>'''
rep('''<section>
<h2><span class="num">8</span>Method and reproducibility</h2>''', SECTION7)

# ---- method list
rep(r'''experiments/hyperoct_proof_check.py  the proof's algebra: Edmonds 6j table vs exact values; the eight identities; sum rule; reciprocity</code></pre>''',
    r'''experiments/hyperoct_proof_check.py  the proof's algebra: Edmonds 6j table vs exact values; the eight identities; sum rule; reciprocity
phb/layer3.py           exact S_n computation of the three-row layer graph (permutation modules, Specht projections, E-copy)
phb/gl3.py              gl_3 Gelfand-Tsetlin modules, invariant form, tensor products, highest-weight vectors, intertwiners
phb/cw2_gl3.py          coefficients via GL_3 recoupling (the tau formula)      phb/cw2_formulas.py  Proposition 7.1
phb/cw2_asymptotics.py  limits, Lambda_CW2, threshold, exponent optimisation
experiments/layer3_collect.py / cw2_R_collect.py / cw2_R_fit.py / cw2_sign.py / cw2_kappa2.py / cw2_kappa_final.py / make_figure6.py</code></pre>''')

# ---- establishes bullets
rep(r'''A formal (Lean) proof has not been attempted.</li>''',
    r'''A formal (Lean) proof has not been attempted.</li>
<li><strong>Section 7</strong> is again our construction. Its closed form is a verified proposition (exact on every computed case, reciprocity exact in rational arithmetic) with a clear identification in the classical literature, not yet a written proof; its exponent gain over the paper is real but of order \(10^{-6}\), and only at small distances.</li>''')

# ---- figure 6 substitution and dynamic table
DYN = r'''out = out.replace("__FIG4__", img("fig4_spherical.png")).replace("__FIG5__", img("fig5_two_row.png")).replace("__FIG6__", img("fig6_cw2.png"))
# ---- Section 7 table and numbers
import json as _json
_cw2p = ROOT / "results" / "cw2_kappa_final.json"
if not _cw2p.exists():
    _cw2p = ROOT / "results" / "cw2_kappa_grid.json"
_rows_cw2 = _json.load(open(_cw2p)) if _cw2p.exists() else []
_tab = []; _pos = []; _neg = []; _maxg = (0.0, None)
for _r in _rows_cw2:
    _kp = _r.get("paper_refined", _r["paper_kappa_CW"]); _k2 = _r.get("cw2_refined", _r["kappa_CW2"]); _k0 = _r["paper_gamma0"]
    _opt = _r.get("cw2_refined_opt", _r["cw2_opt"]); _g = _r.get("paper_refined_opt", _r["paper_opt"])[2]
    _gain = _kp - _k2
    (_pos if _gain > 0 else _neg).append(_r["delta"])
    if _gain > _maxg[0]: _maxg = (_gain, _r["delta"])
    _tab.append(f"<tr><td>{_r['delta']:.3f}</td><td>{_r['M2']:.7f}</td><td>{_kp:.7f} ({_g:.1e})</td><td>{_k0:.7f}</td><td>{_k2:.7f} ({_opt['ell'][2]:.1e})</td><td>{_k0-_k2:+.1e}</td><td>{_gain:+.1e}</td></tr>")
out = out.replace("__CW2TABLE__", "\n".join(_tab) if _tab else "<tr><td colspan=7>pending</td></tr>")
_dr = (f"\\(\\delta\\le{max(_pos):.2f}\\)" if _pos else "no \\(\\delta\\)")
_cross = f"{max(_pos):.2f}" if _pos else "—"
_mg = f"\\({_maxg[0]*1e6:.1f}\\times10^{{-6}}\\)"
out = out.replace("__CW2_MAXGAIN__", _mg).replace("__CW2_DRANGE__", _dr).replace("__CW2_DCROSS__", _cross)
out = out.replace("__CW2_TILE__", (f"{_maxg[0]*1e6:.1f} × 10⁻⁶ bits" if _maxg[1] is not None else "—"))
_txt = ""
if _rows_cw2:
    _txt = (f"Read across a row: at \\(\\delta={_maxg[1]}\\) the paper's exponent is beaten by \\({_maxg[0]*1e6:.1f}\\times10^{{-6}}\\) bits, the largest gain on the grid; "
            f"the optimal third row is tiny (\\(\\ell_3^*\\) of order \\(10^{{-5}}\\)), as the optimal second rows were in Section 6, and the gain has the same square-root-against-entropy mechanism. "
            f"The gain over the paper's own \\(\\gamma=0\\) slice is positive at every grid point.")
    if _neg:
        _txt += f" From \\(\\delta={min(_neg):.2f}\\) on, the paper's \\(\\gamma>0\\) construction wins."
out = out.replace("__CW2_TEXT__", _txt)'''
rep(r'''out = out.replace("__FIG4__", img("fig4_spherical.png")).replace("__FIG5__", img("fig5_two_row.png"))''', DYN)

p.write_text(s, encoding="utf-8")
print("patched build_report.py (section 7)")
