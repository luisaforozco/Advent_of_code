
#!/usr/bin/env python3
import sys
import argparse
from typing import List
import numpy as np
import os

class DSU:
    def __init__(self, n: int):
        self.parent = np.arange(n, dtype=np.int32)
        self.size = np.ones(n, dtype=np.int64)
        self.components = n

    def find(self, x: int) -> int:
        # Path compression
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        # Union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

def parse_points(lines: List[str]) -> np.ndarray:
    pts = []
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        x, y, z = ln.split(",")
        pts.append((int(x), int(y), int(z)))
    return np.array(pts, dtype=np.int64)

def build_all_edges_sorted_by_dist2(pts: np.ndarray) -> np.ndarray:
    """
    Returns an array of shape (M, 3): [i, j, dist2], sorted by dist2 asc,
    for all unique pairs i<j. M = n*(n-1)/2.
    """
    n = len(pts)
    if n < 2:
        return np.empty((0, 3), dtype=np.int64)

    blocks: List[np.ndarray] = []
    for i in range(n - 1):
        diff = pts[i+1:] - pts[i]             # shape: (n-i-1, 3)
        d2 = np.sum(diff * diff, axis=1)      # shape: (n-i-1,)
        js = np.arange(i + 1, n, dtype=np.int32)
        is_col = np.full(js.shape, i, dtype=np.int32)
        block = np.column_stack((is_col, js, d2))
        blocks.append(block)
    edges = np.vstack(blocks)                  # shape: (M, 3)
    order = np.argsort(edges[:, 2], kind="mergesort")  # stable
    return edges[order]

def product_top3_component_sizes(dsu: DSU) -> int:
    n = len(dsu.parent)
    # Force-find to get final roots
    roots = [dsu.find(i) for i in range(n)]
    comp_size = {}
    for r in roots:
        comp_size[r] = dsu.size[r]
    sizes = sorted(comp_size.values(), reverse=True)
    if len(sizes) < 3:
        prod = 1
        for s in sizes:
            prod *= int(s)
        return prod
    return int(sizes[0] * sizes[1] * sizes[2])

def solve_part1(pts: np.ndarray, edges: np.ndarray, K: int) -> int:
    n = len(pts)
    if n == 0:
        return 0
    dsu = DSU(n)
    K = min(K, len(edges))
    for t in range(K):
        i, j, _ = edges[t]
        dsu.union(int(i), int(j))  # counts toward K even if already connected
    return product_top3_component_sizes(dsu)

def solve_part2(pts: np.ndarray, edges: np.ndarray) -> int:
    """
    Keep connecting the closest *unconnected* pairs until all boxes are in one circuit.
    Return the product of the X coordinates of the endpoints of the final effective union.
    """
    n = len(pts)
    if n <= 1:
        return 0  # nothing to connect
    dsu = DSU(n)
    last_i, last_j = None, None
    for i, j, _ in edges:
        if dsu.union(int(i), int(j)):  # only effective unions
            last_i, last_j = int(i), int(j)
            if dsu.components == 1:
                break
    if last_i is None:
        # Shouldn't happen unless input is empty or already fully connected
        return 0
    x_prod = int(pts[last_i][0]) * int(pts[last_j][0])
    return x_prod

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=1000, help="Number of closest pairs to process (Part 1)")
    ap.add_argument("--file", type=str, default=None, help="Path to input file (defaults to input_example.txt if present)")
    ap.add_argument("--part2", action="store_true", help="Solve Part 2 instead of Part 1")
    args = ap.parse_args()

    # Resolve input source: --file > input_example.txt (if exists) > stdin
    if args.file is not None:
        with open(args.file, "r", encoding="utf-8") as f:
            lines = f.read().strip().splitlines()
    else:
        default_path = os.path.join(os.path.dirname(__file__), "input_example.txt")
        if os.path.isfile(default_path):
            with open(default_path, "r", encoding="utf-8") as f:
                lines = f.read().strip().splitlines()
        else:
            lines = sys.stdin.read().strip().splitlines()

    pts = parse_points(lines)
    edges = build_all_edges_sorted_by_dist2(pts)

    if args.part2:
        ans = solve_part2(pts, edges)
    else:
        ans = solve_part1(pts, edges, args.k)

    print(ans)

if __name__ == "__main__":
    main()
