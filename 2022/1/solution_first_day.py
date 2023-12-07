
def answer_first_puzzle():
	file = open("input1.txt", "r")

	elf_winner_calories = 0
	elf_calories = 0

	for line in file:
		if line == '\n':
			if (elf_calories > elf_winner_calories):
				elf_winner_calories = elf_calories
			elf_calories = 0
		else:
			elf_calories += int(line.strip())

	if (elf_calories > elf_winner_calories):
		elf_winner_calories = elf_calories

	print(f"Calories of elf winner: {elf_winner_calories}")

def answer_second_puzzle():
	file = open("input2.txt", "r")

	elf_calories = 0
	elf_calories_list = []

	for line in file:
		if line == '\n':
			elf_calories_list.append(elf_calories)
			elf_calories = 0
		else:
			elf_calories += int(line.strip())

	elf_calories_list.append(elf_calories)

	elf_calories_list.sort(reverse=True)
	answer = sum(elf_calories_list[:3])
	print(f"Calories of 3 top elves: {answer}")

answer_second_puzzle()
