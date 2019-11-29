from enum import Enum
from math import inf
from random import choice
import numpy as np
import collections
import itertools
from basePlayer import BasePlayer
from game import Board
from game import Controller
from game import generateStates
from board import Board
from minimaxPlayer import MinMaxPlayer
from randomPlayer import RandomPlayer
from qlearningPlayer import QLearningPlayer
from humanPlayer import HumanPlayer
from decisionTreePlayer import SVMPlayer
from GeneticAlgorithm import GeneticAlgorithm
from generals import PlayerEnum, load
from generals import State

class Trainer:
    def __init__(self, board, cont):
        self.board = board
        self.cont = cont



""" board = Board(4)
cont = Controller(PlayerEnum.Random, PlayerEnum.QLearningPlayer, board)
cont.training(False, True, 80000)
player2 = cont.player1
player1 = cont.player2
cont.player1 = player1
cont.player2 = player2
cont.training(True, False, 80000)
cont.player1.savePolicy('4x4_80000+80000_round_rotations_random_-1_anyplayer') """
    #cont.player1.loadPolicy("policy_4x4_10000+10000_round_rotations_random_-1_anyplayer")
    #cont.player2.loadPolicy("policy_3x3_100000_round_rotations_random_-1_firstplayer_trial")


def testGame(player1, player2, board, gameNumber):
    cont = Controller(player1, player2, board)

    player1Win = 0
    player2Win = 0
    draw = 0

    for _ in itertools.repeat(None, gameNumber):
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

#Minimax(self, board, depth = 6, heuristic = 4, pruning = True)
#Human(self, board)
#Random(self, board)
#QLearningPlayer(self, board, epszilon = 0.3, alpha = 0.2, gamma = 0.9) még kéne a reward is
#DecisionTree(self, board) egyelőre!!!!
#GeneticAlgoithm(self, board_size, pop_size, generations, parents_number, parents_seletion_mode,
# learnMatch_number, testMatch_number, elitism_num, mutation_num, mutation_prob)
""" b = Board(3)
player1 = QLearningPlayer(b, 0.0) 
player1.states_value = load("policy_4x4_10000+10000_round_rotations_random_-1_anyplayer")
player2 = RandomPlayer(b)
testGame(player1, player2, b, 100) """

ge = GeneticAlgorithm(3, 12, 3, 5, 2, 5000, 100, 2, 3, 18)
print(ge.training())


""" player1Win = 0
player2Win = 0
draw = 0 """
#generateStates(self, player1Type, plyaer2Type, whichPlayerLearn, boardSize, gameNumber)
""" X, Y_Xmoves, Y_Ymoves = generateStates(PlayerEnum.Random, PlayerEnum.Random, 2, 4, 10000)
save("X_random_random_secondplayer_4x4_10000game", X)
save("YX_random_random_secondplayer_4x4_10000game", Y_Xmoves)
save("YY_random_random_secondplayer_4x4_10000game", Y_Ymoves) """


""" print("player1 wins: " + str(player1Win))
print("player2 wins: " + str(player2Win))
print("draws: " + str(draw))
player1Win = 0
player2Win = 0
draw = 0
#cont.player2.loadPolicy("_gdrive_My Drive_policy_10000_round_rotations_minmax_-1_firstplayer")
#cont.player2.loadPolicy("policy_3x3_100000_round_rotations_random_-1_firstplayer_trial")
cont.player2.heuristic = 2
for _ in itertools.repeat(None, 25):
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
player1Win = 0
player2Win = 0
draw = 0
#cont.player2.loadPolicy("_gdrive_My Drive_policy_10000_round_rotations_minmax_-1_firstplayer")
#cont.player2.loadPolicy("policy_3x3_100000_round_rotations_random_-1_firstplayer_trial")
cont.player2.heuristic = 3
for _ in itertools.repeat(None, 25):
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
player1Win = 0
player2Win = 0
draw = 0
#cont.player2.loadPolicy("_gdrive_My Drive_policy_10000_round_rotations_minmax_-1_firstplayer")
#cont.player2.loadPolicy("policy_3x3_100000_round_rotations_random_-1_firstplayer_trial")
cont.player2.heuristic = 4
for _ in itertools.repeat(None, 25):
    winner = cont.trainLoop()
    if winner == cont.player1:
        player1Win = player1Win + 1
    elif winner == cont.player2:
        player2Win = player2Win + 1
    else:
        draw = draw + 1 

print("player1 wins: " + str(player1Win))
print("player2 wins: " + str(player2Win))
print("draws: " + str(draw)) """
#print(cont.player1.states_value)



""" board = Board(3)
cont = Controller(PlayerEnum.QLearningPlayer, PlayerEnum.Random, board)
cont.training(True, False, 200000)
cont.player1.savePolicy('trial') """


""" board = Board(3)
cont = Controller(PlayerEnum.Human, PlayerEnum.MinMax, board)
cont.gameLoop() """



""" board = Board(3)
cont = Controller(PlayerEnum.Human, PlayerEnum.MinMax, board)
board.table[0][0].state = State.X
board.table[0][1].state = State.X
board.table[0][2].state = State.O
board.table[1][0].state = State.O
board.table[2][0].state = State.X

board.print()
cont.player2.heuristic=1
cont.player2.depth=10
cont.player2.move()
board.print() """



    