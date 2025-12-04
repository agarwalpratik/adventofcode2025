# Forklift Accessibility Checker
# A roll '@' is accessible if it has fewer than 4 adjacent '@' (8 directions)

def count_accessible_rolls(grid):
    h = len(grid)
    w = len(grid[0])

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    result_grid = [list(row) for row in grid]
    accessible_count = 0

    for i in range(h):
        for j in range(w):
            if grid[i][j] != '@':
                continue

            adjacent = 0
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < h and 0 <= nj < w and grid[ni][nj] == '@':
                    adjacent += 1

            if adjacent < 4:
                result_grid[i][j] = 'x'
                accessible_count += 1

    return ["".join(row) for row in result_grid], accessible_count


# --------- FILE INPUT VERSION ---------
if __name__ == "__main__":
    with open("input4.txt", "r") as file:
        grid = [line.strip() for line in file if line.strip()]

    marked_grid, answer = count_accessible_rolls(grid)

    # Print answer
    print("Accessible rolls:", answer)

    # Optional: Save marked output
    with open("output_marked.txt", "w") as out:
        out.write("\n".join(marked_grid))

    print("Marked grid saved to output_marked.txt")
