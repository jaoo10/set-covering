#!/usr/bin/python

import sys
import random
import copy
import time

class Subset:
    def __init__(self,cost):
        self.cost = cost
        self.elements = set()

    def setSubElement(self,element):
        self.elements.add(element)

class SetUniverse:
    def __init__(self,setCover,setElements):
        self.setCover = setCover
        self.setElements = setElements

def createSet(filename):
    isData = False
    setCover = dict()
    setElements = set()
    f = open(filename)
    for line in f:
        data = line.strip("\n").split()
        if not isData:
            dataType = data[0].lower()
            if dataType == "dados" or dataType == "densidade":
                isData = True
        else:
            setCover[data[0]] = Subset(float(data[1]))
            for i in range(2,len(data)):
                setElements.add(data[i])
                setCover[data[0]].setSubElement(data[i])
    f.close()
    return SetUniverse(setCover,setElements)

def generatePopulation(universe,subset,maxSize):
    population = list()
    while (len(population) < maxSize):
        solution = set()
        universeTemp = copy.deepcopy(universe)
        while (len(universeTemp) != 0):
            row = random.sample(universeTemp,1)
            for i in subset:
                if row[0] in subset[i].elements:
                    solution.add(i)
                    universeTemp.difference_update(subset[i].elements)
        population.append(solution)
    return population

if __name__ == "__main__":
    random.seed(time.time())
    filename = sys.argv[1]
    setUniverse = createSet(filename)
    for i in setUniverse.setCover:
        print("%s:" % i),
        print(setUniverse.setCover[i].cost),
        print(setUniverse.setCover[i].elements)
    population = generatePopulation(setUniverse.setElements,
            setUniverse.setCover,int(sys.argv[2]))
    for subset in population:
        cost = 0
        for col in subset:
            cost += setUniverse.setCover[col].cost
        print(subset),
        print(cost)
