
def calculate_score(opponents_play, your_play):
	#opponent
	A = 1 #rock
	B = 2 #paper
	C = 3 #scissors

	#your play
	X = 1 #rock
	Y = 2 #paper
	Z = 3 #scissors

	#result
	win = 6
	draw = 3
	lose = 0

	if (opponents_play == 'A'):
		if (your_play == 'X'): score = draw + X
		elif (your_play == 'Y'): score = win + Y
		else: score = lose + Z
	elif(opponents_play == 'B'):
		if (your_play == 'X'): score = lose + X
		elif (your_play == 'Y'): score = draw + Y
		else: score = win + Z
	else:
		if (your_play == 'X'): score = win + X
		elif (your_play == 'Y'): score = lose + Y
		else: score = draw + Z

	return score

def calculate_score_2(opponents_play, outcome_match):
	#opponent
	A = 1 #rock
	B = 2 #paper
	C = 3 #scissors

	#your play
	X = 0 #lose
	Y = 3 #draw
	Z = 6 #win

	#result
	rock = 1
	paper = 2
	scissors = 3

	if (opponents_play == 'A'):
		if (outcome_match == 'X'): score = scissors + X
		elif (outcome_match == 'Y'): score = rock + Y
		else: score = paper + Z
	elif(opponents_play == 'B'):
		if (outcome_match == 'X'): score = rock + X
		elif (outcome_match == 'Y'): score = paper + Y
		else: score = scissors + Z
	else:
		if (outcome_match == 'X'): score = paper + X
		elif (outcome_match == 'Y'): score = scissors + Y
		else: score = rock + Z

	return score

if __name__ == "__main__":
	file = open("input.txt", "r")
	score = 0
	for line in file:
		if line == '\n': next
		else:
			play = line.strip().split(' ')
			#score += calculate_score(play[0], play[1]) #exercise 1
			score += calculate_score_2(play[0], play[1]) #exercise 2

	print(f"Final score: {score}")
