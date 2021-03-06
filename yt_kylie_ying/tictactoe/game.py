# TicTacToe class and play function for the 06 and 07 TicTacToe games
import time


class TicTacToe:
    def __init__(self):
        # we will use a single list to rep 3x3 board
        self.board = [' ' for _ in range(9)]
        self.current_winner = None  # keep track of winner

    def print_board(self):
        # each row
        for row in [self.board[i*3:(i+1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j*3, (j+1)*3)]
                        for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        # if valid move, make a move (assign square to letter), return true
        # if invalid, return false
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # winner if 3 in a row anywhere: we have to check all of them

        # check rows
        row_ind = square // 3
        row = self.board[row_ind*3: (row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True  # 3 in a row, win!

        # check columns
        col_ind = square % 3
        col = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in col]):
            return True  # 3 in a column, win!

        # check diagonals
        # only squares in a diagonal are even numbers
        if square % 2 == 0:  # it's even
            # check left to right diagonal
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            # check right to left diagonal
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        # if all the checks fail, keep going
        return False


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
        if print_game:
            time.sleep(0.8)

    if print_game:
        print('It\'s a tie!')
