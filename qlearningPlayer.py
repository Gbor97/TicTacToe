import itertools
from math import inf
from random import choice
import numpy as np
import pickle

from basePlayer import BasePlayer
from generals import State
from generals import getRivalSign
from board import Board
from board import Cell

class QLearningPlayer(BasePlayer):
    def __init__(self, board, epszilon = 0.3, alpha = 0.2, gamma = 0.9):
        BasePlayer.__init__(self, board)
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
        for _ in itertools.repeat(None, 4):
            boardHash = self.getHash(boardState)
            if self.states_value.get(boardHash) is None:
                boardState = list(zip(*reversed(boardState)))
            else:
                return boardHash
        return None

    def move(self):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random move
            cells = self.board.empty_cells()
            idx = np.random.choice(len(cells))
            move = cells[idx]
        else:
            value_max = -inf
            for poss_move in self.board.empty_cells():
                self.board.table[poss_move[0]][poss_move[1]].state = self.sign
                result = self.checkRotations(self.board.table)
                boardHash = result
                if boardHash is None:
                    value = 0 
                else: 
                    value = self.states_value.get(boardHash)
                if value > value_max:
                    value_max = value
                    move = poss_move
                self.board.table[poss_move[0]][poss_move[1]].state = State.EMPTY
        moved = self.board.move(move[0], move[1], self)
        self.states.append(self.getHash(self.board.table))
        return moved

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        states_rev = self.states[::-1]
        for i in range(len(self.states)):
            st = states_rev[i]
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            if i != len(self.states) - 1:
                st_before_hash = states_rev[i+1]
                st_before = self.getBoardStateFromHash(st_before_hash)
                b = Board(self.board.size)
                b.table = st_before
            else:
                b = Board(self.board.size)
            possible_q_values = []
            for poss_move in b.empty_cells():
                b.table[poss_move[0]][poss_move[1]].state = self.rival_sign
                possible_boardState_hash = self.getHash(b.table)
                value = self.states_value.get(possible_boardState_hash)
                if value != None:
                  possible_q_values.append(value)
                else:
                  possible_q_values.append(0)
            possible_q_value = max(possible_q_values)
            self.states_value[st] = (1 - self.alpha) * self.states_value[st] + self.alpha * (reward + self.decay_gamma *  possible_q_value)
            #reward = self.states_value[st]
        self.states = []

    def getBoardStateFromHash(self, boardStateHash):
        boardState = []
        for i in range(self.board.size):
            row = []
            for j in range(self.board.size):
                if int(boardStateHash[i * self.board.size + j]) == 0:
                    row.append(Cell(State.EMPTY))
                elif int(boardStateHash[i * self.board.size + j]) == 1:
                    row.append(Cell(State.X))
                else: row.append(Cell(State.O))
            boardState.append(row)
        return boardState