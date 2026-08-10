
import random
import time


def generate_random_data_350(size_350):
    """Generate a list of random integers."""
    return [random.randint(0, size_350 * 10) for _ in range(size_350)]


def linear_search_350(values_350, target_350):
    """Scan the list from left to right to find a target value."""
    for index_350, value_350 in enumerate(values_350):
        if value_350 == target_350:
            return index_350
    return -1


def benchmark_linear_search_350(sizes_350, trials_350=5):
    """Measure the average time taken for linear search."""
    results_350 = []

    for size_350 in sizes_350:
        data_350 = generate_random_data_350(size_350)
        target_350 = -1

        total_time_350 = 0.0
        for _ in range(trials_350):
            start_350 = time.perf_counter()
            linear_search_350(data_350, target_350)
            end_350 = time.perf_counter()
            total_time_350 += end_350 - start_350

        average_time_350 = total_time_350 / trials_350
        results_350.append((size_350, average_time_350))
        print(f"Linear Search | n = {size_350:>9} | avg time = {average_time_350:.6f} sec")

    return results_350


def main_350():
    input_sizes_350 = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]

    print("=" * 60)
    print("LINEAR SEARCH - EMPIRICAL BENCHMARK")
    print("=" * 60)

    benchmark_linear_search_350(input_sizes_350, trials_350=5)


if __name__ == "__main__":
    main_350()