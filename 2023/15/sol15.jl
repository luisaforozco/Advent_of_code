function hash_algoritm(input_sequence)
    current_value = 0
    for i in input_sequence
        current_value = ((current_value + Int(i)) * 17) % 256
    end
    return current_value
end

function test_hash_algoritm()
    @assert hash_algoritm("HASH") == 52
end

function sol_part_1(input_file)
    sequence = split(readlines(input_file)[begin], ",")
    sum_results = sum(hash_algoritm.(sequence))
    return sum_results
end

sol_example_1 = sol_part_1("./input_example.txt")
sol_puzzle_part_1 = sol_part_1("./input_puzzle.txt")
println(" Part 1, example: $sol_example_1 \n Part 1, puzzle: $sol_puzzle_part_1")

# Part 2

function get_info_step(step)
    if '=' in step
        x = split(step, "=")
        return [x[begin], parse(Int, x[end])]
    elseif '-' in step
        return [step[begin:end-1]]
    else
        println("WARNING: step $step not recognized")
        return 0
    end
end

function calculate_focusing_power(boxes)
    focusing_power = 0
    for (box_id, steps) in boxes
        for (i, step) in enumerate(steps)
            focusing_power += (box_id + 1) * i * step[2]
        end 
    end
    return focusing_power
end

function sol_part_2(input_file)
    sequence = split(readlines(input_file)[begin], ",")
    boxes = Dict()
    for i in sequence
        step = get_info_step(i)
        box_i = hash_algoritm(step[1])
        box_exists = haskey(boxes, box_i)
        if length(step) == 2 # = operation
            if box_exists
                replace = false
                for (l, lens) in enumerate(boxes[box_i])
                    if lens[begin] == step[begin]
                        boxes[box_i][l] = step
                        replace = true
                        break
                    end
                end
                if !replace
                    push!(boxes[box_i], step)
                end
            else
                boxes[box_i] = [step]
            end
        else # - operation
            if box_exists
                # remove the element from the box
                filter!(e->e[begin] ≠ step[begin], boxes[box_i])
            end
        end
    end
    return calculate_focusing_power(boxes)
end

sol_example_2 = sol_part_2("./input_example.txt")
sol_puzzle_part_2 = sol_part_2("./input_puzzle.txt")
println(" Part 2, example: $sol_example_2 \n Part 2, puzzle: $sol_puzzle_part_2")