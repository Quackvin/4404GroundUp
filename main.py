import lcs as lcsModule
import environment

def main():
	env = environment.Environment('data.txt')
	lcs = lcsModule.LCS()
	run(lcs, env, False)

def run(lcs, env, doTest):
	for instance in env.instances:
		lcs.currIter += 1

		matchSetSize = lcs.doMatching(instance)
		print('match set size: ', matchSetSize)

		'''	---NOT IMPLEMENTED YET---'''
		if(doTest):
			lcs.formPrediction()
			'''-------------------'''
		else:
			lcs.doCorrectSet(instance)
			print('correct set size: ', len(lcs.correctSet))
			if len(lcs.correctSet) == 0:
				lcs.doCovering(instance)
			lcs.updateParameters(matchSetSize)
			if len(lcs.correctSet) > 3: 				# needs more conditions
				print('doing GA')
				lcs.GA(instance.features)			 	# includes GA subsumption
			# lcs.doCorrectSetSubsumption()
			lcs.consolidateClassifiers()
			while len(lcs.population) > lcs.maxPopSize:
				lcs.doDeletion()

		'''---NOT IMPLEMENTED YET---'''
		endcondition = False
		if endcondition:
			savePopulation(lcs.population)
			return 0
		'''-------------------------'''

def savePopulation(population):
	pass
# write to file

main()