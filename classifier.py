class Classifier:
	def __init__(self, currIter, classification):
		self.matchCount = 0
		self.correctCount = 0
		self.accuracy = 0
		self.fitness = 0
		self.numerosity = 1
		self.lastGAIteration = 0
		self.birthIteration = currIter
		self.averageMatchsetSize = 0

		self.rules = []
		self.classification = classification

class Rule:
	def __init__(self):
		self.centres = []
		self.ranges = []