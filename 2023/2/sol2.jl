function sol_part_1(filename::AbstractString)
    # definition of constants in the problem
    max_red_cubes = 12
    max_green_cubes = 13
    max_blue_cubes = 14

    sum_ids_possible_games = 0
    games = readlines(filename)
    for game ∈ games
        info_game = get_info_game(game)
        # condition to be a possible game
        if info_game["red"] <= max_red_cubes && info_game["green"] <= max_green_cubes && info_game["blue"] <= max_blue_cubes
            sum_ids_possible_games += info_game["id_game"]
        end
    end
    return sum_ids_possible_games
end

function get_info_game(game::AbstractString)
    info_game = Dict()
    r = split(game, ":")
    info_game["id_game"] = parse(Int, split(r[1]," ")[2])
    info_game["red"] = 0
    info_game["blue"] = 0
    info_game["green"] = 0
    sets = split(r[2],";")
    for set ∈ sets
        set_info = split(set, ",")
        for set_cubes ∈ set_info
            info_cubes = split(set_cubes, " ")
            color = info_cubes[3] # ignore the first element that is always a space
            number_cubes = parse(Int, info_cubes[2])
            if startswith(color, "r")
                if number_cubes > info_game["red"] 
                    info_game["red"] = number_cubes
                end
            elseif startswith(color, "b")
                if number_cubes > info_game["blue"] 
                    info_game["blue"] = number_cubes
                end
            elseif startswith(color, "g")
                if number_cubes > info_game["green"] 
                    info_game["green"] = number_cubes
                end
            end
        end
    end
    return info_game
end

sol_example_1 = sol_part_1("./input_example.txt")
sol_puzzele_part_1 = sol_part_1("./input_puzzle.txt")
println(" Part 1, example: $sol_example_1 \n Part 1, puzzle: $sol_puzzle_part_1")

function sol_part_2(filename::AbstractString)
    games = readlines(filename)
    sum_power = 0
    for game ∈ games
        println(get_power(game))
        sum_power += get_power(game)
    end
    return sum_power
end


function get_power(game::AbstractString)
    sets = split(split(game, ":")[2],";")
    min_red = 0
    min_blue = 0
    min_green = 0
    for set ∈ sets
        set_info = split(set, ",")
        for set_cubes ∈ set_info
            info_cubes = split(set_cubes, " ")
            color = info_cubes[3] # ignore the first element that is always a space
            number_cubes = parse(Int, info_cubes[2])
            if startswith(color, "r")
                min_red = (number_cubes > min_red) ? number_cubes : min_red
            elseif startswith(color, "b")
                min_blue = (number_cubes > min_blue) ? number_cubes : min_blue
            elseif startswith(color, "g")
                min_green = (number_cubes > min_green) ? number_cubes : min_green
            end
        end
    end
    return min_red * min_blue * min_green
end

sol_example_2 = sol_part_2("./input_example.txt")
sol_puzzele_part_2 = sol_part_2("./input_puzzle.txt")
println(" Part 2, example: $sol_example_2 \n Part 2, puzzle: $sol_puzzele_part_2")