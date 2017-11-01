import os
import pickle
import numpy as np
import re

# run this script with no arguments in the folder with all the cpickle files.
# will create a file called data.txt if it doesn't exist already, otherwise will overwrite it

files = {}
with open('meta.txt','r') as metaFile:
	for line in metaFile:
		line = line.split('\t')[0:2]
		name = re.search(r'/(.+)\.',line[0]).group()[1:-1]
		clss = line[1]
		clss = re.sub(r'/', '_', clss)
		files[name] = clss

allFeats = ''
count = 0
for filename in os.listdir('./pickles'):
	if filename.endswith('.cpickle'):
		# get file name
		nameId = re.sub(r'\.cpickle', '', filename)

		filename = './pickles/' + filename
		data = pickle.load(open(filename,'rb'))

		data = np.array(data['feat'][0])

		instanceFeatures = ''
		aves = []

		for feature in range(0, 40):
			featureSlices = data[:, feature]
			aves.append(np.mean(featureSlices))

		ave = np.mean(aves)

		for feature in range(0,40):
			featureSlices = data[:,feature]
			instanceFeatures += str(np.mean(featureSlices)-ave) + '\t'
			instanceFeatures += str(np.std(featureSlices)) + '\t'
			if feature == 39:
				instanceFeatures += files[nameId] + '\n'

		# print(instanceFeatures)
	allFeats += instanceFeatures
	print('file num : ', count, end="\r")
	count += 1
# print(allFeats)

with open('data_MeanVar.txt', 'w') as saveFile:
	saveFile.write(allFeats)