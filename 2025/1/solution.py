def solve_part1():
    current_position = 50
    zero_count = 0

    #with open('1/input_example.txt', 'r') as f:
    with open('1/input.txt', 'r') as f:    
        rotations = f.readlines()

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:].strip())

        if direction == 'R':
            current_position = (current_position + distance) % 100
        elif direction == 'L':
            current_position = (current_position - distance) % 100
            # Python's % operator can return negative results for negative numbers
            # This ensures it's always positive within 0-99
            if current_position < 0:
                current_position += 100
        
        if current_position == 0:
            zero_count += 1
            
    print(f"Part 1: {zero_count}")

def solve_part2():
    current_pos = 50
    zero_crossings = 0

    with open('1/input_example.txt', 'r') as f:
        rotations = f.readlines()

    for rotation in rotations:
        direction = rotation[0]
        amount = int(rotation[1:].strip())

        if direction == 'R':
            # Right rotation (addition)
            zero_crossings += (current_pos + amount) // 100 - current_pos // 100
            current_pos = (current_pos + amount) % 100
        elif direction == 'L':
            # Left rotation (subtraction)
            zero_crossings += (current_pos - 1) // 100 - (current_pos - amount - 1) // 100
            current_pos = (current_pos - amount) % 100
    
    print(f"Part 2 Example: {zero_crossings}")

    current_pos = 50
    zero_crossings = 0

    with open('1/input.txt', 'r') as f:
        rotations = f.readlines()

    for rotation in rotations:
        direction = rotation[0]
        amount = int(rotation[1:].strip())

        if direction == 'R':
            # Right rotation (addition)
            zero_crossings += (current_pos + amount) // 100 - current_pos // 100
            current_pos = (current_pos + amount) % 100
        elif direction == 'L':
            # Left rotation (subtraction)
            zero_crossings += (current_pos - 1) // 100 - (current_pos - amount - 1) // 100
            current_pos = (current_pos - amount) % 100

    print(f"Part 2: {zero_crossings}")


if __name__ == "__main__":
    solve_part1()
    solve_part2()
