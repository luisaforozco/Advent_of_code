function is_rock(y)
    return y == '#' || y == 'O'
end

function tilt_north(platform)
    for index in CartesianIndices(platform)
        i, j = Tuple(index)
        if i == 1 
            # the 'O' rock is already at the northest position
            continue
        # can also skip the columns that have no 'O'
        elseif platform[i, j] == 'O'
            column = platform[begin:i-1, j]
            min_index = findlast(is_rock, column)
            if min_index === nothing # all elements above were '.'
                min_index = 0
            end
            platform[i, j] = '.' # remove the 'O' from the current position
            platform[min_index+1, j] = 'O' # place the 'O' in the new position
        end 
    end
    return platform
end

function calculate_load(platform)
    load = 0
    indices_O = findall(x -> x == 'O', platform)
    lenght = size(platform)[1]
    for index in indices_O
        i, _ = Tuple(index)
        load += lenght + 1 - i
    end
    return load
end

function sol_part_1(input_file)
    platform = readlines(input_file)
    platform = [s[i] for s in platform, i in 1:length(platform[1])]
    platform = tilt_north(platform)
    return calculate_load(platform)
end

sol_example_1 = sol_part_1("./input_example.txt")
sol_puzzle_part_1 = sol_part_1("./input_puzzle.txt")
println(" Part 1, example: $sol_example_1 \n Part 1, puzzle: $sol_puzzle_part_1")

# Part 2
# Brute force (i.e running all cycles) 
# despite usign memoize is not feasible, and didn't get the right solution for the example.
# Found on the internet a solution that keeps the same implementation of part 1 and rotates the matrix.
using Memoize

@memoize function move(platform, direction, i, j)
    platform[i, j] = '.' # remove the 'O' from the current position
    if direction == "N"
        column = platform[begin:i-1, j]
        min_index = findlast(is_rock, column)
        if min_index === nothing # all elements above were '.'
            min_index = 0
        end
        platform[min_index+1, j] = 'O' # place the 'O' in the new position
    elseif direction == "S"
        column = platform[i+1:end, j]
        min_index = findfirst(is_rock, column)
        if min_index === nothing # all elements above were '.'
            num_rows = size(platform, 1)
            min_index = (num_rows - i) + 1
        end
        platform[min_index+i-1, j] = 'O'
    elseif direction == "W"
        column = platform[i, begin:j-1]
        min_index = findlast(is_rock, column)
        if min_index === nothing # all elements above were '.'
            min_index = 0
        end
        platform[i, min_index+ 1] = 'O'
    else
        column = platform[i, j+1:end]
        min_index = findfirst(is_rock, column)
        if min_index === nothing # all elements above were '.'
            num_cols = size(platform, 2)
            min_index = (num_cols - j) + 1
        end
        platform[i, min_index+j-1] = 'O'
    end
    return platform
end

@memoize function tilt(platform, dir)
    num_cols = size(platform, 2)
    num_rows = size(platform, 1)

    # Define iterators, depending on the direction
    it_rows = 1:num_rows
    it_cols = 1:num_cols
    if dir == "S"
        it_rows = reverse(it_rows)
    elseif dir == "E"
        it_cols = reverse(it_cols)
    end

    # Loop for tilting the platform
    for i in it_rows, j in it_cols
        if (dir == "N" && i == 1) || (dir == "S" && i == num_rows) || (dir == "E" && j == num_cols) || (dir == "W" && j == 1)
        # the 'O' rock is already at the furthest position
            continue
        # can also skip the columns that have no 'O'
        elseif platform[i, j] == 'O'
            platform = move(platform, dir, i, j)
        end 
    end
    return platform
end

function sol_part_2(input_file)
    platform = readlines(input_file)
    platform = [s[i] for s in platform, i in 1:length(platform[1])]
    cycles = 1000000000
    for i in 1:cycles
        platform = tilt(platform, "N")
        platform = tilt(platform, "W")
        platform = tilt(platform, "S")
        platform = tilt(platform, "E")
        if i % 10000000 == 0
            println("Cycle $i")
        end
    end
    return calculate_load(platform)
end

sol_example_2 = sol_part_2("./input_example.txt")
println(" Part 2, example: $sol_example_2")
# sol_puzzle_part_2 = sol_part_2("./input_puzzle.txt")
# println(" Part 2, example: $sol_example_2 \n Part 2, puzzle: $sol_puzzle_part_2")