import classifier as classifierModule
import lcs as lcsModule

def test_doesMatch(lcs):
	testInst = 			[1	,2	,3	,4,	5]
	testRules = classifierModule.Rules()
	testRules.centres = ['#',3,	3.4,4,	6]
	testRules.ranges =  ['#',1,	0.5	,0,	1]
	print(lcs.doesMatch(testRules,testInst))


lcs = lcsModule.LCS()

test_doesMatch(lcs)
