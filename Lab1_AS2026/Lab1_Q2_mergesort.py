"""Benchmark merge sort performance on randomly generated data."""

import random
import time


def generate_random_data_350(size_350):
    """Generate a list of random integers."""
    return [random.randint(0, size_350 * 10) for _ in range(size_350)]


def merge_350(left_350, right_350):
    """Merge two sorted lists into a single sorted list."""
    merged_350 = []
    left_index_350 = 0
    right_index_350 = 0

    while left_index_350 < len(left_350) and right_index_350 < len(right_350):
        if left_350[left_index_350] <= right_350[right_index_350]:
            merged_350.append(left_350[left_index_350])
            left_index_350 += 1
        else:
            merged_350.append(right_350[right_index_350])
            right_index_350 += 1

    merged_350.extend(left_350[left_index_350:])
    merged_350.extend(right_350[right_index_350:])
    return merged_350


def merge_sort_350(values_350):
    """Sort a list using the merge sort divide-and-conquer algorithm."""
    if len(values_350) <= 1:
        return values_350

    middle_350 = len(values_350) // 2
    left_half_350 = merge_sort_350(values_350[:middle_350])
    right_half_350 = merge_sort_350(values_350[middle_350:])

    return merge_350(left_half_350, right_half_350)


def benchmark_merge_sort_350(sizes_350, trials_350=3):
    """Measure the average time taken to run merge sort."""
    results_350 = []

    for size_350 in sizes_350:
        total_time_350 = 0.0
        for _ in range(trials_350):
            data_350 = generate_random_data_350(size_350)
            start_350 = time.perf_counter()
            merge_sort_350(data_350)
            end_350 = time.perf_counter()
            total_time_350 += end_350 - start_350

        average_time_350 = total_time_350 / trials_350
        results_350.append((size_350, average_time_350))
        print(f"Merge Sort | n = {size_350:>6} | avg time = {average_time_350:.6f} sec")

    return results_350


def main_350():
    input_sizes_350 = [100, 500, 1000, 2000, 4000, 8000]

    print("=" * 60)
    print("MERGE SORT - EMPIRICAL BENCHMARK")
    print("=" * 60)

    benchmark_merge_sort_350(input_sizes_350, trials_350=3)


if __name__ == "__main__":
    main_350()