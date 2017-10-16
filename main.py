import lcs as lcsModule
import environment

def main():
	env = environment.Environment()
	lcs = lcsModule.LCS()
	run(lcs, env)

def run(lcs, env, doTest):
	while condition:
		lcs.currIter += 1
		inst = env.getInstance()
		lcs.doMatching(inst, doTest)
		if(doTest):
			lcs.formPrediction()
		# 	do output stuff
		else:
		# do training stuff
			pass

def savePopulation(population):
	pass
# write to file