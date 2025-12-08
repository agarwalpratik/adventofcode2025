#!/usr/bin/env python3
from functools import lru_cache
import sys

def read_grid(filename="input.txt"):
    with open(filename, "r") as f:
        return [list(line.rstrip("\n")) for line in f]

def find_start_col(grid):
    for c, ch in enumerate(grid[0]):
        if ch == "S":
            return c
    raise ValueError("No starting point 'S' found in first row.")

def count_timelines(grid):
    rows = len(grid)
    cols = len(grid[0])
    start_col = find_start_col(grid)

    sys.setrecursionlimit(10000)

    @lru_cache(None)
    def paths_from(r, c):
        """
        r,c = current state meaning the particle is at row r,column c
        and on next step will try to move into grid[r+1][c].
        Return number of distinct timelines starting from this state.
        """
        r_next = r + 1
        # If next move exits the grid -> one timeline ends here
        if r_next >= rows:
            return 1
        # Out of horizontal bounds -> no timeline
        if c < 0 or c >= cols:
            return 0

        cell = grid[r_next][c]
        if cell == "." or cell == "S":
            # Move straight down
            return paths_from(r_next, c)
        elif cell == "^":
            # Split: particle (time) branches left and right starting from same row
            total = 0
            if c - 1 >= 0:
                total += paths_from(r_next, c - 1)
            if c + 1 < cols:
                total += paths_from(r_next, c + 1)
            return total
        else:
            # Any other character blocks the particle
            return 0

    return paths_from(0, start_col)

if __name__ == "__main__":
    grid = read_grid("input.txt")
    answer = count_timelines(grid)
    print(answer)
