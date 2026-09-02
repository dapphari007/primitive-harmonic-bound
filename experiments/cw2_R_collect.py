"""Collect the squared GL_3 recoupling overlaps R_t(lambda, nu)^2 on a grid of generic interior points,
for closed-form mining.  Output: results/cw2_R_data.jsonl with rows [l1, l2, l3, W, p, r, t, R, R^2]."""
import sys, json, time, itertools
sys.path.insert(0, ".")
from phb.cw2_gl3 import R_overlap

def R(lam, r, w, p, t):
    n = sum(lam); N = n - w
    nu = list(lam); nu[r - 1] -= 1
    eps = (w - p, p); eps_t = list(eps); eps_t[t - 1] -= 1
    if eps_t[0] < eps_t[1] or eps_t[1] < 0 or nu[0] < nu[1] or nu[1] < nu[2] or nu[2] < 0:
        return None
    try:
        return R_overlap(tuple(lam), tuple(nu), eps, tuple(eps_t), N)
    except AssertionError:
        return None

out = open("results/cw2_R_data.jsonl", "w")
t0 = time.time(); cnt = 0
L3 = range(0, 3)
for l3 in L3:
    for p in range(l3 + 1, l3 + 4):
        for l2 in range(p + 1, p + 4):
            for W in range(l2 + 1, l2 + 4):
                for l1 in range(W + 1, W + 5):
                    lam = (l1, l2, l3); w = W + p
                    for r in (1, 2, 3):
                        for t in (1, 2):
                            v = R(lam, r, w, p, t)
                            if v is None:
                                continue
                            out.write(json.dumps([l1, l2, l3, W, p, r, t, v, v * v]) + "\n"); cnt += 1
                    out.flush()
    print(f"l3={l3} done, {cnt} rows, {time.time()-t0:.0f}s", flush=True)
out.close()
print("done", cnt, f"{time.time()-t0:.0f}s")
