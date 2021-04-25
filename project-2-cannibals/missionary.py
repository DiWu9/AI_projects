### File: missionary.py
### Implements the missionaries and cannibals problem for state
### space search

from improvedSearch import *
import gym

from gym.envs.classic_control import rendering

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

class MissionaryState(ProblemState):
    """
    Missionaries and Cannibals puzzle: Three missionaries and three cannibals are
    on one side of the river. The goal is to get everyone to the other side of the
    river without leaving any side of the river having more missionaries than cannibals.
    """

    def __init__(self, start, end, operator = None):
        """
        start: the side initially has three missionaries and three cannibals
        end: the side everyone have to get to
        operator: possible move to transit from current state to its child
        """
        self.start = start
        self.end = end
        self.operator = operator

    def __str__(self):
        """
        return a string representation of the state class
        """
        result = ""
        if self.operator is not None:
            result = "Operator: " + self.operator + "\n"
        result += self.dictkey() + "\n"
        return result

    def equals(self, state):
        """
        check if two states are equals
        """
        return self.start == state.start and self.end == state.end and self.boatLocation() == state.boatLocation()

    def dictkey(self):
        """
        convert the state object to a string that can be used as a dictionary
        key to represent unique state (e.g. the initial state can be represented
        as "3M3C,0M0C")
        """
        return self.start + "," + self.end

    def countMissionaryOnStart(self):
        return int(self.start[0])

    def countMissionaryOnEnd(self):
        return int(self.end[0])

    def countCannibalOnStart(self):
        return int(self.start[2])

    def countCannibalOnEnd(self):
        return int(self.end[2])

    def isValidState(self):
        """
        to check if the state is valid, which is: none of two sides of the river having
        more missionaries than cannibals, or there is no cannibals on the side
        """
        if self.countCannibalOnStart() == 0 or self.countCannibalOnEnd() == 0:
            return True
        else:
            return not (self.countMissionaryOnStart() > self.countCannibalOnStart() or self.countMissionaryOnEnd() > self.countCannibalOnEnd())

    def boatLocation(self):
        """
        find the location of the boat on current state
        1 means the boat is on the destination side
        0 means the boat is on the start side
        """
        if self.operator is None:
            return 0
        else:
            if self.operator[0] == 's':
                return 1
            elif self.operator[0] == 'b':
                return 0
            else:
                return -1

    def sendTwoM(self):
        """send two missionaries to destination (end side)"""
        startM = self.countMissionaryOnStart()
        if startM < 2:
            return None
        else:
            newStart = str(startM-2) + self.start[1:]
            newEnd = str(5-startM) + self.end[1:]
            return MissionaryState(newStart,newEnd,"sendTwoM")
    def sendTwoC(self):
        """send two cannibals to destination"""
        startC = self.countCannibalOnStart()
        if startC < 2:
            return None
        else:
            newStart = self.start[0:2] + str(startC-2) + self.start[3]
            newEnd = self.end[0:2] + str(5-startC) + self.end[3]
            return MissionaryState(newStart,newEnd,"sendTwoC")
    def sendMC(self):
        """send a cannibal and a missionary to destination"""
        startM = self.countMissionaryOnStart()
        startC = self.countCannibalOnStart()
        if startM < 1 or startC < 1:
            return None
        else:
            newStart = str(startM-1) + "M" + str(startC-1) + "C"
            newEnd = str(4-startM) + "M" + str(4-startC) + "C"
            return MissionaryState(newStart, newEnd, "sendMC")
    def sendM(self):
        """send a missionary to destination"""
        startM = self.countMissionaryOnStart()
        if startM < 1:
            return None
        else:
            newStart = str(startM-1) + self.start[1:]
            newEnd = str(4-startM) + self.end[1:]
            return MissionaryState(newStart,newEnd,"sendM")
    def sendC(self):
        """send a cannibal to destination"""
        startC = self.countCannibalOnStart()
        if startC < 1:
            return None
        else:
            newStart = self.start[0:2] + str(startC-1) + self.start[3]
            newEnd = self.end[0:2] + str(4-startC) + self.end[3]
            return MissionaryState(newStart, newEnd, "sendC")
    def bringTwoM(self):
        """bring two missionaries back to start"""
        endM = self.countMissionaryOnEnd()
        if endM < 2:
            return None
        else:
            newStart = str(5-endM) + self.start[1:]
            newEnd = str(endM-2) + self.end[1:]
            return MissionaryState(newStart,newEnd,"bringTwoM")
    def bringTwoC(self):
        """bring two cannibals back to start"""
        endC = self.countCannibalOnEnd()
        if endC < 2:
            return None
        else:
            newStart = self.start[0:2] + str(5-endC) + self.start[3]
            newEnd = self.end[0:2] + str(endC-2) + self.end[3]
            return MissionaryState(newStart,newEnd,"bringTwoC")
    def bringMC(self):
        """bring a missionary and a cannibal back to start"""
        endM = self.countMissionaryOnEnd()
        endC = self.countCannibalOnEnd()
        if endM < 1 or endC < 1:
            return None
        else:
            newStart = str(4-endM) + "M" + str(4-endC) + "C"
            newEnd = str(endM-1) + "M" + str(endC-1) + "C"
            return MissionaryState(newStart, newEnd, "bringMC")
    def bringM(self):
        """bring a missionary back to start"""
        endM = self.countMissionaryOnEnd()
        if endM < 1:
            return None
        else:
            newStart = str(4-endM) + self.start[1:]
            newEnd = str(endM-1) + self.end[1:]
            return MissionaryState(newStart,newEnd,"bringM")
    def bringC(self):
        """bring a cannibal back to start"""
        endC = self.countCannibalOnEnd()
        if endC < 1:
            return None
        else:
            newStart = self.start[0:2] + str(4-endC) + self.start[3]
            newEnd = self.end[0:2] + str(endC-1) + self.end[3]
            return MissionaryState(newStart,newEnd,"bringC")

    def applyOperators(self):
        """
        Required method for use with the Search class.
        Returns a list of valid successors to the current state
        """
        sendList = [self.sendTwoM, self.sendTwoC, self.sendMC, self.sendM, self.sendC]
        bringList = [self.bringTwoM, self.bringTwoC, self.bringMC, self.bringM, self.bringC]
        result = []
        if self.boatLocation() == 1: # now boat is on destination side
            for operation in bringList:
                toAdd = operation()
                if toAdd is not None and toAdd.isValidState():
                    result.append(toAdd)
        elif self.boatLocation() == 0: #now boat is on start side
            for operation in sendList:
                toAdd = operation()
                if toAdd is not None and toAdd.isValidState():
                    result.append(toAdd)
        else:
            raise Exception
        return result

#initialState = MissionaryState("3M3C","0M0C")
#print(initialState.sendTwoC(),initialState.sendTwoC(),initialState.sendTwoC())
Search(MissionaryState("3M3C","0M0C"),MissionaryState("0M0C","3M3C","send"),True)
