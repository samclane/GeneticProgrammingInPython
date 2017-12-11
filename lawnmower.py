from enum import Enum


class FieldContents(Enum):
    Grass = ' #'
    Mowed = ' .'
    Mower = 'M'

    def __str__(self):
        return self.value


class Direction:
    Index = None
    XOffset = None
    YOffset = None
    Symbol = None

    def __init__(self, index, xOffset, yOffset, symbol):
        self.Index = index
        self.XOffset = xOffset
        self.YOffset = yOffset
        self.Symbol = symbol

    def move_from(self, location, distance=1):
        return Location(location.X + distance * self.XOffset, location.Y + distance * self.YOffset)


class Directions(Enum):
    North = Direction(0, 0, -1, '^')
    East = Direction(1, 1, 0, '>')
    South = Direction(2, 0, 1, 'v')
    West = Direction(3, -1, 0, '<')

    @staticmethod
    def get_direction_after_turn_left_90_degrees(direction):
        newIndex = direction.Index - 1 if direction.Index > 0 else len(Directions) - 1
        newDirection = next(i for i in Directions if i.value.Index == newIndex)
        return newDirection.value

    @staticmethod
    def get_direction_after_turn_right_90_degrees(direction):
        newIndex = direction.Index + 1 if direction.Index < len(Directions) - 1 else 0
        newDirection = next(i for i in Directions if i.value.Index == newIndex)
        return newDirection.value  # bookmark


class Mower:
    Location = None
    Direction = None

    def __init__(self, location, direction):
        self.Location = location
        self.Direction = direction
        self.StepCount = 0

    def turn_left(self):
        self.StepCount += 1
        self.Direction = Directions.get_direction_after_turn_left_90_degrees(self.Direction)

    def mow(self, field):
        newLocation = self.Direction.move_from(self.Location)
        self.Location = field.fix_location(newLocation)
        self.StepCount += 1
        field.set(self.Location, self.StepCount if self.StepCount > 9 else " {0}".format(self.StepCount))

    def jump(self, field, forward, right):
        newForwardLocation = self.Direction.move_from(self.Location, forward)
        rightDirection = Directions.get_direction_after_turn_right_90_degrees(self.Direction)
        newLocation = rightDirection.move_from(newForwardLocation, right)
        self.Location = field.fix_location(newLocation)
        self.StepCount += 1
        field.set(self.Location, self.StepCount if self.StepCount > 9 else " {0}".format(self.StepCount))


class Location:
    X = None
    Y = None

    def __init__(self, x, y):
        self.X, self.Y = x, y

    def move(self, xOffset, yOffset):
        return Location(self.X + xOffset, self.Y + yOffset)


class Field:
    Field = None
    Width = None
    Height = None

    def __init__(self, width, height, initialContent):
        self.Field = [[initialContent] * width for _ in range(height)]
        self.Width = width
        self.Height = height

    def set(self, location, symbol):
        self.Field[location.Y][location.X] = symbol

    def fix_location(self, location):
        newLocation = Location(location.X, location.Y)
        if newLocation.X < 0:
            newLocation.X += self.Width
        elif newLocation.X >= self.Width:
            newLocation.X %= self.Width

        if newLocation.Y < 0:
            newLocation.Y += self.Height
        elif newLocation.Y >= self.Height:
            newLocation.Y %= self.Height

        return newLocation

    def count_mowed(self):
        return sum(1 for row in range(self.Height) for column in range(self.Width) if
                   self.Field[row][column] != FieldContents.Grass)

    def display(self, mower):
        for rowIndex in range(self.Height):
            if rowIndex != mower.Location.Y:
                row = ' '.join(map(str, self.Field[rowIndex]))
            else:
                r = self.Field[rowIndex][:]
                r[mower.Location.X] = "{0}{1}".format(FieldContents.Mower, mower.Direction.Symbol)
                row = ' '.join(map(str, r))
            print(row)
