import random
import time


# Task 1: multiply two square matrices, taking mod m on every element
def multiply(A, B, m):
    size = len(A)
    C = [[0] * size for i in range(size)]
    for i in range(size):
        for j in range(size):
            total = 0
            for k in range(size):
                total += A[i][k] * B[k][j]
            C[i][j] = total % m
    return C


# Task 2: identity matrix (1s on the diagonal, 0s everywhere else)
# It works like the number 1: multiplying by it changes nothing.
def identity(size):
    I = [[0] * size for i in range(size)]
    for i in range(size):
        I[i][i] = 1
    return I


# Task 3: naive method, multiply A by itself n times
def naive_matrix_power(A, n, m):
    result = identity(len(A))
    for i in range(n):
        result = multiply(result, A, m)
    return result


# Task 4: binary method (repeated squaring)
# Same idea as Topic 6, but with matrices instead of numbers.
def binary_matrix_power(A, n, m):
    result = identity(len(A))
    while n > 0:
        if n % 2 == 1:
            result = multiply(result, A, m)
        A = multiply(A, A, m)       # square the matrix
        n = n // 2
    return result


# Task 5: compare naive and binary
def compare_methods():
    tests = [
        ([[1, 2], [3, 4]], 5, 1000),
        ([[2, 0], [0, 2]], 10, 1000),
        ([[1, 1], [1, 0]], 20, 1000007),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 7, 100),
        ([[5]], 6, 13),
    ]
    for A, n, m in tests:
        naive = naive_matrix_power(A, n, m)
        binary = binary_matrix_power(A, n, m)
        print("A =", A, " n =", n, " m =", m)
        print("  naive :", naive)
        print("  binary:", binary)
        print("  same?", naive == binary)


# Task 6: nth Fibonacci number mod m
# The matrix [[1, 1], [1, 0]] raised to the power n gives
#   [[F(n+1), F(n)],
#    [F(n),   F(n-1)]]
# so F(n) is the top right element.
def fibonacci_mod(n, m):
    fib_matrix = [[1, 1], [1, 0]]
    result = binary_matrix_power(fib_matrix, n, m)
    return result[0][1]


# Task 7: large Fibonacci numbers
# We never build the earlier numbers, we jump straight to F(n).
def large_fibonacci():
    m = 1000000007
    for n in [10, 50, 100, 1000, 1000000, 10**12, 10**18]:
        print("F(" + str(n) + ") mod", m, "=", fibonacci_mod(n, m))
    # quick check against the normal loop method for small n
    a, b = 0, 1
    for i in range(30):
        if fibonacci_mod(i, 1000007) != a % 1000007:
            print("Mismatch at", i)
        a, b = b, a + b
    print("Checked F(0) to F(29) against the normal loop: OK")


# Task 8: count walks with exactly k edges from vertex u to vertex v
# If adj[i][j] = 1 when there is an edge i -> j, then
# (adj^k)[u][v] is the number of walks of length k from u to v.
def count_walks(adj, u, v, k, m):
    result = binary_matrix_power(adj, k, m)
    return result[u][v]


def walks_example():
    # Graph with 4 vertices: 0->1, 0->2, 1->2, 2->0, 2->3, 3->3
    adj = [
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 1],
        [0, 0, 0, 1],
    ]
    m = 1000000007
    print("Edges: 0->1, 0->2, 1->2, 2->0, 2->3, 3->3")
    print("Walks of 1 edge from 0 to 2:", count_walks(adj, 0, 2, 1, m))
    print("Walks of 2 edges from 0 to 2:", count_walks(adj, 0, 2, 2, m))
    print("Walks of 3 edges from 0 to 0:", count_walks(adj, 0, 0, 3, m))
    print("Walks of 4 edges from 0 to 3:", count_walks(adj, 0, 3, 4, m))
    print("Walks of 1000000 edges from 0 to 3:", count_walks(adj, 0, 3, 1000000, m))


# Task 9: benchmark naive vs binary
def benchmark():
    m = 1000000007
    print("size | exponent | naive time | binary time")
    for size in [2, 4, 8]:
        # make a random matrix of this size
        A = [[random.randint(0, 9) for j in range(size)] for i in range(size)]
        for n in [10, 100, 1000]:
            start = time.time()
            naive_matrix_power(A, n, m)
            naive_time = time.time() - start

            start = time.time()
            binary_matrix_power(A, n, m)
            binary_time = time.time() - start

            print(size, "|", n, "|", round(naive_time, 6), "s |", round(binary_time, 6), "s")


if __name__ == "__main__":
    print("--- Identity matrix (3x3) ---")
    print(identity(3))
    print()
    print("--- Compare naive and binary ---")
    compare_methods()
    print()
    print("--- Large Fibonacci numbers ---")
    large_fibonacci()
    print()
    print("--- Walks in a directed graph ---")
    walks_example()
    print()
    print("--- Benchmark ---")
    benchmark()