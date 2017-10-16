import lcs as lcsModule
import environment

def main():
	env = environment.Environment(grass)
	lcs = lcsModule.LCS()
	run(lcs, env)

def run(lcs, env):
	while condition:
		lcs.currIter += 1
		inst = env.getInstance()
		lcs.generateMatchSet(inst)