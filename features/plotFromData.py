import matplotlib.pyplot as plt

classes = {}
with open('data_MeanVar.txt', 'r') as file:
	for line in file:
		instance = line.split('\t')
		features = [float(i) for i in instance[:-1]]
		outcome = instance[-1].strip('\n')

		classes[outcome] = []

print("dict made")

with open('data_MeanVar.txt', 'r') as file:
	for line in file:
		instance = line.split('\t')
		features = [float(i) for i in instance[:-1]]
		outcome = instance[-1].strip('\n')

		classes[outcome].append(features)

print("dict filled")

for key in classes.keys():
	clss = classes[key]
	print('class plotting')

	plt.clf()
	plt.title(key)
	for instance in clss:
		plt.plot(instance)

	plt.show()