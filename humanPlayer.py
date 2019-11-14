from basePlayer import BasePlayer
from generals import getInput

class HumanPlayer(BasePlayer):
    
    def move(self):
        while(True):
            moveX = getInput('# X coord, pls : ')
            moveY = getInput('# Y coord, pls : ')
            if self.board.validateMove(moveX, moveY):
                return self.board.move(moveX, moveY, self)
            else:
                print('Invalid numbers. Try again!')
        