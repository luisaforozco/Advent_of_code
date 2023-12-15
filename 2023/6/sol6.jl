"""
Reads the inputs of the puzzle
# Arguments
- input_file: path to the input file
- with_spaces: true for puzzle 1 in which you should consider the spaces determining different races.
false for puzzle 2 in which is a single race.
"""
function read_races_info(input_file, with_spaces = true)
    
    lines = readlines(input_file)
    times = []
    distances = []
    for line in lines
        if line == "\n" || line == ""
            continue
        elseif startswith(line, "Time:")
            if with_spaces
                info_times = [strip(x) for x in split(split(line, ":")[2], "  ")]
                times = [parse(Int, x) for x in filter(x -> x != "", info_times)]
            else
                info_times = strip(split(line, ":")[2])
                times = [parse(Int, replace(info_times, r"\s+" => ""))]
            end
        elseif startswith(line, "Distance:")
            if with_spaces
                info_distances = [strip(x) for x in split(split(line, ":")[2], "  ")]
                distances = [parse(Int, x) for x in filter(x -> x != "", info_distances)]
            else
                info_distances = strip(split(line, ":")[2])
                distances = [parse(Int, replace(info_distances, r"\s+" => ""))]
            end
        end
    end
    return times, distances
end

"""
Brute force solution to the puzzle
"""
function bf_number_of_ways_to_beat_record(times, distances)
    number_combinations_to_win = 1
    for race in axes(times)[1]
        time = times[race]
        distance_record = distances[race]
        number_ways_to_beat_record  = 0
        for tc in 1:time-1
            distance = tc * (time - tc)
            if distance > distance_record
                number_ways_to_beat_record += 1
            end
        end
        println("$race : $number_ways_to_beat_record")
        if number_ways_to_beat_record != 0
            number_combinations_to_win *= number_ways_to_beat_record
        end
    end
    return number_combinations_to_win
end

function sol_part_1(input_file)
    times, distances = read_races_info(input_file)
    return bf_number_of_ways_to_beat_record(times, distances)
end

sol_puzzle_part_1 = sol_part_1("./input_puzzle.txt")
println(" Part 1, example: $sol_example_1 \n Part 1, puzzle: $sol_puzzle_part_1")

function sol_part_2(input_file)
    times, distances = read_races_info(input_file, false)
    println(times)
    println(distances)
    return bf_number_of_ways_to_beat_record(times, distances)
end

sol_puzzle_part_2 = sol_part_2("./input_puzzle.txt")
println(" Part 2, example: $sol_example_2 \n Part 2, puzzle: $sol_puzzle_part_2")