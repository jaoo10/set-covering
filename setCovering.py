#!/usr/bin/python

from sys import argv
from time import time
from heapq import nsmallest
import random

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
            row = random.sample(universeTemp,1).pop()
            for i in columns:
                if row in subsets[i][1]:
                    solution.add(i)
                    cost += subsets[i][0]
                    universeTemp.difference_update(subsets[i][1])
                if (len(universeTemp) == 0): break
        population.append([cost,solution])
    return population

def selection(population):
    return min([random.sample(population,1).pop() for i in range(3)],
            key = lambda x: x[0])

def mateIndividuals(universe,parents,subsets):
    crossParent = set(parents[0][1])
    crossParent.update(parents[1][1])
    return generatePopulation(universe,crossParent,
            subsets,len(parents))

def mutation(individuals,rate,columns,subsets):
    for indiv in individuals:
        if random.uniform(0,1) <= rate:
            columnsDif = set(columns)
            columnsDif.difference_update(indiv[1])
            if (len(columnsDif) != 0):
                col = random.sample(columnsDif,1).pop()
                indiv[0] += subsets[col][0]
                indiv[1].add(col)

def updatePopulation(population,newIndividuals):
    population.sort(key = lambda indiv: indiv[0])
    for i in range(len(newIndividuals)):
        population[len(population) - (i + 1)] = newIndividuals[i]

#genetic algorithm to solve the set covering problem
def geneticSCP(universe,columns,subsets,populationSize,
        mutationRate,estimateTime):
    startTime = time()
    totalTime = 0
    population = generatePopulation(universe,columns,subsets,
            populationSize)
    while totalTime < estimateTime:
        parents = [selection(population) for i in range(2)]
        newIndividuals = mateIndividuals(universe,parents,subsets)
        mutation(newIndividuals,mutationRate,columns,subsets)
        updatePopulation(population,newIndividuals)
        totalTime = time() - startTime
    showSmallest(population)
    
def showSmallest(population):
    smallest = nsmallest(1, population, key = lambda x: x[0]).pop()
    print("cost: %s" % smallest[0]),
    print(smallest[1])

if __name__ == "__main__":
    random.seed(time())
    filename = argv[1]
    populationSize = int(argv[2])
    mutationRate = float(argv[3])
    estimateTime = float(argv[4])
    universe, columns, subsets = readFile(filename)
    geneticSCP(universe,columns,subsets,populationSize,
            mutationRate,estimateTime)
