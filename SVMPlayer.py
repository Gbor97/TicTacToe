from basePlayer import BasePlayer
import itertools
from math import inf
from random import choice
import numpy as np
from generals import State
import pickle

from minimaxPlayer import MinMaxPlayer
from generals import PlayerEnum
from game import Board
from game import Controller
from generals import g

from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier


class SVMPlayer(BasePlayer):
    def __init__(self, sign, board):
        BasePlayer.__init__(self, board)
        self.states_value = {}  # state -> value

    # get unique hash of current board state
    def getHash(self, boardState):
        boardHash = ""
        for k in range(len(boardState)):
            for l in range(len(boardState)):
                boardHash += str(boardState[k][l].state.value)
        return boardHash

    def training(self, X, Y, rounds=10000):
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
        """scaler = StandardScaler()
        scaler.fit(X)
        X_scaled = scaler.transform(X)
        print(X_scaled) """
        """ for i in range(len(X)):
            print(str(X[i]) + "  " + str(Y[i])) """
        
        
        """ reg = svm.SVR(C=1.0, cache_size=1000, coef0=0.0, degree=3, epsilon=0.1,
                            gamma='auto_deprecated', kernel='rbf', max_iter=-1, shrinking=True,
                            tol=0.001, verbose=False) """
        #SVRmodel.fit(X_scaled, Y)
        
        #reg = RandomForestRegressor(max_depth=3, random_state=0, n_estimators=200)
        

        reg = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')

        #reg = LinearRegression()

        #reg = linear_model.BayesianRidge()

        #reg = linear_model.Lasso(alpha=0.1)

        #reg = linear_model.Ridge(alpha=1.0)

        #reg = RandomForestClassifier(n_estimators=150, max_depth=4, random_state=0) 
        
        #reg = MultinomialNB()

        #reg = KNeighborsClassifier(n_neighbors=3)
        
        reg.fit(X, Y) 

        #print(reg.feature_importances_) 

        result = reg.score(X_train, Y_train)
        print("Accuracy: %.2f%%" % (result*100.0))
        print()
        #print(X[3])
        """ print(X_scaled[1]) """
        #print(Y[3])
        """ for i in range(len(X_test)):
            print(X_test[i])
            print(reg.predict([X_test[i]]))
            print(Y_test[i]) """
        return reg

    def generateStates(self, boardSize, gameNumber):
        board = Board(boardSize)
        cont = Controller(PlayerEnum.Random, PlayerEnum.Random, board)
        boardStates = []
        winStates = []
        winner = -1
        for _ in itertools.repeat(None, gameNumber):
            end = False
            number_of_appends = 0
            while board.freeCellCheck():
                win = False
                move = cont.player1.move()
                boardState = self.transfromBoardState4(self.getHash(board.table))
                if boardState not in boardStates:
                    boardStates.append(boardState)
                    number_of_appends = number_of_appends + 1
                if cont.checkWin(cont.player1.sign, move):
                    win = True
                    end = True
                    winner = 1
                    board.reset()
                    break
                if not board.freeCellCheck():
                    break
                move = cont.player2.move()
                boardState = self.transfromBoardState4(self.getHash(board.table))
                if boardState not in boardStates:
                    boardStates.append(boardState)
                    number_of_appends = number_of_appends + 1 
                if cont.checkWin(cont.player2.sign, move):
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
                for _ in itertools.repeat(None, number_of_appends):
                    winStates.append(winner)
        return [boardStates, winStates]    

    def transfromBoardState4(self, boardStateHash):
        result = []
        for i in range(len(boardStateHash)):
            if boardStateHash[i] == '1':
                result.append(1)
                result.append(0)
                result.append(0)
            elif boardStateHash[i] == '2':
                result.append(0)
                result.append(1)
                result.append(0)
            else:
                result.append(0)
                result.append(0)
                result.append(1)
        return result

    def transfromBoardState5(self, boardStateHash):
        result = []
        for i in range(len(boardStateHash)):
            if boardStateHash[i] == '1':
                result.append(1)
                result.append(0)
            elif boardStateHash[i] == '2':
                result.append(0)
                result.append(1)
            else:
                result.append(0)
                result.append(0)
        return result