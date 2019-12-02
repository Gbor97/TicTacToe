import itertools
from math import inf
from random import choice
import numpy as np
import pickle
import sys

from basePlayer import BasePlayer
from generals import State, load, getHash, save

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC


class RandomForestClassifierPlayer(BasePlayer):
    def __init__(self, clf_x_file, clf_y_file, X = [], Y_Xmoves = [], Y_Ymoves = [], classifier_num = 1):
        BasePlayer.__init__(self)
        self.classifier_num = classifier_num
        if len(X) != 0 and len(Y_Xmoves) != 0 and len(Y_Ymoves) != 0:
            self.clf_x = self.training(X, np.ravel(Y_Xmoves))
            self.clf_y = self.training(X, np.ravel(Y_Ymoves))
        elif clf_x_file != None and clf_y_file != None:
            self.clf_x = load(clf_x_file)
            self.clf_y = load(clf_y_file)
        else:
            raise Exception("You must train or load two ML model")
        self.name = "RandomForestClassifierPlayer"

    def move(self):
        boardState = OneHotEncoding2(getHash(self.board.table))
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
        
        classifiers = [
            LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial', n_jobs=-1),
            RandomForestClassifier(n_estimators=200, n_jobs=-1),
            DecisionTreeClassifier(random_state=0),
            KNeighborsClassifier(n_neighbors=3, n_jobs=-1),
            SVC(gamma='auto')
        ]
        clf = classifiers[self.classifier_num]
        clf.fit(X, Y) 
        print(clf)
        result = clf.score(X_test, Y_test)
        print("Accuracy: %.2f%%" % (result*100.0))
        print()
        print(clf.predict_proba(X[10]))
        return clf

    def saveModels(self): 
        if self.sign == State.X:
            player = "firstplayer"
        else:
            player = "secondplayer"
        save("RFC_" + str(self.board.size) + "x" + str(self.board.size) + "_" + player + "_X", self.clf_x)
        save("RFC_" + str(self.board.size) + "x" + str(self.board.size) + "_" + player + "_Y", self.clf_y)
    
def OneHotEncoding1(self, boardStateHash):
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

def OneHotEncoding2(boardStateHash):
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