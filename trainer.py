from enum import Enum
from math import inf
from random import choice
import numpy as np
import collections
import itertools

from basePlayer import BasePlayer
from controller import Controller
from board import Board
from minimaxPlayer import MiniMaxPlayer
from randomPlayer import RandomPlayer
from qlearningPlayer import QLearningPlayer
from humanPlayer import HumanPlayer
from randomForestClassifierPlayer import RandomForestClassifierPlayer, OneHotEncoding2, getHash
from geneticAlgorithm import GeneticAlgorithm
from generals import State, load, save


class Trainer:

    def trainingQLearningPlayer(self, player1, player2, boardSize, epszilon_strategy = 0, rounds=10000):
        board = Board(boardSize)
        cont = Controller(player1, player2, board) 
        for i in range(rounds):
            if i % 1000 == 0:
                print("Rounds {}".format(i))
            if epszilon_strategy == 1:
                if player1.name == "QLearningPlayer":
                    player1.exp_rate = self.epszilonFirst(rounds, i)
                if player2.name == "QLearningPlayer":
                    player2.exp_rate = self.epszilonFirst(rounds, i)
            if epszilon_strategy == 2:
                if player1.name == "QLearningPlayer":
                    player1.exp_rate = self.epszilonDecreasing(rounds)
                if player2.name == "QLearningPlayer":
                    player2.exp_rate = self.epszilonDecreasing(rounds)
            winner = cont.trainLoop()
            if player1.name == "QLearningPlayer":
              if winner == cont.player1:
                cont.player1.feedReward(1) #win
              elif winner == None:
                cont.player1.feedReward(0) #draw
              else:
                cont.player1.feedReward(-1) #lose
            if player2.name == "QLearningPlayer":
              if winner == cont.player2:
                cont.player2.feedReward(1) #win
              elif winner == None:
                cont.player2.feedReward(0) #draw
              else:
                cont.player2.feedReward(-1) #lose
            cont.board.reset()

    def epszilonFirst(self, rounds, actual_round):
        if actual_round <= rounds / 2:
            return 1
        else:
            return 0

    def epszilonDecreasing(self, rounds):
        return 1/rounds

    def saveQlearningModel(self, boardSize, rounds, player1, player2):
        if player1.name == "QLearningPlayer":
            save("policy_" + str(boardSize) + "x" + str(boardSize) + "_" + str(rounds) + "_round_against_"
                + player2.name + "_firstplayer", player1.states_value)
        if player2.name == "QLearningPlayer":
            save("policy_" + str(boardSize) + "x" + str(boardSize) + "_" + str(rounds) + "_round_against_"
                + player1.name + "_secondplayer", player2.states_value)

    def generateStates(self, player1Type, plyaer2Type, whichPlayerLearn, boardSize, gameNumber):
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
                boardState = OneHotEncoding2(getHash(board.table))
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
                boardState = OneHotEncoding2(getHash(board.table))
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

    def trainingClassifierPlayer(self, X_file, Y_Xmoves_file, Y_Ymoves_file, start_player,
                                 boardSize, classifier_num = 1):
        b = Board(boardSize)
        X = load(X_file)
        Y_Xmoves = load(Y_Xmoves_file)
        Y_Ymoves = load(Y_Ymoves_file)
        if start_player:
            player1 = RandomForestClassifierPlayer(None, None, X, Y_Xmoves, Y_Ymoves, classifier_num)
            player2 = RandomPlayer()
            testGame(player1, player2, b, 1000)
            print("saving...")
            player1.saveModels()
            print("saved")
        else:
            player2 = RandomForestClassifierPlayer(None, None, X, Y_Xmoves, Y_Ymoves, classifier_num)
            player1 = RandomPlayer()
            testGame(player1, player2, b, 1000)
            print("saving...")
            player2.saveModels()
            print("saved")
        
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

    if player1.name == "QLearningPlayer":
        player1.exp_rate = 0.0
    if player2.name == "QLearningPlayer":
        player2.exp_rate = 0.0

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

#Minimax(self, depth = 6, heuristic = 4, pruning = True)
#Human(self)
#Random(self)
#QLearningPlayer(self, learning_file = None, alpha = 0.2, epszilon = 0.3, gamma = 0.9, 
                    #win_reward = 1, draw_reward = 0.3, lose_reward = 0) 
#DecisionTree(self, clf_x, clf_y, X = [], Y_Xmoves = [], Y_Ymoves = [], classifier_num = 1)
#GeneticAlgoithm(self, board_size, start_player, other_player, pop_size, generations, 
                    #parents_number, parents_seletion_mode, learnMatch_number, testMatch_number, 
                    #elitism_num, mutation_num, mutation_prob)


def testAllPlayer():
    #3x3 méretű pályától 6x6 méretű pályáig tesztel
    for i in range(3,6):
        b = Board(i)
        player1list = [MiniMaxPlayer(),
                       RandomPlayer(), 
                       QLearningPlayer("policy_" + str(i) + "x" + str(i) + "_100000_round_against_RandomPlayer_firstplayer"), 
                       QLearningPlayer(), 
                       RandomForestClassifierPlayer("DTC_" + str(i) + "x" + str(i) + "_firstplayer_X", "DTC_" + str(i) + "x" + str(i) + "_firstplayer_Y")]
        player2list = [MiniMaxPlayer(),
                       RandomPlayer(),
                       QLearningPlayer(), 
                       QLearningPlayer(),
                       RandomForestClassifierPlayer("DTC_" + str(i) + "x" + str(i) + "_secondplayer_X", "DTC_" + str(i) + "x" + str(i) + "_secondplayer_Y")]
        for player1 in player1list:
            for player2 in player2list:
                print("board_size: " + str(i))
                print("player1: " + str(player1.name))
                print("player2: " + str(player2.name))
                testGame(player1, player2, b, 100)
                print()


""" b = Board(3)
player2 = SVMPlayer() 
player1 = RandomPlayer() """
""" ge = GeneticAlgorithm(3, 14, 6, 5, 1, 30000, 100, 2, 3, 17)
parameters = ge.training()
print(parameters)
player1.alpha = parameters[0][0]
player1.exp_rate = parameters[0][1]
player1.decay_gamma = parameters[0][2] """

""" X, Y_Xmoves, Y_Ymoves = generateStates(player1, player2, 1, 3, 100000)
save("X_random_random_secondplayer_3x3_100000game", X)
save("YX_random_random_secondplayer_3x3_100000game", Y_Xmoves)
save("YY_random_random_secondplayer_3x3_100000game", Y_Ymoves)
print("saved") """



""" player2 = QLearningPlayer()
player1 = RandomPlayer()
b = Board(3)
trainer = Trainer()
trainer.trainingQLearningPlayer(player1, player2, 3, 100000)
print("saved") """

#testGame(player1, player2, b, 1000)

trainer = Trainer()
""" trainer.trainingClassifierPlayer("X_random_random_firstplayer_3x3_100000game", 
                                    "YX_random_random_firstplayer_3x3_100000game",
                                    "YY_random_random_firstplayer_3x3_100000game", True, 3) """
trainer.trainingClassifierPlayer("X_random_random_firstplayer_3x3_100000game", 
                                    "YX_random_random_firstplayer_3x3_100000game",
                                    "YY_random_random_firstplayer_3x3_100000game", True, 3, 2)

#trainer.trainingQLearningPlayer(QLearningPlayer(), RandomPlayer(), 4, 200000)

#testGame(RandomPlayer(), RandomForestClassifierPlayer("DTC_3x3_secondplayer_X", "DTC_3x3_secondplayer_Y"), Board(3), 1000)

""" cont = Controller(player1, player2, b)
cont.training(True, False, 100000)
save("policy_3x3_100000_round_rotations_random_firstplayer_genetic", player1.states_value)

player1.states_value = load("policy_3x3_100000_round_rotations_random_firstplayer_genetic")
player1.exp_rate = 0.0 """
''' testGame(player1, player2, b, 100)
testGame(player2, player1, b, 100)

b = Board(4)

testGame(player1, player2, b, 100)

testGame(player2, player1, b, 100) '''


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
