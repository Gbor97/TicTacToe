from enum import Enum
from math import inf
from random import choice
import numpy as np
import collections
import itertools
from basePlayer import BasePlayer
from generals import *
from minimaxPlayer import MinMaxPlayer
from randomPlayer import RandomPlayer
from qlearningPlayer import QLearningPlayer
from humanPlayer import HumanPlayer


class Cell:
    def __init__(self):
        self.state = State.EMPTY
    

    def isFree(self):
        if (self.state == State.EMPTY):
            return True
        else:
            return False

class Board:
    def __init__(self, size):
        self.size = size
        self.table = [[Cell() for x in range(size)] for y in range(size)] 

    def validateMove(self, moveX, moveY):
        if (moveX < self.size) and (moveY < self.size) and (self.table[moveX][moveY].isFree()):
            return True
        return False

    def move(self, moveX, moveY, player):
        self.table[moveX][moveY].state = player.sign
        return [moveX, moveY]

    def freeCellCheck(self):
        free = False
        for i in range(self.size):
            for j in range(self.size):
                if self.table[i][j].state == State.EMPTY:
                    free = True
                    break
        return free

    def empty_cells(self):
        cells = []
        for row in range(self.size):
            for column in range(self.size):
                if self.table[row][column].state == State.EMPTY:
                    cells.append([row, column])
        return cells

    def reset(self):
        for i in range(self.size):
            for j in range(self.size):
                self.table[i][j].state = State.EMPTY

    def print(self):
        for i in range(self.size):
            for _ in itertools.repeat(None, self.size):
                print("----",end = '')
            print()
            for j in range(self.size):
                print(self.table[i][j].state.value, end = '')
                print(" | ", end = '')
            print()

class Controller:
    def __init__(self, playerType1, playerType2, board):
        if playerType1==PlayerEnum.Human:
            self.player1 = HumanPlayer(State.X, 1, board, self)
        elif playerType1==PlayerEnum.MinMax:
            self.player1 = MinMaxPlayer(State.X, 2, board, self)
        elif playerType1==PlayerEnum.QLearningPlayer:
            self.player1 = QLearningPlayer(State.X, 3, board, self)
        elif playerType1==PlayerEnum.Random:
            self.player1 = RandomPlayer(State.X, 4, board, self)
        if playerType2==PlayerEnum.Human:
            self.player2 = HumanPlayer(State.O, 1, board, self)
        elif playerType2==PlayerEnum.MinMax:
            self.player2 = MinMaxPlayer(State.O, 3, board, self)  
        elif playerType2==PlayerEnum.QLearningPlayer:
            self.player2 = QLearningPlayer(State.O, 3, board, self) 
        elif playerType2==PlayerEnum.Random:
            self.player2 = RandomPlayer(State.O, 4, board, self)
        self.board = board 
         
        ##else...

    def trainLoop(self):
        while self.board.freeCellCheck():
            win = False
            move = self.player1.move()
            if self.checkWin(self.player1.sign, move):
                win = True
                self.board.reset()
                return self.player1
            if not self.board.freeCellCheck():
                break
            move = self.player2.move()
            if self.checkWin(self.player2.sign, move):
                win = True
                self.board.reset()
                return self.player2
        if not win:
            self.board.reset()
            return None
        

    def gameLoop(self):
        while self.board.freeCellCheck():
            win = False
            self.board.print()
            print('Player1')
            move = self.player1.move()
            if self.checkWin(self.player1.sign, move):
                self.board.print()
                print('*** Congratulations ! Player1 won ! ***')
                win = True
                return self.player1
            self.board.print()
            if not self.board.freeCellCheck():
                break
            print('Player2')
            move = self.player2.move()
            if self.checkWin(self.player2.sign, move):
                self.board.print()
                print('*** Congratulations ! Player2 won ! ***')
                win = True
                return self.player2
        if not win:
            self.board.print()
            print('*** DRAW ***')
            return None 

    def make_win_states(self, move):
        win_states = []
        #row
        win_state = []
        for column in range(self.board.size):
            win_state.append(self.board.table[move[0]][column].state)
        win_states.append(win_state) 
        #column
        win_state = []
        for row in range(self.board.size):
            win_state.append(self.board.table[row][move[1]].state)
        win_states.append(win_state)
        """ for row in range(board.size):
            win_state = []
            for column in range(board.size):
                win_state.append(board.table[row][column].state)
            win_states.append(win_state)
        #columns
        for column in range(board.size):
            win_state = []
            for row in range(board.size):
                win_state.append(board.table[row][column].state)
            win_states.append(win_state) """
        #diagonal from left to right
        win_state = []
        for row in range(self.board.size):
                win_state.append(self.board.table[row][row].state)
        win_states.append(win_state)
        #diagonal from right to left
        win_state = []
        for row in range(self.board.size):
                win_state.append(self.board.table[row][self.board.size - 1 - row].state)
        win_states.append(win_state)
        return win_states

    def checkWin(self, sign, move):
        win_states = self.make_win_states(move)
        state = []
        for _ in itertools.repeat(None, self.board.size):
            state.append(sign)
        return state in win_states

    def training(self, player1Learning = False, player2Learning = False, rounds=10000):
        for i in range(rounds):
            if i % 1000 == 0:
                print("Rounds {}".format(i))
            winner = self.trainLoop()
            if player1Learning:
              if winner == self.player1:
                self.player1.feedReward(1) #win
              elif winner == None:
                self.player1.feedReward(0.3) #draw
              else:
                self.player1.feedReward(0) #lose
            if player2Learning:
              if winner == self.player2:
                self.player2.feedReward(1) #win
              elif winner == None:
                self.player2.feedReward(0.3) #draw
              else:
                self.player2.feedReward(0) #lose
            self.board.reset()



print('Wellcome bitten2')
""" boardSize = 0
while boardSize == 0:
    boardSize = getInput('Board size: ')
board = Board(boardSize)
cont = Controller(PlayerEnum.Human, PlayerEnum.QLearningPlayer, board)
cont.player2.loadPolicy("_gdrive_My Drive_policy_100000_round_rotations_random_-1")
cont.gameLoop()
print("states_values")
print(len(cont.player2.states_value)) """
#for k, v in cont.player2.states_value.items():
#            print(k, v)
