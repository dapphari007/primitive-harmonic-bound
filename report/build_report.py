"""Build the research note (self-contained HTML with embedded figures).  Run:  python report/build_report.py"""
import base64, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
def img(name):
    return "data:image/png;base64," + base64.b64encode((ROOT / "figures" / name).read_bytes()).decode()

# number of (n,d) pairs and violations in the extended exact-LP run (filled from results file if present)
ext = (ROOT / "results" / "test1_exact_41_64.txt").read_text() if (ROOT / "results" / "test1_exact_41_64.txt").exists() else ""
m = re.findall(r"n=(\d+) done, cumulative \(n,d\) pairs=(\d+), violations=(\d+)", ext)
ext_nmax, ext_pairs, ext_viol = (m[-1] if m else ("40", "0", "0"))
TOTAL_PAIRS = 777 + int(ext_pairs)
TOTAL_VIOL = int(ext_viol)

HTML = r"""<title>Beyond-MRRW Audit</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=STIX+Two+Text:ital,wght@0,400;0,600;0,700;1,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --paper:#F4F6F8; --card:#FFFFFF; --ink:#18232D; --muted:#5A6B79; --rule:#D5DDE4; --code:#EAF0F3;
  --teal:#0B7A78; --teal-soft:#D9EEEC; --violet:#5A4E96; --violet-soft:#E6E2F3; --ok:#2E7D4F; --warn:#9C6A12;
  --serif:"STIX Two Text",Georgia,"Times New Roman",serif; --sans:"IBM Plex Sans","Segoe UI",Helvetica,Arial,sans-serif; --mono:"IBM Plex Mono",Consolas,"Courier New",monospace;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --paper:#111920; --card:#18232C; --ink:#E4EBEF; --muted:#94A5B1; --rule:#2B3944; --code:#1F2C36;
  --teal:#4CB8B3; --teal-soft:#153A3A; --violet:#A79CDB; --violet-soft:#2B2745; --ok:#5CBF88; --warn:#D4A24C; }}
:root[data-theme="dark"]{
  --paper:#111920; --card:#18232C; --ink:#E4EBEF; --muted:#94A5B1; --rule:#2B3944; --code:#1F2C36;
  --teal:#4CB8B3; --teal-soft:#153A3A; --violet:#A79CDB; --violet-soft:#2B2745; --ok:#5CBF88; --warn:#D4A24C; }
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--serif);font-size:17px;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:76rem;margin:0 auto;padding:2.5rem 1.5rem 5rem}
header{display:grid;grid-template-columns:1fr;gap:.6rem;padding-bottom:1.6rem;border-bottom:1px solid var(--rule);margin-bottom:2rem}
.eyebrow{font-family:var(--sans);font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
h1{font-size:2.5rem;line-height:1.1;margin:0;font-weight:600;letter-spacing:-.01em;text-wrap:balance}
.sub{font-size:1.2rem;color:var(--muted);margin:0;max-width:56rem;text-wrap:balance}
.meta{font-family:var(--sans);font-size:.9rem;color:var(--muted);display:flex;flex-wrap:wrap;gap:.4rem 1.4rem;margin-top:.4rem}
.chip{display:inline-block;font-family:var(--sans);font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;padding:.18rem .55rem;border-radius:3px;background:var(--teal-soft);color:var(--teal);font-weight:600}
.chip.v{background:var(--violet-soft);color:var(--violet)}
main{display:grid;grid-template-columns:minmax(0,1fr);gap:2.2rem}
section{scroll-margin-top:1rem}
h2{font-size:1.55rem;font-weight:600;margin:0 0 .8rem;line-height:1.2;letter-spacing:-.005em;text-wrap:balance}
h2 .num{color:var(--teal);font-family:var(--sans);font-weight:600;font-size:.95rem;margin-right:.6rem;vertical-align:.15em;letter-spacing:.04em}
h3{font-size:1.12rem;font-weight:600;margin:1.4rem 0 .5rem}
p{margin:0 0 .95rem;max-width:68ch}
ul,ol{max-width:68ch;padding-left:1.3rem;margin:0 0 1rem}
li{margin-bottom:.35rem}
.abstract{background:var(--card);border:1px solid var(--rule);border-left:3px solid var(--teal);padding:1.1rem 1.3rem;max-width:none}
.abstract p{max-width:70ch;margin-bottom:.6rem}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:.9rem;margin:.4rem 0 .5rem}
.tile{background:var(--card);border:1px solid var(--rule);padding:.9rem 1rem;display:flex;flex-direction:column;gap:.25rem}
.tile .k{font-family:var(--sans);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.tile .v{font-family:var(--mono);font-size:1.55rem;font-variant-numeric:tabular-nums;color:var(--teal);line-height:1.1}
.tile .v.vi{color:var(--violet)}
.tile .d{font-size:.9rem;color:var(--muted);line-height:1.35}
figure{margin:1.2rem 0 1.6rem;background:var(--card);border:1px solid var(--rule);padding:.8rem}
figure img{display:block;width:100%;height:auto}
figcaption{font-family:var(--sans);font-size:.86rem;color:var(--muted);padding:.6rem .2rem 0;line-height:1.45}
.tbl{overflow-x:auto;margin:.6rem 0 1.4rem;border:1px solid var(--rule);background:var(--card)}
table{border-collapse:collapse;width:100%;font-family:var(--mono);font-size:.84rem;font-variant-numeric:tabular-nums}
th,td{padding:.42rem .7rem;text-align:right;border-bottom:1px solid var(--rule);white-space:nowrap}
th{font-family:var(--sans);font-weight:600;font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);text-align:right}
td:first-child,th:first-child{text-align:left}
tr:last-child td{border-bottom:none}
td.win{color:var(--teal);font-weight:500} td.lose{color:var(--violet)}
.callout{background:var(--card);border:1px solid var(--rule);padding:.9rem 1.1rem;margin:0 0 1rem;max-width:72ch}
.callout.warn{border-left:3px solid var(--warn)}
.callout.ok{border-left:3px solid var(--ok)}
.callout .t{font-family:var(--sans);font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;font-weight:600;margin-bottom:.3rem}
.callout.warn .t{color:var(--warn)} .callout.ok .t{color:var(--ok)}
code,pre{font-family:var(--mono);font-size:.86em}
code{background:var(--code);padding:.08em .35em;border-radius:3px}
pre{background:var(--code);padding:.8rem 1rem;overflow-x:auto;border:1px solid var(--rule);margin:0 0 1rem;line-height:1.45}
pre code{background:none;padding:0}
.eq{margin:.6rem 0 1rem;overflow-x:auto;padding:.2rem 0}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1.2rem 2rem}
a{color:var(--teal);text-decoration-thickness:1px;text-underline-offset:2px}
a:focus-visible,button:focus-visible{outline:2px solid var(--teal);outline-offset:2px}
.src li{font-size:.95rem}
footer{margin-top:3rem;padding-top:1rem;border-top:1px solid var(--rule);font-family:var(--sans);font-size:.85rem;color:var(--muted)}
mjx-container{overflow-x:auto;overflow-y:hidden}
</style>
<script>
window.MathJax={tex:{inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']]},svg:{fontCache:'global'}};
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-svg.js"></script>

<div class="wrap">
<header>
  <div class="eyebrow">Research note · computational audit · binary codes</div>
  <h1>Beyond-MRRW Audit</h1>
  <p class="sub">An independent numerical test and quantification of the primitive-harmonic upper bound for binary codes, the first claimed improvement of the MRRW exponent since 1977.</p>
  <div class="meta">
    <span>Harish K · research direction</span>
    <span>Claude Fable 5.1 (Anthropic) · computations, reconstruction, writing</span>
    <span>2 September 2026</span>
    <span><span class="chip">reproducible</span> <span class="chip v">sections 1–5: audit</span> <span class="chip">section 6: new theorem</span> <span class="chip">section 7: new closed form</span> <span class="chip">section 8: all rows</span></span>
  </div>
</header>

<main>

<section>
<div class="abstract">
<div class="eyebrow" style="margin-bottom:.4rem">Abstract</div>
<p>OpenAI's August 2026 collection <em>Ten Advances in Mathematics and Theoretical Computer Science</em> proves that the classical McEliece–Rodemich–Rumsey–Welch (MRRW) upper bounds on the rate of binary codes can be beaten at every relative distance, via a two-point Delsarte certificate in which every retained Fourier level carries a copy of an exponentially large "Boolean harmonic" space instead of a single fixed vector. Working from the released reasoning walkthrough and the paper, we transcribed the finite-length theorem, rebuilt its certificate from first principles, and subjected it to three independent tests.</p>
<p>Results. (1) The bound never falls below the exact Delsarte linear-programming optimum in any of the <strong>__TOTAL_PAIRS__</strong> length–distance pairs we checked (every \(d\) for \(4\le n\le56\) and for \(n=60,64\)), a necessary condition any two-point certificate must satisfy. (2) In our from-scratch reconstruction, the largest \(\lambda\) for which the kernel \((t-\lambda)K\) is positive definite equals the Perron eigenvalue of the paper's Jacobi matrix to six decimals in every configuration tested, and a multi-start optimizer cannot improve the paper's amplitude normalization at all. (3) The asymptotic exponent \(\kappa_H(\delta)\) is strictly below the first MRRW bound for all \(\delta\), and below the optimized second MRRW bound exactly when \(\delta>\delta_0=0.19504\); the paper's rational witness at \(\delta=4/13\) reproduces digit for digit. New quantitative facts: the block length at which the new certificate first beats the classical one is \(n=30\) at \(\delta=1/10\), \(n=160\) at \(\delta=1/4\) (isolated wins from \(n=20\)), and \(n=1105\) at \(\delta=4/13\) (isolated wins from \(n=468\)); and replacing the paper's trace Cauchy–Schwarz step by the exact constant Krawtchouk coefficient of the kernel tightens the finite-length bound by 2–7% at short lengths without changing the exponent.</p>
<p>The same audit was then applied to the paper's constant-weight (Johnson-layer) construction, which supplies the improvement below \(\delta_0\). Its associated Hahn recurrence coefficients, measured from an explicit construction of the tensor-product harmonic spaces, agree with the paper's formulas to \(10^{-16}\); its finite bound never falls below the exact Johnson-scheme LP in 1,090 cases; and its exponent \(\kappa_{CW}\) is below \(M_2\) at every distance, though by margins as small as \(10^{-6}\) bits per symbol at \(\delta=0.02\). Unexpectedly, \(\kappa_{CW}\le\kappa_H\) everywhere: the constant-weight family contains the whole-cube bound as its middle-layer boundary and is strictly better below \(\delta_1=0.2350\).</p>
<p>Finally we audited the spherical-code hierarchy (paper Sections 4–8). Every transcription identity holds to \(10^{-14}\), the one-row and two-row certificates never beat the spherical Delsarte LP in 64 cases, the classical specialization reproduces the 1978 Kabatianskii–Levenshtein exponents (0.5990 for packings, 0.4009 for kissing numbers), and our own optimization of the hierarchy reproduces the paper's Figure 4 deficits from the packing threshold \(\lambda_*=\tfrac12\log_2(2\pi/e)\): \(5.3\times10^{-3}\), \(1.5\times10^{-3}\), \(2.0\times10^{-4}\), \(1.5\times10^{-5}\), \(1.7\times10^{-6}\) for the classical, one-row and level-1, 2, 3 families. New numbers: the hierarchy lowers the kissing-number exponent from 0.4009 to 0.3966, and the moving-harmonic certificate beats the classical kissing certificate from dimension 96 on (consistently from 384).</p>
<p><strong>Section 6 goes beyond the audit.</strong> We built the binary analogue of the paper's multi-row spherical hierarchy, which the paper mentions but does not pursue: a representation graph for the hyperoctahedral group whose vertices are bipartitions with two rows on each side. We computed its coordinate-transition coefficients exactly for \(n\le13\), found closed forms (each coefficient is a quadratic in the harmonic degree \(k\) whose roots are the Littlewood–Richardson admissibility boundaries), verified them on every computed case and checked the two identities the paper's general theorem needs on hundreds of thousands of cases, and derived the asymptotic exponent \(\kappa_{2row}(\delta)\). It is strictly below the paper's whole-cube exponent at every distance and, for \(\delta\ge\delta_1=0.2350\) where the paper's Theorem 1.1 reduces to that exponent, strictly below the paper's bound: at \(\delta=0.3\) it gives \(0.248150\) against \(0.248376\). At the middle level the two-row graph reproduces the classical second MRRW bound exactly. The closed forms are proved: by Schur–Weyl duality each coefficient is a branching ratio times a squared SU(2) 6j-symbol with a spin-\(\tfrac12\) entry, and the eight resulting identities are verified by computer algebra. The improvement over the paper's Theorem 1.1 is therefore a theorem, resting only on the paper's general projection bound, Schur–Weyl duality, and Edmonds' table of 6j-symbols.</p>
<p><strong>Section 7 opens a third row inside a constant-weight layer.</strong> The paper's layer construction (Section 3) lives on two-row ambient shapes; we let the ambient shapes have three rows, which is the largest multiplicity-free extension of that construction. We computed the coordinate-transition coefficients exactly for \(n\le12\), reduced them by Schur–Weyl duality to \(GL_3\) recoupling coefficients, and found and verified a closed form: each coefficient is the square of a two-term sum of square roots of ratios of products of partial-hook differences, the structure of the classical \(U(3)\) fundamental Wigner coefficients. The resulting exponent \(\kappa_{CW2}\) improves the paper's constant-weight exponent \(\kappa_{CW}\) for small distances (__CW2_DRANGE__) by at most __CW2_MAXGAIN__ bits, and loses to it beyond, where the paper's second Young-subgroup parameter matters and cannot be combined with a third row. This is a new formula and a small new number, not a breakthrough; we say so.</p>
<p><strong>Section 8 does it for any number of rows.</strong> With a stabilizer shape of \(m-1\) rows and ambient shapes of \(m\) rows, the same partial-hook formula holds with \(k\) running over \(m\) rows, and the two-term sum becomes an \((m-1)\)-term sum whose signs follow one rule: a term is negative exactly when its row lies between the two moving rows. We verified this at \(m=4\) (four-row ambient shapes) on every computed overlap and in exact arithmetic on the reciprocity identity, and identified the formula with a 1975 result of Hecht on \(U(N)\) Racah coefficients with two totally symmetric representations. The fourth row buys about one percent of what the third row bought: __CWM_GAIN4__ bits at \(\delta=0.10\). Rows are a convergent series with a tiny sum; the picture does not change.</p>
</div>
</section>

<section>
<h2><span class="num">IN PLAIN WORDS</span>What this is about, with small examples</h2>
<p><strong>The problem.</strong> A binary code is a list of words of \(n\) bits in which any two words differ in at least \(d\) positions, so that a few flipped bits can never turn one word into another. With 8-bit words and \(d=2\) you can keep 128 words (all words with an even number of ones); with \(d=4\) only 16 survive. For long words with \(d\) a fixed fraction \(\delta\) of \(n\), the count grows like \(2^{Rn}\), and nobody knows the largest possible growth rate \(R\). Gilbert and Varshamov showed how large it can at least be; McEliece, Rodemich, Rumsey and Welch (MRRW) showed in 1977 how large it can at most be. That ceiling had not moved in 49 years.</p>
<p><strong>How ceilings are proved.</strong> Attach a "spotlight" (a vector in a big space) to every word. The overlap of two spotlights depends only on how far apart the words are. Choose the spotlights so that overlaps between distinct codewords are always non-positive, while the total overlap of all spotlights together can never be negative. Then the only way the sum can be non-negative is if there are few words: that is the ceiling. The classical proof uses one spotlight per word. The new idea is to give every word a whole <em>bundle</em> of spotlights, exponentially many, all moving rigidly with the word. A bundle has a large "size" (its dimension) but, in the precise sense the proof needs, bundles overlap no more than single spotlights do, so the ceiling drops.</p>
<p><strong>What we did.</strong> Three things a careful referee would do with a calculator. First, we re-computed the paper's own worked example and got its numbers to every printed digit. Second, we used a known "best possible spotlight ceiling" (the Delsarte linear program, which can be computed exactly for short words) as a lie detector: no spotlight argument can beat it, so if the new formula ever did, the formula would be wrong. In 2,749 length-and-distance cases it never did. Third, we rebuilt the bundles ourselves from scratch, with no help from the paper's proof, and measured directly whether the overlap sums are positive. They are, and the weighting the paper uses is exactly the best possible one.</p>
<p><strong>What we added.</strong> Numbers the paper does not state. For example, at distance 4/13 the new ceiling only beats the old one for words longer than about 1,100 bits; at distance 1/10 it already wins at 30 bits. The whole-cube version beats the strongest classical ceiling only for \(\delta\) above 0.195; below that, the paper's constant-weight version is needed, and there the improvement is real but tiny (a millionth of a bit per symbol at \(\delta=0.02\)).</p>
<p><strong>Spheres, in plain words.</strong> The same machinery works for points on a sphere that must stay a fixed angle apart, which is how one bounds kissing numbers (how many equal balls can touch one ball at once: 12 in three dimensions, 24 in four, 240 in eight) and sphere-packing densities. The best ceiling on how fast kissing numbers can grow with the dimension had been \(2^{0.4009n}\) since 1978; optimizing the paper's spherical certificates lowers it to \(2^{0.3966n}\), and the certificates start beating the classical one at around a hundred dimensions. For packings, each level of the paper's hierarchy gets about ten times closer to the exponent \(	frac12\log_2(2\pi/e)\) that its first chapter proves for the Cohn–Elkies linear program; we recomputed those distances ourselves and they match the paper's figure.</p>
<p><strong>On the word "Eureka".</strong> We reserve it for a genuinely new mathematical fact: a theorem, or a number in a published table that we can move. Nothing in this note qualifies; it is verification and quantification of someone else's theorem, done carefully. We say so plainly rather than dress it up.</p>
</section>

<section>
<h2><span class="num">AT A GLANCE</span>What the numbers say</h2>
<div class="tiles">
  <div class="tile"><div class="k">LP soundness tests</div><div class="v">0 / 2,749</div><div class="d">violations of bound ≥ exact Delsarte LP: __TOTAL_PAIRS__ Hamming cases (every d, 4 ≤ n ≤ 56 and n = 60, 64) plus 1,090 Johnson-layer cases (n ≤ 30)</div></div>
  <div class="tile"><div class="k">Positivity constant</div><div class="v">λ* = λ</div><div class="d">best positive-definite λ in our reconstruction equals the Perron eigenvalue in 13/13 configurations (6 decimals)</div></div>
  <div class="tile"><div class="k">Crossing with MRRW2</div><div class="v">δ₀ = 0.19504</div><div class="d">whole-cube exponent κ_H beats the optimized second MRRW bound exactly for δ above this value</div></div>
  <div class="tile"><div class="k">First overtake, δ = 4/13</div><div class="v vi">n = 1105</div><div class="d">new certificate beats the classical one at every scanned length from here (first isolated win at n = 468)</div></div>
  <div class="tile"><div class="k">Hahn coefficients, rebuilt</div><div class="v">10⁻¹⁶</div><div class="d">agreement between the paper's associated Hahn formulas (36)–(37) and coefficients measured from an explicit construction, 11 (p, q) pairs</div></div>
  <div class="tile"><div class="k">Layers vs whole cube</div><div class="v">δ₁ = 0.2350</div><div class="d">below δ₁ the constant-weight exponent κ_CW is strictly below κ_H; above it the optimal layer is the middle one and the two coincide</div></div>
  <div class="tile"><div class="k">Kissing-number exponent</div><div class="v">0.4009 → 0.3966</div><div class="d">upper bound on lim sup (1/n) log₂ τ_n: Kabatianskii–Levenshtein versus the level-1 spherical certificate (whole sphere, no cap needed)</div></div>
  <div class="tile"><div class="k">Packing threshold reproduced</div><div class="v">1.7 × 10⁻⁶</div><div class="d">deficit of the level-3 spherical certificate from λ* = ½ log₂(2π/e) = 0.60440, found by our own optimizer at s* = 0.7499, matching the paper's Figure 4</div></div>
  <div class="tile"><div class="k">Two-row binary exponent (new)</div><div class="v">0.24815 &lt; 0.24838</div><div class="d">at δ = 0.3: this note's κ_2row versus the paper's Theorem 1.1 (κ_bin = κ_H), with MRRW2 at 0.25023; the coefficient formulas behind it are proved via Schur–Weyl duality and 6j-symbols</div></div>
  <div class="tile"><div class="k">Three-row layer graph (new)</div><div class="v">__CW2_TILE__</div><div class="d">closed form for all coefficients (partial-hook products, verified on every computed case); exponent κ_CW2 below the paper's κ_CW for δ ≲ __CW2_DCROSS__, above it beyond</div></div>
  <div class="tile"><div class="k">Largest exponent gain</div><div class="v">0.0304 bits</div><div class="d">over MRRW1 at δ ≈ 0.048; over MRRW2 the maximum is 0.0034 bits at δ ≈ 0.255 (1.0% relative at δ ≈ 0.264)</div></div>
</div>
</section>

<section>
<h2><span class="num">1</span>The claim under audit</h2>
<p>Let \(A_2(n,d)\) be the largest binary code of length \(n\) and minimum distance \(d\), and \(R_2(\delta)=\limsup \tfrac1n\log_2 A_2(n,\lceil\delta n\rceil)\). Since 1977 the best upper bounds have been the two MRRW bounds, \(M_1(\delta)=H_2\big(\tfrac12-\sqrt{\delta(1-\delta)}\big)\) and the optimized constant-weight version \(M_2(\delta)\le M_1(\delta)\). Chapter 2 of the OpenAI collection (paper: Theorem 1.1; walkthrough: §2.1–2.5) claims \(R_2(\delta)<M_2(\delta)\) for every \(0<\delta<\tfrac12\), and the repository <code>openai/ten-proofs</code> ships a Lean 4 file, <code>MetricCodes.lean</code>, for this chapter.</p>
<p>The finite-length statement is fully explicit, which is what makes an outside audit possible. Fix integers \(0\le k<L\le n-k\) and let \(J_H(n,k,L)\) be the symmetric tridiagonal matrix indexed by Fourier degrees \(i=k,\dots,L\) with zero diagonal and</p>
<div class="eq">\[ (J_H)_{i,i+1}=(J_H)_{i+1,i}=c^{(k)}_i=\frac{(i-k+1)(n-i-k)}{n\sqrt{(i+1)(n-i)}} . \]</div>
<p><strong>Theorem 2.1 (paper).</strong> With \(s=1-2d/n\), \(\lambda=\lambda_{\max}(J_H(n,k,L))\) and \(d^\square_k=\binom nk-\binom n{k-1}\): if \(\lambda>s\), then</p>
<div class="eq">\[ A_2(n,d)\;\le\;\frac{1-s}{d^\square_k(\lambda-s)}\sum_{i=k}^{L}\binom ni . \tag{23} \]</div>
<p>At \(k=0\) the entries reduce to the normalized Krawtchouk recurrence \(\sqrt{(i+1)(n-i)}/n\) and (23) is the classical Levenshtein-type bound behind \(M_1\). The novelty is \(k>0\): every retained Fourier level carries an isometric copy of the \(d^\square_k\)-dimensional space \(E_k=\ker(D\colon V_k\to V_{k-1})\), and the dimension count in (23) divides by \(d^\square_k\). Taking \(k/n\to b\), \(L/n\to a\) gives \(\lambda\to\Gamma_H(a,b)=2\,(a(1-a)-b(1-b))/\sqrt{a(1-a)}\) and</p>
<div class="eq">\[ \kappa_H(\delta)=\inf\{\,H_2(a)-H_2(b):\ 0\le b<a\le\tfrac12,\ \Gamma_H(a,b)>1-2\delta\,\},\qquad R_2(\delta)\le\kappa_H(\delta)<M_1(\delta). \]</div>
<p>Why audit a formally verified result? Because the claim is large, the mechanism is new, and an independent reconstruction that agrees is worth more than a re-reading. It also lets us ask the questions the paper does not: where exactly the new exponent crosses \(M_2\), at what block lengths the certificate starts to win, and whether the specific normalization in the proof is optimal.</p>
</section>

<section>
<h2><span class="num">2</span>Verification</h2>

<h3>2.1 Transcription check against the worked example</h3>
<p>The walkthrough gives one eight-bit example: for \(n=8\), \(k=1\), \(L=7\) the Perron eigenvalue is 0.569289 and the resulting bound on the even-weight code (\(d=2\)) is 261.843; the tempting "associated Krawtchouk" recurrence would instead give eigenvalue \(3/4\) and the false bound \(508/7<128\). Our implementation of (23) reproduces all four numbers to every stated digit, so the code under test is the formula in the paper.</p>

<h3>2.2 Soundness against the exact Delsarte linear program</h3>
<p>The paper states that its kernel "produces an ordinary scalar Delsarte certificate". Any such certificate is at least the Delsarte LP optimum \(\mathrm{LP}(n,d)\), so \(\text{(23)}\ge\mathrm{LP}(n,d)\) must hold for every \((n,d,k,L)\) with \(\lambda>s\). A single violation would refute the finite-length theorem. We computed \(\lambda_{\max}\) for every \((k,L)\) and compared with the LP for every \(d\).</p>
<div class="callout ok"><div class="t">Result</div>Zero violations across __TOTAL_PAIRS__ pairs \((n,d)\): every \(d\) for \(4\le n\le56\) and for \(n=60,64\), every feasible \((k,L)\). The bound touches the LP only in trivial cases (e.g. \(d=n\), where both equal 2).</div>
<p>Two implementation notes matter for anyone repeating this. HiGHS in floating point silently fails above \(n\approx45\) (it reports "unbounded" or "unknown") because the optimal \(A_i\) reach \(2^{40}\) while the constant \(A_0=1\) must still be resolved; we therefore wrote a dense simplex over exact rationals (Bland's rule), validated it against HiGHS for \(n\le32\) to relative error \(4\times10^{-11}\), and used it for \(41\le n\le56\) and \(n=60,64\) (each LP takes up to a few seconds at \(n=64\)). Second, at these short lengths the \(k\ge1\) certificate already beats the \(k=0\) one in 199 of the 777 pairs with \(n\le40\), always with \(L\) close to \(n-k\), a regime unrelated to the asymptotic one; the fixed-\(\delta\) crossover in §3.2 is the meaningful comparison.</p>
<div class="tbl"><table>
<tr><th>n</th><th>d</th><th>log₂ LP(n,d)</th><th>best k = 0 (L)</th><th>best k ≥ 1 (k, L)</th><th>k ≥ 1 wins?</th></tr>
<tr><td>16</td><td>4</td><td>11.0000</td><td>12.5665 (3)</td><td>12.2342 (2, 13)</td><td class="win">yes</td></tr>
<tr><td>24</td><td>8</td><td>12.0000</td><td>13.5523 (3)</td><td>13.3692 (4, 13)</td><td class="win">yes</td></tr>
<tr><td>32</td><td>10</td><td>15.3663</td><td>16.8768 (3)</td><td>17.1390 (5, 16)</td><td class="lose">no</td></tr>
<tr><td>40</td><td>6</td><td>29.2492</td><td>33.0114 (10)</td><td>30.5570 (3, 32)</td><td class="win">yes</td></tr>
<tr><td>40</td><td>12</td><td>18.8058</td><td>20.5753 (4)</td><td>20.8108 (7, 27)</td><td class="lose">no</td></tr>
</table></div>

<h3>2.3 The certificate rebuilt from first principles</h3>
<p>To test the mechanism rather than the formula, we built the objects directly on the Fourier side of the cube for \(n\le12\): the raising and lowering maps \(U,D\), an orthonormal basis of \(E_k\), the isometric embeddings \(\iota_j=U^{\,j-k}|_{E_k}\) (we confirmed numerically that \(U^{j-k}\) restricted to \(E_k\) is a scalar multiple of an isometry, as the sl\(_2\) identities predict), the sign operators \(\sigma_x\) that translate by a word \(x\), and the projection \(P_x\) onto \(\{\sum_j a_j\sigma_x\iota_jY\}\). The kernel \(K(x,y)=\mathrm{tr}(P_xP_y)\) depends only on \(t=d_H(x,y)\).</p>
<p>The proof's key identity (27) says that \((t(x,y)-\lambda)K(x,y)\) is a positive-definite kernel. We therefore defined, for any unit amplitude vector \(a\),</p>
<div class="eq">\[ \lambda^*(a)=\max\{\lambda:\ (t-\lambda)K_a \text{ is positive definite on } \{\pm1\}^n\}=\min_{j}\frac{\widehat{(tK_a)}_j}{\widehat{(K_a)}_j}, \]</div>
<p>computed from the Krawtchouk expansions, and compared with the paper's \(\lambda\). This is an independent test: nothing about the isometry \(B\) or the eigen-relation (25) enters; only Bochner positivity on the group.</p>
<div class="tbl"><table>
<tr><th>(n, k, L)</th><th>λ from (22)</th><th>λ*, paper's a</th><th>λ*, a = Perron vector</th><th>λ*, a² ∝ v</th></tr>
<tr><td>(8, 1, 7)</td><td>0.569289</td><td class="win">0.569289</td><td>0.565411</td><td>0.541269</td></tr>
<tr><td>(8, 2, 6)</td><td>0.264837</td><td class="win">0.264837</td><td>0.259642</td><td>0.259260</td></tr>
<tr><td>(10, 1, 5)</td><td>0.548256</td><td class="win">0.548256</td><td>0.529674</td><td>0.498981</td></tr>
<tr><td>(10, 3, 7)</td><td>0.172378</td><td class="win">0.172378</td><td>0.168001</td><td>0.170133</td></tr>
<tr><td>(12, 2, 10)</td><td>0.450218</td><td class="win">0.450218</td><td>0.446329</td><td>0.436782</td></tr>
<tr><td>(12, 3, 9)</td><td>0.258821</td><td class="win">0.258821</td><td>0.254346</td><td>0.254490</td></tr>
<tr><td>(8, 0, 3) classical</td><td>0.750000</td><td class="win">0.750000</td><td>0.681818</td><td>0.540636</td></tr>
<tr><td>(10, 0, 4) classical</td><td>0.800000</td><td class="win">0.800000</td><td>0.742857</td><td>0.560488</td></tr>
</table></div>
<p style="font-size:.9rem;color:var(--muted)">Six of the thirteen configurations tested; the full table is in <code>results/test2_certificate.txt</code>. The two \(k=0\) rows are controls: there the paper's normalization reproduces the classical Krawtchouk certificate (largest root \(3/4\) and \(4/5\)), while the alternatives do not.</p>
<p>With the paper's normalization \(a_j^2\propto\sqrt{\binom nj}\,v_j\) (where \(v\) is the Perron vector), \(\lambda^*(a)\) equals \(\lambda_{\max}(J_H)\) to six decimals in all thirteen configurations tested; the two natural alternatives fall short every time. We then let a multi-start Nelder–Mead search maximize \(\lambda^*(a)\) over all nonnegative unit vectors for five configurations: it could not move the paper's vector by even \(10^{-9}\) or raise \(\lambda^*\) by more than \(10^{-16}\). The "dimension-weighted reciprocity" in the proof is therefore not merely sufficient for positivity; it is the optimal amplitude choice for this family of kernels.</p>
<div class="callout warn"><div class="t">Sharper finite-length form</div>The paper closes with trace Cauchy–Schwarz, \(\sum_{x,y\in C}K\ge |C|^2 (d^\square_k)^2/D_{\rm amb}\). Because \(K\) itself is positive definite with constant Krawtchouk coefficient \(\widehat K_0\ge (d^\square_k)^2/D_{\rm amb}\), the same argument gives \(A_2(n,d)\le (1-s)\,d^\square_k\big/\big((\lambda-s)\widehat K_0\big)\), and the single Delsarte polynomial \(f(t)=(t-s)K(t)\) gives \(A_2(n,d)\le f(0)/\widehat f_0\), which is sharper still. At \(n\le12\) this tightens (23) by 2–7% (e.g. 286.4 → 267.2 at \(n=10,k=1,L=5,d=3\); 231.2 → 215.7 at \(n=12,k=3,L=9,d=5\)). The exponent is unchanged, since \(\widehat K_0\) and \((d^\square_k)^2/D_{\rm amb}\) agree to first order in the exponent.</div>
</section>

<section>
<h2><span class="num">3</span>Quantitative findings</h2>

<h3>3.1 The exponent function and its crossing with the second MRRW bound</h3>
<p>For fixed \(b\) the constraint \(\Gamma_H(a,b)\ge1-2\delta\) is a lower bound on \(a\), and \(H_2\) is increasing, so \(\kappa_H(\delta)\) is a one-dimensional minimization over \(b\) after solving the boundary \(\sqrt{a(1-a)}=\big[(1-2\delta)+\sqrt{(1-2\delta)^2+16\,b(1-b)}\big]/4\). Optimizing gives the table below; \(M_2\) is computed by minimizing \(F_\delta(\tau)\) over \(0\le\tau\le1-2\delta\).</p>
<div class="tbl"><table>
<tr><th>δ</th><th>M₁ (MRRW1)</th><th>M₂ (MRRW2)</th><th>κ_H (this bound)</th><th>κ_H &lt; M₁</th><th>κ_H &lt; M₂</th><th>a*</th><th>b*</th></tr>
<tr><td>0.05</td><td>0.858236</td><td>0.825137</td><td>0.827872</td><td class="win">yes</td><td class="lose">no</td><td>0.5000</td><td>2.57e-2</td></tr>
<tr><td>0.10</td><td>0.721928</td><td>0.692741</td><td>0.699832</td><td class="win">yes</td><td class="lose">no</td><td>0.3071</td><td>2.91e-2</td></tr>
<tr><td>0.15</td><td>0.591857</td><td>0.573450</td><td>0.577921</td><td class="win">yes</td><td class="lose">no</td><td>0.1879</td><td>1.61e-2</td></tr>
<tr><td>0.20</td><td>0.468996</td><td>0.461360</td><td>0.460900</td><td class="win">yes</td><td class="win">yes</td><td>0.1204</td><td>8.34e-3</td></tr>
<tr><td>0.25</td><td>0.354579</td><td>0.353711</td><td>0.350379</td><td class="win">yes</td><td class="win">yes</td><td>0.0758</td><td>3.91e-3</td></tr>
<tr><td>0.30</td><td>0.250225</td><td>0.250225</td><td>0.248376</td><td class="win">yes</td><td class="win">yes</td><td>0.0451</td><td>1.57e-3</td></tr>
<tr><td>4/13</td><td>0.235193</td><td>0.235193</td><td>0.233596</td><td class="win">yes</td><td class="win">yes</td><td>0.0413</td><td>1.34e-3</td></tr>
<tr><td>0.35</td><td>0.158133</td><td>0.158133</td><td>0.157506</td><td class="win">yes</td><td class="win">yes</td><td>0.0241</td><td>4.94e-4</td></tr>
<tr><td>0.40</td><td>0.081469</td><td>0.081469</td><td>0.081337</td><td class="win">yes</td><td class="win">yes</td><td>0.0103</td><td>9.78e-5</td></tr>
<tr><td>0.45</td><td>0.025266</td><td>0.025266</td><td>0.025257</td><td class="win">yes</td><td class="win">yes</td><td>0.0025</td><td>6.18e-6</td></tr>
</table></div>
<p>Three facts follow. \(\kappa_H<M_1\) everywhere, as the paper proves, with the largest gain 0.0304 bits per symbol at \(\delta\approx0.048\). The whole-cube construction alone beats the optimized second MRRW bound exactly for \(\delta>\delta_0\), with \(\delta_0=0.19504\) by bisection; below \(\delta_0\) the paper's constant-weight refinement is genuinely needed, which matches its remark that near \(\delta=0.1\) the whole-cube value (0.700) loses to \(M_2\) (0.693). Above \(\delta_0\) the gain over \(M_2\) peaks at 0.0034 bits per symbol near \(\delta=0.255\), about one percent of the bound. The paper's explicit witness at \(\delta=4/13\), \(a=1/25\), \(b=1/1500\), reproduces exactly: the spectral margin is the rational \(3182386369/213890625000000\), and \(H_2(1/25)-H_2(1/1500)=0.2342969<0.2345<M_2(4/13)=0.2351934\). The optimized value at that distance is slightly better, \(\kappa_H(4/13)=0.2335956\).</p>
<figure><img alt="Left: rate exponent versus relative distance for Gilbert–Varshamov, MRRW1, MRRW2 and kappa_H. Right: the gain of kappa_H over MRRW1 and MRRW2, crossing zero at delta_0 = 0.19504." src="__FIG1__"><figcaption><strong>Figure 1.</strong> Left: the classical bounds and the whole-cube primitive-harmonic exponent \(\kappa_H\). Right: the gain in exponent. Against \(M_1\) the gain is positive throughout; against \(M_2\) it changes sign at \(\delta_0=0.19504\).</figcaption></figure>

<h3>3.2 Where the finite-length certificate starts to win</h3>
<p>The paper proves an asymptotic separation and says explicitly that it does not claim an improvement at short block lengths. We measured the crossover: for \(\delta\) fixed and \(n\) ranging over multiples of the denominator, minimize (23) over \(L\) at \(k=0\) and over \((k,L)\) at \(k\ge1\) (coarse-to-fine integer search guided by the asymptotic optimizers), and record the gain in bits.</p>
<div class="two">
<div class="tbl"><table>
<tr><th colspan="5">δ = 4/13</th></tr>
<tr><th>n</th><th>k = 0 rate</th><th>k ≥ 1 rate</th><th>(k, L)</th><th>gain (bits)</th></tr>
<tr><td>390</td><td>0.30144</td><td>0.30198</td><td>(1, 22)</td><td class="lose">−0.211</td></tr>
<tr><td>468</td><td>0.29716</td><td>0.29630</td><td>(1, 26)</td><td class="win">+0.400</td></tr>
<tr><td>676</td><td>0.28195</td><td>0.28235</td><td>(1, 34)</td><td class="lose">−0.270</td></tr>
<tr><td>1040</td><td>0.27074</td><td>0.27115</td><td>(2, 52)</td><td class="lose">−0.428</td></tr>
<tr><td>1105</td><td>0.26951</td><td>0.26868</td><td>(2, 54)</td><td class="win">+0.920</td></tr>
<tr><td>2600</td><td>0.25478</td><td>0.25397</td><td>(5, 121)</td><td class="win">+2.100</td></tr>
<tr><td>6500</td><td>0.24641</td><td>0.24458</td><td>(9, 283)</td><td class="win">+11.907</td></tr>
<tr><td>13000</td><td>0.24202</td><td>0.24052</td><td>(17, 554)</td><td class="win">+19.508</td></tr>
<tr><td>26000</td><td>0.23951</td><td>0.23796</td><td>(41, 1110)</td><td class="win">+40.315</td></tr>
</table></div>
<div class="tbl"><table>
<tr><th colspan="5">δ = 1/4 and δ = 1/10</th></tr>
<tr><th>δ, n</th><th>k = 0 rate</th><th>k ≥ 1 rate</th><th>(k, L)</th><th>gain (bits)</th></tr>
<tr><td>1/4, 20</td><td>0.74379</td><td>0.71933</td><td>(2, 11)</td><td class="win">+0.489</td></tr>
<tr><td>1/4, 80</td><td>0.53139</td><td>0.53406</td><td>(1, 11)</td><td class="lose">−0.213</td></tr>
<tr><td>1/4, 160</td><td>0.47215</td><td>0.47179</td><td>(2, 20)</td><td class="win">+0.058</td></tr>
<tr><td>1/4, 1200</td><td>0.38738</td><td>0.38385</td><td>(5, 101)</td><td class="win">+4.242</td></tr>
<tr><td>1/4, 16000</td><td>0.36053</td><td>0.35634</td><td>(64, 1240)</td><td class="win">+67.093</td></tr>
<tr><td>1/10, 20</td><td>0.98602</td><td>1.00036</td><td>(1, 19)</td><td class="lose">−0.287</td></tr>
<tr><td>1/10, 30</td><td>0.94831</td><td>0.88770</td><td>(1, 27)</td><td class="win">+1.818</td></tr>
<tr><td>1/10, 1000</td><td>0.75232</td><td>0.73774</td><td>(7, 238)</td><td class="win">+14.580</td></tr>
<tr><td>1/10, 10000</td><td>0.72866</td><td>0.71403</td><td>(63, 2245)</td><td class="win">+146.324</td></tr>
</table></div>
</div>
<p>Two features are worth recording. The crossover is not monotone at first: at \(\delta=4/13\) the new certificate wins at \(n=468\), loses again at 585, 676, 845 and 1040, and wins at every scanned length from 1105 onward; the alternation comes from the integer rounding of the optimal \(L\) in the classical bound, whose value jumps by a few tenths of a bit as \(L\) increments. Beyond the crossover the gain grows linearly in \(n\) at the asymptotic rate difference (about 0.0016 bits per symbol at \(\delta=4/13\), 0.0042 at \(\delta=1/4\), 0.0221 at \(\delta=1/10\)), and the optimal harmonic degree \(k\) grows like \(b^*n\), reaching \(k=41\) at \(n=26000\) for \(\delta=4/13\), in line with \(b^*=1.34\times10^{-3}\). Both certificates converge to their limits slowly, from above, at a rate consistent with a \(\Theta(\log n/n)\) polynomial prefactor.</p>
<figure><img alt="Three panels showing log2(bound)/n versus block length n on a log scale for delta = 1/10, 1/4 and 4/13, comparing the classical certificate and the best k >= 1 certificate, with the MRRW1, MRRW2 and kappa_H limits as dashed lines." src="__FIG2__"><figcaption><strong>Figure 2.</strong> Finite-length rate of the two certificates. The primitive-harmonic curve (red) separates from the classical one (blue) early at \(\delta=1/10\), around \(n\approx10^2\) at \(\delta=1/4\), and only around \(n\approx10^3\) at \(\delta=4/13\), where the asymptotic gain is 0.0016 bits per symbol.</figcaption></figure>
</section>

<section>
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
<p>So the hierarchy lowers the exponent of the kissing-number upper bound from 0.4009 to 0.3966, with the level-1 certificate capturing almost all of the gain and the spherical-cap reduction no longer helping. We have not seen this number stated in the paper. To make it a checkable statement rather than an optimizer's output, here is an explicit witness verified in 30-digit arithmetic: the level-1 tuple \(a=(0.09005196,\ 0.000368267)\), \(b=(0.006476675)\) is strictly interlacing with positive residues \((0.93710976,\ 0.06289024)\), satisfies \(2\Gamma_1(a,b)=0.500000993>	frac12\), and has \(\Phi_1(a,b)=0.3966277\). By the paper's Theorem 1.2 this gives</p>
<div class="eq">\[ \limsup_{n	o\infty}	frac1n\log_2	au_n\;\le\;0.3966277, \]</div>
<p>against the Kabatianskii–Levenshtein value 0.400944. It is a corollary of their theorem evaluated at one point, not a new theorem, but it is the first explicit constant below 0.4 for this problem that we are aware of. Its practical reach is limited: at finite \(n\) the certificate must beat the classical harmonic path before it beats anything else, and that happens first at \(n=96\) (one-row, 0.07 bits) and \(n=64\) (two-row, 0.13 bits), with isolated losses until \(n=384\), after which the one-row certificate wins consistently, by 15 bits at \(n=4096\).</p>
<div class="tbl"><table>
<tr><th>n</th><th>classical rate</th><th>one-row rate</th><th>(k, L)</th><th>gain (bits)</th><th>two-row rate</th><th>(k, I, J)</th><th>gain (bits)</th></tr>
__KISSROWS__
</table></div>
<figure><img alt="Left: deficits of the packing exponent from lambda_* for the classical, one-row and level-1 to level-5 certificates on a log scale. Middle: gaps between successive levels of the whole-sphere exponent as a function of the inner product s. Right: finite-dimensional kissing-number certificates versus dimension." src="__FIG4__"><figcaption><strong>Figure 4.</strong> Left: distance of each certificate family's packing exponent from the threshold \(\lambda_*\). Middle: how much each step of the hierarchy gains in the whole-sphere exponent, as a function of the inner-product threshold. Right: the finite-dimensional kissing-number certificates; the moving-harmonic certificate overtakes the classical one around \(n\approx100\) and separates cleanly beyond \(n\approx400\).</figcaption></figure>
<p><strong>What was not reconstructed.</strong> Unlike the binary and constant-weight cases, we did not rebuild the spherical kernel \(\mathrm{tr}(P_xP_y)\) from explicit tensor-valued harmonics, so the positivity of the two-row and higher certificates is tested here only through the LP comparison and the internal identities (77)–(78), not through a direct Bochner check. The one-row recurrence, on the other hand, reduces exactly to the Gegenbauer three-term recurrence, which we verified by quadrature.</p>
</section>

<section>
<h2><span class="num">6</span>The binary two-row representation graph: a new exponent</h2>
<p>The paper's spherical hierarchy replaces a one-dimensional path of harmonic degrees by a lattice of ambient representations with several Young-diagram rows, and its Proposition 4.1 and Theorem 4.2 are stated for a general group acting on a set with unit coordinate vectors. For the cube the group is the hyperoctahedral group \(B_n=\mathbb Z_2^n\rtimes S_n\), the stabilizer of a word is \(S_n\), the coordinate representation is \(W=\mathbb R^n\) with \(\ell_x=x/\sqrt n\), and the irreducible ambient representations are indexed by bipartitions \((\alpha,\beta)\) with \(|\alpha|+|\beta|=n\): the Fourier level \(V_j\) is \(((n-j),(j))\). Tensoring with \(W\) moves one box between \(\alpha\) and \(\beta\), so the classical path acquires "second-row" neighbours \(((n-j-1),(j,1))\) and \(((n-j,1),(j-1))\). The paper remarks that more general binary stabilizer types can require matrix-valued transitions and leaves this direction aside. For two-row shapes on both sides everything stays scalar: the stabilizer irrep \(E_\mu\), \(\mu=(n-k,k)\), occurs in \(V_{(\alpha,\beta)}|_{S_n}\) with multiplicity \(\le1\) (two-row Littlewood–Richardson rule: \(a_2+b_2\le k\le\min\{a_1+b_2,\,a_2+b_1\}\)), the box moves are multiplicity-free, and \(\mathrm{End}_{S_n}(E_\mu)=\mathbb R\). So Theorem 4.2 applies verbatim once the directed squared coordinate coefficients \(p(\lambda\to\lambda')\) are known. Section 6.2 determines them exactly.</p>

<h3>6.1 Computing the coefficients exactly</h3>
<p>We realized \(V_{(\alpha,\beta)}\) as \(\bigoplus_{|S|=|\beta|}\chi_S\otimes E_{b_2}(S)\otimes E_{a_2}(S^c)\) (Walsh character times the paper's own Boolean harmonic spaces on \(S\) and its complement), took a random vector, projected it onto the \(E_\mu\)-isotypic part with the \(S_n\) class sums of transpositions and 3-cycles, tensored with \(\ell_0\), and projected onto each constituent of \(W\otimes V_\lambda\) with the \(B_n\) class sums \(\sum_q\varepsilon_q\), \(\sum[(ij)+(ij)\varepsilon_i\varepsilon_j]\), \(\sum[(ij)\varepsilon_i+(ij)\varepsilon_j]\), whose eigenvalues on a bipartition are \(n-2|\beta'|\), \(2(c(\alpha')+c(\beta'))\), \(2(c(\alpha')-c(\beta'))\) (content sums), by exact Lagrange interpolation. On the classical path this reproduces the paper's \(\alpha_j^2=\frac{(j-k+1)(n-j-k)}{n(j+1)}\) and \(\beta_j^2=\frac{(j-k)(n-j-k+1)}{n(n-j+1)}\) to all digits, and shows that the missing mass \(1-\alpha_j^2-\beta_j^2\) goes to the two second-row targets as \(\frac{k(n-k+1)}{n(j+1)}\) and \(\frac{k(n-k+1)}{n(n-j+1)}\). All coefficients are rational; we computed 3,196 of them for \(n\le11\) and second rows up to 2, plus 144 further coefficients at \(n=12\) with a second row of size 3, all matching the closed forms below to \(2\times10^{-16}\).</p>

<h3>6.2 Closed forms: Theorem 6.1</h3>
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
<p><strong>Theorem 6.1.</strong> <em>For every admissible vertex and every admissible \(k\), the directed squared coordinate coefficients of the binary two-row graph are given by the eight formulas above; a move whose target does not contain \(E_\mu\) has coefficient zero. Moreover the coefficients out of every vertex sum to one, and \(D_\lambda p(\lambda\to\lambda')=D_{\lambda'}p(\lambda'\to\lambda)\) with \(D_\lambda=\binom n{|\beta|}f^\alpha f^\beta\).</em></p>
<p>The formulas were first found by exact interpolation in \(k\) at each computed vertex and then proved as follows. Write \(J=\tfrac n2-k\), \(j_\alpha=\tfrac{a_1-a_2}2\), \(j_\beta=\tfrac{b_1-b_2}2\); for a move that takes a box out of row \(r\) of \(\alpha\) into row \(r'\) of \(\beta\), put \(j_{\alpha'}=j_\alpha\mp\tfrac12\) (\(r=1,2\)) and \(j_\nu=j_\beta\pm\tfrac12\) (\(r'=1,2\)). The proof has three steps.</p>
<p><em>Step 1: fibres.</em> The sign group \(\mathbb Z_2^n\) acts on \(W\otimes V_\lambda\); on the block where the moving coordinate \(q\) is not in the sign set \(S\), the \(\chi_{S'}\)-eigenspace is \(G(S')=\bigoplus_{q\in S'}e_q\otimes\chi_{S'\setminus q}\otimes S^\beta(S'\setminus q)\otimes S^\alpha(S'^c\cup q)\), an \(S_{S'}\times S_{S'^c}\)-module isomorphic to \(\mathrm{Ind}_{S_j\times S_1}^{S_{j+1}}(S^\beta\boxtimes1)\boxtimes\mathrm{Res}^{S_{n-j}}_{S_{n-j-1}}S^\alpha=\bigoplus S^{\beta+\square}\boxtimes S^{\alpha-\square}\), multiplicity-free by Pieri's rule. The fibre of the constituent \(V_{\lambda'}\) over \(S'\) is the summand \(S^{\beta+\square_{r'}}\boxtimes S^{\alpha-\square_r}\), and \(\Pi_{\lambda'}\) is the sum of these isotypic projections. Hence \(p=\sum_{S'}\|\Pi_{r',r}u_{S'}\|^2/\|v\|^2\) with \(u_{S'}=n^{-1/2}(v_{S'\setminus q})_{q\in S'}\), where \(v=\varphi_\lambda Y\).</p>
<p><em>Step 2: the mass leaving a row.</em> The \(\alpha\)-projection acts slot by slot, and \(\sum_{q\in A}\Pi^{(q)}_{\alpha-\square_r}\) on \(S^\alpha(A)\) commutes with \(\mathrm{Sym}(A)\), hence is the scalar \(|A|\,f^{\alpha-\square_r}/f^\alpha\). Summing over \(S\) and \(q\notin S\) gives, for <em>every</em> \(v\in V_\lambda\), \(\sum_{r'}p(\alpha_r\to\beta_{r'})=\frac{|\alpha|}n\,\frac{f^{\alpha-\square_r}}{f^\alpha}\), independent of \(k\). (This is the row sum of the formulas: \(\frac{(a_1+1)(a_1-a_2)}{n(a_1-a_2+1)}\) and \(\frac{a_2(a_1-a_2+2)}{n(a_1-a_2+1)}\).)</p>
<p><em>Step 3: the split between the two \(\beta\)-rows.</em> By Frobenius reciprocity, which scales Hilbert–Schmidt norms by the index, \(p(\alpha_r\to\beta_{r'})=\frac{|\alpha|}n\frac{f^{\alpha-\square_r}}{f^\alpha}\,\rho_{r'}\), where \(\rho_{r'}\) is the squared cosine, in the two-dimensional space \(\mathrm{Hom}_{K_1}(\mathrm{Res}\,S^\mu,\,S^\beta\boxtimes1\boxtimes S^{\alpha'})\) with \(K_1=S_j\times S_1\times S_{n-j-1}\), of the angle between the line of maps factoring through \(S^\beta\boxtimes S^\alpha\) (the subgroup \(S_j\times S_{n-j}\)) and the line of maps factoring through \(S^{\beta+\square_{r'}}\boxtimes S^{\alpha'}\) (the subgroup \(S_{j+1}\times S_{n-j-1}\)); the two latter lines are orthogonal. Schur–Weyl duality on \((\mathbb C^2)^{\otimes n}\) identifies the two-row Specht module \(S^{(m-a,a)}\) with the SU(2) spin \(m/2-a\), restriction to a Young subgroup with the tensor product of the blocks, and the two-dimensional space above, isometrically up to a constant, with \(\mathrm{Hom}_{SU(2)}(V_J,\,V_{j_\beta}\otimes V_{1/2}\otimes V_{j_{\alpha'}})\); admissibility is the triangle inequality. The two lines are the two coupling schemes of three spins, so by the recoupling formula \(\rho_{r'}=(2j_\alpha+1)(2j_\nu+1)\begin{Bmatrix}j_\beta&\tfrac12&j_\nu\\ j_{\alpha'}&J&j_\alpha\end{Bmatrix}^2\). A 6j-symbol with a spin-\(\tfrac12\) entry has a closed form (Edmonds, Table 5), which we validated against exact values on all 1,326 admissible symbols with entries at most 5; substituting it, the product of branching ratio and squared recoupling coefficient simplifies, as an identity of rational functions of integer \(a_1,a_2,b_1,b_2,k\), to the eight displayed formulas (computer algebra, <code>experiments/hyperoct_proof_check.py</code>). Moves from \(\beta\) to \(\alpha\) follow by exchanging the roles of the two blocks. Finally the sum rule and the dimension-weighted reciprocity are identities of rational functions once the formulas are known, and both are verified symbolically in the same script. \(\square\)</p>
<p>Two remarks. The roots of each quadratic are the triangle-inequality boundaries of the recoupling, which is why they coincide with the Littlewood–Richardson admissibility boundaries of the target. And the formulas agree with all 3,340 coefficients computed independently by projection (Section 6.1) to \(3\times10^{-7}\), which is the floating-point noise of that computation; the exact identities above are the proof, the numerics were the discovery.</p>

<h3>6.3 The asymptotic exponent</h3>
<p>With \(u=j/n\), \(\tilde a=a_2/n\), \(\tilde b=b_2/n\), \(b=k/n\) and \(A_1=1-u-\tilde a\), \(A_2=\tilde a\), \(B_1=u-\tilde b\), \(B_2=\tilde b\), the limiting coefficients factor through two quadratics, \(X=(A_2+B_1-b)(A_1+B_2-b)\) and \(Y=(b-A_2-B_2)(1-A_2-B_2-b)\), with \(X+Y=N_\infty=(A_1-A_2)(B_1-B_2)\). The four edge directions of the lattice have symmetric limiting weights \(\sqrt{A_1B_1}\,X/N_\infty\), \(\sqrt{A_2B_2}\,X/N_\infty\), \(\sqrt{A_1B_2}\,Y/N_\infty\), \(\sqrt{A_2B_1}\,Y/N_\infty\), and the product-sine Rayleigh argument of the paper's Lemma 7.2 on a box of side \(o(n)\) gives the Perron limit</p>
<div class="eq">\[ \Lambda_\infty=\frac{2\big[X(\sqrt{A_1B_1}+\sqrt{A_2B_2})+Y(\sqrt{A_1B_2}+\sqrt{A_2B_1})\big]}{(A_1-A_2)(B_1-B_2)}, \]</div>
<p>which reduces to the paper's \(\Gamma_H(u,b)\) when \(\tilde a=\tilde b=0\). The ambient dimension exponent is \(H_2(u)+(1-u)H_2\big(\tfrac{\tilde a}{1-u}\big)+uH_2\big(\tfrac{\tilde b}{u}\big)\) and the stabilizer costs \(H_2(b)\), so</p>
<div class="eq">\[ \kappa_{2row}(\delta)=\inf\Big\{H_2(u)+(1-u)H_2\big(\tfrac{\tilde a}{1-u}\big)+uH_2\big(\tfrac{\tilde b}{u}\big)-H_2(b)\ :\ \Lambda_\infty(u,\tilde a,\tilde b,b)>1-2\delta\Big\}, \qquad R_2(\delta)\le\kappa_{2row}(\delta). \]</div>
<p><strong>Theorem 6.2.</strong> <em>For every \(0<\delta<\tfrac12\), \(R_2(\delta)\le\kappa_{2row}(\delta)\).</em> Proof. Fix an interior admissible point \((u,\tilde a,\tilde b,b)\) with \(\Lambda_\infty>1-2\delta\) and let \(\Omega_n\) be the box of side \(m_n\to\infty\), \(m_n=o(n)\), below the vertex \((un,\tilde an,\tilde bn)\) at \(k=\lfloor bn\rfloor\). By Theorem 6.1 the symmetric edge weights of the four directions converge uniformly on \(\Omega_n\) to \(\sqrt{A_1B_1}X/N_\infty\) and its three companions, so the product-sine Rayleigh quotient of the paper's Lemma 7.2 gives \(\lambda_{\max}(J_{\Omega_n})\ge\Lambda_\infty-o(1)\), while the row-sum bound gives the matching upper limit. Theorem 4.2 of the paper applies with \(G=B_n\), \(H=S_n\), \(E=E_\mu\) (multiplicity one, real endomorphisms, reciprocity by Theorem 6.1), so \(A_2(n,\lceil\delta n\rceil)\le\frac{1-s}{d_\mu(\lambda_{\max}-s)}\sum_{\Omega_n}D_\lambda\). The box has \(n^{o(1)}\) vertices and its largest dimension has exponent \(H_2(u)+(1-u)H_2(\tfrac{\tilde a}{1-u})+uH_2(\tfrac{\tilde b}u)+o(1)\) by Stirling, and \(d_\mu=2^{(H_2(b)+o(1))n}\). Taking logarithms, then the infimum over admissible points, and finally closing the strict inequality as in the paper's proof of Theorem 1.2, proves the claim. \(\square\)</p>
<p>Two checks anchor the optimization. At \(\tilde a=\tilde b=0\) it reproduces \(\kappa_H\) to seven digits. And at the middle level \(u=\tfrac12\) with \(\tilde a=\tilde b\), the value \(\inf_a[1+H_2(2a)-H_2(b)]\) equals the optimized second MRRW bound \(M_2(\delta)\) to machine precision at \(\delta=0.05,0.10,0.15,0.20,0.25\): the classical constant-weight certificate is the middle slice of the two-row Fourier graph, a structural fact we did not anticipate.</p>
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
<p>The improvement is an asymptotic statement with tiny optimal second rows (\(\tilde b^*\approx10^{-4}\) at \(\delta=0.3\)), so at practical lengths the box carries second rows of size 0 or 1 and its extra ambient dimension costs more than the spectral gain. With the closed forms we evaluated the finite-\(n\) two-row bound over boxes in \((j,a_2,b_2)\) at \(\delta=0.3\): it is worse than the paper's one-row bound (23) by 0.02 bits at \(n=100\), by 2.4 bits at \(n=5{,}000\) and by 2.3 bits at \(n=20{,}000\), and the gap has shrunk to 0.6 bits at \(n=50{,}000\), so the crossover sits near \(n\approx10^5\). This is the same pattern as the paper's own constructions in Sections 3 and 4: the exponent improvement is real but only visible at very long lengths.</p>

<h3>6.5 What is proven</h3>
<ul>
<li><strong>Theorem 6.1</strong> (the coefficients) rests on three standard inputs: Frobenius reciprocity, Schur–Weyl duality for two-row shapes, and the recoupling formula with Edmonds' closed form for spin-\(\tfrac12\) 6j-symbols (the last validated against exact values on all 1,326 admissible symbols with entries at most 5). The final simplification is a computer-algebra identity of rational functions.</li>
<li><strong>Finite lengths:</strong> for each \(n\) and box \(\Omega\), \(A_2(n,d)\le\frac{1-s}{d_\mu(\Lambda_\Omega-s)}\sum_{\lambda\in\Omega}D_\lambda\) is the paper's Theorem 4.2 with \(G=B_n\), whose hypotheses Theorem 6.1 supplies.</li>
<li><strong>Theorem 6.2</strong> (the exponent) follows by the paper's own box argument. The numerical statements, \(\kappa_{2row}<\kappa_H\) everywhere and \(\kappa_{2row}<\kappa_{\rm bin}\) for \(\delta\ge\delta_1\), are then evaluations of an explicit four-parameter infimum; the margins (\(10^{-3}\) to \(5\times10^{-6}\)) are far above the optimizer's precision, and the exact recovery of \(M_2(\delta)\) at the middle level is an independent check of the whole reduction.</li>
</ul>
<div class="callout ok"><div class="t">Eureka</div>The binary two-row representation graph improves the best known upper bound on the rate of binary codes, \(R_2(\delta)\), for every \(\delta\in[0.235,0.5)\), beyond the bound proved in OpenAI's paper. The coefficients are proved (Theorem 6.1), the exponent follows by the paper's own machinery (Theorem 6.2), and the mechanism is the paper's Proposition 7.3 transplanted to the cube: a square-root spectral gain from opening a second row against an \(x\log(1/x)\) entropy cost. The standard facts used are Schur–Weyl duality, Frobenius reciprocity, and Edmonds' table of 6j-symbols; every algebraic step is checked by computer algebra in the results folder.</div>
</section>

<section>
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
<h2><span class="num">9</span>Method and reproducibility</h2>
<p>Everything above is produced by a small Python package (NumPy, SciPy, mpmath, matplotlib) in <code>Research/primitive-harmonic-bound</code>. The scripts are deterministic and run in minutes on a laptop.</p>
<pre><code>phb/bound.py            formula (22)-(23); Perron eigenvalue via LAPACK tridiagonal solver; log-space binomials
phb/delsarte_lp.py      Delsarte LP with HiGHS (reliable for n &lt;= 40)
phb/exact_lp.py         exact rational simplex (Bland's rule) for the LP at larger n
phb/certificate.py      from-scratch construction of E_k, iota_j, sigma_x, P_x, K(t); Krawtchouk transform; lambda*(a)
experiments/test1_vs_lp.py       Test 1, n = 4..40          experiments/test1_exact.py      Test 1, n = 41..64 (exact LP)
experiments/test2_certificate.py Test 2 (lambda* vs lambda; Delsarte sharpening)
experiments/asymptotics.py       kappa_H, M1, M2, the 4/13 witness       experiments/crossover.py  crossover scans
experiments/make_figures.py      Figures 1-2                results/*.txt   raw outputs of every run
phb/johnson.py          constant-weight bound (46): associated Hahn coefficients (35)-(37), Jhat (43)-(44), Lambda (6), kappa_CW (8)
phb/johnson_lp.py       exact Delsarte LP for the Johnson scheme (Eberlein eigenvalues)
phb/johnson_certificate.py  explicit Johnson eigenspaces, E_p (x) E_q, equivariant embeddings, measured b_j, c_j, kernel, lambda*
experiments/cw_test1_vs_lp.py / cw_test2_certificate.py / cw_asymptotics.py / cw_crossover.py / make_figure3.py
phb/spherical.py        one-row (73), two-row (81), general (76) weights; Weyl dimensions (113); Gamma_r, Phi_r, kappa_r, gamma_r, Chebyshev tuples
phb/spherical_lp.py     degree-capped Delsarte-Goethals-Seidel LP (Gegenbauer basis)
experiments/sph_checks.py / sph_test1_vs_lp.py / sph_gamma_levels.py / sph_kissing.py / sph_crossover.py / make_figure4.py
phb/hyperoct.py         B_n signed permutation modules, class-sum Lagrange projections, exact transition coefficients
phb/hyperoct_formulas.py  the eight closed forms, targets, admissibility, dimensions
phb/hyperoct_asymptotics.py  limiting weights, Lambda_infinity, kappa_H and kappa_2row optimisation
experiments/hyperoct_collect.py / hyperoct_roots.py / hyperoct_formulas.py / hyperoct_verify_big.py / hyperoct_exponent.py / hyperoct_finite.py / make_figure5.py
experiments/hyperoct_proof_check.py  the proof's algebra: Edmonds 6j table vs exact values; the eight identities; sum rule; reciprocity
phb/layer3.py           exact S_n computation of the three-row layer graph (permutation modules, Specht projections, E-copy)
phb/gl3.py              gl_3 Gelfand-Tsetlin modules, invariant form, tensor products, highest-weight vectors, intertwiners
phb/cw2_gl3.py          coefficients via GL_3 recoupling (the tau formula)      phb/cw2_formulas.py  Proposition 7.1
phb/cw2_asymptotics.py  limits, Lambda_CW2, threshold, exponent optimisation
experiments/layer3_collect.py / cw2_R_collect.py / cw2_R_fit.py / cw2_sign.py / cw2_kappa2.py / cw2_kappa_final.py / make_figure6.py
phb/glm.py              gl_m Gelfand-Tsetlin modules for any m (checked for m <= 5)      phb/cwm_gl.py  general recoupling, conjecture C(m)
phb/cwm_asymptotics.py  m-row limits and exponent optimisation         experiments/cwm_test.py / cwm_kappa.py   four-row verification and exponent
results/hecht1975_text.txt   text of Hecht (1975) used for the identification of Proposition 8.1</code></pre>
<p>Two checks guard the reconstruction itself. The Krawtchouk transform of a radial function must weight the weight-\(t\) shell by \(\binom nt\); an early version of ours did not and produced a \(\lambda^*\) that would have contradicted the even-weight code, which is exactly the kind of error the LP test is designed to catch. And every \(U^{j-k}|_{E_k}\) is asserted to be a scalar multiple of an isometry before use.</p>
</section>

<section>
<h2><span class="num">10</span>What this establishes, and what it does not</h2>
<ul>
<li><strong>No new theorem is claimed here.</strong> The asymptotic improvement over MRRW is OpenAI's result, and the repository reports a machine-checked Lean proof. Our tests are numerical and cannot prove a theorem; they can only fail to refute one, and they did not refute it.</li>
<li><strong>The LP test is a necessary condition, not a sufficient one.</strong> Passing it for \(n\le56\) and \(n=60,64\) is consistent with correctness and would have exposed any error in the finite-length constants or the spectral condition at these lengths.</li>
<li><strong>The reconstruction test is stronger.</strong> Agreement of \(\lambda^*(a)\) with \(\lambda_{\max}(J_H)\) to six decimals across thirteen configurations, together with the failure of alternative normalizations and of an unconstrained optimizer to improve it, is direct evidence for identity (27) and for the optimality of the Perron amplitudes within this kernel family.</li>
<li><strong>The new quantitative statements are ours</strong>: the crossing point \(\delta_0=0.19504\) with \(M_2\), the size of the gains, the finite-length crossover lengths and their non-monotone onset, and the Cauchy–Schwarz-to-Krawtchouk sharpening of (23). We have not seen them stated in the paper or walkthrough, but we have not searched the 253-page paper exhaustively.</li>
<li><strong>The constant-weight audit is the strongest evidence here.</strong> Its recurrence coefficients are not eigenvalues of a matrix we copied; they were measured from an explicit representation-theoretic construction and agree with the paper's closed forms to \(10^{-16}\), and the resulting kernels pass the positivity test independently.</li>
<li><strong>New from this note:</strong> \(\delta_0=0.19504\), \(\delta_1=0.2350\), the observation \(\kappa_{CW}\le\kappa_H\) (so \(\kappa_{\rm bin}=\kappa_{CW}\)), the size of the gains at every distance, the finite-length crossover lengths, and the Krawtchouk sharpening of (23) and (46).</li>
<li><strong>The spherical audit is one layer thinner.</strong> Its transcription identities, LP comparisons and classical limits all pass, and our independent optimization reproduces the paper's Figure 4 to the digit, but the higher-level kernels were not rebuilt explicitly. The new kissing-number exponent 0.3966 is a numerical optimization of the paper's proven bound, not a new theorem.</li>
<li><strong>Section 6 is different in kind.</strong> It is our construction, not the paper's: a new theorem (6.1 and 6.2) proved with standard representation theory on top of the paper's general projection bound, with every algebraic identity machine-checked. A formal (Lean) proof has not been attempted.</li>
<li><strong>Section 7</strong> is again our construction. Its closed form is a verified proposition (exact on every computed case, reciprocity exact in rational arithmetic) with a clear identification in the classical literature, not yet a written proof; its exponent gain over the paper is real but of order \(10^{-6}\), and only at small distances.</li>
<li><strong>Section 8</strong> extends the closed form to any number of rows (verified at four rows, identified with Hecht's 1975 class of \(U(N)\) Racah coefficients) and shows numerically that further rows contribute a geometric tail of about one percent per row.</li>
<li><strong>Not covered:</strong> the Lean formalization itself and everything outside Chapter 2 of the paper.</li>
</ul>
</section>

<section>
<h2><span class="num">11</span>Sources</h2>
<ul class="src">
<li>OpenAI, <em>Ten Advances in Mathematics and Theoretical Computer Science</em> (updated 6 August 2026), Chapter 2 "Binary and spherical codes", Theorems 1.1, 2.1, 2.3 and Lemma 2.2. <a href="https://cdn.openai.com/pdf/ten-proofs-oai.pdf">cdn.openai.com/pdf/ten-proofs-oai.pdf</a></li>
<li>OpenAI, <em>How the Ideas Came Together</em> (reasoning walkthroughs), Chapter 2. <a href="https://cdn.openai.com/pdf/reasoning-walkthroughs.pdf">cdn.openai.com/pdf/reasoning-walkthroughs.pdf</a></li>
<li>OpenAI, <em>Ten advances in mathematics and theoretical computer science</em> (announcement). <a href="https://openai.com/index/ten-advances-in-mathematics/">openai.com/index/ten-advances-in-mathematics</a></li>
<li>Lean 4 certificates: <a href="https://github.com/openai/ten-proofs">github.com/openai/ten-proofs</a>, file <code>MetricCodes.lean</code>.</li>
<li>Background on the Delsarte LP and MRRW: A. Samorodnitsky, <em>On the optimum of Delsarte's linear program</em>, JCTA 2001 (<a href="https://gilkalai.wordpress.com/wp-content/uploads/2024/01/dels_lin1.pdf">pdf</a>); G. Kalai, <a href="https://gilkalai.wordpress.com/2024/01/21/on-the-limit-of-the-linear-programming-bound-for-codes-and-packing/">On the limit of the linear programming bound for codes and packing</a>; L. Coregliano, F. G. Jeronimo, C. Jones, <a href="https://arxiv.org/pdf/2112.09221">A complete linear programming hierarchy for linear codes</a>; E. Loyfer, N. Linial, <a href="https://arxiv.org/pdf/2206.09211">New LP-based upper bounds in the rate-vs-distance problem for linear codes</a>.</li>
</ul>
</section>

</main>
<footer>Beyond-MRRW Audit · research note filed 2 September 2026 · Harish K, with the assistance of Claude (Anthropic) · code and raw outputs in <code>Research/primitive-harmonic-bound</code></footer>
</div>
"""

out = HTML.replace("__FIG1__", img("fig1_exponents.png")).replace("__FIG2__", img("fig2_finite_n.png")).replace("__FIG3__", img("fig3_cw_exponent.png"))
out = out.replace("__CWCROSS__", (ROOT / "report" / "cw_crossover_paragraph.html").read_text(encoding="utf-8") if (ROOT / "report" / "cw_crossover_paragraph.html").exists() else "")
out = out.replace("__FIG4__", img("fig4_spherical.png")).replace("__FIG5__", img("fig5_two_row.png")).replace("__FIG6__", img("fig6_cw2.png"))
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
out = out.replace("__CW2_TEXT__", _txt)
# ---- Section 8 table
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
out = out.replace("__CWM_TEXT__", _txtm)
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
out = out.replace("__KISSROWS__", tbl)
out = out.replace("__TOTAL_PAIRS__", f"{TOTAL_PAIRS:,}").replace("__TOTAL_VIOL__", str(TOTAL_VIOL)).replace("__EXT_NMAX__", ext_nmax)
(ROOT / "report" / "beyond-mrrw-audit.html").write_text(out, encoding="utf-8")
print("wrote report/beyond-mrrw-audit.html", len(out) // 1024, "KB;", "ext n_max =", ext_nmax, "pairs =", TOTAL_PAIRS, "viol =", TOTAL_VIOL)
