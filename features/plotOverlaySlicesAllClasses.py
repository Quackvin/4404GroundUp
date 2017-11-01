import os
import pickle
import numpy as np
import re
import matplotlib.pyplot as plt

# run this script with no arguments in the folder with all the cpickle files.
# will create a file called data.txt if it doesn't exist already, otherwise will overwrite it
files = {}
classes = {}
with open('meta.txt','r') as metaFile:
	for line in metaFile:
		line = line.split('\t')[0:2]
		name = re.search(r'/(.+)\.',line[0]).group()[1:-1]
		clss = line[1]
		clss = re.sub(r'/', '_', clss)
		files[name] = clss
		classes[clss] = 0

# count = 0
for filename in os.listdir('./pickles'):
	if filename.endswith('.cpickle'):
		# get file name
		nameId = re.sub(r'\.cpickle', '', filename)

		filename = './pickles/' + filename
		data = pickle.load(open(filename,'rb'))

		data = np.array(data['feat'][0])

		outcome = files[nameId]
		graphNum = classes[outcome]

		plt.clf()

		if(classes[outcome] < 10):
			aves = []

			for feature in range(40):
				featureSlices = data[:, feature]
				aves.append(np.mean(featureSlices))

			ave = np.mean(aves)

			plt.title('File: ' + nameId + '->' + outcome)
			plt.gca().set_ylim(-11,0)
			plt.xlabel('Mel Band Feature Number')
			plt.ylabel('Log Magnitude')

			for i in range(np.shape(data)[1]):
				plt.plot(data[i,:]-ave)
			plt.savefig('newPlots/'+outcome+str(graphNum)+'.png')
			classes[outcome] += 1
		# count += 1
	# if all classifications have 10 then break
	numKeys = len(classes.keys())
	for key in classes.keys():
		if classes[key] > 10:
			numKeys -= 1
	if numKeys == 0:
		break