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

		# Parameters for GA
		self.probabilityCrossover = 0.75

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
		# TODO: description
		# creates 2 new classifiers
		# applies subsuption to correct set after adding children into it
		# put matchset and correctset back into population

		# Update last GA iteration for all classifiers in correct set
		self.updateLastGAIterations()

		# Select parents
		parent1 = self.selectParents()
		parent2 = self.selectParents()

		# Initialise children
		child1 = parent1
		child2 = parent2
		child1.numerosity = 1
		child2.numerosity = 1
		child1.birthIteration = self.currIter
		child2.birthIteration = self.currIter
		
		# Apply crossover
		if random.random() < self.probabilityCrossover:
			(child1, child2) = self.doCrossover(child1, child2)

		# TODO
		self.doMutation()
		self.correctSet.append(children[0])
		self.correctSet.append(children[1])
		#self.doSubsumption()
		pass
	

	def updateLastGAIterations(self):
		# Called by GA
		# Loops through correct set and sets lastGAIteration of all elements to currIter
		for classifier in self.correctSet:
			classifier.lastGAIteration = self.currIter

	def selectParent(self):
		# Select a parents classifier for GA from correct set using Roulette-Wheel Selection
		# With Roulette-Wheel Selection, the probability of selecting a given classifier in the
		# correct set is proportional to its fitness.
		fitnessSum = 0
		for classifier in self.correctSet:
			fitnessSum += classifier.fitness

		choicePoint = random.random()*fitnessSum	# select position on wheel
		fitnessSum = 0
		for classifier in self.correctSet:
			fitnessSum += classifier.fitness
			if fitnessSum > choicePoint: 	# return classifier at selected position on wheel
				return classifier

	def doCrossover(self, childA, childB):
		# Applies crossover to two children classifiers and returns the modifier children
		# Uses two point crossover
		# TODO: include option for single point crossover (third argument or based on an internal parameter)
		pass

	def doMutation(self):
		pass
	# rules in paper
	# do probabilities here

	def doSubsumption(self):
		pass
	# applies to correct set