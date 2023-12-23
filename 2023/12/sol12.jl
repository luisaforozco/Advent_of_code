function get_groups(row)
    groups = []
    count = 0
    for i in row
        if i == '#'
            count += 1
        else
            if (count > 0) push!(groups, count) end
            count = 0
        end
    end
    if (count > 0) push!(groups, count) end
    return groups
end

function get_combinations(X)
    function my_bitstring(n, length)
        binary = string(n, base = 2)
        return lpad(binary, length, '0')
    end
    # from 1 to avoid element with all 0s. -2 instead of -1 to avoid elements with all 1s
    binary_combinations = [my_bitstring(i, X) for i in 1:(2^X - 2)]
    return [replace(i, '1' => '#', '0' => '.') for i in binary_combinations ]
end

function get_num_arrangements(record)
    row , groups = split(record, " ")
    groups = parse.(Int64, split(groups, ","))
    # a shortcut for a specific case: all the ? are . or # Only one solution
    all_damaged = replace(row, '?' => '#')
    if get_groups(row) == groups || get_groups(all_damaged) == groups 
        return 1
    end

    # testing all possible combinations (brute force)
    idx_unknown = [i for i in eachindex(row) if row[i] == '?']
    combinations = get_combinations(length(idx_unknown))
    arrangements = 0
    for i in eachindex(combinations)
        new_row = collect(row)
        for j in eachindex(combinations[i])
            new_row[idx_unknown[j]] = combinations[i][j]
        end
        if get_groups(new_row) == groups
            arrangements += 1
        end
    end
    return arrangements
end

function sol_part_1(input_file)
    records = readlines(input_file)
    sum_arrangements = 0 
    for record in records
        sum_arrangements += get_num_arrangements(record)
    end
    return sum_arrangements
end

sol_example_1 = sol_part_1("./input_example.txt")
sol_puzzle_part_1 = sol_part_1("./input_puzzle.txt")
println(" Part 1, example: $sol_example_1 \n Part 1, puzzle: $sol_puzzle_part_1")

# Part 2

function unfold(records)
    unfolded_records = []
    for record in records
        row , groups = split(record, " ")
        groups = repeat(groups * ",", 5)[begin:end-1]
        row = repeat(row * "?", 5)[begin:end-1]
        push!(unfolded_records, row * " " * groups)
    end
    return unfolded_records
end

cache = Dict()
function count_arrangements(row, groups)
    result = 0
    if isempty(groups)
        return '#' in row ? 0 : 1
    end
    key = (row, groups)
    if key in keys(cache)
       return cache[key]
    end
    length(row) < sum(groups) + length(groups) - 1 && return 0
    if !('.' in row[begin:groups[begin]])
        if length(row) == groups[begin] || row[groups[begin]+1] != '#'
            result += count_combinations(row[groups[begin] + 2:end], groups[begin+1:end])
        end
    end
    if row[begin] != '#'
        result += count_combinations(row[begin + 1:end], groups)
    end
    cache[key] = result
    return result
end

function sol_part_2(input_file)
    records = unfold(readlines(input_file))
    sum_arrangements = 0 
    for record in records
        row, groups = split(record, " ")
        groups = parse.(Int64, split(groups, ","))
        arr_record = count_arrangements(row, groups)
        println(arr_record)
        sum_arrangements += arr_record
    end
    return sum_arrangements
end

sol_example_2 = sol_part_2("./input_example.txt")
sol_puzzle_part_2 = sol_part_2("./input_puzzle.txt")
println(" Part 2, example: $sol_example_2 \n Part 2, puzzle: $sol_puzzle_part_2")