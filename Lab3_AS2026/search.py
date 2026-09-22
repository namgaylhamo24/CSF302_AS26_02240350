import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Menu-Driven Program: Binary Search vs Ternary Search


def generate_array_350(n):
    values = random.sample(range(1, n * 10 + 1), n)
    values.sort()
    return values


def binary_search_350(arr, key):
    lo, hi = 0, len(arr) - 1
    count_350 = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        count_350 += 1
        if arr[mid] == key:
            return mid, count_350
        count_350 += 1
        if arr[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, count_350


def ternary_search_350(arr, key):
    lo, hi = 0, len(arr) - 1
    count_350 = 0
    while lo <= hi:
        third = (hi - lo) // 3
        mid1 = lo + third
        mid2 = hi - third

        count_350 += 1
        if arr[mid1] == key:
            return mid1, count_350

        count_350 += 1
        if arr[mid2] == key:
            return mid2, count_350

        count_350 += 1
        if key < arr[mid1]:
            hi = mid1 - 1
        else:
            count_350 += 1
            if key > arr[mid2]:
                lo = mid2 + 1
            else:
                lo, hi = mid1 + 1, mid2 - 1
    return -1, count_350


def best_case_350(arr):
    n = len(arr)
    bs_key = arr[(n - 1) // 2]
    _, bs_count = binary_search_350(arr, bs_key)

    ts_key = arr[(n - 1) // 3]
    _, ts_count = ternary_search_350(arr, ts_key)

    return bs_count, ts_count


def worst_case_350(arr):
    missing_key = arr[-1] + 1
    _, bs_count = binary_search_350(arr, missing_key)
    _, ts_count = ternary_search_350(arr, missing_key)
    return bs_count, ts_count


def comparison_table_350(sizes):
    ns_350, bs_best_350, ts_best_350, bs_worst_350, ts_worst_350 = [], [], [], [], []
    print(f"{'n':>9} | {'BS best':>8} | {'TS best':>8} | {'BS worst':>9} | {'TS worst':>9}")
    for n_350 in sizes:
        arr_350 = generate_array_350(n_350)
        bs_b, ts_b = best_case_350(arr_350)
        bs_w, ts_w = worst_case_350(arr_350)
        ns_350.append(n_350)
        bs_best_350.append(bs_b)
        ts_best_350.append(ts_b)
        bs_worst_350.append(bs_w)
        ts_worst_350.append(ts_w)
        print(f"{n_350:>9} | {bs_b:>8} | {ts_b:>8} | {bs_w:>9} | {ts_w:>9}")

    plt.plot(ns_350, bs_worst_350, marker="o", label="Binary Search (worst)")
    plt.plot(ns_350, ts_worst_350, marker="s", label="Ternary Search (worst)")
    plt.xscale("log")
    plt.xlabel("n (log scale)")
    plt.ylabel("Comparisons")
    plt.title("Binary vs Ternary Search")
    plt.legend()
    plt.savefig("q3_search_comparison.png")

    # Analysis: Best case is 1 comparison for both. In the worst case,
    # Binary Search does fewer comparisons than Ternary Search for the
    # same n, since Binary halves the array each step (T(n)=T(n/2)+O(1))
    # while Ternary does 2 comparisons per step despite splitting into
    # thirds (T(n)=T(n/3)+O(2)), so 2*log3(n) ends up larger than log2(n).


def print_menu_350():
    print("""
1. Generate n sorted random numbers -> Array
2. Display Array
3. Search for a key using Binary Search
4. Search for a key using Ternary Search
5. Step count for best case
6. Step count for worst case
7. Step count comparison table
0. Exit""")


def main():
    arr_350 = []
    while True:
        print_menu_350()
        choice_350 = input("Enter choice: ").strip()

        if choice_350 == "1":
            n_350 = int(input("Enter n: "))
            arr_350 = generate_array_350(n_350)

        elif choice_350 == "2":
            print(arr_350)

        elif choice_350 == "3":
            key_350 = int(input("Enter key: "))
            idx, count = binary_search_350(arr_350, key_350)
            print(f"Index: {idx}, Comparisons: {count}")

        elif choice_350 == "4":
            key_350 = int(input("Enter key: "))
            idx, count = ternary_search_350(arr_350, key_350)
            print(f"Index: {idx}, Comparisons: {count}")

        elif choice_350 == "5":
            bs_count, ts_count = best_case_350(arr_350)
            print(f"Binary: {bs_count}, Ternary: {ts_count}")

        elif choice_350 == "6":
            bs_count, ts_count = worst_case_350(arr_350)
            print(f"Binary: {bs_count}, Ternary: {ts_count}")

        elif choice_350 == "7":
            comparison_table_350([10, 100, 1000, 10000, 100000, 1000000])

        elif choice_350 == "0":
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()