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

test_doMatching()
test_doesMatch()
test_doCorrectSet()
