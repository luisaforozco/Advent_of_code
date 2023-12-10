function convert_line_to_list_numbers(line)
    winning_numbers, numbers_we_have = split(split(line, ":")[2], "|")
    winning_numbers = filter(x -> x != "", split(winning_numbers, " "))
    numbers_we_have = filter(x -> x != "", split(numbers_we_have, " "))
    winning_numbers = [parse(Int, x) for x in winning_numbers]
    numbers_we_have = [parse(Int, x) for x in numbers_we_have]
    return winning_numbers, numbers_we_have
end

function sol_part_1(input_file)
    lines = readlines(input_file)
    total_points = 0
    for line in lines
        winning_numbers, numbers_we_have = convert_line_to_list_numbers(line)
        points_worth = 0
        for number in numbers_we_have
            if number in winning_numbers
                points_worth = (points_worth > 0) ? points_worth*2 : 1
            end
        end
        total_points += points_worth
    end
    return total_points
end

sol_example_1 = sol_part_1("input_example.txt")
sol_puzzle_part_1 = sol_part_1("./input_puzzle.txt")
println(" Part 1, example: $sol_example_1 \n Part 1, puzzle: $sol_puzzle_part_1")

function sol_part_2(input_file)
    lines = readlines(input_file)
    num_instances = ones(length(lines)) # number of lines is number of cards
    for (card_id, line) in enumerate(lines)
        winning_numbers, numbers_we_have = convert_line_to_list_numbers(line)
        num_matching_elements = length(intersect(winning_numbers, numbers_we_have))
        for i in 1:num_matching_elements
            num_instances[card_id+i] += num_instances[card_id]
        end
    end
    return sum(num_instances)
end

sol_example_2 = sol_part_2("input_example.txt")
sol_puzzle_part_2 = sol_part_2("./input_puzzle.txt")
println(" Part 2, example: $sol_example_2 \n Part 2, puzzle: $sol_puzzle_part_2")