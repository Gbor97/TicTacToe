from unittest import TestCase

from game import *


class TestTicTacToeGame(TestCase):
    """Class to run unit tests for the TicTacToeGame class."""

    def test_qlearningplayer_rotate(self):
        """Test case for the check_game_over function.
        Test for game over with a win.
        """
        board = Board(3)
        cont = Controller(PlayerEnum.Human, PlayerEnum.QLearningPlayer, board)
        cont.player2.states_value['110000022'] = 0.1
        cont.player2.states_value['001001202'] = 1
        cont.player2.states_value['110000202'] = 0.2
        board.table[0][0].state = State.X
        board.table[0][1].state = State.X
        board.table[2][2].state = State.O
        move = cont.player2.move()

        self.assertEqual(move, [0,2])
    
    def test_check_win_row(self):
        """Test case for the check_game_over function.
        Test for game over with a win.
        """
        board = Board(3)
        cont = Controller(PlayerEnum.Human, PlayerEnum.Human, board)
        board.table[0][0].state = State.X
        board.table[0][1].state = State.X
        board.table[2][2].state = State.O
        board.table[2][1].state = State.O
        board.move(0, 2, cont.player1)
        winner = cont.checkWin(cont.player1.sign, [0, 2])

        self.assertEqual(winner, cont.player1)
    
    def test_check_win_column(self):
        """Test case for the check_game_over function.
        Test for game over with a loss.
        """
        board = Board(3)
        cont = Controller(PlayerEnum.Human, PlayerEnum.Human, board)
        board.table[0][0].state = State.X
        board.table[1][0].state = State.X
        board.table[2][2].state = State.O
        board.table[2][1].state = State.O
        board.move(2, 0, cont.player1)
        winner = cont.checkWin(cont.player1.sign, [2, 0])

        self.assertEqual(winner, cont.player1)

    def test_check_win_diagonal1(self):
        """Test case for the check_game_over function.
        Test for game over with a loss.
        """
        board = Board(3)
        cont = Controller(PlayerEnum.Human, PlayerEnum.Human, board)
        board.table[0][0].state = State.X
        board.table[1][1].state = State.X
        board.table[2][1].state = State.O
        board.table[2][0].state = State.O
        board.move(2, 2, cont.player1)
        winner = cont.checkWin(cont.player1.sign, [2, 2])

        self.assertEqual(winner, cont.player1)

    def test_check_win_diagonal2(self):
        """Test case for the check_game_over function.
        Test for game over with a loss.
        """
        board = Board(3)
        cont = Controller(PlayerEnum.Human, PlayerEnum.Human, board)
        board.table[0][2].state = State.X
        board.table[1][1].state = State.X
        board.table[2][1].state = State.O
        board.table[2][2].state = State.O
        board.move(2, 0, cont.player1)
        winner = cont.checkWin(cont.player1.sign, [2, 0])

        self.assertEqual(winner, cont.player1)

        def test_check_draw(self):
        """Test case for the check_game_over function.
        Test for game over with a win.
        """
        board = Board(3)
        cont = Controller(PlayerEnum.Human, PlayerEnum.Human, board)
        board.table[0][0].state = State.X
        board.table[0][1].state = State.X
        board.table[0][2].state = State.O
        board.table[1][0].state = State.O
        board.table[1][1].state = State.X
        board.table[1][2].state = State.X
        board.table[2][0].state = State.X
        board.table[2][1].state = State.O
        board.move(2, 2, cont.player2)
        

        self.assertEqual(gameLoop faszság kéne)
