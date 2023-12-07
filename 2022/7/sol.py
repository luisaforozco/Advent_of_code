class Branch:
	def __init__(self, nameI, parentI, pathI) -> None:
		self.name = nameI
		self.parent = parentI
		self.sons = []  #containing elements of the type Branch
		self.size = 0
		self.path = pathI
		self.files = []
	
	def add_son(self, sonI):
		self.sons.append(sonI)

	def give_son_named(self, name_sonI):
		for i in self.sons:
			if i.name == name_sonI:
				return i
		print(f'Dir {name_sonI} does not exist in {self.path}')

	def calc_size(self):
		total_size = 0
		for i in self.files:
			# print(f"size is {i.size}")
			total_size += i.size
		for j in self.sons:
			total_size += j.calc_size()
		return total_size

	def calc_size_smaller_than(self, max_size):
		size_local = 0
		# checking this dir
		dir_size = self.calc_size()
		#print(f"dir size: {dir_size}")
		if(dir_size <= max_size):
			size_local += dir_size
			print(f"dir size is smaller than 100000: {dir_size}")
		return size_local

	def calc_total_size_dirs_smaller_than(self, max_size, size_total):
		# checking subdirectories
		for j in self.sons:
			size_total += j.calc_size_smaller_than(max_size)
			size_total = j.calc_total_size_dirs_smaller_than(max_size, size_total)
		
		print(f"size total: {size_total}")
		return size_total

	def find_directory_closest_to(self, size_target, best_dir):
		dir_size = self.calc_size()
		if (dir_size >= size_target) and (best_dir.calc_size() > dir_size):
			best_dir = self

		for j in self.sons:
			best_dir = j.find_directory_closest_to(size_target, best_dir)

		return best_dir

if __name__ == "__main__":
	file = open("input.txt", "r")
	
	current_branch = None	
	root_branch = None
	for line in file:
		if line == '\n': next
		line = line.strip()
		line_splitted = line.split(" ")
		# current_path = ""
		if line_splitted[0] == "$":     #reading a command
			if line_splitted[1] == "cd":		#change dir
				if line_splitted[2] == "/": 
					# current_path = "root"
					current_branch = Branch("", None, "root")
					root_branch = current_branch
				elif line_splitted[2] == "..":
					current_branch = current_branch.parent
					# current_path = current_branch.name
				else: 					# go to directory line_splitted[2]
					current_branch = current_branch.give_son_named(line_splitted[2])
			elif line_splitted[1] == "ls":	
				reading_mode = True

		elif line_splitted[0] == "dir":
			new_dir = Branch(line_splitted[1], current_branch, current_branch.path+"/"+line_splitted[1])
			current_branch.sons.append(new_dir)
		else: 			# this should be a file
			new_file = Branch(line_splitted[1], current_branch, current_branch.path+"/"+line_splitted[1])
			new_file.size = int(line_splitted[0])
			current_branch.files.append(new_file)
	
	# look through the whole tree for the size of the dir's
	size_dirs_smaller = 0
	size_dirs_smaller = root_branch.calc_total_size_dirs_smaller_than(100000, size_dirs_smaller)
	print(f'Total size of dirs of size <  100000 {size_dirs_smaller}')

	# second exercise:
	total_used_space = root_branch.calc_size()
	unused_space = 70000000 - total_used_space
	size_required = 30000000 - unused_space
	print(f"Unused space: {unused_space}, size required: {size_required}")
	best_to_delete = root_branch.find_directory_closest_to(size_required, root_branch)
	print(f"The size of the best directory to delete is: {best_to_delete.calc_size()}")

