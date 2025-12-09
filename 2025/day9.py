class Coordinate:
    def __init__(self, x=None, y=None):
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return f"Coordinate(x={self.x}, y={self.y})"

def parse_input(path):
    with open(path, 'r') as file:
        lines = [line.rstrip('\n') for line in file]
    # ignore empty lines
    lines = [l for l in lines if l.strip()]
    data = [line.split(',') for line in lines]
    return [Coordinate(d[0], d[1]) for d in data]

def max_rectangle_area(points):
    n = len(points)
    if n < 2:
        return 0, None
    max_area = 0
    best_pair = None
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i+1, n):
            x2, y2 = points[j]
            # use inclusive tile counts: if corners are at x=2 and x=11,
            # width should be 10 tiles (11 - 2 + 1). Same for height.
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height
            if area > max_area:
                max_area = area
                best_pair = ((x1, y1), (x2, y2))
    return max_area, best_pair


def build_allowed_tiles(red_points):
    """Given an ordered list of red tiles (wrapping), build the set of allowed tiles
    (red and green). Green tiles include the straight segments between adjacent
    red tiles and any tiles inside the closed loop formed by those segments.
    """
    if not red_points:
        return set()
    red = set(red_points)
    n = len(red_points)
    boundary = set()
    for i in range(n):
        x1, y1 = red_points[i]
        x2, y2 = red_points[(i + 1) % n]
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                boundary.add((x1, y))
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                boundary.add((x, y1))
        else:
            raise ValueError("Adjacent red tiles must share a row or column")

    allowed = set(boundary) | red

    # Bounding box for flood fill (pad by 1 so we have an exterior starting point)
    bx_min = min(x for x, _ in boundary) - 1
    bx_max = max(x for x, _ in boundary) + 1
    by_min = min(y for _, y in boundary) - 1
    by_max = max(y for _, y in boundary) + 1

    # Flood fill from outside to identify outside tiles; anything not reached
    # and not part of the boundary is interior and therefore green.
    from collections import deque

    start = (bx_min, by_min)
    q = deque([start])
    visited = set()
    while q:
        x, y = q.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if (x, y) in boundary:
            continue
        if x < bx_min or x > bx_max or y < by_min or y > by_max:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) not in visited:
                q.append((nx, ny))

    # Any cell inside bbox that is not boundary and not visited is interior
    for x in range(bx_min + 1, bx_max):
        for y in range(by_min + 1, by_max):
            if (x, y) not in boundary and (x, y) not in visited:
                allowed.add((x, y))

    return allowed


def max_rectangle_area_allowed(red_points):
    """Compute largest axis-aligned rectangle whose opposite corners are red
    tiles and every tile inside (inclusive) is red or green according to the
    loop defined by red_points (which are ordered and wrap).
    Returns (area, ((x1,y1),(x2,y2)))
    """
    if not red_points:
        return 0, None

    # Build a compressed grid covering only coordinates relevant to the
    # boundary and small padding. Each compressed cell represents a rectangular
    # block of real integer coordinates; we'll compute how many real tiles in
    # each block are allowed, then use prefix sums to test rectangles in O(1).
    from bisect import bisect_right

    # Build boundary segments
    segs = []
    n = len(red_points)
    for i in range(n):
        x1, y1 = red_points[i]
        x2, y2 = red_points[(i + 1) % n]
        segs.append((x1, y1, x2, y2))

    xs = set()
    ys = set()
    for x, y in red_points:
        xs.add(x)
        xs.add(x + 1)
        ys.add(y)
        ys.add(y + 1)

    for x1, y1, x2, y2 in segs:
        if x1 == x2:
            ys.add(min(y1, y2))
            ys.add(max(y1, y2) + 1)
            xs.add(x1)
            xs.add(x1 + 1)
        elif y1 == y2:
            xs.add(min(x1, x2))
            xs.add(max(x1, x2) + 1)
            ys.add(y1)
            ys.add(y1 + 1)
        else:
            raise ValueError("Adjacent red tiles must share a row or column")

    minx = min(x for x, _ in red_points)
    maxx = max(x for x, _ in red_points)
    miny = min(y for _, y in red_points)
    maxy = max(y for _, y in red_points)
    xs.add(minx - 1)
    xs.add(maxx + 2)
    ys.add(miny - 1)
    ys.add(maxy + 2)

    xs = sorted(xs)
    ys = sorted(ys)

    # compressed cell counts
    nx = len(xs) - 1
    ny = len(ys) - 1
    grid = [[0] * nx for _ in range(ny)]

    # helper to find index for a coordinate
    def ix_of(x):
        return bisect_right(xs, x) - 1

    def iy_of(y):
        return bisect_right(ys, y) - 1

    # mark boundary cells
    for x1, y1, x2, y2 in segs:
        if x1 == x2:
            ix = ix_of(x1)
            ylo = min(y1, y2)
            yhi = max(y1, y2)
            iy0 = iy_of(ylo)
            iy1_idx = iy_of(yhi)
            for iy in range(iy0, iy1_idx + 1):
                grid[iy][ix] = 2
        else:
            iy = iy_of(y1)
            xlo = min(x1, x2)
            xhi = max(x1, x2)
            ix0 = ix_of(xlo)
            ix1_idx = ix_of(xhi)
            for ix in range(ix0, ix1_idx + 1):
                grid[iy][ix] = 2

    # flood fill from outside (0,0) should be outside because of padding
    from collections import deque
    q = deque()
    visited = [[False] * nx for _ in range(ny)]
    # find an outside starting cell: pick corner (0,0) if within bounds
    q.append((0, 0))
    while q:
        cy, cx = q.popleft()
        if cy < 0 or cy >= ny or cx < 0 or cx >= nx:
            continue
        if visited[cy][cx]:
            continue
        if grid[cy][cx] == 2:
            continue
        visited[cy][cx] = True
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q.append((cy + dy, cx + dx))

    # now compute cell allowed values (number of real integer tiles in cell if allowed, else 0)
    cell_vals = [[0] * nx for _ in range(ny)]
    for iy in range(ny):
        for ix in range(nx):
            if visited[iy][ix]:
                # outside -> not allowed
                continue
            # interior or boundary -> allowed
            dx = xs[ix + 1] - xs[ix]
            dy = ys[iy + 1] - ys[iy]
            cell_vals[iy][ix] = dx * dy

    # build prefix sums over cell_vals
    ps = [[0] * (nx + 1) for _ in range(ny + 1)]
    for iy in range(ny):
        row_sum = 0
        for ix in range(nx):
            row_sum += cell_vals[iy][ix]
            ps[iy + 1][ix + 1] = ps[iy][ix + 1] + row_sum

    def rect_all_allowed(x1, y1, x2, y2):
        ix1 = ix_of(min(x1, x2))
        ix2 = ix_of(max(x1, x2))
        iy1 = iy_of(min(y1, y2))
        iy2 = iy_of(max(y1, y2))
        # clamp
        ix1 = max(0, min(ix1, nx - 1))
        ix2 = max(0, min(ix2, nx - 1))
        iy1 = max(0, min(iy1, ny - 1))
        iy2 = max(0, min(iy2, ny - 1))
        area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        s = ps[iy2 + 1][ix2 + 1] - ps[iy1][ix2 + 1] - ps[iy2 + 1][ix1] + ps[iy1][ix1]
        return s == area

    best_area = 0
    best_pair = None
    n = len(red_points)
    for i in range(n):
        x1, y1 = red_points[i]
        for j in range(i + 1, n):
            x2, y2 = red_points[j]
            if x1 == x2 or y1 == y2:
                # allow thin rectangles (width or height 1)
                pass
            # compute inclusive area
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if area <= best_area:
                continue
            xlo, xhi = min(x1, x2), max(x1, x2)
            ylo, yhi = min(y1, y2), max(y1, y2)
            if rect_all_allowed(xlo, ylo, xhi, yhi):
                best_area = area
                best_pair = ((x1, y1), (x2, y2))

    return best_area, best_pair

def main():
    coords = parse_input('day9.input')
    points = [(c.x, c.y) for c in coords]
    area, pair = max_rectangle_area(points)
    print(f"Max rectangle area (unconstrained): {area}")
    if pair:
        print(f"Opposite corners: {pair[0]} and {pair[1]}")

    # Now compute the largest rectangle constrained to red+green tiles
    allowed_area, allowed_pair = max_rectangle_area_allowed(points)
    print(f"Max rectangle area (red+green constrained): {allowed_area}")
    if allowed_pair:
        print(f"Opposite corners (constrained): {allowed_pair[0]} and {allowed_pair[1]}")

if __name__ == '__main__':
    main()
