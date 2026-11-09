import json
import random
import time

random.seed(2026)


# ---------------------------------------------------------------- merge sort (Lab 1 style)
def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out = []
    i = j = 0
    nl, nr = len(left), len(right)
    while i < nl and j < nr:
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


# ---------------------------------------------------------------- counting sort
def counting_sort(a, k, key=None):
    """Stable counting sort of a, whose keys are integers in 0..k.
    key(x) gives the key of element x (default: x itself)."""
    cnt = [0] * (k + 1)
    if key is None:
        for x in a:
            cnt[x] += 1
    else:
        for x in a:
            cnt[key(x)] += 1
    for i in range(1, k + 1):          # cnt[v] = number of elements with key <= v
        cnt[i] += cnt[i - 1]
    out = [None] * len(a)
    for x in reversed(a):              # right-to-left scan => stability
        kx = x if key is None else key(x)
        cnt[kx] -= 1
        out[cnt[kx]] = x
    return out


# ---------------------------------------------------------------- LSD radix sort
def radix_sort(a, base):
    if not a:
        return a
    m = max(a)
    exp = 1
    while m // exp > 0:
        digits = [(x // exp) % base for x in a]
        cnt = [0] * base
        for d in digits:
            cnt[d] += 1
        for i in range(1, base):
            cnt[i] += cnt[i - 1]
        out = [0] * len(a)
        for idx in range(len(a) - 1, -1, -1):   # stable, right-to-left
            d = digits[idx]
            cnt[d] -= 1
            out[cnt[d]] = a[idx]
        a = out
        exp *= base
    return a


def timed(f, *args):
    t0 = time.perf_counter()
    r = f(*args)
    return r, time.perf_counter() - t0


def check(result, data):
    assert result == sorted(data), "wrong result"


def stability_demo():
    n = 20
    pairs = [(random.randint(0, 4), i) for i in range(n)]
    out = counting_sort(pairs, 4, key=lambda p: p[0])
    print("Stability demo (key, original index):")
    print("  input :", pairs)
    print("  output:", out)
    ok = all(not (out[i][0] == out[i + 1][0] and out[i][1] > out[i + 1][1])
             for i in range(n - 1))
    print("  equal keys keep original order:", ok)
    assert ok
    big = [(random.randint(0, 50), i) for i in range(100000)]
    out = counting_sort(big, 50, key=lambda p: p[0])
    ok_big = all(out[i][0] < out[i + 1][0] or
                 (out[i][0] == out[i + 1][0] and out[i][1] < out[i + 1][1])
                 for i in range(len(out) - 1))
    print("  stability check on 100,000 pairs:", ok_big)
    assert ok_big
    return {"small_input": pairs, "small_output": out, "big_ok": ok_big}


def main():
    res = {"stability": stability_demo()}

    # (a) n = 100,000, vary k
    n = 100_000
    exp_k = []
    for k in [10, 10**3, 10**5, 10**7]:
        data = [random.randint(0, k) for _ in range(n)]
        row = {"k": k, "n": n}
        r, row["counting"] = timed(counting_sort, data, k); check(r, data)
        r, row["radix10"] = timed(radix_sort, data, 10); check(r, data)
        r, row["radix256"] = timed(radix_sort, data, 256); check(r, data)
        r, row["merge"] = timed(merge_sort, data); check(r, data)
        exp_k.append(row)
        print(row, flush=True)
    res["vary_k"] = exp_k

    # (b) k = 1e9, vary n
    k = 10**9
    exp_n = []
    for n in [10_000, 20_000, 50_000, 100_000, 200_000, 500_000, 1_000_000]:
        data = [random.randint(0, k) for _ in range(n)]
        row = {"n": n, "k": k}
        r, row["radix10"] = timed(radix_sort, data, 10); check(r, data)
        r, row["radix256"] = timed(radix_sort, data, 256); check(r, data)
        r, row["merge"] = timed(merge_sort, data); check(r, data)
        _, row["builtin_sorted"] = timed(sorted, data)
        exp_n.append(row)
        print(row, flush=True)
    res["vary_n"] = exp_n

    with open("q2_results.json", "w") as f:
        json.dump(res, f, indent=1)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Plot 1: vary k
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ks = [r["k"] for r in exp_k]
    for key, lab, mk in [("counting", "Counting sort", "o"), ("radix10", "Radix (base 10)", "s"),
                         ("radix256", "Radix (base 256)", "^"), ("merge", "Merge sort", "d")]:
        ax.plot(ks, [r[key] for r in exp_k], marker=mk, label=lab)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("range k (n = 100,000)"); ax.set_ylabel("time (s)")
    ax.set_title("Q2: effect of the key range k"); ax.grid(True, which="both", alpha=.3)
    ax.legend(); fig.tight_layout(); fig.savefig("q2_vary_k.png", dpi=150)

    # Plot 2: vary n
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ns = [r["n"] for r in exp_n]
    for key, lab, mk in [("radix10", "Radix (base 10)", "s"), ("radix256", "Radix (base 256)", "^"),
                         ("merge", "Merge sort", "d"), ("builtin_sorted", "Python sorted() (reference)", "x")]:
        ax.plot(ns, [r[key] for r in exp_n], marker=mk, label=lab)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("n (k = 10^9)"); ax.set_ylabel("time (s)")
    ax.set_title("Q2: growth with n for k = 10^9"); ax.grid(True, which="both", alpha=.3)
    ax.legend(); fig.tight_layout(); fig.savefig("q2_vary_n.png", dpi=150)


if __name__ == "__main__":
    main()