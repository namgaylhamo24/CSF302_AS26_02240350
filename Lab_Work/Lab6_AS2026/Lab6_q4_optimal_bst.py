"""Lab 6 - Q4 (optional): Optimal binary search tree.

Keys k1..kn with search probabilities p[1..n]; dummy keys d0..dn (unsuccessful searches)
with probabilities q[0..n].  Exact arithmetic (Fractions) is used so 2.75 comes out exactly.
"""
import json
import random
from fractions import Fraction


def optimal_bst(p, q):
    n = len(p)
    e = [[Fraction(0)] * (n + 1) for _ in range(n + 2)]
    w = [[Fraction(0)] * (n + 1) for _ in range(n + 2)]
    root = [[0] * (n + 1) for _ in range(n + 2)]
    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]
    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            w[i][j] = w[i][j - 1] + p[j - 1] + q[j]
            best = None
            for r in range(i, j + 1):
                t = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if best is None or t < best:
                    best, root[i][j] = t, r
            e[i][j] = best
    return e, w, root


def tree_lines(root, n):
    def label(i, j):
        return f"d{j}" if j < i else f"k{root[i][j]}"

    out = []

    def rec(i, j, prefix, is_last, top):
        out.append(label(i, j) if top else prefix + ("└── " if is_last else "├── ") + label(i, j))
        if j < i:
            return
        r = root[i][j]
        child = prefix if top else prefix + ("    " if is_last else "│   ")
        rec(i, r - 1, child, False, False)
        rec(r + 1, j, child, True, False)

    rec(1, n, "", True, True)
    return out


def cost_of_tree(root, p, q, i, j, depth=0):
    """Expected cost computed from the printed structure: sum (depth+1) * probability."""
    if j < i:
        return (depth + 1) * q[j]
    r = root[i][j]
    return ((depth + 1) * p[r - 1] + cost_of_tree(root, p, q, i, r - 1, depth + 1)
            + cost_of_tree(root, p, q, r + 1, j, depth + 1))


def brute_force(p, q, i, j, depth=0):
    """Exhaustive search over every BST shape on k_i..k_j (independent of the DP recurrence)."""
    if j < i:
        return (depth + 1) * q[j]
    return min((depth + 1) * p[r - 1] + brute_force(p, q, i, r - 1, depth + 1)
               + brute_force(p, q, r + 1, j, depth + 1) for r in range(i, j + 1))


def fmt(x):
    return f"{float(x):.2f}"


def main():
    p = [Fraction(x) for x in ("0.15", "0.10", "0.05", "0.10", "0.20")]
    q = [Fraction(x) for x in ("0.05", "0.10", "0.05", "0.05", "0.05", "0.10")]
    n = len(p)
    assert sum(p) + sum(q) == 1
    e, w, root = optimal_bst(p, q)

    print("p =", [fmt(x) for x in p])
    print("q =", [fmt(x) for x in q])
    print("\ne[i][j]  (expected cost of an optimal tree on k_i..k_j)")
    print("      " + "".join(f"   j={j}" for j in range(0, n + 1)))
    for i in range(1, n + 2):
        print(f" i={i} " + "".join(f"{fmt(e[i][j]):>6}" if j >= i - 1 else "      " for j in range(0, n + 1)))
    print("\nroot[i][j]")
    print("      " + "".join(f"   j={j}" for j in range(1, n + 1)))
    for i in range(1, n + 1):
        print(f" i={i} " + "".join(f"{root[i][j]:>6}" if j >= i else "      " for j in range(1, n + 1)))

    best = e[1][n]
    print(f"\nExpected search cost = {float(best)}")
    assert float(best) == 2.75
    print("\nOptimal tree (top = root; first child = left subtree, second = right subtree)\n")
    lines = tree_lines(root, n)
    print("\n".join(lines))

    c_tree = cost_of_tree(root, p, q, 1, n)
    c_brute = brute_force(p, q, 1, n)
    print(f"\nCost recomputed from the printed tree : {float(c_tree)}")
    print(f"Cost found by exhaustive search       : {float(c_brute)}")
    assert c_tree == c_brute == best

    rng = random.Random(5)
    for _ in range(200):
        k = rng.randint(1, 7)
        wts = [rng.randint(1, 20) for _ in range(2 * k + 1)]
        tot = sum(wts)
        pp = [Fraction(x, tot) for x in wts[:k]]
        qq = [Fraction(x, tot) for x in wts[k:]]
        ee, _, rr = optimal_bst(pp, qq)
        assert ee[1][k] == brute_force(pp, qq, 1, k) == cost_of_tree(rr, pp, qq, 1, k)
    print("DP == exhaustive search on 200 further random instances (1..7 keys).")

    json.dump({"expected_cost": float(best), "tree": lines,
               "root": [[root[i][j] for j in range(n + 1)] for i in range(n + 2)]},
              open("q4_results.json", "w"), indent=1)


if __name__ == "__main__":
    main()