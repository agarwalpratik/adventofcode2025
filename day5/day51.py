def count_fresh_ingredients(filename="input.txt"):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")

    ranges = []
    i = 0

    # Read ranges until blank line
    while i < len(lines) and lines[i]:
        start, end = map(int, lines[i].split("-"))
        ranges.append((start, end))
        i += 1

    # Skip blank line
    i += 1

    # Read available ingredient IDs
    ingredients = list(map(int, lines[i:]))

    fresh_count = 0

    for ingredient in ingredients:
        for start, end in ranges:
            if start <= ingredient <= end:
                fresh_count += 1
                break  # No need to check other ranges

    print("Fresh Ingredients Count:", fresh_count)


# Run the function
count_fresh_ingredients()
