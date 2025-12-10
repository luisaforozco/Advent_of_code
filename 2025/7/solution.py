from collections import defaultdict

def solution_part_1(manifold):
    """
    Solves the first part of the puzzle.
    """
    start_row = -1
    start_col = -1
    for r, line in enumerate(manifold):
        if 'S' in line:
            start_row = r
            start_col = line.find('S')
            break

    if start_row == -1:
        print("Error: Starting position 'S' not found in the manifold.")
        return

    beams = {start_col}
    total_splits = 0
    height = len(manifold)
    width = len(manifold[0])

    for r in range(start_row + 1, height):
        next_beams = set()
        for c in beams:
            if 0 <= c < width:
                char = manifold[r][c]
                if char == '^':
                    total_splits += 1
                    next_beams.add(c - 1)
                    next_beams.add(c + 1)
                else:
                    next_beams.add(c)
        
        beams = next_beams
        if not beams:
            break

    print(f"Solution part 1: The total number of splits is: {total_splits}")


def solution_part_2(manifold):
    """
    Solves the second part of the puzzle.
    """
    start_row = -1
    start_col = -1
    for r, line in enumerate(manifold):
        if 'S' in line:
            start_row = r
            start_col = line.find('S')
            break

    if start_row == -1:
        print("Error: Starting position 'S' not found in the manifold.")
        return

    timelines = {start_col: 1}
    completed_timelines = 0
    height = len(manifold)
    width = len(manifold[0])

    for r in range(start_row + 1, height):
        next_timelines = defaultdict(int)
        for c, count in timelines.items():
            char = manifold[r][c]
            if char == '^':
                # Split left
                new_c_left = c - 1
                if 0 <= new_c_left < width:
                    next_timelines[new_c_left] += count
                else:
                    completed_timelines += count
                
                # Split right
                new_c_right = c + 1
                if 0 <= new_c_right < width:
                    next_timelines[new_c_right] += count
                else:
                    completed_timelines += count
            else:  # '.'
                next_timelines[c] += count
        
        timelines = next_timelines
        if not timelines:
            break
            
    completed_timelines += sum(timelines.values())

    print(f"Solution part 2: The total number of timelines is: {completed_timelines}")


if __name__ == "__main__":
    with open('7/input.txt') as f:
        manifold_data = [line.rstrip('\n') for line in f.readlines()]
    
    # solution_part_1(manifold_data)
    solution_part_2(manifold_data)