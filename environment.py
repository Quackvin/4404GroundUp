class Environment:
	def __init__(self):
		self.instances = []

	def parseDatafile(self):
		pass

class Instance:
	def __init__(self, features, outcome):
		self.features = features
		self.outcome = outcome
