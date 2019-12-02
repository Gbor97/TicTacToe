from basePlayer import BasePlayer
import numpy as np

class RandomPlayer(BasePlayer):
    def __init__(self):
        BasePlayer.__init__(self)
        self.name = "RandomPlayer"

    def move(self):
        cells = self.board.empty_cells()
        idx = np.random.choice(len(cells))
        move = cells[idx]
        return self.board.move(move[0], move[1], self)