def count_total_fresh_ids(filename="input.txt"):
    ranges = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            # Stop reading when we hit the blank line
            if not line:
                break

            # Only process proper range lines
            if "-" in line:
                start, end = map(int, line.split("-"))
                ranges.append((start, end))

    # Sort ranges by starting point
    ranges.sort()

    merged = []
    for start, end in ranges:
        if not merged or start > merged[-1][1] + 1:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    # Count total unique IDs
    total_fresh = 0
    for start, end in merged:
        total_fresh += (end - start + 1)

    print("Total Fresh Ingredient IDs:", total_fresh)


# Run it
count_total_fresh_ids()
