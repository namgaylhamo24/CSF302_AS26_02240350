import json
import random

INF = float("inf")


def matrix_chain(d):
    """Bottom-up DP.  m[i][j] = min scalar multiplications for A_i..A_j,
    s[i][j] = the split k that achieves it."""
    n = len(d) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            m[i][j] = INF
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + d[i - 1] * d[k] * d[j]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k
    return m, s


def parenthesise(s, i, j):
    if i == j:
        return f"A{i}"
    k = s[i][j]
    return "(" + parenthesise(s, i, k) + parenthesise(s, k + 1, j) + ")"


def left_to_right_cost(d):
    """((A1 A2) A3) ... An : multiplying (A1..A_{k-1}) [d0 x d_{k-1}] by A_k [d_{k-1} x d_k]."""
    return sum(d[0] * d[k - 1] * d[k] for k in range(2, len(d)))


def all_parenthesisations(d, i, j):
    """Brute force: every full parenthesisation of A_i..A_j as (cost, string)."""
    if i == j:
        return [(0, f"A{i}")]
    out = []
    for k in range(i, j):
        for c1, s1 in all_parenthesisations(d, i, k):
            for c2, s2 in all_parenthesisations(d, k + 1, j):
                out.append((c1 + c2 + d[i - 1] * d[k] * d[j], "(" + s1 + s2 + ")"))
    return out


def catalan(x):
    from math import comb
    return comb(2 * x, x) // (x + 1)


def analyse(name, d, results):
    n = len(d) - 1
    m, s = matrix_chain(d)
    best = m[1][n]
    par = parenthesise(s, 1, n)
    ltr = left_to_right_cost(d)
    row = {"name": name, "dims": d, "n": n, "optimal": best, "parenthesisation": par,
           "left_to_right": ltr, "ratio": ltr / best if best else 1.0}
    if n <= 8:
        trees = all_parenthesisations(d, 1, n)
        bf = min(c for c, _ in trees)
        costs = dict((sstr, c) for c, sstr in trees)
        assert len(trees) == catalan(n - 1)
        assert bf == best, f"DP {best} != brute force {bf}"
        assert costs[par] == best, "DP parenthesisation does not achieve the DP cost"
        row.update({"brute_force": bf, "trees_checked": len(trees), "match": True})
    results.append(row)
    return row


def main():
    results = []
    tests = [("CLRS example", [30, 35, 15, 5, 10, 20, 25]), ("small example", [5, 4, 6, 2, 7])]
    rng = random.Random(6)
    for t in range(1, 6):
        n = rng.randint(3, 8)
        tests.append((f"random {t}", [rng.randint(2, 50) for _ in range(n + 1)]))

    for name, d in tests:
        r = analyse(name, d, results)
        print(f"{name}")
        print(f"  dims                : <{', '.join(map(str, d))}>   ({r['n']} matrices)")
        print(f"  minimum multiplications: {r['optimal']:,}")
        print(f"  optimal order       : {r['parenthesisation']}")
        print(f"  left-to-right cost  : {r['left_to_right']:,}  ({r['ratio']:.2f} x optimal)")
        print(f"  brute force         : {r['brute_force']:,} over {r['trees_checked']} parenthesisations "
              f"-> {'MATCH' if r['match'] else 'MISMATCH'}\n")

    # extra stress test of the verification
    trials = 0
    for _ in range(1000):
        n = rng.randint(1, 8)
        d = [rng.randint(1, 60) for _ in range(n + 1)]
        analyse("stress", d, [])
        trials += 1
    print(f"Stress test: DP == brute force on {trials} further random chains of 1..8 matrices.")

    assert results[0]["optimal"] == 15125
    json.dump({"tests": results, "stress_trials": trials}, open("q2_results.json", "w"), indent=1)


if __name__ == "__main__":
    main()