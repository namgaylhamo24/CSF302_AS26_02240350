import json
import random
import sys
import time


# ---------------------------------------------------------------- inversion counting
def inversions_brute(a, time_limit=None):
    """Count pairs i < j with a[i] > a[j]. Returns None if time_limit (s) is exceeded."""
    n = len(a)
    total = 0
    t0 = time.perf_counter()
    for i in range(n - 1):
        ai = a[i]
        for j in range(i + 1, n):
            if ai > a[j]:
                total += 1
        if time_limit is not None and (i & 63) == 0 and time.perf_counter() - t0 > time_limit:
            return None
    return total


def _sort_count(a):
    n = len(a)
    if n <= 1:
        return a, 0
    mid = n // 2
    left, x = _sort_count(a[:mid])
    right, y = _sort_count(a[mid:])
    out, i, j, cross = [], 0, 0, 0
    nl, nr = len(left), len(right)
    while i < nl and j < nr:
        if left[i] <= right[j]:            # ties are NOT inversions
            out.append(left[i]); i += 1
        else:                              # left[i..] are all > right[j]
            out.append(right[j]); j += 1
            cross += nl - i
    out.extend(left[i:]); out.extend(right[j:])
    return out, x + y + cross


def inversions_merge(a):
    return _sort_count(a)[1]


# ---------------------------------------------------------------- Kendall tau
def kendall_tau_distance(rank_a, rank_b):
    """rank_a[m], rank_b[m] = position (1 = best) each user gave movie m.
    Relabel the movies in user A's order; the inversions of B's positions
    (listed in that order) = number of movie pairs the two users order differently."""
    order_a = sorted(range(len(rank_a)), key=lambda m: rank_a[m])
    seq = [rank_b[m] for m in order_a]
    return inversions_merge(seq)


def read_ranking(name, n):
    while True:
        raw = input(f"{name}: enter the rank (1..{n}, 1 = favourite) of movie 1..{n}, space separated:\n> ")
        try:
            r = [int(x) for x in raw.split()]
        except ValueError:
            print("  Please enter integers only."); continue
        if sorted(r) != list(range(1, n + 1)):
            print(f"  Each rank 1..{n} must be used exactly once. Try again."); continue
        return r


def kendall_program():
    n = 10
    print("Kendall tau distance between two users' rankings of 10 movies")
    a = read_ranking("User A", n)
    b = read_ranking("User B", n)
    d = kendall_tau_distance(a, b)
    pairs = n * (n - 1) // 2
    print(f"\nKendall tau distance = {d} (out of {pairs} movie pairs)")
    print(f"Normalised distance  = {d / pairs:.3f}  (0 = identical, 1 = opposite)")
    print(f"Similarity           = {1 - d / pairs:.3f}")
    print(f"Kendall tau coefficient = {1 - 2 * d / pairs:.3f}")


# ---------------------------------------------------------------- experiments
def verify():
    random.seed(7)
    trials = 0
    for _ in range(300):
        n = random.randint(0, 2000)
        a = [random.randint(0, 10 * max(n, 1)) for _ in range(n)]
        assert inversions_brute(a) == inversions_merge(a)
        trials += 1
    for _ in range(100):  # arrays with many ties
        n = random.randint(0, 500)
        a = [random.randint(0, 5) for _ in range(n)]
        assert inversions_brute(a) == inversions_merge(a)
        trials += 1
    for n in (2000, 1000):  # extremes
        assert inversions_merge(list(range(n))) == 0
        assert inversions_merge(list(range(n, 0, -1))) == n * (n - 1) // 2
        assert inversions_brute(list(range(n, 0, -1))) == n * (n - 1) // 2
    print(f"Verified brute force == merge-based on {trials} random arrays (sizes up to 2,000) "
          "plus sorted / reverse-sorted extremes.")
    return trials


def timing():
    random.seed(99)
    sizes = [1000, 2000, 5000, 10_000, 20_000, 50_000, 100_000, 200_000,
             500_000, 1_000_000]
    rows, brute_stopped = [], False
    for n in sizes:
        a = [random.randint(0, 10 * n) for _ in range(n)]
        row = {"n": n}
        t0 = time.perf_counter()
        inv_m = inversions_merge(a)
        row["merge_s"] = time.perf_counter() - t0
        row["inversions"] = inv_m
        if not brute_stopped:
            t0 = time.perf_counter()
            inv_b = inversions_brute(a, time_limit=60)
            t = time.perf_counter() - t0
            if inv_b is None:
                row["brute_s"] = None
                row["brute_note"] = f"aborted after {t:.0f} s (> 60 s)"
                brute_stopped = True
            else:
                assert inv_b == inv_m
                row["brute_s"] = t
        else:
            row["brute_s"] = None
            row["brute_note"] = "not run (brute force already exceeded 60 s)"
        rows.append(row)
        print(row, flush=True)
    with open("q3_results.json", "w") as f:
        json.dump({"verified_trials": VERIFIED, "timing": rows}, f, indent=1)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    bn = [r["n"] for r in rows if r["brute_s"] is not None]
    bt = [r["brute_s"] for r in rows if r["brute_s"] is not None]
    ax.plot(bn, bt, "o-", label="Brute force  O(n²)")
    ax.plot([r["n"] for r in rows], [r["merge_s"] for r in rows], "s-", label="Merge-based  O(n log n)")
    ax.axhline(60, color="grey", ls="--", lw=1, label="60 s cut-off")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("n"); ax.set_ylabel("time (s)")
    ax.set_title("Q3: counting inversions"); ax.grid(True, which="both", alpha=.3)
    ax.legend(); fig.tight_layout(); fig.savefig("q3_inversions.png", dpi=150)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "kendall":
        kendall_program()
    else:
        VERIFIED = verify()
        timing()