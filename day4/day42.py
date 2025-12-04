from pathlib import Path

# ===== CONFIG =====
INPUT_FILE = "input4.txt"          # Your input file
OUTPUT_FILE = "final_grid.txt"     # Final grid after all removals

# ==================

# Load grid
grid = [list(line.strip()) for line in Path(INPUT_FILE).read_text().splitlines()]

h = len(grid)
w = len(grid[0])

# 8-direction neighbors
dirs = [
    (-1,-1), (-1,0), (-1,1),
    (0,-1),          (0,1),
    (1,-1),  (1,0),  (1,1)
]

total_removed = 0
rounds = 0
removed_each_round = []

while True:
    to_remove = []

    # Find all accessible rolls this round
    for i in range(h):
        for j in range(w):
            if grid[i][j] != '@':
                continue

            adj = 0
            for di, dj in dirs:
                ni, nj = i + di, j + dj
                if 0 <= ni < h and 0 <= nj < w:
                    if grid[ni][nj] == '@':
                        adj += 1

            if adj < 4:
                to_remove.append((i, j))

    # Stop when no more can be removed
    if not to_remove:
        break

    rounds += 1
    removed_each_round.append(len(to_remove))
    total_removed += len(to_remove)

    # Remove all marked rolls
    for i, j in to_remove:
        grid[i][j] = '.'

# Save final grid
final_grid = "\n".join("".join(row) for row in grid)
Path(OUTPUT_FILE).write_text(final_grid)

# ===== RESULTS =====
print("Grid size:", h, "x", w)
print("Total rounds:", rounds)
print("Total rolls removed:", total_removed)
print("Removed per round:", removed_each_round)
print("Final grid saved to:", OUTPUT_FILE)
