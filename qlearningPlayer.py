from basePlayer import BasePlayer
import itertools
from math import inf
from random import choice
import numpy as np
from generals import State
import pickle

class QLearningPlayer(BasePlayer):
    def __init__(self, sign, type, board, cont, alpha = 0.2, epszilon = 0.3, gamma = 0.9):
        BasePlayer.__init__(self, sign, type, board, cont)
        self.states = []  # record all positions taken
        self.alpha = alpha 
        self.exp_rate = epszilon
        self.decay_gamma = gamma
        self.states_value = {}  # state -> value

    # get unique hash of current board state
    def getHash(self, boardState):
        boardHash = ""
        for k in range(len(boardState)):
            for l in range(len(boardState)):
                boardHash += str(boardState[k][l].state.value)
        return boardHash

    def checkRotations(self, boardState):
        boardStateoriginal = boardState
        i = 0
        for i in range (0, 4):
            boardHash = self.getHash(boardState)
            if self.states_value.get(boardHash) is None:
                boardState = list(zip(*reversed(boardState)))
            else:
                """ print("original")
                print(self.getHash(boardStateoriginal))
                print("rotation wowowowo")
                print(boardHash) """
                return [boardHash, i]
        return [None, None]

    def move(self):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random move
            cells = self.board.empty_cells()
            idx = np.random.choice(len(cells))
            move = cells[idx]
            #print("RANDOMRANDOMRANDOM ")
        else:
            value_max = -inf
            for poss_move in self.board.empty_cells():
                self.board.table[poss_move[0]][poss_move[1]].state = self.sign
                result = self.checkRotations(self.board.table)
                boardHash = result[0]
                rotationNumber = result[1]
                if boardHash is None:
                    value = 0 
                    #print('LOL')
                else: 
                    value = self.states_value.get(boardHash)
                    #print('megtaláltam, value: ' + str(value))
                    #print('board: ' + boardHash)
                """  rotationBoard = [[0 for x in range(self.board.size)] for y in range(self.board.size)]
                    rotationBoard[poss_move[0]][poss_move[1]] = 1
                    #self.board.table[poss_move[0]][poss_move[1]].state = State.EMPTY
                    for i in range(0, rotationNumber):
                        rotationBoard = list(zip(*reversed(rotationBoard)))
                    for i in range(len(rotationBoard)):
                        for j in range(len(rotationBoard[i])):
                            if rotationBoard[i][j] == 1:
                                poss_move[0] = i
                                poss_move[1] = j """
                #print("value", value)
                if value > value_max:
                    #print("v:" + str(value))
                    #print("mv: " + str(value_max))
                    value_max = value
                    move = poss_move
                self.board.table[poss_move[0]][poss_move[1]].state = State.EMPTY
        # print("{} takes action {}".format(self.name, action))
        moved = self.board.move(move[0], move[1], self)
        self.states.append(self.getHash(self.board.table))
        return moved
        

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        #print("states")
        #for k in self.states:
        #    print(k)
        #print("states_values")
        #for k, v in self.states_value.items():
        #    print(k, v)
        #    print("fasz")
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.alpha * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]
        self.states = []

    
    def savePolicy(self, name):
        fw = open('policy_' + name, 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()