import pygame

from basePlayer import BasePlayer
from generals import getInput

class HumanPlayer(BasePlayer):
    def __init__(self, visual = False):
        BasePlayer.__init__(self)
        self.name = "HumanPlayer"
        self.visual = visual
    
    def move(self):
        if self.visual:
            return self.moveVisual()
        else:
            return self.moveConsol()

    def moveConsol(self):
        while(True):
            moveX = getInput('# X coord, pls : ')
            moveY = getInput('# Y coord, pls : ')
            if self.board.validateMove(moveX, moveY):
                return self.board.move(moveX, moveY, self)
            else:
                print('Invalid numbers. Try again!')

    def moveVisual(self):
        while(True):
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cellX, cellY = pos[0] // (600 // self.board.size), pos[1] // (600 // self.board.size) 
                print(cellX)
                print(cellY)
                if self.board.validateMove(cellX, cellY):
                    return self.board.move(cellX, cellY, self)
                else:
                    print('Invalid move. Try again!')
        