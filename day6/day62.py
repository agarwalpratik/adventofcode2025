from functools import reduce
from operator import mul

def parse_and_solve(lines):
    lines = [ln.rstrip("\n") for ln in lines]
    if not lines:
        return 0, []

    nrows = len(lines)
    width = max(len(ln) for ln in lines)

    # Pad all lines to equal width
    padded = [ln.ljust(width, " ") for ln in lines]

    # Identify separator columns (columns that are all spaces)
    separator = [all(padded[r][c] == " " for r in range(nrows)) for c in range(width)]

    # Find problem blocks (non-separator column groups)
    blocks = []
    c = 0
    while c < width:
        if separator[c]:
            c += 1
            continue
        start = c
        while c < width and not separator[c]:
            c += 1
        end = c - 1
        blocks.append((start, end))

    results = []
    op_row = padded[-1]  # last row contains operators

    for (start, end) in blocks:
        # ✅ Extract digit columns RIGHT → LEFT
        numbers = []

        col = end
        while col >= start:
            digits = []
            for r in range(nrows - 1):  # ignore operator row
                ch = padded[r][col]
                if ch.strip():
                    digits.append(ch)

            if digits:
                # Most significant digit at top → bottom
                num = int("".join(digits))
                numbers.append(num)

            col -= 1

        # ✅ Read operator
        op = op_row[start:end+1].strip()[0]

        if op == "+":
            value = sum(numbers)
        elif op == "*":
            value = reduce(mul, numbers, 1)
        else:
            raise ValueError(f"Invalid operator '{op}'")

        results.append((numbers, op, value))

    grand_total = sum(v for (_, _, v) in results)
    return grand_total, results


def main():
    # ✅ READ FROM FILE
    with open("input.txt", "r") as file:
        data = file.read().splitlines()

    total, results = parse_and_solve(data)

    for idx, (nums, op, value) in enumerate(results, start=1):
        expr = f" {op} ".join(str(n) for n in nums)
        print(f"Problem {idx}: {expr} = {value}")

    print("-" * 40)
    print(f"Grand total: {total}")


if __name__ == "__main__":
    main()
