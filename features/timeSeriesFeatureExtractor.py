import os
import pickle
import numpy as np
import re
import matplotlib.pyplot as plt

# run this script with no arguments in the folder with all the cpickle files.
# will create a file called data.txt if it doesn't exist already, otherwise will overwrite it
targetOutcome = 'office'
outputFile = 'data_' + targetOutcome + '.txt'

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


		for i in range(np.shape(data)[1]):
			plt.plot(data[i,:])
			# print(np.shape(np.fft.rfft(data[:,i])))
		# plt.plot(data[0,:])
		plt.show()
		count += 1
	if count>20:
		break

		# print(instanceFeatures)
	allFeats += instanceFeatures
print(allFeats)

# with open(outputFile, 'w') as saveFile:
# 	saveFile.write(allFeats)