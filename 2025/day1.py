from pprint import pprint

DIAL_START = 50

def spin_dial(start, direction, number):
    # Effective displacement on the 0..99 dial
    disp = number % 100

    if direction == 'L':
        end = start - disp
    else:
        end = start + disp

    if end < 0:
        end += 100
    elif end > 99:
        end -= 100

    # Count how many t in 1..k cause the dial to be at 0.
    # For R (increasing): position at t is (start + t) mod 100 -> hits 0 when t ≡ (100 - start) mod 100
    # For L (decreasing): position at t is (start - t) mod 100 -> hits 0 when t ≡ start mod 100
    if direction == 'R':
        offset = (100 - start) % 100
    else:
        offset = start % 100

    # If offset == 0, the first time to hit 0 is after 100 clicks
    if offset == 0:
        offset = 100

    if number < offset:
        passes_zero = 0
    else:
        passes_zero = 1 + (number - offset) // 100

    return end, passes_zero

    
def main():
    data = []
    with open('one.input', 'r') as file:
        for line in file:
            data.append(line.rstrip('\n'))
    current = DIAL_START
    total_zero_hits = 0

    for d in data:
        current, zp = spin_dial(current, d[0], int(d[1:]))
        total_zero_hits += zp

    return total_zero_hits


total = main()
print(f'total zero hits: {total}')