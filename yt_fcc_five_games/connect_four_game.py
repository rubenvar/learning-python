import numpy as np
import pygame

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PINK = (255, 0, 255)
GREEN = (0, 255, 0)

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

# draw the graphics


def draw_board(board, screen):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r *
                             SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            gap_color = BLACK
            if board[r][c] == 1:
                gap_color = PINK
            elif board[r][c] == 2:
                gap_color = GREEN

            pygame.draw.circle(screen, gap_color, (int(
                c*SQUARE_SIZE + SQUARE_SIZE/2), int(r*SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)
            pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2 - 10)
width = COL_COUNT * SQUARE_SIZE
height = (ROW_COUNT+1) * SQUARE_SIZE

size = width, height

screen = pygame.display.set_mode(size)
draw_board(np.flip(board, 0), screen)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(
                    screen, PINK, (posx, int(SQUARE_SIZE/2)), RADIUS)
            elif turn == 1:
                pygame.draw.circle(
                    screen, GREEN, (posx, int(SQUARE_SIZE/2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))

            # player 1
            if turn == 0:
                posx = event.pos[0]
                col = int(posx / SQUARE_SIZE)
                # make the move
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!", 1, PINK)
                        screen.blit(label, (40, 10))
                        game_over = True

            # player 2
            else:
                posx = event.pos[0]
                col = int(posx / SQUARE_SIZE)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins!", 1, GREEN)
                        screen.blit(label, (40, 10))
                        game_over = True

            # turn will alternate between 0 and 1
            turn = (turn + 1) % 2

            print_board(board)
            draw_board(np.flip(board, 0), screen)

            if game_over:
                pygame.time.wait(3000)
