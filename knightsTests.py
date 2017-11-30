import random


class Position:
    X = None
    Y = None

    def __init__(self, x, y):
        self.X = x
        self.Y = y


def get_attacks(location, boardWidth, boardHeight):
    return [i for i in set(
        Position(x + location.X, y + location.Y) for x in [-2, -1, 1, 2] if 0 <= x + location.X < boardWidth for y in
        [-2, -1, 1, 2] if 0 <= y + location.Y < boardHeight and abs(y) != abs(x))]


def create(fnGetRandomPosition, expectedKnights):
    genes = [fnGetRandomPosition() for _ in range(expectedKnights)]
    return genes


def mutate(genes, fnGetRandomPosition):
    index = random.randrange(0, len(genes))
    genes[index] = fnGetRandomPosition()  # bookmark
