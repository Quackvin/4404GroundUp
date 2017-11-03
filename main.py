import lcs as lcsModule
import classifier as classifierModule
import log as logModule
import environment, json, time

def main():
	# Parameters: [numberOfTrainingIterations, maxPopulationSize,
	# 				coveringWildcardProbability, ruleRangesFactor,
	# 				fitnessPowerFactor, deletionThreshold, deletionFitnessScale,
	# 				aveIterationsBtwnGARuns, crossoverProb, allelMutationProb, wildcardMutationProb, mutationScale,
	# 				subsumtionExpThreshold, subsumptionAccuracyThreshold]
	parameterList = [10000, 100,
					 0.3, 0.5,
					 5, 30, 0.2,
					 55, 0.5, 0.02, 0.1, 0.1,
					 20, 0.9]
	# Allocate training and testing files
	testfile = './features/data_office_car_only_testing.txt'
	trainingfile = './features/data_office_car_only_training.txt'
	# Name of save file for population
	populationSaveFile = 'classifierPopulation'+str(parameterList)+'.json'
	# Initialise log
	log = logModule.Log('./testing_result.txt', 'error.txt')

	# Name of population file to load, don't load if empty string
	loadPopulationFile = ''

	start = time.time()

	train(trainingfile, parameterList, log, populationSaveFile, loadPopulationFile)
	test(testfile, parameterList , log, populationSaveFile)

	print('Time taken (s): ', time.time()-start)

def train(trainingFile, parameterList, log, saveFile, loadPop):
	# Load training instances from file
	env = environment.Environment(trainingFile)
	# Initialise LCS
	lcs = lcsModule.LCS(parameterList, log)

	if loadPop:
		loadPopulation(lcs, loadPop)

	print('**********Training Start*********')
	while True:
		for instance in env.instances:
			lcs.currIter += 1

			# Generate match set, record matchSetSize for later use
			matchSetSize = lcs.doMatching(instance)

			lcs.doCorrectSet(instance)

			if len(lcs.correctSet) == 0:
				lcs.doCovering(instance)

			# Update classifier parameters
			lcs.updateParameters(matchSetSize)

			# Perform genetic algorithm
			if len(lcs.correctSet) > 2 and (lcs.getAverageTimePeriod() > lcs.GAThreshold) :
				print('iteration: ', lcs.currIter, " --- CorrectSet size: ", str(len(lcs.correctSet)), ' --- GA run: 1', end='   \r', flush=True)
				lcs.GA(instance.features)  # includes GA subsumption
			else:
				print('iteration: ', lcs.currIter, " --- CorrectSet size: ", str(len(lcs.correctSet)), ' --- GA run: 0', end='   \r', flush=True)

			if lcs.doCorrectSetSubsumption:
				lcs.correctSetSubsumption()

			# Put classifiers from correct and match sets back in the population
			lcs.consolidateClassifiers()

			if len(lcs.population) > lcs.maxPopSize:
				lcs.doDeletion()

			endcondition = lcs.currIter > lcs.maxNumberOfIteration
			if endcondition:
				savePopulation(lcs.population, saveFile)
				print('**********Training Done**********')
				return 0

def test(testfile, parameterList , log , saveFile):
	print('**********Testing Start*********')
	# Load testing instances from file
	env = environment.Environment(testfile)
	# Initialise LCS
	lcs = lcsModule.LCS(parameterList, log)
	# Load trained population
	loadPopulation(lcs, saveFile)

	correctCount = 0
	numberOfInstance = 0
	numberOfUncovered = 0

	confusionMatrix        = env.initConfusionMatrix()
	confusionMatrix_ratio  = env.initConfusionMatrix()

	for instance in env.instances:
		numberOfInstance += 1

		# Check instance against classifier population
		result = lcs.classifyInstance(instance)

		if result == -1:
			numberOfUncovered += 1
			confusionMatrix[instance.outcome]["Uncovered"] += 1
		else:
			confusionMatrix[instance.outcome][result] += 1

		if result == instance.outcome:
			correctCount += 1

	result = correctCount / numberOfInstance
	print("---Accuracy: " + str(result))
	print("---Number of uncovered instances:" + str(numberOfUncovered))
	print('**********Testing Done*********')

	for cls in confusionMatrix:
		class_occurance_sum = 0
		for cls2 in confusionMatrix[cls]:
			class_occurance_sum += confusionMatrix[cls][cls2]

		for cls3 in confusionMatrix[cls]:
			confusionMatrix_ratio[cls][cls3] = confusionMatrix[cls][cls3]/class_occurance_sum

	log.logMessage("Confusion Matrix: " + str(confusionMatrix))
	log.logMessage("Confusion Ration Matrix: " + str(confusionMatrix_ratio))
	log.logTestResult(result, numberOfUncovered, parameterList)





def savePopulation(population, fileName):
	print('\nSaving')
	with open(fileName, 'w') as writeFile:
		for classifier in population:
			classifierDict = classifier.__dict__.copy()
			classifierDict['rules'] = classifierDict['rules'].__dict__
			classifierString = json.dumps(classifierDict) + '\n'
			writeFile.write(classifierString)


def loadPopulation(lcs, fileName):
	with open(fileName, 'r') as readFile:
		for classifierStr in readFile:
			classifierDict = json.loads(classifierStr)

			rules = classifierModule.Rules()
			rules.centres = classifierDict['rules']['centres']
			rules.ranges = classifierDict['rules']['ranges']

			classifier = classifierModule.Classifier(classifierDict['birthIteration'], classifierDict['outcome'], rules)
			classifier.matchCount = classifierDict['matchCount']
			classifier.correctCount = classifierDict['correctCount']
			classifier.accuracy = classifierDict['accuracy']
			classifier.fitness = classifierDict['fitness']
			classifier.numerosity = classifierDict['numerosity']
			classifier.lastGAIteration = classifierDict['lastGAIteration']
			classifier.aveMatchSetSize = classifierDict['aveMatchSetSize']

			lcs.population.append(classifier)

main()
