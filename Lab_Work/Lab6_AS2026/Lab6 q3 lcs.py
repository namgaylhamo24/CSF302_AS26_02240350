"""Lab 6 - Q3: Longest common subsequence.

Usage
  python lab6_q3_lcs.py                         -> all experiments (uses sample_old.txt / sample_new.txt)
  python lab6_q3_lcs.py diff FILE1 FILE2        -> line-by-line diff of two text files
"""
import json
import os
import random
import sys
import time

SAMPLE_OLD = """Meeting agenda - algorithms study group
1. Welcome and attendance
2. Review of Lab 5 results
3. Quicksort worst cases
4. Counting sort and radix sort
5. Inversions and Kendall tau
6. Plan for Lab 6
7. Any other business
Next meeting: Thursday
"""
SAMPLE_NEW = """Meeting agenda - algorithms study group
1. Welcome and attendance
2. Review of Lab 5 results
3. Quicksort worst cases
4. Counting sort and radix sort
5. Dynamic programming: rod cutting
6. Dynamic programming: matrix chain
7. Plan for Lab 6
8. Any other business
Next meeting: Friday
"""


# ------------------------------------------------------------------ 1. table
def lcs_table(X, Y):
    m, n = len(X), len(Y)
    c = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
            else:
                c[i][j] = max(c[i - 1][j], c[i][j - 1])
    return c


def print_table(X, Y, c):
    print("      " + "".join(f"{ch:>3}" for ch in ["-"] + list(Y)))
    for i in range(len(X) + 1):
        lab = "-" if i == 0 else X[i - 1]
        print(f"  {lab:>2}  " + "".join(f"{v:>3}" for v in c[i]))


# ------------------------------------------------------------------ 2. reconstruct
def reconstruct(X, Y, c):
    i, j, out = len(X), len(Y), []
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            out.append(X[i - 1]); i -= 1; j -= 1
        elif c[i - 1][j] >= c[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))


# ------------------------------------------------------------------ 3. two rows
def lcs_length_two_rows(X, Y):
    if len(Y) > len(X):          # keep the rows as short as possible: min(m, n) + 1
        X, Y = Y, X
    prev = [0] * (len(Y) + 1)
    cur = [0] * (len(Y) + 1)
    for i in range(1, len(X) + 1):
        for j in range(1, len(Y) + 1):
            if X[i - 1] == Y[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = cur[j - 1] if cur[j - 1] > prev[j] else prev[j]
        prev, cur = cur, prev
    return prev[len(Y)]


# ------------------------------------------------------------------ 4. brute force
def is_subsequence(sub, Y):
    it = iter(Y)
    return all(ch in it for ch in sub)


def lcs_brute(X, Y):
    """Try every subsequence of X (2^|X| of them) and keep the longest one that is also in Y."""
    n = len(X)
    best = ""
    for mask in range(1 << n):
        sub = "".join(X[i] for i in range(n) if (mask >> i) & 1)
        if len(sub) > len(best) and is_subsequence(sub, Y):
            best = sub
    return best


# ------------------------------------------------------------------ 5. diff
def diff_lines(a, b):
    """LCS-based diff.  Returns a list of (op, line), op in {' ', '-', '+'}."""
    m, n = len(a), len(b)
    c = [[0] * (n + 1) for _ in range(m + 1)]       # c[i][j] = LCS of a[i:], b[j:]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if a[i] == b[j]:
                c[i][j] = c[i + 1][j + 1] + 1
            else:
                c[i][j] = max(c[i + 1][j], c[i][j + 1])
    out, i, j = [], 0, 0
    while i < m and j < n:
        if a[i] == b[j]:
            out.append((" ", a[i])); i += 1; j += 1
        elif c[i + 1][j] >= c[i][j + 1]:
            out.append(("-", a[i])); i += 1
        else:
            out.append(("+", b[j])); j += 1
    while i < m:
        out.append(("-", a[i])); i += 1
    while j < n:
        out.append(("+", b[j])); j += 1
    return out, c[0][0]


def diff_files(f1, f2, show=True):
    a = open(f1, encoding="utf-8").read().splitlines()
    b = open(f2, encoding="utf-8").read().splitlines()
    ops, L = diff_lines(a, b)
    assert [x for o, x in ops if o != "+"] == a, "diff does not rebuild the old file"
    assert [x for o, x in ops if o != "-"] == b, "diff does not rebuild the new file"
    if show:
        for o, x in ops:
            print(f"{o} {x}")
    return {"old_lines": len(a), "new_lines": len(b), "unchanged": L,
            "removed": len(a) - L, "added": len(b) - L}


def main():
    # Work in the folder that contains this script, so the sample files are found (and the
    # result files are written) no matter which folder the script was started from.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for name, text in (("sample_old.txt", SAMPLE_OLD), ("sample_new.txt", SAMPLE_NEW)):
        if not os.path.exists(name):          # recreate the sample files if they are missing
            with open(name, "w", encoding="utf-8") as f:
                f.write(text)

    X, Y = "ABCBDAB", "BDCABA"
    print(f"X = {X}, Y = {Y}\n\nLCS table c[i][j] (rows: prefixes of X, columns: prefixes of Y)")
    c = lcs_table(X, Y)
    print_table(X, Y, c)
    lcs = reconstruct(X, Y, c)
    print(f"\nLCS length = {c[len(X)][len(Y)]}, one LCS = {lcs}")
    assert is_subsequence(lcs, X) and is_subsequence(lcs, Y) and len(lcs) == c[-1][-1]
    two = lcs_length_two_rows(X, Y)
    print(f"Two-row version returns length {two}")
    assert two == c[-1][-1] == len(lcs_brute(X, Y))

    rng = random.Random(61)
    for _ in range(500):
        a = "".join(rng.choice("ABC") for _ in range(rng.randint(0, 25)))
        b = "".join(rng.choice("ABC") for _ in range(rng.randint(0, 25)))
        t = lcs_table(a, b)
        r = reconstruct(a, b, t)
        assert lcs_length_two_rows(a, b) == t[-1][-1] == len(r)
        assert is_subsequence(r, a) and is_subsequence(r, b)
    print("Checked table / reconstruction / two-row version on 500 random string pairs.")

    # ---- timing, lengths 5..18
    print("\nDP vs brute force (random strings over {A,C,G,T}, mean of 3 pairs)")
    rows = []
    for n in range(5, 19):
        t_dp = t_bf = 0.0
        for _ in range(3):
            a = "".join(rng.choice("ACGT") for _ in range(n))
            b = "".join(rng.choice("ACGT") for _ in range(n))
            reps = 200
            t0 = time.perf_counter()
            for _ in range(reps):
                tt = lcs_table(a, b)
            t_dp += (time.perf_counter() - t0) / reps
            t0 = time.perf_counter()
            bf = lcs_brute(a, b)
            t_bf += time.perf_counter() - t0
            assert len(bf) == tt[-1][-1] and is_subsequence(bf, b)
        rows.append({"n": n, "dp_s": t_dp / 3, "brute_s": t_bf / 3})
        print(rows[-1], flush=True)

    # ---- diff
    print("\nDiff of sample_old.txt and sample_new.txt  (' ' unchanged, '-' removed, '+' added)\n")
    stats = diff_files("sample_old.txt", "sample_new.txt")
    print("\n", stats)

    json.dump({"timing": rows, "diff": stats}, open("q3_results.json", "w"), indent=1)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.plot([r["n"] for r in rows], [r["brute_s"] for r in rows], "o-", label="Brute force  O(2^n · n)")
    ax.plot([r["n"] for r in rows], [r["dp_s"] for r in rows], "s-", label="DP table  O(n²)")
    ax.set_yscale("log"); ax.set_xlabel("string length n (both strings)"); ax.set_ylabel("time (s)")
    ax.set_title("Q3: LCS, DP vs brute force"); ax.grid(True, which="both", alpha=.3); ax.legend()
    fig.tight_layout(); fig.savefig("q3_lcs_timing.png", dpi=150)


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "diff":
        diff_files(sys.argv[2], sys.argv[3])
    else:
        main()