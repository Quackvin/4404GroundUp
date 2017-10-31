import lcs as lcsModule
import classifier as classifierModule
import environment
import json
import log as logModule


def explore():
    log = logModule.Log('testing_result_6.txt' , 'error_6.txt')
    # for a in [10000, 15000, 200000]:
    # for b in [200, 400, 600, 1000]:
    for c in [0.3, 0.6, 0.8]:
        for d in [0.6, 0.4, 0.2]:
            for e in [3, 4, 5]:
                for f in [20, 25, 30]:
                    for h in [0.1, 0.2, 0.3]:
                        for i in [25, 50, 75]:
                            for j in [0.15, 0.25, 0.35,0.55]:
                                for k in [0.01, 0.02, 0.03, 0.1]:
                                    env = environment.Environment('dataTrain.txt')
                                    parameterList = [10000, 2500, c, d, e, f, h, i, j, k, 0.1, 0.1, 20, 0.9]
                                    lcs = lcsModule.LCS(parameterList , log)
                                    run(lcs, env)
                                    [x, y] = test('dataTest.txt' , parameterList , log)
                                    log.logTestResult(x,y,parameterList)



def main(loadPop, debug):
    log = logModule.Log('testing_result_k.txt', 'error_k.txt')
    env = environment.Environment('features/data_means_training.txt')
    parameterList = [10000, 2000, 0.3, 0.5, 5, 30, 0.2, 55, 0.5, 0.02, 0.1, 0.1, 20, 0.9]
    lcs = lcsModule.LCS(parameterList, log)
    if loadPop:
        loadPopulation(lcs)
    run(lcs, env, debug)
    [a, b] = test('./features/data_means_testing.txt', parameterList , log, debug)
    log.logTestResult(a, b, parameterList)
    with open('testing_no_means_result.txt', 'a') as dataFile_1:
        dataFile_1.write("--------------------------------------------------------------------------------------------")
        dataFile_1.write(str(parameterList) + "\n")
        dataFile_1.write("Accuracy  " + str(a) + "   Uncovered: " + str(b) + "\n")


def test(testfile , parameterList , log, debug):
    print('**********Testing Start*********')
    lcs = lcsModule.LCS(parameterList, log)
    loadPopulation(lcs)
    env = environment.Environment(testfile)
    correctCount = 0
    numberOfInstance = 0
    numberOfUncovered = 0

    # resultClassDict = {}
    # actualClassDict = {}

    for instance in env.instances:
        numberOfInstance += 1
        result = lcs.classifyInstance(instance, debug)
        if debug:
            print("LCS decision: " + str(result) + "    True anser: " + str(instance.outcome))
        if result == -1:
            numberOfUncovered += 1
            # if instance.outcome in actualClassDict:
                #actualClassDict[instance.outcome]

        if (result == instance.outcome):
            correctCount += 1

    result = correctCount / numberOfInstance
    print("---Accuracy: " + str(result))
    print("---Number of uncovered instances:" + str(numberOfUncovered))
    print('**********Testing Done*********')

    return [result, numberOfUncovered]


def run(lcs, env, debug):
    print('**********Training*********')
    while True:
        for instance in env.instances:
            # if lcs.currIter == 10000:
            #     print("===============================================================================================")
            #     print("Tetsing Start")
            #     savePopulation(lcs.population)
            #     [a, b] = test('dataTest.txt', lcs.parameterList, lcs.log)
            #     lcs.log.logTestResult(a, b, lcs.parameterList)

            print('iteration: ', lcs.currIter, end='\r', flush=True)
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
            #if len(lcs.correctSet) > 3:  # needs more conditions

            # print("hahah  " + str(lcs.getAverageTimePeriod()))
            # print("GAthreshold  " + str(lcs.GAThreshold))
            if debug:
                print("---CorrectSet size:  " + str(len(lcs.correctSet)))
            if (len(lcs.correctSet) > 2 ): #and ( lcs.getAverageTimePeriod() > lcs.GAThreshold) :
                if debug:
                    print("running GA..............................................")
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
    with open('classifierPopulation_no_means.json', 'w') as writeFile:
        for classifier in population:
            classifierDict = classifier.__dict__
            classifierDict['rules'] = classifierDict['rules'].__dict__
            classifierString = json.dumps(classifierDict) + '\n'
            writeFile.write(classifierString)


def loadPopulation(lcs):
    with open('classifierPopulation_no_means.json', 'r') as readFile:
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

main(False, False)
# log = logModule.Log('testing_result_3.txt', 'error_3.txt')
# parameterList = [10000, 1500, 0.1, 0.4, 10, 0.2, 30, 0.45, 0.55, 0.02, 0.1, 0.1, 20, 0.9]
# test('data.txt' , parameterList , log )
# explore()
