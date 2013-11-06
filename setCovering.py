#!/usr/bin/python

from sys import argv
from random import seed, sample
from time import time
from heapq import nsmallest

#read the file and return a list with the universe and the subsets
def readFile(filename):
    isData = False
    subsets = dict()
    universe = set()
    columns = set()
    f = open(filename)
    for line in f:
        data = line.strip("\n").split()
        if not isData:
            dataType = data[0].lower()
            if dataType == "dados" or dataType == "densidade":
                isData = True
        else:
            subsets[data[0]] = [float(data[1]),set()]
            columns.add(data[0])
            for i in range(2,len(data)):
                universe.add(data[i])
                subsets[data[0]][1].add(data[i])
    f.close()
    return universe, columns, subsets

def generatePopulation(universe,columns,subsets,maxSize):
    population = list()
    while (len(population) < maxSize):
        solution = set()
        cost = 0
        universeTemp = set(universe)
        while (len(universeTemp) != 0):
            row = sample(universeTemp,1).pop()
            for i in columns:
                if row in subsets[i][1]:
                    solution.add(i)
                    cost += subsets[i][0]
                    universeTemp.difference_update(subsets[i][1])
                if (len(universeTemp) == 0): break
        population.append([cost,solution])
    return population

def selection(population):
    return min([sample(population,1).pop() for i in range(3)],
            key = lambda x: x[0])

def mateIndividuals(universe,parents,subsets):
    crossParent = set(parents[0][1])
    crossParent.update(parents[1][1])
    return generatePopulation(universe,crossParent,
            subsets,len(parents))

def updatePopulation(population,newIndividuals):
    population.sort(key = lambda indiv: indiv[0])
    for i in range(len(newIndividuals)):
        population[len(population) - (i + 1)] = newIndividuals[i]

#genetic algorithm to solve the set covering problem
def geneticSCP(universe,columns,subsets,size,estimateTime):
    startTime = time()
    totalTime = 0
    population = generatePopulation(universe,columns,subsets,size)
    while totalTime < estimateTime:
        parents = [selection(population) for i in range(2)]
        newIndividuals = mateIndividuals(universe,parents,subsets)
        updatePopulation(population,newIndividuals,parents)
        totalTime = time() - startTime
    print(nsmallest(1, population, key = lambda x: x[0])).pop()

if __name__ == "__main__":
    seed(time())
    filename = argv[1]
    size = int(argv[2])
    estimateTime = float(argv[3])
    universe, columns, subsets = readFile(filename)
    geneticSCP(universe,columns,subsets,size,estimateTime)
    #for i in subsets: # get the subsets
    #    print(i), #print the column (subset)
    #    print(subsets[i][0]), #the cost of the column
    #    print(subsets[i][1])  #the elements of the column
    #print(universe)
