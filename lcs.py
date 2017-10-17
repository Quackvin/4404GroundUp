import classifier, random

class LCS:
	# '#' indicates wildcard
	def __init__(self):
		# put all LCS parameters here
		self.population = []	# list of Classifier objects
		self.matchSet = []
		self.correctSet = []

		self.maxPopSize = 100
		self.coveringWildcardProbability = 0.3

		self.currIter = 0


	def doMatching(self, instance):
		self.matchSet = []
		unmatchedPopulation = []

		matchCount = 0
		# move matching classifiers from population to matchSet
		for classifier in self.population:
			if self.doesMatch(classifier.rules, instance.features):
				self.matchSet.append(classifier)
				matchCount += 1
			else:
				unmatchedPopulation.append(classifier)

		self.population = unmatchedPopulation
		return matchCount


	def doesMatch(self, classifierRules, instanceFeatures):
		for i in range(len(classifierRules)):
			# false if not wildcard and outside range from centre
			if instanceFeatures[i] != '#' and \
					(	instanceFeatures[i] < classifierRules.getLowerBound(i) or
						instanceFeatures[i] > classifierRules.getUpperBound(i)	):
				return False
		return True


	def doCorrectSet(self, instance):
		self.correctSet = []
		incorrectSet = []

		# move correct matches from matchSet to correctSet
		for classifier in self.matchSet:
			if classifier.outcome == instance.outcome:
				self.correctSet.append(classifier)
			else:
				incorrectSet.append(classifier)

		self.matchSet = incorrectSet


	def doCovering(self, instance):
		outcome = instance.outcome
		rules = classifier.Rules()
		for feat in instance.features:
			# add centres
			if random.randrange(0,100)/100 < self.coveringWildcardProbability:
				rules.centres.append('#')
			else:
				rules.centres.append(feat)
			# add ranges
			if random.randrange(0,100)/100 < self.coveringWildcardProbability:
				rules.ranges.append('#')
			else:
				rules.ranges.append(feat/10)
		''' 	add a range too. Need to decide on range for range values. Currently 10% of centre		'''

		self.correctSet.append(classifier.Classifier(self.currIter, outcome, rules))


	def updateParameters(self, matchSetSize):
		for classifier in self.correctSet:
			classifier.matchCount += 1
			classifier.correctCount += 1
			classifier.accuracy = classifier.correctCount / classifier.matchCount
			classifier.aveMatchSetSize = (classifier.aveMatchSetSize * (classifier.matchCount - 1) + matchSetSize) / (
			classifier.matchCount)
			"""	fitness """
		for classifier in self.matchSet:
			classifier.matchCount += 1
			classifier.accuracy = classifier.correctCount / classifier.matchCount
			classifier.aveMatchSetSize = (classifier.aveMatchSetSize * (classifier.matchCount - 1) + matchSetSize) / (
			classifier.matchCount)
			"""	fitness """


	def consolidateClassifiers(self):
		for classifier in self.correctSet:
			self.population.append(classifier)
		self.correctSet = []

		for classifier in self.matchSet:
			self.population.append(classifier)
		self.matchSet = []


	def doDeletion(self):
		pass
	# general deletion for if population is too big


	def classifyInstance(self):
		pass
	# 	used for testing


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