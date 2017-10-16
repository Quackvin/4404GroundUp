import classifier

class LCS:
	def __init__(self, maxPopSize):
		# put all LCS parameters here
		self.population = []
		self.currIter = 0
		self.matchSet = []
		self.correctSet = []
		self.maxPopSize = maxPopSize

	def doMatching(self, instance, doTest):
		classifierIndex = 0
		for classifer in self.population:
			if(self.doesMatch(classifier.rules, instance.features)):
				self.correctSet.append(self.population.pop(classifierIndex))
			classifierIndex += 1

		pass
	# if doTest, ignore training function
	# 	initialise empty match set
	# 	compare each rule to instance
	# 	add matches to match set
	# 	do covering if not enough matches

	def doesMatch(self, classifierRules, instanceFeatures):
		pass

	def doCovering(self):

		self.population.append(classifier.Classifier(self.currIter, classifcation))
		pass

	def doCorrectSet(self):
		pass
	# pop them out of match set
	# generate correct and incorrect sets
	# used for training

	def classifyInstance(self):
		pass
	# 	used for testing

	def updateParameters(self):
		pass

	def doDeletion(self):
		pass
	# general deletion for if population is too big

#########################################################################

	def GA(self):
		self.updateLastGAIterations()
		parents = self.selectParents()
		self.initialiseChildParameters()
		children = self.doCrossover(parents)
		self.doMutation()
		self.correctSet.append(children[0])
		self.correctSet.append(children[1])
		self.doSubsumption()
		pass
	# creates 2 new classifiers
	# applies subsuption to correct set after adding children into it
	# put matchset and correctset back into population

	def updateLastGAIterations(self):
		pass
		# loops through correct set and sets lastGAIter in all elements of correct set to currIter

	def selectParents(self):
		pass
	# goes through correct set and uses roulette wheel selection to choose two parents and returns them

	def initialiseChildParameters(self):
		pass
	# rules in the paper (fitness and accuray from parents)

	def doCrossover(self, parents):
		pass
	# returns children
	# rules in paper

	def doMutation(self):
		pass
	# rules in paper
	# do probabilities here

	def doSubsumption(self):
		pass
	# applies to correct set