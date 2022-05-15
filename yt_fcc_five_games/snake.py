import random
import pygame
import tkinter as tk
from tkinter import messagebox


# each cube
class Cube(object):
    w = 500
    rows = 25

    def __init__(self, start, dirx=1, diry=0, color=(255, 0, 0)):
        self.pos = start
        self.dirx = 1
        self.diry = 0
        self.color = color

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        # +1 and -2 so we can see the grid and the cube doesn't completely fill the square
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        # eyes
        if eyes:
            center = dis // 2
            radius = 3
            circle_1_middle = (i*dis+center-radius, j*dis+8)
            circle_2_middle = (i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circle_1_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_2_middle, radius)


# composed of Cubes
class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        # create the head at passed position
        self.head = Cube(pos)
        # store the head in the body
        self.body.append(self.head)
        # what direction the snake is moving (always only one direction = one of them is 0)
        self.dirx = 0
        self.diry = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # gets all keys that can be pressed = can detect two keys pressed at once = move diagonally, etc.
            keys = pygame.key.get_pressed()

            for _ in keys:
                if keys[pygame.K_LEFT]:
                    self.dirx = -1
                    self.diry = 0
                    # store where the head is (key) and what direction it turned (value)
                    # so the cubes turn where the head did, when they arrive
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pygame.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pygame.K_UP]:
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pygame.K_DOWN]:
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            # turn each cube when thay reach the turn location
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    # after last cube turns, remove from turn registry
                    self.turns.pop(p)
            # or move them
            else:
                # if edge, appear on the other side
                if c.dirx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirx == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])
                elif c.diry == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.diry == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                else:
                    # advance
                    c.move(c.dirx, c.diry)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 0
        self.diry = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry

        # where to add the cube depending on what direction is the snake moving
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
        if dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
        if dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))

        # what drection to move the cube after it's added
        self.body[-1].dirx = dx
        self.body[-1].diry = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                # draw eyes only in first cube (head)
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_grid(w, rows, surface):
    grid_color = (120, 120, 120)
    size_between = w // rows

    x = 0
    y = 0

    for _ in range(rows):
        # each time increase the x and y by the "grid size"
        x += size_between
        y += size_between
        # and draw lines
        pygame.draw.line(surface, grid_color, (0, y),
                         (w, y))  # horizontal line (constant y)
        pygame.draw.line(surface, grid_color, (x, 0),
                         (x, w))  # vertical line (constant x)


def redraw_window(surface):
    global width, rows, snake, snack
    surface.fill((0, 0, 0))
    snake.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()


def random_snack(rows, snake):
    positions = snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        # check all the current positions of snake body
        # to not put the snack on them
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    # root.attributes("-topmost", True)  # window appears on top
    root.withdraw()  # invisible
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, snake, snack
    width = 500
    rows = 25
    win = pygame.display.set_mode((width, width))
    snake = Snake((255, 0, 0), (10, 10))
    snack = Cube(random_snack(rows, snake), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        # delay to make the game go a little slower. lower = faster
        pygame.time.delay(50)
        clock.tick(10)  # run at 10 frames per second. lower = slower
        snake.move()  # go
        # if snake eats snack
        if snake.body[0].pos == snack.pos:
            # add cube to snake if it eats the snack:
            snake.add_cube()
            # and draw new snack
            snack = Cube(random_snack(rows, snake), color=(0, 255, 0))

        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x+1:])):
                print('Score', len(snake.body))
                message_box("You lost", "Play again...")
                snake.reset((10, 10))
                break
        redraw_window(win)

    pass

# rows =
# w =
# h =

# Cube.rows = rows
# Cube.w = w


main()
