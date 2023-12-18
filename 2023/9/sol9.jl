using DelimitedFiles

function predict_next_value(history)
    current_history = diff(history)
    all_zero = all(x -> x == 0, current_history)
    last_elements = [history[end], current_history[end]]
    while(!all_zero)
        current_history = diff(current_history)
        all_zero = all(x -> x == 0, current_history)
        push!(last_elements, current_history[end])
    end

    prediction = 0
    for i in length(last_elements):-1:2
        prediction = prediction + last_elements[i-1]
    end
    return prediction
end

function sol_part_1(input_file)
    report = readdlm(input_file, Int32)
    sum_predicitons = 0
    for history in eachrow(report) # default in julia is on columns
        sum_predicitons += predict_next_value(history)
    end
    return sum_predicitons
end

sol_example_1 = sol_part_1("./input_example.txt")
sol_puzzle_part_1 = sol_part_1("./input_puzzle.txt")
println(" Part 1, example: $sol_example_1 \n Part 1, puzzle: $sol_puzzle_part_1")

# Part 2
function predict_prev_value(history)
    current_history = diff(history)
    all_zero = all(x -> x == 0, current_history)
    first_elements = [history[begin], current_history[begin]]
    while(!all_zero)
        current_history = diff(current_history)
        all_zero = all(x -> x == 0, current_history)
        push!(first_elements, current_history[begin])
    end

    prediction = 0
    for i in length(first_elements):-1:2
        prediction = first_elements[i-1] - prediction
    end
    return prediction
end

function sol_part_2(input_file)
    report = readdlm(input_file, Int32)
    sum_predicitons = 0
    for history in eachrow(report) # default in julia is on columns
        sum_predicitons += predict_prev_value(history)
    end
    return sum_predicitons
end

sol_example_2 = sol_part_2("./input_example.txt")
sol_puzzle_part_2 = sol_part_2("./input_puzzle.txt")
println(" Part 2, example: $sol_example_2 \n Part 2, puzzle: $sol_puzzle_part_2")