import gym
import numpy as np

from gym.envs.classic_control import rendering

MAX_ITERATIONS = 10

taxi_game = gym.make("Taxi-v3")
taxi_game.reset()

print("Action space: ", taxi_game.action_space)
print("Observation space: ", taxi_game.observation_space)


for i in range(MAX_ITERATIONS):
    random_action = taxi_game.action_space.sample()
    new_state, reward, done, info = taxi_game.step(
       random_action)
    print(reward)
    print(new_state)
    taxi_game.render()
    if done:
        break
taxi_game.close()
