import numpy as np
import os
from pylab import *
from pandas import DataFrame, read_csv

# General syntax to import a library but no functions:
##import (library) as (give the library a nickname/alias)
import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number


"""
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

class DataProducer:
    """
    convert the csv files to graphs
    """

    def writeCSV(self, title, number, initialSeeds, parameters, evaluations, bestfitness):

        """CSV writter"""

        fitnessDataSet = list(zip(evaluations, bestfitness))
        df = pd.DataFrame(data = fitnessDataSet, columns = ['evaluations', 'bestfitness'])
        df.to_csv(title + str(number) + ".csv", index = False,\
         header = ["#evaluations","current best fitness"])

    def generateGraphForRR(self, maxGen):
        """
        generate the graph for normal royal road analysis
        maxGen: maximum generation to record


        x: number of evaluations runned
        y: current best fitness
        """
        files = []
        evaluations = []
        total_fitness = []
        min_fitness = []
        mean_fitness = []
        max_fitness = []
        for i in range(1,31):
            filename = "RR_normal" + str(i) + ".csv"
            files.append(filename)

        for j in range(len(files)):
            data = np.loadtxt("RR_normal_data/" + files[j], dtype = int , delimiter=',')
            fitness = []
            for k in range(maxGen):
                if len(evaluations) < maxGen: # evaluation only have to add once because all runs are the same
                    if len(data) >= maxGen: # add until maxGen is reached
                        evaluations.append(data[k][0])
                fitness.append(data[k][1])
            total_fitness.append(fitness)

        for i in range(maxGen):
            current_fitness = []
            for j in range(30):
                current_fitness.append(total_fitness[j][i])
            min_fitness.append(min(current_fitness))
            max_fitness.append(max(current_fitness))
            mean_fitness.append(round(sum(current_fitness)/len(current_fitness)))

        plot(evaluations, min_fitness, color = 'red', linewidth = 2.5, linestyle = "-", label = "minimum fitness")
        plot(evaluations, max_fitness, color = 'blue', linewidth = 2.5, linestyle = "-", label = "maximum fitness")
        plot(evaluations, mean_fitness, color = 'black', linewidth = 5, linestyle = "-", label = "average fitness")

        legend()
        savefig('RR_normal.png')

    def generateGraphForRR_No_Imed(self, maxGen):
        """
        generate the graph for normal royal road analysis without intermediate schemas
        maxGen: maximum generation to record


        x: number of evaluations runned
        y: current best fitness
        """
        files = []
        evaluations = []
        total_fitness = []
        min_fitness = []
        mean_fitness = []
        max_fitness = []
        for i in range(1,31):
            filename = "RR_no_imed" + str(i) + ".csv"
            files.append(filename)

        for j in range(len(files)):
            data = np.loadtxt("RR_no_intermediate/" + files[j], dtype = int , delimiter=',')
            fitness = []
            for k in range(maxGen):
                if len(evaluations) < maxGen: # evaluation only have to add once because all runs are the same
                    if len(data) >= maxGen: # add until maxGen is reached
                        evaluations.append(data[k][0])
                fitness.append(data[k][1])
            total_fitness.append(fitness)

        for i in range(maxGen):
            current_fitness = []
            for j in range(30):
                current_fitness.append(total_fitness[j][i])
            min_fitness.append(min(current_fitness))
            max_fitness.append(max(current_fitness))
            mean_fitness.append(round(sum(current_fitness)/len(current_fitness)))

        plot(evaluations, min_fitness, color = 'red', linewidth = 2.5, linestyle = "-", label = "minimum fitness")
        plot(evaluations, max_fitness, color = 'blue', linewidth = 2.5, linestyle = "-", label = "maximum fitness")
        plot(evaluations, mean_fitness, color = 'black', linewidth = 5, linestyle = "-", label = "average fitness")

        legend()
        savefig('RR_no_imed.png')

    def generateGraphForHC(self, maxGen):
        """
        generate the graph for normal royal road analysis without intermediate schemas
        maxGen: maximum generation to record


        x: number of evaluations runned
        y: current best fitness
        """
        files = []
        evaluations = []
        total_fitness = []
        min_fitness = []
        mean_fitness = []
        max_fitness = []
        for i in range(1,31):
            filename = "MountainClimbing" + str(i) + ".csv"
            files.append(filename)

        for j in range(len(files)):
            data = np.loadtxt("HillClimber_data/" + files[j], dtype = int , delimiter=',')
            fitness = []
            for k in range(maxGen):
                if len(evaluations) < maxGen: # evaluation only have to add once because all runs are the same
                    if len(data) >= maxGen: # add until maxGen is reached
                        evaluations.append(data[k][0])
                fitness.append(data[k][1])
            total_fitness.append(fitness)

        for i in range(maxGen):
            current_fitness = []
            for j in range(30):
                current_fitness.append(total_fitness[j][i])
            min_fitness.append(min(current_fitness))
            max_fitness.append(max(current_fitness))
            mean_fitness.append(round(sum(current_fitness)/len(current_fitness)))

        plot(evaluations, min_fitness, color = 'red', linewidth = 2.5, linestyle = "-", label = "minimum fitness")
        plot(evaluations, max_fitness, color = 'blue', linewidth = 2.5, linestyle = "-", label = "maximum fitness")
        plot(evaluations, mean_fitness, color = 'black', linewidth = 5, linestyle = "-", label = "average fitness")

        legend()
        savefig('HillClimber.png')

    def generateGraphForHC_HamingDist(self, maxGen):
        """
        generate the graph for normal royal road analysis without intermediate schemas
        maxGen: maximum generation to record


        x: number of evaluations runned
        y: current best fitness
        """
        files = []
        evaluations = []
        total_fitness = []
        min_fitness = []
        mean_fitness = []
        max_fitness = []
        for i in range(1,31):
            filename = "MountainClimbing" + str(i) + ".csv"
            files.append(filename)

        for j in range(len(files)):
            data = np.loadtxt("HillClimber_data_using_haming_distance/" + files[j], dtype = int , delimiter=',')
            fitness = []
            for k in range(maxGen):
                if len(evaluations) < maxGen: # evaluation only have to add once because all runs are the same
                    if len(data) >= maxGen: # add until maxGen is reached
                        evaluations.append(data[k][0])
                fitness.append(data[k][1])
            total_fitness.append(fitness)

        for i in range(maxGen):
            current_fitness = []
            for j in range(30):
                current_fitness.append(total_fitness[j][i])
            min_fitness.append(min(current_fitness))
            max_fitness.append(max(current_fitness))
            mean_fitness.append(round(sum(current_fitness)/len(current_fitness)))

        plot(evaluations, min_fitness, color = 'red', linewidth = 2.5, linestyle = "-", label = "minimum fitness")
        plot(evaluations, max_fitness, color = 'blue', linewidth = 2.5, linestyle = "-", label = "maximum fitness")
        plot(evaluations, mean_fitness, color = 'black', linewidth = 5, linestyle = "-", label = "average fitness")

        legend()
        savefig('HC_haming_distance.png')

if __name__ == '__main__':
    dp = DataProducer()
    #dp.generateGraphForRR(100)
    dp.generateGraphForRR_No_Imed(100)
    #dp.generateGraphForHC_HamingDist(30)
    #data = np.loadtxt("RR_normal_data/RR_normal1.csv", dtype = int, delimiter = ',')
    #print(data[0][1])
