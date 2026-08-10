"""Benchmark the naive trial division method for generating prime numbers."""

import time


# Keep the demo practical: the naive method becomes very slow for 500,000 and 1,000,000.
MAX_DEMO_SIZE_350 = 100_000


def is_prime_naive_350(number_350):
    """Return True if number_350 is prime using direct trial division."""
    if number_350 < 2:
        return False
    for divisor_350 in range(2, number_350):
        if number_350 % divisor_350 == 0:
            return False
    return True


def generate_primes_naive_350(limit_350):
    """Generate all prime numbers up to the given limit using naive trial division."""
    primes_350 = []
    for number_350 in range(2, limit_350 + 1):
        if is_prime_naive_350(number_350):
            primes_350.append(number_350)
    return primes_350


def benchmark_naive_350(sizes_350):
    """Measure the time required to generate primes using the naive method."""
    results_350 = []
    for limit_350 in sizes_350:
        start_350 = time.perf_counter()
        primes_350 = generate_primes_naive_350(limit_350)
        end_350 = time.perf_counter()
        elapsed_350 = end_350 - start_350
        results_350.append((limit_350, len(primes_350), elapsed_350))
        print(
            f"Naive Trial Division | N = {limit_350:>9} | "
            f"primes found = {len(primes_350):>7} | time = {elapsed_350:.6f} sec"
        )
    return results_350


def main_350():
    input_sizes_350 = [10_000, 50_000, 100_000, 500_000, 1_000_000]

    if MAX_DEMO_SIZE_350 is not None:
        input_sizes_350 = [size_350 for size_350 in input_sizes_350 if size_350 <= MAX_DEMO_SIZE_350]

    print("=" * 60)
    print("NAIVE TRIAL DIVISION - EMPIRICAL BENCHMARK")
    print("=" * 60)

    benchmark_naive_350(input_sizes_350)


if __name__ == "__main__":
    main_350()