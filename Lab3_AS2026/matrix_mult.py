import random
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from strassen import strassen_350

# Traditional Matrix Multiplication O(n^3) vs Strassen's Algorithm


def generate_matrix_350(n):
    return [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]


def traditional_350(a, b):
    n = len(a)
    c = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            total = 0
            for k in range(n):
                total += a[i][k] * b[k][j]
            c[i][j] = total
    return c


if __name__ == "__main__":
    sizes_350 = [2, 4, 8, 16, 32, 64, 128]
    trad_times_350 = []
    strassen_times_350 = []

    print(f"{'n':>5} | {'Traditional':>12} | {'Strassen':>12} | {'Match'}")
    for n_350 in sizes_350:
        a_350 = generate_matrix_350(n_350)
        b_350 = generate_matrix_350(n_350)

        start_350 = time.perf_counter()
        c1_350 = traditional_350(a_350, b_350)
        t1_350 = time.perf_counter() - start_350

        start_350 = time.perf_counter()
        c2_350 = strassen_350(a_350, b_350)
        t2_350 = time.perf_counter() - start_350

        match_350 = (c1_350 == c2_350)
        trad_times_350.append(t1_350)
        strassen_times_350.append(t2_350)

        print(f"{n_350:>5} | {t1_350:>12.6f} | {t2_350:>12.6f} | {match_350}")

    plt.plot(sizes_350, trad_times_350, marker="o", label="Traditional")
    plt.plot(sizes_350, strassen_times_350, marker="s", label="Strassen")
    plt.xlabel("Matrix size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Traditional vs Strassen Matrix Multiplication")
    plt.legend()
    plt.savefig("q1_matrix_mult_comparison.png")

    # Analysis: All results matched (correctness verified). Traditional
    # is faster than Strassen here since Strassen's recursion and extra
    # additions cost more than they save at these matrix sizes in Python.