"""Closest pair of points: brute force and divide and conquer.

Both functions take a list of (x, y) points (n >= 2) and return (d, i, j):
the smallest distance d and the indices i < j of a pair achieving it.
If several pairs tie for the smallest distance, either function may return
any one of them (the distance d is always the same).
"""

from math import sqrt


def closest_pair_brute(points):
    """Check every pair. Theta(n^2)."""
    n = len(points)
    if n < 2:
        raise ValueError("need at least 2 points")
    best = None
    bi = bj = -1
    for i in range(n - 1):
        xi, yi = points[i]
        for j in range(i + 1, n):
            dx = xi - points[j][0]
            dy = yi - points[j][1]
            d2 = dx * dx + dy * dy
            if best is None or d2 < best:
                best, bi, bj = d2, i, j
    return sqrt(best), bi, bj


def closest_pair(points):
    """Divide and conquer. Theta(n log n).

    Steps
      1. Sort the points by x once (O(n log n)).
      2. Split at the middle, solve both halves recursively.
      3. Let delta be the better of the two halves. Only points within
         delta of the dividing line can beat it, so collect that strip,
         ordered by y, and compare each strip point with the few
         neighbours whose y is within delta (at most 7 can be).
      4. The recursion also returns its points sorted by y, built by
         merging the two halves, so step 3 costs O(n), not O(n log n).
    """
    n = len(points)
    if n < 2:
        raise ValueError("need at least 2 points")

    # Attach original indices, sort by x (ties broken by y).
    px = sorted(((x, y, i) for i, (x, y) in enumerate(points)),
                key=lambda p: (p[0], p[1]))

    d2, i, j = _solve(px)
    return sqrt(d2), min(i, j), max(i, j)


def _brute_small(P):
    """Brute force on a small list of (x, y, idx). Returns (d2, i, j)."""
    best = None
    bi = bj = -1
    for a in range(len(P) - 1):
        xa, ya, ia = P[a]
        for b in range(a + 1, len(P)):
            dx = xa - P[b][0]
            dy = ya - P[b][1]
            d2 = dx * dx + dy * dy
            if best is None or d2 < best:
                best, bi, bj = d2, ia, P[b][2]
    return best, bi, bj


def _merge_by_y(L, R):
    """Merge two lists already sorted by y. O(len(L) + len(R))."""
    out = []
    a = b = 0
    while a < len(L) and b < len(R):
        if L[a][1] <= R[b][1]:
            out.append(L[a])
            a += 1
        else:
            out.append(R[b])
            b += 1
    out.extend(L[a:])
    out.extend(R[b:])
    return out


def _solve(P):
    """P is sorted by x. Returns (best_d2, i, j) and re-sorts P by y in place.

    Squared distances are used internally to avoid square roots.
    """
    n = len(P)
    if n <= 3:
        res = _brute_small(P)
        P.sort(key=lambda p: p[1])
        return res

    mid = n // 2
    mid_x = P[mid][0]            # dividing line
    left, right = P[:mid], P[mid:]

    best_l = _solve(left)        # left, right now sorted by y
    best_r = _solve(right)
    best = best_l if best_l[0] <= best_r[0] else best_r

    merged = _merge_by_y(left, right)
    P[:] = merged

    # Strip: points with (x - mid_x)^2 < best distance squared, ordered by y.
    d2 = best[0]
    strip = [p for p in merged if (p[0] - mid_x) ** 2 < d2]

    for a in range(len(strip)):
        xa, ya, ia = strip[a]
        for b in range(a + 1, len(strip)):
            dy = strip[b][1] - ya
            if dy * dy >= best[0]:
                break            # later points are even farther in y
            dx = strip[b][0] - xa
            cand = dx * dx + dy * dy
            if cand < best[0]:
                best = (cand, ia, strip[b][2])
    return best