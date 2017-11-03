class Environment:

    def __init__(self, datafile):
        self.instances = self.parseDatafile(datafile)
        self.classList = self.getAllClasses()

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

    def getAllClasses(self):
        class_list=[]
        for instance in self.instances:
            if instance.outcome in class_list:
                pass
            else:
                class_list.append(instance.outcome)
        return class_list

    def initConfusionMatrix(self):
        confusionMatrix = {}
        for cls in self.classList:
            Dict = {}
            for cls2 in self.classList:
                Dict[cls2] = 0
            Dict["Uncovered"] = 0
            confusionMatrix[cls] = Dict

        return confusionMatrix

class Instance:
    def __init__(self, features, outcome):
        self.features = features
        self.outcome  = outcome

if __name__ == "__main__":
    env = Environment('dataTrain.txt')

    confusionMatrix = env.initConfusionMatrix()

    print(confusionMatrix)