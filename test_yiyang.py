import lcs as lcsModule
import classifier as classifierModule
import environment
import json
import main as M


def a():
    env = environment.Environment('dataFULL.txt')
    print("hahah")
    lcs = lcsModule.LCS( parameterList = [10000, 2000, 0.3, 0.5, 5, 20, 0.1, 25, 0.55, 0.02, 0.1, 0.1, 20, 0.9] )
    M.loadPopulation(lcs)
    lcs.GA()

if __name__ == "__main__":
    a()
