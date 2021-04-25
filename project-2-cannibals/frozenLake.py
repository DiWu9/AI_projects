### File: frozenLake.py
### Implements frozen lake puzzle in the open AI gym problem for state
### space search

from improvedSearch import *
import gym
from gym.envs.classic_control import rendering

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

class FrozenLakeState(ProblemState):

    def __init__(self, env, state, reward, operator = None):
        """
        state: the current position
        operator: possible move to transit from current state to its child
        """
        self.environment = env
        self.state = state
        self.reward = reward
        self.operator = operator

    def __str__(self):
        """
        return a string representation of the state class
        """
        result = ""
        if self.operator is not None:
            result += "By go " + self.operator + ": "
        else:
            result += "Initial: "
        result += "reach " + str(self.state) + "\n"
        return result

    def equals(self, anotherState):
        """
        check if two states are equals
        """
        return self.state == anotherState.state and self.reward == anotherState.reward

    def dictkey(self):
        return str(int(self.state)) + "," + str(int(self.reward))

    def goUp(self):
        current_state = self.state
        if current_state in [9,15]:
            return None
        else:
            new_environment = self.cloneEnv()
            new_state,reward,done,info = new_environment.step(UP)
            to_return = FrozenLakeState(self.environment, new_state, reward, "up")
        return to_return

    def goDown(self):
        current_state = self.state
        if current_state in [1,3,8]:
            return None
        else:
            new_environment = self.cloneEnv()
            new_state,reward,done,info = new_environment.step(DOWN)
            to_return = FrozenLakeState(self.environment, new_state, reward, "down")
        return to_return

    def goLeft(self):
        current_state = self.state
        if current_state in [6,13]:
            return None
        else:
            new_environment = self.cloneEnv()
            new_state,reward,done,info = new_environment.step(LEFT)
            to_return = FrozenLakeState(self.environment, new_state, reward, "left")
        return to_return

    def goRight(self):
        current_state = self.state
        if current_state in [4,6,10]:
            return None
        else:
            new_environment = self.cloneEnv()
            new_state,reward,done,info = new_environment.step(RIGHT)
            to_return = FrozenLakeState(new_environment, new_state, reward, "right")
        return to_return

    def applyOperators(self):
        """
        Required method for use with the Search class.
        Returns a list of valid successors to the current state
        """
        #self.renderCurrentEnvironment()
        to_return = []
        possible_moves = [self.goUp(),self.goDown(),self.goRight(),self.goLeft()]
        for move in possible_moves:
            if not move is None:
                to_return.append(move)
        return to_return

    def cloneEnv(self):
        frozenLake = gym.make("FrozenLake-v0", is_slippery = False)
        frozenLake.reset()
        if self.state == 0:
            return frozenLake
        elif self.state == 1:
            frozenLake.step(RIGHT)
            return frozenLake
        elif self.state == 2:
            frozenLake.step(RIGHT)
            frozenLake.step(RIGHT)
            return frozenLake
        elif self.state == 3:
            frozenLake.step(RIGHT)
            frozenLake.step(RIGHT)
            return frozenLake
        elif self.state == 4:
            frozenLake.step(DOWN)
            return frozenLake
        elif self.state == 6:
            frozenLake.step(RIGHT)
            frozenLake.step(RIGHT)
            frozenLake.step(DOWN)
            return frozenLake
        elif self.state == 8:
            frozenLake.step(DOWN)
            frozenLake.step(DOWN)
            return frozenLake
        elif self.state == 9:
            frozenLake.step(DOWN)
            frozenLake.step(DOWN)
            frozenLake.step(RIGHT)
            return frozenLake
        elif self.state == 10:
            frozenLake.step(DOWN)
            frozenLake.step(DOWN)
            frozenLake.step(RIGHT)
            frozenLake.step(RIGHT)
            return frozenLake
        elif self.state == 13:
            frozenLake.step(DOWN)
            frozenLake.step(DOWN)
            frozenLake.step(RIGHT)
            frozenLake.step(DOWN)
            return frozenLake
        elif self.state == 14:
            frozenLake.step(DOWN)
            frozenLake.step(DOWN)
            frozenLake.step(RIGHT)
            frozenLake.step(DOWN)
            frozenLake.step(RIGHT)
            return frozenLake
        elif self.state == 15:
            frozenLake.step(DOWN)
            frozenLake.step(DOWN)
            frozenLake.step(RIGHT)
            frozenLake.step(DOWN)
            frozenLake.step(RIGHT)
            frozenLake.step(RIGHT)
            return frozenLake
        else:
            return None

    def renderCurrentEnvironment(self):
        self.environment.render()

frozenLake = gym.make("FrozenLake-v0", is_slippery = False)
frozenLake.reset()
#print(FrozenLakeState(frozenLake, 5).isValidState())

Search(FrozenLakeState(frozenLake, 0, 0), FrozenLakeState(frozenLake, 15, 1))

"""
initial_state = FrozenLakeState(frozenLake, 0, 0)
initial_state.renderCurrentEnvironment()
print("initial state: ", initial_state)
list = initial_state.applyOperators()
print(len(list))
for i in range(len(list)):
    state = list[i]
    state.renderCurrentEnvironment()
    print(state)
    """
