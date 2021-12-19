import pygame
import Enemy
import Player
from Client import screenWidth
class Bullets(pygame.sprite.Sprite):
    bulletGroupEnemy = pygame.sprite.Group()
    bulletGroup = pygame.sprite.Group()
    enemyGroup = pygame.sprite.Group()
    def __init__(self,imgType, x, y, scale, direction,speed):
        pygame.sprite.Sprite.__init__(self)
        #self.flip = False
        self.imgType = imgType
        image = pygame.image.load(f"img/bullet/{self.imgType}.png")
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.speed = speed
        self.direction = direction
        self.bulletGroupEnemy = bulletGroupEnemy
        self.player = Player('player',200,200,0.7,8,20) #Do jebanej poprawy nie wiem gdzie zapisać w kodzie playera, narazie chce żeby to działało wogóle
        
    #def move(self, movingLeft, movingRight):
    #    deltax = 0
    #    deltay = 0

    #    if movingLeft:
     #       deltax = -self.speed
    #        self.flip = True
     #       self.direction = -1
     #   if movingRight:
     #       deltax = self.speed
     #       self.flip = False
     #       self.direction = 1
     #   self.rect.x += deltax
     #   self.rect.y += deltay
    def update(self):
        if self.direction == 1 or self.direction == -1:
            self.rect.x += (self.direction * self.speed)
        if self.direction == 2 or self.direction == -2:
            self.rect.y += ((self.direction/2)* self.speed)
        
            
        if self.rect.right < 0 or self.rect.left > screenWidth:
            self.kill()
        
        
        if pygame.sprite.spritecollide(self.player, bulletGroupEnemy, False):
            if self.player.alive:
                self.player.health -= 2.5
                self.player.healthMin -= 2.5
                #print(player.health)
                self.kill()
        for enemy in enemyGroup:        
            if pygame.sprite.spritecollide(enemy, bulletGroup, False):
                if enemy.alive:
                    enemy.healthMin -=20
                    enemy.health -= 20
                    
                    print(enemy.health)
                    self.kill()
            
#players_group = pygame.sprite.Group()
bulletGroupEnemy = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
#player = Player(int(screenWidth) / 2 ,  screenHeight - 100, 10, 10 )
#player = Player('player',200,200,0.7,8,20) #Do jebanej poprawy nie wiem gdzie zapisać w kodzie playera, narazie chce żeby to działało wogóle
############################################
enemy = Enemy('enemy',400,400,0.6,4,2.5)
enemy1 = Enemy('enemy',200,300,0.6,4,2.5)
enemy2 = Enemy('enemy',100,500,0.6,4,2.5)
enemy3 = Enemy('enemy',300,100,0.6,4,2.5)

enemyGroup.add(enemy)
enemyGroup.add(enemy1)
#enemyGroup.add(enemy2)
#enemyGroup.add(enemy3)


#players_group.add(player)
#player = Player(200,200,1, 3,8)
#bullet = Bullets(100, 100, 8 , )