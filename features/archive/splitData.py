data = []

with open('data_means.txt', 'r') as loadFile:
	for line in loadFile:
		data.append(line)

length = len(data)

count = 0
testing = []
training = []
for i in range(length):
	if i < 3*length/4:
		training.append(data[i])
	else:
		testing.append(data[i])

with open('data_means_testing.txt', 'w') as saveFile:
	for line in testing:
		saveFile.write(line)

with open('data_means_training.txt', 'w') as saveFile:
	for line in training:
		saveFile.write(line)

