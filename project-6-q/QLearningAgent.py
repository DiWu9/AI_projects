import numpy as np
import coffeegame
import math
import gym


from gym.envs.classic_control import rendering

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

class QLearningAgent:
    """
    according to the result of find_best_parameter, it turns out that 0.2, 0.7, 0.4
    is the set of parameters that find the result with least time
    """
    def __init__(self, environment, alpha = 0.2, gamma = 0.7, epsilon = 0.4,
     maxSteps = 40, maxEpisode = 5000, render = True):
        """
        alpha: learning rate
        gamma: discount rate
        epsilon: exploration rate
        """
        self.environment = environment
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
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
        return [firstAvgReward/1000, secondAvgReward/1000, thirdAvgReward/1000,
        fourthAvgReward/1000, fifthAvgReward/1000]
        """
        print("Average reward (first 1000 episode): ", firstAvgReward/1000)
        print("Average reward (second 1000 episode): ", secondAvgReward/1000)
        print("Average reward (third 1000 episode): ", thirdAvgReward/1000)
        print("Average reward (fourth 1000 episode): ", fourthAvgReward/1000)
        print("Average reward (fifth 1000 episode): ", fifthAvgReward/1000)
        """

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

    def init(self):
        """
        start learning and print output
        """
        self.learn()
        reward, steps = self.behave()
        """
        print(self.getQTable())
        print("total reward: ", reward)
        print("steps made: ", steps)
        """

if __name__ == '__main__':
    agent_coffee = QLearningAgent(coffeegame.CoffeeEnv())
    agent_coffee.init()

    env = gym.make("FrozenLake-v0", is_slippery = False)
    agent_frozen = QLearningAgent(env)
    agent_frozen.init()
