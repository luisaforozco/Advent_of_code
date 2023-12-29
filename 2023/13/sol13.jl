function read_patterns(input_file)
    lines = readlines(input_file)
    patterns, pattern_i = [], []
    for line in lines
        if isempty(line) # next pattern
            if !isempty(pattern_i)
                push!(patterns, pattern_i)
                pattern_i = []
            end
        else
            push!(pattern_i, line)
        end
    end
    return push!(patterns, pattern_i)
end

function check_reflection_rows(pattern)
    num_rows = length(pattern)
    for i in 2:num_rows
        if pattern[i] == pattern[i - 1]
            j = 1
            reflection = true
            while j+i <= num_rows && i-j > 1
                if pattern[i+j] != pattern[i-j-1]
                    reflection = false
                    break
                end
                j += 1
            end
            if reflection
                return i-1
            end
        end
    end
    return 0
end

function check_reflection_cols(pattern)
    num_cols = length(pattern[1])
    matrix = [s[i] for s in pattern, i in 1:length(pattern[1])]
    for i in 2:num_cols
        if matrix[:, i] == matrix[:, i - 1]
            j = 1
            reflection = true
            while j+i <= num_cols && i-j > 1
                reflection = matrix[:,i+j] == matrix[:,i-j-1]
                if !reflection
                    break
                end
                j += 1
            end
            if reflection
                return i-1
            end
        end
    end
    return 0
end

function sol_part_1(input_file)
    patterns = read_patterns(input_file)
    row_sum, col_sum = 0, 0
    for pattern in patterns
        row_sum += check_reflection_rows(pattern)
        col_sum += check_reflection_cols(pattern)
    end
    return col_sum + (100 * row_sum)
end

sol_example_1 = sol_part_1("./input_example.txt")
sol_puzzle_part_1 = sol_part_1("./input_puzzle.txt")
println(" Part 1, example: $sol_example_1 \n Part 1, puzzle: $sol_puzzle_part_1")