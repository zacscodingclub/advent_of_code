from pprint import pprint

XMAS = "XMAS"
MAS = "MAS"

def part_one():
    count = 0
    lookup = []
    with open('four.input', 'r') as file:
        for i, line in enumerate(file):
            lookup.append(list(line.strip()))
    # for line in data.split():
    #     lookup.append(list(line))
    # print(lookup)
                      
    for i, line in enumerate(lookup):
        line_length = len(line)
        for j in range(line_length):
            vertical = ""
            horizontal = ""
            diag_right = ""
            diag_left = ""
            # Status update print
            print(f'count: {count}, i: {i}, j: {j}')

            # check horizontal (foward and reverse)
            if j < line_length - 3:
                horizontal = "".join(line[j: j+4])
                print(f'horizontal: {horizontal}, reversed: {horizontal[::-1]}')
                if XMAS in horizontal or XMAS in horizontal[::-1]:
                    print('*** XMAS horizontal, count +=1')
                    count += 1

            # check diagonals
            if i < len(lookup) - 3 and j < line_length - 3:
                diag_right = "".join([
                    lookup[i][j],
                    lookup[i+1][j+1],
                    lookup[i+2][j+2],
                    lookup[i+3][j+3]
                ])
                print(f'diag_right: {diag_right}, reversed: {diag_right[::-1]}')
                if XMAS in diag_right or XMAS in diag_right[::-1]:
                    print('*** XMAS diag_right, count +=1')
                    count += 1
                
            if i < line_length - 3 and j > 2:
                diag_left = "".join([
                    lookup[i][j],
                    lookup[i+1][j-1],
                    lookup[i+2][j-2],
                    lookup[i+3][j-3]
                ])
                print(f'diag_left: {diag_left}, reversed: {diag_left[::-1]}')
                if XMAS in diag_left or XMAS in diag_left[::-1]:
                    print('*** XMAS diag_left, count +=1')
                    count += 1

            # check vertical (up and down)
            if i < len(lookup) - 3:
                vertical = "".join([
                    lookup[i][j],
                    lookup[i+1][j],
                    lookup[i+2][j],
                    lookup[i+3][j]
                ])
                print(f'vertical: {vertical}, reversed: {vertical[::-1]}')
                if XMAS in vertical or XMAS in vertical[::-1]:
                    print('*** XMAS vertical, count +=1')
                    count += 1
            
        print('')
    print(count)


def main(data):
    count = 0
    lookup = []
    with open('four.input', 'r') as file:
        for i, line in enumerate(file):
            lookup.append(list(line.strip()))
    # for line in data.split():
    #     lookup.append(list(line))
    print(lookup)
                      
    for i, line in enumerate(lookup):
        line_length = len(line)
        for j in range(line_length):
            # Status update print
            print(f'count: {count}, i: {i}, j: {j}')

            # check right
            if i < len(lookup) - 2 and j < line_length-2:
                diag_right = "".join([
                    lookup[i][j],
                    lookup[i+1][j+1],
                    lookup[i+2][j+2],
                ])
                diag_left = "".join([
                    lookup[i][j+2],
                    lookup[i+1][j+1],
                    lookup[i+2][j],
                ])
                print(f'diag_right: {diag_right}, reversed: {diag_right[::-1]}')
                print(f'diag_left: {diag_left}, reversed: {diag_left[::-1]}')
                if (MAS in diag_right or MAS in diag_right[::-1]) and (MAS in diag_left or MAS in diag_left[::-1]):
                    print("*** x-mas found")
                    count += 1



            
        print('')
    print(count)




test_input = '''
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
'''

test_input2 = '''
.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
'''

main(test_input)
