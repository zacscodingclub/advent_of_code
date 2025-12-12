from collections import deque


def parse_input(filename: str = 'day11.input') -> dict:
    """Parse the input file into a directed graph (adjacency list)."""
    adj: dict[str, list[str]] = {}
    with open(filename, 'r') as fh:
        for line in fh:
            line = line.strip()
            if not line or ':' not in line:
                continue
            name, rest = line.split(':', 1)
            name = name.strip()
            neighbors = [tok for tok in rest.split() if tok]
            adj[name] = neighbors
            for n in neighbors:
                adj.setdefault(n, [])
    adj.setdefault('out', [])
    return adj


def topological_sort(adj: dict) -> list:
    """Return nodes in topological order (sources first)."""
    in_degree = {n: 0 for n in adj}
    for src, dests in adj.items():
        for d in dests:
            in_degree[d] = in_degree.get(d, 0) + 1

    queue = deque([n for n, deg in in_degree.items() if deg == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for nbr in adj.get(node, []):
            in_degree[nbr] -= 1
            if in_degree[nbr] == 0:
                queue.append(nbr)

    return order


def count_all_paths_dag(adj: dict, start: str, target: str) -> int:
    """Count all paths from start to target in a DAG using DP. O(V + E)."""
    topo = topological_sort(adj)
    paths_to = {n: 0 for n in adj}
    paths_to[start] = 1

    for node in topo:
        if paths_to[node] == 0:
            continue
        for nbr in adj.get(node, []):
            paths_to[nbr] += paths_to[node]

    return paths_to.get(target, 0)


def main():
    graph = parse_input()

    # DAG path counting: paths(svr->fft) * paths(fft->dac) * paths(dac->out)
    seg1 = count_all_paths_dag(graph, 'svr', 'fft')
    seg2 = count_all_paths_dag(graph, 'fft', 'dac')
    seg3 = count_all_paths_dag(graph, 'dac', 'out')

    print(f'total paths through svr -> fft -> dac -> out: {seg1 * seg2 * seg3}')


if __name__ == '__main__':
    main()
