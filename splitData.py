import os
print(os.getcwd())

with open('features/data_means_training.txt', 'w') as dataTrain:
	with open('features/data_means_testing.txt', 'w') as dataTest:
		with open('features/data_means.txt', 'r') as dataFile:
			j = 0
			for line in dataFile:
				if j%4 == 0:
					dataTest.write(line)
					j += 1
				else:
					dataTrain.write(line)
					j += 1