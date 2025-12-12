def parse_input(filename: str = 'day12.input') -> dict:
    with open(filename) as f:
        lines = f.read().strip().split('\n')

    shapes = {}
    regions = []
    current_index = None
    current_shape = []

    for line in lines:
        # Region line: WxH: quantities
        if 'x' in line and ':' in line and line.split(':')[0].strip().replace('x', '').isdigit():
            if current_index is not None and current_shape:
                shapes[current_index] = current_shape
                current_index = None
                current_shape = []

            dims, counts = line.split(':')
            width, height = map(int, dims.strip().split('x'))
            quantities = list(map(int, counts.strip().split()))
            regions.append({
                'width': width,
                'height': height,
                'quantities': quantities
            })
        # Shape header: index:
        elif ':' in line and line.split(':')[0].strip().isdigit():
            if current_index is not None and current_shape:
                shapes[current_index] = current_shape
            idx, rest = line.split(':', 1)
            current_index = int(idx)
            current_shape = []
            if rest.strip():
                current_shape.append(rest.strip())
        elif line.strip() and current_index is not None:
            current_shape.append(line)

    if current_index is not None and current_shape:
        shapes[current_index] = current_shape

    # Convert to coordinate sets, but we only need the size
    shape_sizes = {}
    for idx, lines in shapes.items():
        size = sum(line.count('#') for line in lines)
        shape_sizes[idx] = size

    return {'shape_sizes': shape_sizes, 'regions': regions}


def main():
    data = parse_input()
    shape_sizes = data['shape_sizes']

    print(f"Parsed {len(shape_sizes)} shapes: {shape_sizes}")
    print(f"Parsed {len(data['regions'])} regions")

    # If total cells needed <= area, it fits
    count = 0
    for i, region in enumerate(data['regions']):
        area = region['width'] * region['height']
        cells_needed = sum(shape_sizes[idx] * qty for idx, qty in enumerate(region['quantities']))
        fits = cells_needed <= area

        if fits:
            count += 1

        if i < 5 or i % 200 == 0:
            print(f"  Region {i+1}: {region['width']}x{region['height']}={area}, need {cells_needed} -> {'YES' if fits else 'NO'}")

    print(count)


if __name__ == '__main__':
    main()
