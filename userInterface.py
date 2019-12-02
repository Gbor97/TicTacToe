import pygame
import os
from generals import State


class Grid:
    def __init__(self, board):
        self.grid = board
        self.cell_size_unit = 600 // board.size
        grid_lines = []
        for i in range (board.size-1):
            grid_lines.append((((i+1) * self.cell_size_unit, 0), ((i+1) * self.cell_size_unit, 600)))
            grid_lines.append(((0, (i+1) * self.cell_size_unit), (600, (i+1) * self.cell_size_unit)))
        self.grid_lines = grid_lines
        self.letterX = pygame.image.load(os.path.join('res', 'letterX' + str(self.grid.size) + '.png'))
        self.letterO = pygame.image.load(os.path.join('res', 'letterO' + str(self.grid.size) + '.png'))

    def draw(self, surface):
        for line in self.grid_lines:
            pygame.draw.line(surface, (200, 200, 200), line[0], line[1], 2)

        for x in range(len(self.grid.table)):
            for y in range(len(self.grid.table[x])):
                if self.grid.table[y][x].state == State.X:
                    surface.blit(self.letterX, (y * self.cell_size_unit, x * self.cell_size_unit))
                elif self.grid.table[y][x].state == State.O:
                    surface.blit(self.letterO, (y * self.cell_size_unit, x * self.cell_size_unit))
