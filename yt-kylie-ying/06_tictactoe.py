import time
from tictactoe.player import HumanPlayer, RandomComputerPlayer
from tictactoe.game import TicTacToe


def play(game, x_player, o_player, print_game=True):
    # return the winner (the letter) or None for a tie
    if print_game:
        game.print_board_nums()

    letter = 'X'  # starting letter
    # iterate while the game has empty squares
    # (don't worry about winner, it will break the loop and return)
    while game.empty_squares():
        # get the move from the player
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print('\n' + letter + f' makes a move to square {square}')
                game.print_board()
                print('')  # empty line

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter

            # after move, alternate letters
            letter = 'O' if letter == 'X' else 'X'  # switch players

        # tiny break
        time.sleep(0.8)

    if print_game:
        print('It\'s a tie!')


if __name__ == '__main__':
    x_player = HumanPlayer('X')
    o_player = RandomComputerPlayer('O')
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)
