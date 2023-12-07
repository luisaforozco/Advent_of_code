import numpy as np

def give_repeated_character(str_a, str_b):
	""" Exercise 1"""
	for i in str_a:
		if (str_b.count(i) > 0):
			print(f"Duplicated character is: {i}")
			return i

	print('Couldnt find duplicated character')

def give_value_char(character):
	""" Exercise 1 """
	asci_a = ord('a')
	if ord(character) >= asci_a: #if lower case
		return ord(character) - ord('a') + 1
	else: #upper case
		return ord(character) - ord('A') + 27

def excercise_1():
	file = open("input.txt", "r")
	score = 0
	for line in file:
		if line == '\n': next
		else:
			lenght = len(line.strip())
			if lenght%2 == 0: lenght = int(lenght/2)
			else: print('The lenght of this line is odd')
			first_string = line[0:lenght]
			second_string = line[lenght:]
			rep_character = give_repeated_character(first_string, second_string)
			score += give_value_char(rep_character)

	print(f"Final score: {score}")


def find_repeated_element(list_bags):

	for i in list_bags[0]: #going trough the chars or 1st bag
		repeatings = 1
		for j in range(1,len(list_bags)):
			if (list_bags[j].count(i) > 0): repeatings += 1

		if(repeatings == len(list_bags)): return i

	print('Couldnt find common character in the bags')

if __name__ == "__main__":
	file = open("input.txt", "r")
	count_group = 0
	list_3_bags = []
	sum_priorities_badges = 0
	for line in file:
		if line == '\n': next
		else:
			list_3_bags.append(line.strip())
			count_group += 1
			if count_group == 3:
				badge = find_repeated_element(list_3_bags)
				print(badge)
				sum_priorities_badges += give_value_char(badge)
				count_group = 0
				list_3_bags = []

	print(f"Sum of priorities: {sum_priorities_badges}")
