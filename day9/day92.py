def point_in_polygon(x, y, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]

        if y1 == y2:
            continue

        if y < min(y1, y2) or y >= max(y1, y2):
            continue

        xinters = (y - y1) * (x2 - x1) / (y2 - y1) + x1
        if xinters > x:
            inside = not inside

    return inside


def segment_intersects_rectangle(e1, e2, rx1, ry1, rx2, ry2):
    # Vertical segment
    x1, y1 = e1
    x2, y2 = e2

    if x1 == x2:
        x = x1
        if rx1 < x < rx2:
            return not (max(y1, y2) < ry1 or min(y1, y2) > ry2)

    # Horizontal segment
    if y1 == y2:
        y = y1
        if ry1 < y < ry2:
            return not (max(x1, x2) < rx1 or min(x1, x2) > rx2)

    return False


def solve(filename="input.txt"):
    reds = []
    with open(filename) as f:
        for line in f:
            x, y = map(int, line.strip().split(","))
            reds.append((x, y))

    n = len(reds)

    max_area = 0
    best = None

    for i in range(n):
        x1, y1 = reds[i]
        for j in range(i + 1, n):
            x2, y2 = reds[j]

            rx1, rx2 = min(x1, x2), max(x1, x2)
            ry1, ry2 = min(y1, y2), max(y1, y2)

            if rx1 == rx2 or ry1 == ry2:
                continue

            # ---- 1. Test rectangle center ----
            cx = (rx1 + rx2) / 2
            cy = (ry1 + ry2) / 2
            if not point_in_polygon(cx, cy, reds):
                continue

            # ---- 2. Test edge midpoints ----
            test_points = [
                ((rx1 + rx2) / 2, ry1 + 0.5),
                ((rx1 + rx2) / 2, ry2 - 0.5),
                (rx1 + 0.5, (ry1 + ry2) / 2),
                (rx2 - 0.5, (ry1 + ry2) / 2),
            ]

            failed = False
            for px, py in test_points:
                if not point_in_polygon(px, py, reds):
                    failed = True
                    break

            if failed:
                continue

            # ---- 3. Ensure no polygon edge slices through rectangle ----
            for k in range(n):
                e1 = reds[k]
                e2 = reds[(k + 1) % n]
                if segment_intersects_rectangle(e1, e2, rx1, ry1, rx2, ry2):
                    failed = True
                    break

            if failed:
                continue

            # ---- Rectangle is VALID ----
            area = (rx2 - rx1 + 1) * (ry2 - ry1 + 1)

            if area > max_area:
                max_area = area
                best = ((x1, y1), (x2, y2))

    print("\n✅ FINAL CORRECT ANSWER")
    print("Max rectangle area:", max_area)
    print("Best red corner pair:", best)


solve()
