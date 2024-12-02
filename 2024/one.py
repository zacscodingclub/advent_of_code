def main():
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


main()