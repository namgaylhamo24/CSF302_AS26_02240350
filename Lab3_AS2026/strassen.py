import random

# Strassen's Matrix Multiplication (n must be power of 2)

def split_350(m):
    n = len(m)
    mid = n // 2
    a11 = [row[:mid] for row in m[:mid]]
    a12 = [row[mid:] for row in m[:mid]]
    a21 = [row[:mid] for row in m[mid:]]
    a22 = [row[mid:] for row in m[mid:]]
    return a11, a12, a21, a22


def add_350(a, b):
    n = len(a)
    return [[a[i][j] + b[i][j] for j in range(n)] for i in range(n)]


def sub_350(a, b):
    n = len(a)
    return [[a[i][j] - b[i][j] for j in range(n)] for i in range(n)]


def combine_350(c11, c12, c21, c22):
    top = [r1 + r2 for r1, r2 in zip(c11, c12)]
    bottom = [r1 + r2 for r1, r2 in zip(c21, c22)]
    return top + bottom


def strassen_350(a, b):
    n = len(a)
    if n == 1:
        return [[a[0][0] * b[0][0]]]

    a11, a12, a21, a22 = split_350(a)
    b11, b12, b21, b22 = split_350(b)

    m1 = strassen_350(add_350(a11, a22), add_350(b11, b22))
    m2 = strassen_350(add_350(a21, a22), b11)
    m3 = strassen_350(a11, sub_350(b12, b22))
    m4 = strassen_350(a22, sub_350(b21, b11))
    m5 = strassen_350(add_350(a11, a12), b22)
    m6 = strassen_350(sub_350(a21, a11), add_350(b11, b12))
    m7 = strassen_350(sub_350(a12, a22), add_350(b21, b22))

    c11 = add_350(sub_350(add_350(m1, m4), m5), m7)
    c12 = add_350(m3, m5)
    c21 = add_350(m2, m4)
    c22 = add_350(sub_350(add_350(m1, m3), m2), m6)

    return combine_350(c11, c12, c21, c22)


if __name__ == "__main__":
    n_350 = 4
    a_350 = [[random.randint(0, 9) for _ in range(n_350)] for _ in range(n_350)]
    b_350 = [[random.randint(0, 9) for _ in range(n_350)] for _ in range(n_350)]

    print("Matrix A:")
    for row in a_350:
        print(row)
    print("Matrix B:")
    for row in b_350:
        print(row)

    result_350 = strassen_350(a_350, b_350)
    print("A x B (Strassen):")
    for row in result_350:
        print(row)