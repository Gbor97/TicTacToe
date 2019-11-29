from generals import PlayerEnum
from generals import State
from enum import Enum

class BasePlayer:
    def __init__(self, board):
        self.sign = State.EMPTY
        self.rival_sign = State.EMPTY
        self.board = board

    def move(self, moveX, moveY):
        raise NotImplementedError()

    def setSign(self, Start):
        if Start:
            self.sign = State.X
            self.rival_sign = State.O
        else:
            self.sign = State.O
            self.rival_sign = State.X
