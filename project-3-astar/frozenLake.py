from informedSearch import *
import gym
from gym.envs.classic_control import rendering

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

GOAL_ROW = 4
GOAL_COL = 4

class FrozenLake(InformedProblemState):
    """
    The eight puzzle consists of a three by three board with eight
    numbered tiles and a blank space. A tile adjacent to the blank
    space can slide into the space. The object is to figure out the
    steps needed to get from one configuration of the tiles to
    another.
    """
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
            to_return = FrozenLake(self.environment, new_state, reward, "up")
        return to_return

    def goDown(self):
        current_state = self.state
        if current_state in [1,3,8]:
            return None
        else:
            new_environment = self.cloneEnv()
            new_state,reward,done,info = new_environment.step(DOWN)
            to_return = FrozenLake(self.environment, new_state, reward, "down")
        return to_return

    def goLeft(self):
        current_state = self.state
        if current_state in [6,13]:
            return None
        else:
            new_environment = self.cloneEnv()
            new_state,reward,done,info = new_environment.step(LEFT)
            to_return = FrozenLake(self.environment, new_state, reward, "left")
        return to_return

    def goRight(self):
        current_state = self.state
        if current_state in [4,6,10]:
            return None
        else:
            new_environment = self.cloneEnv()
            new_state,reward,done,info = new_environment.step(RIGHT)
            to_return = FrozenLake(new_environment, new_state, reward, "right")
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

    def heuristic(self, goalState):
        """
        estimate the distance from the current 8puzzle state to the goal state
        """
        return self.manhattanDistance(GOAL_ROW, GOAL_COL)

    """---helper functions---"""
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

    def manhattanDistance(self, goal_row, goal_col):
        """
        calculate the sum of manhattan distance of each points from the current
        state to the goal state
        """
        current_state = self.state
        ith_row = current_state // 4 + 1
        ith_col = current_state % 4 + 1
        diff_row = abs(goal_row - ith_row)
        diff_col = abs(goal_col - ith_col)
        return diff_row + diff_col

    def renderCurrentEnvironment(self):
        self.environment.render()


if __name__ == '__main__':
    frozenLake = gym.make("FrozenLake-v0", is_slippery = False)
    frozenLake.reset()
    initialState = FrozenLake(frozenLake, 0, 0)
    goalState = FrozenLake(frozenLake, 15, 1)
    InformedSearch(initialState, goalState)
