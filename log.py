class Log:
    def __init__(self, resultFile, errorFile):
        self.__resultFile = resultFile
        self.__errorFile  = errorFile

    def logMessage(self, msg):
        with open(self.__resultFile, 'a' ) as dataFile_1:
            dataFile_1.write(str(msg) + "\n")
            dataFile_1.write("-------------------------------------------------------------" + "\n")

    def logTestResult(self, x , y , parameterList ):
        with open(self.__resultFile, 'a' ) as dataFile_1:
            dataFile_1.write(str(parameterList) + "\n")
            dataFile_1.write("Accuracy  " + str(x) + "  Uncovered: " + str(y) + "\n")
            dataFile_1.write("-------------------------------------------------------------" + "\n")
            dataFile_1.write("\n")

    def logError(self , message):
        with open(self.__errorFile, 'a') as errorFile:
            errorFile.write(message)