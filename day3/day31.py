def max_two_digit_from_line(line: str) -> int:
    digits = [int(ch) for ch in line.strip() if ch.isdigit()]
    n = len(digits)

    max_val = -1
    for i in range(n):
        for j in range(i + 1, n):
            val = digits[i] * 10 + digits[j]
            if val > max_val:
                max_val = val

    return max_val


def solve(filename="input.txt"):
    total = 0

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                total += max_two_digit_from_line(line)

    print("Final Total Output Joltage:", total)


# Run the solution
solve()
