import pygame

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0


class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Player:
    def __init__(self, coords, width, height, color):
        self.coords = coords
        self.width = width
        self.heigth = height
        self.color = color
        self.rect = (self.coords.x, self.coords.y, width, height)
        self.vel = 10

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.coords.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.coords.x += self.vel

        if keys[pygame.K_UP]:
            self.coords.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.coords.y += self.vel
        self.rect = (self.coords.x, self.coords.y, self.heigth, self.heigth)


def redrawWindow(win, player):

    win.fill((255, 255, 255))
    player.draw(win)
    pygame.display.update()


def main():
    run = True
    p = Player(Coords(1, 1), 10, 10, (0, 255, 0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()
        redrawWindow(win, p)


main()
