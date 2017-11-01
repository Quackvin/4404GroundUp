keyList = ['beach\n', 'bus\n', 'cafe/restaurant\n', 'car\n', 'city_center\n', 'forest_path\n', 'grocery_store\n',
           'home\n', 'library\n', 'metro_station\n', 'office\n', 'park\n', 'residential_area\n', 'train\n', 'tram\n']

filename = 'Result_12.txt'		# Result_12.txt appears to have the best results so far

with open(filename, 'r') as results:
	for line in results:
		# Remove opening annotation and convert to dictionary
		line = line.replace('Confusion Matrix:', '')
		cMat = eval(line)


		for key in keyList:
			rowSum = 0;
			tmp = cMat[key]
			for sub_key in keyList:
				print('{:3d}'.format(tmp[sub_key]), end=' ')
				rowSum = rowSum + tmp[sub_key]
			print(' {:3d}'.format(rowSum))

		break
