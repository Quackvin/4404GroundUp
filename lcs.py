import classifier, random

class LCS:
	# '#' indicates wildcard
	# correct count is used as the analog for experience (in classifier parameters)
	def __init__(self):
		# Sets
		self.population = []
		self.matchSet = []
		self.correctSet = []

		# General parameters
		self.currIter = 0
		self.maxPopSize = 100
		self.coveringWildcardProbability = 0.3
		self.initialRangeFactor = 0.1			# when initialising a rule, set range = initialRangeFactor*centre
		

		# Parameters for GA
		self.GAThreshold = 25					# average iterations between GA applications
		self.probabilityCrossover = 0.75
		self.probabilityAlleleMutation = 0.02
		self.probabilityWildcardMutation = 0.2
		self.mutationScale = 0.1

		# Subsumption paramerers
		self.GASubsumption = True
		self.correctSetSubsumption = True
		self.subsumeExpThreshold = 20
		self.subsumeAccuracyThreshold = 0.9
		# XCS required prediction error (related to accuracy) to be below a certain threshold. In this
		# implementation (supervised learning) we do not have prediction accuracy. Hence, correct set
		# accuracy is used instead. Standard values for this parameter could only be found for reinforcement
		# learning cases. The starting value of 0.9 was chosen based on the standard values in the
		# literature being 10% of the maximum reward in the reinforcement learning. Hence, 90% accuracy
		# was chosen as the threshold.


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

			################################################################################
			# AARON: I think this is a bug: instanceFeatures refers to the instance from the
			# environment, which will never be a whilecard. The check needs to be that the
			# classifier rule is not a wildcard
			################################################################################

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
			
			###########################################################################################
			# AARON: I think there may be an issue. Does it make sense for the centre to hae a wildcard
			# but not the range, or vice versa? I.e. you can't do matching if only one is a wildcard.
			# So I think you should either set both to wildcards, or both to definite values.
			###########################################################################################

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
				# AARON: I have defined self.initialRangeFactor = 0.1 and used this for a similar task in setRuleToRandom (within doMutation)

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

	# Move classifiers from the correct set back to the population
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

	# TASK: description
	# TASK: GA called in every iteration, work out probabilities in GA function (i.e. whether to run)
	#
	# creates 2 new classifiers
	# applies subsuption to correct set after adding children into it
	# put matchset and correctset back into population

	# instanceFeatures is required for mutation back from a wildcard
	#
	# GA
	# Called by main
	#
	def GA(self, instanceFeatures):

		# TASK: check average time since last GA iteration, if too high, run GA. Else, just run doSubsumption

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

		# Apply mutation
		self.doMutation(child1, instanceFeatures)
		self.doMutation(child2, instanceFeatures)

		# Apply GA subsumption and add non-subsumed children to correct set
		if self.GASubsumption:
			# First child
			if self.doesSubsume(parent1, child1):
				parent1.numerosity += 1
			elif self.doesSubsume(parent2, child1):
				parent2.numerosity += 1
			else:
				self.correctSet.append(child1)
			
			# Second child
			if self.doesSubsume(parent1, child2):
				parent1.numerosity += 1
			elif self.doesSubsume(parent2, child2):
				parent2.numerosity += 1
			else:
				self.correctSet.append(child2)

		# Apply correct set subsumption
		if self.correctSetSubsumption:
			self.doCorrectSetSubsumption()
	

	# updateLastGAIterations
	# Called by GA
	# Loops through correct set and sets lastGAIteration of all elements to currIter
	def updateLastGAIterations(self):
		for classifier in self.correctSet:
			classifier.lastGAIteration = self.currIter


	# selectParents
	# Called by GA
	# Select a parents classifiers for GA from correct set using Roulette-Wheel Selection.
	# With Roulette-Wheel Selection, the probability of selecting a given classifier in the
	# correct set is proportional to its fitness.
	def selectParent(self):
		fitnessSum = 0
		for classifier in self.correctSet:
			fitnessSum += classifier.fitness

		choicePoint = random.random()*fitnessSum  # select position on wheel
		fitnessSum = 0
		for classifier in self.correctSet:
			fitnessSum += classifier.fitness
			if fitnessSum > choicePoint:  # return classifier at selected position on wheel
				return classifier


	# doCrossover
	# Called by GA
	# Applies two-point crossover to two children classifiers and returns the modified children.
	# Note: crossover is limited to occur only between components of the rule, not between 
	# alleles. That is, the crossover point will never be between a centre and its corresponding
	# range value. The crossover point will never split a (centre, range) pair.
	#
	# TASK: add option for single point crossover (e.g. extra argument or internal parameter)
	# TASK: add averaging of parameters. Use a weighted average based on the amount crossed over (an improvement compared to Butz & Wilson)
	def doCrossover(self, childA, childB):
		n_conditions = len(childA.rules)	# number of components in a classifier rule
		x = random.random()*2*n_conditions			# continuous implementation has two alleles per component
		y = random.random()*2*n_conditions
		if x > y:
			x, y = y, x
		
		i = 0
		while i < y:
			if x <= i and y > i:
				childA.rules.centres[i], childB.rules.centres[i] = childB.rules.centres[i], childA.rules.centres[i]
				childA.rules.rangse[i], childB.rules.ranges[i] = childB.rules.ranges[i], childA.rules.ranges[i]
			i += 1
		
		return (childA, childB)
	

	# doMutation
	# Called by GA
	# Apply mutation to a single classifier. Mutation considers each allele (all centres and
	# ranges) independently and randomly selects some for mutation based on a set probability.
	#
	# Mutation cases:
	# 1. Non-wildcard to non-wildcard: as per on Sowden (2007) and Stone & Bull (2003), this
	#    type of mutation is applied by adding an increment in the range (-m,m) to any allele
	#    selected for such mutation.
	# 2. Non-wildcard to wildcard: performed with probability probabilityWildcardMutation
	# 3. Wildcard to non-wildcard: similar to Stone & Bull (2003), this is performed by 
	#    initialising the rule (centre and range) based on the current environment instance.
	#    The centre value is calculated by multilying the instance value by a random factor
	#    close to 1. range is calculated as initialRangeFactor times the centre value.
	def doMutation(self, child, instanceFeatures):
		# Mutation of rule centre values
		for i in range(0,len(child.rules)):
			# Mutate allele stochastically
			if random.random() < self.probabilityAlleleMutation:
				# Wildcard to non-wildcard
				if child.rules.centres[i] == '#':
					self.setRuleToRandom(child,instanceFeatures,i)
				# Non-wildcard to wildcard
				elif random.random() < self.probabilityWildcardMutation:
					child.rules.centres[i] = '#'
					child.rules.ranges[i] = '#'
				# Non-wildcard to non-wildcard
				else:
					child.rules.centres[i] += self.mutationScale * random.uniform(-1,1)

		# Mutation of rule range values
		for i in range(0,len(child.rules.ranges)):
			# Mutate allele stochastically
			if random.random() < self.probabilityAlleleMutation:
				# Wildcard to non-wildcard
				if child.rules.ranges[i] == '#':
					self.setRuleToRandom(child,instanceFeatures,i)
				# Non-wildcard to wildcard
				elif random.random() < self.probabilityWildcardMutation:
					child.rules.centres[i] = '#'
					child.rules.ranges[i] = '#'
				# Non-wildcard to non-wildcard
				else:
					child.rules.ranges[i] += self.mutationScale * random.uniform(-1,1)


	# setRuleToRandom
	# Called by doMutation
	# Initialises a rule (aka predicate or condition) based on the current value in the instance
	# from the environment. rules.centre is initialised to the value from the environment instance
	# multiplied by a random factor equal to mutationScale times a random number in (-1,1). 
	# rules.range is initialised to initialRangeFactor times the centre value.
	def setRuleToRandom(self, child, instanceFeatures, index):
		child.rules.centres[index] = instanceFeatures[index] * (1 + self.mutationScale * random.uniform(-1,1))
		child.rules.ranges[index] = child.rules.centres[index] * self.initialRangeFactor


	# doesSubsume
	# Called by GA (in GA subsumption) and doCorrectSetSubsumption
	# Checks whether a given classifier (the subsumer) subsumes another (the subsumee). The
	# requirements for this are that: (1) they share the same action, (2) the sumsumer is 
	# sufficiently experiences and accurate, and (3) the subsumer is more general.
	def doesSubsume(self, subsumer, subsumee):
		if subsumer.outcome == subsumee.outcome:
			if self.couldSubsume(subsumer):
				if isMoreGeneral(subsumer, subsumee):
					return True

		return False


	# couldSubsume
	# Called by doesSubsume
	# Checks if the potential subsumer is sufficiently experienced (large enough correctCount)
	# and accurate to be considered for subsumption.
	def couldSubsume(self, classifier):
		if classifier.correctCount > self.subsumeExpThreshold:
			if classifier.accuracy > self.subsumeAccuracyThreshold:
				return True

		return False

	# isMoreGeneral
	# Called by doesSubsume
	# Checks that the proposed subsumer is more general than the proposed subsumee at each predicate
	# (aka rule element or condition). To be more general at a given predicate, the subsumer must either
	# have a wildcard at that point or be such that its upper bound exceeds that of the subsumee while
	# its lower bound is also lower than that of the subsumee. That is, it must at least the same range
	# of values as the subsumee.
	def isMoreGeneral(self, subsumer, subsumee):
		for i in range(0,len(subsumer.rules)):
			if sumsumer.rules.centre[i] != '#':
				if (sumsumer.getLowerBound(i) > sumsumee.getLowerBound(i) or
					sumsumer.getUpperBound(i) < sumsumee.getUpperBound(i)):
					return False
		
		return True

	#TASK: code this function
	#
	# doCorrectSetSubsumption
	# Called by main
	def doCorrectSetSubsumption(self):
		pass
		

	# applies to correct set
	# need more checks for whether a classifier is more general
	# consider having some tolerance, i.e. the subsumee doesn't have to be fully encompassed by the subsumer - partial overlap allowed
	# if we don't do this, I suspect subsumption will be very rare
	