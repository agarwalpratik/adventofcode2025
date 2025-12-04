# max_joltage_k.py
def max_k_subsequence_number(line: str, k: int) -> int:
    digits = [ch for ch in line.strip() if ch.isdigit()]
    n = len(digits)
    if n < k:
        raise ValueError(f"Line too short (n={n}) for k={k}")
    res = []
    start = 0
    for remaining in range(k, 0, -1):
        end = n - remaining  # inclusive
        # find index of maximum digit in digits[start:end+1]
        best_idx = start
        best_d = digits[start]
        # linear scan within window
        for i in range(start + 1, end + 1):
            d = digits[i]
            if d > best_d:
                best_d = d
                best_idx = i
                if best_d == '9':
                    break
        res.append(best_d)
        start = best_idx + 1
    return int(''.join(res))

def total_for_file(path: str, k: int = 12):
    total = 0
    count = 0
    with open(path, 'r') as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            val = max_k_subsequence_number(s, k)
            total += val
            count += 1
    return count, total

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    count, total = total_for_file(path, k)
    print(f"Processed banks: {count}")
    print(f"Sum of maxima (k={k}): {total}")
