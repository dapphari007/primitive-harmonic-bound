"""One-off patch: add Section 8 (m-row layer graphs, four-row results) to build_report.py (idempotent)."""
import pathlib
p = pathlib.Path(__file__).with_name("build_report.py")
s = p.read_text(encoding="utf-8")
if "Proposition 8.1" in s:
    print("already patched"); raise SystemExit

def rep(old, new):
    global s
    assert old in s, f"anchor not found: {old[:90]!r}"
    s = s.replace(old, new, 1)

# ---- chip
rep(r'''<span class="chip">section 7: new closed form</span></span>''',
    r'''<span class="chip">section 7: new closed form</span> <span class="chip">section 8: all rows</span></span>''')

# ---- abstract paragraph
rep(r'''This is a new formula and a small new number, not a breakthrough; we say so.</p>''',
    r'''This is a new formula and a small new number, not a breakthrough; we say so.</p>
<p><strong>Section 8 does it for any number of rows.</strong> With a stabilizer shape of \(m-1\) rows and ambient shapes of \(m\) rows, the same partial-hook formula holds with \(k\) running over \(m\) rows, and the two-term sum becomes an \((m-1)\)-term sum whose signs follow one rule: a term is negative exactly when its row lies between the two moving rows. We verified this at \(m=4\) (four-row ambient shapes) on every computed overlap and in exact arithmetic on the reciprocity identity, and identified the formula with a 1975 result of Hecht on \(U(N)\) Racah coefficients with two totally symmetric representations. The fourth row buys about one percent of what the third row bought: __CWM_GAIN4__ bits at \(\delta=0.10\). Rows are a convergent series with a tiny sum; the picture does not change.</p>''')

# ---- renumber 8,9,10 -> 9,10,11
rep('<h2><span class="num">10</span>Sources</h2>', '<h2><span class="num">11</span>Sources</h2>')
rep('<h2><span class="num">9</span>What this establishes, and what it does not</h2>', '<h2><span class="num">10</span>What this establishes, and what it does not</h2>')
rep('<h2><span class="num">8</span>Method and reproducibility</h2>', '<h2><span class="num">9</span>Method and reproducibility</h2>')

SECTION8 = r'''<section>
<h2><span class="num">8</span>Any number of rows: the general formula, and why rows stop paying</h2>
<p>Section 7 is the case \(m=3\) of a family. Let the stabilizer irrep be \(E=S^{\varepsilon}\boxtimes\mathbf 1_{S_N}\) with \(\varepsilon\) a shape of \(w\) with \(m-1\) rows. By Pieri's rule the ambient irreps \(S^\lambda\) with \(\mathrm{Hom}_H(E,S^\lambda)\ne0\) are exactly the shapes \(\lambda\) with \(m\) rows interlacing \(\varepsilon\), each with multiplicity one, so the paper's Theorem 4.2 applies for every \(m\). The paper's construction is \(m=2\), Section 7 is \(m=3\). The reduction of Section 7.2 is uniform in \(m\): a move \(\lambda\to\lambda'=\lambda-\square_r+\square_{r'}\) has coefficient \(\frac wN\frac{f^{\lambda'}}{f^\nu}\tau^2\) with \(\tau=\sum_{t=1}^{m-1}\frac{f^{\varepsilon-\square_t}}{f^\varepsilon}R_t(\lambda,\nu)R_t(\lambda',\nu)\), where \(R_t\) is the overlap of two coupling schemes in \(V_{\varepsilon-\square_t}\otimes\mathbb C^m\otimes\mathrm{Sym}^N\mathbb C^m\) for \(GL_m\). We implemented \(GL_m\) modules in the Gelfand–Tsetlin basis for general \(m\) (commutation relations, Serre relations, adjointness and Weyl dimensions all exact for \(m\le5\)) and computed the overlaps at \(m=4\).</p>

<h3>8.1 Proposition 8.1: the closed form for all rows</h3>
<p>Write partial hooks \(Q_k=\lambda_k+m-k\) and \(P_k=\varepsilon_k+m-k\) (\(k=1,\dots,m\), with \(\varepsilon_m=0\)). Then, for \(\nu=\lambda-\square_r\) and \(t\le m-1\),</p>
<div class="eq">\[R_t(\lambda,\nu)^2=\frac{\prod_{k\ne r}|P_t-Q_k-1|\;\prod_{k\ne t}|Q_r-P_k|}{\prod_{k\ne t}|P_t-P_k-1|\;\prod_{k\ne r}|Q_r-Q_k|},\qquad \tau=\sum_{t=1}^{m-1}(-1)^{[r\le t]+[r'\le t]}\,\frac{f^{\varepsilon-\square_t}}{f^\varepsilon}\,R_t(\lambda,\nu)R_t(\lambda',\nu),\]</div>
<p>with \(R_t\ge0\): the \(t\)-th term is negative exactly when row \(t\) lies between the two moving rows. For \(m=3\) this is Proposition 7.1 (the rule gives \((-1)^{r+r'}\)). At \(m=4\) the formula for \(R_t^2\) agrees with the \(GL_4\) computation on all 183 squared overlaps at generic four-row points (to \(10^{-15}\)); the sign rule was read off the computed products for all twelve move types; the resulting coefficients satisfy the dimension-weighted reciprocity exactly in rational arithmetic on 517 of 517 random cases, reduce to Proposition 7.1 when the fourth row and the third stabilizer row are empty (to \(6\times10^{-17}\)), and have positive self-loops.</p>
<p>The formula is not new to the literature in substance. Hecht (Commun. Math. Phys. 41, 1975) derived the general \(U(N)\) Racah coefficient for the recoupling of \([f^1]\times[f^2]\times[f^3]\) when two of the representations are totally symmetric, by expressing it as a matrix element of a permutation operator in the Young–Yamanouchi basis; the answer is a product of factors \(1-1/\tau_{ik}\) of "axial distances" \(\tau_{ik}=(f_i-i)-(f_k-k)\), which are exactly partial-hook differences, and for a single moving box (\(p=1\)) it is a pure product. Our \(R_t\) is a Racah coefficient of that class, with \([1]\) and \([N]\) the two totally symmetric representations. We have not carried out the specialisation of his phases and normalisation, so Proposition 8.1 stays a verified proposition; the route to a theorem is now a citation and bookkeeping rather than a new idea.</p>

<h3>8.2 The exponent for four rows</h3>
<p>The limits of Section 7.4 hold verbatim with \(m\) rows: \(p_{r\to r'}=\frac\alpha{1-\alpha}\ell_r\tilde\tau^2\), \(\tilde\tau=\sum_t\sigma_t\frac{\omega_t}\alpha\sqrt{\tilde R_t(r)\tilde R_t(r')}\), \(\Lambda=1-\sum_{r<r'}(\sqrt{p_{r\to r'}}-\sqrt{p_{r'\to r}})^2\), and the bound is the infimum of \(1-H_2(\alpha)+H(\ell)-\alpha H(\omega/\alpha)\) over interlacing \((\ell,\omega)\) with \(\Lambda\) above the Johnson threshold. The finite-\(n\) closed forms converge to these limits like \(1/n\) at four rows, and the general code reproduces the three-row exponent exactly. The optimum was sought with the three-row optimum as a seed (a fourth row and a third stabilizer row grown from zero) and with random starts.</p>
<table><thead><tr><th>δ</th><th>paper κ_CW</th><th>three rows κ_CW2</th><th>four rows κ_CW3</th><th>fourth row buys</th><th>third row bought</th><th>four rows vs paper</th></tr></thead><tbody>
__CWMTABLE__
</tbody></table>
<p>__CWM_TEXT__</p>

<h3>8.3 Assessment</h3>
<ul>
<li><strong>New:</strong> the uniform description of the whole family (Proposition 8.1 with its sign rule), and the recognition that these moving-subspace graphs are governed by Hecht's class of Racah coefficients, which explains why the two-row binary graph of Section 6 had product coefficients (there the fundamental representation was the only moving piece) and why the layer graphs are squares of sums.</li>
<li><strong>Small:</strong> each additional row buys about one percent of the previous row's gain, at ever smaller optimal row sizes. The series converges to essentially the three-row value. Within the paper's framework, rows inside a layer are exhausted.</li>
<li><strong>What would change the picture:</strong> not more rows, but a different stabilizer. The one lever the framework leaves is the multiplicity-one condition; every extension we found that beats it (two nontrivial Young-subgroup factors with more than two ambient rows) violates it. A framework that tolerates multiplicity, or a stabilizer that is not a Young subgroup, is where a larger gain would have to come from.</li>
</ul>
<div class="callout"><div class="t">Not a Eureka</div>The rows are a convergent series with a tiny sum. We now know the whole series in closed form, and we know where its total lands: within \(10^{-5}\) of the paper's bound at small distances, on the right side of it.</div>
</section>

<section>
<h2><span class="num">9</span>Method and reproducibility</h2>'''
rep('''<section>
<h2><span class="num">9</span>Method and reproducibility</h2>''', SECTION8)

# ---- method list
rep(r'''experiments/layer3_collect.py / cw2_R_collect.py / cw2_R_fit.py / cw2_sign.py / cw2_kappa2.py / cw2_kappa_final.py / make_figure6.py</code></pre>''',
    r'''experiments/layer3_collect.py / cw2_R_collect.py / cw2_R_fit.py / cw2_sign.py / cw2_kappa2.py / cw2_kappa_final.py / make_figure6.py
phb/glm.py              gl_m Gelfand-Tsetlin modules for any m (checked for m <= 5)      phb/cwm_gl.py  general recoupling, conjecture C(m)
phb/cwm_asymptotics.py  m-row limits and exponent optimisation         experiments/cwm_test.py / cwm_kappa.py   four-row verification and exponent
results/hecht1975_text.txt   text of Hecht (1975) used for the identification of Proposition 8.1</code></pre>''')

# ---- establishes bullets
rep(r'''its exponent gain over the paper is real but of order \(10^{-6}\), and only at small distances.</li>''',
    r'''its exponent gain over the paper is real but of order \(10^{-6}\), and only at small distances.</li>
<li><strong>Section 8</strong> extends the closed form to any number of rows (verified at four rows, identified with Hecht's 1975 class of \(U(N)\) Racah coefficients) and shows numerically that further rows contribute a geometric tail of about one percent per row.</li>''')

# ---- dynamic table
DYN = r'''# ---- Section 8 table
_cwmp = ROOT / "results" / "cwm_kappa_all.json"
if not _cwmp.exists():
    _cwmp = ROOT / "results" / "cwm_kappa.json"
_rows_cwm = sorted(_json.load(open(_cwmp)), key=lambda r: r["delta"]) if _cwmp.exists() else []
_cw2f = {r["delta"]: r for r in _rows_cw2}
_tabm = []; _g4_at_01 = None; _ratios = []
for _r in _rows_cwm:
    _d = _r["delta"]; _k3 = _r["kappa_m3"]; _k4 = _r["kappa_m4"]; _kp = _r["paper"]
    _g43 = _k3 - _k4
    _g32 = (_cw2f[_d]["paper_gamma0"] - _cw2f[_d].get("cw2_refined", _cw2f[_d]["kappa_CW2"])) if _d in _cw2f else float("nan")
    if _g32 == _g32 and _g32 > 0: _ratios.append(_g43 / _g32)
    if abs(_d - 0.10) < 1e-9: _g4_at_01 = _g43
    _tabm.append(f"<tr><td>{_d:.3f}</td><td>{_kp:.7f}</td><td>{_k3:.7f}</td><td>{_k4:.7f}</td><td>{_g43:+.1e}</td><td>{_g32:+.1e}</td><td>{_kp-_k4:+.1e}</td></tr>")
out = out.replace("__CWMTABLE__", "\n".join(_tabm) if _tabm else "<tr><td colspan=7>pending</td></tr>")
out = out.replace("__CWM_GAIN4__", (f"\\({_g4_at_01*1e7:.1f}\\times10^{{-7}}\\)" if _g4_at_01 is not None else "a few \\(10^{-7}\\)"))
_txtm = ""
if _rows_cwm:
    _rat = (sum(_ratios) / len(_ratios)) if _ratios else float("nan")
    _txtm = (f"The fourth row's gain over three rows is between {min(r['kappa_m3']-r['kappa_m4'] for r in _rows_cwm):.1e} and {max(r['kappa_m3']-r['kappa_m4'] for r in _rows_cwm):.1e} bits on the grid, "
             f"about {100*_rat:.1f}% of what the third row gained over the paper's two-row slice at the same distance; the optimal fourth row is of order \\(10^{{-8}}\\) to \\(10^{{-7}}\\) and the optimal third stabilizer row of order \\(10^{{-6}}\\). "
             f"Extrapolating the geometric trend, all further rows together add less than two percent of the third row's gain. The paper's \\(\\gamma>0\\) construction still wins from \\(\\delta=0.15\\) on.")
out = out.replace("__CWM_TEXT__", _txtm)'''
rep(r'''out = out.replace("__CW2_TEXT__", _txt)''', r'''out = out.replace("__CW2_TEXT__", _txt)
''' + DYN)

p.write_text(s, encoding="utf-8")
print("patched build_report.py (section 8)")
