"""Benchmark bubble sort performance on randomly generated data."""

import random
import time


def generate_random_data_350(size_350):
    """Generate a list of random integers."""
    return [random.randint(0, size_350 * 10) for _ in range(size_350)]


def bubble_sort_350(values_350):
    """Sort a list using the bubble sort algorithm."""
    data_350 = values_350.copy()
    length_350 = len(data_350)

    for index_350 in range(length_350 - 1):
        swapped_350 = False
        for position_350 in range(length_350 - 1 - index_350):
            if data_350[position_350] > data_350[position_350 + 1]:
                data_350[position_350], data_350[position_350 + 1] = data_350[position_350 + 1], data_350[position_350]
                swapped_350 = True
        if not swapped_350:
            break

    return data_350


def benchmark_bubble_sort_350(sizes_350, trials_350=3):
    """Measure the average time taken to run bubble sort."""
    results_350 = []

    for size_350 in sizes_350:
        total_time_350 = 0.0
        for _ in range(trials_350):
            data_350 = generate_random_data_350(size_350)
            start_350 = time.perf_counter()
            bubble_sort_350(data_350)
            end_350 = time.perf_counter()
            total_time_350 += end_350 - start_350

        average_time_350 = total_time_350 / trials_350
        results_350.append((size_350, average_time_350))
        print(f"Bubble Sort | n = {size_350:>6} | avg time = {average_time_350:.6f} sec")

    return results_350


def main_350():
    input_sizes_350 = [100, 500, 1000, 2000, 4000, 8000]

    print("=" * 60)
    print("BUBBLE SORT - EMPIRICAL BENCHMARK")
    print("=" * 60)

    benchmark_bubble_sort_350(input_sizes_350, trials_350=3)


if __name__ == "__main__":
    main_350()