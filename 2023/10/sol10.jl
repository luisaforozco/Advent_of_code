# constants
UP = CartesianIndex(0, -1)
DOWN = CartesianIndex(0, 1)
RIGHT = CartesianIndex(1, 0)
LEFT = CartesianIndex(-1, 0)

function is_possible_move(current, next, direction)
    if next == '.'
        return false
    elseif direction == UP
        if current == '-' || current == 'F' || current == '7' ||next == 'L' || next == 'J' || next == 'L'
            return false
        else
            return true
        end
    elseif direction == DOWN
        if current == '-' || current == 'L' || current == 'J' || next == '-' || next == 'F' || next == '7'
            return false
        else
            return true
        end
    elseif direction == RIGHT
        if current == '|' || current == '7' || current == 'J' || next == '|' || next == 'F' || next == 'L'
            return false
        else
            return true
        end
    elseif direction == LEFT
        if current == '|' || current == 'L' || current == 'F' || next == '|' || next == '7' || next == 'J'
            return false
        else
            return true
        end
    end
    println("Error: couldn't determine if move is possible")
    return false
end

function check_out_of_bounds(index, matrix)
    return !all(1 <= index[i] <= size(matrix, i) for i in 1:length(index))
end 

function get_loop(matrix)
    current_index = findfirst(isequal('S'), matrix)
    moves = [UP, DOWN, RIGHT, LEFT]
    loop = []
    prev_move = current_index
    while(true)
        current = matrix[current_index]
        if matrix[current_index] == 'S' && !isempty(loop)
            return loop
        else
            for move in moves
                if check_out_of_bounds(current_index + move, matrix)
                    continue # out of bouds
                elseif is_possible_move(current, matrix[current_index + move], move)
                    if current_index + move != prev_move
                        current_index += move
                        push!(loop, current_index)
                        break
                    end
                end
            end
            #debug
            #println("current: $current, next current index: $current_index, prev move: $prev_move")
            if (length(loop) > 1) 
                prev_move = loop[end-1]
            end
        end
    end
    return loop
end

function calculate_distance(matrix)
    loop = get_loop(matrix)
    return length(loop) / 2
end

function sol_part_1(input_file)
    lines = readlines(input_file)
    matrix = hcat([collect(line) for line in lines]...)
    return calculate_distance(matrix)
end

sol_example_1 = sol_part_1("./input_example1a.txt")
sol_example_1b = sol_part_1("./input_example1b.txt")
println(" Part 1, example a: $sol_example_1 \n Part 1, example b: $sol_example_1b")
sol_puzzle_part_1 = sol_part_1("./input_puzzle.txt")
println(" Part 1, example: $sol_example_1 \n Part 1, puzzle: $sol_puzzle_part_1")

# Part 2 not working

mutable struct Segment
    start::CartesianIndex
    finish::CartesianIndex
    x_coef::Float64
    y_coef::Float64
end

function precompute_segments(path)
    segments = [Segment(path[i], path[i+1], 0.0, 0.0) for i in 1:length(path)-1]
    for segment in segments
        segment.x_coef = (segment.finish[1] - segment.start[1]) / (segment.finish[2] - segment.start[2])
        segment.y_coef = segment.start[2]
    end
    return segments
end

function is_inside(point, segments)
    count = 0
    for segment in segments
        if (segment.start[2] ≤ point[2] < segment.finish[2]) || (segment.finish[2] ≤ point[2] < segment.start[2])
            x_intersect = segment.start[1] + (point[2] - segment.y_coef) * segment.x_coef
            if x_intersect > point[1]
                count += 1
            end
        end
    end
    return count % 2 != 0
end

function find_inside_points(matrix, path)
    segments = precompute_segments(path)
    inside_points = Vector{CartesianIndex}()
    for i in 1:size(matrix, 1)
        for j in 1:size(matrix, 2)
            if is_inside(CartesianIndex(i, j), segments)
                push!(inside_points, CartesianIndex(i, j))
            end
        end
    end
    return inside_points
end

function sol_part_2(input_file)
    lines = readlines(input_file)
    matrix = hcat([collect(line) for line in lines]...)
    loop = get_loop(matrix)
    return length(find_inside_points(matrix, loop))
end

sol_example_2a = sol_part_2("./input_example2a.txt")
sol_example_2b = sol_part_2("./input_example2b.txt")
sol_example_2c = sol_part_2("./input_example2c.txt")
println("Part 2, \n example a: $sol_example_2a \n example b: $sol_example_2b \n example c: $sol_example_2c")