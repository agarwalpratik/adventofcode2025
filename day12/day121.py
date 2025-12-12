def parse_input(filename="input.txt"):
    with open(filename) as f:
        lines = [line.rstrip("\n") for line in f]

    shapes = {}
    i = 0

    # Parse shapes
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if ":" in line and line.split(":")[0].isdigit():
            idx = int(line.split(":")[0])
            i += 1
            block = []
            while i < len(lines) and lines[i].strip() not in [""] and ":" not in lines[i]:
                block.append(lines[i])
                i += 1
            shapes[idx] = block
        else:
            break

    # Parse regions
    regions = []
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        if ":" not in line:
            continue
        left, right = line.split(":")
        w, h = map(int, left.split("x"))
        counts = list(map(int, right.split()))
        regions.append((w, h, counts))

    return shapes, regions


def orientations(shape):
    """Return all distinct rotated/flipped versions and their widths/heights."""
    grids = set()

    grid = shape

    def rotate(g):
        return ["".join(g[::-1][r][c] for r in range(len(g)))
                for c in range(len(g[0]))]

    def flip(g):
        return [row[::-1] for row in g]

    work = grid
    for _ in range(4):
        work = rotate(work)
        grids.add(tuple(work))
        grids.add(tuple(flip(work)))

    sizes = []
    for g in grids:
        rows = len(g)
        cols = len(g[0])
        w = cols
        h = rows
        # bounding box of '#'
        xs = []
        ys = []
        for y in range(h):
            for x in range(w):
                if g[y][x] == "#":
                    xs.append(x)
                    ys.append(y)
        if xs:
            bw = max(xs) - min(xs) + 1
            bh = max(ys) - min(ys) + 1
            sizes.append((bw, bh))

    return sizes


def shape_area(shape):
    return sum(row.count("#") for row in shape)


def can_fit_region(W, H, shapes, counts):
    total_area = 0

    for idx, c in enumerate(counts):
        if c == 0:
            continue
        if idx not in shapes:
            return False

        shp = shapes[idx]
        area = shape_area(shp)
        total_area += area * c

        oris = orientations(shp)

        # Must fit at least one orientation
        fits = False
        for w, h in oris:
            if (w <= W and h <= H) or (w <= H and h <= W):
                fits = True
                break
        if not fits:
            return False

    # Area check
    return total_area <= W * H


def main():
    shapes, regions = parse_input("input.txt")
    count = 0
    for W, H, counts in regions:
        if can_fit_region(W, H, shapes, counts):
            count += 1
    print(count)


if __name__ == "__main__":
    main()
