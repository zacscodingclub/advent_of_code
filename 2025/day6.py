def parse_input(path):
    # Read all lines preserving spaces (we need column positions)
    with open(path, 'r') as file:
        lines = [line.rstrip('\n') for line in file]

    if not lines:
        return []

    nrows = len(lines)
    maxlen = max(len(l) for l in lines)
    # pad lines so character indexing is safe
    lines = [l.ljust(maxlen) for l in lines]

    # Determine which columns contain any non-space character
    col_nonspace = [any(lines[r][c] != ' ' for r in range(nrows)) for c in range(maxlen)]

    # Find contiguous spans of non-empty columns -> each span is one problem block
    groups = []
    c = 0
    while c < maxlen:
        if not col_nonspace[c]:
            c += 1
            continue
        start = c
        while c < maxlen and col_nonspace[c]:
            c += 1
        end = c - 1
        groups.append((start, end))

    problems = []
    for start, end in groups:
        # Within a block, each column (within start..end) that has any non-space
        # in the digit rows (all rows except the last) represents a number.
        number_cols = [col for col in range(start, end + 1) if any(lines[r][col] != ' ' for r in range(nrows - 1))]

        nums = []
        for col in number_cols:
            # Build the number by concatenating non-space chars from top to the row before the last
            digits = ''.join(lines[r][col] for r in range(nrows - 1) if lines[r][col] != ' ')
            if digits:
                nums.append(digits)

        # The operator for the problem is the (rightmost) non-space character in the bottom row of the block
        op = None
        for col in range(end, start - 1, -1):
            if lines[-1][col] != ' ':
                op = lines[-1][col]
                break

        if nums and op:
            # Keep order of numbers as found left-to-right within the block
            problems.append(tuple(nums + [op]))

    return problems

def evaluate_problem(problem):
    operator = problem[-1]
    problem = problem[:-1]
    int_problem = [int(x) for x in problem]

    if operator == "*":
        cur = 1
        for el in int_problem:
            cur *= el
    elif operator == "+":
        cur = 0
        for el in int_problem:
            cur += el
    return cur

def sum_problems(problems):
    total = 0
    for problem in problems:        
        
        total += evaluate_problem(problem)

    return total

def main():
    math_problems = parse_input('day6.input')
    total = sum_problems(math_problems)
    return total

if __name__ == '__main__':
    print(main())
