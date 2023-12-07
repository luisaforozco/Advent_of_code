number_words = Dict(
        "zero" => '0',
        "one" => '1',
        "two" => '2',
        "three" => '3',
        "four" => '4',
        "five" => '5',
        "six" => '6',
        "seven" => '7',
        "eight" => '8',
        "nine" => '9'
    )

function digits_in_string(str::AbstractString, count_num_in_words::Bool=false)
    digits = []
    for (index, c) in enumerate(str)
        if isdigit(c)
            push!(digits, c)
            continue
        elseif count_num_in_words
            for num_wd ∈ keys(number_words)
                if startswith(str[index:end], num_wd)
                    push!(digits, number_words[num_wd])
                    break
                end
            end
        end
    end
    return digits
end

function get_calibration_value(list_lines, count_num_in_words::Bool=false)
    calibration_value = 0
    for line ∈ list_lines
        digits_line = digits_in_string(line, count_num_in_words)
        calibration_value += parse(Int, digits_line[1] * digits_line[end])
    end
    return calibration_value
end

# Part 1
function sol_part_1(filename, name_puzzle)
    lines = readlines(filename)
    calibration_value = get_calibration_value(lines)
    println("$name_puzzle : $calibration_value")
end

sol_part_1("./input_example.txt", "Part 1, test")
sol_part_1("./input_puzzle.txt", "Part 1, Puzzle answer")

# Part 2
function sol_part_2(filename, name_puzzle)
    lines = readlines(filename)
    calibration_value = get_calibration_value(lines, true)
    println("$name_puzzle : $calibration_value")
end

sol_part_2("./input_example_2.txt", "Part 2, test")
sol_part_2("./input_puzzle.txt", "Part 2, Puzzle answer")
