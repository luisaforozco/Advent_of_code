from typing import Dict, List, Tuple
from collections import defaultdict
import sys


def parse_input(data: str) -> Dict[str, List[str]]:
    """Parse lines of the form 'node: a b c' into an adjacency dict."""
    graph: Dict[str, List[str]] = defaultdict(list)
    for line in data:
        if not line: continue
        if ':' not in line:
            graph.setdefault(line, [])
            continue
        name, rhs = line.split(':', 1)
        outs = rhs.strip().split() if rhs.strip() else []
        graph[name.strip()] = outs
    return dict(graph)

def find_all_paths(graph: Dict[str, List[str]], start: str = 'you', end: str = 'out') -> List[List[str]]:
    """Return all simple paths (no repeated nodes) from start to end using DFS."""
    paths: List[List[str]] = []

    def dfs(node: str, path: List[str], visited: set):
        if node == end:
            paths.append(path.copy())
            return
        for nxt in graph.get(node, []):
            if nxt in visited:
                continue
            visited.add(nxt)
            path.append(nxt)
            dfs(nxt, path, visited)
            path.pop()
            visited.remove(nxt)

    # Initialize
    visited = {start}
    dfs(start, [start], visited)
    return paths


def solution_part_1(data: str) -> int:
    """Return the number of different simple paths from 'you' to 'out'."""
    graph = parse_input(data)
    paths = find_all_paths(graph, 'you', 'out')
    return len(paths)

def solution_part_2(data: str, start='svr', end='out', must_visit=('dac', 'fft')) -> Tuple[int, int]:
    graph = parse_input(data)
    dac, fft = must_visit
    memo = {}

    def dfs(node: str, seen_dac: bool, seen_fft: bool) -> Tuple[int, int]:
        # Returns (total_paths, paths_with_both)
        key = (node, seen_dac, seen_fft)
        if key in memo:
            return memo[key]

        if node == end:
            # If we reached end, count path
            total = 1
            with_both = 1 if seen_dac and seen_fft else 0
            memo[key] = (total, with_both)
            return memo[key]

        total_paths = 0
        both_paths = 0
        for nxt in graph.get(node, []):
            nd = seen_dac or (nxt == dac)
            nf = seen_fft or (nxt == fft)
            t, b = dfs(nxt, nd, nf)
            total_paths += t
            both_paths += b

        memo[key] = (total_paths, both_paths)
        return memo[key]

    return dfs(start, start == dac, start == fft)


def format_path(path: List[str]) -> str:
    return " -> ".join(path)

def _self_test():
    EXAMPLE = """aaa: you hhh
        you: bbb ccc
        bbb: ddd eee
        ccc: ddd eee fff
        ddd: ggg
        eee: out
        fff: out
        ggg: out
        hhh: ccc fff iii
        iii: out
    """

    EXPECTED_PATHS_STR = {
        "you -> bbb -> ddd -> ggg -> out",
        "you -> bbb -> eee -> out",
        "you -> ccc -> ddd -> ggg -> out",
        "you -> ccc -> eee -> out",
        "you -> ccc -> fff -> out",
    }

    # Compute on example
    graph = parse_input(EXAMPLE)
    paths = find_all_paths(graph, 'you', 'out')
    paths_str = {format_path(p) for p in paths}
    count = solution_part_1(EXAMPLE)

    print("Self-test on example input:")
    for p in sorted(paths_str):
        print(p)
    print(f"Total paths: {count}")

    # Assertions
    assert count == 5, f"Expected 5 paths, got {count}"
    assert paths_str == EXPECTED_PATHS_STR, "Path set doesn't match expected"
    print("✔ Tests passed.")


if __name__ == "__main__":
    with open('11/input.txt') as f:
        data = [line.rstrip('\n') for line in f.readlines()]
    #_self_test()
    #print(f"Result part 1: {solution_part_1(data)}")
    print(f"Result part 2: {solution_part_2(data)}")
    