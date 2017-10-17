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

class Rules:
	def __init__(self):
		self.centres = []
		self.ranges = []

	def getLowerBound(self, i):
		return self.centres[i] - self.ranges[i]

	def getUpperBound(self, i):
		return self.centres[i] + self.ranges[i]