import re

def parse_line(line: str):
    # target pattern
    pat = re.search(r"\[(.*?)\]", line).group(1)
    n = len(pat)
    target = sum((1 << i) for i, ch in enumerate(pat) if ch == '#')
    # buttons
    buttons = []
    for grp in re.findall(r"\((.*?)\)", line):
        grp = grp.strip()
        idxs = [int(x) for x in grp.split(',')] if grp else []
        mask = 0
        for i in idxs:
            if not (0 <= i < n):
                raise ValueError(f"Button index {i} out of range for {n} lights")
            mask |= (1 << i)
        buttons.append(mask)
    return target, buttons, n

def min_presses(target_mask, btn_masks):
    # Meet-in-the-middle over subsets of buttons
    m = len(btn_masks)
    m1 = m // 2
    left, right = btn_masks[:m1], btn_masks[m1:]

    # Left: map sum mask -> minimal presses
    left_best = {0: 0}
    for s in range(1, 1 << m1):
        # compute incrementally via lowest set bit
        t = s & -s
        k = (t.bit_length() - 1)
        prev = s ^ t
        # derive current mask from prev
        # To keep code simple and fast enough, just recompute from bits:
        cur_mask, cnt = 0, 0
        x = s
        while x:
            b = x & -x
            i = (b.bit_length() - 1)
            cur_mask ^= left[i]
            cnt += 1
            x ^= b
        if cur_mask not in left_best or cnt < left_best[cur_mask]:
            left_best[cur_mask] = cnt

    # Right: enumerate and combine
    best = float('inf')
    R = len(right)
    for s in range(1 << R):
        cur_mask, cnt = 0, 0
        x = s
        while x:
            b = x & -x
            i = (b.bit_length() - 1)
            cur_mask ^= right[i]
            cnt += 1
            x ^= b
        need = target_mask ^ cur_mask
        if need in left_best:
            best = min(best, cnt + left_best[need])
    return best

def solution_part_1(data):
    per_machine = []
    for line in data:
        target, buttons, _ = parse_line(line)
        per_machine.append(min_presses(target, buttons))

    print("Per-machine minimum presses:", per_machine)
    print("Total:", sum(per_machine))
    return per_machine

#-- Part 2

def solution_part_2(data):
    import re
    from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpInteger, PULP_CBC_CMD

    total = 0
    for line in data:
        line = line.strip()
        if not line:
            continue

        # Parse joltage targets
        targets = list(map(int, re.search(r"\{(.*?)\}", line).group(1).split(',')))
        n = len(targets)

        # Parse buttons
        buttons = []
        for grp in re.findall(r"\((.*?)\)", line):
            idxs = [int(x) for x in grp.split(',') if x.strip()]
            idxs = [i for i in idxs if 0 <= i < n]
            buttons.append(idxs)

        # Build ILP
        prob = LpProblem("JoltageConfig", LpMinimize)
        x = [LpVariable(f"x{i}", lowBound=0, cat=LpInteger) for i in range(len(buttons))]

        # Constraints: sum of contributions = target for each counter
        for j in range(n):
            prob += lpSum(x[i] for i, btn in enumerate(buttons) if j in btn) == targets[j]

        # Objective: minimize total presses
        prob += lpSum(x)

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))
        total += sum(v.value() for v in x)

    return int(total)
    

if __name__ == "__main__":
    with open('10/input.txt') as f:
        data = [line.rstrip('\n') for line in f.readlines()]

    #print(f"Solution part 1: {solution_part_1(data)}")
    print(f"Solution part 2: {solution_part_2(data)}")