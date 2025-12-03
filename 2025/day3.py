
def calculate_joltage(bank, k=2):
    """
    Return the maximum number (as int) obtainable by choosing exactly `k` digits
    from `bank` (a string of digits) while preserving relative order and
    concatenating them.

    Uses a monotonic-stack greedy algorithm (O(n) time, O(n) space):
    iterate left->right, keep a stack of chosen digits; while the current
    digit is greater than stack top and we still can drop digits (enough
    remaining to reach k), pop the stack. Push current digit. At end, take
    the first k digits from the stack.
    """
    n = len(bank)
    if k <= 0:
        return 0
    if k >= n:
        # If k >= length, the best we can do is the whole bank
        return int(bank) if bank else 0

    stack = []
    # number of digits we are allowed to drop to reach k digits
    to_remove = n - k

    for c in bank:
        # while we can remove and top < current, pop to make room for larger
        while stack and to_remove > 0 and stack[-1] < c:
            stack.pop()
            to_remove -= 1
        stack.append(c)

    # If we still have removals left, drop from the end
    if to_remove > 0:
        stack = stack[: -to_remove]

    # Take first k digits and return as integer
    result = ''.join(stack[:k])
    return int(result)

def main():
    cumulative_joltage = 0
    with open('day3.input', 'r') as file:
        for line in file:
            j = calculate_joltage(line.rstrip('\n'), 12)
            cumulative_joltage += j
    print(cumulative_joltage)
    
main()

