from pprint import pprint

DIAL_START = 50

def spin_dial(start, direction, number):
    if number > 100:
        print(f'WOAH, big dog over here {number}')
    number = number % 99

    if direction == 'L':
        print(f'subtracting {start} - {number}')
        end = start - number        
    else:
        print(f'adding {start} + {number}')
        end = start + number

    if end < 0:
        # print(f'less than zero {end}, calculating')
        # 0, L, 5 => 0 - 5 = -5 => 95
        print(f'end < 0 {end}')
        end = end + 100
    elif end > 99:
        print(f'end > 99 {end}')
        # print(f'more than 99 {end}, calculating')
        # 95, R, 60 => 55 95 + 60 => 155
        end = end - 100
    return end 

    
def main():
    data = []
    with open('one.input', 'r') as file:
        for line in file:
            data.append(line.rstrip('\n'))
    
    current, count = 50, 0

    for d in data:
        print(f'=======================')
        print(f'checking {current}, {d}')
        current = spin_dial(current, d[0], int(d[1:]))
        #print(f'landed on {current}')
        if current == 0:
            # print(f'count going up! {count}')
            count += 1
    return count

print(f'landed on 0 {main()} times')