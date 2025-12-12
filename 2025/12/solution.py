from typing import List, Tuple, Dict, Set
# ------------------------------
# Parse
# ------------------------------
def parse_puzzle(lines: str):
    shapes: Dict[int, List[str]] = {}
    regions: List[Tuple[int, int, List[int]]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line:
            i += 1
            continue
        if ":" in line and line.split(":")[0].strip().isdigit():
            idx = int(line.split(":")[0].strip())
            i += 1
            grid_rows = []
            while i < len(lines) and lines[i] and not (":" in lines[i] and lines[i].split(":")[0].strip().isdigit()):
                if "x" in lines[i] and ":" in lines[i] and lines[i].split(":")[0].count("x") == 1:
                    break
                # allow spaces inside shape lines (strip them)
                grid_rows.append(lines[i].replace(" ", ""))
                i += 1
            shapes[idx] = grid_rows
            continue
        else:
            break
    while i < len(lines):
        line = lines[i]
        if not line:
            i += 1
            continue
        if ":" in line and "x" in line.split(":")[0]:
            left, right = line.split(":", 1)
            w, h = [int(x) for x in left.strip().split("x")]
            counts = [int(x) for x in right.strip().split()] if right.strip() else []
            regions.append((w, h, counts))
        i += 1
    max_idx = max(shapes.keys()) if shapes else -1
    ordered_shapes = [shapes[k] for k in range(max_idx + 1)]
    return ordered_shapes, regions

# ------------------------------
# Geometry
# ------------------------------
def shape_cells_from_grid(grid_rows: List[str]) -> Set[Tuple[int, int]]:
    cells = set()
    for y, row in enumerate(grid_rows):
        for x, ch in enumerate(row):
            if ch == '#':
                cells.add((x, y))
    return cells

def normalize(cells: Set[Tuple[int, int]]):
    minx = min(x for x, _ in cells)
    miny = min(y for _, y in cells)
    return tuple(sorted(((x - minx, y - miny) for x, y in cells)))

def rotate90(cells: Set[Tuple[int, int]]):
    return set((-y, x) for x, y in cells)

def flip_x(cells: Set[Tuple[int, int]]):
    return set((-x, y) for x, y in cells)

def all_orientations(cells: Set[Tuple[int, int]]):
    seen = set()
    out = []
    base = cells
    variants = []
    for _ in range(4):
        variants.append(base)
        base = rotate90(base)
    for v in variants:
        for vv in (v, flip_x(v)):
            n = normalize(vv)
            if n not in seen:
                seen.add(n)
                out.append(n)
    return out

# ------------------------------
# Bitset DLX cache per (w,h)
# ------------------------------
class BoardModel:
    __slots__ = ("w","h","row_primary","row_cells","prim_rows_bits","conflict_masks")
    def __init__(self, w:int, h:int, row_primary:List[int], row_cells:List[Tuple[int,...]]):
        self.w = w; self.h = h
        self.row_primary = row_primary
        self.row_cells = row_cells
        # Build bitset indices
        n_rows = len(row_primary)
        self.prim_rows_bits: List[int] = []
        max_shape = max(row_primary) + 1 if row_primary else 0
        self.prim_rows_bits = [0] * max_shape
        for r, i in enumerate(row_primary):
            self.prim_rows_bits[i] |= (1 << r)
        # cells -> rows bitset
        cells_rows_bits = [0] * (w*h)
        for r, cells in enumerate(row_cells):
            bit = (1 << r)
            for c in cells:
                cells_rows_bits[c] |= bit
        # Precompute conflict mask per row: union of all rows sharing any cell
        self.conflict_masks = [0] * n_rows
        for r, cells in enumerate(row_cells):
            m = 0
            for c in cells:
                m |= cells_rows_bits[c]
            self.conflict_masks[r] = m  # includes r itself

PLACEMENT_CACHE: Dict[Tuple[int,int,Tuple[Tuple[str,...],...]], BoardModel] = {}

def enumerate_model(w:int, h:int, shapes:List[List[str]]) -> BoardModel:
    # Hash shapes by their normalized orientation lists to safely cache across calls
    shapes_cells = [shape_cells_from_grid(g) for g in shapes]
    orient_lists = [tuple(all_orientations(c)) for c in shapes_cells]
    shapes_key = tuple(tuple(rows) for rows in shapes)
    key = (w, h, shapes_key)
    if key in PLACEMENT_CACHE:
        return PLACEMENT_CACHE[key]

    row_primary: List[int] = []
    row_cells: List[Tuple[int, ...]] = []

    for i, orients in enumerate(orient_lists):
        for orient in orients:
            maxx = max(x for x, _ in orient)
            maxy = max(y for _, y in orient)
            # translations
            for ty in range(0, h - maxy):
                for tx in range(0, w - maxx):
                    cells_idx = []
                    for (ox, oy) in orient:
                        ax = tx + ox
                        ay = ty + oy
                        cells_idx.append(ay * w + ax)  # in-bounds guaranteed by maxx/maxy
                    row_primary.append(i)
                    row_cells.append(tuple(sorted(cells_idx)))

    model = BoardModel(w, h, row_primary, row_cells)
    PLACEMENT_CACHE[key] = model
    return model

# ------------------------------
# Bitset Algorithm-X with multiplicities
# ------------------------------
def can_fit_region_bits(w:int, h:int, counts:List[int], shapes:List[List[str]]) -> bool:
    # quick area bound
    areas = [len(shape_cells_from_grid(g)) for g in shapes]
    need_area = sum(areas[i] * (counts[i] if i < len(counts) else 0) for i in range(len(shapes)))
    if need_area > w*h:
        return False

    model = enumerate_model(w, h, shapes)
    n_shapes = max(model.row_primary)+1 if model.row_primary else len(shapes)
    req = counts[:] + [0] * (n_shapes - len(counts)) if len(counts) < n_shapes else counts[:n_shapes]

    # Shapes with zero requirement can be ignored in branching
    def choose_shape(active_mask:int) -> int:
        best_i = -1
        best_count = 1 << 30
        for i in range(n_shapes):
            if req[i] <= 0: continue
            c = (active_mask & model.prim_rows_bits[i]).bit_count()
            if c < best_count:
                best_count = c; best_i = i
                if c == 0: break
        return best_i

    # Early fail: any required shape has zero available placements initially
    init_mask = (1 << len(model.row_primary)) - 1
    for i in range(n_shapes):
        if req[i] > 0 and ((init_mask & model.prim_rows_bits[i]).bit_count() == 0):
            return False

    # recursion
    def search(active_mask:int) -> bool:
        # all requirements satisfied
        if all(rq <= 0 for rq in req):
            return True
        i = choose_shape(active_mask)
        if i == -1:  # nothing left but requirements not all zero
            return False
        avail = active_mask & model.prim_rows_bits[i]
        if avail == 0:
            return False

        # iterate set bits in 'avail' (low-bit popping)
        while avail:
            low = avail & -avail
            r = low.bit_length() - 1
            avail ^= low

            prev_mask = active_mask
            req[i] -= 1
            # deactivate r and all rows conflicting with it
            active_mask = active_mask & ~model.conflict_masks[r]
            if search(active_mask):
                return True
            # backtrack
            active_mask = prev_mask
            req[i] += 1
        return False

    return search(init_mask)

def solution_part_1(puzzle_text: str) -> int:
    shapes, regions = parse_puzzle(puzzle_text)
    total = 0
    for (w,h,counts) in regions:
        if len(counts) < len(shapes):
            counts = counts + [0]*(len(shapes)-len(counts))
        if can_fit_region_bits(w,h,counts,shapes):
            total += 1
    return total

if __name__ == "__main__":
    with open('12/input.txt') as f:
        data = [line.rstrip('\n') for line in f.readlines()]
    print(solution_part_1(data))
