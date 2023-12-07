import numpy as np

def move_head(direction, pos_head):
	delta_x = 0
	delta_y = 0
	if direction == 'U': delta_y = 1
	elif direction == 'D': delta_y = -1
	elif direction == 'R': delta_x = 1
	else: delta_x = -1
	pos_head += np.array([delta_x, delta_y])
	return pos_head

def move_tail(pos_head, pos_tail):
	diff_pos = pos_head - pos_tail
	if np.linalg.norm(np.array(diff_pos)) < 1.5: # dont have to move it
		return pos_tail
	elif np.linalg.norm(np.array(diff_pos)) > 2: # diagonal move 
		if abs(diff_pos[0]) == 1:
			pos_tail[0] = pos_head[0]
			pos_tail[1] += (diff_pos[1]/2.0)
		elif abs(diff_pos[1]) == 1:
			pos_tail[0] += (diff_pos[0]/2.0)
			pos_tail[1] = pos_head[1]
		else:
			pos_tail[0] += (diff_pos[0]/2.0)
			pos_tail[1] += (diff_pos[1]/2.0)

	else: # just two away in straight line
		pos_tail += (diff_pos/2.0).astype(int)
	return pos_tail



if __name__ == "__main__":
	
	pos_head = np.array([0,0])
	pos_tail = [np.array([0,0]) for x in range(10)]
	his_head = []
	his_tail = []

	file = open("input.txt", "r")
	for line in file:
		if line == '\n': continue
		line = line.strip()
		direction = line.split(" ")[0]
		steps = int(line.split(" ")[1])

		for i in range(0,steps):
			pos_tail[0] = move_head(direction, pos_tail[0])
			for j in range(1,10):
				pos_tail[j] = move_tail(pos_tail[j-1], pos_tail[j])

			his_tail.append(np.copy(pos_tail[-1]))
			his_head.append(np.copy(pos_tail[0]))

	tuple_his_tail = []
	for i in his_tail :
		tuple_his_tail.append(tuple(i))
		
	print(f'positions head {his_head}, len {len(his_head)}')
	print(f'positions tail {his_tail}')
	answer = len(set(tuple_his_tail))

	print(f'Number of unique coordinates is {answer}')


