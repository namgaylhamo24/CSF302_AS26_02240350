import json
import sys
import time

sys.setrecursionlimit(10000)

BASE = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]  # p[0] = 0 is a dummy


def price_table(n):
    p = BASE[:]
    for i in range(11, n + 1):
        p.append(3 * i)
    return p[: n + 1]


# ------------------------------------------------------------------ 1. naive
def rod_naive(p, n, cnt):
    cnt[0] += 1
    if n == 0:
        return 0
    q = -1
    for i in range(1, n + 1):
        v = p[i] + rod_naive(p, n - i, cnt)
        if v > q:
            q = v
    return q


# ------------------------------------------------------------------ 2. memoised
def rod_memo(p, n, cnt):
    r = [-1] * (n + 1)
    s = [0] * (n + 1)

    def rec(m):
        cnt[0] += 1
        if r[m] >= 0:
            return r[m]
        if m == 0:
            q = 0
        else:
            q = -1
            for i in range(1, m + 1):
                v = p[i] + rec(m - i)
                if v > q:          # strict '>' : the smallest first piece wins ties
                    q = v
                    s[m] = i
        r[m] = q
        return q

    rec(n)
    return r[n], s


# ------------------------------------------------------------------ 3. bottom-up
def rod_bottom_up(p, n, cnt=None):
    r = [0] * (n + 1)
    s = [0] * (n + 1)
    for j in range(1, n + 1):
        q = -1
        for i in range(1, j + 1):
            if cnt is not None:
                cnt[0] += 1
            v = p[i] + r[j - i]
            if v > q:
                q = v
                s[j] = i
        r[j] = q
    return r[n], s


def pieces(s, n):
    out = []
    while n > 0:
        out.append(s[n])
        n -= s[n]
    return out


def time_it(f, reps):
    t0 = time.perf_counter()
    for _ in range(reps):
        f()
    return (time.perf_counter() - t0) / reps


def main():
    # ---- part 4: revenue and pieces for n = 1..10
    p10 = price_table(10)
    print("Price table  length:", list(range(1, 11)))
    print("             price :", p10[1:])
    print("\n n | max revenue | pieces")
    print("---+-------------+----------------")
    table10 = []
    for n in range(1, 11):
        rv, s = rod_bottom_up(p10, n)
        rv_m, s_m = rod_memo(p10, n, [0])
        rv_n = rod_naive(p10, n, [0])
        assert rv == rv_m == rv_n, "versions disagree"
        assert pieces(s, n) == pieces(s_m, n)
        assert sum(pieces(s, n)) == n and sum(p10[x] for x in pieces(s, n)) == rv
        print(f"{n:2d} | {rv:11d} | {pieces(s, n)}")
        table10.append({"n": n, "revenue": rv, "pieces": pieces(s, n)})

    # ---- part 5: counts and time for n = 5, 10, 15, 20, 25
    print("\nCall counts and times (p[i] = 3*i for i > 10)")
    reps_naive = {5: 2000, 10: 200, 15: 10, 20: 2, 25: 1}
    rows = []
    for n in [5, 10, 15, 20, 25]:
        p = price_table(n)
        c_naive, c_memo, c_bu = [0], [0], [0]
        rv_n = rod_naive(p, n, c_naive)
        rv_m, s_m = rod_memo(p, n, c_memo)
        rv_b, s_b = rod_bottom_up(p, n, c_bu)
        assert rv_n == rv_m == rv_b
        t_naive = time_it(lambda: rod_naive(p, n, [0]), reps_naive[n])
        t_memo = time_it(lambda: rod_memo(p, n, [0]), 2000)
        t_bu = time_it(lambda: rod_bottom_up(p, n), 2000)
        row = {"n": n, "revenue": rv_n, "pieces": pieces(s_b, n),
               "calls_naive": c_naive[0], "calls_memo": c_memo[0],
               "evals_bottom_up": c_bu[0],
               "t_naive": t_naive, "t_memo": t_memo, "t_bottom_up": t_bu}
        rows.append(row)
        print(row, flush=True)
        assert c_naive[0] == 2 ** n
        assert c_memo[0] == n * (n + 1) // 2 + 1
        assert c_bu[0] == n * (n + 1) // 2

    json.dump({"table10": table10, "experiment": rows}, open("q1_results.json", "w"), indent=1)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ns = [r["n"] for r in rows]
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot(ns, [r["calls_naive"] for r in rows], "o-", label="Naive  (2^n)")
    ax[0].plot(ns, [r["calls_memo"] for r in rows], "s-", label="Memoised  (n(n+1)/2 + 1)")
    ax[0].plot(ns, [r["evals_bottom_up"] for r in rows], "^--", label="Bottom-up evaluations  (n(n+1)/2)")
    ax[0].set_yscale("log"); ax[0].set_xlabel("n"); ax[0].set_ylabel("recursive calls / evaluations")
    ax[0].set_title("Q1: work done"); ax[0].grid(True, which="both", alpha=.3); ax[0].legend(fontsize=8)
    ax[1].plot(ns, [r["t_naive"] for r in rows], "o-", label="Naive")
    ax[1].plot(ns, [r["t_memo"] for r in rows], "s-", label="Memoised")
    ax[1].plot(ns, [r["t_bottom_up"] for r in rows], "^-", label="Bottom-up")
    ax[1].set_yscale("log"); ax[1].set_xlabel("n"); ax[1].set_ylabel("time (s)")
    ax[1].set_title("Q1: running time"); ax[1].grid(True, which="both", alpha=.3); ax[1].legend()
    fig.tight_layout(); fig.savefig("q1_rod_cutting.png", dpi=150)


if __name__ == "__main__":
    main()