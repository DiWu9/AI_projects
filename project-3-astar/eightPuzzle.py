from informedSearch import *

class EightPuzzle(InformedProblemState):
    """
    The eight puzzle consists of a three by three board with eight
    numbered tiles and a blank space. A tile adjacent to the blank
    space can slide into the space. The object is to figure out the
    steps needed to get from one configuration of the tiles to
    another.
    """
    def __init__(self, board, operator = None):
        self.board = board
        self.operator = operator
    def __str__(self):
        """
        Required method for use with the Search class.
        Returns a string representation of the state.
        """
        if len(self.board) != 9:
            print("The size of the board is invalid.")
            raise Exception
        result = ""
        if self.operator is not None:
            result += "Operator: " + self.operator + "\n"
        currentPosition = 1
        for number in self.board:
            if number is None:
                result += "  "
            else:
                result += str(number) + " "
            if currentPosition % 3 == 0:
                result += "\n"
            currentPosition += 1
        return result
    def equals(self, puzzleState):
        """
        Required method for use with the Search class.
        Determines whether the state instance and the given
        state are equal.
        """
        return self.board == puzzleState.board
    def dictkey(self):
        """
        Required method for use with the Search class.
        Returns a string that can be used as a ditionary key to
        represent unique states.
        """
        result = ""
        for number in self.board:
            if number is None:
                result += "s"
            else:
                result += str(number)
        return result
    def moveRight(self):
        """move the blank space on the board right"""
        toReturn = self.clone()
        rowOfSpace = toReturn.getPos(None)[0]
        colOfSpace = toReturn.getPos(None)[1]
        if colOfSpace < 3:
            numToSwap = toReturn.getVal((rowOfSpace,colOfSpace+1))
            toReturn.updatePosition((rowOfSpace,colOfSpace+1),None)
            toReturn.updatePosition((rowOfSpace,colOfSpace),numToSwap)
        return toReturn
    def moveLeft(self):
        """move the blank space on the board left"""
        toReturn = self.clone()
        rowOfSpace = toReturn.getPos(None)[0]
        colOfSpace = toReturn.getPos(None)[1]
        if colOfSpace > 1:
            numToSwap = self.getVal((rowOfSpace,colOfSpace-1))
            toReturn.updatePosition((rowOfSpace,colOfSpace-1),None)
            toReturn.updatePosition((rowOfSpace,colOfSpace),numToSwap)
        return toReturn
    def moveUp(self):
        """move the blank space on the board up"""
        toReturn = self.clone()
        rowOfSpace = toReturn.getPos(None)[0]
        colOfSpace = toReturn.getPos(None)[1]
        if rowOfSpace > 1:
            numToSwap = toReturn.getVal((rowOfSpace-1,colOfSpace))
            toReturn.updatePosition((rowOfSpace,colOfSpace),numToSwap)
            toReturn.updatePosition((rowOfSpace-1,colOfSpace),None)
        return toReturn
    def moveDown(self):
        """move the blank space on the board down"""
        toReturn = self.clone()
        rowOfSpace = toReturn.getPos(None)[0]
        colOfSpace = toReturn.getPos(None)[1]
        if rowOfSpace < 3:
            numToSwap = toReturn.getVal((rowOfSpace+1,colOfSpace))
            toReturn.updatePosition((rowOfSpace,colOfSpace),numToSwap)
            toReturn.updatePosition((rowOfSpace+1,colOfSpace),None)
        return toReturn
    def applyOperators(self):
        """
        Required method for use with the Search class.
        Returns a list of valid successors to the current state
        """
        #print("-----")
        #print(self.moveRight())
        #print(self.moveLeft())
        #print(self.moveUp())
        #print(self.moveDown())
        #print("-----")
        return [self.moveRight(),self.moveLeft(),self.moveUp(),self.moveDown()]
    def heuristic(self, goalState):
        """
        estimate the distance from the current 8puzzle state to the goal state
        """
        return self.manhattanDistance(goalState)

    """---helper functions---"""

    def clone(self):
        return EightPuzzle(self.board[:], self.operator)

    def manhattanDistance(self, goalState):
        """
        calculate the sum of manhattan distance of each points from the current
        state to the goal state
        """
        toReturn = 0
        for num in self.board:
            if num != None:
                rowDistance = abs(self.getPos(num)[0]-goalState.getPos(num)[0])
                colDistance = abs(self.getPos(num)[1]-goalState.getPos(num)[1])
                toReturn += rowDistance + colDistance
        return toReturn
    def numTilesOutOfSpace(self, goalState):
        """
        count the number of tiles in which the current number is different from
        the number in the goal state
        """
        count = 0;
        for row in [1,2,3]:
            for col in [1,2,3]:
                if self.getVal((row,col)) != goalState.getVal((row,col)):
                    count += 1
        return count
    def updatePosition(self, position, val):
        """
        update the board by replacing the selected 2D position with val
        position is a tuple (row,col)
        """
        indexToUpdate = self.convertPosToIndex(position)
        self.board[indexToUpdate] = val

    def convertPosToIndex(self, position):
        """covert the 2D position to index of the board list"""
        return (position[0]-1)*3+(position[1]-1)

    def getSpaceIndex(self):
        """get the index position of the blank space"""
        index = 0
        while index < len(self.board):
            if self.board[index] is None:
                return index
            index += 1
        raise Exception("getSpaceIndex: cannot find blank space")

    def getVal(self, position):
        """get the val in position (row, col) of the board"""
        row = position[0]
        col = position[1]
        if row > 3 or col > 3:
            raise Exception("getVal: position out of bound")
        else:
            return self.board[self.convertPosToIndex(position)]

    def getPos(self, val):
        """
        get the 2D position of a value on the 3X3 board
        for example, to get the space postion on the following board:
        1 2 3
        4   6
        7 8 5
        will return the tuple (2,2), representing the blank space
        is at row 2, column 2
        """
        ROW = 3
        COL = 3
        row = 0
        while row < ROW:
            col = 0
            while col < COL:
                if self.board[row*3+col] == val:
                    return (row+1,col+1)
                col += 1
            row += 1
        raise Exception("getPos: cannot the value on the board")


if __name__ == '__main__':
    initialStateA = EightPuzzle([None,1,3,8,2,4,7,6,5])
    initialStateB = EightPuzzle([1,3,4,8,6,2,None,7,5])
    initialStateC = EightPuzzle([1,3,None,4,2,5,8,7,6])
    initialStateD = EightPuzzle([7,1,2,8,None,3,6,5,4])
    initialStateE = EightPuzzle([8,1,2,7,None,4,6,5,3])
    initialStateF = EightPuzzle([2,6,3,4,None,5,1,8,7])
    initialStateG = EightPuzzle([7,3,4,6,1,5,8,None,2])
    initialStateH = EightPuzzle([7,4,5,6,None,3,8,1,2])
#    initialStateI = EightPuzzle([None,1,2,3,4,5,6,7,8])
#    initialStateJ = EightPuzzle([1,2,3,4,5,6,7,8,None])
    goalState = EightPuzzle([1,2,3,8,None,4,7,6,5])
#    print(initialStateA.dictkey())
#    print(initialStateA.equals(initialStateA.clone()))
    #print(initialState1.updatePosition((1,1),1))
    #print(initialState1)
    #print(initialState1.moveUp())
    #print(initialState1.moveDown())
    #print(initialState1.moveRight())
    #print(initialState1.moveLeft())
    print("Test A: ")
    InformedSearch(initialStateA, goalState)
    InformedSearch(initialStateB, goalState)
    print("Test C: ")
    InformedSearch(initialStateC, goalState)
    print("Test D: ")
    InformedSearch(initialStateD, goalState)
    print("Test E: ")
    InformedSearch(initialStateE, goalState)
    print("Test F: ")
    InformedSearch(initialStateF, goalState)
    print("Test G: ")
    InformedSearch(initialStateG, goalState)
    print("Test H: ")
    InformedSearch(initialStateH, goalState)
#    InformedSearch(initialStateI, goalState)
#    InformedSearch(initialStateJ, goalState)
