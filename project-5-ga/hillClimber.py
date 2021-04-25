import numpy as np

from pandas import DataFrame, read_csv

from dataProducer import *

# General syntax to import a library but no functions:
##import (library) as (give the library a nickname/alias)
import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number


class HillClimber:

    def __init__(self, length, size, mutationRate):
        """
        length: length of solutions (bitstrings)
        size: size of population
        """
        self.stringLength = length
        self.populationSize = size

        self.schemas = []
        self.schema_dict = {}

        self.numOfEval = 0

        self.mutationRate = mutationRate

        self.population = []
        self.fitness_list = []

        self.initializeSchema()
        self.generateSeeds()


    def getPopulation(self):
        return self.population

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

    def hamingDistance(self, string):
        """
        calculate the haming distance
        it turns out that using hamingDistance is much faster
        """
        self.numOfEval += 1
        toReturn = 0
        for i in range(self.stringLength):
            if string[i] == "1":
                toReturn += 1
        return toReturn

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

    def selectHalf(self):
        targetSize = int(len(self.population)/2)
        self.population = self.population[:targetSize]
        self.fitness_list = self.fitness_list[:targetSize]

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

    def produceChildren(self):
        self.selectHalf()
        for i in range(len(self.population)):
            self.addString(self.mutation(self.population[i]))

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

    def start(self):
        ithGen = 0
        optimalFitness = self.getOptimalFitness()
        bestFitnessEachGen = []
        evaluationList = []
        evaluationList.append(self.numOfEval)
        bestFitnessEachGen.append(self.fitness_list[0])
        while True:
            self.produceChildren()
            ithGen += 1
            bestFitness = self.fitness_list[0]
            #print(bestFitness)
            evaluationList.append(self.numOfEval)
            bestFitnessEachGen.append(bestFitness)
            if bestFitness == optimalFitness:
                print(ithGen)
                return [evaluationList, bestFitnessEachGen, ithGen]

def generateHCData():
    dp = DataProducer()
    for i in range(12,31):
        hc = HillClimber(64, 128, 0.005)
        initialSeeds = hc.getPopulation()
        [evaluations, bestFitness, totalGeneration] = hc.start()
        dp.writeCSV("MountainClimbing", i, initialSeeds, [64, 128, 0.005], \
        evaluations, bestFitness)

if __name__ == '__main__':
    hc = HillClimber(64, 128, 0.005)
    hc.start()
    #generateHCData()
