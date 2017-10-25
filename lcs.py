import classifier as classifierModule
import random

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
		self.maxPopSize = 1000
		self.coveringWildcardProbability = 0.3
		self.initialRangeFactor = 0.1		   	# when initialising a rule, set range = abs(initialRangeFactor*centre)
		self.powerParameter = 5					# value based on paper's stated typical value
		self.deletionThreshold = 20
		self.deletionFitnessScale = 0.1
		self.featurePrecision = 0.00000000001

		# Parameters for GA
		self.GAThreshold = 25				   	# average iterations between GA applications
		self.probabilityCrossover = 0.75
		self.probabilityAlleleMutation = 0.02
		self.probabilityWildcardMutation = 0.2
		self.mutationScale = 0.1

		# Subsumption paramerers
		self.GASubsumption = True
		self.correctSetSubsumption = True
		self.subsumeExpThreshold = 20
		self.subsumeAccuracyThreshold = 0.9
		# Note on subsumeAccuracyThreshold:
		# XCS required prediction error (related to accuracy) to be below a certain threshold. In this
		# implementation (supervised learning) we do not have prediction accuracy. Hence, correct set
		# accuracy is used instead. Standard values for this parameter could only be found for reinforcement
		# learning cases. The starting value of 0.9 was chosen based on the standard values in the
		# literature being 10% of the maximum reward in the reinforcement learning. Hence, 90% accuracy
		# was chosen as the threshold.

	def doMatching(self, instance):
		self.matchSet = []
		unmatchedPopulation = []

		# matchCount = 0
		# move matching classifiers from population to matchSet
		for classifier in self.population:
			if self.doesMatch(classifier.rules, instance.features):
				self.matchSet.append(classifier)
				# matchCount += 1
			else:
				unmatchedPopulation.append(classifier)

		self.population = unmatchedPopulation


	def doesMatch(self, classifierRules, instanceFeatures):
		for i in range(len(classifierRules.centres)):
			# false if not wildcard and outside range from centre
			if(classifierRules.centres[i] != "#"):
				if(instanceFeatures[i] < classifierRules.getLowerBound(i) or
						   instanceFeatures[i] > classifierRules.getUpperBound(i)):
					# print('l:',classifierRules.getLowerBound(i),'F:',instanceFeatures[i],'u:',classifierRules.getUpperBound(i))
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

		self.matchSet = incorrectSet  # matchSet currently is only consisting of incorrectSet, but the left over correct set will be added back later


	# using currIter to give the classifier a number ID????
	def doCovering(self, instance):
		outcome = instance.outcome
		rules = classifierModule.Rules()
		for feat in instance.features:
			if random.randrange(0,100)/100 < self.coveringWildcardProbability:
				rules.centres.append('#')
				rules.ranges.append('#')
			else:
				rules.centres.append(feat)
				rules.ranges.append(abs(feat) * self.initialRangeFactor)
		classifier = (classifierModule.Classifier(self.currIter, outcome, rules))
		self.correctSet.append(classifier)


	def updateParameters(self):
		matchSetSize = len(self.correctSet) + len(self.matchSet)
		for classifier in self.correctSet:
			classifier.matchCount   += 1
			classifier.correctCount += 1
			classifier.accuracy = classifier.correctCount / classifier.matchCount
			classifier.aveMatchSetSize = (classifier.aveMatchSetSize * (classifier.matchCount - 1) + matchSetSize) / (
			classifier.matchCount)
			classifier.fitness = pow(classifier.accuracy,self.powerParameter)

		for classifier in self.matchSet:
			classifier.matchCount += 1
			classifier.accuracy = classifier.correctCount / classifier.matchCount
			classifier.aveMatchSetSize = (classifier.aveMatchSetSize * (classifier.matchCount - 1) + matchSetSize) / (
			classifier.matchCount)
			classifier.fitness = pow(classifier.accuracy, self.powerParameter)

			#fitness from "A Scalable Evolutionary Learning Classifier System for Knowledge Discovery in Stream Data Mining"

	# Move classifiers from the correct set back to the population
	def consolidateClassifiers(self):
		for classifier in self.correctSet:
			self.population.append(classifier)
		self.correctSet = []

		for classifier in self.matchSet:
			self.population.append(classifier)
		self.matchSet = []


	def doDeletion(self):
		voteSum = 0
		popFitnessSum = sum([x.fitness for x in self.population])
		popAveFitness = popFitnessSum / len(self.population)

		for classifier in self.population:
			voteSum = voteSum + self.deletionVote(classifier, popAveFitness)
		choicePoint = random.uniform(0,1) * voteSum

		voteSum = 0
		for i in range(len(self.population)):
			voteSum = voteSum + self.deletionVote(self.population[i], popAveFitness)
			if voteSum >= choicePoint:
				if self.population[i].numerosity > 1:
					self.population[i].numerosity -= 1
				else:
					self.population.pop(i)
				break

	def deletionVote(self, classifier, popAveFitness):
		vote = classifier.aveMatchSetSize * classifier.numerosity

		if classifier.matchCount > self.deletionThreshold \
			and classifier.fitness/classifier.numerosity < self.deletionFitnessScale * popAveFitness:
			if classifier.fitness == 0:
				# to fix divide by 0 error
				vote = vote * popAveFitness / self.featurePrecision
			else:
				vote = vote * popAveFitness / (classifier.fitness/classifier.numerosity)

		return vote

	# only for testing and monitoring
	def getAveClassifierAcc(self):
		return sum([classifier.accuracy for classifier in self.population]) / len(self.population)


	def classifyInstance(self):
		pass
	#	 used for testing


#########################################################################

	# TASK: description
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

		# TASK: check average time since last GA iteration, run if above threshold

		# Update last GA iteration for all classifiers in correct set
		self.updateLastGAIterations()

		# Select parents
		###########################################
		# Kevin: Removed 's' from function call to match function declaration
		###########################################
		parent1 = self.selectParent()
		parent2 = self.selectParent()

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
			if fitnessSum >= choicePoint:  # return classifier at selected position on wheel
				return classifier
			#####################################
			# KEVIN:  changed > to >= to account for edge cases
			#####################################


	# doCrossover
	# Called by GA
	# Applies two-point crossover to two children classifiers and returns the modified children.
	# Note: crossover is limited to occur only between components of the rule, not between 
	# alleles. That is, the crossover point will never be between a centre and its corresponding
	# range value. The crossover point will never split a (centre, range) pair.
	#
	# ENHACEMENT-: add option for single point crossover
	# TASK: averaging of child parameters, weighted average based on the amount crossed over This
	# would be an improvement compared to Butz & Wilson
	def doCrossover(self, childA, childB):
		n_conditions = len(childA.rules.centres)	# number of components in a classifier rule
		################################
		x = random.random()*n_conditions			# continuous implementation has two alleles per component
		y = random.random()*n_conditions
		# KEVIN: Removed the 2x scalar. It was causing out of bounds errors
		################################
		if x > y:
			# x is the smaller value
			x, y = y, x
		
		i = 0
		while i < y:
			if x <= i and y > i:
				childA.rules.centres[i], childB.rules.centres[i] = childB.rules.centres[i], childA.rules.centres[i]
				childA.rules.ranges[i], childB.rules.ranges[i] = childB.rules.ranges[i], childA.rules.ranges[i]
			i += 1
		
		return (childA, childB)
	

	# doMutation
	# Called by GA
	# Apply mutation to a single classifier. Mutation considers each allele (all centres and
	# ranges) independently and randomly selects some for mutation based on a set probability.
	#
	# Mutation cases:
	# 1. Non-wildcard to non-wildcard: as per on Sowden (2007) and Stone & Bull (2003), this
	#	 type of mutation is applied by adding an increment in the range (-m,m) to any allele
	#	 selected for such mutation.
	# 2. Non-wildcard to wildcard: performed with probability probabilityWildcardMutation
	# 3. Wildcard to non-wildcard: similar to Stone & Bull (2003), this is performed by 
	#	 initialising the rule (centre and range) based on the current environment instance.
	#	 The centre value is calculated by multilying the instance value by a random factor
	#	 close to 1. range is calculated as initialRangeFactor times the centre value.
	def doMutation(self, child, instanceFeatures):
		# Mutation of rule centre values
		for i in range(0,len(child.rules.centres)):
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
				###############################
				# KEVIN: Should a range be added on here? (use abs() so range is always positive)
				###############################

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
	# Called by GA (in GA subsumption)
	# Checks whether a given classifier (the subsumer) subsumes another (the subsumee). The
	# requirements for this are that: (1) they share the same action, (2) the sumsumer is 
	# sufficiently experiences and accurate, and (3) the subsumer is more general.
	def doesSubsume(self, subsumer, subsumee):
		if subsumer.outcome == subsumee.outcome:
			if self.couldSubsume(subsumer):
				##########################################
				if self.isMoreGeneral(subsumer, subsumee):
				# KEVIN: added self. to call self.isMoreGeneral
				##########################################
					return True

		return False


	# couldSubsume
	# Called by doesSubsume and doCorrectSetSubsumption
	# Checks if the potential subsumer is sufficiently experienced (large enough correctCount)
	# and accurate to be considered for subsumption.
	def couldSubsume(self, classifier):
		if classifier.correctCount > self.subsumeExpThreshold:
			if classifier.accuracy > self.subsumeAccuracyThreshold:
				return True
		return False


	# isMoreGeneral
	# Called by doesSubsume and doCorrectSetSubsumption
	# Checks that the proposed subsumer is more general than the proposed subsumee at each predicate
			# (aka rule element or condition). To be more general at a given predicate, the subsumer must
	# either have a wildcard at that point or be such that its upper bound exceeds that of the
	# subsumee while its lower bound is also lower than that of the subsumee. That is, it must at
	# least the same range of values as the subsumee.
	#
	# ENHANCEMENT: consider adding some tolerance to this comparison. That is, if the bounds of the
	# subsumer don't quite cover the subsumee, but come very close, it may be acceptable to say
	# that is it more general. MOTIVATION: I suspect that it is unlikely for any classifier to be
	# more general given the number of predicated/rule elements. Hence, we should allow some
	# tolerance for 'not quite more general'.
	def isMoreGeneral(self, subsumer, subsumee):
		for i in range(0, len(subsumer.rules)):
			# if subsumee has a wildcard that subsumer doesnt, then subsumer is not more general
			if subsumee.rules.centre[i] == '#':
				if subsumer.rules.centre[i] == '#':
					return  True
				else:
					return False
			# no wildcards should get to here
			# if either bound of the subsumee is  closer to the subsumer's centre and the subsumee has a larger range
			elif (subsumer.getLowerBound(i) > subsumee.getLowerBound(i) or subsumer.getUpperBound(i) < subsumee.getUpperBound(i)) \
							and subsumer.ranges[i] < subsumee.ranges[i]:
				return False
		return True


	# doCorrectSetSubsumption
	# Called by main (before GA)
	# Searches the correct set for the most general classifier that is sufficiently experienced
	# and accurate to be used for subsumption. All other classifiers in the correct set are then
	# compared to this for potential subsumption. Valid subsumees are subsumed with their
	# numerosity added to that of the most general classifier. Subsumed classifiers are deleted
	# from the correct set.
	def doCorrectSetSubsumption(self):
		# Initialise most general classifier vraiable
		initRules = classifierModule.Rules()
		mostGeneralClassifier = classifierModule.Classifier(self.currIter, 0, initRules)
		tmpCorrectSet = []

		# Search for most general classifier in the correct set
		for classifier in self.correctSet:
			if self.couldSubsume(classifier):
				####################################
				if len(mostGeneralClassifier.rules.centres) == 0:
					mostGeneralClassifier = classifier
				# KEVIN: Made this into separate conditional so dummy classifier isn't added to correct set
				####################################
				elif (classifier.wildcardCount > mostGeneralClassifier.wildcardCount or
						(classifier.wildcardCount == mostGeneralClassifier.wildcardCount and
						classifier.sumRange > mostGeneralClassifier.sumRange)):
					# Move old most general classifier to tmp set and update it
					tmpCorrectSet.append(mostGeneralClassifier)
					mostGeneralClassifier = classifier
				else:
					# If not most general, add to tmp set
					tmpCorrectSet.append(classifier)

		# Perform subsumption if a suitable mostGeneralClassifier was found
		if len(mostGeneralClassifier.rules.centres) != 0:
			####################################
			for classifier in tmpCorrectSet:
			# KEVIN: tmpCorrectSet wasn't being used as a class element so the "self" reference was removed
				if self.isMoreGeneral(mostGeneralClassifier, classifier):
					mostGeneralClassifier.numerosity += classifier.numerosity
				else:
					self.correctSet.append(classifier)
			# KEVIN: Modified to append straight to correctSet if not subsumed
			####################################
			# Return mostGeneralClassifier to correct set if it isnt the dummy one
			self.correctSet.append(mostGeneralClassifier)
