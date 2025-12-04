# Invalid Product ID Finder (File Input Version)
# Reads product ID ranges from input.txt

invalid_ids = []

# Read input from file
with open("input.txt", "r") as file:
    ranges_input = file.read().strip()

for part in ranges_input.split(","):
    start, end = map(int, part.split("-"))
    
    for n in range(start, end + 1):
        s = str(n)

        # Must be even-length and no leading zero
        if len(s) % 2 == 0 and s[0] != '0':
            half = len(s) // 2
            if s[:half] == s[half:]:
                invalid_ids.append(n)

# Output results
print("Invalid Product IDs Found:")
print(invalid_ids)

print("\nTotal Invalid IDs:", len(invalid_ids))
print("Sum of Invalid IDs:", sum(invalid_ids))
