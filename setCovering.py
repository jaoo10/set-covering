import sys

class Set:
    def __init__(self,setCover,density):
        self.setCover = setCover
        self.density = density

def createSet(filename):
    f = open(filename)
    isData = False
    setCover = dict()
    density = 0
    for line in f:
        data = line.strip("\n").split()
        if not isData:
            dataType = data[0].lower()
            if dataType == "dados":
                isData = True
            elif dataType == "densidade":
                isData = True
                density = float(data[1]) / 100
        else:
            setCover[data[0]] = dict()
            for i in range(2,len(data)):
                setCover[data[0]][data[i]] = float(data[1])
    f.close()
    return Set(setCover,density)

if __name__ == "__main__":
    filename = sys.argv[1]
    setProblem = createSet(filename)
    for i in setProblem.setCover:
        print("%s: " % i),
        print(setProblem.setCover[i])
    print setProblem.density
