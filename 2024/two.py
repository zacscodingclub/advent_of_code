from pprint import pprint

def parse_integers_from_line(line):
    return list(map(int, line.split()))


def diff_list(lst, low, high):
    if not all(isinstance(x, int) for x in lst):
        raise ValueError("List must contain only integers")
     
    if len(lst) <= 1:
        return True

    for i in range(len(lst) - 1):
        diff = abs(lst[i+1] - lst[i])
        # Check if difference is less than 1 or greater than or equal to 4
        if diff < low or diff >= high:
            return False
        
    return True


def evaluate_line(line):
    is_increasing = all(line[i] < line[i+1] for i in range(len(line)-1))
    is_decreasing = all(line[i] > line[i+1] for i in range(len(line)-1))
    
    # print(f'checking line {line}')
    # print(f'is it increasing? {is_increasing}')
    # print(f'is it decreasing? {is_decreasing}')
    if is_increasing or is_decreasing:
        if diff_list(line, 1, 4):
            return True
        else:
            return False
    else:
        return False

def main():
    safe_lines = []
    data = []

    with open('two.input', 'r') as file:
        for line in file:
            data.append(parse_integers_from_line(line))

    pre_damper_lines = []
    for line in data:
        if evaluate_line(line):
            safe_lines.append(line)
        else:
            pre_damper_lines.append(line)

    for line in pre_damper_lines:
        dampers_needed = 0
     
        # walk through removing each element and evaluate it
        for i in range(len(line)):
            tmp = list(line)
            del tmp[i]
            print(f'i: {i}, {dampers_needed}, {line}, {tmp}')
            if evaluate_line(tmp):
                safe_lines.append(line)
                break

    print(len(safe_lines))



test_input = [
    [7, 6, 4, 2, 1],
    [1, 2, 7, 8, 9],
    [9, 7, 6, 2, 1],
    [1, 3, 2, 4, 5],
    [8, 6, 4, 4, 1],
    [1, 3, 6, 7, 9],
]


main()