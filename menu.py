import os
from random import randrange
import pygame
import pygameMenu

from controller import Controller
from board import Board
from minimaxPlayer import MiniMaxPlayer
from qlearningPlayer import QLearningPlayer
from humanPlayer import HumanPlayer
from randomForestClassifierPlayer import RandomForestClassifierPlayer

COLOR_BACKGROUND = (128, 0, 128)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
PLAYER1 = ['HUMAN PLAYER']
PLAYER2 = ['HUMAN PLAYER']
BOARD_SIZE = [3]
MENU_BACKGROUND_COLOR = (228, 55, 36)
WINDOW_SIZE = (600, 600)

main_menu = None
surface = None

def change_player1(value, player):
    PLAYER1[0] = player

def change_player2(value, player):
    PLAYER2[0] = player

def change_board_size(value, board_size):
    BOARD_SIZE[0] = board_size

def play_function(player1, player2, board_size):
    print(board_size[0])
    if player1 == ['HUMAN PLAYER']:
        player1_ = HumanPlayer(True)
    elif player1 == ['MINIMAX PLAYER']:
        player1_ = MiniMaxPlayer()
    elif player1 == ['QLEARNING PLAYER']:
        player1_ = QLearningPlayer("policy_3x3_100000_round_against_RandomPlayer_firstplayer") #todo
    elif player1 == ['RFC PLAYER']:
        player1_ = RandomForestClassifierPlayer("DTC_3x3_firstplayer_X", "DTC_3x3_firstplayer_Y") #todo
    if player2 == ['HUMAN PLAYER']:
        player2_ = HumanPlayer(True)
    elif player2 == ['MINIMAX PLAYER']:
        player2_ = MiniMaxPlayer()
    elif player2 == ['QLEARNING PLAYER']:
        player2_ = QLearningPlayer("policy_3x3_100000_round_against_RandomPlayer_secondplayer (1)") #todo
    elif player2 == ['RFC PLAYER']:
        player2_ = RandomForestClassifierPlayer("DTC_3x3_secondplayer_X", "DTC_3x3_secondplayer_Y") #todo
    cont = Controller(player1_, player2_, Board(board_size[0]))
    cont.visualLoop()


def main_background():
    """
    Function used by menus, draw on background while menu is active.
    :return: None
    """
    global surface
    surface.fill(COLOR_BACKGROUND)
    


def main(test=False):
    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global main_menu
    global surface

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Tic-tac-toe')

    # -------------------------------------------------------------------------
    # Create menus
    # -------------------------------------------------------------------------

    # Main menu
    main_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.7),
                                menu_width=int(WINDOW_SIZE[0] * 0.7),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='Play menu',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )

    main_menu.add_option('Start', 
                         play_function,
                         PLAYER1,
                         PLAYER2,
                         BOARD_SIZE)
    main_menu.add_selector('Select Player1: ',
                           [('Human', 'HUMAN PLAYER'),
                            ('MiniMax', 'MINIMAX PLAYER'),
                            ('Q-learning', 'QLEARNING PLAYER'),
                            ('RFC', 'RFC PLAYER'),
                            ],
                           onchange=change_player1,
                           selector_id='select_player1')
    main_menu.add_selector('Select Player2: ',
                           [('Human', 'HUMAN PLAYER'),
                            ('MiniMax', 'MINIMAX PLAYER'),
                            ('Q-learning', 'QLEARNING PLAYER'),
                            ('RFC', 'RFC PLAYER'),
                            ],
                           onchange=change_player2,
                           selector_id='select_player2')
    main_menu.add_selector('Select Board Size: ',
                           [('3', 3),
                            ('4', 4),
                            ('5', 5),
                            ('6', 6),
                            ],
                           onchange=change_board_size,
                           selector_id='select_board_size')
    while True:

        # Paint background
        main_background()

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        main_menu.mainloop(events, disable_loop=test)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()