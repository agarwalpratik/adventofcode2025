from collections import defaultdict

def count_paths():
    graph = defaultdict(list)

    # Read input
    with open("input.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            left, right = line.split(":")
            node = left.strip()
            neighbors = right.strip().split()
            graph[node].extend(neighbors)

    start = "you"
    end = "out"

    # DFS to count all paths
    def dfs(node, visited):
        if node == end:
            return 1
        
        total = 0
        for nxt in graph[node]:
            # avoid cycles
            if nxt not in visited:
                total += dfs(nxt, visited | {nxt})
        return total

    return dfs(start, {start})


if __name__ == "__main__":
    print(count_paths())
