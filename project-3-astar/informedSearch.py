from pq import *
from search import *

class InformedProblemState(ProblemState):
    """
    An interface class for problem domains.
    """
    def __str__(self):
        """
        Returns a string representing the state.
        """
        abstract()
    def applyOperators(self):
        """
        Returns a list of valid successors to the current state.
        """
        abstract()
    def equals(self, state):
        """
        Tests whether the state instance equals the given state.
        """
        abstract()
    def dictkey(self):
        """
        Returns a string that can be used as a dictionary key to
        represent unique states.
        """
        abstract()
    def heuristic(self, goalState):
        """
        estimate the distance from the current state to the goal state
        """
        abstract()

class InformedNode(Node):
    """
    A Node class to be used in combination with A* search.  A
    node contains a state, a parent node, the depth of the node in
    the search tree, and the goal state.
    The root node should be at depth 0.
    """
    def __init__(self, state, parent, depth, goalState):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.goalState = goalState
    def priority(self):
        """
        calculate the node's f value:
        f = g (cost of path from start to n) + h (estimate cheapest path from n to goal)
        """
        return self.depth + self.state.heuristic(self.goalState)
    def __str__(self):
        result = "\nState: \n" +  str(self.state)
        result += "\nDepth: " + str(self.depth)
        if self.parent != None:
            result += "\nParent: \n" + str(self.parent.state)
        return result

class InformedSearch(Search):
    """
    A general Search class that can be used for any problem domain.
    Given instances of an initial state and a goal state in the
    problem domain, this class will print the solution or a failure
    message.  The problem domain should be based on the ProblemState
    class.
    """
    def __init__(self, initialState, goalState, verbose=False):
        self.q = PriorityQueue()
        self.q.enqueue(InformedNode(initialState, None, 0, goalState))
        self.goalState = goalState
        self.verbose = verbose
        self.visitedStates = dict()
        self.visitedStates.update({initialState.dictkey():initialState})
        solution = self.execute()
        if solution == None:
            print("Search failed")
        else:
            self.showPath(solution)
    def execute(self):
        numNodeExpanded = 0
        while not self.q.empty():
            current = self.q.dequeue()
            numNodeExpanded += 1
            if current.state.heuristic(self.goalState) == 0:
                print("Total Nodes Expanded: ",numNodeExpanded)
                return current
            else:
                successors = current.state.applyOperators()
                numChildren = 0
                for nextState in successors:
                    addable = False
                    stateKey = nextState.dictkey()
                    state = self.visitedStates.get(stateKey,None)
                    if state is None:
                        addable = True
                    else:
                        addable = not state.equals(nextState)
                    if addable:
                        self.visitedStates.update({stateKey:nextState})
                        n = InformedNode(nextState, current, current.depth+1, self.goalState)
                        self.q.enqueue(n)
                        numChildren += 1
                if self.verbose:
                    print("Expanded:", current)
                    print( "Number of successors:", numChildren)
                    print("Total nodes expanded:", numNodeExpanded)
                    print("Queue length:", self.q.size())
                    print("-------------------------------")
        return None
    def inVisitedState(self, toCheck):
        for state in self.visitedStates:
            if toCheck.equals(state):
                return True
        return False
    def showPath(self, node):
        path = self.buildPath(node)
        for current in path:
            print(current.state)
        print("Goal reached in", current.depth, "steps")
    def buildPath(self, node):
        """
        Beginning at the goal node, follow the parent links back
        to the start state.  Create a list of the states traveled
        through during the search from start to finish.
        """
        result = []
        while node != None:
            result.insert(0, node)
            node = node.parent
        return result
