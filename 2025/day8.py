class XYZCoordinate:
    def __init__(self, x=None, y=None, z=None):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __repr__(self):
        return f"XYZCoordinate(x={self.x}, y={self.y}, z={self.z})"


def parse_input(path):
    with open(path, 'r') as file:
        lines = [line.rstrip('\n') for line in file]
    data = [line.split(',') for line in lines]
    return [XYZCoordinate(d[0], d[1], d[2]) for d in data]


def solve(coords, K=1000):
    """Connect the K closest pairs among `coords` and return (result, top3_sizes).

    `coords` is a list of `XYZCoordinate`.
    """
    n = len(coords)
    import heapq

    # Use a max-heap (store negative distances) to keep K smallest pairs
    heap = []  # will store tuples (-dist, i, j)

    def sqdist(a: XYZCoordinate, b: XYZCoordinate) -> int:
        dx = a.x - b.x
        dy = a.y - b.y
        dz = a.z - b.z
        return dx*dx + dy*dy + dz*dz

    for i in range(n):
        ai = coords[i]
        for j in range(i+1, n):
            d = sqdist(ai, coords[j])
            if len(heap) < K:
                heapq.heappush(heap, (-d, i, j))
            else:
                if -heap[0][0] > d:
                    heapq.heapreplace(heap, (-d, i, j))

    # Extract pairs and sort ascending by distance
    pairs = [(-item[0], item[1], item[2]) for item in heap]
    pairs.sort()

    # Union-Find
    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return True

    for dist, i, j in pairs:
        union(i, j)

    # Compute component sizes
    comps = {}
    for i in range(n):
        r = find(i)
        comps[r] = comps.get(r, 0) + 1

    sizes = sorted(comps.values(), reverse=True)
    top3 = sizes[:3]
    from functools import reduce
    import operator
    result = reduce(operator.mul, top3, 1)
    return result, top3


def last_merge(coords):
    """Return (product, coord_a, coord_b, distance_sq) for the last
    pair that causes all coords to become a single connected component.
    """
    n = len(coords)

    def sqdist(a: XYZCoordinate, b: XYZCoordinate) -> int:
        dx = a.x - b.x
        dy = a.y - b.y
        dz = a.z - b.z
        return dx*dx + dy*dy + dz*dz

    # Build all pairs and sort by distance ascending
    pairs = []
    for i in range(n):
        ai = coords[i]
        for j in range(i+1, n):
            pairs.append((sqdist(ai, coords[j]), i, j))
    pairs.sort()

    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return True

    # Process pairs until the entire set is connected
    for d, i, j in pairs:
        merged = union(i, j)
        if merged:
            # check size of the root
            r = find(i)
            if size[r] == n:
                a = coords[i]
                b = coords[j]
                return a.x * b.x, a, b, d

    return None


def main():
   # When run as script, print both parts: K=1000 result and last merge product
    data = parse_input('day8.input')
    res1, top3 = solve(data, K=1000)
    print('After 1000 pairs: Top component sizes:', top3)
    print('After 1000 pairs: Result:', res1)

    last = last_merge(data)
    if last is not None:
        prod, a, b, d = last
        print('Final merge between:', a, 'and', b)
        print('Distance squared:', d)
        print('Product of X coordinates:', prod)
    else:
        print('All already connected or no merge occurred')


if __name__ == '__main__':
    main()
