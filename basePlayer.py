from generals import PlayerEnum
from enum import Enum

class BasePlayer:
    def __init__(self, sign, type, board, cont):
        self.sign = sign
        self.type = PlayerEnum(type)
        self.board = board
        self.cont = cont

    def move(self, moveX, moveY):
        raise NotImplementedError()