import itertools
from math import inf
from random import choice
import numpy as np
import pickle
import sys

from basePlayer import BasePlayer
from generals import State
from generals import load
from generals import getHash
from generals import transfromBoardState5

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
from sklearn.tree import DecisionTreeClassifier


class SVMPlayer(BasePlayer):
    def __init__(self, board):
        BasePlayer.__init__(self, board)
        X = load("X_random_random_secondplayer_4x4_10000game")
        Y_Xmoves = load("YX_random_random_secondplayer_4x4_10000game")
        Y_Ymoves = load("YY_random_random_secondplayer_4x4_10000game")
        self.clf_x = self.training(X, np.ravel(Y_Xmoves))
        self.clf_y = self.training(X, np.ravel(Y_Ymoves))

    def move(self):
        boardState = transfromBoardState5(getHash(self.board.table))
        #print(boardState)
        prob_x = self.clf_x.predict_proba([boardState])
        prob_y = self.clf_y.predict_proba([boardState])
        prob_all = np.dot(prob_x.T, prob_y)
        prob_all = prob_all.tolist()
        free_cells = self.board.empty_cells()
        max_prob = 0.0
        for cell in free_cells:
            if max_prob <= prob_all[cell[0]][cell[1]]:
                max_prob = prob_all[cell[0]][cell[1]]
                move_x = cell[0]
                move_y = cell[1]
        return self.board.move(move_x, move_y, self)
        

    def training(self, X, Y, rounds=10000):
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.35, random_state=42)
        """scaler = StandardScaler()
        scaler.fit(X)
        X_scaled = scaler.transform(X)
        print(X_scaled) """
        """ for i in range(len(X)):
            print(str(X[i]) + "  " + str(Y[i])) """
        
        
        """ reg = svm.SVR(C=1.0, cache_size=1000, coef0=0.0, degree=3, epsilon=0.1,
                            gamma='auto_deprecated', kernel='rbf', max_iter=-1, shrinking=True,
                            tol=0.001, verbose=False) """
        
        #reg = RandomForestRegressor(max_depth=3, random_state=0, n_estimators=200)
        

        #reg = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')

        #reg = LinearRegression()

        #reg = linear_model.BayesianRidge()

        #reg = linear_model.Lasso(alpha=0.1)

        #reg = linear_model.Ridge(alpha=1.0)

        reg = RandomForestClassifier(n_estimators=200) 

        #reg = DecisionTreeClassifier(random_state=0)
        
        #reg = MultinomialNB()

        #reg = KNeighborsClassifier(n_neighbors=3)
        
        reg.fit(X, Y) 

        #print(reg.feature_importances_) 

        result = reg.score(X_test, Y_test)
        print("Accuracy: %.2f%%" % (result*100.0))
        print()
        #print(X[3])
        """ print(X_scaled[1]) """
        #print(Y[3])
        """ for i in range(len(X_test)):
            print(X_test[i])
            print(reg.predict(X_test[i]))
            print(Y_test[i]) """
        return reg
            

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
    
    def unique(self, list1): 
  
        # intilize a null list 
        unique_list = [] 
      
        # traverse for all elements 
        for x in list1: 
            # check if exists in unique_list or not 
            if x not in unique_list: 
                unique_list.append(x)
        return unique_list
        

""" board = Board(3)
cont = Controller(PlayerEnum.SVMPlayer, PlayerEnum.Random, board)
player1 = SVMPlayer(State.X, 5, board, cont, State.O)
player1.move() """

#print(player1.makeXandY())

""" Matrix = player1.generateStates(3, 100000)
Y_Xmoves = Matrix[:,2*3*3]
Y_Ymoves = Matrix[:,2*3*3+1]
Matrix = np.delete(Matrix, 2*3*3+1, 1)
X = np.delete(Matrix, 2*3*3, 1)
np.set_printoptions(threshold=sys.maxsize) """
""" player1.save("random_input_classifier_X_moves", X)
player1.save("random_input_classifier_Y_Xmoves", Y_Xmoves)
player1.save("random_input_classifier_Y_Ymoves", Y_Ymoves) """

""" X = player1.load("random_input_classifier_X_moves")
Y_Xmoves = player1.load("random_input_classifier_Y_Xmoves")
Y_Ymoves = player1.load("random_input_classifier_Y_Ymoves") """
""" print(len(X))
print(len(player1.unique(X)))
print(len(Y))
print(len(player1.unique(Y))) """


""" clf_x = player1.training(X, np.ravel(Y_Xmoves))
clf_y = player1.training(X, np.ravel(Y_Ymoves)) """

