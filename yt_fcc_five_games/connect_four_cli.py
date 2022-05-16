import numpy as np

ROW_COUNT = 6
COL_COUNT = 7
WIN_SIZE = 4


def create_board():
    board = np.zeros((ROW_COUNT, COL_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    # if the top row of the selected column is still available (has a 0)
    # it means the column selected is correct, not filled up
    return board[ROW_COUNT-1][col] == 0


def get_next_open_row(board, col):
    # find next available row where the piece can go
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # one way of doing it is checking the whole board for a winning combination after each move
    # check horizontals
    for c in range(COL_COUNT-(WIN_SIZE-1)):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # check verticals
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT-(WIN_SIZE-1)):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # check diagonals up
    for c in range(COL_COUNT-(WIN_SIZE-1)):
        for r in range(ROW_COUNT-(WIN_SIZE-1)):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # check diagonals down
    for c in range(COL_COUNT-(WIN_SIZE-1)):
        for r in range((WIN_SIZE-1), ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


board = create_board()
print_board(board)
game_over = False
turn = 0

while not game_over:
    # ask for player 1 input
    if turn == 0:
        col = int(input("Player 1, choose column (0-6): "))

        # make the move
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

            if winning_move(board, 1):
                print("🎊 Player 1 wins!")
                game_over = True

    # ask for player 2 input
    else:
        col = int(input("Player 2, choose column (0-6): "))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                print("🎊 Player 2 wins!")
                game_over = True

    print_board(board)

    # turn will alternate between 0 and 1
    turn = (turn + 1) % 2
