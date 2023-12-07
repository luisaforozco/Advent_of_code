def move_create_one_by_one(creates,van,naar,ncreates):
	for i in range(0,ncreates):
		creates[naar].append(creates[van][-1])
		creates[van].pop(-1)
	return creates

def move_creates(creates,van,naar,ncreates):
	creates[naar].extend(creates[van][-ncreates:])
	del creates[van][-ncreates:]
	return creates

if __name__ == "__main__":
	file = open("input.txt", "r")
	creates = []
	for i in range(0,9):
		creates.append([])


	for line in file:
		if line == '\n': next
		elif '[' in line:
			for i in range(1,len(line),4):
				if not line[i] == ' ' :creates[int((i+3)/4-1)].insert(0,line[i])
		elif 'move' in line:
			line = line.strip().split(' ')
			ncreates = int(line[1])
			van = int(line[3]) - 1
			naar = int(line[5]) - 1
			print(f'ncreates {ncreates} , van {van} , naar {naar}')
			#creates = move_create_one_by_one(creates,van,naar,ncreates) #ex 1
			creates = move_creates(creates,van,naar,ncreates)
		print(f'creates is {creates}')

	result = ""
	for i in range(0,9):
		if len(creates[i]) > 0:
			result += creates[i][-1]

	print(f'the result is {result}')



