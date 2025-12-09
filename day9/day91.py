def largest_rectangle_area(filename="input.txt"):
    points = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            x, y = map(int, line.split(","))
            points.append((x, y))

    print("POINTS READ FROM FILE:")
    print(points)
    print()

    max_area = 0
    best_pair = None

    n = len(points)

    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]

            if x1 == x2 or y1 == y2:
                continue

            area = abs(x1 - x2 + 1) * abs(y1 - y2 + 1)
            print(f"Checking {points[i]} & {points[j]} => Area = {area}")

            if area > max_area:
                max_area = area
                best_pair = ((x1, y1), (x2, y2))

    print("\nFINAL RESULT")
    print("Largest Rectangle Area:", max_area)
    print("Using Corner Tiles:", best_pair)


largest_rectangle_area()
