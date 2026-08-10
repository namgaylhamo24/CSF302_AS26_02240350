"""Benchmark the optimized trial division method for generating prime numbers."""

import math
import time


def is_prime_optimized_350(number_350):
    """Return True if number_350 is prime by checking divisors only up to sqrt(number_350)."""
    if number_350 < 2:
        return False
    if number_350 == 2:
        return True
    if number_350 % 2 == 0:
        return False

    limit_350 = math.isqrt(number_350)
    for divisor_350 in range(3, limit_350 + 1, 2):
        if number_350 % divisor_350 == 0:
            return False
    return True


def generate_primes_optimized_350(limit_350):
    """Generate all prime numbers up to the given limit using optimized trial division."""
    primes_350 = []
    for number_350 in range(2, limit_350 + 1):
        if is_prime_optimized_350(number_350):
            primes_350.append(number_350)
    return primes_350


def benchmark_optimized_350(sizes_350):
    """Measure the time required to generate primes using the optimized method."""
    results_350 = []
    for limit_350 in sizes_350:
        start_350 = time.perf_counter()
        primes_350 = generate_primes_optimized_350(limit_350)
        end_350 = time.perf_counter()
        elapsed_350 = end_350 - start_350
        results_350.append((limit_350, len(primes_350), elapsed_350))
        print(
            f"Optimized Trial Division | N = {limit_350:>9} | "
            f"primes found = {len(primes_350):>7} | time = {elapsed_350:.6f} sec"
        )
    return results_350


def main_350():
    input_sizes_350 = [10_000, 50_000, 100_000, 500_000, 1_000_000]

    print("=" * 60)
    print("OPTIMIZED TRIAL DIVISION - EMPIRICAL BENCHMARK")
    print("=" * 60)

    benchmark_optimized_350(input_sizes_350)


if __name__ == "__main__":
    main_350()