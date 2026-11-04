"""Tests for sorts.py. Run with:  python test_sorts.py   (or pytest).

sorted() is used here ONLY to check answers, as the brief allows.
"""

import random
import sys
import unittest

from sorts import quicksort_basic, quicksort_improved

SORTS = {
    "basic": quicksort_basic,
    "improved(cutoff=16)": quicksort_improved,
    "improved(cutoff=1)": lambda a: quicksort_improved(a, cutoff=1),
    "improved(cutoff=64)": lambda a: quicksort_improved(a, cutoff=64),
}


def stack_depth():
    d, f = 0, sys._getframe()
    while f:
        d, f = d + 1, f.f_back
    return d


class TestAgainstSorted(unittest.TestCase):
    def test_random_lists(self):
        rng = random.Random(2026)
        for name, f in SORTS.items():
            for _ in range(600):
                n = rng.randint(0, 200)
                a = [rng.randint(-1000, 1000) for _ in range(n)]
                expected = sorted(a)
                f(a)
                self.assertEqual(a, expected, name)

    def test_random_lists_many_duplicates(self):
        rng = random.Random(5)
        for name, f in SORTS.items():
            for _ in range(600):
                a = [rng.randint(0, 9) for _ in range(rng.randint(0, 150))]
                expected = sorted(a)
                f(a)
                self.assertEqual(a, expected, name)


class TestRequiredCases(unittest.TestCase):
    def check(self, a):
        for name, f in SORTS.items():
            b = a[:]
            f(b)
            self.assertEqual(b, sorted(a), name)

    def test_empty(self):
        self.check([])

    def test_one_element(self):
        self.check([42])

    def test_two_elements(self):
        self.check([2, 1])
        self.check([1, 2])

    def test_all_equal(self):
        self.check([7] * 100)

    def test_already_sorted(self):
        self.check(list(range(100)))

    def test_reverse_sorted(self):
        self.check(list(range(100, 0, -1)))

    def test_negative_numbers(self):
        self.check([-5, 3, -1, 0, -10, 8, -3, -3, 2])

    def test_all_negative(self):
        self.check([-1, -2, -3, -4, -5, -5])

    def test_cutoff_larger_than_list(self):
        a = [5, 2, 9, 1]
        quicksort_improved(a, cutoff=1000)
        self.assertEqual(a, [1, 2, 5, 9])


class TestInPlace(unittest.TestCase):
    def test_sorts_the_same_list_object_and_returns_none(self):
        for name, f in SORTS.items():
            a = [3, 1, 2]
            ident = id(a)
            self.assertIsNone(f(a), name)
            self.assertEqual(id(a), ident)
            self.assertEqual(a, [1, 2, 3])


class TestBehaviourOnBadData(unittest.TestCase):
    def test_basic_crashes_on_long_sorted_input(self):
        # The problem described in the brief: depth ~ n on sorted data.
        with self.assertRaises(RecursionError):
            quicksort_basic(list(range(5000)))

    def test_improved_survives_bad_inputs_with_tiny_recursion_limit(self):
        # The improved sort recurses at most ~log2(n) deep, so it must work
        # even when we leave only 100 frames of headroom.
        old = sys.getrecursionlimit()
        sys.setrecursionlimit(stack_depth() + 100)
        try:
            for a in (list(range(100000)),
                      list(range(100000, 0, -1)),
                      [5] * 100000,
                      [random.Random(1).randint(0, 9) for _ in range(100000)]):
                expected = sorted(a)
                quicksort_improved(a)
                self.assertEqual(a, expected)
        finally:
            sys.setrecursionlimit(old)


if __name__ == "__main__":
    unittest.main(verbosity=2)