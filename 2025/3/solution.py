import heapq

def solution_part_1(data):
    joltage = 0 
    for line in data.splitlines():
        # get two largest number in the line
        nums = [int(ch) for ch in line]
        max1, index1 = max(((v, i) for i, v in enumerate(nums[:-1])), key=lambda x: x[0])
        max2 = max(nums[index1+1:])
        joltage += int(str(max1) + str(max2))
    
    return joltage  


def largest_joltage(num_str, k=12):
    """
    Pick exactly k digits from num_str to form the largest number,
    preserving original order.
    """
    drop = len(num_str) - k
    stack = []
    for digit in num_str:
        while drop and stack and stack[-1] < digit:
            stack.pop()
            drop -= 1
        stack.append(digit)

    return ''.join(stack[:k])


def solution_part_2(data):
    k = 12 # retrieve top k largest numbers
    return sum(int(largest_joltage(line, k)) for line in data.splitlines())

if __name__ == "__main__":
    with open("3/input.txt", "r") as f:
        data = f.read()

    #print(f"Part 1: Total output joltage is {solution_part_1(data)}")
    print(f"Part 2: Result is {solution_part_2(data)}")