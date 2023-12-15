function read_mapping_functions(input_file)
    lines = readlines(input_file)
    seeds = []
    mapping_functions = Dict()
    for i in 1:7
        mapping_functions[i] = []
    end
    current_map = 0
    for line in lines
        if line == "\n" || line == ""
            continue
        elseif startswith(line, "seeds:")
            seeds = filter(x -> x != "", split(split(line, ":")[2], " "))
            seeds = [parse(Int, x) for x in seeds]
        elseif startswith(line, "seed-to-soil")
            current_map = 1
        elseif startswith(line, "soil-to-fertilizer")
            current_map = 2
        elseif startswith(line, "fertilizer-to-water")
            current_map = 3
        elseif startswith(line, "water-to-light")
            current_map = 4
        elseif startswith(line, "light-to-temperature")
            current_map = 5
        elseif startswith(line, "temperature-to-humidity")
            current_map = 6
        elseif startswith(line, "humidity-to-location")
            current_map = 7
        else # numbers
            info_map = [parse(Int, x) for x in filter(x -> x != "", split(line, " "))]
            push!(mapping_functions[current_map], info_map)
        end
    end
    return seeds, mapping_functions
end

function get_seed_location(seed, mapping_functions)
    source = seed
    for i in 1:7
        dest = -1
        for map in mapping_functions[i]
            dest_cat, source_cat, range_lenght = map
            # check if source is in range
            if source_cat <= source && source_cat + range_lenght >= source
                dest = (source - source_cat) + dest_cat
                break
            end
        end
        source = (dest != -1) ? dest : source
        #println("map $i : $source")
    end
    return source
end 

function sol_part_1(input_file)
    seeds, mapping_functions = read_mapping_functions(input_file)
    locations = []
    for seed in seeds
        push!(locations, get_seed_location(seed, mapping_functions))
    end    
    return minimum(locations)
end

#sol_example_1 = sol_part_1("input_example.txt")
#sol_puzzle_part_1 = sol_part_1("./input_puzzle.txt")
#println(" Part 1, example: $sol_example_1 \n Part 1, puzzle: $sol_puzzle_part_1")

function correction_to_seeds(seeds)
    new_list_of_seeds = []
    start = 0
    for seed_pos in 1:length(seeds)
        if seed_pos % 2 == 0
            range_lenght = seeds[seed_pos]
            append!(new_list_of_seeds, collect(start:start + range_lenght - 1))
        else
            start = seeds[seed_pos]
        end
    end
    return new_list_of_seeds
end

function sol_part_2(input_file)
    seeds, mapping_functions = read_mapping_functions(input_file)
    seeds = correction_to_seeds(seeds)
    locations = []
    for seed in seeds
        push!(locations, get_seed_location(seed, mapping_functions))
    end    
    return minimum(locations)
end

sol_example_2 = sol_part_2("input_example.txt")
sol_puzzle_part_2 = sol_part_2("./input_puzzle.txt")
println(" Part 2, example: $sol_example_2 \n Part 2, puzzle: $sol_puzzle_part_2")
