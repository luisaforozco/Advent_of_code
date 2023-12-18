struct Node
    name::String
    L::String
    R::String
end

function read_network(input_file)
    lines = readlines(input_file)
    instructions = ""
    nodes = []
    for line in lines
        if line == "\n" || line == ""
            continue
        elseif contains(line, "=")
            name = strip(split(line, "=")[1])
            L = replace(split(split(line, "=")[2], ", ")[1], " (" => "")
            R = replace(split(split(line, "=")[2], ", ")[2], ")" => "")
            push!(nodes, Node(name, L, R))
        else # instructions
            instructions = line
        end
    end
    return instructions, Dict(n.name => n for n in nodes)
end    

function num_steps_to_ZZZ(instructions, nodes)
    steps = 0
    current_node = nodes["AAA"]
    len_ins = length(instructions)
    while true
        steps += 1
        index_instruction = (steps%len_ins > 0) ? steps%len_ins : len_ins
        instruction = instructions[index_instruction]
        next_node = get(nodes, getfield(current_node, Symbol(instruction)), nothing)
        #println("i: $index_instruction, ins : $instruction, curr node: $current_node, next node: $next_node") #debug
        if next_node.name == "ZZZ"
            return steps
        end
        current_node = next_node
    end
    return steps
end

function sol_part_1(input_file)
    instructions, nodes = read_network(input_file)
    return num_steps_to_ZZZ(instructions, nodes)
end

sol_example_1 = sol_part_1("./input_example1b.txt")
sol_puzzle_part_1 = sol_part_1("./input_puzzle.txt")
println(" Part 1, example: $sol_example_1 \n Part 1, puzzle: $sol_puzzle_part_1")

function num_steps_to_all_Z(instructions, nodes)
    steps = 0
    current_nodes = [n for (key, n) in nodes if endswith(n.name, "A")]
    len_ins = length(instructions)
    while true
        steps += 1
        index_instruction = (steps%len_ins > 0) ? steps%len_ins : len_ins
        instruction = instructions[index_instruction]
        for (i, curr_node) in enumerate(current_nodes)
            next_node = get(nodes, getfield(curr_node, Symbol(instruction)), nothing)
            current_nodes[i] = next_node
        end
        if count(node -> endswith(node.name, "Z"), current_nodes) == length(current_nodes)
            return steps
        end
        if steps%1000 == 0
            println("steps: $steps")
        end
    end
    return steps
end

function sol_part_2(input_file)
    instructions, nodes = read_network(input_file)
    return num_steps_to_all_Z(instructions, nodes)
end

sol_example_2 = sol_part_2("./input_example2.txt")
sol_puzzle_part_2 = sol_part_2("./input_puzzle.txt")
println(" Part 2, example: $sol_example_2 \n Part 2, puzzle: $sol_puzzle_part_2")