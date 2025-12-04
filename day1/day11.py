def find_password_from_file(filename):
    dial = 50   # Starting position
    count_zero = 0

    with open(filename, "r") as file:
        for line in file:
            move = line.strip()
            if not move:
                continue  # Skip empty lines

            direction = move[0]
            steps = int(move[1:])

            if direction == 'L':
                dial = (dial - steps) % 100
            elif direction == 'R':
                dial = (dial + steps) % 100

            if dial == 0:
                count_zero += 1

    return count_zero


# ---- FILE INPUT ----
filename = "input.txt"
password = find_password_from_file(filename)
print("Password:", password)
