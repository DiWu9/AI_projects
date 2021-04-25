from updatedKonane import *
import math


class MinimaxNode:
    """
    Black always goes first and is considered the maximizer.
    White always goes second and is considered the minimizer.
    In the file minimax.py, implement a MinimaxNode class to hold the necessary
    information for a search node in a minimax game tree. It should include the
    following data:
        state: the current board configuration
        operator: the move that resulted in the current board configuration
        depth: the depth of the node in the search tree
        player: maximizer or minimizer
    """
    def __init__(self, state, operator, depth, player):
        self.state = state
        self.operator = operator
        self.depth = depth
        self.player = player

    def equals(self, minimaxNode):
        if self.state == minimaxNode.state:
            if self.player == self.player:
                if self.depth == self.depth:
                    return True
        return False

    """getters"""
    def getDepth(self):
        return self.depth

    def getState(self):
        return self.state

    def getPlayer(self):
        return self.player

    def getOperator(self):
        return self.operator

class MinimaxPlayer(Konane, Player):
    """
    In the file minimax.py, implement a MinimaxPlayer class that inherits from
    both thePlayer class and the Konane. Your class must override the abstract
    methods initialize and getMove from the Player class. It should also implement
    several other methods, which are described in the file.

    Notice that the first line of the MinimaxPlayer constructor calls the
    constructor of the Konane base class. Also notice that the depth limit for
    the search is passed in as an argument to the class. Therefore you will not
    need to pass it as an argument to the minimax method. You should be able to
    use your MinimaxPlayer in the following way:

    game = Konane(8)
    game.playNGames(2, MinimaxPlayer(8, 2), MinimaxPlayer(8, 1), False)
    Executing the above commands should demonstrate that the minimax player
    which searches to depth 2 will outperform a minimax player which only
    searches to depth 1.
    Game 0
    MinimaxDepth2 wins
    Game 1
    MinimaxDepth2 wins
    MinimaxDepth2 2 MinimaxDepth1 0
    """

    def __init__(self, size, depthLimit):
        Konane.__init__(self, size)
        Player.__init__(self)
        self.limit = depthLimit

    def initialize(self, side):
        """
        Initializes the player's color and name.
        """
        self.side = side
        self.name = "MinimaxDepth_" + str(self.limit) + "_Woody"

    def getMove(self, board):
        """
        Returns the chosen move based on doing an alphaBetaMinimax search.
        """
        rootNode = MinimaxNode(board, None, 0, self.side)
        return self.alphaBetaMinimax(rootNode, -math.inf, math.inf)

    def staticEval(self, node):
        """
        Returns an estimate of the value of the state associated
        with the given node.

        Implement an appropriate static evaluator for Konane. The key difference
        between Konane players will be in how they evaluate boards. Based on our
        reading, the static evaluator should:

            Order the end states correctly
            Be time efficient to compute
            Be strongly correlated with the actual chances of winning

        features to consider:
            1. number difference
            2. moveable directions (0-4)
            3. number of chess that can move
        """
        score = 0
        board = node.getState()
        for i in range(self.size):
            for j in range(self.size):
                selectedSide = board[i][j]
                if selectedSide == "B":
                    score += self.evaluatePosition(board, i, j)
                elif selectedSide == "W":
                    score -= self.evaluatePosition(board, i, j)
        return score

    def evaluatePosition(self, board, r, c):
        """
        evaluate a position by checking if the select position can make moves
        """
        f1 = 4
        f2 = 1
        f3 = 1
        moveable = 0
        numMoves = 0
        if board[r][c] == "B":
            numMoves = self.countMoves(board, r, c, "W")
            if numMoves > 0:
                moveable = 1
        elif board[r][c] == "W":
            numMoves = self.countMoves(board, r, c, "B")
            if numMoves > 0:
                moveable = 1
        return f1*moveable + f2*numMoves + f3

    def countMoves(self, board, r, c, opponent):
        """
        count how many moveable directions can the chess in position [r,c] have
        """
        count = 0
        if self.moveable(board, r, c, 1, 0, 1, opponent):
            count += 1
        if self.moveable(board, r, c, -1, 0, 1, opponent):
            count += 1
        if self.moveable(board, r, c, 0, 1, 1, opponent):
            count += 1
        if self.moveable(board, r, c, 0, -1, 1, opponent):
            count += 1
        return count

    def moveable(self, board, r, c, rd, cd, factor, opponent):
        """
        check whether a jump is possible starting at (r,c) and going in
        the direction determined by the row dela and column delta.
        it is different from check because it does not detect multiple jumps.
        """
        return self.contains(board,r+factor*rd,c+factor*cd,opponent) and \
           self.contains(board,r+(factor+1)*rd,c+(factor+1)*cd,'.')


    def successors(self, node):
        """
        Returns a list of the successor nodes for the given node.
        """
        toReturn = []
        currentBoard = node.getState()
        moves = self.generateMoves(currentBoard, node.getPlayer())
        for move in moves:
            r1 = move[0]
            c1 = move[1]
            r2 = move[2]
            c2 = move[3]
            if (self.valid(r1, c1) and self.valid(r2, c2)):
                nextState = self.nextBoard(currentBoard, node.getPlayer(), move)
                childNode = MinimaxNode(nextState, move, node.getDepth() + 1,
                self.opponent(node.getPlayer()))
                toReturn.append(childNode)
        return toReturn


    def alphaBetaMinimax(self, node, alpha, beta):
        """
        Returns the best score for the player associated with the
        given node.  Also sets the instance variable bestMove to the
        move associated with the best score at the root node.
        Initialize alpha to -infinity and beta to +infinity.

        return the best move
        """
        children = self.successors(node)
        if len(children) == 0:
            return []
        moveValDict = {}
        if self.side == "B":
            bestVal = -math.inf
            for child in children:
                val = self.helperAlphaBetaMinimax(child, -math.inf, math.inf)
                moveValDict[val] = child.getOperator()
                bestVal = max(bestVal, val)
        else:
            bestVal = math.inf
            for child in children:
                val = self.helperAlphaBetaMinimax(child, -math.inf, math.inf)
                moveValDict[val] = child.getOperator()
                bestVal = min(bestVal, val)
        return moveValDict[bestVal]

    def helperAlphaBetaMinimax(self, node, alpha, beta):
        children = self.successors(node)

        # if reaches the maximum depth
        if node.getDepth() >= self.limit:
            return self.staticEval(node)

        # if reaches a leaf node
        if len(children) == 0:
            return self.staticEval(node)

        # if it's black's role (maximizer's row)
        if node.getPlayer() == 'B':
            bestVal = -math.inf
            for child in children:
                val = self.helperAlphaBetaMinimax(child, alpha, beta)
                if bestVal < val:
                    bestVal = val
                alpha = max(alpha, bestVal)
                if beta <= alpha:
                    break
            return bestVal

        # if it's white's role (minimizer's role)
        else:
            bestVal = math.inf
            for child in children:
                val = self.helperAlphaBetaMinimax(child, alpha, beta)
                if val < bestVal:
                    bestVal = val
                beta = min(beta,bestVal)
                if beta <= alpha:
                    break
            return bestVal


if __name__ == '__main__':
    player = MinimaxPlayer(8,2)
