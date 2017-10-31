import lcs as lcsModule
import classifier as classifierModule
import environment
import json
import log as logModule

def explore2():
    parameterLists = [
        [600, 200, 0.15, 0.5, 5, 30, 0.2, 55, 0.5, 0.02, 0.1, 0.1, 20, 0.9],
        # population size change
        [5000, 1000, 0.15, 0.5, 5, 30, 0.2, 55, 0.5, 0.02, 0.1, 0.1, 20, 0.9],
        [5000, 2000, 0.15, 0.5, 5, 30, 0.2, 55, 0.5, 0.02, 0.1, 0.1, 20, 0.9],
        [5000, 3000, 0.15, 0.5, 5, 30, 0.2, 55, 0.5, 0.02, 0.1, 0.1, 20, 0.9],
        # covering probability change
        [5000, 2000, 0.3, 0.5, 5, 30, 0.2, 55, 0.5, 0.02, 0.1, 0.1, 20, 0.9],
        [5000, 2000, 0.4, 0.5, 5, 30, 0.2, 55, 0.5, 0.02, 0.1, 0.1, 20, 0.9],
        [5000, 2000, 0.5, 0.5, 5, 30, 0.2, 55, 0.5, 0.02, 0.1, 0.1, 20, 0.9],
        # initial factor range change
        [5000, 2000, 0.3, 0.6, 5, 30, 0.2, 55, 0.5, 0.02, 0.1, 0.1, 20, 0.9],
        [5000, 2000, 0.3, 0.1, 5, 30, 0.2, 55, 0.5, 0.02, 0.1, 0.1, 20, 0.9],

        # change iteration
        [10000, 700, 0.3,  0.5, 5, 30, 0.2, 55, 0.5, 0.02, 0.1, 0.1, 20, 0.9],
        [10000, 1000, 0.3, 0.5, 5, 30, 0.2, 55, 0.5, 0.02, 0.1, 0.1, 20, 0.9],
        [10000, 2000, 0.3, 0.5, 5, 30, 0.2, 55, 0.5, 0.02, 0.1, 0.1, 20, 0.9],
        [10000, 2000, 0.3, 0.5, 5, 30, 0.2, 55, 0.7, 0.02, 0.1, 0.1, 20, 0.9],

    ]
    for i in range(len(parameterLists)):
        log = logModule.Log('Result_'+str(i)+'.txt', 'Result_'+str(i)+'.txt')
        env = environment.Environment('dataTrain.txt')
        parameterList = parameterLists[i]
        lcs = lcsModule.LCS(parameterList, log)
        run(lcs, env)
        [a, b] = test('dataTest.txt', parameterList, log)
        log.logTestResult(a, b, parameterList)


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



def main(loadPop):
    log = logModule.Log('testing_result_7.txt', 'error_7.txt')
    env = environment.Environment('dataTrain.txt')
    parameterList = [5000, 1000, 0.15, 0.5, 5, 30, 0.2, 55, 0.5, 0.02, 0.1, 0.1, 20, 0.9]
    lcs = lcsModule.LCS(parameterList, log)
    if loadPop:
        loadPopulation(lcs)
    run(lcs, env)
    [a, b] = test('dataTest.txt', parameterList , log)
    log.logTestResult(a, b, parameterList)
    with open('testing_result.txt', 'a') as dataFile_1:
        dataFile_1.write("--------------------------------------------------------------------------------------------")
        dataFile_1.write(str(parameterList) + "\n")
        dataFile_1.write("Accuracy  " + str(a) + "   Uncovered: " + str(b) + "\n")


def test(testfile , parameterList , log ):
    print('**********Testing Start*********')
    lcs = lcsModule.LCS(parameterList, log)
    loadPopulation(lcs,'classifierPopulation'+str(lcs.parameterList)+'.json' )
    env = environment.Environment(testfile)
    correctCount = 0
    numberOfInstance = 0
    numberOfUncovered = 0

    confusionMatrix        = env.initConfusionMatrix()
    confusionMatrix_ratio  = env.initConfusionMatrix()

    for instance in env.instances:

        numberOfInstance += 1
        result = lcs.classifyInstance(instance)

        # print("LCS decision: " + str(result) + "    True anser: " + str(instance.outcome))
        if result == -1:
            numberOfUncovered += 1
            confusionMatrix[instance.outcome]["Uncovered"] += 1
        else:
            confusionMatrix[instance.outcome][result] += 1

        if result == instance.outcome:
            correctCount += 1

    result = correctCount / numberOfInstance
    print("---Accuracy: " + str(result))
    print("---Number of uncovered instances:" + str(numberOfUncovered))
    print('**********Testing Done*********')

    for cls in confusionMatrix:
        class_occurance_sum = 0
        for cls2 in confusionMatrix[cls]:
            class_occurance_sum += confusionMatrix[cls][cls2]

        for cls3 in confusionMatrix[cls]:
            confusionMatrix_ratio[cls][cls3] = confusionMatrix[cls][cls3]/class_occurance_sum


    log.logMessage("Confusion Matrix: " + str(confusionMatrix))
    log.logMessage("Confusion Ration Matrix: " + str(confusionMatrix_ratio))

    return [result, numberOfUncovered]


def run(lcs, env):
    print('**********Training*********')
    while True:

        for instance in env.instances:

            # if lcs.currIter !=0 and lcs.currIter % 500 == 0:
            # #     print("===============================================================================================")
            # #     print("Tetsing Start")
            #     savePopulation(lcs.population)
            #     lcs.log.logMessage("Result at iteration   " + str(lcs.currIter))
            #     [a, b] = test('data.txt', lcs.parameterList, lcs.log)
            #     lcs.log.logTestResult(a, b, lcs.parameterList)
            #     loadPopulation(lcs)

            # print('iteration: ', lcs.currIter)
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
            # print("---CorrectSet size:  " + str(len(lcs.correctSet)))

            if len(lcs.correctSet) > 2 and ( lcs.getAverageTimePeriod() > lcs.GAThreshold) :
                # print("running GA..............................................")
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
                savePopulation(lcs.population, 'classifierPopulation'+str(lcs.parameterList)+'.json')
                print('**********END**********')
                return 0


def savePopulation(population, saveName):
    print('\nSaving')
    #with open('classifierPopulation_5.json', 'w') as writeFile:
    with open(saveName, 'w') as writeFile:
        for classifier in population:
            classifierDict = classifier.__dict__
            classifierDict['rules'] = classifierDict['rules'].__dict__
            classifierString = json.dumps(classifierDict) + '\n'
            writeFile.write(classifierString)


def loadPopulation(lcs, saveName):
    # with open('classifierPopulation_5.json', 'r') as readFile:
    with open(saveName, 'r') as readFile:
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

# main(False)
# log = logModule.Log('testing_result_8.txt', 'error_8.txt')
# parameterList = [5000, 1000, 0.15, 0.5, 5, 30, 0.2, 55, 0.5, 0.02, 0.1, 0.1, 20, 0.9]
# test('dataTest.txt' , parameterList , log )
explore2()
