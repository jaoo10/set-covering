#!/usr/bin/python

from sys import argv
from time import time
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
        population.append([cost,solution])
    return population

def selection(population):
    return min([random.sample(population,1).pop() for i in range(3)],
            key = lambda x: x[0])

def mateIndividuals(universe,parents,subsets):
    crossParent = set(parents[0][1])
    crossParent.update(parents[1][1])
    return generatePopulation(universe,crossParent,
            subsets,1).pop()

def mutation(individual,rate,columns,subsets):
    if random.uniform(0,1) <= rate:
        columnsDif = set(columns)
        columnsDif.difference_update(individual[1])
        if (len(columnsDif) != 0):
            col = random.sample(columnsDif,1).pop()
            individual[0] += subsets[col][0]
            individual[1].add(col)

def updatePopulation(population,newIndividual,extremes):
    population.sort(key = lambda indiv: indiv[0])
    population[len(population) - 1] = newIndividual
    extremes[0] = population[len(population) - 2][0] #max cost
    extremes[1] = population[0][0] #min cost

def VND(universe,subsets,solution,r):
    s = solution
    k = 1
    while k <= r:
        neighbor = generatePopulation(universe,s[1],subsets,1).pop()
        if (neighbor[0] < s[0]):
            s = neighbor
            k = 1
        else:
            k += 1
    return s

#genetic algorithm to solve the set covering problem
def geneticSCP(universe,columns,subsets,populationSize,
        mutationRate,estimateTime):
    startTime = time()
    totalTime = 0
    extremes = [i for i in range(2)] #max and min costs
    population = generatePopulation(universe,columns,subsets,
            populationSize)
    while totalTime < estimateTime and int(extremes[0]) != int(extremes[1]):
        parents = [selection(population) for i in range(2)]
        newIndividual = mateIndividuals(universe,parents,subsets)
        mutation(newIndividual,mutationRate,columns,subsets)
        newIndividual = VND(universe,subsets,newIndividual,5)
        updatePopulation(population,newIndividual,extremes)
        totalTime = time() - startTime
    return population[0], totalTime

if __name__ == "__main__":
    random.seed(time())
    filename = argv[1]
    populationSize = int(argv[2])
    mutationRate = float(argv[3])
    estimateTime = float(argv[4])
    universe, columns, subsets = readFile(filename)
    smallest, totalTime = geneticSCP(universe,columns,subsets,populationSize,
            mutationRate,estimateTime)
    print("cost: %s" % smallest[0]),
    print("time: %.2fs" % totalTime),
    print(smallest[1])
