
# Matrix Operations
import numpy
import heapq

# I/O Part
print("Please give the file name at the same directory with script: ")
fileName = input(" ~ ")

with open(fileName) as f:
	firstLine = f.readline()
	numberOfPeople = int(firstLine[10:])
	
	# All people names
	people = []
	for i in range(0, numberOfPeople):
		line = f.readline()
		name = line.split()[-1]
		name = name.replace("\"", "")
		people.append(name)

	# In order to skip '*Edges' line
	f.readline()

	# All edges
	allEdges = f.readlines()

	# Matrix for pages
	matrix = numpy.zeros((numberOfPeople, numberOfPeople))
	vert = []
	for edge in allEdges:
		edge = edge.replace("\n", "")
		vert = edge.split()
		vert = [float(i) for i in vert]
		matrix[vert[1]-1][vert[0]-1] = 1
		matrix[vert[0]-1][vert[1]-1] = 1

	# Teleport value
	teleportValue = 0.15 / numberOfPeople

	for i in range(0, numberOfPeople):
		total = 0
		for j in range(0, numberOfPeople):
			total += matrix[i][j]
		
		if total != 0:
			value = 0.85 / total
		
		for j in range(0, numberOfPeople):
			if matrix[i][j] == 1.0:
				matrix[i][j] = value + teleportValue
			else:
				matrix[i][j] = teleportValue

	# Teleport matrix
	teleportVector = numpy.empty((1, numberOfPeople))
	teleportVector.fill(0.15)

	# Initial matrix multiplication
	result1 = numpy.empty((1, numberOfPeople))
	result2 = numpy.dot(teleportVector, matrix)
	result2 = result2 / numpy.sum(result2)

	# Loop until rank matrix is same as previous one
	while not numpy.allclose(result1, result2):
		result1 = result2
		result2 = numpy.dot(result2, matrix)
		result2 = result2 / numpy.sum(result2)

	result = numpy.array(result1)[0].tolist()
	dictionary = dict(zip(people, result))
	keys = heapq.nlargest(50, dictionary, key=dictionary.get)
	
	index = 1
	for key in keys:
		print(str(index) + ". " + key + " -> " + str(dictionary[key]))
		# First 10 digits from point
		#print(str(index) + ". " + key + " -> " + "%.10f" % dictionary[key])
		index += 1

f.close()