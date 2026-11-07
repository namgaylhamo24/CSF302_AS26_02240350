"""Part C analysis for Assignment 4. Run:  python analyze_booking.py

All randomness is seeded, so the numbers are the same on every machine.
Writes: results_booking.json, ratio_summary.csv, ratios_hist.png
"""

import csv
import json
import random
import statistics

from booking import (_dp, best_schedule, brute_force, greedy_earliest_finish,
                     greedy_highest_fee)

BRIEF = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000), (12, 14, 2500), (16, 18, 2000)]
CE_EARLIEST = [(0, 10, 100), (1, 2, 1)]
CE_FEE = [(0, 5, 10), (5, 10, 10), (0, 10, 15)]
CE_BOTH = [(0, 10, 100), (0, 5, 60), (5, 10, 60), (1, 2, 1)]


def small_instance(rng, fee_lo=1, fee_hi=20):
    """0 to 10 requests, same generator family as the unit tests."""
    out = []
    for _ in range(rng.randint(0, 10)):
        s = rng.randint(0, 20)
        out.append((s, s + rng.randint(1, 6), rng.randint(fee_lo, fee_hi)))
    return out


def large_instance(rng, mode):
    """50 requests. start 0..96, duration 1..12 hours.
    'independent': fee uniform 1,000..10,000 whatever the length.
    'proportional': fee = duration x hourly rate (500..1,000)."""
    out = []
    for _ in range(50):
        s = rng.randint(0, 96)
        d = rng.randint(1, 12)
        fee = rng.randint(1000, 10000) if mode == "independent" else d * rng.randint(500, 1000)
        out.append((s, s + d, fee))
    return out


def summarise(ratios):
    return {
        "average": statistics.mean(ratios),
        "median": statistics.median(ratios),
        "worst": min(ratios),
        "optimal_pct": 100 * sum(1 for r in ratios if r > 1 - 1e-12) / len(ratios),
    }


def main():
    res = {}

    # ---- C1: counterexamples ----
    ce = {}
    for name, reqs in (("earliest", CE_EARLIEST), ("fee", CE_FEE), ("both", CE_BOTH)):
        ce[name] = {
            "requests": reqs,
            "optimal": best_schedule(reqs),
            "brute": brute_force(reqs),
            "earliest_finish": greedy_earliest_finish(reqs),
            "highest_fee": greedy_highest_fee(reqs),
        }
    res["counterexamples"] = ce

    # ---- DP table for the brief's example (for the report) ----
    order, p, opt = _dp(BRIEF)
    res["dp_table"] = [
        {"j": j, "request": BRIEF[order[j - 1]], "orig_index": order[j - 1], "p": p[j], "opt": opt[j]}
        for j in range(1, len(BRIEF) + 1)
    ]

    # ---- C3: ratios over 1,000 random inputs of 50 requests ----
    ratio_data = {}
    for mode, seed in (("independent", 4001), ("proportional", 4002)):
        rng = random.Random(seed)
        r_ef, r_hf = [], []
        for _ in range(1000):
            reqs = large_instance(rng, mode)
            opt_total = best_schedule(reqs)[0]
            ef = greedy_earliest_finish(reqs)[0]
            hf = greedy_highest_fee(reqs)[0]
            assert ef <= opt_total and hf <= opt_total
            r_ef.append(ef / opt_total)
            r_hf.append(hf / opt_total)
        ratio_data[mode] = {"earliest_finish": r_ef, "highest_fee": r_hf}
        res[f"ratios_{mode}"] = {"earliest_finish": summarise(r_ef), "highest_fee": summarise(r_hf)}

    # ---- testing vs proof: how long do random tests keep passing? ----
    stream = random.Random(2026)
    first_fail = {"earliest_finish": None, "highest_fee": None}
    n_tests = 0
    pass_counts = {"earliest_finish": 0, "highest_fee": 0}
    for t in range(1, 1001):
        reqs = small_instance(stream)
        best = best_schedule(reqs)[0]
        n_tests += 1
        for key, f in (("earliest_finish", greedy_earliest_finish), ("highest_fee", greedy_highest_fee)):
            ok = f(reqs)[0] == best
            pass_counts[key] += ok
            if not ok and first_fail[key] is None:
                first_fail[key] = t
    res["small_random_tests"] = {
        "n": n_tests,
        "pass_pct": {k: 100 * v / n_tests for k, v in pass_counts.items()},
        "first_failure_at_test": first_fail,
    }

    # ---- equal fees: earliest finish should always be optimal ----
    rng = random.Random(77)
    fails = 0
    for _ in range(1000):
        reqs = small_instance(rng, 100, 100)
        if greedy_earliest_finish(reqs)[0] != brute_force(reqs)[0]:
            fails += 1
    res["equal_fee_failures_out_of_1000"] = fails

    # ---- write files ----
    with open("results_booking.json", "w") as fh:
        json.dump(res, fh, indent=2)
    with open("ratio_summary.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["fee_model", "rule", "average_ratio", "median_ratio", "worst_ratio", "pct_inputs_optimal"])
        for mode in ("independent", "proportional"):
            for rule in ("earliest_finish", "highest_fee"):
                s = res[f"ratios_{mode}"][rule]
                w.writerow([mode, rule, f"{s['average']:.4f}", f"{s['median']:.4f}",
                            f"{s['worst']:.4f}", f"{s['optimal_pct']:.1f}"])

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
    for ax, mode in zip(axes, ("independent", "proportional")):
        bins = [i / 40 for i in range(0, 41)]
        ax.hist(ratio_data[mode]["earliest_finish"], bins=bins, alpha=0.7, label="earliest finish")
        ax.hist(ratio_data[mode]["highest_fee"], bins=bins, alpha=0.7, label="highest fee")
        ax.set_title(f"Fee model: {mode}")
        ax.set_xlabel("greedy revenue / optimal revenue")
        ax.grid(True, alpha=0.3)
    axes[0].set_ylabel("Number of inputs (out of 1,000)")
    axes[0].legend()
    fig.tight_layout()
    fig.savefig("ratios_hist.png", dpi=200)


if __name__ == "__main__":
    main()