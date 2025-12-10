#!/usr/bin/env python3
import re
import sys
from itertools import product

INPUT_PATH = "input.txt"

def parse_line(line):
    m = re.search(r'\[([.#]+)\]', line)
    if not m:
        raise ValueError("No indicator diagram found in line: " + line)
    pattern = m.group(1)
    nlights = len(pattern)
    buttons = re.findall(r'\(([0-9,]*)\)', line)
    toggle_vectors = []
    for b in buttons:
        if b.strip() == "":
            toggle_vectors.append([0]*nlights)
            continue
        idxs = list(map(int, b.split(',')))
        vec = [0]*nlights
        for i in idxs:
            if i < 0 or i >= nlights:
                raise ValueError(f"Button index {i} out of range for line: {line}")
            vec[i] = 1
        toggle_vectors.append(vec)
    target = [1 if c == '#' else 0 for c in pattern]
    return nlights, toggle_vectors, target

def gf2_solve_min_weight(A_cols, b):
    if not A_cols:
        return 0 if all(x==0 for x in b) else None
    m = len(A_cols[0])
    n = len(A_cols)
    rows_bits = [0]*m
    for j, col in enumerate(A_cols):
        for i, bit in enumerate(col):
            if bit:
                rows_bits[i] |= (1 << j)
    rhs = [int(bit) for bit in b]
    pivot_row_for_col = {}
    pivot_col_for_row = {}
    r = 0
    for col in range(n):
        sel = None
        for i in range(r, m):
            if (rows_bits[i] >> col) & 1:
                sel = i
                break
        if sel is None:
            continue
        if sel != r:
            rows_bits[sel], rows_bits[r] = rows_bits[r], rows_bits[sel]
            rhs[sel], rhs[r] = rhs[r], rhs[sel]
        pivot_row_for_col[col] = r
        pivot_col_for_row[r] = col
        for i in range(m):
            if i != r and ((rows_bits[i] >> col) & 1):
                rows_bits[i] ^= rows_bits[r]
                rhs[i] ^= rhs[r]
        r += 1
        if r == m:
            break
    for i in range(r, m):
        if rows_bits[i] == 0 and rhs[i] == 1:
            return None
    x0 = [0]*n
    for col, row in pivot_row_for_col.items():
        x0[col] = rhs[row]
    free_cols = [c for c in range(n) if c not in pivot_row_for_col]
    nullspace = []
    for fc in free_cols:
        vec = [0]*n
        vec[fc] = 1
        for col, row in pivot_row_for_col.items():
            if (rows_bits[row] >> fc) & 1:
                vec[col] = 1
        nullspace.append(vec)
    k = len(nullspace)
    if k == 0:
        return sum(x0)
    best = None
    for mask in range(1 << k):
        x = x0.copy()
        for i in range(k):
            if (mask >> i) & 1:
                for j in range(n):
                    x[j] ^= nullspace[i][j]
        w = sum(x)
        if best is None or w < best:
            best = w
    return best

def solve_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        print("Error: file not found:", path)
        sys.exit(1)
    total = 0
    per = []
    for ln in lines:
        nlights, buttons, target = parse_line(ln)
        m = gf2_solve_min_weight(buttons, target)
        if m is None:
            print("No solution for line:", ln)
            sys.exit(1)
        per.append(m)
        total += m
    print("Per-machine minimum presses:", per)
    print("Total minimum presses:", total)

if __name__ == "__main__":
    solve_file(INPUT_PATH)
