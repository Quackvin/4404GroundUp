import classifier as classifierModule
import lcs as lcsModule
import environment as environmentModule

def test_doMatching():
	lcs = lcsModule.LCS()
	testRules = classifierModule.Rules()
	testFeats = 			[1, 	2, 		3, 		4, 		-3.1]
	testRules.centres =		['#',	3,		3.4,	4,		-2]
	testRules.ranges = 		['#', 	1, 		0.5, 	0, 		1.5]

	testInst = environmentModule.Instance(testFeats, 1)

	testClassifier = classifierModule.Classifier(0, 1, testRules)
	lcs.population.append(testClassifier)

	testClassifier = classifierModule.Classifier(0, 2, testRules)
	lcs.population.append(testClassifier)

	print(lcs.doMatching(testInst))

def test_doesMatch():
	lcs = lcsModule.LCS()

	testRules = classifierModule.Rules()
	testInst = 				[1	,	2,		3,		4,		-3.1]
	testRules.centres = 	['#',	3,		3.4,	4,		-2]
	testRules.ranges =  	['#',	1,		0.5	,	0,		1.5]
	print(lcs.doesMatch(testRules,testInst))

def test_doCorrectSet():
	lcs = lcsModule.LCS()
	testRules = classifierModule.Rules()
	testFeats = [1, 2, 3, 4, -3.1]
	testRules.centres = ['#', 3, 3.4, 4, -2]
	testRules.ranges = ['#', 1, 0.5, 0, 1.5]

	testInst = environmentModule.Instance(testFeats, 1)

	testClassifier = classifierModule.Classifier(0, 1, testRules)
	lcs.population.append(testClassifier)

	testClassifier = classifierModule.Classifier(0, 2, testRules)
	lcs.population.append(testClassifier)

	lcs.doMatching(testInst)
	lcs.doCorrectSet(testInst)
	print('cSet', len(lcs.correctSet), 'mSet', len(lcs.matchSet), 'pop', len(lcs.population))


def test_doCorrectSetSubsumption_noSub():
    lcs = lcsModule.LCS()

    # Define test rules
    testRules1 = classifierModule.Rules()
    testRules2 = classifierModule.Rules()
    testRules1.centres = [1.5, 2.5, 1.8, 3.5, 0]
    testRules1.ranges = [0.7, 1, 0.5, 4, 1.5]
    testRules2.centres = ['#', 3, 3.4, 4, -2]
    testRules2.ranges = ['#', 1, 0.5, 0, 1.5]

    # Define test classifiers
    testClassifier1 = classifierModule.Classifier(0, 1, testRules1)
    testClassifier1.accuracy = 1
    testClassifier1.correctCount = 50
    lcs.correctSet.append(testClassifier1)
    testClassifier2 = classifierModule.Classifier(0, 2, testRules2)
    testClassifier2.accuracy = 1
    testClassifier2.correctCount = 50
    lcs.correctSet.append(testClassifier2)

    # Call doCorrectSetSubsumption
    lcs.doCorrectSetSubsumption()

    # Check outputs
    if len(lcs.correctSet) != 2 or lcs.correctSet[0].numerosity != 1 or lcs.correctSet[1].numerosity != 1:
        print("doCorrectSetSubsumption: no subsumption test failed!")
        print("correct set size: ", len(lcs.correctSet))
    else:
        print("doCorrectSetSubsumption: no subsumption test passed")


def test_doCorrectSetSubsumption_sub():
    lcs = lcsModule.LCS()

    # Define test rules
    testRules1 = classifierModule.Rules()
    testRules2 = classifierModule.Rules()
    testRules1.centres = [1.5, 2.5, 3, 3.5, -2.5]
    testRules1.ranges = [0.7, 0.5, 0.5, 0, 1.5]
    testRules2.centres = ['#', 3, 3.4, 4, -2]
    testRules2.ranges = ['#', 1.5, 5, 2, 4]


    # Define test classifiers
    testClassifier1 = classifierModule.Classifier(0, 1, testRules1)
    testClassifier1.accuracy = 1
    testClassifier1.correctCount = 50
    lcs.correctSet.append(testClassifier1)
    testClassifier2 = classifierModule.Classifier(0, 2, testRules2)
    testClassifier2.accuracy = 1
    testClassifier2.correctCount = 50
    lcs.correctSet.append(testClassifier2)

    # Call doCorrectSetSubsumption
    lcs.doCorrectSetSubsumption()

    # Check outputs
    if len(lcs.correctSet) != 1 or lcs.correctSet[0].numerosity != 2 or lcs.correctSet[0].rules.centres[0] != '#':
        print("doCorrectSetSubsumption: subsumption test failed!")
    else:
        print("doCorrectSetSubsumption: subsumption test passed")


test_doMatching()
test_doesMatch()
test_doCorrectSet()
test_doCorrectSetSubsumption_noSub()
test_doCorrectSetSubsumption_sub()
