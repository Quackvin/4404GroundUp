import lcs as lcsModule
import classifier as classifierModule
import environment
import json

def main(loadPop):
	env = environment.Environment('dataFull.txt')
	lcs = lcsModule.LCS()
	if loadPop:
		loadPopulation(lcs)
	run(lcs, env, False)

def run(lcs, env, doTest):
	if doTest:
		print('**********Testing**********')
	else:
		print('**********Training*********')

	for instance in env.instances:
		print('iteration: ', lcs.currIter, end='\r', flush=True)
		lcs.currIter += 1

		matchSetSize = lcs.doMatching(instance)
		'''	---NOT IMPLEMENTED YET---'''
		if(doTest):
			lcs.formPrediction()
			'''-------------------'''
		else:
			lcs.doCorrectSet(instance)
			if len(lcs.correctSet) == 0:
				lcs.doCovering(instance)
			lcs.updateParameters(matchSetSize)
			if len(lcs.correctSet) > 3: 				# needs more conditions
				lcs.GA(instance.features)			 	# includes GA subsumption
			lcs.doCorrectSetSubsumption()
			lcs.consolidateClassifiers()
			if len(lcs.population) > lcs.maxPopSize:
				lcs.doDeletion()

			# print(lcs.getAveClassifierAcc())

		'''---NOT IMPLEMENTED YET---'''
		endcondition = False
		'''-------------------------'''
		if endcondition:
			break

	savePopulation(lcs.population)
	print('**********END**********')

def savePopulation(population):
	print('\nSaving')
	with open('classifierPopulation.json', 'w') as writeFile:
		for classifier in population:
			classifierDict = classifier.__dict__
			classifierDict['rules'] = classifierDict['rules'].__dict__
			classifierString = json.dumps(classifierDict) + '\n'
			writeFile.write(classifierString)

def loadPopulation(lcs):
	with open('classifierPopulation.json', 'r') as readFile:
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

main(False)