using PolygonOps

# Definition of constants: directions to move in the matrix.
U = [-1, 0]
D = [ 1, 0]
L = [ 0,-1]
R = [ 0, 1]

function read_input(input_file)
    input = readlines(input_file)
    current_index = [1, 1]
    contour = [current_index] # empty because the end point is the same as start
    for line in input
        direction, num_steps, color = split(line, " ")
        num_steps = parse(Int, num_steps)
        for _ in 1:num_steps
            if direction == "U"
                current_index += U
            elseif direction == "D"
                current_index += D
            elseif direction == "L"
                current_index += L
            elseif direction == "R"
                current_index += R
            end
            push!(contour, current_index)
        end
    end
    min_x = minimum(map(x -> x[1], contour))
    min_y = minimum(map(y -> y[2], contour))
    # re-normalize the indices 
    contour = [p .- [min_x, min_y] .+ 1 for p in contour]
    return contour
end

function print_contour(contour)
    max_x = maximum([p[1] for p in contour])
    max_y = maximum([p[2] for p in contour])
    top_view = zeros(Int, max_x, max_y)
    for x in 1:max_x
        for y in 1:max_y
            if [x, y] in contour
                top_view[x, y] = 1
                #print("#")
            else
                #print(".")
            end
        end
        #println()
    end
    return top_view
end

function dig_interior!(top_view, contour)
    # define contour polygon
    polygon = [Tuple(p) for p in contour]
    #loop trough top_view
    for index in CartesianIndices(top_view)
        if top_view[index] == 0
            # check if is inside contour
            x, y = Tuple(index)
            if inpolygon((x, y), polygon) == 1
                top_view[index] = 1
            end
        end
    end
    return top_view
end

function test(input_file)
    contour = read_input(input_file)
    @assert length(contour)-1 == 38
    polygon = [Tuple(p) for p in contour]
    @assert inpolygon((4, 4), polygon) == 1
    @assert inpolygon((1, 4), polygon) == -1
end

function sol_part_1(input_file)
    contour = read_input(input_file)
    top_view = print_contour(contour)
    top_view = dig_interior!(top_view, contour)
    return count(x -> x != 0, top_view)
end

test("./input_example.txt")
sol_example_1 = sol_part_1("./input_example.txt")
sol_puzzle_part_1 = sol_part_1("./input_puzzle.txt")
println(" Part 1, example: $sol_example_1 \n Part 1, puzzle: $sol_puzzle_part_1")

# Part 2
# too slow to check

function read_input_2(input_file)
    input = readlines(input_file)
    current_index = [1, 1]
    contour = [current_index] # empty because the end point is the same as start
    for line in input
        _, _, color = split(strip(line), " ")
        direction = color[end-1]
        num_steps = color[begin+2 : end-2] # get rid of the brackets
        num_steps = parse(Int, num_steps, base=16)
        for _ in 1:num_steps
            #0 means R, 1 means D, 2 means L, and 3 means U
            if direction == '3'
                current_index += U
            elseif direction == '1'
                current_index += D
            elseif direction == '2'
                current_index += L
            elseif direction == '0'
                current_index += R
            end
            push!(contour, current_index)
        end
    end
    min_x = minimum(map(x -> x[1], contour))
    min_y = minimum(map(y -> y[2], contour))
    # re-normalize the indices 
    contour = [p .- [min_x, min_y] .+ 1 for p in contour]
    return contour
end

function sol_part_2(input_file)
    contour = read_input_2(input_file)
    top_view = print_contour(contour)
    top_view = dig_interior!(top_view, contour)
    return count(x -> x != 0, top_view)
end

sol_example_2 = sol_part_2("./input_example.txt")
println(" Part 2, example: $sol_example_2")
#sol_puzzle_part_2 = sol_part_2("./input_puzzle.txt")
#println(" Part 2, example: $sol_example_2 \n Part 2, puzzle: $sol_puzzle_part_2")