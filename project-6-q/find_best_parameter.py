import QLearningAgent as qa
import QLearningAgent2 as qa2

import time
import numpy as np
import coffeegame

alpha_values = np.linspace(0.05,0.2,4)
gamma_values = np.linspace(0.4,0.8,5)
epsilon_values = np.linspace(0.4,0.6,5)

def findBestParameter():
    environment = coffeegame.CoffeeEnv()
    shortest_time = np.inf
    for alpha in alpha_values:
        for gamma in gamma_values:
            for epsilon in epsilon_values:
                print(alpha, gamma, epsilon)
                start = time.time()
                agent_coffee = qa.QLearningAgent(environment, alpha, gamma, epsilon)
                avg_reward = agent_coffee.learn()
                end = time.time()
                time_span = end - start
                if shortest_time > time_span:
                    shortest_time = time_span
                    best_parameter = [alpha, gamma, epsilon]
    return [best_parameter, shortest_time]

print(findBestParameter())
