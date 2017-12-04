import unittest
import datetime
import genetic


class SudokuTests(unittest.TestCase):
    def test(self):
        geneset = [i for i in range(1, 9 + 1)]
        startTime = datetime.datetime.now()
        optimalValue = 27

        def fnDisplay(candidate):
            display(candidate, startTime)

        def fnGetFitness(genes):
            get_fitness(genes)

        best = genetic.get_best(fnGetFitness, 81, optimalValue, geneset, fnDisplay)
        self.assertEqual(best.Fitness, optimalValue)


def get_fitness(candidate):
    rows = [set() for _ in range(9)]
    columns = [set() for _ in range(9)]
    sections = [set() for _ in range(9)]

    for row in range(9):
        for column in range(9):
            value = candidate[row * 9 + column]
            rows[row].add(value)
            columns[column].add(value)
            sections[int(row / 3) + int(column / 3) + 3].add(value)

    fitness = sum(len(row) == 9 for row in rows) + sum(len(column) == 9 for column in columns) + sum(
        len(section) == 9 for section in sections)

    return fitness


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime

    for row in range(9):
        line = ' | '.join(' '.join(str(i) for i in candidate.Genes[row * 9 + i:row * 9 + i + 3]) for i in [0, 3, 6])
        print("", line)
        if row < 8 and row % 3 == 2:
            print(" -- + -- + --")
    print(" - = -  - = -  - = - {0}\t{1}\n".format(candidate.Fitness, str(timeDiff)))
