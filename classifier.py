class Classifier:
    def __init__(self, currIter, outcome, rules):
        self.matchCount = 0
        self.correctCount = 0
        self.accuracy = 0
        self.fitness = 0
        self.numerosity = 1
        self.lastGAIteration = 0
        self.birthIteration = currIter
        self.aveMatchSetSize = 0

        self.rules = rules
        self.outcome = outcome

    # Counts the number of wildcard elements (precepts) in the classifier rules
    def wildcardCount(self):
        count = 0
        for i in range(0, len(self.rules.centres)):
            if self.rules.centres[i] == '#':
                count += 1
        
        return count

    # Calculated the sum of all ranges in the classifier rules that are not wildcards
    def sumRange(self):
        sum = 0
        for i in range(0, len(self.rules)):
            if self.rules.centres[i] != '#':
                sum += self.rules.ranges[i]

        return sum


class Rules:
    def __init__(self):
        self.centres = []
        self.ranges = []

        # Values to be used for upper and lower bounds in case of wildcard
        self.minLowerBound = -9999
        self.maxUpperBound = +9999


    def getLowerBound(self, i):
        if self.centres[i] == '#':
            return self.minLowerBound

        return self.centres[i] - self.ranges[i]


    def getUpperBound(self, i):
        if self.centres[i] == '#':
            return self.maxUpperBound

        return self.centres[i] + self.ranges[i]