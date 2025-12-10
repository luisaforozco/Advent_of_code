def solution_part_1(data):
    best_pair_1, best_pair_2, area = brute_max_area(data)
    print(f"Best rectangle: {best_pair_1}, {best_pair_2}")
    return area

def brute_max_area(points):
    best = ((None,None),(None,None),0.0)
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i+1, n):
            x2, y2 = points[j]
            a = (abs(x2-x1)+1) * (abs(y2-y1)+1)
            if a > best[2]:
                best = (points[i], points[j], a)
    return best

#---- Part 2
from typing import List, Tuple

# ---- Geometry + helpers ----

def build_edges(poly: List[Tuple[int,int]]):
    """
    Build orthogonal polygon edges from ordered vertex list (wrap-around).
    Returns:
      horiz: list of horizontal edges as (y, x1, x2) with x1 <= x2
      vert:  list of vertical edges   as (x, y1, y2) with y1 <= y2
    """
    n = len(poly)
    horiz = []  # (y, x1, x2)
    vert  = []  # (x, y1, y2)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if y1 == y2:
            if x1 == x2:
                continue
            if x1 <= x2:
                horiz.append((y1, x1, x2))
            else:
                horiz.append((y1, x2, x1))
        elif x1 == x2:
            if y1 <= y2:
                vert.append((x1, y1, y2))
            else:
                vert.append((x1, y2, y1))
        else:
            raise ValueError("Polygon edges must be axis-aligned")
    return horiz, vert

def merge_intervals(intervals: List[Tuple[float,float]]) -> List[Tuple[float,float]]:
    if not intervals:
        return []
    intervals.sort()
    res = [list(intervals[0])]
    for a, b in intervals[1:]:
        if a <= res[-1][1]:
            if b > res[-1][1]:
                res[-1][1] = b
        else:
            res.append([a, b])
    return [(a, b) for a, b in res]

def horizontal_coverage(y: int, horiz, vert) -> List[Tuple[float,float]]:
    """
    Coverage of the horizontal line y by polygon (interior or boundary).
    Uses vertical edges for crossings (half-open rule) + adds colinear horizontal edges.
    Returns merged intervals [L, R] (closed coverage in practice).
    """
    xs = []
    for x, y1, y2 in vert:
        if y1 <= y < y2:      # half-open to handle vertices once
            xs.append(x)
    xs.sort()
    cov = []
    for i in range(0, len(xs), 2):
        if i + 1 < len(xs):
            cov.append((xs[i], xs[i+1]))
    # add horizontal boundary overlaps
    for yy, x1, x2 in horiz:
        if yy == y:
            cov.append((x1, x2))
    return merge_intervals(cov)

def vertical_coverage(x: int, horiz, vert) -> List[Tuple[float,float]]:
    """
    Coverage of the vertical line x by polygon (interior or boundary).
    Symmetric to horizontal_coverage.
    """
    ys = []
    for y, x1, x2 in horiz:
        if x1 <= x < x2:
            ys.append(y)
    ys.sort()
    cov = []
    for i in range(0, len(ys), 2):
        if i + 1 < len(ys):
            cov.append((ys[i], ys[i+1]))
    for xx, y1, y2 in vert:
        if xx == x:
            cov.append((y1, y2))
    return merge_intervals(cov)

def interval_contains(intervals: List[Tuple[float,float]], a: float, b: float) -> bool:
    if a > b:
        a, b = b, a
    for L, R in intervals:
        if L <= a and b <= R:
            return True
    return False

def rect_inside_polygon(a: Tuple[int,int], b: Tuple[int,int], horiz, vert) -> bool:
    """
    Check if the axis-aligned rectangle with opposite corners a, b
    lies fully within/on the orthogonal polygon defined by (horiz, vert).
    Criterion: all 4 sides lie within polygon coverage (boundary or interior).
    """
    x1, y1 = a
    x2, y2 = b
    minx, maxx = sorted((x1, x2))
    miny, maxy = sorted((y1, y2))

    # Horizontal sides y=miny and y=maxy must be covered across [minx, maxx]
    if not interval_contains(horizontal_coverage(miny, horiz, vert), minx, maxx):
        return False
    if not interval_contains(horizontal_coverage(maxy, horiz, vert), minx, maxx):
        return False

    # Vertical sides x=minx and x=maxx must be covered across [miny, maxy]
    if not interval_contains(vertical_coverage(minx, horiz, vert), miny, maxy):
        return False
    if not interval_contains(vertical_coverage(maxx, horiz, vert), miny, maxy):
        return False

    return True


def solution_part_2(points: List[Tuple[int,int]]) -> int:
    """
    Max inclusive area among rectangles whose interior+boundary
    is a subset of the polygon (boundary + interior).
    """
    horiz, vert = build_edges(points)
    n = len(points)
    best = 0
    for i in range(n):
        for j in range(i+1, n):
            if rect_inside_polygon(points[i], points[j], horiz, vert):
                area = (abs(points[i][0] - points[j][0]) + 1) * (abs(points[i][1] - points[j][1]) + 1)
                if area > best:
                    best = area
    return best

#---
        
if __name__ == "__main__":
    with open('9/input.txt') as f:
        data_pre = [line.rstrip('\n') for line in f.readlines()]
        data = []
        for line in data_pre:
            data.append(tuple(map(int, line.split(','))))

    #print(f"Part 1: {solution_part_1(data)}")
    print(f"Part 2: {solution_part_2(data)}")