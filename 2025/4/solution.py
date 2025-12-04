import copy
import numpy as np

def solution_part_1(matrix):
    res = copy.deepcopy(matrix) # debug
    count = 0
    for i in range(len(matrix)):          # rows
        for j in range(len(matrix[i])):   # columns
            if not matrix[i][j] == '@':
                continue
            n_adjacent_rolls = 0
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0: continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < len(matrix) and 0 <= nj < len(matrix[i]):
                        if matrix[ni][nj] == '@':
                            n_adjacent_rolls += 1
                    if n_adjacent_rolls > 4:
                        break
            if n_adjacent_rolls < 4:
                count += 1
                res[i][j]='x' #debug
    #print(np.array(res)) # debug
    return count, res


def solution_part_2(matrix):
    count, matrix = solution_part_1(matrix)
    total = count
    while (count > 0):
        count, matrix = solution_part_1(matrix)
        total += count
    return total


if __name__ == "__main__":
    matrix = []
    with open('4/input.txt', 'r', encoding='utf-8') as f:
        for line in f:
            matrix.append(list(line.rstrip('\n')))

    print(f"Part 1: {solution_part_1(matrix)[0]}")
    print(f"Part 2: {solution_part_2(matrix)}")