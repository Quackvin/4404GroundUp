import os
print(os.getcwd())

with open('dataTrain.txt', 'w') as dataTrain:
    with open('dataTest.txt', 'w') as dataTest:
        with open('dataFull.txt', 'r') as dataFile:
            j = 0
            for line in dataFile:
                print(line)
                a = line.split('\t')
                print( len(a) )
                if len(a) == 81:
                    if j%4 == 0:
                        dataTest.write(line)
                        j += 1
                    else:
                        dataTrain.write(line)
                        j += 1