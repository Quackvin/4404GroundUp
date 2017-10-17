import lcs as lcsModule
import environment

def main():
	env = environment.Environment('data.txt')
	lcs = lcsModule.LCS(100)
	run(lcs, env, True)

def run(lcs, env, doTest):
	condition = False
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

main()