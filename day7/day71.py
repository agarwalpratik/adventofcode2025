from collections import deque

def count_splits_from_file(filename="input.txt"):
    with open(filename, "r") as f:
        grid = [list(line.rstrip("\n")) for line in f]

    rows = len(grid)
    cols = len(grid[0])

    # Find the starting position S
    start_col = None
    for c in range(cols):
        if grid[0][c] == "S":
            start_col = c
            break

    if start_col is None:
        print("ERROR: No starting point 'S' found.")
        return

    # Each beam is represented as (row, col)
    queue = deque()
    queue.append((0, start_col))

    # ✅ CRITICAL FIX: Track visited beam states
    visited = set()

    split_count = 0

    while queue:
        r, c = queue.popleft()

        # Move beam downward
        r += 1

        # If beam exits the grid, stop it
        if r >= rows:
            continue

        # ✅ Prevent infinite reprocessing
        if (r, c) in visited:
            continue
        visited.add((r, c))

        cell = grid[r][c]

        if cell == "." or cell == "S":
            # Beam continues straight down
            queue.append((r, c))

        elif cell == "^":
            # ✅ Count valid split
            split_count += 1

            # Left beam
            if c - 1 >= 0:
                queue.append((r, c - 1))

            # Right beam
            if c + 1 < cols:
                queue.append((r, c + 1))

        # Any other character blocks the beam

    print("✅ Total tachyon beam splits:", split_count)


if __name__ == "__main__":
    count_splits_from_file("input.txt")
