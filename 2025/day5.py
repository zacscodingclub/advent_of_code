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
    starts = [iv[0] for iv in merged]
    count = 0
    for val in available:
        i = bisect.bisect_right(starts, val) - 1
        if i >= 0 and merged[i][0] <= val <= merged[i][1]:
            count += 1
    return count

def total_fresh_ids(merged):
    total = 0
    for a, b in merged:
        total += b + 1 - a
    return total


def main():
    intervals, available = parse_input('day5.input')
    merged = merge_intervals(intervals)
    print(total_fresh_ids(merged))
    return count_fresh(merged, available)

if __name__ == '__main__':
    print(main())
