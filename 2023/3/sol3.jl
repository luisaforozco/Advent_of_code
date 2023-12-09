# all characters minus '.'
punctuation_characters = Set(['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'])

function has_adjacent_symbol(matrix, position)
    for i in -1:1
        for j in -1:1
            if position[1] + i < 1 || position[1] + i > length(matrix[:, position[2]])
                continue
            end
            if i == 0 && j == 0
                continue
            elseif position[2] + j < 1 || position[2] + j > length(matrix[position[1], :])
                continue
            elseif matrix[position[1] + i, position[2] + j] in punctuation_characters
                return true
            end
        end
    end
    return false
end

function get_parent_number(matrix::Matrix{Char}, position::Tuple{Int64, Int64})
    min_x_pos = position[1]
    for i in -1:-1:-4
        min_bound = max(position[1] + i, 1)
        if isnumeric(matrix[min_bound, position[2]])
            min_x_pos = min_bound
        else
            break # case of finding a '.' or punctuation_characters
        end
    end
    max_x_pos = position[1]
    for i in 1:1:4
        max_bound = min(position[1] + i, length(matrix[:,position[2]]))
        if isnumeric(matrix[max_bound, position[2]])
            max_x_pos = max_bound
        else
            break # case of finding a '.' or punctuation_characters
        end
    end
    result_string = ""
    for i in min_x_pos:max_x_pos
        result_string *= matrix[i, position[2]]
    end
    return parse(Int, result_string)
end

function sol_1(input_file)
    lines = readlines(input_file)
    matrix = hcat([collect(line) for line in lines]...) # matrix, access element: matrix[row, col]
    num_rows, num_cols = size(matrix)
    sum_part_numbers =  0
    prev_added_number = 0
    for j in 1:num_cols
        for i in 1:num_rows
            if isnumeric(matrix[i, j]) && has_adjacent_symbol(matrix, (i, j))
                current_number = get_parent_number(matrix, (i, j))
                if prev_added_number != current_number
                    sum_part_numbers += current_number
                    prev_added_number = current_number
                end
            else # case of . or character
                prev_added_number = 0
            end
        end
    end
    return sum_part_numbers
end

sol_example_1 = sol_1("input_example.txt")
sol_puzzle_part_1 = sol_1("input_puzzle.txt")
println(" Part 1, example: $sol_example_1 \n Part 1, puzzle: $sol_puzzle_part_1")

function adjacent_parts(matrix, position)
    num_parts_adjacent = 0
    parts_adjacent = [0, 0]
    for i in -1:1
        for j in -1:1
            if position[1] + i < 1 || position[1] + i > length(matrix[:, position[2]])
                continue
            elseif i == 0 && j == 0
                continue
            elseif position[2] + j < 1 || position[2] + j > length(matrix[position[1], :])
                continue
            elseif isnumeric(matrix[position[1] + i, position[2] + j]) 
                num_parts_adjacent += 1
                number_adjacent = get_parent_number(matrix, (position[1] + i, position[2] + j))
                if parts_adjacent[1] == 0 
                    parts_adjacent[1] = number_adjacent
                elseif parts_adjacent[2] == 0 && number_adjacent != parts_adjacent[1]
                    parts_adjacent[2] = number_adjacent
                end
            end
        end
    end
    return parts_adjacent
end

function sol_2(input_file)
    lines = readlines(input_file)
    matrix = hcat([collect(line) for line in lines]...) # matrix, access element: matrix[row, col]
    num_rows, num_cols = size(matrix)
    sum_gear_ratios =  0
    # Loop over each element in the matrix
    for j in 1:num_cols
        for i in 1:num_rows
            if matrix[i, j] == '*'
                parts_adjacent = adjacent_parts(matrix, (i, j))
                sum_gear_ratios += parts_adjacent[1] * parts_adjacent[2]
            end
        end
    end
    return sum_gear_ratios
end

sol_example_2 = sol_2("input_example.txt")
sol_puzzle_part_2 = sol_2("input_puzzle.txt")
println(" Part 2, example: $sol_example_2 \n Part 2, puzzle: $sol_puzzle_part_2")