#!/usr/bin/python

from sys import argv
from random import seed, sample
from copy import deepcopy
from time import time

#read the file and return a list with the universe and the subsets
def readFile(filename):
    isData = False
    subsets = dict()
    universe = set()
    f = open(filename)
    for line in f:
        data = line.strip("\n").split()
        if not isData:
            dataType = data[0].lower()
            if dataType == "dados" or dataType == "densidade":
                isData = True
        else:
            subsets[data[0]] = [float(data[1]),set()]
            for i in range(2,len(data)):
                universe.add(data[i])
                subsets[data[0]][1].add(data[i])
    f.close()
    return universe, subsets

def generatePopulation(universe,subset,maxSize):
    population = list()
    while (len(population) < maxSize):
        solution = set()
        universeTemp = deepcopy(universe)
        cost = 0
        while (len(universeTemp) != 0):
            row = sample(universeTemp,1).pop()
            for i in subset:
                if row in subset[i][1]:
                    solution.add(i)
                    cost += subset[i][0]
                    universeTemp.difference_update(subset[i][1])
        population.append([solution,cost])
    return population

def selection(population):
    individuals = list()
    for i in range(0,3): individuals.append(sample(population,1).pop())
    return min(individuals, key = lambda individual: individual[1])

if __name__ == "__main__":
    seed(time())
    filename = argv[1]
    universe, subsets = readFile(filename)
    for i in subsets: # get the subsets
        print(i), #print the column (subset)
        print(subsets[i][0]), #the cost of the column
        print(subsets[i][1])  #the elements of the column
    print(universe)
    print
    population = generatePopulation(universe,subsets,int(argv[2]))
    individual = selection(population)
    for solution in population:
        print(solution)
    print
    print(individual)
