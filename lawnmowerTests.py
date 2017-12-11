import random
import unittest
import datetime
import genetic
import lawnmower


# Bookmark: 213

class Mow:
    def __init__(self):
        pass

    @staticmethod
    def execute(mower, field):
        mower.mow(field)

    def __str__(self):
        return "mow"


class Turn:
    def __init__(self):
        pass

    @staticmethod
    def execute(mower, field):
        mower.turn_left()

    def __str__(self):
        return "turn"


class Jump:
    Forward = None
    Right = None

    def __init__(self, forward, right):
        self.Forward = forward
        self.Right = right

    def execute(self, mower, field):
        mower.jump(field, self.Forward, self.Right)

    def __str__(self):
        return "jump({0},{1})".format(self.Forward, self.Right)


class Program:
    Main = None

    def __init__(self, instructions):
        self.Main = instructions

    def evaluate(self, mower, field):
        for instruction in self.Main:
            instruction.execute(mower, field)

    def print(self):
        print(' '.join(map(str, self.Main)))


def create(geneSet, minGenes, maxGenes):
    numGenes = random.randint(minGenes, maxGenes)
    genes = [random.choice(geneSet)() for _ in range(1, numGenes)]
    return genes


class LawnmowerTests(unittest.TestCase):
    def test_mow_turn(self):
        width = height = 8
        geneSet = [lambda: Mow(), lambda: Turn()]
        minGenes = width * height
        maxGenes = int(1.5 * minGenes)
        maxMutationRounds = 3
        expectedNumberOfInstructions = 78

        def fnCreateField():
            return lawnmower.ToroidField(width, height, lawnmower.FieldContents.Grass)

        self.run_with(geneSet, width, height, minGenes, maxGenes, expectedNumberOfInstructions, maxMutationRounds,
                      fnCreateField)

    def test_mow_turn_jump(self):
        width = height = 8
        geneSet = [lambda: Mow(), lambda: Turn(),
                   lambda: Jump(random.randint(0, min(width, height)), random.randint(0, min(width, height)))]
        minGenes = width * height
        maxGenes = int(1.5 * minGenes)
        maxMutationRounds = 1
        expectedNumberOfInstructions = 64

        def fnCreateField():
            return lawnmower.ToroidField(width, height, lawnmower.FieldContents.Grass)

        self.run_with(geneSet, width, height, minGenes, maxGenes, expectedNumberOfInstructions, maxMutationRounds,
                      fnCreateField)

    def run_with(self, geneSet, width, height, minGenes, maxGenes, expectedNumberOfInstructions, maxMutationRounds,
                 fnCreateField):
        mowerStartLocation = lawnmower.Location(int(width / 2), int(height / 2))
        mowerStartDirection = lawnmower.Directions.South.value
        optimalFitness = Fitness(width * height, expectedNumberOfInstructions)
        startTime = datetime.datetime.now()

        def fnCreate():
            return create(geneSet, 1, height)

        def fnEvaluate(instructions):
            program = Program(instructions)
            mower = lawnmower.Mower(mowerStartLocation, mowerStartDirection)
            field = fnCreateField()
            program.evaluate(mower, field)
            return field, mower, program

        def fnGetFitness(genes):
            return get_fitness(genes, fnEvaluate)

        def fnDisplay(candidate):
            display(candidate, startTime, fnEvaluate)

        def fnMutate(child):
            mutate(child, geneSet, minGenes, maxGenes, fnGetFitness, maxMutationRounds)

        best = genetic.get_best(fnGetFitness, None, optimalFitness, None, fnDisplay, fnMutate, fnCreate, poolSize=10,
                                crossover=crossover)
        self.assertTrue(not best.Fitness > optimalFitness)


class Fitness:
    TotalMowed = None
    TotalInstructions = None

    def __init__(self, totalMowed, totalInstructions):
        self.TotalMowed = totalMowed
        self.TotalInstructions = totalInstructions

    def __gt__(self, other):
        if self.TotalMowed != other.TotalMowed:
            return self.TotalMowed > other.TotalMowed
        return self.TotalInstructions < other.TotalInstructions

    def __str__(self):
        return "{0} mowed with {1} instructions".format(self.TotalMowed, self.TotalInstructions)


def get_fitness(genes, fnEvaluate):
    field = fnEvaluate(genes)[0]
    return Fitness(field.count_mowed(), len(genes))


def display(candidate, startTime, fnEvaluate):
    field, mower, program = fnEvaluate(candidate.Genes)
    timeDiff = datetime.datetime.now() - startTime
    field.display(mower)
    print("{0}\t{1}".format(candidate.Fitness, str(timeDiff)))
    program.print()


def mutate(genes, geneSet, minGenes, maxGenes, fnGetFitness, maxRounds):
    count = random.randint(1, maxRounds)
    initialFitness = fnGetFitness(genes)
    while count > 0:
        count -= 1
        if fnGetFitness(genes) > initialFitness:
            return
        adding = len(genes) == 0 or (len(genes) < maxGenes and random.randint(0, 5) == 0)
        if adding:
            genes.append(random.choice(geneSet)())
            continue

        removing = len(genes) > minGenes and random.randint(0, 50) == 0
        if removing:
            index = random.randrange(0, len(genes))
            del genes[index]
            continue

        index = random.randrange(0, len(genes))
        genes[index] = random.choice(geneSet)()


def crossover(parent, otherParent):
    childGenes = parent[:]
    if len(parent) <= 2 or len(otherParent) < 2:
        return childGenes
    length = random.randint(1, len(parent) - 2)
    start = random.randrange(0, len(parent) - length)
    childGenes[start:start + length] = otherParent[start:start + length]
    return childGenes
