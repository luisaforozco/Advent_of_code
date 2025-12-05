import numpy as np

def solution_part_1(data):
    ranges, _, ingredients = data.partition("\n\n")
    num_fresh_ingredients = 0
    for ing in ingredients.splitlines():
        for r in ranges.splitlines():
            r_i = r.strip().split("-")
            if int(r_i[0]) <= int(ing) <= int(r_i[1]): 
                num_fresh_ingredients +=1
                break
    
    return num_fresh_ingredients


def solution_part_2_first_shot(data):
    # Naive, the list doesn't fit in memory
    ranges, _, _ = data.partition("\n\n")
    list_fresh_ingredients = set([])
    for r in ranges.splitlines():
        r_i = r.strip().split("-")
        arr = np.arange(int(r_i[0]), int(r_i[1])+1)
        new_items = set(arr) - list_fresh_ingredients
        list_fresh_ingredients.update(new_items)

    return len(list_fresh_ingredients)

def solution_part_2(data):
    ranges_text, _, _ = data.partition("\n\n")
    intervals = []
    for line in ranges_text.splitlines():
        line = line.strip()
        if not line: continue
        a_str, b_str = line.split("-")
        a, b = int(a_str), int(b_str)
        if a > b:
            a, b = b, a
        intervals.append((a, b))

    if not intervals:
        return 0

    # Sort by start, then merge overlapping OR adjacent intervals
    intervals.sort()
    merged = []
    sa, sb = intervals[0]
    for a, b in intervals[1:]:
        if a <= sb + 1:         
            if b > sb:
                sb = b
        else:
            merged.append((sa, sb))
            sa, sb = a, b
    merged.append((sa, sb))

    # Sum sizes of merged intervals (inclusive ends)
    return sum(b - a + 1 for a, b in merged)


if __name__ == "__main__":
    with open("5/input_example.txt", "r") as f:
        data = f.read()

    print(f"Part 1:  {solution_part_1(data)}")
    print(f"Part 2: Result is {solution_part_2(data)}")