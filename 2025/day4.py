from typing import List, Tuple


def count_accessible(grid: List[str]) -> int:
    """Return the number of rolls '@' that have fewer than 4 adjacent '@'s.

    grid: list of equal-length strings consisting of '.' and '@'
    """
    if not grid:
        return 0
    rows = len(grid)
    cols = len(grid[0])
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '@':
                continue
            adj = 0
            for dr, dc in dirs:
                rr, cc = r + dr, c + dc
                if 0 <= rr < rows and 0 <= cc < cols and grid[rr][cc] == '@':
                    adj += 1
            if adj < 4:
                count += 1
    return count


def mark_accessible(grid: List[str]) -> List[str]:
    """Return a new grid where accessible rolls are replaced with 'x'."""
    rows = len(grid)
    if rows == 0:
        return []
    cols = len(grid[0])
    out = [list(row) for row in grid]
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '@':
                continue
            adj = 0
            for dr, dc in dirs:
                rr, cc = r + dr, c + dc
                if 0 <= rr < rows and 0 <= cc < cols and grid[rr][cc] == '@':
                    adj += 1
            if adj < 4:
                out[r][c] = 'x'
    return ["".join(row) for row in out]


def remove_accessible_once(grid: List[str]) -> Tuple[List[str], int]:
    """Remove all accessible rolls (adjacent < 4) in one pass.

    Returns the new grid and number removed in this pass.
    """
    rows = len(grid)
    if rows == 0:
        return [], 0
    cols = len(grid[0])
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    out = [list(row) for row in grid]
    to_remove = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '@':
                continue
            adj = 0
            for dr, dc in dirs:
                rr, cc = r + dr, c + dc
                if 0 <= rr < rows and 0 <= cc < cols and grid[rr][cc] == '@':
                    adj += 1
            if adj < 4:
                to_remove.append((r, c))
    for r, c in to_remove:
        out[r][c] = '.'
    return ["".join(row) for row in out], len(to_remove)


def total_removed(grid: List[str]) -> int:
    """Simulate repeated removals until no accessible rolls remain.

    Returns the total number of rolls removed.
    """
    cur = list(grid)
    total = 0
    while True:
        cur, removed = remove_accessible_once(cur)
        if removed == 0:
            break
        total += removed
    return total


def main():
    # sample from prompt
    sample = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@.",
    ]
    print("Sample total removed (expected 43):", total_removed(sample))

    # now puzzle input if available
    try:
        data = []
        with open('day4.input', 'r') as file:
            for line in file:
                data.append(line.rstrip('\n'))
        if data:
            print("Puzzle input accessible count:", count_accessible(data))
            print("Puzzle input total removed:", total_removed(data))
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    main()
