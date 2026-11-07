"""Tests for booking.py. Run with:  python test_booking.py   (or pytest)."""

import random
import unittest

from booking import (best_schedule, brute_force, greedy_earliest_finish,
                     greedy_highest_fee)

ALL = (greedy_earliest_finish, greedy_highest_fee, best_schedule, brute_force)

BRIEF = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000), (12, 14, 2500), (16, 18, 2000)]

# Small counterexamples (each is checked against the DP and brute force below)
CE_EARLIEST = [(0, 10, 100), (1, 2, 1)]                           # optimum 100
CE_FEE = [(0, 5, 10), (5, 10, 10), (0, 10, 15)]                   # optimum 20
CE_BOTH = [(0, 10, 100), (0, 5, 60), (5, 10, 60), (1, 2, 1)]      # optimum 120


def fits(a, b):
    return a[1] <= b[0] or b[1] <= a[0]


def assert_valid(tc, requests, result):
    """The (total, chosen) pair must be a feasible schedule with the right total."""
    total, chosen = result
    tc.assertEqual(chosen, sorted(set(chosen)), "indices must be unique and ascending")
    for i in chosen:
        tc.assertTrue(0 <= i < len(requests))
    for a in range(len(chosen)):
        for b in range(a + 1, len(chosen)):
            tc.assertTrue(fits(requests[chosen[a]], requests[chosen[b]]),
                          f"requests {chosen[a]} and {chosen[b]} overlap")
    tc.assertEqual(total, sum(requests[i][2] for i in chosen))


def random_requests(rng, max_n=10, fee_lo=0, fee_hi=20):
    n = rng.randint(0, max_n)
    out = []
    for _ in range(n):
        start = rng.randint(0, 20)
        out.append((start, start + rng.randint(1, 6), rng.randint(fee_lo, fee_hi)))
    return out


class TestBriefExample(unittest.TestCase):
    def test_example_from_the_brief(self):
        self.assertEqual(greedy_earliest_finish(BRIEF), (7500, [0, 3, 4]))
        self.assertEqual(best_schedule(BRIEF), (10000, [1, 4]))
        self.assertEqual(brute_force(BRIEF), (10000, [1, 4]))
        self.assertEqual(greedy_highest_fee(BRIEF)[0], 10000)


class TestDPAgainstBruteForce(unittest.TestCase):
    def test_random_inputs_0_to_10_requests(self):
        rng = random.Random(2026)
        for _ in range(1500):
            reqs = random_requests(rng)
            expected = brute_force(reqs)
            got = best_schedule(reqs)
            self.assertEqual(got[0], expected[0], reqs)
            assert_valid(self, reqs, got)

    def test_random_inputs_with_many_ties(self):
        # tiny time range and fee range: lots of back-to-back requests,
        # identical requests and tied totals
        rng = random.Random(11)
        for _ in range(1000):
            n = rng.randint(0, 10)
            reqs = []
            for _ in range(n):
                s = rng.randint(0, 6)
                reqs.append((s, s + rng.randint(1, 3), rng.randint(0, 3)))
            self.assertEqual(best_schedule(reqs)[0], brute_force(reqs)[0], reqs)
            assert_valid(self, reqs, best_schedule(reqs))


class TestEdgeCases(unittest.TestCase):
    def test_no_requests(self):
        for f in ALL:
            self.assertEqual(f([]), (0, []), f.__name__)

    def test_one_request(self):
        for f in ALL:
            self.assertEqual(f([(3, 5, 700)]), (700, [0]), f.__name__)

    def test_all_overlapping(self):
        reqs = [(0, 10, 5), (2, 8, 9), (1, 9, 7), (3, 7, 4)]   # all share time 3..7
        for f in (best_schedule, brute_force):
            self.assertEqual(f(reqs), (9, [1]), f.__name__)
        for f in ALL:
            total, chosen = f(reqs)
            self.assertEqual(len(chosen), 1, f.__name__)

    def test_none_overlapping(self):
        reqs = [(0, 1, 10), (2, 3, 20), (4, 5, 30), (6, 7, 40)]
        for f in ALL:
            self.assertEqual(f(reqs), (100, [0, 1, 2, 3]), f.__name__)

    def test_back_to_back_requests_fit(self):
        reqs = [(9, 12, 100), (12, 15, 100), (15, 18, 100)]    # each ends when the next starts
        for f in ALL:
            self.assertEqual(f(reqs), (300, [0, 1, 2]), f.__name__)

    def test_one_minute_overlap_does_not_fit(self):
        reqs = [(9, 12, 100), (11, 15, 100)]
        for f in ALL:
            self.assertEqual(len(f(reqs)[1]), 1, f.__name__)

    def test_identical_requests(self):
        reqs = [(1, 4, 50), (1, 4, 50), (1, 4, 50)]
        for f in ALL:
            self.assertEqual(f(reqs)[0], 50, f.__name__)

    def test_zero_fee_requests(self):
        reqs = [(0, 5, 0), (5, 10, 0)]
        for f in ALL:
            self.assertEqual(f(reqs)[0], 0, f.__name__)

    def test_input_not_modified_and_unsorted_input_handled(self):
        reqs = [(16, 18, 2000), (13, 17, 4000), (9, 12, 3000), (12, 14, 2500), (10, 16, 8000)]
        copy = list(reqs)
        total, chosen = best_schedule(reqs)
        self.assertEqual(reqs, copy)
        self.assertEqual(total, 10000)
        self.assertEqual(sorted(reqs[i] for i in chosen), [(10, 16, 8000), (16, 18, 2000)])


class TestValidation(unittest.TestCase):
    def test_bad_requests_rejected(self):
        for bad in ([(5, 5, 10)], [(6, 5, 10)], [(1, 2, -3)], [(1, 2)]):
            for f in ALL:
                with self.assertRaises(ValueError, msg=f"{f.__name__} {bad}"):
                    f(bad)

    def test_brute_force_refuses_large_inputs(self):
        with self.assertRaises(ValueError):
            brute_force([(i, i + 1, 1) for i in range(16)])


class TestGreedyRules(unittest.TestCase):
    def test_greedy_results_are_always_feasible(self):
        rng = random.Random(5)
        for _ in range(1000):
            reqs = random_requests(rng, max_n=30)
            assert_valid(self, reqs, greedy_earliest_finish(reqs))
            assert_valid(self, reqs, greedy_highest_fee(reqs))

    def test_greedy_never_beats_the_optimum(self):
        rng = random.Random(6)
        for _ in range(1000):
            reqs = random_requests(rng, max_n=30)
            best = best_schedule(reqs)[0]
            self.assertLessEqual(greedy_earliest_finish(reqs)[0], best)
            self.assertLessEqual(greedy_highest_fee(reqs)[0], best)

    def test_equal_fees_earliest_finish_is_optimal(self):
        # Required by the brief: with equal fees, earliest-finish is optimal.
        rng = random.Random(7)
        for _ in range(1500):
            reqs = random_requests(rng, max_n=10, fee_lo=100, fee_hi=100)
            self.assertEqual(greedy_earliest_finish(reqs)[0], brute_force(reqs)[0], reqs)
        for _ in range(500):  # larger inputs, checked against the DP
            reqs = random_requests(rng, max_n=40, fee_lo=100, fee_hi=100)
            self.assertEqual(greedy_earliest_finish(reqs)[0], best_schedule(reqs)[0], reqs)


class TestCounterexamples(unittest.TestCase):
    def test_earliest_finish_is_not_optimal(self):
        self.assertEqual(brute_force(CE_EARLIEST)[0], 100)
        self.assertEqual(best_schedule(CE_EARLIEST)[0], 100)
        self.assertEqual(greedy_earliest_finish(CE_EARLIEST), (1, [1]))

    def test_highest_fee_is_not_optimal(self):
        self.assertEqual(brute_force(CE_FEE)[0], 20)
        self.assertEqual(best_schedule(CE_FEE), (20, [0, 1]))
        self.assertEqual(greedy_highest_fee(CE_FEE), (15, [2]))

    def test_one_instance_where_both_rules_fail(self):
        self.assertEqual(brute_force(CE_BOTH)[0], 120)
        self.assertEqual(best_schedule(CE_BOTH), (120, [1, 2]))
        self.assertEqual(greedy_earliest_finish(CE_BOTH), (61, [2, 3]))
        self.assertEqual(greedy_highest_fee(CE_BOTH), (100, [0]))


if __name__ == "__main__":
    unittest.main(verbosity=2)