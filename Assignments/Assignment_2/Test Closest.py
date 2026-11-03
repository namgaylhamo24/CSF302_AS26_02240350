"""Tests for closest.py. Run with:  python test_closest.py   (or pytest)."""

import random
import unittest
from math import dist, isclose

from closest import closest_pair, closest_pair_brute


def check_valid(points, result):
    """The (d, i, j) triple must be internally consistent."""
    d, i, j = result
    assert 0 <= i < j < len(points), f"bad indices {i}, {j}"
    assert isclose(d, dist(points[i], points[j]), abs_tol=1e-9), "d does not match indices"


class TestExample(unittest.TestCase):
    def test_brief_example(self):
        pts = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
        for f in (closest_pair_brute, closest_pair):
            d, i, j = f(pts)
            self.assertAlmostEqual(d, 2 ** 0.5)
            self.assertEqual((i, j), (0, 5))


class TestRandomAgainstBrute(unittest.TestCase):
    def test_random_integer_points(self):
        rng = random.Random(2026)
        for _ in range(1000):
            n = rng.randint(2, 50)
            # small coordinate range on purpose: forces many ties and duplicates
            pts = [(rng.randint(0, 30), rng.randint(0, 30)) for _ in range(n)]
            b, f = closest_pair_brute(pts), closest_pair(pts)
            self.assertTrue(isclose(b[0], f[0], abs_tol=1e-9), (pts, b, f))
            check_valid(pts, f)

    def test_random_float_points(self):
        rng = random.Random(7)
        for _ in range(1000):
            n = rng.randint(2, 50)
            pts = [(rng.uniform(-100, 100), rng.uniform(-100, 100)) for _ in range(n)]
            b, f = closest_pair_brute(pts), closest_pair(pts)
            self.assertTrue(isclose(b[0], f[0], rel_tol=1e-12), (pts, b, f))
            check_valid(pts, f)


class TestEdgeCases(unittest.TestCase):
    def test_exactly_two_points(self):
        pts = [(5, 5), (8, 9)]
        for f in (closest_pair_brute, closest_pair):
            self.assertEqual(f(pts), (5.0, 0, 1))

    def test_two_points_given_in_reverse_x_order(self):
        pts = [(8, 9), (5, 5)]
        for f in (closest_pair_brute, closest_pair):
            d, i, j = f(pts)
            self.assertEqual((d, i, j), (5.0, 0, 1))

    def test_duplicate_points(self):
        pts = [(1, 1), (9, 9), (4, 2), (9, 9), (7, 3)]
        for f in (closest_pair_brute, closest_pair):
            d, i, j = f(pts)
            self.assertEqual(d, 0.0)
            self.assertEqual((i, j), (1, 3))

    def test_all_duplicates(self):
        pts = [(3, 3)] * 10
        d, i, j = closest_pair(pts)
        self.assertEqual(d, 0.0)
        check_valid(pts, (d, i, j))

    def test_all_on_vertical_line(self):
        rng = random.Random(1)
        for _ in range(200):
            n = rng.randint(2, 50)
            pts = [(4, rng.randint(0, 1000)) for _ in range(n)]
            b, f = closest_pair_brute(pts), closest_pair(pts)
            self.assertAlmostEqual(b[0], f[0])
            check_valid(pts, f)

    def test_all_on_horizontal_line(self):
        rng = random.Random(2)
        for _ in range(200):
            n = rng.randint(2, 50)
            pts = [(rng.randint(0, 1000), 4) for _ in range(n)]
            b, f = closest_pair_brute(pts), closest_pair(pts)
            self.assertAlmostEqual(b[0], f[0])
            check_valid(pts, f)

    def test_closest_pair_straddles_dividing_line(self):
        # 8 points sorted by x; the split is between x=3 and x=4.
        # Left half and right half each have a best gap of 10,
        # but (3, 5) and (4, 5) are only 1 apart, across the line.
        pts = [(0, 0), (1, 100), (2, 50), (3, 5),
               (4, 5), (5, 80), (6, 20), (7, 200)]
        for f in (closest_pair_brute, closest_pair):
            d, i, j = f(pts)
            self.assertAlmostEqual(d, 1.0)
            self.assertEqual((i, j), (3, 4))

    def test_straddling_pair_with_shuffled_input_order(self):
        base = [(0, 0), (1, 100), (2, 50), (3, 5),
                (4, 5), (5, 80), (6, 20), (7, 200)]
        rng = random.Random(3)
        for _ in range(100):
            pts = base[:]
            rng.shuffle(pts)
            d, i, j = closest_pair(pts)
            self.assertAlmostEqual(d, 1.0)
            self.assertEqual({pts[i], pts[j]}, {(3, 5), (4, 5)})

    def test_many_points_share_the_dividing_x(self):
        # many points with x equal to the split value, stressing the strip
        rng = random.Random(4)
        for _ in range(200):
            n = rng.randint(4, 50)
            pts = [(rng.choice([5, 5, 5, 4, 6]), rng.randint(0, 100)) for _ in range(n)]
            b, f = closest_pair_brute(pts), closest_pair(pts)
            self.assertAlmostEqual(b[0], f[0])
            check_valid(pts, f)

    def test_input_not_modified(self):
        pts = [(3, 1), (1, 2), (2, 9), (8, 8)]
        copy = pts[:]
        closest_pair(pts)
        self.assertEqual(pts, copy)

    def test_fewer_than_two_points_raises(self):
        for f in (closest_pair_brute, closest_pair):
            with self.assertRaises(ValueError):
                f([(1, 1)])


if __name__ == "__main__":
    unittest.main(verbosity=2)