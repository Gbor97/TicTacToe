from enum import Enum
from math import inf
from random import choice
import numpy as np
import collections
import itertools

from basePlayer import BasePlayer
from generals import State
from generals import getHash
from generals import transfromBoardState5
from generals import PlayerEnum
from board import Board
from minimaxPlayer import MinMaxPlayer
from randomPlayer import RandomPlayer
from qlearningPlayer import QLearningPlayer
from humanPlayer import HumanPlayer
from decisionTreePlayer import SVMPlayer




class Controller:
    def __init__(self, player1, player2, board):
        self.player1 = player1
        self.player1.setSign(True)
        self.player2 = player2
        self.player2.setSign(False)
        self.board = board 

    def trainLoop(self):
        while self.board.freeCellCheck():
            win = False
            move = self.player1.move()
            if self.board.checkWin(self.player1.sign, move):
                win = True
                self.board.reset()
                return self.player1
            if not self.board.freeCellCheck():
                break
            move = self.player2.move()
            if self.board.checkWin(self.player2.sign, move):
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
            if self.board.checkWin(self.player1.sign, move):
                self.board.print()
                print('*** Congratulations ! Player1 won ! ***')
                win = True
                return self.player1
            self.board.print()
            if not self.board.freeCellCheck():
                break
            print('Player2')
            move = self.player2.move()
            if self.board.checkWin(self.player2.sign, move):
                self.board.print()
                print('*** Congratulations ! Player2 won ! ***')
                win = True
                return self.player2
        if not win:
            self.board.print()
            print('*** DRAW ***')
            return None 

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

def generateStates(player1Type, plyaer2Type, whichPlayerLearn, boardSize, gameNumber):
    board = Board(boardSize)
    cont = Controller(player1Type, plyaer2Type, board)
    boardStates = []
    boardStatesTotal = []
    winner = -1
    for _ in itertools.repeat(None, gameNumber):
        end = False
        number_of_appends = 0
        while board.freeCellCheck():
            win = False
            #save the boardState before the move
            boardState = transfromBoardState5(getHash(board.table))
            move = cont.player1.move()
            if whichPlayerLearn == 1:
                if boardState not in boardStates:
                    boardState.append(move[0])
                    boardState.append(move[1])
                    boardStates.append(boardState)
                    number_of_appends = number_of_appends + 1
            if board.checkWin(cont.player1.sign, move):
                win = True
                end = True
                winner = 1
                board.reset()
                break
            if not board.freeCellCheck():
                break
            boardState = transfromBoardState5(getHash(board.table))
            move = cont.player2.move()
            if whichPlayerLearn == 2:
                if boardState not in boardStates:
                    boardState.append(move[0])
                    boardState.append(move[1])
                    boardStates.append(boardState)
                    number_of_appends = number_of_appends + 1
            if board.checkWin(cont.player2.sign, move):
                win = True
                end = True
                winner = 2
                board.reset()
                break
        if not win:
            board.reset()
            end = True
            winner = 0
        if end:
            if winner == whichPlayerLearn:    
                boardStatesTotal = boardStatesTotal + boardStates
            boardStates = []
    #the last move is the winnig move, it is not necessary
    del boardStatesTotal[-1]
    #becouse wu use transfromBoardState5 -> one cell represented by 2 value (which sign there)
    Matrix = np.matrix(boardStatesTotal)
    Y_Xmoves = Matrix[:,2*boardSize*boardSize]
    Y_Ymoves = Matrix[:,2*boardSize*boardSize+1]
    Matrix = np.delete(Matrix, 2*boardSize*boardSize+1, 1)
    X = np.delete(Matrix, 2*boardSize*boardSize, 1)
    return [X, Y_Xmoves, Y_Ymoves]
    


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
