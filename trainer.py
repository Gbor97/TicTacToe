from enum import Enum
from math import inf
from random import choice
import numpy as np
import collections
import itertools
from basePlayer import BasePlayer
from game import Board
from game import Controller
from generals import *
from minimaxPlayer import MinMaxPlayer
from randomPlayer import RandomPlayer
from qlearningPlayer import QLearningPlayer
from humanPlayer import HumanPlayer

class Trainer:
    def __init__(self, board, cont):
        self.board = board
        self.cont = cont
        
""" board = Board(4)
cont = Controller(PlayerEnum.Random, PlayerEnum.QLearningPlayer, board)
cont.training(False, True, 10000)
player2 = cont.player1
player1 = cont.player2
cont.player1 = player1
cont.player2 = player2
cont.training(True, False, 100000)
cont.player1.savePolicy('4x4_100000+100000_round_rotations_random_-1_anyplayer') """

board = Board(4)
cont = Controller(PlayerEnum.Random, PlayerEnum.MinMax, board)
player1Win = 0
player2Win = 0
draw = 0
#cont.player1.loadPolicy("_gdrive_My Drive_policy_10000_round_rotations_minmax_-1_firstplayer")
#cont.player1.loadPolicy("policy_3x3_100000_round_rotations_random_-1_firstplayer_trial")
for _ in itertools.repeat(None, 10):
    winner = cont.trainLoop()
    if winner == cont.player1:
        player1Win = player1Win + 1
    elif winner == cont.player2:
        player2Win = player2Win + 1
    else:
        draw = draw + 1 

print("player1 wins: " + str(player1Win))
print("player2 wins: " + str(player2Win))
print("draws: " + str(draw))
#print(cont.player1.states_value)



""" board = Board(3)
cont = Controller(PlayerEnum.QLearningPlayer, PlayerEnum.Random, board)
cont.training(True, False, 200000)
cont.player1.savePolicy('trial') """


""" board = Board(4)
cont = Controller(PlayerEnum.Human, PlayerEnum.MinMax, board)
cont.gameLoop() """



""" board = Board(4)
cont = Controller(PlayerEnum.Human, PlayerEnum.MinMax, board)
board.table[0][0].state = State.O
board.table[1][1].state = State.X
board.table[1][3].state = State.X
board.table[1][0].state = State.O
print(cont.player2.heuristic4(0, [1,0]))

board.print()
board.table[1][0].state = State.EMPTY
board.table[0][1].state = State.O
print(cont.player2.heuristic4(0, [0,1]))

board.print()
board.table[0][1].state = State.EMPTY """

    