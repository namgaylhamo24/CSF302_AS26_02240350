"""Quicksort variants for the Thimphu transaction-sorting problem.

Both functions sort a list of integers IN PLACE into ascending order and
return None (like list.sort). Neither uses sorted() or list.sort().
"""

import random


# --------------------------------------------------------------------------
# Part A (1): textbook quicksort, Lomuto partition, last element as pivot
# --------------------------------------------------------------------------

def quicksort_basic(a):
    """Textbook quicksort. Slow and deeply recursive on sorted/duplicate data."""
    _qs_basic(a, 0, len(a) - 1)


def _qs_basic(a, lo, hi):
    if lo >= hi:
        return
    p = _lomuto(a, lo, hi)
    _qs_basic(a, lo, p - 1)
    _qs_basic(a, p + 1, hi)


def _lomuto(a, lo, hi):
    """Partition a[lo..hi] around a[hi]. Returns the pivot's final index."""
    pivot = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1


# --------------------------------------------------------------------------
# Part A (2): improved quicksort
# --------------------------------------------------------------------------

def quicksort_improved(a, cutoff=16):
    """Randomised quicksort with an insertion-sort cutoff.

    1. Random pivot            -> no fixed input (e.g. sorted) is always bad.
    2. Three-way partition     -> a run of equal keys is finished in one pass,
                                  so heavy duplication (Nu 100, Nu 500) is cheap.
    3. Insertion sort for parts of size <= cutoff.
    4. Recurse on the SMALLER part, loop on the larger one -> the recursion
       depth is at most log2(n), whatever the pivots turn out to be.
    """
    _qs_improved(a, 0, len(a) - 1, cutoff)


def _qs_improved(a, lo, hi, cutoff):
    while hi - lo + 1 > cutoff and hi - lo + 1 > 1:
        # random pivot value
        pivot = a[random.randint(lo, hi)]

        # three-way partition (Dijkstra): a[lo..lt-1] < pivot,
        # a[lt..gt] == pivot, a[gt+1..hi] > pivot
        lt, i, gt = lo, lo, hi
        while i <= gt:
            v = a[i]
            if v < pivot:
                a[lt], a[i] = v, a[lt]
                lt += 1
                i += 1
            elif v > pivot:
                a[i], a[gt] = a[gt], v
                gt -= 1
            else:
                i += 1

        # recurse on the smaller side, loop on the larger side
        if lt - lo < hi - gt:
            _qs_improved(a, lo, lt - 1, cutoff)
            lo = gt + 1
        else:
            _qs_improved(a, gt + 1, hi, cutoff)
            hi = lt - 1

    _insertion_sort(a, lo, hi)


def _insertion_sort(a, lo, hi):
    """Insertion sort on a[lo..hi] (inclusive). Does nothing if size <= 1."""
    for i in range(lo + 1, hi + 1):
        v = a[i]
        j = i - 1
        while j >= lo and a[j] > v:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = v