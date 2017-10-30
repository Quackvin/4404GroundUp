import os
import pickle
import numpy as np
import re

# run this script with no arguments in the folder with all the cpickle files.
# will create a file called data.txt if it doesn't exist already, otherwise will overwrite it

files = {}
categories = {}
with open('meta.txt','r') as metaFile:
	for line in metaFile:
		line = line.split('\t')[0:2]
		name = re.search(r'/(.+)\.',line[0]).group()[1:-1]
		clss = line[1]
		clss = re.sub(r'/', '_', clss)
		files[name] = clss
		categories[clss] = ''

count = 0
for filename in os.listdir('./pickles'):
	if filename.endswith('.cpickle'):
		# get file name
		nameId = re.sub(r'\.cpickle', '', filename)

		filename = './pickles/' + filename
		data = pickle.load(open(filename,'rb'))

		data = np.array(data['feat'][0])

		instanceFeatures = ''
		for feature in range(0,40):
			featureSlices = data[:,feature]
			instanceFeatures += str(np.mean(featureSlices)) + '\t'
			instanceFeatures += str(np.std(featureSlices)) + '\t'
			if feature == 39:
				outcome = files[nameId]
				instanceFeatures += outcome + '\n'
				categories[outcome] += instanceFeatures

for key in categories.keys():
	outfile = 'data/' + key + '_data.txt'
	with open(outfile, 'w') as saveFile:
		saveFile.write(categories[key])