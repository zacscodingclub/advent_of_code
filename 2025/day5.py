def parse_input(path):
    intervals = []
    available = []
    after_range = False
    with open(path, 'r') as file:
        for line in file:
            stripped = line.strip()
            if len(stripped) == 0:
                after_range = True
                continue

            if not after_range:
                left, right = stripped.split("-")
                i_left, i_right = int(left), int(right)
                intervals.append((i_left, i_right))
            else:
                available.append(int(stripped))

    return intervals, available


def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort()
    merged = []
    for l, r in intervals:
        if not merged or l > merged[-1][1] + 1:
            merged.append([l, r])
        else:
            merged[-1][1] = max(merged[-1][1], r)
    return merged


def count_fresh(merged, available):
    import bisect
    if not merged:
        return 0
    def total_fresh_ids(merged):
        """Return the total number of distinct IDs covered by the merged ranges.

        Each interval is inclusive, so an interval `a-b` contributes `b - a + 1` IDs.
        """
        total = 0
        for a, b in merged:
            total += (b - a + 1)
        return total

def main():
    try:
        intervals, available = parse_input('day5.input')
        merged = merge_intervals(intervals)
        print(total_fresh_ids(merged))
        return count_fresh(merged, available)
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    print(main())
