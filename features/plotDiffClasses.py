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
		classes[clss] = {'means':[], 'stdDevs':[], 'aveMeans':[], 'aveStds':[], 'mins':[], 'maxs':[]}

for filename in os.listdir('./pickles'):
	if filename.endswith('.cpickle'):
		# get file name
		nameId = re.sub(r'\.cpickle', '', filename)
		filename = './pickles/' + filename
		data = pickle.load(open(filename,'rb'))

		data = np.array(data['feat'][0])
		outcome = files[nameId]

		mean = []
		stdD = []
		classes[outcome]['mins'] = np.amin(data, axis=0)
		classes[outcome]['maxs'] = np.amax(data, axis=0)
		for i in range(np.shape(data)[1]):
			mean.append(np.mean(data[:,i]))
			stdD.append(np.std(data[:,i]))
		classes[outcome]['means'].append(mean)
		classes[outcome]['stdDevs'].append(stdD)

for key in classes.keys():
	cate = classes[key]
	cate['means'] = np.array(cate['means'])
	cate['stdDevs'] = np.array(cate['stdDevs'])

	dim = np.shape(cate['means'])
	for i in range(dim[1]):
		cate['aveMeans'].append(np.mean(cate['means'][:,i]))
		cate['aveStds'].append(np.mean(cate['stdDevs'][:, i]))

	plt.title('Averages')
	plt.plot(cate['aveMeans'], label=key)

plt.legend()
plt.show()


plt.clf()
for key in classes.keys():
	cate = classes[key]
	plt.title('Standard Deviations')
	plt.plot(cate['aveStds'], label=key)

plt.legend()
plt.show()