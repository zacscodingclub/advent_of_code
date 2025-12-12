import re

def parse_line(line):
    """Parse a single machine line.

    Returns:
      - light_diagram: list of characters found inside the square brackets
      - wiring_schematics: list of lists of ints parsed from each parentheses group
      - joltage_requirements: list of ints parsed from the curly braces group
    """

    line = line.rstrip('\n')

    # Indicator light diagram: single [...] group
    m = re.search(r"\[([^\]]*)\]", line)
    if m:
        light_diagram_str = m.group(1)
        light_diagram = list(light_diagram_str)
    else:
        light_diagram = []

    # Wiring schematics: one or more (...) groups
    wiring_schematics = []
    for grp in re.findall(r"\(([^)]*)\)", line):
        # Skip empty groups
        if not grp.strip():
            wiring_schematics.append([])
            continue
        # parse numbers separated by commas and possibly spaces
        parts = [p.strip() for p in grp.split(',') if p.strip()]
        try:
            nums = [int(p) for p in parts]
        except ValueError:
            nums = []
        wiring_schematics.append(nums)

    # Joltage requirements: single {...} group with comma-separated ints
    joltage_requirements = []
    m2 = re.search(r"\{([^}]*)\}", line)
    if m2:
        contents = m2.group(1)
        parts = [p.strip() for p in contents.split(',') if p.strip()]
        try:
            joltage_requirements = [int(p) for p in parts]
        except ValueError:
            joltage_requirements = []

    return light_diagram, wiring_schematics, joltage_requirements

def parse_input(path):
    with open(path, 'r') as file:
        lines = [parse_line(line) for line in file]
    return lines


def solve_machine(light_diagram, wiring_schematics):
    """Solve A x = b over GF(2).

    light_diagram: list of '.' or '#' chars (length m)
    wiring_schematics: list of lists; each inner list contains zero-based indices toggled by that button (length n)

    Returns: tuple (solvable: bool, presses: list of 0/1 of length n or None)
    If solvable, returns one valid parity solution (0/1 per button). If multiple solutions exist, free vars set to 0.
    """
    m = len(light_diagram)
    n = len(wiring_schematics)

    # RHS vector b: 1 for '#', 0 for '.'
    b = [1 if c == '#' else 0 for c in light_diagram]

    # Build augmented matrix (m x (n+1)): rows = lights, cols = buttons
    # Entry (i,j) = 1 if button j toggles light i
    aug = [[0] * (n + 1) for _ in range(m)]
    for j, col in enumerate(wiring_schematics):
        for idx in col:
            if 0 <= idx < m:
                aug[idx][j] = 1
    for i in range(m):
        aug[i][n] = b[i]

    # Gaussian elimination over GF(2) to reduced row echelon form
    pivot_row = 0
    pivot_cols = {}
    for c in range(n):
        # find pivot
        pivot = None
        for r in range(pivot_row, m):
            if aug[r][c] == 1:
                pivot = r
                break
        if pivot is None:
            continue
        # swap
        aug[pivot_row], aug[pivot] = aug[pivot], aug[pivot_row]
        # eliminate other rows
        for r in range(m):
            if r != pivot_row and aug[r][c] == 1:
                # row r ^= pivot_row
                for k in range(c, n + 1):
                    aug[r][k] ^= aug[pivot_row][k]
        pivot_cols[c] = pivot_row
        pivot_row += 1
        if pivot_row >= m:
            break

    # Check for inconsistency: row of zeros in coefficients but RHS 1
    for r in range(m):
        if all(aug[r][c] == 0 for c in range(n)) and aug[r][n] == 1:
            return False, None

    # Identify free columns
    pivot_set = set(pivot_cols.keys())
    free_cols = [c for c in range(n) if c not in pivot_set]

    # For each assignment to free columns, compute pivot variables and pick minimal Hamming weight
    best = None
    max_enum = 1 << len(free_cols)
    # If too many free vars, fall back to the particular solution with free vars = 0
    if len(free_cols) > 20:
        presses = [0] * n
        for c, r in pivot_cols.items():
            presses[c] = aug[r][n] & 1
        return True, presses

    for mask in range(max_enum):
        x = [0] * n
        # set free vars according to mask
        for i, c in enumerate(free_cols):
            x[c] = (mask >> i) & 1
        # compute pivot vars using pivot rows: x[c] = aug[r][n] - sum_{j in free_cols} aug[r][j]*x[j]
        for c, r in pivot_cols.items():
            s = aug[r][n]
            for j in free_cols:
                if aug[r][j]:
                    s ^= x[j]
            x[c] = s & 1
        weight = sum(x)
        if best is None or weight < best[0]:
            best = (weight, x)
            if weight == 0:
                break

    return True, best[1]


def solve_joltage_ilp(wiring_schematics, joltage_requirements, timeout=None):
    """Solve integer program min sum(x_j) s.t. A x = b, x_j >= 0 integers using PuLP.

    Returns (solvable, presses_list, total)
    If PuLP isn't available, raises ImportError.
    """
    import pulp

    m = len(joltage_requirements)
    n = len(wiring_schematics)
    b = list(joltage_requirements)

    # quick infeasibility test: if any counter i has no buttons affecting it but b[i] > 0 -> infeasible
    touched = [False] * m
    for j, col in enumerate(wiring_schematics):
        for i in set(col):
            if 0 <= i < m:
                touched[i] = True
    for i in range(m):
        if not touched[i] and b[i] != 0:
            return False, None, 0

    # create LP
    prob = pulp.LpProblem("joltage", pulp.LpMinimize)
    # variables
    x = [pulp.LpVariable(f"x_{j}", lowBound=0, cat='Integer') for j in range(n)]
    # objective
    prob += pulp.lpSum(x)
    # constraints
    for i in range(m):
        coeffs = []
        for j, col in enumerate(wiring_schematics):
            if i in col:
                coeffs.append(x[j])
        prob += (pulp.lpSum(coeffs) == b[i])

    # optional timeout (seconds) for solver
    solver = None
    # Use CBC via PuLP; silence solver output with msg=False
    if timeout is not None:
        solver = pulp.PULP_CBC_CMD(timeLimit=int(timeout), msg=False)
    else:
        solver = pulp.PULP_CBC_CMD(msg=False)
    res = prob.solve(solver)

    # If solver reports infeasible, return quickly
    if hasattr(pulp, 'LpStatus') and pulp.LpStatus[prob.status] == 'Infeasible':
        return False, None, 0

    presses = [int(pulp.value(var)) if pulp.value(var) is not None else 0 for var in x]
    total = sum(presses)
    return True, presses, total

def main():
    data = parse_input('day10.input')
    total_presses = 0
    startable = 0
    not_startable = 0
    for i, (light_diagram, wiring_schematics, joltage_requirements) in enumerate(data, start=1):
        solvable, presses = solve_machine(light_diagram, wiring_schematics)
        if not solvable:
            not_startable += 1
            continue
        startable += 1
        total_presses += sum(presses)
    print(f"Lights mode: {startable} startable, {not_startable} not startable; total minimal presses: {total_presses}")

    # Now solve joltage configuration mode (ignore light diagrams)
    total_joltage = 0
    configured = 0
    not_configurable = 0
    no_requirements = 0
    for i, (light_diagram, wiring_schematics, joltage_requirements) in enumerate(data, start=1):
        if not joltage_requirements:
            no_requirements += 1
            continue
        # Use ILP solver (PuLP/CBC) — assumed available
        solvable_j, presses_j, total_j = solve_joltage_ilp(wiring_schematics, joltage_requirements, timeout=30)
        if not solvable_j:
            not_configurable += 1
            continue
        configured += 1
        total_joltage += total_j
    print(f"Joltage mode: {configured} configured, {not_configurable} not configurable, {no_requirements} had no requirements; total minimal presses: {total_joltage}")

if __name__ == '__main__':
    main()
