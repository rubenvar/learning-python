import pygame
import random

# setting up global vars
# creating the data structure for pieces
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700

horizontal_blocks = 10
vertical_blocks = 20
block_size = 30

play_width = horizontal_blocks * block_size  # 300
play_height = vertical_blocks * block_size  # 600

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

GREY = (128, 128, 128)
WHITE = (255, 255, 255)

# SHAPE FORMATS
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
                (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    # creates a list of (20) lists of (10) lists of (black) colors
    grid = [[(0, 0, 0) for _ in range(horizontal_blocks)]
            for _ in range(vertical_blocks)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # if (i,j) position is in locked_positions
            if (j, i) in locked_positions:
                # change it from (0,0,0) color
                # to whatever color is stored in locked_positions
                c = locked_positions[(j, i)]
                grid[i][j] = c

    return grid


def get_shape_format(shape):
    # get the current format from the list of lists of formats
    return shape.shape[shape.rotation % len(shape.shape)]
    # Example:
    # for:
    # - shape = T
    # - position = 2
    # - len(T.shape) = 4
    # format = T[2 % 4] = T[2] = one of the sublists ([....., ..00.], etc.)


def convert_shape_format(shape):
    # return the actual positions taken by the current piece in it's current format
    positions = []
    format = get_shape_format(shape)

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                # current position + where the shape is in the current format
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        # formats have empty '.'s that we need to fix the offset for (-2, -4):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    # get every possible position in the 10x20 (hor_blocks x vert_blocks) grid
    # if they are empty ((0,0,0) color)
    accepted_pos = [[(j, i) for j in range(horizontal_blocks) if grid[i][j] == (0, 0, 0)]
                    for i in range(vertical_blocks)]  # list of lists of tuples
    # into one dimensional list (flatten the list)
    accepted_pos = [j for sub in accepted_pos for j in sub]  # list of tuples

    # current positions of the shape
    formatted = convert_shape_format(shape)

    # compare current positions with allowed positions and return it
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    # if any y is < 1, we are above the top and we lost 😞
    for pos in positions:
        _, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('Oxigen', size, bold=True)
    label = font.render(text, True, color)

    # center the text in the middle of the screen
    surface.blit(label, (top_left_x + play_width/2 - label.get_width() /
                 2, top_left_y + play_height/2 - label.get_height()/2))


def draw_grid(surface, grid):
    for i in range(len(grid)):
        x = top_left_x
        y = top_left_y + i*block_size  # horizontal line => constant y
        pygame.draw.line(surface, GREY, (x, y), (x+play_width, y))
        for j in range(len(grid[i])):
            x = top_left_x + j*block_size  # vertical line => constant x
            y = top_left_y
            pygame.draw.line(surface, GREY, (x, y), (x, y+play_height))


def clear_rows(grid, locked):
    removed_rows_count = 0
    # (for loop backwards)
    for i in range(len(grid)-1, -1, -1):
        # in each row
        row = grid[i]
        # if there is no (0,0,0), it's full of pieces
        if (0, 0, 0) not in row:
            removed_rows_count += 1
            removed_row_ind = i
            # so clear each of those positions in locked_positions
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    # so we end up with the grid having one less row at the bottom (~)

    # after deleting whole row at the bottom
    # we need to:
    # - shift every row down to "fill that gap"
    # - and add a new row at the top so the grid is not shorter every time
    if removed_rows_count > 0:
        # if inc > 0, we have removed at least one row
        # ⬇ this sorts the list of locked positions based on the y, and loops backwards
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < removed_row_ind:
                # rows that are above the removed one
                new_key = (x, y+removed_rows_count)
                # get the last row values (colors) and add them at the new key
                locked[new_key] = locked.pop(key)

    # return how many rows removed to count that for the score
    return removed_rows_count


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('Oxygen', 20)
    label = font.render('Next shape:', True, WHITE)

    # placement
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    # draw a constant image outside the grid, not moving
    # (that's why we don't reuse the convert_shape_format function)
    format = get_shape_format(shape)
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size,
                                 sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def get_max_score():
    # read score from file
    with open('assets/score.txt', 'r') as f:  # open file to read
        lines = f.readlines()  # get lines
        score = lines[0].strip()  # get first line and clean it

    return score


def update_score(nscore):
    # keeps score in a file after games
    score = get_max_score()

    with open('assets/score.txt', 'w') as f:  # open file to write
        if int(score) > nscore:
            f.write(str(score))  # keep old
        else:
            f.write(str(nscore))  # write new


def draw_window(surface, grid, score=0, max_score=0):
    # paint all black
    surface.fill((0, 0, 0))

    # write the title
    font = pygame.font.SysFont('Oxygen', 60)
    label = font.render('Tetris', True, WHITE)
    # placement: "center" of the screen
    surface.blit(label, (top_left_x + play_width /
                 2 - label.get_width()/2, block_size))

    # write the current score
    font = pygame.font.SysFont('Oxygen', 20)
    label = font.render('Score: ' + str(score), True, WHITE)
    # placement
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    # write
    surface.blit(label, (sx + 10, sy + 160))

    # write the max score
    label = font.render('Max score: ' + str(max_score), True, WHITE)
    # placement
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    # write
    surface.blit(label, (sx + 10, sy + 200))

    # paint with the colors kept in grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size,
                             top_left_y + i*block_size, block_size, block_size), 0)

    # border around play area
    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x,
                     top_left_y, play_width, play_height), 4)


def main(surface):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()

    clock = pygame.time.Clock()

    fall_time = 0
    fall_speed = 0.27
    level_time = 0

    max_score = get_max_score()
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()  # adds time since last while iteration

        # increase the speed every 5 seconds
        if level_time/1000 > 5:
            level_time = 0
            # 0.12 == minimum it can get to while still being playable
            if fall_speed > 0.12:
                # how much it increases every time
                fall_speed -= 0.001

        # auto move down until the piece gets to the bottom
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1  # move the piece down
            # check if we are at the bottom:
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1  # revert
                change_piece = True  # and chenge to next piece

        # respond to keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1  # move
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1  # move
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1

                if event.key == pygame.K_DOWN:
                    current_piece.y += 1  # move
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1

                if event.key == pygame.K_UP:
                    current_piece.rotation += 1  # rotate
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        # current shape position
        shape_pos = convert_shape_format(current_piece)

        # paint the piece positions if they are inside grid (y > -1)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # when we need to change piece
        if change_piece:
            # lock the current piece
            for pos in shape_pos:
                # add piece positions to locked_positions list and paint them
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            # get the new piece
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            # clear the rows after locking the piece and getting the new one
            score += clear_rows(grid, locked_positions) * horizontal_blocks

        # draw things
        draw_window(surface, grid, score, max_score)
        draw_next_shape(next_piece, surface)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(surface, 'You lost!', 100, WHITE)
            pygame.display.update()
            pygame.time.delay(1500)  # delay to see the 'you lost' text
            run = False
            update_score(score)  # keep score in file


def main_menu(surface):
    run = True
    while run:
        surface.fill((0, 0, 0))
        draw_text_middle(surface, 'Press any key to play', 50, WHITE)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # default quit
            if event.type == pygame.KEYDOWN:
                main(surface)  # start when they press any key

    pygame.display.quit()


surface = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')  # window title

main_menu(surface)  # start game
