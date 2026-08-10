"""Benchmark the Sieve of Eratosthenes method for generating prime numbers."""

import time


def sieve_of_eratosthenes_350(limit_350):
    """Generate all prime numbers up to the given limit using the sieve algorithm."""
    if limit_350 < 2:
        return []

    is_prime_350 = [True] * (limit_350 + 1)
    is_prime_350[0] = is_prime_350[1] = False

    candidate_350 = 2
    while candidate_350 * candidate_350 <= limit_350:
        if is_prime_350[candidate_350]:
            for multiple_350 in range(candidate_350 * candidate_350, limit_350 + 1, candidate_350):
                is_prime_350[multiple_350] = False
        candidate_350 += 1

    return [number_350 for number_350, flag_350 in enumerate(is_prime_350) if flag_350]


def benchmark_sieve_350(sizes_350):
    """Measure the time required to generate primes using the sieve method."""
    results_350 = []
    for limit_350 in sizes_350:
        start_350 = time.perf_counter()
        primes_350 = sieve_of_eratosthenes_350(limit_350)
        end_350 = time.perf_counter()
        elapsed_350 = end_350 - start_350
        results_350.append((limit_350, len(primes_350), elapsed_350))
        print(
            f"Sieve of Eratosthenes | N = {limit_350:>9} | "
            f"primes found = {len(primes_350):>7} | time = {elapsed_350:.6f} sec"
        )
    return results_350


def main_350():
    input_sizes_350 = [10_000, 50_000, 100_000, 500_000, 1_000_000]

    print("=" * 60)
    print("SIEVE OF ERATOSTHENES - EMPIRICAL BENCHMARK")
    print("=" * 60)

    benchmark_sieve_350(input_sizes_350)


if __name__ == "__main__":
    main_350()