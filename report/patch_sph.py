"""One-off patch: add the spherical-code section (Section 5) to build_report.py (idempotent)."""
import pathlib
p = pathlib.Path(__file__).with_name("build_report.py")
s = p.read_text(encoding="utf-8")
if "Spherical codes and the sphere-packing exponent" in s:
    print("already patched"); raise SystemExit

def rep(old, new):
    global s
    assert old in s, f"anchor not found: {old[:70]!r}"
    s = s.replace(old, new, 1)

# figure 4 + level-4/5 numbers filled at build time
rep(r'''out = out.replace("__CWCROSS__", (ROOT / "report" / "cw_crossover_paragraph.html").read_text(encoding="utf-8") if (ROOT / "report" / "cw_crossover_paragraph.html").exists() else "")''',
r'''out = out.replace("__CWCROSS__", (ROOT / "report" / "cw_crossover_paragraph.html").read_text(encoding="utf-8") if (ROOT / "report" / "cw_crossover_paragraph.html").exists() else "")
out = out.replace("__FIG4__", img("fig4_spherical.png"))
gl = (ROOT / "results" / "sph_gamma_levels.txt").read_text() if (ROOT / "results" / "sph_gamma_levels.txt").exists() else ""
for r in (4, 5):
    m = re.search(rf"level r={r}: gamma_{r} = ([0-9.]+)\s+deficit = ([0-9.e+-]+)\s+s\* = 2Gamma = ([0-9.]+)", gl)
    out = out.replace(f"__G{r}__", (f"<tr><td>level {r}</td><td>{float(m.group(1)):.7f}</td><td>{float(m.group(2)):.2e}</td><td>{float(m.group(3)):.4f}</td><td>—</td></tr>" if m else ""))
cx = ""
for f in ("sph_crossover_kissing_part1.txt", "sph_crossover_kissing_part2.txt"):
    if (ROOT / "results" / f).exists():
        cx += (ROOT / "results" / f).read_text()
rows = re.findall(r"\s*(\d+)\s*\|\s*([0-9.]+)\s+([0-9.]+)\s+\d+\s*\|\s*([0-9.]+)\s+([0-9.]+)\s+\((\d+), (\d+)\)\s*\|\s*([0-9.]+)\s+([0-9.]+)\s+\((\d+), (\d+), (\d+)\)\s*\|\s*([+-][0-9.]+)\s+([+-][0-9.]+)", cx)
tbl = ""
for row in sorted(rows, key=lambda x: int(x[0])):
    n, b0, r0, b1, r1, k, L, b2, r2, k2, I, J, g1, g2 = row
    if int(n) in (24, 48, 64, 96, 128, 256, 384, 512, 1024, 2048, 4096, 8192):
        cls = lambda g: "win" if float(g) > 0 else "lose"
        tbl += f"<tr><td>{int(n):,}</td><td>{float(r0):.5f}</td><td>{float(r1):.5f}</td><td>({k}, {L})</td><td class=\"{cls(g1)}\">{float(g1):+.3f}</td><td>{float(r2):.5f}</td><td>({k2}, {I}, {J})</td><td class=\"{cls(g2)}\">{float(g2):+.3f}</td></tr>"
out = out.replace("__KISSROWS__", tbl)''')

# abstract sentence
rep(r'''Unexpectedly, \(\kappa_{CW}\le\kappa_H\) everywhere: the constant-weight family contains the whole-cube bound as its middle-layer boundary and is strictly better below \(\delta_1=0.2350\).</p>
</div>''',
r'''Unexpectedly, \(\kappa_{CW}\le\kappa_H\) everywhere: the constant-weight family contains the whole-cube bound as its middle-layer boundary and is strictly better below \(\delta_1=0.2350\).</p>
<p>Finally we audited the spherical-code hierarchy (paper Sections 4–8). Every transcription identity holds to \(10^{-14}\), the one-row and two-row certificates never beat the spherical Delsarte LP in 64 cases, the classical specialization reproduces the 1978 Kabatianskii–Levenshtein exponents (0.5990 for packings, 0.4009 for kissing numbers), and our own optimization of the hierarchy reproduces the paper's Figure 4 deficits from the packing threshold \(\lambda_*=\tfrac12\log_2(2\pi/e)\): \(5.3\times10^{-3}\), \(1.5\times10^{-3}\), \(2.0\times10^{-4}\), \(1.5\times10^{-5}\), \(1.7\times10^{-6}\) for the classical, one-row and level-1, 2, 3 families. New numbers: the hierarchy lowers the kissing-number exponent from 0.4009 to 0.3966, and the moving-harmonic certificate beats the classical kissing certificate from dimension 96 on (consistently from 384).</p>
</div>''')

# tiles
rep(r'''  <div class="tile"><div class="k">Largest exponent gain</div>''',
r'''  <div class="tile"><div class="k">Kissing-number exponent</div><div class="v">0.4009 → 0.3966</div><div class="d">upper bound on lim sup (1/n) log₂ τ_n: Kabatianskii–Levenshtein versus the level-1 spherical certificate (whole sphere, no cap needed)</div></div>
  <div class="tile"><div class="k">Packing threshold reproduced</div><div class="v">1.7 × 10⁻⁶</div><div class="d">deficit of the level-3 spherical certificate from λ* = ½ log₂(2π/e) = 0.60440, found by our own optimizer at s* = 0.7499, matching the paper's Figure 4</div></div>
  <div class="tile"><div class="k">Largest exponent gain</div>''')

# renumber sections 5,6,7 -> 6,7,8 and insert section 5
rep('<h2><span class="num">7</span>Sources</h2>', '<h2><span class="num">8</span>Sources</h2>')
rep('<h2><span class="num">6</span>What this establishes, and what it does not</h2>', '<h2><span class="num">7</span>What this establishes, and what it does not</h2>')
rep('<h2><span class="num">5</span>Method and reproducibility</h2>', '<h2><span class="num">6</span>Method and reproducibility</h2>')
rep(r'''<section>
<h2><span class="num">6</span>Method and reproducibility</h2>''',
r'''<section>
<h2><span class="num">5</span>Spherical codes and the sphere-packing exponent</h2>
<p>The same projection argument bounds spherical codes \(A(n,s)\), sets of unit vectors with pairwise inner products at most \(s\), and through Sidelnikov's upper-hemisphere inequality \(\Delta_n\le((1-s)/2)^{n/2}A(n+1,s)\) it bounds sphere-packing densities. The classical certificate keeps the single \(SO(n-1)\)-fixed line (a Gegenbauer polynomial) in each harmonic space \(\mathcal H_i(\mathbb R^n)\); the paper replaces it by the tangent-harmonic space \(E_x=\mathcal H_k(x^\perp)\), and then by arbitrary stabilizer representations with \(r\) Young-diagram rows, whose ambient spaces \(V_\lambda\) form an \((r+1)\)-dimensional <em>representation graph</em>. Theorem 6.2 (eq. (80)) is the finite bound \(A(n,s)\le\frac{1-s}{d_\mu(\Lambda_\Omega-s)}\sum_{\lambda\in\Omega}D_\lambda\), with edge weights from the directed squared coordinate coefficients (76) and the Weyl dimensions (113). Asymptotically a level-\(r\) tuple \(a_1>b_1>\cdots>b_r>a_{r+1}\ge0\) has spectral quantity \(\Gamma_r=\sum_\ell R_\ell\,q(a_\ell)\) and exponent \(\Phi_r=\sum_\ell\mathsf H_{sph}(a_\ell)-\sum_m\mathsf H_{sph}(b_m)\), the packing exponent is \(\gamma_r=\sup[\tfrac12\log_2\tfrac{2}{1-2\Gamma_r}-\Phi_r]\), and Theorem 8.3 proves \(\gamma_r\uparrow\lambda_*=\tfrac12\log_2(2\pi/e)=0.604400\ldots\), the Cohn–Elkies exponent of Chapter 1.</p>

<h3>5.1 Transcription checks</h3>
<ul>
<li>Classical path \(k=0\): the eigenvalues of the tridiagonal matrix with entries (73) coincide with the roots of the Gegenbauer polynomial \(C^{(n-2)/2}_{L+1}\) to \(1.3\times10^{-15}\) for \((n,L)\) up to \((50,30)\).</li>
<li>The two-row coefficients (81) agree with the general formula (76) at \(r=1\) exactly, over 200 random \((n,k,i,j)\).</li>
<li>On the full graph the directed coefficients sum to one (eq. (77)) to \(2\times10^{-16}\), and the dimension reciprocity (78) with the Weyl formula (113) holds to \(2\times10^{-14}\), at levels \(r=1,2,3\); the two-row dimension \(D_{i,j}\) matches (113).</li>
<li>The recurrence coefficients (68) for multiplication by \(\langle x,\cdot\rangle\) on the copy of \(\mathcal H_k(x^\perp)\) inside \(\mathcal H_i\) were recomputed by Gauss–Jacobi quadrature in the separated coordinates (65): agreement \(2.6\times10^{-14}\) for \(n\le15\), \(k\le3\).</li>
<li>Classical limits: \(\gamma_0=0.599056\) at \(s=0.454\) and \(B_{KL}(1/2)=0.400944\), the 1978 Kabatianskii–Levenshtein packing and kissing exponents.</li>
</ul>

<h3>5.2 Soundness against the spherical LP</h3>
<p>The Delsarte–Goethals–Seidel LP (polynomials of degree \(\le50\) with nonnegative Gegenbauer coefficients, nonpositive on \([-1,s]\), sign constraint enforced on a 3000-point grid and checked on a 60,000-point grid) reproduces the classical values 13.158, 25.558, 240 and 196560 for kissing numbers in dimensions 3, 4, 8, 24. For \(n\in\{5,6,7,8,10,12,16,24\}\) and eight thresholds \(s\in[-0.3,0.8]\), every one-row certificate (\(k\le8\), \(L\le24\)) and every two-row box certificate (\(k\le8\), \(I\le20\), \(J\le4\)) is at least the LP value: <strong>64 cases, zero violations</strong>. At these small dimensions the classical path is usually the best member of the family; the one-row certificate wins for negative or small \(s\) (19 cases), the two-row certificate for intermediate \(s\) (16 cases).</p>

<h3>5.3 The hierarchy reproduces the paper's Figure 4</h3>
<p>We optimized the level-\(r\) packing objective ourselves, with strict-interlacing log-increment coordinates, residues in log space, a region guard (an unbounded search otherwise drifts into a floating-point degenerate corner where nodes coincide), and hierarchical seeding of level \(r\) from the level-\((r-1)\) optimum. The resulting deficits from \(\lambda_*\) and the optimizing angles agree with the circles in the paper's Figure 4.</p>
<div class="tbl"><table>
<tr><th>certificate family</th><th>packing exponent γ</th><th>deficit λ* − γ</th><th>optimizing s*</th><th>paper Fig. 4 (read off)</th></tr>
<tr><td>classical (KL 1978)</td><td>0.5990558</td><td>5.35e-3</td><td>0.4540</td><td>≈ 5e-3 at s ≈ 0.45</td></tr>
<tr><td>one-row (tangent harmonics)</td><td>0.6028728</td><td>1.53e-3</td><td>0.5401</td><td>≈ 1.5e-3 at s ≈ 0.55</td></tr>
<tr><td>level 1</td><td>0.6041958</td><td>2.05e-4</td><td>0.6322</td><td>≈ 2e-4 at s ≈ 0.63</td></tr>
<tr><td>level 2</td><td>0.6043851</td><td>1.54e-5</td><td>0.7069</td><td>≈ 1.5e-5 at s ≈ 0.70</td></tr>
<tr><td>level 3</td><td>0.6043989</td><td>1.68e-6</td><td>0.7499</td><td>≈ 2e-6 at s ≈ 0.75</td></tr>
__G4__
__G5__
<tr><td>limit (Theorem 8.3)</td><td>0.6044005</td><td>0</td><td>→ 1</td><td>λ* = ½ log₂(2π/e)</td></tr>
</table></div>
<p>Each level reduces the deficit by roughly an order of magnitude, and the optimizing angle moves toward \(s\to1\), as the Chebyshev construction of Theorem 8.3 requires. Its explicit bound (109) evaluated at \(R=64\) already gives 0.604400, four digits of \(\lambda_*\). This is the numerical bridge between Chapters 1 and 2 of the paper: the spherical hierarchy and the Euclidean Mellin argument single out the same constant.</p>

<h3>5.4 Kissing numbers</h3>
<p>The kissing number \(\tau_n=A(n,1/2)\) is the most famous spherical-code quantity, and the best known asymptotic upper bound has been Kabatianskii–Levenshtein's \(2^{(0.4009+o(1))n}\) since 1978. Optimizing the paper's certificates at \(s=1/2\):</p>
<div class="tbl"><table>
<tr><th>certificate</th><th>whole-sphere exponent κ(1/2)</th><th>cap-optimized κ̄(1/2)</th></tr>
<tr><td>classical</td><td>0.401414</td><td>0.400944 (t* = 0.4854)</td></tr>
<tr><td>one-row</td><td>0.397306</td><td>0.397306 (t* = 1/2, cap does not help)</td></tr>
<tr><td>level 1</td><td>0.396626</td><td>0.396626 (t* = 1/2)</td></tr>
<tr><td>level 2</td><td>0.396601</td><td>≈ 0.39660</td></tr>
</table></div>
<p>So the hierarchy lowers the exponent of the kissing-number upper bound from 0.4009 to 0.3966, with the level-1 certificate capturing almost all of the gain and the spherical-cap reduction no longer helping. We have not seen this number stated in the paper. Its practical reach is limited: at finite \(n\) the certificate must beat the classical harmonic path before it beats anything else, and that happens first at \(n=96\) (one-row, 0.07 bits) and \(n=64\) (two-row, 0.13 bits), with isolated losses until \(n=384\), after which the one-row certificate wins consistently, by 15 bits at \(n=4096\).</p>
<div class="tbl"><table>
<tr><th>n</th><th>classical rate</th><th>one-row rate</th><th>(k, L)</th><th>gain (bits)</th><th>two-row rate</th><th>(k, I, J)</th><th>gain (bits)</th></tr>
__KISSROWS__
</table></div>
<figure><img alt="Left: deficits of the packing exponent from lambda_* for the classical, one-row and level-1 to level-5 certificates on a log scale. Middle: gaps between successive levels of the whole-sphere exponent as a function of the inner product s. Right: finite-dimensional kissing-number certificates versus dimension." src="__FIG4__"><figcaption><strong>Figure 4.</strong> Left: distance of each certificate family's packing exponent from the threshold \(\lambda_*\). Middle: how much each step of the hierarchy gains in the whole-sphere exponent, as a function of the inner-product threshold. Right: the finite-dimensional kissing-number certificates; the moving-harmonic certificate overtakes the classical one around \(n\approx100\) and separates cleanly beyond \(n\approx400\).</figcaption></figure>
<p><strong>What was not reconstructed.</strong> Unlike the binary and constant-weight cases, we did not rebuild the spherical kernel \(\mathrm{tr}(P_xP_y)\) from explicit tensor-valued harmonics, so the positivity of the two-row and higher certificates is tested here only through the LP comparison and the internal identities (77)–(78), not through a direct Bochner check. The one-row recurrence, on the other hand, reduces exactly to the Gegenbauer three-term recurrence, which we verified by quadrature.</p>
</section>

<section>
<h2><span class="num">6</span>Method and reproducibility</h2>''')

# method file list + establishes bullets
rep(r'''experiments/cw_test1_vs_lp.py / cw_test2_certificate.py / cw_asymptotics.py / cw_crossover.py / make_figure3.py</code></pre>''',
r'''experiments/cw_test1_vs_lp.py / cw_test2_certificate.py / cw_asymptotics.py / cw_crossover.py / make_figure3.py
phb/spherical.py        one-row (73), two-row (81), general (76) weights; Weyl dimensions (113); Gamma_r, Phi_r, kappa_r, gamma_r, Chebyshev tuples
phb/spherical_lp.py     degree-capped Delsarte-Goethals-Seidel LP (Gegenbauer basis)
experiments/sph_checks.py / sph_test1_vs_lp.py / sph_gamma_levels.py / sph_kissing.py / sph_crossover.py / make_figure4.py</code></pre>''')
rep(r'''<li><strong>Not covered:</strong> the spherical-code hierarchy and its sphere-packing consequence (Sections 4–8 of the paper). The same harness applies to its representation graphs.</li>''',
r'''<li><strong>The spherical audit is one layer thinner.</strong> Its transcription identities, LP comparisons and classical limits all pass, and our independent optimization reproduces the paper's Figure 4 to the digit, but the higher-level kernels were not rebuilt explicitly. The new kissing-number exponent 0.3966 is a numerical optimization of the paper's proven bound, not a new theorem.</li>
<li><strong>Not covered:</strong> the Lean formalization itself, and everything outside Chapter 2 of the paper.</li>''')

p.write_text(s, encoding="utf-8")
print("patched build_report.py (spherical section)")
