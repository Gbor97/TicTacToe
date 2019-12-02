from enum import Enum
from math import inf
from random import choice
import numpy as np
import collections
import itertools
import pygame
import os

from generals import State
from generals import getHash
from board import Board
from userInterface import Grid
from textMenu import TextMenu

class Controller:
    def __init__(self, player1, player2, board):
        self.player1 = player1
        self.player1.setSign(True)
        self.player1.board = board
        self.player2 = player2
        self.player2.setSign(False)
        self.player2.board = board
        self.board = board 

    def trainLoop(self):
        while self.board.freeCellCheck():
            win = False
            move = self.player1.move()
            #self.board.print()
            if self.board.checkWin(self.player1.sign, move):
                win = True
                self.board.reset()
                return self.player1
            if not self.board.freeCellCheck():
                break
            move = self.player2.move()
            #self.board.print()
            if self.board.checkWin(self.player2.sign, move):
                win = True
                self.board.reset()
                return self.player2
            if not self.board.freeCellCheck():
                break
        if not win:
            self.board.reset()
            return None

    def gameLoop(self):
        while self.board.freeCellCheck():
            win = False
            self.board.print()
            print('Player1')
            move = self.player1.move()
            if self.board.checkWin(self.player1.sign, move):
                self.board.print()
                print('*** Congratulations! Player1 won! ***')
                win = True
                return self.player1
            self.board.print()
            if not self.board.freeCellCheck():
                break
            print('Player2')
            move = self.player2.move()
            if self.board.checkWin(self.player2.sign, move):
                self.board.print()
                print('*** Congratulations! Player2 won! ***')
                win = True
                return self.player2
        if not win:
            self.board.print()
            print('*** DRAW ***')
            return None


    def visualLoop(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '200,100'
        surface = pygame.display.set_mode((600,600))
        pygame.display.set_caption('Tic-tac-toe')

        grid = Grid(self.board)
        running = True
        player1turn = True
        winner = None

        surface.fill((10,10,10))
        grid.draw(surface)
        pygame.display.flip()

        while running:
            while winner == None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        winner = 3
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:
                            if player1turn:
                                player1turn = False
                                move = self.player1.move()
                                grid.draw(surface)
                                pygame.display.flip()
                                if self.board.checkWin(self.player1.sign, move):
                                    winner = 1
                                    break
                                if not self.board.freeCellCheck():
                                    winner = 0
                                    break
                            else:
                                player1turn = True
                                move = self.player2.move()
                                grid.draw(surface)
                                pygame.display.flip()
                                if self.board.checkWin(self.player2.sign, move):
                                    winner = 2
                                    break
                                if not self.board.freeCellCheck():
                                    winner = 0
                                    break
            textMenu = TextMenu(surface)
            if winner == 1:
                textMenu.add_line('*** Congratulations! Player1 won! ***')
                textMenu.draw()
                pygame.display.flip()
            elif winner == 2:
                textMenu.add_line('*** Congratulations! Player2 won! ***')
                textMenu.draw()
                pygame.display.flip()
            elif winner == 0:
                textMenu.add_line('*** DRAW! ***')
                textMenu.draw()
                pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:
                            running = False
                if event.type == pygame.QUIT:
                        running = False
                        winner = 3
                        exit()
                

            
    


print('Wellcome bitten2')