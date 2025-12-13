#!/usr/bin/env python3
from itertools import combinations
from bisect import bisect_right, bisect_left
import sys

# ---------- Input parsing ----------
def parse_lines(lines):
    pts = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        x_str, y_str = s.split(',')
        pts.append((int(x_str), int(y_str)))
    return pts

# ---------- Build boundary set ----------
def build_boundary_set(red_pts):
    red_set = set(red_pts)
    boundary = set()
    xs = [x for x,_ in red_pts]
    ys = [y for _,y in red_pts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    n = len(red_pts)
    for i in range(n):
        x1,y1 = red_pts[i]
        x2,y2 = red_pts[(i+1) % n]
        if x1 == x2:
            y0,y1s = sorted((y1,y2))
            for y in range(y0, y1s+1):
                boundary.add((x1,y))
        elif y1 == y2:
            x0,x1s = sorted((x1,x2))
            for x in range(x0, x1s+1):
                boundary.add((x,y1))
        else:
            raise ValueError("Adjacent red tiles must share row or column")
    return red_set, boundary, (min_x, max_x, min_y, max_y)

# ---------- Merge contiguous xs into runs ----------
def merge_sorted_xs(xs):
    """xs: sorted list of ints. Return list of (start,end) inclusive merged runs."""
    if not xs:
        return []
    runs = []
    s = xs[0]
    e = xs[0]
    for x in xs[1:]:
        if x == e + 1:
            e = x
        else:
            runs.append((s,e))
            s = x
            e = x
    runs.append((s,e))
    return runs

# ---------- Build allowed intervals per row ----------
def build_allowed_intervals_per_row(boundary_set, bbox):
    min_x, max_x, min_y, max_y = bbox
    intervals_by_row = {}  # y -> list of (start,end) inclusive, merged, sorted

    # Pre-group boundary x positions by row
    boundary_by_row = {}
    for x,y in boundary_set:
        if y < min_y or y > max_y:
            continue
        boundary_by_row.setdefault(y, []).append(x)

    # For each row in bbox, compute allowed intervals
    for y in range(min_y, max_y+1):
        xs = boundary_by_row.get(y)
        if not xs:
            # no boundary on this row -> either fully outside or fully interior.
            # But for a simple closed orthogonal polygon this is rare; skip (no allowed)
            intervals_by_row[y] = []
            continue
        xs.sort()
        runs = merge_sorted_xs(xs)  # boundary runs
        allowed = []
        # include boundary runs themselves
        for r in runs:
            allowed.append(r)
        # interior runs are between runs[0] and runs[1], runs[2] and runs[3], ...
        # i.e., between run[i].end+1 .. run[i+1].start-1 for i = 0,2,4,...
        for i in range(0, len(runs)-1, 2):
            left_end = runs[i][1]
            right_start = runs[i+1][0]
            if left_end + 1 <= right_start - 1:
                allowed.append((left_end+1, right_start-1))
        # merge allowed intervals (they may overlap or touch)
        if not allowed:
            intervals_by_row[y] = []
            continue
        allowed.sort()
        merged = []
        s,e = allowed[0]
        for a,b in allowed[1:]:
            if a <= e + 1:
                e = max(e,b)
            else:
                merged.append((s,e))
                s,e = a,b
        merged.append((s,e))
        intervals_by_row[y] = merged
    return intervals_by_row

# ---------- Check coverage of [x0..x1] by intervals on a row ----------
def row_covers_interval(intervals, x0, x1):
    # intervals: list of (s,e) sorted non-overlapping
    if not intervals:
        return False
    # find rightmost interval with start <= x0 using bisect on starts
    starts = [iv[0] for iv in intervals]
    i = bisect_right(starts, x0) - 1
    if i < 0:
        return False
    s,e = intervals[i]
    return e >= x1

# ---------- Main rectangle search ----------
def max_allowed_rectangle_area(red_pts, intervals_by_row):
    max_area = 0
    best = None
    # Precompute list of red points for combinations
    for (x1,y1),(x2,y2) in combinations(red_pts, 2):
        if x1 == x2 or y1 == y2:
            continue
        x0,x1g = sorted((x1,x2))
        y0,y1g = sorted((y1,y2))
        area = (x1g - x0 + 1) * (y1g - y0 + 1)
        if area <= max_area:
            continue
        ok = True
        # check each row quickly
        for y in range(y0, y1g+1):
            intervals = intervals_by_row.get(y)
            if not row_covers_interval(intervals, x0, x1g):
                ok = False
                break
        if ok:
            max_area = area
            best = ((x1,y1),(x2,y2))
    return max_area, best

# ---------- Solve ----------
def solve_from_lines(lines):
    red_pts = parse_lines(lines)
    red_set, boundary_set, bbox = build_boundary_set(red_pts)
    intervals_by_row = build_allowed_intervals_per_row(boundary_set, bbox)
    area, pair = max_allowed_rectangle_area(red_pts, intervals_by_row)
    return area, pair

# ---------- Entry point ----------
if __name__ == "__main__":

    with open("input.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
        if not any(line.strip() for line in lines):
            raise FileNotFoundError

    area, pair = solve_from_lines(lines)
    print(area)
    if pair:
        print("Corners:", pair[0], "and", pair[1])
