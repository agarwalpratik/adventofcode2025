#!/usr/bin/env python3
"""
Connect the 1000 pairs of junction boxes which are closest together.
Reads coordinates from 'input.txt' (one X,Y,Z per line).
Prints the product of the sizes of the three largest circuits after those 1000 connections.
"""

from itertools import combinations
import heapq
import math
import sys
from typing import List, Tuple

INPUT_FILE = "input.txt"
K = 1000  # number of closest pairs to connect

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        # path compression
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        # union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

def read_points(filename: str) -> List[Tuple[int,int,int]]:
    pts = []
    with open(filename, "r") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            parts = s.split(",")
            if len(parts) != 3:
                raise ValueError(f"bad line in input: {line!r}")
            x,y,z = map(int, parts)
            pts.append((x,y,z))
    return pts

def squared_dist(a: Tuple[int,int,int], b: Tuple[int,int,int]) -> int:
    dx = a[0]-b[0]
    dy = a[1]-b[1]
    dz = a[2]-b[2]
    return dx*dx + dy*dy + dz*dz

def main():
    pts = read_points(INPUT_FILE)
    n = len(pts)
    if n == 0:
        print("No points found in input.")
        return

    # If there are fewer than 2 points, trivial answer:
    if n < 2:
        sizes = [1] if n == 1 else []
        largest = sorted(sizes, reverse=True)[:3]
        prod = 1
        for s in largest:
            prod *= s
        print(prod)
        return

    # Generate all unordered pairs with squared distances as (dist, i, j).
    # Use heapq.nsmallest to get the K smallest pairs without sorting the whole list.
    pair_iter = ((squared_dist(pts[i], pts[j]), i, j) for i, j in combinations(range(n), 2))
    k = min(K, n*(n-1)//2)
    smallest_pairs = heapq.nsmallest(k, pair_iter, key=lambda t: t[0])

    dsu = DSU(n)
    # For clarity / debugging you might want to track how many unions actually changed components:
    unions_done = 0
    for dist_sq, i, j in smallest_pairs:
        if dsu.union(i, j):
            unions_done += 1
    # compute component sizes
    comp_sizes = {}
    for i in range(n):
        r = dsu.find(i)
        comp_sizes[r] = comp_sizes.get(r, 0) + 1
    sizes = sorted(comp_sizes.values(), reverse=True)
    # take top 3 sizes (if fewer than 3 components, treat missing as 1)
    top3 = sizes[:3]
    while len(top3) < 3:
        top3.append(1)
    prod = 1
    for s in top3:
        prod *= s

    print(prod)

if __name__ == "__main__":
    main()
