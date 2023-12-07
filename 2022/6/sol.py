def check_if_repeated(packet):
	return len(set(packet)) == len(packet)


if __name__ == "__main__":
	file = open("input_test.txt", "r")
	num_characters = 4 # 1st exercise
	num_characters = 14 # 2nd exercise

	for line in file:
		if line == '\n': next
		line = line.strip()
		for i in range(num_characters,len(line)):
			if check_if_repeated(line[(i-num_characters):i]): break


	print(f'the result is {i}')



