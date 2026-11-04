"""One-off check: random-pivot Lomuto vs the three-way partition in sorts.py."""
import random, time
from sorts import _insertion_sort, quicksort_improved, _lomuto

def qs(a, lo, hi, cutoff=16):
    while hi - lo + 1 > cutoff:
        k = random.randint(lo, hi); a[k], a[hi] = a[hi], a[k]
        p = _lomuto(a, lo, hi)
        if p - lo < hi - p:
            qs(a, lo, p - 1, cutoff); lo = p + 1
        else:
            qs(a, p + 1, hi, cutoff); hi = p - 1
    _insertion_sort(a, lo, hi)

def t(f, data):
    a = data[:]; t0 = time.perf_counter(); f(a); return time.perf_counter() - t0

for n in (4000, 16000, 64000):
    rng = random.Random(n)
    d = [rng.randint(0, 9) for _ in range(n)]
    r = [rng.randint(0, 10**9) for _ in range(n)]
    print(n, "dups  lomuto+random %.4f  3-way %.4f" % (t(lambda a: qs(a,0,len(a)-1), d), t(quicksort_improved, d)),
             "| random lomuto+random %.4f  3-way %.4f" % (t(lambda a: qs(a,0,len(a)-1), r), t(quicksort_improved, r)), flush=True)