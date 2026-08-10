"""Benchmark binary search performance on randomly generated data."""

import random
import time


def generate_random_data_350(size_350):
    """Generate a list of random integers."""
    return [random.randint(0, size_350 * 10) for _ in range(size_350)]


def binary_search_350(values_350, target_350):
    """Search for a target value in a sorted list using binary search."""
    left_350 = 0
    right_350 = len(values_350) - 1

    while left_350 <= right_350:
        middle_350 = (left_350 + right_350) // 2
        if values_350[middle_350] == target_350:
            return middle_350
        if values_350[middle_350] < target_350:
            left_350 = middle_350 + 1
        else:
            right_350 = middle_350 - 1

    return -1


def benchmark_binary_search_350(sizes_350, trials_350=5):
    """Measure the average time taken for binary search on sorted data."""
    results_350 = []

    for size_350 in sizes_350:
        data_350 = generate_random_data_350(size_350)

        sort_start_350 = time.perf_counter()
        sorted_data_350 = sorted(data_350)
        sort_end_350 = time.perf_counter()
        sort_time_350 = sort_end_350 - sort_start_350

        target_350 = sorted_data_350[-1] + 1

        total_time_350 = 0.0
        for _ in range(trials_350):
            start_350 = time.perf_counter()
            binary_search_350(sorted_data_350, target_350)
            end_350 = time.perf_counter()
            total_time_350 += end_350 - start_350

        average_time_350 = total_time_350 / trials_350
        results_350.append((size_350, sort_time_350, average_time_350))
        print(
            f"Binary Search | n = {size_350:>9} | sort time = {sort_time_350:.6f} sec "
            f"| avg search time = {average_time_350:.6f} sec"
        )

    return results_350


def main_350():
    input_sizes_350 = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]

    print("=" * 60)
    print("BINARY SEARCH - EMPIRICAL BENCHMARK")
    print("=" * 60)

    benchmark_binary_search_350(input_sizes_350, trials_350=5)


if __name__ == "__main__":
    main_350()