from math import inf
import random
from random import choice

from generals import State
from generals import getRivalSign
from basePlayer import BasePlayer

class MiniMaxPlayer(BasePlayer):
    def __init__(self, depth = 6, heuristic = 4, pruning = True):
        BasePlayer.__init__(self)
        self.MAX = 1
        self.MIN = -1 
        self.depth = depth
        self.pruning = pruning
        self.heuristic = heuristic
        self.name = "MinMaxPlayer"
        random.seed(7)

    def getStatesOfArray(self, array_of_cells):
        array_of_states = []
        for i in range(len(array_of_cells)):
            array_of_states.append(array_of_cells[i].state)
        return array_of_states

    def heuristic4(self, depth, move):
        result = self.basicHeuristic(move)
        if result != None:
            return result
        elif depth == 0:
            own_sign_num = 0
            rival_sign_num = 0
            for j in range(self.board.size):
                array_of_states = self.getStatesOfArray(self.board.table[j])
                if (array_of_states.count(self.rival_sign) == 0):
                    array_of_states_own = self.getStatesOfArray(self.board.table[j])
                    own_sign_num = own_sign_num + array_of_states_own.count(self.sign)
                elif (array_of_states.count(self.sign) == 0):
                    rival_sign_num = rival_sign_num + array_of_states.count(self.rival_sign)
                elif (array_of_states.count(self.sign) == 1):
                    own_sign_num = own_sign_num + array_of_states.count(self.rival_sign)
                column = []
                for k in range(self.board.size):
                    column.append(self.board.table[k][j].state)
                if (column.count(self.rival_sign) == 0):
                    own_sign_num = own_sign_num + column.count(self.sign)
                elif (column.count(self.sign) == 0):
                    rival_sign_num = rival_sign_num + column.count(self.rival_sign)
                elif (column.count(self.sign) == 1):
                    own_sign_num = own_sign_num + column.count(self.rival_sign)
            diag1 = []
            diag2 = []
            for l in range(self.board.size):
                diag1.append(self.board.table[l][l].state)
                diag2.append(self.board.table[l][self.board.size - 1 - l].state)
            if (diag1.count(self.rival_sign) == 0):
                own_sign_num = own_sign_num + diag1.count(self.sign)
            elif (diag1.count(self.sign) == 0):
                rival_sign_num = rival_sign_num + diag1.count(self.rival_sign)
            elif (diag1.count(self.sign) == 1):
                own_sign_num = own_sign_num + diag1.count(self.rival_sign)
            if (diag2.count(self.rival_sign) == 0):
                own_sign_num = own_sign_num + diag2.count(self.sign)
            elif (diag2.count(self.sign) == 0):
                rival_sign_num = rival_sign_num + diag2.count(self.rival_sign)
            elif (diag2.count(self.sign) == 1):
                own_sign_num = own_sign_num + diag2.count(self.rival_sign)
            return [-1, -1, own_sign_num - rival_sign_num]

    def heuristic3(self, depth, move):
        result = self.basicHeuristic(move)
        if result != None:
            return result
        elif depth == 0:
            own_sign_num = 0
            for j in range(self.board.size):
                array_of_states = self.getStatesOfArray(self.board.table[j])
                if (array_of_states.count(self.rival_sign) == 0):
                    array_of_states_own = self.getStatesOfArray(self.board.table[j])
                    own_sign_num = own_sign_num + array_of_states_own.count(self.sign)
                column = []
                for k in range(self.board.size):
                    column.append(self.board.table[k][j].state)
                if (column.count(self.rival_sign) == 0):
                    own_sign_num = own_sign_num + column.count(self.sign)
            diag1 = []
            diag2 = []
            for l in range(self.board.size):
                diag1.append(self.board.table[l][l].state)
                diag2.append(self.board.table[l][self.board.size - 1 - l].state)
            if (diag1.count(self.rival_sign) == 0):
                own_sign_num = own_sign_num + diag1.count(self.sign)
            if (diag2.count(self.rival_sign) == 0):
                own_sign_num = own_sign_num + diag2.count(self.sign)
            return [-1, -1, own_sign_num]

    def heuristic2(self, depth, move):
        result = self.basicHeuristic(move)
        if result != None:
            return result
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

    def heuristic1(self, depth, move):
        if self.board.checkWin(self.sign, move):
            score = +1
            return [-1, -1, score]
        elif self.board.checkWin(self.rival_sign, move):
            score = -1
            return [-1, -1, score]
        elif depth == 0 or not self.board.freeCellCheck():
            score = 0
            return [-1, -1, score]

    def basicHeuristic(self, move):
        if self.board.checkWin(self.sign, move):
            score = inf
            #self.basePoint
            return [-1, -1, score]
        elif self.board.checkWin(self.rival_sign, move):
            score = - inf
            #self.basePoint
            return [-1, -1, score]
        elif not self.board.freeCellCheck():
            score = 0
            return [-1, -1, score]
        

    def minimax(self, boardState, depth, player, sign, alpha, beta, move = None):
        #best_scores = []
        if player == self.MAX:
            best = [-1, -1, -inf]
        else:
            best = [-1, -1, +inf]
        if move != None:
            if self.heuristic == 1:
                score = self.heuristic1(depth, move)
            elif self.heuristic == 2:
                score = self.heuristic2(depth, move)
            elif self.heuristic == 3:
                score = self.heuristic3(depth, move)
            elif self.heuristic == 4:
                score = self.heuristic4(depth, move)
            if score != None:
                return score
        for cell in self.board.empty_cells():
            #
            x, y = cell[0], cell[1]
            boardState.table[x][y].state = sign
            """ print(player == self.MIN)
            boardState.print() """
            if player == self.MIN:
                score = self.minimax(boardState, depth - 1, self.MAX, self.sign, alpha, beta, [x, y])
            else:
                score = self.minimax(boardState, depth - 1, self.MIN, self.rival_sign, alpha, beta, [x, y])
            boardState.table[x][y].state = State.EMPTY
            score[0], score[1] = x, y


            if player == self.MAX:
                if score[2] > best[2]:
                    #if score[2] != best[2]:
                    #    best_scores.clear()
                    best = score  # max value
                    #best_scores.append(best)
                    """ print("max") """
                alpha = max(alpha, score[2])
                if beta <= alpha:
                    break
            else:
                if score[2] < best[2]:
                    #if score[2] != best[2]:
                    #    best_scores.clear()
                    best = score  # min value
                    #best_scores.append(best)
                    """ print("min") """
                beta = min(beta, score[2])
                if beta <= alpha:
                    break
        return best
        

    def move(self):
        if len(self.board.empty_cells()) < self.depth:
            depth = len(self.board.empty_cells())
        else:
            depth = self.depth
        if depth == 0 or not self.board.freeCellCheck():
            return
        if depth == self.board.size*self.board.size:
            x = choice(range(self.board.size))
            y = choice(range(self.board.size))
        else:
            move = self.minimax(self.board, depth, self.MAX, self.sign, -inf, +inf)
            x, y = move[0], move[1]
        return self.board.move(x, y, self)
