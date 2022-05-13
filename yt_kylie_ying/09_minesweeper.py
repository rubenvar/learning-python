import random
import re


# create a board object to represent the minesweeer game
class Board:
    def __init__(self, dim_size, num_bombs):
        # 1. keep track of these parameters
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # 2. create the board
        self.board = self.make_new_board()  # plant bombs
        self.assing_values_to_board()

        # 3. set to track the locations uncovered: (row, col) tuples into this set
        self.dug = set()  # so if dig at (0, 0) => self.dug({0,0})

    def make_new_board(self):
        # construct new board with dim size and num bombs
        # construct the list of lists here

        # generate a square board from the dim size param
        board = [[None for _ in range(self.dim_size)]
                 for _ in range(self.dim_size)]

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            # each location has an "id" (from 0 to square of dim_size - 1 (max size))
            loc = random.randint(0, self.dim_size**2 - 1)
            # get position of that location
            row = loc // self.dim_size  # number of times dim_size goes into loc is the row
            col = loc % self.dim_size  # remainer is the index of column in that row

            if board[row][col] == '*':
                # there is a bomb there already, don't increase, keep going
                continue

            board[row][col] = '*'  # plant the bomb
            bombs_planted += 1

        return board

    def assing_values_to_board(self):
        # precompute and assign a value (0-8) to each location so we know how many bombs it has around
        # instead of having to check every time for every location later
        # check every col in every row:
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if it's a bomb, don't calculate
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # iterate through each of the neighboring positions + sum number of bombs

        # top left: (row-1, col-1)
        # top middle: (row-1, col)
        # top right: (row-1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle: (row+1, col)
        # bottom right: (row+1, col+1)

        num_neighboring_boms = 0
        # every combination of the 3x3 grid around the position (row, col) passed
        # with the max() and min() to make sure to not go out of bounds
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    # original location, don't check
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_boms += 1

        return num_neighboring_boms

    def dig(self, row, col):
        # dig at location
        # return True if successful dig, False if bomb

        # hit a bomb -> game over
        # location with neighboring bombs -> finish dig
        # location with no neighboring bombs -> recursively dig neighbors

        self.dug.add((row, col))  # keep track that it's dug

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        # keep digging: check neighboring for numbers
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue  # don't dig if already dug
                self.dig(r, c)  # recurse

        # if initial not bomb, we shouldn't hit a bomb here
        return True

    def __str__(self):
        # magic function: it'll print the return
        # returns a string with the board

        # create a new array that represents the output
        visible_board = [[None for _ in range(
            self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # into a nice string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(len(max(columns, key=len)))

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


def play(dim_size=10, num_bombs=10):
    # play the game:
    # 1. create the board + plant the bombs
    # 2. show the user the board + ask where to dig
    # 3a. if bomb, show game over
    # 3a. if not bomb, dig recursively until each square is next to at least one bomb
    # 4. repeat 2 and 3 until no more places to dig -> Victory!

    # 1.
    board = Board(dim_size, num_bombs)

    safe = True
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        # 2.
        print(board)
        # regex to handle spaces after comma
        user_input = re.split(
            ',(\\s)*',
            input("Where would you like to dig? Input as 'row,col': ")
        )
        row, col = int(user_input[0]), int(user_input[-1])
        # check input
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Please try again.")
            continue
        # if valid, dig
        safe = board.dig(row, col)

        if not safe:
            break  # dug a bomb, game over

    # 3.
    # 2 options
    if safe:
        # 3b.
        print("🎊 Congratulations, you win!")
    else:
        # 3a.
        print("💣 Sorry, bomb. Game over!")
    # reveal the whole board at the end
    board.dug = [(r, c) for r in range(board.dim_size)
                 for c in range(board.dim_size)]
    print(board)


if __name__ == '__main__':  # good practice
    play()
