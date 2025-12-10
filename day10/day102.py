#!/usr/bin/env python3
"""
solve_joltage.py

Reads 'input.txt' from the current directory. Each non-empty line should be:
[pattern] (button...) (button...) ... {joltages...}

The script ignores the indicator-light pattern (square brackets) and uses the
button parentheses and curly braces (joltages) to solve the joltage-mode ILP:
  minimize sum(x_j)  subject to  A x = b, x >= 0 integer
per machine, and prints per-machine minima and the total.

Requires: pulp (install with `pip install pulp` if not present).
"""
import re
import sys
from pathlib import Path

try:
    import pulp
except Exception as e:
    print("This script requires 'pulp'. Install with: pip install pulp")
    raise

INPUT = Path("input.txt")
if not INPUT.exists():
    print("Error: input.txt not found in current folder.")
    sys.exit(1)

def parse_line(line):
    # ignore bracket pattern, parse button groups and joltage numbers
    # pattern in [..] is ignored here
    m = re.search(r'\[([.#]+)\]', line)
    # parse buttons (parentheses)
    buttons = re.findall(r'\(([0-9,]*)\)', line)
    # parse joltages in curly braces
    j = re.search(r'\{([0-9,\s-]+)\}', line)
    if j is None:
        raise ValueError("No {joltages} found in line: " + line)
    joltages = [int(s) for s in j.group(1).split(',') if s.strip()!='']
    m_counters = len(joltages)
    # build button columns
    A_cols = []
    for b in buttons:
        if b.strip() == '':
            vec = [0]*m_counters
        else:
            idxs = [int(s) for s in b.split(',') if s.strip()!='']
            vec = [0]*m_counters
            for idx in idxs:
                if idx < 0 or idx >= m_counters:
                    raise ValueError(f"Button index {idx} out of range (0..{m_counters-1}) in line: {line}")
                vec[idx] = 1
        A_cols.append(vec)
    return A_cols, joltages

def solve_machine(A_cols, b):
    n = len(A_cols)
    m = len(b)
    # Build matrix A as list of rows for convenience
    A_rows = [[A_cols[j][i] for j in range(n)] for i in range(m)]

    # LP variables: x_j >= 0 integers
    prob = pulp.LpProblem("joltage_min_presses", pulp.LpMinimize)
    x = [pulp.LpVariable(f"x_{j}", lowBound=0, cat="Integer") for j in range(n)]
    # objective
    prob += pulp.lpSum(x)
    # constraints: for each counter i, sum_j A[i,j]*x_j == b[i]
    for i in range(m):
        prob += (pulp.lpSum(A_rows[i][j] * x[j] for j in range(n)) == b[i])
    # solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    if pulp.LpStatus[prob.status] != "Optimal":
        return None  # infeasible or unbounded (shouldn't happen)
    val = int(pulp.value(prob.objective))
    # gather solution vector if you want:
    sol = [int(pulp.value(var)) for var in x]
    return val, sol

# read file
lines = [ln.strip() for ln in INPUT.read_text(encoding='utf-8').splitlines() if ln.strip()]
total = 0
per = []
solutions = []
for ln in lines:
    A_cols, b = parse_line(ln)
    res = solve_machine(A_cols, b)
    if res is None:
        print("No feasible solution for line:", ln)
        sys.exit(1)
    val, sol = res
    per.append(val)
    solutions.append(sol)
    total += val

# Output
for i, ln in enumerate(lines):
    print(f"Machine {i+1}: min presses = {per[i]}, example presses = {solutions[i]}")
print("Total minimum presses for all machines:", total)
