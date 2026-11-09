import csv
import json
import random
import sys
import time

random.seed(12345)


# ---------------------------------------------------------------- partitions
def lomuto(a, lo, hi, c):
    p = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= p:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    c[0] += hi - lo  # exactly one comparison per element in lo..hi-1
    return i + 1


def hoare(a, lo, hi, c):
    p = a[lo]
    i, j = lo - 1, hi + 1
    n = 0
    while True:
        i += 1
        n += 1
        while a[i] < p:
            i += 1
            n += 1
        j -= 1
        n += 1
        while a[j] > p:
            j -= 1
            n += 1
        if i >= j:
            c[0] += n
            return j
        a[i], a[j] = a[j], a[i]


def three_way(a, lo, hi, c):
    """Dutch national flag. Returns (lt, gt): a[lo:lt] < p, a[lt..gt] == p, a[gt+1:hi+1] > p."""
    p = a[hi]
    lt, i, gt = lo, lo, hi
    n = 0
    while i <= gt:
        x = a[i]
        n += 1
        if x < p:
            a[lt], a[i] = x, a[lt]
            lt += 1
            i += 1
        else:
            n += 1
            if x > p:
                a[i], a[gt] = a[gt], x
                gt -= 1
            else:
                i += 1
    c[0] += n
    return lt, gt


# ---------------------------------------------------------------- sorts
def qs_lomuto(a, lo, hi, c):
    while lo < hi:
        m = lomuto(a, lo, hi, c)
        if m - lo < hi - m:
            qs_lomuto(a, lo, m - 1, c)
            lo = m + 1
        else:
            qs_lomuto(a, m + 1, hi, c)
            hi = m - 1


def qs_hoare(a, lo, hi, c):
    while lo < hi:
        m = hoare(a, lo, hi, c)  # parts: lo..m and m+1..hi
        if m - lo + 1 < hi - m:
            qs_hoare(a, lo, m, c)
            lo = m + 1
        else:
            qs_hoare(a, m + 1, hi, c)
            hi = m


def qs_random(a, lo, hi, c):
    while lo < hi:
        r = random.randint(lo, hi)
        a[r], a[hi] = a[hi], a[r]
        m = lomuto(a, lo, hi, c)
        if m - lo < hi - m:
            qs_random(a, lo, m - 1, c)
            lo = m + 1
        else:
            qs_random(a, m + 1, hi, c)
            hi = m - 1


def qs_three_way(a, lo, hi, c):
    while lo < hi:
        lt, gt = three_way(a, lo, hi, c)
        if lt - lo < hi - gt:
            qs_three_way(a, lo, lt - 1, c)
            lo = gt + 1
        else:
            qs_three_way(a, gt + 1, hi, c)
            hi = lt - 1


VARIANTS = {
    "Lomuto (last pivot)": qs_lomuto,
    "Hoare (first pivot)": qs_hoare,
    "Randomised": qs_random,
    "Three-way (last pivot)": qs_three_way,
}


# ---------------------------------------------------------------- inputs
def make_input(kind, n):
    if kind == "random":
        return [random.randint(0, 10 * n) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "reverse":
        return list(range(n, 0, -1))
    if kind == "duplicates":
        return [random.randint(0, 9) for _ in range(n)]
    raise ValueError(kind)


KINDS = ["random", "sorted", "reverse", "duplicates"]
SIZES = [1000, 2000, 4000, 8000, 16000]


def run(sort, data):
    a = data[:]
    c = [0]
    t0 = time.perf_counter()
    sort(a, 0, len(a) - 1, c)
    t = time.perf_counter() - t0
    assert a == sorted(data), "sort produced a wrong result"
    return c[0], t


def main():
    rows = []
    for kind in KINDS:
        for n in SIZES:
            data = make_input(kind, n)
            for name, sort in VARIANTS.items():
                reps = 3 if n <= 4000 else 1
                best_t, comps = None, None
                for _ in range(reps):
                    comps, t = run(sort, data)
                    best_t = t if best_t is None else min(best_t, t)
                rows.append({"input": kind, "n": n, "variant": name,
                             "comparisons": comps, "seconds": round(best_t, 5)})
                print(f"{kind:10s} n={n:6d} {name:24s} comps={comps:12d} t={best_t:9.4f}s",
                      flush=True)
    with open("q1_results.json", "w") as f:
        json.dump(rows, f, indent=1)
    with open("q1_results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()