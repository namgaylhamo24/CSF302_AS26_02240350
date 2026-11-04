"""Benchmarks for sorts.py (Assignment 3, Part C).

Produces: timings_sorts.csv, basic_deep_recursion.csv, cutoff.csv,
          comparisons.csv, graph_sizes.png, graph_cutoff.png
Run:  python benchmark_sorts.py      (takes a few minutes)
"""

import csv
import random
import statistics
import sys
import time

from sorts import quicksort_basic, quicksort_improved

SIZES = [1000 * 2 ** k for k in range(7)]          # 1,000 ... 64,000
CUTOFFS = [1, 4, 8, 16, 32, 64]
INPUTS = ["random", "sorted", "duplicates"]


def make(kind, n, seed):
    rng = random.Random(seed)
    if kind == "random":
        return [rng.randint(0, 10 ** 9) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "duplicates":
        return [rng.randint(0, 9) for _ in range(n)]
    raise ValueError(kind)


def run(sort, data):
    """Time one sort of a fresh copy. Returns seconds, or 'crash'."""
    a = data[:]
    t0 = time.perf_counter()
    try:
        sort(a)
    except RecursionError:
        return "crash"
    t = time.perf_counter() - t0
    assert a == sorted(data), "sort gave wrong answer"
    return t


def median_run(sort, data, repeats):
    ts = [run(sort, data) for _ in range(repeats)]
    if "crash" in ts:
        return "crash"
    return statistics.median(ts)


def main():
    random.seed(1)

    # ---------- Part C(1): three input types, three methods ----------
    methods = {
        "basic": quicksort_basic,
        "improved": quicksort_improved,           # cutoff = 16
        "sorted()": lambda a: a.sort(),           # timing reference only
    }
    results = {}                                   # (kind, method, n) -> time|'crash'
    for kind in INPUTS:
        for n in SIZES:
            data = make(kind, n, seed=n)
            for name, f in methods.items():
                results[(kind, name, n)] = median_run(f, data, 3)
            print(kind, n, {m: results[(kind, m, n)] for m in methods}, flush=True)

    with open("timings_sorts.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["input", "n", "basic_s", "improved_s", "sorted_s"])
        for kind in INPUTS:
            for n in SIZES:
                row = []
                for m in methods:
                    v = results[(kind, m, n)]
                    row.append(v if v == "crash" else f"{v:.6f}")
                w.writerow([kind, n] + row)

    # ---------- Part C(2): quadratic behaviour of basic with the recursion
    # limit raised, so we can see the T(n) = T(n-1) + Theta(n) growth that the
    # default limit hides behind a crash ----------
    deep_sizes = [1000, 2000, 4000, 8000, 16000]
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(1_000_000)
    deep = []
    for kind in ("sorted", "duplicates", "random"):
        for n in deep_sizes:
            data = make(kind, n, seed=n)
            deep.append((kind, n, median_run(quicksort_basic, data, 1)))
            print("deep", deep[-1], flush=True)
    sys.setrecursionlimit(old)
    with open("basic_deep_recursion.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["input", "n", "basic_seconds_with_raised_limit"])
        for kind, n, t in deep:
            w.writerow([kind, n, f"{t:.6f}"])

    # ---------- Part C(3): cutoff study, n = 100,000 random ----------
    N = 100_000
    data = make("random", N, seed=99)
    cut_rows = []
    for c in CUTOFFS:
        t = median_run(lambda a, c=c: quicksort_improved(a, cutoff=c), data, 5)
        cut_rows.append((c, t))
        print("cutoff", c, t, flush=True)
    t_builtin = median_run(lambda a: a.sort(), data, 5)
    with open("cutoff.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["cutoff", "seconds_n100000_random"])
        for c, t in cut_rows:
            w.writerow([c, f"{t:.6f}"])
        w.writerow(["sorted()", f"{t_builtin:.6f}"])
    best_cut, best_t = min(cut_rows, key=lambda r: r[1])
    print("best cutoff", best_cut, best_t, "sorted()", t_builtin)

    # ---------- Part C(4): algorithm vs language: count comparisons ----------
    class Counted:
        n = 0
        __slots__ = ("v",)

        def __init__(self, v):
            self.v = v

        def __lt__(self, other):
            Counted.n += 1
            return self.v < other.v

        def __gt__(self, other):
            Counted.n += 1
            return self.v > other.v

    base = make("random", N, seed=99)
    objs = [Counted(v) for v in base]
    Counted.n = 0
    sorted(objs)
    cmp_builtin = Counted.n
    objs = [Counted(v) for v in base]
    Counted.n = 0
    quicksort_improved(objs, cutoff=best_cut)
    cmp_improved = Counted.n
    with open("comparisons.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["method", "comparisons_n100000_random"])
        w.writerow(["sorted() (Timsort)", cmp_builtin])
        w.writerow([f"quicksort_improved (cutoff={best_cut})", cmp_improved])
    print("comparisons", cmp_builtin, cmp_improved)

    # ---------- graphs ----------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)
    # fixed colour per method so a panel with no basic points (all crashed)
    # does not shift the colour cycle
    styles = {"basic": ("o-", "Basic", "tab:blue"),
              "improved": ("s-", "Improved (cutoff 16)", "tab:orange"),
              "sorted()": ("^--", "sorted() / list.sort", "tab:green")}
    for ax, kind in zip(axes, INPUTS):
        for m, (fmt, label, colour) in styles.items():
            pts = [(n, results[(kind, m, n)]) for n in SIZES
                   if results[(kind, m, n)] != "crash"]
            if pts:
                ax.loglog([p[0] for p in pts], [p[1] for p in pts], fmt,
                          color=colour, label=label)
        crashed = [n for n in SIZES if results[(kind, "basic", n)] == "crash"]
        if crashed:
            ax.axvline(crashed[0], color="red", linestyle=":", linewidth=1)
            ax.text(crashed[0] * 1.05, 2e-4, f"basic: RecursionError\nfrom n={crashed[0]:,}",
                    color="red", fontsize=8)
        ax.set_title(f"{kind} input")
        ax.set_xlabel("n")
        ax.grid(True, which="both", alpha=0.3)
    axes[0].set_ylabel("Time (seconds)")
    axes[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig("graph_sizes.png", dpi=200)

    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.plot([str(c) for c, _ in cut_rows], [t for _, t in cut_rows], "o-")
    ax.axhline(t_builtin, color="grey", linestyle="--", label="sorted()")
    ax.set_xlabel("cutoff")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("quicksort_improved, n = 100,000 random")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig("graph_cutoff.png", dpi=200)


if __name__ == "__main__":
    main()