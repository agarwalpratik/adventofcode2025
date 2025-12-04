def is_invalid_id(n: int) -> bool:
    s = str(n)
    length = len(s)

    # Try all possible base pattern sizes
    for size in range(1, length // 2 + 1):
        if length % size == 0:
            pattern = s[:size]
            repeats = length // size

            if pattern * repeats == s and repeats >= 2:
                return True

    return False


# ---- READ INPUT FROM FILE ----
with open("input.txt", "r") as file:
    ranges_input = file.read().strip()

invalid_ids = []

for part in ranges_input.split(","):
    start, end = map(int, part.split("-"))

    for n in range(start, end + 1):
        if is_invalid_id(n):
            invalid_ids.append(n)

# ---- OUTPUT RESULTS ----
print("Invalid Product IDs Found:")
print(invalid_ids)

print("\nTotal Invalid IDs:", len(invalid_ids))
print("Sum of Invalid IDs:", sum(invalid_ids))
