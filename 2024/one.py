from collections import Counter

def part_one():
    column_a, column_b = [], []

    with open('one.input', 'r') as file:
        for line in file:
            sp = line.split(", ")
            column_a.append(sp[0])
            column_b.append(sp[1])

    sorted_a = sorted(column_a)
    sorted_b = sorted(column_b)

    cumulative = 0

    for i, el in enumerate(sorted_a):
        cumulative += abs(int(sorted_a[i]) - int(sorted_b[i]))
    
    print(cumulative)

def main():
    column_a, column_b = [], []

    with open('one.input', 'r') as file:
        for line in file:
            sp = line.split(", ")
            column_a.append(sp[0])
            column_b.append(sp[1].strip())

    counter_b = Counter(column_b)

    cumulative = 0

    # Calculate a total similarity score by adding up each number in the 
    # left list after multiplying it by the number of times that number 
    # appears in the right list.
    for i in column_a:
        print(f'searching for {i}... found {counter_b[i]} times')
        cumulative += int(i) * counter_b[i]
    
    print(cumulative)


main()