from functools import reduce
from operator import mul

def parse_and_solve(lines):
    # remove trailing newlines
    lines = [ln.rstrip("\n") for ln in lines]
    if not lines:
        return 0, []

    # pad to same width
    width = max(len(ln) for ln in lines)
    padded = [ln.ljust(width, " ") for ln in lines]

    # identify separator columns (columns that are all spaces)
    nrows = len(padded)
    separator = [all(padded[r][c] == " " for r in range(nrows)) for c in range(width)]

    # find contiguous non-separator column ranges (blocks)
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
    # last line contains operators
    op_row = padded[-1]

    for (start, end) in blocks:
        nums = []
        for r in range(nrows - 1):
            segment = padded[r][start:end+1].strip()
            if segment != "":
                nums.append(int(segment))

        op_segment = op_row[start:end+1].strip()
        op = op_segment[0]

        if op == "+":
            value = sum(nums)
        elif op == "*":
            value = reduce(mul, nums, 1)
        else:
            raise ValueError(f"Invalid operator '{op}'")

        results.append((nums, op, value))

    grand_total = sum(v for (_, _, v) in results)
    return grand_total, results


def main():
    # ✅ READ INPUT FROM FILE
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
