def find_password_method_click(rotations):
    dial = 50   # Starting position
    count_zero = 0

    for move in rotations:
        direction = move[0]
        steps = int(move[1:])

        for _ in range(steps):
            if direction == 'L':
                dial = (dial - 1) % 100
            elif direction == 'R':
                dial = (dial + 1) % 100

            # Count EVERY time it hits 0
            if dial == 0:
                count_zero += 1

    return count_zero


# ---- FILE INPUT SECTION ----
with open("input.txt", "r") as file:
    rotations = [line.strip() for line in file if line.strip()]

password = find_password_method_click(rotations)
print("New Password (Method 0x434C49434B):", password)
