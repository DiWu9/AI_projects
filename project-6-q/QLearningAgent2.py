import numpy as np
import coffeegame
import math
import gym

import os
from pylab import *
from pandas import DataFrame, read_csv

# General syntax to import a library but no functions:
##import (library) as (give the library a nickname/alias)
import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

class QLearningAgent:

    def __init__(self, environment, alpha = 0.1, gamma = 0.6, decay_rate = 0.0002, maxSteps = 40, maxEpisode = 5000, render = True):
        """
        alpha: learning rate
        gamma: discount rate
        epsilon: exploration rate
        """
        self.environment = environment
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = 1
        self.decay_rate = decay_rate

        self.maxSteps = maxSteps
        self.maxEpisode = maxEpisode

        self.render = render

        self.state_space_size = environment.observation_space.n
        self.action_space_size = environment.action_space.n

        self.qTable = np.zeros((self.state_space_size,self.action_space_size))

    def learn(self):
        """
        perform q-learning
        """
        firstAvgReward = 0
        secondAvgReward = 0
        thirdAvgReward = 0
        fourthAvgReward = 0
        fifthAvgReward = 0
        for i in range(self.maxEpisode):
            self.updateEpsilon()
            state = self.environment.reset()
            stepsMade = 0
            while stepsMade < self.maxSteps:
                random_float = np.random.uniform(0,1)
                if random_float < self.epsilon:
                    action = np.random.randint(self.action_space_size)
                else:
                    action = self.findGreatestAction(state)
                new_state,reward,done,info = self.environment.step(action)
                if i < 1000:
                    firstAvgReward += reward
                elif i < 2000 and i >= 1000:
                    secondAvgReward += reward
                elif i < 3000 and i >= 2000:
                    thirdAvgReward += reward
                elif i < 4000 and i >= 3000:
                    fourthAvgReward += reward
                else:
                    fifthAvgReward += reward
                self.qTable[state,action] = self.qTable[state, action] * (1 - self.alpha) + \
                                        self.alpha * (reward + self.gamma * np.max(self.qTable[new_state, :]))
                if (done):
                    break
                else:
                    state = new_state
            if self.epsilon <= 0:
                break

        return [firstAvgReward/1000, secondAvgReward/1000, thirdAvgReward/1000,
        fourthAvgReward/1000, fifthAvgReward/1000]

    def plotAvgReward(self, avg_rewards, lineColor, puzzleName):
        """
        plot the graph to visualize reward increases
        """
        ithAverage = []
        for i in range(len(avg_rewards)):
            ithAverage.append(i+1)
        plt.plot(ithAverage, avg_rewards, color = lineColor, linewidth = 2.5,
        linestyle = "-", label = puzzleName)
        plt.xlabel("ith 1000 episode")
        plt.ylabel("average reward")
        plt.savefig('decay_average_reward.png')

    def getQTable(self):
        return self.qTable

    def behave(self):
        """
        choose actions from start state to finish state
        """
        done = False
        steps = []
        total_reward = 0
        current_state = self.environment.reset()
        while not done:
            if self.render:
                self.environment.render()
            action = self.findGreatestAction(current_state)
            steps.append(action)
            new_state,reward,done,info = self.environment.step(action)
            total_reward += reward
            current_state = new_state
        if self.render:
            self.environment.render()
        return [total_reward, steps]

    def findGreatestAction(self, state):
        """
        find the best action accroding to the q value
        """
        possible_rewards = self.qTable[state]
        best_action = -1
        highest_reward = -math.inf
        for i in range(len(possible_rewards)):
            current_reward = possible_rewards[i]
            if current_reward > highest_reward:
                best_action = i
                highest_reward = current_reward
        return best_action

    def updateEpsilon(self):
        self.epsilon = self.epsilon - self.decay_rate

    def init(self, color, puzzleName):
        """
        start learning and print output
        """
        avg_rewards = self.learn()
        #self.plotAvgReward(avg_rewards, color, puzzleName)
        reward, steps = self.behave()
        print(self.getQTable())
        print("total reward: ", reward)
        print("steps made: ", steps)

if __name__ == '__main__':
    agent_coffee = QLearningAgent(coffeegame.CoffeeEnv())
    agent_coffee.init('red', 'coffee game')

    env = gym.make("FrozenLake-v0", is_slippery = False)
    agent_frozen = QLearningAgent(env)
    agent_frozen.init('blue', 'frozen lake')
