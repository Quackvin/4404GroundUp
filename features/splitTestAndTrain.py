import os
import numpy as np

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
	if filename.endswith('_data.txt'):
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
