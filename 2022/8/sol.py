import numpy as np

def is_visible(list_trees: np.array):
	last_element = list_trees[-1]
	who_is_bigger_or_equal = list_trees >= last_element
	# remove the last element (himself, so always True)
	# True is 1, False is 0
	if sum(who_is_bigger_or_equal[:-1]) > 0: return False
	else: return True

def count_visible_trees(map_trees: np.array):
	visible = 0

	# count the edges
	shape = np.shape(map_trees)
	visible += 2*(shape[0]-2) # substracting start and end
	visible += 2*shape[1]

	# count inside
	for i in range(1,shape[0]-1):
		for j in range(1,shape[1]-1):
			top = map_trees[0:i+1,j]
			if is_visible(top):
				visible += 1
				continue

			left = map_trees[i,0:j+1]
			if is_visible(left):
				visible += 1
				continue

			right = map_trees[i,j:]
			if is_visible(np.flip(right)):
				visible += 1
				continue

			bottom = map_trees[i:,j]
			if is_visible(np.flip(bottom)):
				visible += 1
				continue

	return visible

def calc_viewing_distance(list_trees: np.array):
	last_element = list_trees[-1]
	viewing_distance = 1
	for i in range(len(list_trees)-2,-1,-1):
		print(i)
		if(list_trees[i] < last_element):
			viewing_distance += 1
		elif(list_trees[i] == last_element):
			return viewing_distance
		else: return viewing_distance

	return viewing_distance - 1


def calc_scenic_score(map_trees: np.array):
	best_score = 0
	shape = np.shape(map_trees)
	for i in range(1,shape[0]-1):
		for j in range(1,shape[1]-1):
			top = map_trees[0:i+1,j]
			left = map_trees[i,0:j+1]
			right = np.flip(map_trees[i,j:])
			bottom = np.flip(map_trees[i:,j])
			scenic_score = calc_viewing_distance(top)\
						 * calc_viewing_distance(left)\
						 * calc_viewing_distance(right)\
						 * calc_viewing_distance(bottom)
			if scenic_score > best_score: best_score = scenic_score

	return best_score


list_map = []
if __name__ == "__main__":
	# 1. read the file and load the contents to list_map
	file = open("input.txt", "r")
	for line in file:
		if line == '\n': continue
		line = line.strip()
		line = list(map(int,line))
		list_map.append(line)

	# 2. Search for answer in list_map
	visible_trees = count_visible_trees(np.array(list_map))
	print(f"There are {visible_trees} visible trees.")

	# 2nd exercise
	best_scenic_score = calc_scenic_score(np.array(list_map))
	print(f"The best scenic score is: {best_scenic_score}")

