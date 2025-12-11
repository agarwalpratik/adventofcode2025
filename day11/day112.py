from collections import defaultdict
from functools import lru_cache

def solve():
    graph = defaultdict(list)

    # Read input graph
    with open("input.txt") as f:
        for line in f:
            if ":" not in line:
                continue
            a, b = line.split(":")
            src = a.strip()
            dsts = b.split()
            graph[src].extend(dsts)

    START = "svr"
    END = "out"
    A = "dac"
    B = "fft"

    # -----------------------
    # Memoized path counting
    # -----------------------

    @lru_cache(None)
    def count_paths(u, target):
        """Count total paths from u → target (no storing paths)."""
        if u == target:
            return 1
        total = 0
        for v in graph[u]:
            total += count_paths(v, target)
        return total

    # Count ways to reach A (dac) and B (fft)
    @lru_cache(None)
    def count_to(u, mid):
        """Count paths from u → mid."""
        if u == mid:
            return 1
        total = 0
        for v in graph[u]:
            total += count_to(v, mid)
        return total

    # Count ways A → B → out and B → A → out

    # svr → dac → fft → out
    paths_svr_dac = count_to(START, A)
    paths_dac_fft = count_to(A, B)
    paths_fft_out = count_paths(B, END)

    count_order1 = paths_svr_dac * paths_dac_fft * paths_fft_out

    # svr → fft → dac → out
    paths_svr_fft = count_to(START, B)
    paths_fft_dac = count_to(B, A)
    paths_dac_out = count_paths(A, END)

    count_order2 = paths_svr_fft * paths_fft_dac * paths_dac_out

    # Final answer
    result = count_order1 + count_order2

    print("Number of paths from svr to out that visit BOTH dac and fft:", result)


if __name__ == "__main__":
    solve()
