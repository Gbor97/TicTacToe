from enum import Enum
from generals import State
import itertools

class Cell:
    def __init__(self, state = State.EMPTY):
        self.state = state

    def isFree(self):
        if (self.state == State.EMPTY):
            return True
        else:
            return False

class Board:
    def __init__(self, size):
        self.size = size
        self.table = [[Cell() for x in range(size)] for y in range(size)] 

    def validateMove(self, moveX, moveY):
        if (moveX < self.size) and (moveY < self.size) and (self.table[moveX][moveY].isFree()):
            return True
        return False

    def move(self, moveX, moveY, player):
        self.table[moveX][moveY].state = player.sign
        return [moveX, moveY]

    def freeCellCheck(self):
        free = False
        for i in range(self.size):
            for j in range(self.size):
                if self.table[i][j].state == State.EMPTY:
                    free = True
                    break
        return free

    def empty_cells(self):
        cells = []
        for row in range(self.size):
            for column in range(self.size):
                if self.table[row][column].state == State.EMPTY:
                    cells.append([row, column])
        return cells

    def reset(self):
        for i in range(self.size):
            for j in range(self.size):
                self.table[i][j].state = State.EMPTY

    def print(self):
        for i in range(self.size):
            for _ in itertools.repeat(None, self.size):
                print("----",end = '')
            print()
            for j in range(self.size):
                print(self.table[i][j].state.value, end = '')
                print(" | ", end = '')
            print()

    def make_win_states(self, move):
        win_states = []
        #row
        win_state = []
        for column in range(self.size):
            win_state.append(self.table[move[0]][column].state)
        win_states.append(win_state) 
        #column
        win_state = []
        for row in range(self.size):
            win_state.append(self.table[row][move[1]].state)
        win_states.append(win_state)
        """ for row in range(board.size):
            win_state = []
            for column in range(board.size):
                win_state.append(board.table[row][column].state)
            win_states.append(win_state)
        #columns
        for column in range(board.size):
            win_state = []
            for row in range(board.size):
                win_state.append(board.table[row][column].state)
            win_states.append(win_state) """
        #diagonal from left to right
        win_state = []
        for row in range(self.size):
                win_state.append(self.table[row][row].state)
        win_states.append(win_state)
        #diagonal from right to left
        win_state = []
        for row in range(self.size):
                win_state.append(self.table[row][self.size - 1 - row].state)
        win_states.append(win_state)
        return win_states

    def checkWin(self, sign, move):
        win_states = self.make_win_states(move)
        state = []
        for _ in itertools.repeat(None, self.size):
            state.append(sign)
        return state in win_states