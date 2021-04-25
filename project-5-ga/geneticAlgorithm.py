import numpy as np
from dataProducer import *

from pandas import DataFrame, read_csv

# General syntax to import a library but no functions:
##import (library) as (give the library a nickname/alias)
import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number


class GeneticAlgorithm:
    """
    1. 64-bit bitstrings
    2. Population size 128
    3. simple fitness proportional selection: you may implement sigma scaling
    (described on the first page of this paper) if you so choose.
    4. Crossover Rate: 0.7 per pair of parents i.e. 70% of new members added
    to population come as a result of crossover (followed by mutation), and the
    remainder via mutation only.
    5. Mutation Rate: 0.005 per locus.
    note: mutation is applied both to offspring of a single parent as well
    as to offspring created through crossover.

    Gathering Data:

    At a minimum you'll be running three experiments:
        Hillclimber
        RR GA
        RR GA without intermediate levels
    for each experiment (with same parameters), be sure to do 30 independent
    runs with different random seeds.  Keep track of the *best* fitness for
    each generation. Your graphs (below) of fitness over time should then
    aggregate those 30 data sets to display the min/max/mean fitness over the
    30 runs.

    Each run of an experiment should produce a file of data saved in a text
    format (csv), and should contain a header with the random seed for that run,
    as well as the parameter settings, followed by column headings and data (you
    may use the PANDAS package if you'd like)

    Graph the data from each experiment onto a single graph with shared axes.
    *The x axis of your graphs should be fitness evaluations not generations*.

    Follow Mitchell's guidance regarding Hillclimbing parameters and duration of
    experiment.
    """

    def __init__(self, length, size, crossoverRate, mutationRate, intermediateLevel = True):
        """
        initialize population:
        length: length of solutions (bitstrings)
        size: size of population
        crossoverRate: the chance two solutions will do crossover
        mutationRate: the chance of mutation of each bit
        """

        self.stringLength = length
        self.populationSize = size
        self.crossoverRate = crossoverRate
        self.mutationRate = mutationRate

        self.population = []
        self.fitness_list = []

        self.schemas = []
        self.schema_dict = {}
        self.numOfEval = 0

        if intermediateLevel:
            self.initializeSchema()
        else:
            self.initializeSchemaNoMidLevel()

        self.generateSeeds()

    def getPopulation(self):
        return self.population

    def getFitnessList(self):
        return self.fitness_list

    def generateSeeds(self):
        """
        generate ramdom seeds to be beginning population
        """
        for i in range(self.populationSize):
            seed = self.generateSeed()
            self.addString(seed)

    def generateSeed(self):
        """
        generate a random bit string
        """
        toReturn = ""
        for currentIndex in range(self.stringLength):
            toReturn += str(np.random.randint(2))
        return toReturn

    def fitness(self, string):
        """
        royal road fitness function, return the fitness of a bitstring
        """
        fitness = 0
        self.numOfEval += 1
        for i in range(len(self.schemas)):
            currentSchema = self.schemas[i]
            fitness += self.schema_dict[currentSchema] * self.sigma(currentSchema, string)
        return fitness

    def sigma(self, schema, string):
        """
        the sigma function that returns 1 when the bitstring is an instance of
        the schema, otherwise 0
        """
        for i in range(self.stringLength):
            if schema[i] == '1' and string[i] != '1':
                return 0
        return 1

    def initializeSchema(self):
        """
        initialize the set of schemas for RR, which includes intermediate levels

        note: the function only generates 64-bit schemas
        """
        for order in [8,16,32,64]:
            numOfSchemas = int(self.stringLength/order)
            for i in range(0, numOfSchemas):
                schema = "*"*order*i + "1"*order + \
                "*"*order*(numOfSchemas - i - 1)
                self.schema_dict[schema] = order
                self.schemas.append(schema)


    def initializeSchemaNoMidLevel(self):
        """
        initialize the set of schemas for RR without intermediate levels

        note: the function only generates 64-bit schemas
        """
        for order in [8,64]:
            numOfSchemas = int(self.stringLength/order)
            for i in range(0, numOfSchemas):
                schema = "*"*order*i + "1"*order + \
                "*"*order*(numOfSchemas - i - 1)
                self.schema_dict[schema] = order
                self.schemas.append(schema)

    def crossover(self, string1, string2):
        """
        crossover between two bit strings
        """
        if self.crossoverRate - np.random.uniform(0,1):
            crossoverIndex = np.random.randint(self.stringLength)
            crossoverString1 = string1[:crossoverIndex]
            crossoverString2 = string2[:crossoverIndex]
            string1 = crossoverString2 + string1[crossoverIndex:]
            string2 = crossoverString1 + string2[crossoverIndex:]
        return [self.mutation(string1), self.mutation(string2)]

    def mutation(self, string):
        """
        mutate a bit string
        """
        mutation_dict = {"0":"1","1":"0"}
        str_list = list(string)
        for i in range(self.stringLength):
            if np.random.uniform(0,1) - self.mutationRate < 0:
                str_list[i] = mutation_dict[string[i]]
        return "".join(str_list)

    def addString(self, bitString):
        """
        add the string in to maintain the order
        """
        stringFitness = self.fitness(bitString)
        if stringFitness == 0:
            self.fitness_list.append(stringFitness)
            self.population.append(bitString)
            return
        if len(self.fitness_list) == 0:
            self.fitness_list.append(stringFitness)
            self.population.append(bitString)
            return
        elif len(self.fitness_list) == 1:
            if stringFitness > self.fitness_list[0]:
                self.fitness_list.insert(0,stringFitness)
                self.population.insert(0,bitString)
                return
            else:
                self.fitness_list.append(stringFitness)
                self.population.append(bitString)
                return
        else:
            if stringFitness > self.fitness_list[0]:
                self.fitness_list.insert(0,stringFitness)
                self.population.insert(0,bitString)
                return
            elif stringFitness < self.fitness_list[-1]:
                self.fitness_list.append(stringFitness)
                self.population.append(bitString)
                return
            for i in range(0, len(self.fitness_list)-1):
                if self.fitness_list[i+1] <= stringFitness and stringFitness <= self.fitness_list[i]:
                    self.fitness_list.insert(i+1,stringFitness)
                    self.population.insert(i+1,bitString)
                    return

    def getOptimalFitness(self):
        return self.fitness("1"*self.stringLength)

    def chooseParents(self):
        """
        choose parent for crossover
        """
        toReturn = []
        accumulatedList = [self.fitness_list[0]]
        for i in range(len(self.fitness_list)-1):
            accumulatedList.append(accumulatedList[i] + self.fitness_list[i+1])
        if accumulatedList[-1] == 0:
            idx1 = np.random.randint(0,len(self.population))
            idx2 = np.random.randint(0,len(self.population))
            return [self.population[idx1],self.population[idx2]]
        else:
            idx1 = np.random.randint(0,accumulatedList[-1])
            idx2 = np.random.randint(0,accumulatedList[-1])
            if idx1 < accumulatedList[0]:
                toReturn.append(self.population[0])
            if idx2 < accumulatedList[0]:
                toReturn.append(self.population[0])
            for i in range(len(accumulatedList) - 1):
                if idx1 < accumulatedList[i+1] and idx1 >= accumulatedList[i]:
                    toReturn.append(self.population[i])
                if idx2 < accumulatedList[i+1] and idx2 >= accumulatedList[i]:
                    toReturn.append(self.population[i])
            return toReturn

    def produceChildren(self):
        numToProduce = self.populationSize
        childrenList = []
        while numToProduce - len(childrenList) > 0:
            crossoverParents = self.chooseParents()
            children = self.crossover(crossoverParents[0], crossoverParents[1])
            childrenList += children
        for i in range(len(childrenList)):
            self.addString(childrenList[i])


    def selectHalf(self):
        targetSize = int(len(self.population)/2)
        self.population = self.population[:targetSize]
        self.fitness_list = self.fitness_list[:targetSize]

    def start(self):
        ithGen = 0
        optimalFitness = self.getOptimalFitness()
        bestFitnessEachGen = []
        evaluationList = []
        evaluationList.append(self.numOfEval)
        bestFitnessEachGen.append(self.fitness_list[0])
        while True:
            self.produceChildren()
            self.selectHalf()
            ithGen += 1
            bestFitness = self.fitness_list[0]
            evaluationList.append(self.numOfEval)
            bestFitnessEachGen.append(bestFitness)
            if bestFitness == optimalFitness:
                print(ithGen)
                return [evaluationList, bestFitnessEachGen,ithGen]


def generateRRData():
    dp = DataProducer()
    for i in range(1,31):
        ga = GeneticAlgorithm(64, 128, 0.7, 0.005)
        initialSeeds = ga.getPopulation()
        [evaluations, bestFitness, totalGeneration] = ga.start()
        dp.writeCSV("RR_normal", i, initialSeeds, [64, 128, 0.7, 0.005], \
        evaluations, bestFitness)

def generateRRNoIntermediateData():
    dp = DataProducer()
    for i in range(1,31):
        ga = GeneticAlgorithm(64, 128, 0.7, 0.005, False)
        initialSeeds = ga.getPopulation()
        [evaluations, bestFitness, totalGeneration] = ga.start()
        dp.writeCSV("RR_no_imed", i, initialSeeds, [64, 128, 0.7, 0.005], \
        evaluations, bestFitness)


if __name__ == '__main__':
    ga = GeneticAlgorithm(64, 128, 0.7, 0.005, False)
    #generateRRData()
    ga.start()
    #generateRRNoIntermediateData()
