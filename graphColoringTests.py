import csv
import unittest
import datetime
import genetic


def load_data(localFileName):
    rules = set()
    nodes = set()
    with open(localFileName, mode='r') as infile:
        content = infile.read().splitlines()
    for row in content:
        if row[0] == 'e':
            nodeIds = row.split(' ')[1:3]
            rules.add(Rule(nodeIds[0], nodeIds[1]))
            nodes.add(nodeIds[0])
            nodes.add(nodeIds[1])
            continue
        if row[0] == 'n':
            nodeIds = row.split(' ')
            nodes.add(nodeIds[1])
    return rules, nodes


class Rule:
    Node = None
    Adjacent = None

    def __init__(self, node, adjacent):
        if node < adjacent:
            node, adjacent = adjacent, node
        self.Node = node
        self.Adjacent = adjacent

    def __eq__(self, other):
        return self.Node == other.Node and self.Adjacent == other.Adjacent

    def __hash__(self):
        return hash(self.Node) * 397 ^ hash(self.Adjacent)

    def __str__(self):
        return self.Node + " -> " + self.Adjacent

    def IsValid(self, genes, nodeIndexLookup):
        index = nodeIndexLookup[self.Node]
        adjacentStateIndex = nodeIndexLookup[self.Adjacent]
        return genes[index] != genes[adjacentStateIndex]


def build_rules(items):
    rulesAdded = {}

    for state, adjacent in items.items():
        for adjacentState in adjacent:
            if adjacentState == '':
                continue
            rule = Rule(state, adjacentState)
            if rule in rulesAdded:
                rulesAdded[rule] += 1
            else:
                rulesAdded[rule] = 1

    for k, v in rulesAdded.items():
        if v != 2:
            print("rule {0} is not bidirectional".format(k))

    return rulesAdded.keys()


class GraphColoringTests(unittest.TestCase):
    @staticmethod
    def test_convert_file():
        states = load_data("adjacent_states.csv")
        output = []
        nodeCount = edgeCount = 0
        for state, adjacents in states.items():
            nodeCount += 1
            for adjacent in adjacents:
                if adjacent == "":
                    output.append("n {0} 0".format(state))
                else:
                    output.append("e {0} {1}".format(state, adjacent))
                    edgeCount += 1
        with open('./adjacent_states.csv', mode='w+') as outfile:
            print("p edge {0} {1}".format(nodeCount, edgeCount), file=outfile)
            for line in sorted(output):
                print(line, file=output)

    def test_states(self):
        self.color("adjacent_states.csv", ["Orange", "Yellow", "Green", "Blue"])

    def color(self, file, colors):
        rules, nodes = load_data(file)
        optimalValue = len(rules)
        colorLookup = {color[0]: color for color in colors}
        geneset = list(colorLookup.keys())
        startTime = datetime.datetime.now()
        nodeIndexLookup = {key: index for index, key in enumerate(sorted(nodes))}

        def fnDisplay(candidate):
            display(candidate, startTime)

        def fnGetFitness(genes):
            return get_fitness(genes, rules, nodeIndexLookup)

        best = genetic.get_best(fnGetFitness, len(nodes), optimalValue, geneset, fnDisplay)
        self.assertTrue(not optimalValue > best.Fitness)

        keys = sorted(nodes)
        for index in range(len(nodes)):
            print(keys[index] + " is " + colorLookup[best.Genes[index]])

    def test_benchmark(self):
        genetic.Benchmark.run(lambda: self.test_states)



def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("{0}\t{1}\t{2}".format(''.join(map(str, candidate.Genes)), candidate.Fitness, str(timeDiff)))


def get_fitness(genes, rules, stateIndexLookup):
    rulesThatPass = sum(1 for rule in rules if rule.IsValid(genes, stateIndexLookup))
    return rulesThatPass
