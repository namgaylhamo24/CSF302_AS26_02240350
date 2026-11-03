"""Timing experiments for closest.py.

Produces: timings.csv, crossover.csv, timing_graph.png
Run:  python benchmark.py
"""

import csv
import random
import statistics
import time

from closest import closest_pair, closest_pair_brute

SIZES = [1000 * 2 ** k for k in range(7)]       # 1,000 ... 64,000
TIME_LIMIT = 60.0                                # seconds, brute force cut-off


def make_points(n, seed):
    rng = random.Random(seed)
    return [(rng.uniform(0, 100000), rng.uniform(0, 100000)) for _ in range(n)]


def time_once(f, pts):
    t0 = time.perf_counter()
    f(pts)
    return time.perf_counter() - t0


def median_time(f, pts, repeats):
    return statistics.median(time_once(f, pts) for _ in range(repeats))


def main():
    rows = []
    brute_stopped = False
    prev_brute = None
    for n in SIZES:
        pts = make_points(n, seed=n)
        dc = median_time(closest_pair, pts, 3)

        brute = None
        note = ""
        # Brute force is Theta(n^2): doubling n multiplies time by ~4.
        # Do not start a run that is predicted to exceed the 60 s limit.
        if brute_stopped or (prev_brute is not None and prev_brute * 4 > TIME_LIMIT):
            brute_stopped = True
            note = "stopped (predicted > 60 s)"
        else:
            brute = median_time(closest_pair_brute, pts, 3 if n <= 4000 else 1)
            prev_brute = brute
            if brute > TIME_LIMIT:
                brute_stopped = True
        rows.append((n, brute, dc, note))
        print(n, brute, dc, note, flush=True)

    with open("timings.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["n", "brute_seconds", "divide_conquer_seconds", "note"])
        for n, b, d, note in rows:
            w.writerow([n, "" if b is None else f"{b:.6f}", f"{d:.6f}", note])

    # ---- crossover search ----
    cross = []
    first_dc_faster = None
    stable_from = None
    for n in list(range(4, 64, 2)) + list(range(64, 400, 4)):
        pts = make_points(n, seed=n)
        reps = 200 if n < 100 else 60
        b = median_time(closest_pair_brute, pts, reps)
        d = median_time(closest_pair, pts, reps)
        cross.append((n, b, d))
        if d < b:
            if first_dc_faster is None:
                first_dc_faster = n
            if stable_from is None:
                stable_from = n
        else:
            stable_from = None
    with open("crossover.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["n", "brute_seconds", "divide_conquer_seconds"])
        for n, b, d in cross:
            w.writerow([n, f"{b:.9f}", f"{d:.9f}"])
    print("first n where D&C faster:", first_dc_faster)
    print("D&C faster for every tested n from:", stable_from)

    # ---- log-log graph ----
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ns = [r[0] for r in rows]
    dcs = [r[2] for r in rows]
    bn = [r[0] for r in rows if r[1] is not None]
    bt = [r[1] for r in rows if r[1] is not None]
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.loglog(bn, bt, "o-", label="Brute force")
    ax.loglog(ns, dcs, "s-", label="Divide and conquer")
    # reference slopes anchored at the first measured point
    ax.loglog(ns, [bt[0] * (n / ns[0]) ** 2 for n in ns], "--", color="grey",
              linewidth=0.8, label=r"reference $n^2$")
    import math
    ax.loglog(ns, [dcs[0] * (n * math.log2(n)) / (ns[0] * math.log2(ns[0])) for n in ns],
              ":", color="grey", linewidth=1.0, label=r"reference $n\log n$")
    ax.set_xlabel("Number of points n")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("Closest pair: running time (log-log)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig("timing_graph.png", dpi=200)


if __name__ == "__main__":
    main()