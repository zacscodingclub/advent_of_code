def parse_input(path):
    with open(path, 'r') as file:
        lines = [line.rstrip('\n') for line in file]
    return lines

def split_beams(rows):
    width = len(rows[0])
    beams = {rows[0].index('S')}
    total_created = 1
    splits = 0
    for i in range(1, len(rows)):
        row = rows[i]
        next_beams = set()

        for beam in beams:
            if beam < 0 or beam >= width:
                continue
            cell = row[beam]
            if cell == '^':
                # original beam stops; spawn left and right (they'll propagate starting next row)
                splits += 1
                for nb in (beam - 1, beam + 1):
                    if 0 <= nb < width:
                        next_beams.add(nb)
                        total_created += 1
            else:
                # beam continues downward
                next_beams.add(beam)

        beams = next_beams
    return len(beams), total_created, splits
    
def main():
    data = parse_input('day7.input')
    active, total, splits = split_beams(data)
    timelines = count_timelines(data)
    print(timelines)
    print(active)
    print(total)
    print(splits)
    return active

def count_timelines(rows):
    """Count timelines when a single quantum particle takes both branches at each splitter.

    Returns the total number of timelines active after processing the whole manifold.
    """
    from collections import defaultdict

    width = len(rows[0])
    counts = defaultdict(int)
    counts[rows[0].index('S')] = 1

    for row in rows[1:]:
        next_counts = defaultdict(int)
        for col, c in counts.items():
            if col < 0 or col >= width:
                continue
            if row[col] == '^':
                # each of the c timelines splits into left and right
                for nb in (col - 1, col + 1):
                    if 0 <= nb < width:
                        next_counts[nb] += c
            else:
                # timelines continue downward
                next_counts[col] += c
        counts = next_counts

    return sum(counts.values())

if __name__ == '__main__':
    print(main())
