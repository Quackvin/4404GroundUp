import os

class Environment:
    def __init__(self, datafile):
        """

        :rtype: object
        """
        self.instances = self.parseDatafile(datafile)

    def parseDatafile(self, datafile):
        with open(datafile, 'r') as data:
            allInstances = []
            for line in data:
                dataline = line.split('\t')
                outcome = dataline[-1]
                features = []
                for feat in dataline[0:-1]:
                    features.append(float(feat))
                allInstances.append(Instance(features, outcome))
            return allInstances


class Instance:
    def __init__(self, features, outcome):
        self.features = features
        self.outcome = outcome
