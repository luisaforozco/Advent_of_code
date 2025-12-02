def is_invalid_id(n):
    s = str(n)
    if len(s) % 2 != 0:
        return False
    half = len(s) // 2
    return s[:half] == s[half:]

def solution_part_1(data):
    ranges = data.strip().split(',')
    total_invalid_id_sum = 0
    for r in ranges:
        start, end = map(int, r.split('-'))
        for i in range(start, end + 1):
            if is_invalid_id(i):
                total_invalid_id_sum += i
    return total_invalid_id_sum

def is_invalid_id_part_2(n):
    s = str(n)
    s_len = len(s)
    for i in range(1, s_len // 2 + 1):
        if s_len % i == 0:
            repeating_unit = s[:i]
            repetitions = s_len // i
            if repetitions > 1 and s == repeating_unit * repetitions:
                return True
    return False

def solution_part_2(data):
    ranges = data.strip().split(',')
    total_invalid_id_sum = 0
    for r in ranges:
        start, end = map(int, r.split('-'))
        for i in range(start, end + 1):
            if is_invalid_id_part_2(i):
                total_invalid_id_sum += i
    return total_invalid_id_sum

if __name__ == "__main__":
    with open("2/input.txt", "r") as f:
        data = f.read()
    
    result_part_1 = solution_part_1(data)
    print(f"Part 1: The sum of the invalid IDs is: {result_part_1}")
    
    result_part_2 = solution_part_2(data)
    print(f"Part 2: The sum of the invalid IDs is: {result_part_2}")
