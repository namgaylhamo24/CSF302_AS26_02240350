import time


# Task 5: input validation
# Every function below calls this first.
def check_input(a, b, m):
    if m <= 0:
        raise ValueError("Modulus must be a positive number")
    if b < 0:
        raise ValueError("Exponent cannot be negative")
    # A negative base is fine, a % m turns it into a number from 0 to m-1
    return a % m


# Task 1: naive method
# Multiply the base by itself b times, taking mod each time.
def naive_mod_pow(a, b, m):
    a = check_input(a, b, m)
    result = 1 % m          # if b = 0 the answer is 1 (and 0 when m = 1)
    for i in range(b):
        result = (result * a) % m
    return result


# Task 2: binary exponentiation (square and multiply)
# Idea: a^b = (a^2)^(b/2) when b is even, and a * a^(b-1) when b is odd.
# So we keep squaring a and halving b, which takes only about log2(b) steps.
def binary_mod_pow(a, b, m):
    a = check_input(a, b, m)
    result = 1 % m
    while b > 0:
        if b % 2 == 1:              # b is odd, so multiply result by a
            result = (result * a) % m
        a = (a * a) % m             # square the base
        b = b // 2                  # halve the exponent
    return result


# Task 4: same as above but using bitwise operations
# b & 1 checks if b is odd, b >> 1 divides b by 2.
def binary_mod_pow_bitwise(a, b, m):
    a = check_input(a, b, m)
    result = 1 % m
    while b > 0:
        if b & 1:
            result = (result * a) % m
        a = (a * a) % m
        b = b >> 1
    return result


# Task 3: compare the outputs
def compare_methods():
    tests = [
        (2, 10, 1000),
        (3, 0, 7),       # zero exponent
        (5, 3, 1),       # modulus 1
        (0, 5, 13),      # zero base
        (7, 1, 13),
        (-3, 5, 7),      # negative base
        (10, 100, 17),
        (12, 50, 97),
        (123, 456, 789),
    ]
    print("a, b, m | naive | binary | bitwise | python pow")
    for a, b, m in tests:
        r1 = naive_mod_pow(a, b, m)
        r2 = binary_mod_pow(a, b, m)
        r3 = binary_mod_pow_bitwise(a, b, m)
        r4 = pow(a, b, m)    # Python's built-in, used to double check
        same = (r1 == r2 == r3 == r4)
        print(a, b, m, "|", r1, "|", r2, "|", r3, "|", r4, "|", "OK" if same else "DIFFERENT")


# Task 5: show that bad input is handled
def test_bad_input():
    bad_inputs = [
        (2, -1, 5),    # negative exponent
        (2, 3, 0),     # modulus zero
        (2, 3, -5),    # negative modulus
    ]
    for a, b, m in bad_inputs:
        try:
            binary_mod_pow(a, b, m)
        except ValueError as error:
            print((a, b, m), "->", error)
    print("zero exponent: 9^0 mod 7 =", binary_mod_pow(9, 0, 7))
    print("negative base: (-3)^5 mod 7 =", binary_mod_pow(-3, 5, 7))


# Task 6: measure the time
def time_methods():
    a = 7
    m = 1000000007
    print("exponent | naive time | binary time")
    for b in [1000, 10000, 100000, 1000000, 10000000]:
        start = time.time()
        naive_mod_pow(a, b, m)
        naive_time = time.time() - start

        start = time.time()
        binary_mod_pow(a, b, m)
        binary_time = time.time() - start

        print(b, "|", round(naive_time, 6), "s |", round(binary_time, 8), "s")


if __name__ == "__main__":
    print("--- Compare outputs ---")
    compare_methods()
    print()
    print("--- Input validation ---")
    test_bad_input()
    print()
    print("--- Timing ---")
    time_methods()