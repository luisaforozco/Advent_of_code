import numpy as np
import time

def check_if_contained(sections_1, sections_2):
	"""
	Args:
		sections_1 :  List [start:str, end:str]
	"""
	if int(sections_1[0]) <= int(sections_2[0]) and int(sections_1[1]) >= int(sections_2[1]):
		print(f"{sections_1} contains {sections_2}")
		return 1
	if int(sections_2[0]) <= int(sections_1[0]) and int(sections_2[1]) >= int(sections_1[1]):
		print(f"{sections_1} is contained by {sections_2}")
		return 1
	#print(f"Not containing {sections_1} and {sections_2}")
	return 0

def check_if_overlaps(sections_1, sections_2):
	sections_1 = [int(x) for x in sections_1]
	sections_2 = [int(x) for x in sections_2]

	range_1 = range(sections_1[0], sections_1[1]+1)
	range_2 = range(sections_2[0], sections_2[1]+1)

	for i in range_1:
		if i in range_2: return 1

	for i in range_2:
		if i in range_1: return 1

	return 0

def check_if_overlaps_H(sections_1, sections_2):
	sections_1 = [int(x) for x in sections_1]
	sections_2 = [int(x) for x in sections_2]

	if sections_1[1] < sections_2[0] or sections_2[1] < sections_1[0]:
		return 0

	return 1

def exercise_1():
	file = open("input_test.txt", "r")
	answer = 0

	for line in file:
		if line == '\n': next
		else:
			elf_pairs=(line.strip()).split(',')
			elf_assignment = [None] * len(elf_pairs)
			for i in range(0,len(elf_pairs)):
				elf_assignment[i]=elf_pairs[i].split('-')
			#print (f"{elf_assignment[0]} ennus {elf_assignment[1]}")

			answer += check_if_contained(elf_assignment[0],elf_assignment[1])

	print(f"Fully contained pairs = {answer}")
	return answer

if __name__ == "__main__":
	file = open("input.txt", "r")
	answer_H = 0
	answer_L = 0
	Luisa_fastest = 0
	Herman_fastest = 0
	draw_time = 0
	time_L = 0
	time_H = 0
	total = 0
	for line in file:
		if line == '\n': next
		else:
			elf_pairs=(line.strip()).split(',')
			elf_assignment = [None] * len(elf_pairs)
			for i in range(0,len(elf_pairs)):
				elf_assignment[i]=elf_pairs[i].split('-')
			#print (f"{elf_assignment[0]} ennus {elf_assignment[1]}")
			time_start_L = time.time()
			answer_L += check_if_overlaps(elf_assignment[0],elf_assignment[1])
			time_L += time.time() - time_start_L
			#print(f"Time Luisa: { time_L}")

			time_start_H = time.time()
			answer_H += check_if_overlaps_H(elf_assignment[0],elf_assignment[1])
			time_H += time.time() - time_start_H
			#if (time_L > time_H): Herman_fastest += 1
			#elif (time_L < time_H): Luisa_fastest += 1
			#else: draw_time += 1
			#total += 1
			#print(f"Time Herman: {time.time() - time_start_H }")
	#print(f"Herman: {Herman_fastest/total}, Luisa: {Luisa_fastest/total}, draw: {draw_time/total}")
	print(f"Total times, Herman: {time_H}, Luisa: {time_L}, H/L = {time_H/time_L}")
	print(f"Overlapping pairs (Herman) = {answer_H}")
	print(f"Overlapping pairs (Luisa) = {answer_L}")
