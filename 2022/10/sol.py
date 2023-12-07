import numpy as np

def add_one_cyle(X, cycles, total_signal_strenght):
	cycles += 1
	if cycles in important_cycles:
		total_signal_strenght += X*cycles
		print(f"Important cycle {cycles}, with X {X} and total {total_signal_strenght} line {line}")

	return total_signal_strenght, cycles


def ex_1():
	file = open("input.txt", "r")
	cycles = 0
	X = 1
	total_signal_strenght = 0
	important_cycles = [20, 60, 100, 140, 180, 220]
	for line in file:
		if line == '\n': continue
		line = line.strip()
		if line[0]=='n': # noop
			total_signal_strenght, cycles = add_one_cyle(X, cycles, total_signal_strenght)
		else: # addx
			total_signal_strenght, cycles = add_one_cyle(X, cycles, total_signal_strenght)
			total_signal_strenght, cycles = add_one_cyle(X, cycles, total_signal_strenght)
			delta_x = int(line.split(" ")[1])
			X += delta_x

	print(f"The sum of signal strenght of the important cycles is {total_signal_strenght}")


def add_one_cyle_2(X, cycles, interface):
	cycles += 1

	y = int(np.floor(cycles/40))
	if y >= 6: y = 5

	x = cycles % 40
	if x == 0: x = 40
	x = x-1

	if x <= X+1 and x >= X-1: sprit = "#"
	else: sprit = "."

	interface[y,x] = sprit
	#print(*interface, sep="\n")
	print(interface[y,:])
	print(f"cycle {cycles}, CRT draws in pos: {x}, X: {X}, sprit: {sprit}")

	return cycles, interface

def ex_2():
	np.set_printoptions(suppress=True,linewidth=1000,threshold=1000)
	file = open("input.txt", "r")
	cycles = 0
	X = 1

	#creation of interface
	interface =[]
	for i in range(0,6):
		line_i = []
		for j in range(0,40):
			line_i.append(".")
		interface.append(line_i)
	interface = np.array(interface)

	for line in file:
		if line == '\n': continue
		line = line.strip()
		if line[0]=='n': # noop
			 cycles, interface = add_one_cyle_2(X, cycles, interface)
		else: # addx
			cycles, interface = add_one_cyle_2(X, cycles, interface)
			cycles, interface = add_one_cyle_2(X, cycles, interface)
			delta_x = int(line.split(" ")[1])
			X += delta_x
			#cycles, interface = add_one_cyle_2(X, cycles, interface)
	print('\n --- final --- \n')
	print(*interface, sep="\n")
if __name__=="__main__":
	ex_2()
