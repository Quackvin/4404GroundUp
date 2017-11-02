import matplotlib.pyplot as plt

classes = {}

# with open('data_MeanVar.txt', 'r') as file:
# 	for line in file:
# 		instance = line.split('\t')
# 		features = [float(i) for i in instance[:-1]]
# 		outcome = instance[-1].strip('\n')
#
# 		if outcome not in classes.keys():
# 			classes[outcome] = []
# 		classes[outcome].append(features)
#
# print(classes.keys())
#
# for key in classes.keys():
# 	clss = classes[key]
# 	print(key + ' plotting meanvar')
#
# 	plt.clf()
# 	plt.title('Mean Variance Per Mel Band for all '+ key + ' files')
# 	plt.xlabel('Mel Band')
# 	plt.ylabel('Mean Variance')
# 	for instance in clss:
# 		plt.plot(instance[0::2])
# 	plt.savefig('meanvar/' + key + '.png')


classes = {}
with open('data_all.txt', 'r') as file:
	for line in file:
		instance = line.split('\t')
		features = [float(i) for i in instance[:-1]]
		outcome = instance[-1].strip('\n')

		if outcome not in classes.keys():
			classes[outcome] = []
		classes[outcome].append(features)

for key in classes.keys():
	clss = classes[key]
	print(key + ' plotting mean')

	plt.clf()
	plt.title('Mean Per Mel Band for all '+ key + ' files')
	plt.xlabel('Mel Band')
	plt.ylabel('Mean')
	for instance in clss:
		plt.plot(instance[0::2])
	plt.savefig('mean/' + key.replace('/', '_') + '.png')