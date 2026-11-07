"""Booking the hall: two greedy rules, dynamic programming and brute force.

A request is a tuple (start, finish, fee) with start < finish and fee >= 0.
Two requests fit together if one finishes no later than the other starts
(finish_a <= start_b or finish_b <= start_a), so back-to-back events are fine.

Every function returns (total_fee, chosen), where chosen is a list of indices
into the ORIGINAL input list, in increasing order. When several schedules tie
for the best total, which one is returned is not specified; only the total is.
"""

from bisect import bisect_right


def _validate(requests):
    """Reject requests that would break the 'fits' rule or the DP."""
    for k, r in enumerate(requests):
        if len(r) != 3:
            raise ValueError(f"request {k} must be (start, finish, fee)")
        start, finish, fee = r
        if not start < finish:
            raise ValueError(f"request {k}: start must be before finish")
        if fee < 0:
            raise ValueError(f"request {k}: fee must not be negative")


def _fits(a, b):
    """True if requests a and b can share the hall."""
    return a[1] <= b[0] or b[1] <= a[0]


def _result(requests, chosen):
    return sum(requests[i][2] for i in chosen), sorted(chosen)


# --------------------------------------------------------------------------
# Greedy rule 1: earliest finish first
# --------------------------------------------------------------------------

def greedy_earliest_finish(requests):
    """Sort by finish time; accept each request that fits. O(n log n).

    Ties on finish time go to the higher fee, then the lower index.
    Because requests are taken in finish order, a request fits exactly when
    it starts no earlier than the finish of the last accepted request.
    """
    _validate(requests)
    order = sorted(range(len(requests)),
                   key=lambda i: (requests[i][1], -requests[i][2], i))
    chosen = []
    last_finish = None
    for i in order:
        start, finish, _ = requests[i]
        if last_finish is None or start >= last_finish:
            chosen.append(i)
            last_finish = finish
    return _result(requests, chosen)


# --------------------------------------------------------------------------
# Greedy rule 2: highest fee first
# --------------------------------------------------------------------------

def greedy_highest_fee(requests):
    """Sort by fee, highest first; accept each request that fits. O(n^2) worst.

    Ties on fee go to the earlier finish, then the lower index. Accepted
    requests are no longer in time order, so each candidate is checked
    against every request accepted so far.
    """
    _validate(requests)
    order = sorted(range(len(requests)),
                   key=lambda i: (-requests[i][2], requests[i][1], i))
    chosen = []
    for i in order:
        if all(_fits(requests[i], requests[j]) for j in chosen):
            chosen.append(i)
    return _result(requests, chosen)


# --------------------------------------------------------------------------
# Dynamic programming: weighted interval scheduling
# --------------------------------------------------------------------------

def _dp(requests):
    """Fill the DP table.

    order : original indices sorted by finish time
    p[j]  : how many requests (in sorted order) finish no later than request j
            starts; these are exactly the first p[j] requests, and no other
            request before j fits with j. Positions are 1-based, p[0] unused.
    opt[j]: best total fee using only the first j requests in sorted order.

    OPT(j) = max( OPT(j-1),  fee_j + OPT(p(j)) )
    """
    n = len(requests)
    order = sorted(range(n), key=lambda i: (requests[i][1], requests[i][0], i))
    finishes = [requests[i][1] for i in order]
    p = [0] * (n + 1)
    opt = [0] * (n + 1)
    for j in range(1, n + 1):
        start, _, fee = requests[order[j - 1]]
        # Every request at sorted position >= j-1 finishes after `start`
        # (finish >= this finish > start), so the count never includes
        # request j itself or anything later: p[j] <= j-1.
        p[j] = bisect_right(finishes, start)
        opt[j] = max(opt[j - 1], fee + opt[p[j]])
    return order, p, opt


def best_schedule(requests):
    """Maximum total fee by dynamic programming. O(n log n)."""
    _validate(requests)
    order, p, opt = _dp(requests)
    chosen = []
    j = len(requests)
    while j > 0:
        fee = requests[order[j - 1]][2]
        if fee + opt[p[j]] > opt[j - 1]:     # taking request j is strictly better
            chosen.append(order[j - 1])
            j = p[j]
        else:                                 # skipping it is at least as good
            j -= 1
    return opt[len(requests)], sorted(chosen)


# --------------------------------------------------------------------------
# Brute force (for checking only)
# --------------------------------------------------------------------------

def brute_force(requests):
    """Try every subset. O(2^n * n^2), so only for n <= 15.

    Feasibility is checked pairwise straight from the definition of 'fits',
    deliberately not sharing any logic with the DP.
    """
    _validate(requests)
    n = len(requests)
    if n > 15:
        raise ValueError("brute_force is for checking only: n must be <= 15")
    best_total, best_set = 0, []
    for mask in range(1 << n):
        idx = [i for i in range(n) if (mask >> i) & 1]
        ok = all(_fits(requests[a], requests[b])
                 for pos, a in enumerate(idx) for b in idx[pos + 1:])
        if ok:
            total = sum(requests[i][2] for i in idx)
            if total > best_total:
                best_total, best_set = total, idx
    return best_total, best_set