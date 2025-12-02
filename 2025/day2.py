def find_invalid_ids(start, end):
    found = set()
    # Work with strings of start/end to know length bounds
    s_start = str(start)
    s_end = str(end)
    min_len = len(s_start)
    max_len = len(s_end)

    # Consider every total length between min and max
    for total_len in range(min_len, max_len + 1):
        # base_len must divide total_len and repeat_count r = total_len//base_len >= 2
        for base_len in range(1, total_len // 2 + 1):
            if total_len % base_len != 0:
                continue
            r = total_len // base_len

            # base must not have leading zeros: lowest base is 10**(base_len-1)
            low = 10 ** (base_len - 1)
            high = 10 ** base_len - 1

            for base in range(low, high + 1):
                s = str(base)
                val = int(s * r)
                if val < start:
                    continue
                if val > end:
                    # as base increases, val increases monotonically; break early
                    break
                found.add(val)

    return found

def main():
    all_invalid = []
    with open('day2.input', 'r') as file:
        for line in file:
            for id_string in line.rstrip('\n').split(','):
                if not id_string:
                    continue
                start_s, end_s = id_string.split('-')
                inv = find_invalid_ids(int(start_s), int(end_s))
                all_invalid.extend(inv)


    print(f"Total sum of invalid IDs: {sum(all_invalid)}")

if __name__ == '__main__':
    main()