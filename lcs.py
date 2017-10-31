import classifier as classifierModule
import random, copy, math

class LCS:
    # '#' indicates wildcard
    # correct count is used as the analog for experience (in classifier parameters)
    def __init__(self, parameterList , log):
        """"
        :parameterList :
        """
        # Sets
        self.population = []
        self.matchSet = []
        self.correctSet = []
        self.log = log
        self.parameterList = parameterList

        # General parameters
        self.maxNumberOfIteration =         parameterList[0]
        self.currIter =                     0
        self.maxPopSize =                   parameterList[1]
        self.coveringWildcardProbability =  parameterList[2]
        self.initialRangeFactor =           parameterList[3]  # when initialising a rule, set range = abs(initialRangeFactor*centre)
        self.powerParameter =               parameterList[4]  # value based on paper's stated typical value
        self.deletionThreshold =            parameterList[5]
        self.deletionFitnessScale =         parameterList[6]
        self.deletionScale =                2
        self.featurePrecision =             0.00000000001  #

        # Parameters for GA
        self.GAThreshold =                  parameterList[7]  # average iterations between GA applications
        self.probabilityCrossover =         parameterList[8]
        self.probabilityAlleleMutation =    parameterList[9]
        self.probabilityWildcardMutation =  parameterList[10]
        self.mutationScale =                parameterList[11]

        # Subsumption parameters
        self.GASubsumption = True
        self.doCorrectSetSubsumption = True
        self.subsumptionTolerance = 0.5
        self.subsumeExpThreshold =          parameterList[12]
        self.subsumeAccuracyThreshold =     parameterList[13]


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
        for i in range(len(classifierRules.centres)):
            # false if not wildcard and outside range from centre
            if(classifierRules.centres[i] != "#"):
                if(instanceFeatures[i] < classifierRules.getLowerBound(i,0) or
                           instanceFeatures[i] > classifierRules.getUpperBound(i,0)):
                    # print('l:',classifierRules.getLowerBound(i,0),'F:',instanceFeatures[i],'u:',classifierRules.getUpperBound(i,0))
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

        # when a classifier is generated from covering, set its lastGAiteration as teh current iteration
        classifier.lastGAIteration = self.currIter

        self.correctSet.append(classifier)


    def updateParameters(self, matchSetSize):
        for classifier in self.correctSet:
            classifier.matchCount   += 1
            classifier.correctCount += 1
            classifier.accuracy = classifier.correctCount / classifier.matchCount
            classifier.aveMatchSetSize = (classifier.aveMatchSetSize * (classifier.matchCount - 1) + matchSetSize) / (
            classifier.matchCount)
            classifier.fitness = pow(classifier.accuracy, self.powerParameter)

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

    #make sure testing is deleting unfit classifiers
    def deletionVote(self, classifier, popAveFitness):
        vote = classifier.aveMatchSetSize * classifier.numerosity
        if classifier.matchCount > self.deletionThreshold*self.scaleDeletionThreshold(self.currIter-classifier.birthIteration) \
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

    # classify an given instance using the classifiers in the current population
    # pass in an instance that is to be classfied
    # return a class that has the highest votes from all the classifiers in the population
    def classifyInstance(self, instance):
        classDict = {}

        for classifier in self.population:
            if self.doesMatch(classifier.rules, instance.features):
                vote = classifier.fitness * classifier.numerosity
                if classifier.outcome in list(classDict.keys()) :
                    classDict[classifier.outcome] += vote
                else :
                    classDict[classifier.outcome] = vote
        # if the length of class dictionary is 0 after trying to match it with every classifer in the population, then this instance
        # is not covered by the LCS system. therefore return -1
        if len(classDict) == 0:
            return -1
        else:
            value = list(classDict.values())
            keys  = list(classDict.keys())
            # print(classDict)
            return keys[value.index(max(value))]
    #	 used for testing

    def scaleDeletionThreshold(self, age):
        ageThresh = 200
        return (math.pi/2 - math.atan((age-ageThresh)/20))/3.05


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
        # parent1 = self.selectParent()
        # parent2 = self.selectParent()

        # using selectParent_nonrepeat()
        [parent1, parent2] = self.selectParents_nonrepreat()

        # Initialise children
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)

        child1.numerosity = 1
        child2.numerosity = 1
        child1.birthIteration = self.currIter
        child2.birthIteration = self.currIter

        # Apply crossover
        if random.random() < self.probabilityCrossover:
            (child1, child2) = self.doCrossover(child1, child2)

            # if crossover is done on those two children,
            # then their classifier parameter will be set as the average of their parents
            # as the fitness is calculated as (correct/match)^power
            # therefore children's matchCount and correcctCount are set to be the sum of both parents'
            child1.setFitness(parent1, parent2)
            child2.setFitness(parent1, parent2)

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
                #print("... child 1 added to population")
                self.correctSet.append(child1)

            # Second child
            if self.doesSubsume(parent1, child2):
                parent1.numerosity += 1
            elif self.doesSubsume(parent2, child2):
                parent2.numerosity += 1
            else:
                #print("... child 2 added to population")
                self.correctSet.append(child2)

    # getAverageTimePeriod()
    #calculate and return the average time period since the last GA for the correctSet
    def getAverageTimePeriod(self):
        """"
        :return avgTs average time period since last GA for the whole correctSet
        """
        ts = 0
        numerositySum = 0
        for classifier in self.correctSet:
            ts += (self.currIter - classifier.lastGAIteration) * classifier.numerosity
            numerositySum += classifier.numerosity
    
        avgTs = ts/numerositySum
        #print("Average Time Period: "+str(avgTs))
        return avgTs

    # updateLastGAIterations
    # Called by GA
    # Loops through correct set and sets lastGAIteration of all elements to currIter
    def updateLastGAIterations(self):
        for classifier in self.correctSet:
            classifier.lastGAIteration = self.currIter

    # selectParents
    # Called by GA
    # Select two parents classifiers for GA from correct set using Roulette-Wheel Selection.
    # With Roulette-Wheel Selection, the probability of selecting a given classifier in the
    # correct set is proportional to its fitness.
    # It is made sure that the parents selected are not identical
    def selectParents_nonrepreat(self):
        """"
        :return [ parent 1, parent 2]  a list containing the two parents selected from the correct set
        """
        fitnessSum = 0
        for classifier in self.correctSet:
            fitnessSum += classifier.fitness

        parentsList = []

        # first Roulette-Wheel Selection
        choicePoint = random.random() * fitnessSum  # select position on wheel
        fitnessSum2 = 0
        for classifier in self.correctSet:
            fitnessSum2 += classifier.fitness
            if fitnessSum2 >= choicePoint:  # return classifier at selected position on wheel
                parentsList.append(classifier)
                # temporarily remove the selected classifier in the set so that this classifier will not be selected
                # in the next draw
                self.correctSet.remove(classifier)
                # quit the for loop once a classifier has been drawn
                break

        # second Roulette-Wheel Selection
        # now the fitnessSum needs to minus the fitness of the classifier that was just selected
        fitnessSum = fitnessSum - parentsList[0].fitness
        choicePoint = random.random() * fitnessSum  # select position on wheel
        fitnessSum2 = 0
        for classifier in self.correctSet:
            fitnessSum2 += classifier.fitness
            if fitnessSum2 >= choicePoint:  # return classifier at selected position on wheel
                parentsList.append(classifier)
                # quit the for loop once a classifier has been drawn
                break

        if len(parentsList) != 2:
            msg = str(self.correctSet) + "\n"
            self.log.logError(msg)
            parentsList.append(parentsList[0])

        # now add the temporarily removed classifier back to the correctSet
        self.correctSet.append(parentsList[0])

        return parentsList


    # selectParents
    # Called by GA
    # Select a parents classifiers for GA from correct set using Roulette-Wheel Selection.
    # With Roulette-Wheel Selection, the probability of selecting a given classifier in the
    # correct set is proportional to its fitness.
    # def selectParent(self):
    #     fitnessSum = 0
    #     for classifier in self.correctSet:
    #         fitnessSum += classifier.fitness
    #
    #     choicePoint = random.random()*fitnessSum  # select position on wheel
    #     fitnessSum = 0
    #     for classifier in self.correctSet:
    #         fitnessSum += classifier.fitness
    #         if fitnessSum >= choicePoint:  # return classifier at selected position on wheel
    #             return classifier


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
        x = random.random()*n_conditions			# continuous implementation has two alleles per component
        y = random.random()*n_conditions
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
                    # TASK: check range does not go negative

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
    # requirements for this are that: (1) they share the same action, (2) the subsumer is
    # sufficiently experiences and accurate, and (3) the subsumer is more general.
    def doesSubsume(self, subsumer, subsumee):
        if subsumer.outcome == subsumee.outcome:
            if self.couldSubsume(subsumer):
                if self.isMoreGeneral(subsumer, subsumee):
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
        for i in range(0, len(subsumer.rules.centres)):
            # If the subsumee has a wildcard that the subsumer does not, return False
            if subsumee.rules.centres[i] == '#' and subsumer.rules.centres[i] == '#':
                continue
                #return False
            # If neither has a wildcard, check upper and lower bounds
            elif subsumer.rules.getLowerBound(i, self.subsumptionTolerance) > subsumee.rules.getLowerBound(i, 0) or \
                 subsumer.rules.getUpperBound(i, self.subsumptionTolerance) < subsumee.rules.getUpperBound(i, 0) :
                return False

        return True


    # correctSetSubsumption
    # Called by main (before GA)
    # Searches the correct set for the most general classifier that is sufficiently experienced
    # and accurate to be used for subsumption. All other classifiers in the correct set are then
    # compared to this for potential subsumption. Valid subsumees are subsumed with their
    # numerosity added to that of the most general classifier. Subsumed classifiers are deleted
    # from the correct set.
    def correctSetSubsumption(self):
        # Initialise most general classifier variable
        initRules = classifierModule.Rules()
        mostGeneralClassifier = classifierModule.Classifier(self.currIter, 0, initRules)
        tmpCorrectSet = []

        # Search for most general classifier in the correct set
        for classifier in self.correctSet:
            if self.couldSubsume(classifier):
                # If mostGeneralClassifier is not assigned, assign it a classifier that can subsume
                if len(mostGeneralClassifier.rules.centres) == 0:
                    mostGeneralClassifier = classifier
                # If current classifier is more general, overwrite mostGeneralClassifier
                # and move the old one to the tmpCorrectSet
                # In this case, "more general" is interpreted as having more wildcards or an equal number of wildcards
                # but a larger total range.
                elif (classifier.wildcardCount() > mostGeneralClassifier.wildcardCount() or
                        (classifier.wildcardCount() == mostGeneralClassifier.wildcardCount() and
                        classifier.sumRange() > mostGeneralClassifier.sumRange())):
                    tmpCorrectSet.append(mostGeneralClassifier)	# return old version to tmp set
                    mostGeneralClassifier = classifier			# update new version
                # If current classifier in not most general, add it to tmp set
                else:
                    tmpCorrectSet.append(classifier)
            # If current classifier in not most general, add it to tmp set
            # Note that this is done outside the if (couldSubsume) condition as well as inside it
            # since classifiers need to be appended to tmpCorrectSet in either case
            else:
                tmpCorrectSet.append(classifier)

        # Perform subsumption if a suitable mostGeneralClassifier was found
        if len(mostGeneralClassifier.rules.centres) != 0:

            print("... doing correct set subsumption")

            self.correctSet = []   # reset correct set
            for classifier in tmpCorrectSet:
                if self.isMoreGeneral(mostGeneralClassifier, classifier):
                    print("... subsumed a classifier")
                    mostGeneralClassifier.numerosity += classifier.numerosity
                else:
                    self.correctSet.append(classifier)
            # Return mostGeneralClassifier to correct set if it isn't the dummy one
            self.correctSet.append(mostGeneralClassifier)
