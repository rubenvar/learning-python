import pygame
from network import Network

width = 500
height = 500

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')

GREEN = (0, 255, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
CLIENT_NUMBER = 0


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        # move on key press
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def read_pos(str):
    # "decode" position string into tupple
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    # "enconde" position tupple into string
    return str(tup[0]) + "," + str(tup[1])


def redraw_window(win, player, player2):
    win.fill(WHITE)
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    # get the starting position on first connection
    start_pos = read_pos(n.get_pos())
    p = Player(start_pos[0], start_pos[1], 100, 100, GREEN)
    p2 = Player(0, 0, 100, 100, GREY)
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        # send current position to server
        # will get the other player's position as a response
        p2_pos = n.send(make_pos((p.x, p.y)))
        p2_pos = read_pos(p2_pos)
        p2.x = p2_pos[0]
        p2.y = p2_pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()
        redraw_window(win, p, p2)


main()
