from basePlayer import BasePlayer
import itertools
from math import inf
from random import choice
import numpy as np
from generals import State
import pickle


from minimaxPlayer import MinMaxPlayer
from generals import *
from game import Board
from game import Controller

from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.linear_model import LogisticRegression

class SVMPlayer(BasePlayer):
    def __init__(self, sign, type, board, cont, rival_sign):
        BasePlayer.__init__(self, sign, type, board, cont)
        self.states_value = {}  # state -> value
        self.board = board
        self.sign = sign
        self.rival_sign = rival_sign

    # get unique hash of current board state
    def getHash(self, boardState):
        boardHash = ""
        for k in range(len(boardState)):
            for l in range(len(boardState)):
                boardHash += str(boardState[k][l].state.value)
        return boardHash

    # get unique hash of current board state
    def getArrayOfHash(self, boardHashString):
        boardState = []
        for c in boardHashString:
            boardState.append(int(c))
        return boardState

    def checkRotations(self, boardState):
        i = 0
        for i in range (0, 4):
            boardHash = self.getHash(boardState)
            if self.states_value.get(boardHash) is None:
                boardState = list(zip(*reversed(boardState)))
            else:
                 return [boardHash, i]
        return [None, None]

    """ def move(self):
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
                    rotationBoard = [[0 for x in range(self.board.size)] for y in range(self.board.size)]
                    rotationBoard[poss_move[0]][poss_move[1]] = 1
                    self.board.table[poss_move[0]][poss_move[1]].state = State.EMPTY
                    for i in range(0, rotationNumber):
                        rotationBoard = list(zip(*reversed(rotationBoard)))
                    for i in range(len(rotationBoard)):
                        for j in range(len(rotationBoard[i])):
                            if rotationBoard[i][j] == 1:
                                poss_move[0] = i
                                poss_move[1] = j
                # print("value", value)
                if value > value_max:
                    #print("v:" + str(value))
                    #print("mv: " + str(value_max))
                    value_max = value
                    move = poss_move
                self.board.table[poss_move[0]][poss_move[1]].state = State.EMPTY
        # print("{} takes action {}".format(self.name, action))
        self.states.append(self.getHash(self.board.table))
        return self.board.move(move[0], move[1], self) """
        

    def training(self, X, Y, rounds=10000):
        """ self.loadPolicy("_gdrive_My Drive_policy_regression_input")
        X = []
        Y = []
        print(len(self.states_value))
        for key in self.states_value:
            #Bs= self.getBoardStateFromHash(key)
            #res1 = self.transfromBoardState(Bs)
            #res2 = self.transfromBoardState3(Bs)
            #joinedlist = res1 + res2
            #X.append(joinedlist)
            X.append(self.transfromBoardState(self.getBoardStateFromHash(key)))
            #X.append(self.getArrayOfHash(key))
            Y.append(self.states_value[key]) """
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
        
        reg.fit(X_train, Y_train)  

        #print(reg.feature_importances_)

        result = reg.score(X_test, Y_test)
        print("Accuracy: %.2f%%" % (result*100.0))
        print()
        print(X[3])
        """ print(X_scaled[1]) """
        print(Y[3])
        print(reg.predict([X[3]]))
        return reg

    def generateStates(self, boardSize, gameNumber):
        board = Board(boardSize)
        cont = Controller(PlayerEnum.Random, PlayerEnum.Random, board)
        boardStates = []
        winStates = []
        winner = -1
        for _ in itertools.repeat(None, gameNumber):
            end = False
            number_of_moves = 0
            while board.freeCellCheck():
                win = False
                move = cont.player1.move()
                number_of_moves = number_of_moves + 1
                boardStates.append(self.transfromBoardState4(self.getHash(board.table)))
                if cont.checkWin(cont.player1.sign, move):
                    win = True
                    end = True
                    winner = 1
                    board.reset()
                    break
                if not board.freeCellCheck():
                    break
                move = cont.player2.move()
                number_of_moves = number_of_moves + 1
                boardStates.append(self.transfromBoardState4(self.getHash(board.table)))  
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
                for _ in itertools.repeat(None, number_of_moves):
                    winStates.append(winner)
        return [boardStates, winStates]
            
    
    def savePolicy(self, name):
        fw = open('policy_' + name, 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()

    def getBoardStateFromHash(self, boardStateHash):
        boardState = []
        for i in range(self.board.size):
            row = []
            for j in range(self.board.size):
                row.append(int(boardStateHash[i * self.board.size + j]))
            boardState.append(row)
        return boardState

    #result: ha az ellenfélnek nincs benne jele, akkor a saját jeleim száma
    #        ha az ellenfélnek van és nekem nincs, akkor -ellenfél jelei száma
    #        ha az ellenfélnek van és nekem több van, vagy full üres, akkor 0
    def transfromBoardState(self, boardState):
        own_sign_num = 0
        rival_sign_num = 0
        result = []
        for j in range(self.board.size):
            if (boardState[j].count(self.rival_sign.value) == 0):
                own_sign_num = own_sign_num + boardState[j].count(self.sign.value)
                result.append(boardState[j].count(self.sign.value))
            elif (boardState[j].count(self.sign.value) == 0):
                rival_sign_num = rival_sign_num + boardState[j].count(self.rival_sign.value)
                result.append(-boardState[j].count(self.rival_sign.value))
            else:
                result.append(0)
            column = []
            for k in range(self.board.size):
                column.append(boardState[k][j])
            if (column.count(self.rival_sign.value) == 0):
                own_sign_num = own_sign_num + column.count(self.sign.value)
                result.append(column.count(self.sign.value))
            elif (column.count(self.sign.value) == 0):
                rival_sign_num = rival_sign_num + column.count(self.rival_sign.value)
                result.append(-column.count(self.rival_sign.value))
            else:
                result.append(0)
            diag1 = []
            diag2 = []
        for l in range(self.board.size):
            diag1.append(boardState[l][l])
            diag2.append(boardState[l][self.board.size - 1 - l])
        if (diag1.count(self.rival_sign.value) == 0):
            own_sign_num = own_sign_num + diag1.count(self.sign.value)
            result.append(diag1.count(self.sign.value))
        elif (diag1.count(self.sign.value) == 0):
            rival_sign_num = rival_sign_num + diag1.count(self.rival_sign.value)
            result.append(-diag1.count(self.rival_sign.value))
        else:
            result.append(0)
        if (diag2.count(self.rival_sign.value) == 0):
            own_sign_num = own_sign_num + diag2.count(self.sign.value)
            result.append(diag2.count(self.sign.value))
        elif (diag2.count(self.sign.value) == 0):
            rival_sign_num = rival_sign_num + diag2.count(self.rival_sign.value)
            result.append(-diag2.count(self.rival_sign.value))
        else:
            result.append(0)
        return result

    #result: ha az ellenfélnek nincs benne jele, akkor a saját jeleim száma
    #        ha az ellenfélnek van és nekem nincs, akkor -ellenfél jelei száma
    #        ha az ellenfélnek van és nekem is van, de nekem csak 1, akkor boards.size//2
    #        ha az ellenfélnek van és nekem több is van, vagy full üres, akkor 0
    def transfromBoardState2(self, boardState):
        own_sign_num = 0
        rival_sign_num = 0
        result = []
        for j in range(self.board.size):
            if (boardState[j].count(self.rival_sign.value) == 0):
                own_sign_num = own_sign_num + boardState[j].count(self.sign.value)
                result.append(boardState[j].count(self.sign.value))
            elif (boardState[j].count(self.sign.value) == 0):
                rival_sign_num = rival_sign_num + boardState[j].count(self.rival_sign.value)
                result.append(-boardState[j].count(self.rival_sign.value))
            elif (boardState[j].count(self.sign.value) == 1):
                result.append(self.board.size // 2)
                own_sign_num = own_sign_num + self.board.size // 2
            else:
                result.append(0)
            column = []
            for k in range(self.board.size):
                column.append(boardState[k][j])
            if (column.count(self.rival_sign.value) == 0):
                own_sign_num = own_sign_num + column.count(self.sign.value)
                result.append(column.count(self.sign.value))
            elif (column.count(self.sign.value) == 0):
                rival_sign_num = rival_sign_num + column.count(self.rival_sign.value)
                result.append(-column.count(self.rival_sign.value))
            elif (column.count(self.sign.value) == 1):
                result.append(self.board.size // 2)
                own_sign_num = own_sign_num + self.board.size // 2
            else:
                result.append(0)
            diag1 = []
            diag2 = []
        for l in range(self.board.size):
            diag1.append(boardState[l][l])
            diag2.append(boardState[l][self.board.size - 1 - l])
        if (diag1.count(self.rival_sign.value) == 0):
            own_sign_num = own_sign_num + diag1.count(self.sign.value)
            result.append(diag1.count(self.sign.value))
        elif (diag1.count(self.sign.value) == 0):
            rival_sign_num = rival_sign_num + diag1.count(self.rival_sign.value)
            result.append(-diag1.count(self.rival_sign.value))
        elif (diag1.count(self.sign.value) == 1):
            result.append(self.board.size // 2)
            own_sign_num = own_sign_num + self.board.size // 2
        else:
            result.append(0)
        if (diag2.count(self.rival_sign.value) == 0):
            own_sign_num = own_sign_num + diag2.count(self.sign.value)
            result.append(diag2.count(self.sign.value))
        elif (diag2.count(self.sign.value) == 0):
            rival_sign_num = rival_sign_num + diag2.count(self.rival_sign.value)
            result.append(-diag2.count(self.rival_sign.value))
        elif (diag2.count(self.sign.value) == 1):
            result.append(self.board.size // 2)
            own_sign_num = own_sign_num + self.board.size // 2
        else:
            result.append(0)
        #return result
        return own_sign_num - rival_sign_num

    #result: ugyanaz, mint a transfromBoardState2 logikája, csak nem az egész pályára nézve, hanem külön tekitnve 
    #        a sorokra, az oszlopokra és a diagonálokra
    def transfromBoardState3(self, boardState):
        own_sign_num = 0
        rival_sign_num = 0
        row_num = 0
        column_num = 0
        diag_num = 0
        result = []
        for j in range(self.board.size):
            if (boardState[j].count(self.rival_sign.value) == 0):
                own_sign_num = own_sign_num + boardState[j].count(self.sign.value)
                row_num = row_num + boardState[j].count(self.sign.value)
                result.append(boardState[j].count(self.sign.value))
            elif (boardState[j].count(self.sign.value) == 0):
                rival_sign_num = rival_sign_num + boardState[j].count(self.rival_sign.value)
                result.append(-boardState[j].count(self.rival_sign.value))
                row_num = row_num - boardState[j].count(self.rival_sign.value)
            elif (boardState[j].count(self.sign.value) == 1):
                result.append(self.board.size // 2)
                row_num = row_num + self.board.size // 2
                #own_sign_number-t kéne növelni itt
            else:
                result.append(0)
            column = []
            for k in range(self.board.size):
                column.append(boardState[k][j])
            if (column.count(self.rival_sign.value) == 0):
                own_sign_num = own_sign_num + column.count(self.sign.value)
                result.append(column.count(self.sign.value))
                column_num = column_num + column.count(self.sign.value)
            elif (column.count(self.sign.value) == 0):
                rival_sign_num = rival_sign_num + column.count(self.rival_sign.value)
                result.append(-column.count(self.rival_sign.value))
                column_num = column_num - column.count(self.rival_sign.value)
            elif (column.count(self.sign.value) == 1):
                result.append(self.board.size // 2)
                column_num = column_num + self.board.size // 2
                #own_sign_number-t kéne növelni itt
            else:
                result.append(0)
            diag1 = []
            diag2 = []
        for l in range(self.board.size):
            diag1.append(boardState[l][l])
            diag2.append(boardState[l][self.board.size - 1 - l])
        if (diag1.count(self.rival_sign.value) == 0):
            own_sign_num = own_sign_num + diag1.count(self.sign.value)
            result.append(diag1.count(self.sign.value))
            diag_num = diag_num + diag1.count(self.sign.value)
        elif (diag1.count(self.sign.value) == 0):
            rival_sign_num = rival_sign_num + diag1.count(self.rival_sign.value)
            result.append(-diag1.count(self.rival_sign.value))
            diag_num = diag_num - diag1.count(self.rival_sign.value)
        elif (diag1.count(self.sign.value) == 1):
            result.append(self.board.size // 2)
            diag_num = diag_num + self.board.size // 2
            #own_sign_number-t kéne növelni itt
        else:
            result.append(0)
        if (diag2.count(self.rival_sign.value) == 0):
            own_sign_num = own_sign_num + diag2.count(self.sign.value)
            result.append(diag2.count(self.sign.value))
            diag_num = diag_num + diag2.count(self.sign.value)
        elif (diag2.count(self.sign.value) == 0):
            rival_sign_num = rival_sign_num + diag2.count(self.rival_sign.value)
            result.append(-diag2.count(self.rival_sign.value))
            diag_num = diag_num - diag2.count(self.rival_sign.value)
        elif (diag2.count(self.sign.value) == 1):
            result.append(self.board.size // 2)
            diag_num = diag_num + self.board.size // 2
            #own_sign_number-t kéne növelni itt
        else:
            result.append(0)
        result2 = []
        result2.append(row_num)
        result2.append(column_num)
        result2.append(diag_num)
        return result

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

    #szar
    def makeXandY(self):
        X = []
        Y = []
        fromYtoQ = dict()
        self.loadPolicy("_gdrive_My Drive_policy_regression_input")
        for key in self.states_value:
            X.append(self.transfromBoardState5(key))
            Y.append(self.transfromBoardState2(self.getBoardStateFromHash(key)))
        return [X, Y]
        

        


board = Board(4)
cont = Controller(PlayerEnum.MinMax, PlayerEnum.QLearningPlayer, board)
player1 = SVMPlayer(State.X, 5, board, cont, State.O)


#print(player1.makeXandY())
X, Y = player1.generateStates(3, 100000)

player1.training(X, Y)

#print(player1.transfromBoardState4("0001010202020000"))
#print(player1.transfromBoardState2(player1.getBoardStateFromHash("0001010202020000")))

