from itertools import combinations
import heapq

INPUT_FILE = "input.txt"

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

def read_points(filename):
    points = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                x, y, z = map(int, line.split(","))
                points.append((x, y, z))
    return points

def squared_dist(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return dx*dx + dy*dy + dz*dz

def main():
    points = read_points(INPUT_FILE)
    n = len(points)

    dsu = DSU(n)

    # Build all possible edges
    edges = []
    for i, j in combinations(range(n), 2):
        dist2 = squared_dist(points[i], points[j])
        edges.append((dist2, i, j))

    # Sort by distance
    edges.sort(key=lambda x: x[0])

    # Process edges until everything is connected
    for dist2, i, j in edges:
        if dsu.union(i, j):
            # If this union caused full connectivity, this is the FINAL edge
            if dsu.components == 1:
                x1 = points[i][0]
                x2 = points[j][0]
                print(x1 * x2)
                return

if __name__ == "__main__":
    main()
