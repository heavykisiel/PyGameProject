import pygame

import Enemy as enemy
import Bullets
from Client import screen, screenHeight, screenWidth, red, green
from Bullets import bulletGroup



shoot = False
class Player(pygame.sprite.Sprite):
    def __init__(self,imgType, x, y, scale, speed, speedBullet):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.health = 100  
        self.imgType = imgType
        self.speed = speed
        self.speedBullet = speedBullet
        self.direction = 1
        #self.vertical = 1
        self.flip = False
        self.images = []
        self.index = 0
        for i in range(6):
            img = pygame.image.load(f"img/{self.imgType}/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.healthMax = 100
        self.healthMin = self.health
        self.rect.center = [x,y]
        self.shootCooldown = 0
        self.counterOfMoves= 0
        self.lastShot = pygame.time.get_ticks()
        self.healthTimer = 0

    def move(self, movingLeft, movingRight,movingUP, movingDOWN ):
        
        deltax = 0
        deltay = 0
        
        if movingLeft:
            deltax = -self.speed
            self.flip = True
            self.direction = -1
        if movingRight:
            deltax = self.speed
            self.flip = False
            self.direction = 1

        if movingDOWN:
            deltay = self.speed
            #self.vertical = 1
            self.direction = 2
        if movingUP:
            deltay = -self.speed
            #self.vertical = -1
            self.direction = -2
        

        self.rect.x += deltax
        self.rect.y += deltay
    def shoot(self):
        
        if self.shootCooldown ==0:
            self.shootCooldown = 20
            if self.direction == 1 or self.direction == -1:
                bullet = Bullets("bullet",self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery,1, self.direction,self.speedBullet)
                bulletGroup.add(bullet)
            else:
                if self.direction == 2: 
                    bullet = Bullets("bullet",self.rect.centerx, self.rect.centery  + (0.5 * self.rect.size[0] * self.direction),1, self.direction, self.speedBullet)
                    bulletGroup.add(bullet)
                else:
                    bullet = Bullets("bullet",self.rect.centerx, self.rect.centery +(0.5 * self.rect.size[0] * self.direction),1, self.direction, self.speedBullet)
                    bulletGroup.add(bullet)
    #def animation(self):
    def changeImage(self):  #zmiana avatara playera
        if self.direction == 1 and shoot == False:
            self.image = self.images[4]
        elif self. direction == 1:
            self.image = self.images[0]
        if self.direction == -1 and shoot == False:
            self.image = self.images[5]    
        elif self.direction == -1:
            self.image = self.images[3]
        elif self.direction == 2 and shoot == False:
            self.image = self.images[5]
        elif self.direction == 2:
            self.image = self.images[1]
        elif self.direction == -2 and shoot == False:
            self.image = self.images[5]
        elif self.direction == -2:
            self.image = self.images[2] 


    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
           
  
    def healthRegenerator(self):   # regeneracja zycia jesli moby nie bija
        if self.healthTimer ==0:
            
            if player.health < 100 and enemy.shoot == False:  
                player.health +=1
                
                player.healthMin +=1
                self.healthTimer = 50
                print(self.health)
                
    def draw(self):
        screen.blit(self.image, self.rect)
    def update(self):
        if self.shootCooldown > 0:
            self.shootCooldown -= 1
        if self.healthTimer > 0:
            self.healthTimer -= 1
        self.healthRegenerator()
        self.check_alive()
        key = pygame.key.get_pressed()
        #cooldown = 100
        #time_now = pygame.time.get_ticks()
        #if key[pygame.K_SPACE] and time_now - self.lastShot > cooldown:
         #   bullet  = Bullets(self.rect.centerx, self.rect.top)
         #   bullet_group.add(bullet)
         #   self.lastShot = time_now
        #speed = 8
        if self.rect.left > 0:
            self.rect.x -= self.speed
        if (self.rect.right+10) < screenWidth:
            self.rect.x += self.speed
        if (self.rect.bottom + 10) > screenHeight:
            self.rect.y -= self.speed
        if self.rect.top < 0:
            self.rect.y += self.speed
        pygame.draw.rect(screen, red, (self.rect.x,(self.rect.bottom +5),self.rect.width, 5))
        if self.healthMin >0:
            pygame.draw.rect(screen, green, (self.rect.x,(self.rect.bottom +5),int(self.rect.width * (self.healthMin / self.healthMax)), 5))
        if self.health == 0:
            self.kill()


