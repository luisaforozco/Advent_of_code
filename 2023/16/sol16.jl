# Definition of constants: directions to move in the matrix.
U = [-1, 0]
D = [ 1, 0]
L = [ 0,-1]
R = [ 0, 1]

"""
Recursive function that moves the beam in the contraption, updating the energy matrix.
Checks if the position and direction have been visited before, if so returns the energy matrix (breaks the recursion).
"""
function move_beam(contraption, energy, pos, dir; checks=[])
    # check if the position and direction have been visited before
    if isempty(checks)
        push!(checks, [pos, dir])
    elseif [pos, dir] in checks
        return energy
    else
        push!(checks, [pos, dir])
    end

    U_pos = pos + U
    D_pos = pos + D
    L_pos = pos + L
    R_pos = pos + R
    x, y = pos
    energy[x, y] += 1

    if contraption[x, y] == '|'
        if checkbounds(Bool, contraption, U_pos[1], U_pos[2])
            move_beam(contraption, energy, U_pos, U, checks=checks) 
        end
        if checkbounds(Bool, contraption, D_pos[1], D_pos[2])
            move_beam(contraption, energy, D_pos, D, checks=checks) 
        end
    elseif contraption[x, y] == '-'
        if checkbounds(Bool, contraption, L_pos[1], L_pos[2]) 
            move_beam(contraption, energy, L_pos, L, checks=checks) 
        end
        if checkbounds(Bool, contraption, R_pos[1], R_pos[2]) 
            move_beam(contraption, energy, R_pos, R, checks=checks) 
        end
    elseif contraption[x, y] == '/'
        if dir==L && checkbounds(Bool, contraption, D_pos[1], D_pos[2]) > 0 # L->D
            move_beam(contraption, energy, D_pos, D, checks=checks)
        elseif dir==R && checkbounds(Bool, contraption, U_pos[1], U_pos[2]) # R->U
            move_beam(contraption, energy, U_pos, U, checks=checks)
        elseif dir==U && checkbounds(Bool, contraption, R_pos[1], R_pos[2]) # U->R
            move_beam(contraption, energy, R_pos, R, checks=checks)
        elseif dir==D && checkbounds(Bool, contraption, L_pos[1], L_pos[2]) # D->L
            move_beam(contraption, energy, L_pos, L, checks=checks)
        end
    elseif contraption[x, y] == '\\'
        if dir==L && checkbounds(Bool, contraption, U_pos[1], U_pos[2]) # L->U
            move_beam(contraption, energy, U_pos, U, checks=checks)
        elseif dir==R && checkbounds(Bool, contraption, D_pos[1], D_pos[2]) # R->D
            move_beam(contraption, energy, D_pos, D, checks=checks)
        elseif dir==D && checkbounds(Bool, contraption, R_pos[1], R_pos[2]) # D->R
            move_beam(contraption, energy, R_pos, R, checks=checks)
        elseif dir==U && checkbounds(Bool, contraption, L_pos[1], L_pos[2]) # U->L
            move_beam(contraption, energy, L_pos, L, checks=checks)
        end
    else # case of '.'
        pos += dir
        if checkbounds(Bool, contraption, pos[1], pos[2])
            move_beam(contraption, energy, pos, dir, checks=checks)
        end
    end
    return energy
end

function sol_part_1(input_file)
    input = readlines(input_file)
    contraption = [s[i] for s in input, i in 1:length(input[1])]
    energy = zeros(Int, size(contraption, 1), size(contraption, 2))
    energy = move_beam(contraption, energy, [1, 1], R)
    return count(x -> x != 0, energy)
end

sol_example_1 = sol_part_1("./input_example.txt")
sol_puzzle_part_1 = sol_part_1("./input_puzzle.txt")
println(" Part 1, example: $sol_example_1 \n Part 1, puzzle: $sol_puzzle_part_1")

# Part 2

function test_algorithm(input_file)
    input = readlines(input_file)
    contraption = [s[i] for s in input, i in 1:length(input[1])]

    energy = zeros(Int, size(contraption, 1), size(contraption, 2))
    energy_1 = move_beam(contraption, energy, [1, 1], R)
    tiles_energized_1 = count(x -> x != 0, energy_1)
    @assert tiles_energized_1 == 46

    energy = zeros(Int, size(contraption, 1), size(contraption, 2))
    energy_2 = move_beam(contraption, energy, [1, 4], D)
    tiles_energized_2 = count(x -> x != 0, energy_2)
    @assert tiles_energized_2 == 51
end

function check_different_IC(contraption)
    max_tiles_energized = 0
    num_rows, num_cols = size(contraption)
    # check beam entering from top and bottom
    for i in 1:num_cols
        energy = zeros(Int, num_rows, num_cols)
        energy = move_beam(contraption, energy, [1, i], D)
        tiles_energized = count(x -> x != 0, energy)
        if tiles_energized > max_tiles_energized
            max_tiles_energized = tiles_energized
        end
        energy = zeros(Int, num_rows, num_cols)
        energy = move_beam(contraption, energy, [num_rows, i], U)
        tiles_energized = count(x -> x != 0, energy)
        if tiles_energized > max_tiles_energized
            max_tiles_energized = tiles_energized
        end
    end

    # check beam entering from Left and Right
    for i in 1:num_rows
        energy = zeros(Int, num_rows, num_cols)
        energy = move_beam(contraption, energy, [i, 1], R)
        tiles_energized = count(x -> x != 0, energy)
        if tiles_energized > max_tiles_energized
            max_tiles_energized = tiles_energized
        end

        energy = zeros(Int, num_rows, num_cols)
        energy = move_beam(contraption, energy, [i, num_cols], L)
        tiles_energized = count(x -> x != 0, energy)
        if tiles_energized > max_tiles_energized
            max_tiles_energized = tiles_energized
        end
    end
    return max_tiles_energized
end

function sol_part_2(input_file)
    input = readlines(input_file)
    contraption = [s[i] for s in input, i in 1:length(input[1])]
    return check_different_IC(contraption)
end

# run tests
test_algorithm("./input_example.txt")

sol_example_2 = sol_part_2("./input_example.txt")
sol_puzzle_part_2 = sol_part_2("./input_puzzle.txt")
println(" Part 2, example: $sol_example_2 \n Part 2, puzzle: $sol_puzzle_part_2")