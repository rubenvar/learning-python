from tictactoe.player import HumanPlayer, RandomComputerPlayer
from tictactoe.game import TicTacToe, play


if __name__ == '__main__':
    x_player = HumanPlayer('X')
    o_player = RandomComputerPlayer('O')
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)
