import numpy as np
from math import prod

def solution_part_1(matrix):
    matrix = np.array(matrix)
    total = 0
    for i in range(np.shape(matrix)[1]):
        op = matrix[-1, i]
        col = matrix[:-1, i].astype(int)
        if op == '+':
            total += np.sum(col)
            print(np.sum(col))
        else:
            total += np.prod(col)
            print(np.prod(col))
    return total

# def transform_numbers(list_numbers):
#     max_len = max(len(s) for s in list_numbers)
#     new_list = []
#     print(f"{max_len=}")
#     for i in range(max_len-1, -1, -1):
#         new_num = ''
#         for num in list_numbers:
#             if len(num) > i: new_num += num[i]
#         print(new_num)
#         new_list.append(new_num)

#     return new_list


def solution_part_2_todo(matrix):
    matrix = np.array(matrix)
    total = 0
    for i in range(np.shape(matrix)[1]):
        transform_numbers(matrix[:-1, i])
        op = matrix[-1, i]


from functools import reduce
from operator import mul

def solution_part_2(lines):
    # keep spaces/tabs; strip only newlines
    lines = [ln.rstrip('\r\n') for ln in lines]
    # remove trailing blank lines
    while lines and lines[-1].strip() == '':
        lines.pop()
    if not lines:
        return 0

    # last row that contains an operator
    op_row = max(i for i, row in enumerate(lines) if any(ch in '+*' for ch in row))

    # rectangular grid up to operator row
    width = max(len(row) for row in lines[:op_row + 1])
    grid = [row.ljust(width) for row in lines[:op_row + 1]]
    R, C = op_row + 1, width  # rows 0..op_row; row R-1 is operator row

    def is_sep(c: int) -> bool:
        # separator = column that is whitespace in all rows
        return all(grid[r][c].isspace() for r in range(R))

    def col_digits(col: int) -> str:
        # digits from top to just above operator row
        return ''.join(ch for ch in (grid[r][col] for r in range(R - 1)) if ch.isdigit())

    total = 0
    c = 0
    while c < C:
        if is_sep(c):
            c += 1
            continue

        # one problem = contiguous non-separator columns
        start = c
        while c < C and not is_sep(c):
            c += 1
        cols = list(range(start, c))

        # operator column (exactly one in valid input)
        op_cols = [col for col in cols if grid[R - 1][col] in '+*']
        if len(op_cols) != 1:
            raise ValueError(f"Expected 1 operator in block {start}..{c-1}, found {len(op_cols)}")
        op_col = op_cols[0]
        op = grid[R - 1][op_col]

        # IMPORTANT: include the operator column as a number too
        nums = []
        for col in cols:
            ds = col_digits(col)
            if ds:
                nums.append(int(ds))

        if op == '+':
            total += sum(nums)
        else:
            acc = 1
            for v in nums:
                acc *= v
            total += acc

    return total


def debug_blocks(lines):
    lines = [ln.rstrip('\r\n') for ln in lines]
    while lines and lines[-1].strip() == '':
        lines.pop()
    width = max(len(row) for row in lines)
    # find op row
    op_row = max(i for i, row in enumerate(lines) if any(ch in '+*' for ch in row))
    grid = [row.ljust(width) for row in lines[:op_row + 1]]
    R, C = op_row + 1, width

    def is_sep(c): return all(grid[r][c].isspace() for r in range(R))
    def col_to_int(col):
        ds = ''.join(ch for ch in (grid[r][col] for r in range(R - 1)) if ch.isdigit())
        return int(ds) if ds else None

    c = 0
    k = 0
    while c < C:
        if is_sep(c):
            c += 1
            continue
        start = c
        while c < C and not is_sep(c):
            c += 1
        cols = list(range(start, c))
        op_cols = [col for col in cols if grid[R - 1][col] in '+*']
        op = grid[R - 1][op_cols[0]] if op_cols else '?'
        nums = [col_to_int(col) for col in cols if col not in op_cols]
        nums = [n for n in nums if n is not None]
        print(f"block #{k}: cols {start}-{c-1}, op={op}, nums={nums}")
        k += 1


if __name__ == "__main__":
    matrix = []
    with open('6/input_example.txt', 'r', encoding='utf-8') as f:
        for line in f:
            matrix.append(line.strip().split())

    #print(f"Part 1: {solution_part_1(matrix)}")

    # Part 2
    with open('6/input.txt', 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]

    print(f"Part 2: {solution_part_2(lines)}")
    debug_blocks(lines)