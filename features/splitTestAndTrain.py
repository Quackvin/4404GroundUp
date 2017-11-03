import os
import numpy as np

def method1():
	# Extract test and training data based on a chosen percentage of training data
	# Data is extracted evenly across all data classes (i.e. the proportion or 'car' instances will be the same as 'office'
	# samples.
	# Data are then stored in data_training.txt and data_testing.txt in the data/ directory
	# Note that separatedFeatureExtractor *must* be run first so that the data files for each class are already geenrated
	# and stored in the data/ directory.

	# Parameters
	percentTraining = 0.6

	# Variables
	numberOfInstances = 312
	data = []
	data_training = []
	data_testing = []
	nFiles = 0

	# Open each *_data.txt file and add to a list of all instances, sorted by endpoint
	# Note that this list (of lists) includes the endpoints (classifications) at the end of each row
	for filename in os.listdir('./data'):
		if filename.endswith('_dat.txt'):
			nFiles = nFiles + 1
			with open('./data/' + filename, 'r') as loadFile:
				for line in loadFile:
					data.append(line)

	# Sort data randomly into training and testing bins
	for index in range(0, numberOfInstances ):		# loop through each instance
		if index % 10 < percentTraining*10:			# select percentage for training sata
			for n in range(0, nFiles):				# ... then through each file's data
				data_training.append(data[index + n*numberOfInstances])
		else:
			for n in range(0, nFiles):				# ... or for testing data
				data_testing.append(data[index + n*numberOfInstances])

	print('Proportion training: ', '{:3.2f}'.format(100*np.size(data_training)/np.size(data)))
	print('Proportion testing:  ', '{:3.2f}'.format(100*np.size(data_testing)/np.size(data)))

	# Write to files
	with open('data_training.txt', 'w') as saveFile:
		for line in data_training:
			saveFile.write(line)

	with open('data_testing.txt', 'w') as saveFile:
		for line in data_testing:
			saveFile.write(line)

# split the data_stds file into testing and training, it is made sure that the number of classes in each file is equally proportional
def method2(filename):
    print(os.getcwd())
    classDict = {}
    with open(filename, 'r') as ReadFile:
        with open(filename.split('.')[0]+'_training.txt', 'w') as TrainFile:
            with open(filename.split('.')[0]+'_testing.txt', 'w') as TestFile:
                for line in ReadFile:
                    a = line.split('\t')
                    cls = a[-1]
                    if cls in classDict:
                        classDict[cls] += 1
                    else:
                        classDict[cls] = 1
                    if classDict[cls] % 4 == 0:
                        classDict[cls] = 1
                        TestFile.write(line)
                    else:
                        TrainFile.write(line)

def method3():
    for filename in os.listdir('./data'):
        if 'car' in filename or 'office' in filename :
            with open('./data/'+filename, 'r') as ReadFile:
                with open('data_office_car_training.txt', 'a') as TrainFile:
                    with open('data_office_car_testing.txt', 'a') as TestFile:
                        j = 0
                        for line in ReadFile:
                            j += 1
                            if j%4 == 0:
                                j = 0
                                TestFile.write(line)
                            else:
                                TrainFile.write(line)

        else:
            with open('./data/'+filename, 'r') as ReadFile:
                with open('data_office_car_training.txt', 'a') as TrainFile:
                    with open('data_office_car_testing.txt', 'a') as TestFile:
                        j = 0
                        for line in ReadFile:
                            splitted = line.split('\t')
                            splitted[-1] = 'other\n'
                            newline = '\t'.join(splitted)
                            j += 1
                            if j % 4 == 0:
                                j = 0
                                TestFil
                                e.write(newline)
                            else:
                                TrainFile.write(newline)
def method4():
    for filename in os.listdir('./data'):
        if 'car' in filename or 'office' in filename or 'city_center' in filename or 'forest_path' in filename or 'metro_station' in filename :
            with open('./data/'+filename, 'r') as ReadFile:
                with open('data_office_car_city_forest_metro_training.txt', 'a') as TrainFile:
                    with open('data_office_car_city_forest_metro_testing.txt', 'a') as TestFile:
                        j = 0
                        for line in ReadFile:
                            j += 1
                            if j%4 == 0:
                                j = 0
                                TestFile.write(line)
                            else:
                                TrainFile.write(line)

def method5():
	# Extract test and training data based on a chosen percentage of training data
	# Data is extracted evenly across all data classes (i.e. the proportion or 'car' instances will be the same as 'office'
	# samples.
	# Data are then stored in data_training.txt and data_testing.txt in the data/ directory
	# Note that separatedFeatureExtractor *must* be run first so that the data files for each class are already geenrated
	# and stored in the data/ directory.

	# Parameters
	percentTraining = 0.6

	# Variables
	numberOfInstances = 312
	data = []
	data_training = []
	data_testing = []
	nFiles = 0

	# Open each *_data.txt file and add to a list of all instances, sorted by endpoint
	# Note that this list (of lists) includes the endpoints (classifications) at the end of each row
	with open('data_MeanVar.txt', 'r') as loadFile:
		for line in loadFile:
			data.append(line)

	# Sort data randomly into training and testing bins
	for index in range(0, numberOfInstances ):		# loop through each instance
		if index % 10 < percentTraining*10:			# select percentage for training sata
			for n in range(0, nFiles):				# ... then through each file's data
				data_training.append(data[index + n*numberOfInstances])
		else:
			for n in range(0, nFiles):				# ... or for testing data
				data_testing.append(data[index + n*numberOfInstances])

	print('Proportion training: ', '{:3.2f}'.format(100*np.size(data_training)/np.size(data)))
	print('Proportion testing:  ', '{:3.2f}'.format(100*np.size(data_testing)/np.size(data)))

	# Write to files
	with open('data_meanVar_training.txt', 'w') as saveFile:
		for line in data_training:
			saveFile.write(line)

	with open('data_meanVar_testing.txt', 'w') as saveFile:
		for line in data_testing:
			saveFile.write(line)

method4()
# method4()
# method2('data_MeanVar.txt')
