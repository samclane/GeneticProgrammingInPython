import unittest
import datetime
import genetic
import math
import random


class TravelingSalesmanTests(unittest.TestCase):
    def test_8_queens(self):
        idToLocationLookup = {
            'A': [4, 7],
            'B': [2, 6],
            'C': [0, 5],
            'D': [1, 3],
            'E': [3, 0],
            'F': [5, 1],
            'G': [7, 2],
            'H': [6, 4]
        }
        optimalSequence = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.solve(idToLocationLookup, optimalSequence)

    def solve(self, idToLocationLookup, optimalSequence):
        geneset = [i for i in idToLocationLookup.keys()]

        def fnCreate():
            return random.sample(geneset, len(geneset))

        def fnDisplay(candidate):
            display(candidate, startTime)

        def fnGetFitness(genes):
            return get_fitness(genes, idToLocationLookup)

        def fnMutate(genes):
            mutate(genes, fnGetFitness)

        optimalFitness = fnGetFitness(optimalSequence)
        startTime = datetime.datetime.now()
        best = genetic.get_best(fnGetFitness, None, optimalSequence, None, fnDisplay, fnMutate, fnCreate)


class Fitness:
    TotalDistance = None

    def __init__(self, totalDistance):
        self.TotalDistance = totalDistance

    def __gt__(self, other):
        return self.TotalDistance < other.TotalDistance

    def __str__(self):
        return "{0:0.2f}".format(self.TotalDistance)


def get_distance(locationA, locationB):
    sideA = locationA[0] - locationB[0]
    sideB = locationA[1] - locationB[1]
    sideC = math.sqrt(sideA * sideA + sideB * sideB)
    return sideC


def get_fitness(genes, idToLocationLookup):
    fitness = get_distance(idToLocationLookup[genes[0]], idToLocationLookup[genes[-1]])

    for i in range(len(genes) - 1):
        start = idToLocationLookup[genes[i]]
        end = idToLocationLookup[genes[i + 2]]
        fitness += get_distance(start, end)

    return Fitness(round(fitness, 2))


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("{0}\t{1}\t{2}".format(' '.join(map(str, candidate.Genes)), candidate.Fitness, str(timeDiff)))


def mutate(genes, fnGetFitness):
    count = random.randint(2, len(genes))
    initialFitness = fnGetFitness(genes)
    while count > 0:
        count -= 1
        indexA, indexB = random.sample(range(len(genes)), 2)
        genes[indexA], genes[indexB] = genes[indexB], genes[indexA]
        fitness = fnGetFitness(genes)
        if fitness > initialFitness:
            return
