from basePlayer import BasePlayer
from math import inf
from generals import State
import random
from random import choice

class MinMaxPlayer(BasePlayer):
    def __init__(self, sign, type, board, cont, pruning = True):
        BasePlayer.__init__(self, sign, type, board, cont)
        self.MAX = 1
        self.MIN = -1 
        self.rival_sign = self.getRivalSign()
        self.pruning = pruning
        random.seed(7)

    def getRivalSign(self):
        if self.sign == State.X:
            return State.O
        else:
            return State.X

    def getStatesOfArray(self, array_of_cells):
        array_of_states = []
        for i in range(len(array_of_cells)):
            array_of_states.append(array_of_cells[i].state)
        return array_of_states



    def calcBasePoint(self):
        return self.board.size * (self.board.size * 2 + 2)

    def heuristic4(self, depth, move):
        if self.cont.checkWin(self.sign, move):
            score = self.calcBasePoint()
            return [-1, -1, score]
        elif self.cont.checkWin(self.rival_sign, move):
            score = - self.calcBasePoint()
            return [-1, -1, score]
        elif not self.board.freeCellCheck():
            score = 0
            return [-1, -1, score]
        elif depth == 0:
            own_sign_num = 0
            rival_sign_num = 0
            rowpoint = None 
            columnpoint = None 
            diag1point = None
            diag2point = None
            for j in range(self.board.size):
                array_of_states = self.getStatesOfArray(self.board.table[j])
                if (array_of_states.count(self.rival_sign) == 0):
                    array_of_states_own = self.getStatesOfArray(self.board.table[j])
                    rowpoint = array_of_states_own.count(self.sign)
                    own_sign_num = own_sign_num + array_of_states_own.count(self.sign)
                    """ print("own " + str(own_sign_num))
                    print("row " + str(j))
                    print(array_of_states_own)
                    print(array_of_states_own.count(self.sign)) """
                elif (array_of_states.count(self.sign) == 0):
                    rival_sign_num = rival_sign_num + array_of_states.count(self.rival_sign)
                    #print(2)
                elif (array_of_states.count(self.sign) == 1):
                    own_sign_num = own_sign_num + array_of_states.count(self.rival_sign)
                    rowpoint = self.board.size // 2
                    """ print("own " + str(own_sign_num))
                    print("row " + str(j))
                    print(array_of_states_own)
                    print(array_of_states_own.count(self.sign)) """
                column = []
                for k in range(self.board.size):
                    column.append(self.board.table[k][j].state)
                if (column.count(self.rival_sign) == 0):
                    columnpoint = column.count(self.sign)
                    own_sign_num = own_sign_num + column.count(self.sign)
                    """ print("own " + str(own_sign_num))
                    print("column " + str(j))
                    print(column)
                    print(column.count(self.sign)) """
                elif (column.count(self.sign) == 0):
                    rival_sign_num = rival_sign_num + column.count(self.rival_sign)
                    #print(5)
                elif (column.count(self.sign) == 1):
                    own_sign_num = own_sign_num + column.count(self.rival_sign)
                    columnpoint = self.board.size // 2
                    """ print("own " + str(own_sign_num))
                    print("column " + str(j))
                    print(column)
                    print(column.count(self.sign)) """
                diag1 = []
                diag2 = []
            for l in range(self.board.size):
                diag1.append(self.board.table[l][l].state)
                diag2.append(self.board.table[l][self.board.size - 1 - l].state)
            if (diag1.count(self.rival_sign) == 0):
                diag1point = diag1.count(self.sign)
                own_sign_num = own_sign_num + diag1.count(self.sign)
                """ print("own " + str(own_sign_num))
                print("diag1 " + str(j))
                print(diag1)
                print(diag1.count(self.sign)) """
            elif (diag1.count(self.sign) == 0):
                rival_sign_num = rival_sign_num + diag1.count(self.rival_sign)
                #print(8)
            elif (diag1.count(self.sign) == 1):
                own_sign_num = own_sign_num + diag1.count(self.rival_sign)
                diag1point = self.board.size // 2
                """ print("own " + str(own_sign_num))
                print("diag1 " + str(j))
                print(diag1)
                print(diag1.count(self.sign)) """
            if (diag2.count(self.rival_sign) == 0):
                own_sign_num = own_sign_num + diag2.count(self.sign)
                diag2point = diag2.count(self.sign)
                """ print("own " + str(own_sign_num))
                print("diag2 " + str(j))
                print(diag2)
                print(diag2.count(self.sign)) """
            elif (diag2.count(self.sign) == 0):
                rival_sign_num = rival_sign_num + diag2.count(self.rival_sign)
                #print(11)
            elif (diag2.count(self.sign) == 1):
                own_sign_num = own_sign_num + diag2.count(self.rival_sign)
                diag1point = self.board.size // 2
                """ print("own " + str(own_sign_num))
                print("diag2 " + str(j))
                print(diag2)
                print(diag2.count(self.sign)) """
            return [-1, -1, own_sign_num - rival_sign_num, rowpoint, columnpoint, diag1point, diag2point, diag1, diag2]

    def heuristic3(self, depth, move):
        if self.cont.checkWin(self.sign, move):
            score = self.calcBasePoint()
            return [-1, -1, score]
        elif self.cont.checkWin(self.rival_sign, move):
            score = - self.calcBasePoint()
            return [-1, -1, score]
        elif not self.board.freeCellCheck():
            score = 0
            return [-1, -1, score]
        elif depth == 0:
            own_sign_num = 0
            rowpoint = None 
            columnpoint = None 
            diag1point = None
            diag2point = None
            for j in range(self.board.size):
                array_of_states = self.getStatesOfArray(self.board.table[j])
                if (array_of_states.count(self.rival_sign) == 0):
                    array_of_states_own = self.getStatesOfArray(self.board.table[j])
                    rowpoint = array_of_states_own.count(self.sign)
                    own_sign_num = own_sign_num + array_of_states_own.count(self.sign)
                column = []
                for k in range(self.board.size):
                    column.append(self.board.table[k][j].state)
                if (column.count(self.rival_sign) == 0):
                    columnpoint = column.count(self.sign)
                    own_sign_num = own_sign_num + column.count(self.sign)
                diag1 = []
                diag2 = []
            for l in range(self.board.size):
                diag1.append(self.board.table[l][l].state)
                diag2.append(self.board.table[l][self.board.size - 1 - l].state)
            if (diag1.count(self.rival_sign) == 0):
                diag1point = diag1.count(self.sign)
                own_sign_num = own_sign_num + diag1.count(self.sign)
            if (diag2.count(self.rival_sign) == 0):
                own_sign_num = own_sign_num + diag2.count(self.sign)
                diag2point = diag2.count(self.sign)
            if(own_sign_num != 0):
                """ print(move)
                print("SCORE:" + str(own_sign_num)) """
            return [-1, -1, own_sign_num, rowpoint, columnpoint, diag1point, diag2point, diag1, diag2]

    def heuristic2(self, depth, move):
        if self.cont.checkWin(self.sign, move):
            score = self.calcBasePoint()
            return [-1, -1, score]
        elif self.cont.checkWin(self.rival_sign, move):
            score = - self.calcBasePoint()
            return [-1, -1, score]
        elif not self.board.freeCellCheck():
            score = 0
            return [-1, -1, score]
        elif depth == 0:
            own_sign_num = 0
            rivale_sign_num = 0
            for j in range(self.board.size):
                array_of_states = self.getStatesOfArray(self.board.table[j])
                own_sign_num = own_sign_num + array_of_states.count(self.sign)
                rivale_sign_num = rivale_sign_num + array_of_states.count(self.rival_sign)
                column = []
                for k in range(self.board.size):
                    column.append(self.board.table[k][j].state)
                own_sign_num = own_sign_num + column.count(self.sign)
                rivale_sign_num = rivale_sign_num + column.count(self.rival_sign)
                diag1 = []
                diag2 = []
            for l in range(self.board.size):
                diag1.append(self.board.table[l][l].state)
                diag2.append(self.board.table[l][self.board.size - 1 - l].state)
            own_sign_num = own_sign_num + diag1.count(self.sign)
            rivale_sign_num = rivale_sign_num + diag1.count(self.rival_sign)
            own_sign_num = own_sign_num + diag2.count(self.sign)
            rivale_sign_num = rivale_sign_num + diag2.count(self.rival_sign)
            score = own_sign_num - rivale_sign_num
            return [-1, -1, score]

    def heuirstic1(self, depth):
            if self.cont.checkWin(self.sign):
                score = +1
            elif self.cont.checkWin(self.rival_sign):
                score = -1
            elif depth == 0:
                score = 0
            return score

    def minimax(self, boardState, depth, player, sign, alpha, beta, move = None):
        #print("depth: "+str(depth))
        if player == self.MAX:
            best = [-1, -1, -inf]
        else:
            best = [-1, -1, +inf]
        if move != None:
            #self.rival_sign = self.getRivalSign()
            score = self.heuristic4(depth, move)
            if score != None:
                return score

        #print(self.empty_cells(boardState))
        for cell in self.board.empty_cells():
            x, y = cell[0], cell[1]
            boardState.table[x][y].state = sign
            rival_sign = State.EMPTY
            if self.sign == State.X:
                rival_sign = State.O
            else:
                rival_sign = State.X
            #print(str(sign) + ": "+ str(x)+", "+str(y))
            if player == self.MIN:
                score = self.minimax(boardState, depth - 1, self.MAX, self.sign, alpha, beta, [x, y])
            else:
                score = self.minimax(boardState, depth - 1, self.MIN, rival_sign, alpha, beta, [x, y])
            boardState.table[x][y].state = State.EMPTY
            score[0], score[1] = x, y

            if player == self.MAX:
                if score[2] > best[2]:
                    best = score  # max value
                alpha = max(alpha, score[2])
                if beta <= alpha:
                    break
            else:
                if score[2] < best[2]:
                    best = score  # min value
                beta = min(beta, score[2])
                if beta <= alpha:
                    break
        #if best = -1 -1 , válassz random
        #print("best: "+ str(score))
        #print("depth:" + str(depth))
        return best
        

    def move(self):
        if len(self.board.empty_cells()) < 6:
            depth = len(self.board.empty_cells())
        else:
            depth = 6
        if depth == 0 or not self.board.freeCellCheck():
            return
        #print(depth)
        if depth == self.board.size*self.board.size:
            x = choice(range(self.board.size))
            y = choice(range(self.board.size))
        else:
            move = self.minimax(self.board, depth, self.MAX, self.sign, -inf, +inf)
            #print(move)
            x, y = move[0], move[1]

        return self.board.move(x, y, self)
