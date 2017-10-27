import lcs as lcsModule
import classifier as classifierModule
import environment
import json


def explore():
    for a in [10000, 20000, 300000]:
        for b in [1500, 2000, 2500, 3000]:
            for c in [0.1, 0.2, 0.3, 0.4]:
                for d in [0.2, 0.4, 0.6]:
                    for e in [10, 20, 30]:
                        for f in [0.1, 0.2, 0.3]:
                            for h in [20, 25, 30]:
                                for i in [0.45, 0.55, 0.65]:
                                    env = environment.Environment('dataFull.txt')
                                    parameterList = [a, b, c, d, e, f, h, i, 0.55, 0.02, 0.1, 0.1, 20, 0.9]
                                    lcs = lcsModule.LCS(parameterList)
                                    run(lcs, env)
                                    [x, y] = test('data.txt' , parameterList)
                                    with open('testing_result.txt', 'a') as dataFile_1:
                                        dataFile_1.write(str(parameterList) + "\n")
                                        dataFile_1.write("Accuracy  " + str(x) + "Uncovered: " + str(y) + "\n" )
                                        dataFile_1.write("-------------------------------------------------------------" + "\n")

def main(loadPop):
    env = environment.Environment('dataFull.txt')
    parameterList = [10000, 2000, 0.3, 0.5, 5, 20, 0.1, 25, 0.55, 0.02, 0.1, 0.1, 20, 0.9]
    lcs = lcsModule.LCS(parameterList)
    if loadPop:
        loadPopulation(lcs)
    run(lcs, env)
    [a, b] = test('data.txt', parameterList = [10000, 2000, 0.3, 0.5, 5, 20, 0.1, 25, 0.55, 0.02, 0.1, 0.1, 20, 0.9] )
    with open('testing_result.txt', 'a') as dataFile_1:
        dataFile_1.write(str(parameterList))
        dataFile_1.write("Accuracy  " + str(a) + "Uncovered: " + str(b))


def test(testfile , parameterList):
    print('**********Testing Start*********')
    lcs = lcsModule.LCS(parameterList)
    loadPopulation(lcs)
    env = environment.Environment(testfile)
    correctCount = 0
    numberOfInstance = 0
    numberOfUncovered = 0
    for instance in env.instances:
        numberOfInstance += 1
        result = lcs.classifyInstance(instance)
        print("LCS decision: " + str(result) + "    True anser: " + str(instance.outcome))
        if result == -1:
            numberOfUncovered += 1

        if (result == instance.outcome):
            correctCount += 1

    result = correctCount / numberOfInstance
    print("---Accuracy: " + str(result))
    print("---Number of uncovered instances:" + str(numberOfUncovered))
    print('**********Testing Done*********')

    return [result, numberOfUncovered]


def run(lcs, env):
    print('**********Training*********')
    while True:
        for instance in env.instances:
            print('iteration: ', lcs.currIter)
            lcs.currIter += 1

            matchSetSize = lcs.doMatching(instance)
            '''	---NOT IMPLEMENTED YET---'''
            # if (doTest):
            #    lcs.formPrediction()
            #    '''-------------------'''
            # else:
            lcs.doCorrectSet(instance)
            if len(lcs.correctSet) == 0:
                lcs.doCovering(instance)
            lcs.updateParameters(matchSetSize)
            if len(lcs.correctSet) > 3:  # needs more conditions
                lcs.GA(instance.features)  # includes GA subsumption
            lcs.doCorrectSetSubsumption()
            lcs.consolidateClassifiers()
            if len(lcs.population) > lcs.maxPopSize:
                lcs.doDeletion()

            # print(lcs.getAveClassifierAcc())

            '''---NOT IMPLEMENTED YET---'''
            endcondition = lcs.currIter > lcs.maxNumberOfIteration
            '''-------------------------'''
            if endcondition:
                savePopulation(lcs.population)
                print('**********END**********')
                return 0


def savePopulation(population):
    print('\nSaving')
    with open('classifierPopulation_2.json', 'w') as writeFile:
        for classifier in population:
            classifierDict = classifier.__dict__
            classifierDict['rules'] = classifierDict['rules'].__dict__
            classifierString = json.dumps(classifierDict) + '\n'
            writeFile.write(classifierString)


def loadPopulation(lcs):
    with open('classifierPopulation_2.json', 'r') as readFile:
        for classifierStr in readFile:
            classifierDict = json.loads(classifierStr)

            rules = classifierModule.Rules()
            rules.centres = classifierDict['rules']['centres']
            rules.ranges = classifierDict['rules']['ranges']

            classifier = classifierModule.Classifier(classifierDict['birthIteration'], classifierDict['outcome'], rules)
            classifier.matchCount = classifierDict['matchCount']
            classifier.correctCount = classifierDict['correctCount']
            classifier.accuracy = classifierDict['accuracy']
            classifier.fitness = classifierDict['fitness']
            classifier.numerosity = classifierDict['numerosity']
            classifier.lastGAIteration = classifierDict['lastGAIteration']
            classifier.aveMatchSetSize = classifierDict['aveMatchSetSize']

            lcs.population.append(classifier)

main(False)
#test('data.txt' , parameterList = [10000, 2000, 0.3, 0.5, 5, 20, 0.1, 25, 0.55, 0.02, 0.1, 0.1, 20, 0.9] )
#explore()
