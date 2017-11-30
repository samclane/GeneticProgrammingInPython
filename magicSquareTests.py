import unittest
import datetime
import genetic


class MagicSquareTests(unittest.TestCase):
    def test_size_3(self):
        self.generate(3)

    def geneerate(self, diagonalSize):
        nSquared = diagonalSize * diagonalSize
        geneset = [i for i in range(1, nSquared + 1)]
        expectedSum = diagonalSize * (nSquared + 1) / 2

        def fnGetFitness(genes):
            return get_fitness(genes, diagonalSize, expectedSum)


def get_fitness(genes, diagonalSize, expectedSum):
    rows, columns, northeastDiagonalSum, southeastDiagonalSum = get_sums(genes, diagonalSize)

    fitness = sum(1 for s in rows + columns + [southeastDiagonalSum, northeastDiagonalSum] if s == expectedSum)

    return fitness


def get_sums(genes, diagonalSize):
    rows = [0 for _ in range(diagonalSize)]
    columns = [0 for _ in range(diagonalSize)]
    southeastDiagonalSum = 0
    northeastDiagonalSum = 0
    for row in range(diagonalSize):
        for column in range(diagonalSize):
            value = genes[row * diagonalSize + column]
            rows[row] += value
            columns[column] += value
        southeastDiagonalSum += genes[row * diagonalSize + row]
        northeastDiagonalSum += genes[row * diagonalSize + (diagonalSize - 1 - row)]

    return rows, columns, northeastDiagonalSum, southeastDiagonalSum
