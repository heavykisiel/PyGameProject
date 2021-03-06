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


class Player(pygame.sprite.Sprite):
    def __init__(self, coords, width, heigth, color):
        self.coords = coords
        self.width = width
        self.heigth = heigth
        self.color = color
        #self.rect = (self.coords.x, self.coords.y, width, heigth)
        img = pygame.image.load('img/player/player_model.png')
        self.image = pygame.transform.scale(img, (img.get_width(), img.get_height()))
        self.rect = self.image.get_rect()
        self.rect.center = (self.coords.x, self.coords.y)
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
        p.move()
        redrawWindow(win, p)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


main()
