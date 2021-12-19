import pygame
from pygame.locals import *
import random

import Bullets
import Player
player = Player.player

clock = pygame.time.Clock()
fps = 60


screenWidth = 800
screenHeight = 800

screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Makingstupidthings")

red = (255,0,0)
green = (0,255,0)
Size = 100
movingLeft = False
movingRight = False
movingUP = False
movingDOWN = False
shoot = False
#player = Player(200,200,1, 3,8)


background = pygame.image.load("img/background/background.png")

def draw_background():
    screen.blit(background,(0,0))

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
           
    def shoot(self):
        
        if self.shootCooldown ==0:
            self.shootCooldown = 20
            if self.direction == 1 or self.direction == -1:
                bullet = Bullets("bullet",self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery,1, self.direction,self.speedBullet)
                Bullets.bulletGroup.add(bullet)
            else:
                if self.direction == 2: 
                    bullet = Bullets("bullet",self.rect.centerx, self.rect.centery  + (0.5 * self.rect.size[0] * self.direction),1, self.direction, self.speedBullet)
                    Bullets.bulletGroup.add(bullet)
                else:
                    bullet = Bullets("bullet",self.rect.centerx, self.rect.centery +(0.5 * self.rect.size[0] * self.direction),1, self.direction, self.speedBullet)
                    Bullets.bulletGroup.add(bullet)
    #def animation(self):
    def healthRegenerator(self):   # regeneracja zycia jesli moby nie bija
        if self.healthTimer ==0:
            
            if Bullets.player.health < 100 and enemy.shoot == False:  
                Bullets.player.health +=1
                
                Bullets.player.healthMin +=1
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




class Enemy(pygame.sprite.Sprite):
    def __init__(self,imgType, x, y, scale, speed, speedBullet):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.health = 100  
        self.imgType = imgType
        self.speed = speed
        self.speedBullet = speedBullet
        self.direction = 1 # moze byc 1,-1 lub 0 (0 w przypadku jak jest velocity 2 lub -2)
        self.velocity = 2 # moze byc 2 lub -2 
        self.flip = False
        image = pygame.image.load(f"img/enemy/{self.imgType}.png")
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.healthMax = 100
        self.healthMin = self.health
        self.rect.center = [x,y]
        self.shootCooldown = 0
        
        self.lastShot = pygame.time.get_ticks()
        self.randomRun = False 
        self.randomRun2 = False
        self.randomRunCounter = 0
        self.randomRunCounter2 =0
        self.visibilityLeft = pygame.Rect(0,0,800,20)  # 50  width 50 hight od jakiej widocznosci
        self.visibilityRight = pygame.Rect(0,0,800,20)
        self.visibilityBottom = pygame.Rect(0,0,20,800)
        self.visibilityTop = pygame.Rect(0,0,20,800)
        

    def move(self, aiMovingLeft, aiMovingRight,aiMovingUP, aiMovingDOWN ):
        
        deltax = 0
        deltay = 0
        
        if aiMovingLeft:
            deltax = -self.speed
            #self.flip = True
            self.direction = -1
        if aiMovingRight:
            deltax = self.speed
            #self.flip = False
            self.direction = 1

        if aiMovingDOWN:
            deltay = self.speed
            self.velocity = 2
            
        if aiMovingUP:
            deltay = -self.speed
            self.velocity = -2
            
        

        self.rect.x += deltax
        self.rect.y += deltay
    def AI(self):
        
       #aiMovingLeft = False
        #aiMovingDOWN = False
        #aiMovingUP = False
        #aiMovingRight = False
        
        if self.alive and Bullets.player.alive:
            if self.randomRun == False and random.randint(1,100) == 1:   #random module losowanie random od 1,100
                self.randomRun = True
                self.randomRunCounter = 500
                self.direction *= -1
                self.velocity *= -1
                

            
            elif self.visibilityLeft.colliderect(Bullets.player.rect):
                self.direction = -1
                self.shoot()
            elif self.visibilityRight.colliderect(Bullets.player.rect):
                self.direction = 1
                self.shoot()
            elif self.visibilityTop.colliderect(Bullets.player.rect):
                self.velocity = -2
                self.direction = 0
                self.shoot()
            elif self.visibilityBottom.colliderect(Bullets.player.rect):
                self.velocity = 2
                self.direction = 0
                self.shoot()
            
                    
            
            else:
                    
                if self.randomRun == False:
                    
                    if self.direction == 1:
                        aiMovingRight = True
                        aiMovingUP = False
                        aiMovingLeft = False
                        aiMovingDOWN = False
                       
                    
                    elif self.direction == -1:                        
                       
                        aiMovingRight = False
                        aiMovingUP= False
                        aiMovingDOWN = False
                        aiMovingLeft = True
                        self.direction == 1
                        
                    elif self.direction == 0 and self.velocity == 2:
                        aiMovingRight = False
                        aiMovingUP= False
                        aiMovingDOWN = True
                        aiMovingLeft = False
                        self.direction ==1
                        
                    elif self.direction == 0 and self.velocity == -2:
                            
                        aiMovingRight = False
                        aiMovingUP= True
                        aiMovingDOWN = False
                        aiMovingLeft = False
                        self.direction ==1
                        
                                    
                    
                    self.move(aiMovingLeft,aiMovingRight,aiMovingUP,aiMovingDOWN)
                    
                  
                    self.visibilityLeft.center = (self.rect.left - 300,self.rect.centery)   # zasieg mobów
                    self.visibilityRight.center = (self.rect.left +300, self.rect.centery )
                    self.visibilityTop.center = (self.rect.centerx, self.rect.centery -300)
                    self.visibilityBottom.center = (self.rect.centerx, self.rect.centery + 300)
                    #pygame.draw.rect(screen,red,self.visibilityRight)
                    #pygame.draw.rect(screen,green,self.visibilityLeft)
                    #pygame.draw.rect(screen,green,self.visibilityTop)
                    #pygame.draw.rect(screen,green,self.visibilityBottom)

                else:
                    self.randomRunCounter -= 1
                    self.randomRunCounter2 -=1  

                
                    if self.randomRunCounter <= 0:
                        self.randomRun = False
                    elif self.randomRunCounter2 <= 0:
                        self.randomRun = False
                        
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.shoot = False
            if Bullets.player.health <80:
                Bullets.player.healthMin +=20
                Bullets.player.health +=20

    def shoot(self):
        
        if self.shootCooldown ==0:
            self.shootCooldown = 30
            if self.direction == 1 or self.direction == -1:
                bullet = Bullets("bullet",self.rect.centerx + (0.75 * self.rect.size[0] * self.direction),self.rect.centery,2, self.direction,self.speedBullet)
                Bullets.bulletGroupEnemy.add(bullet)
            else:
                if self.velocity == 2: 
                    bullet = Bullets("bullet",self.rect.centerx, self.rect.centery  + (0.5 * self.rect.size[0] * self.velocity) ,2, self.velocity, self.speedBullet)
                    Bullets.bulletGroupEnemy.add(bullet)
                else:
                    bullet = Bullets("bullet",self.rect.centerx, self.rect.centery +(0.5 * self.rect.size[0] * self.velocity),2, self.velocity, self.speedBullet)
                    Bullets.bulletGroupEnemy.add(bullet)
    
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    def update(self):
        if self.shootCooldown > 0:
            self.shootCooldown -= 1

        self.check_alive()
        
        if self.rect.left > 100:
            self.rect.x -= self.speed
            #self.direction = 1
            
        if (self.rect.right+100) < screenWidth:
            self.rect.x += self.speed
            #self.direction = -1
            
        if (self.rect.bottom + 100) > screenHeight:
            self.rect.y -= self.speed
            self.direction = 1
        if self.rect.top < 10:
            self.rect.y += self.speed
            self.direction = -1
        pygame.draw.rect(screen, red, (self.rect.x,(self.rect.bottom +5),self.rect.width, 5))
        if self.healthMin >0:
            pygame.draw.rect(screen, green, (self.rect.x,(self.rect.bottom +5),int(self.rect.width * (self.healthMin / self.healthMax)), 5))
        if self.health == 0:
            self.kill()



run=True
while run:

    clock.tick(fps)
    draw_background()

    Bullets.player.move(movingLeft,movingRight,movingUP, movingDOWN)
    Bullets.player.changeImage()
    Bullets.player.draw()
    Bullets.player.update()
    if Bullets.player.health == 0:
        
        run = False
    
    Bullets.bulletGroup.update()
    Bullets.bulletGroup.draw(screen)
    Bullets.bulletGroupEnemy.update()
    Bullets.bulletGroupEnemy.draw(screen)
    
    for enemy in Bullets.enemyGroup:
        enemy.AI()
        enemy.update()
        enemy.draw()
        

    if Bullets.player.alive:
        if shoot:
            Bullets.player.shoot()


    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_LEFT:
                movingLeft = True
                
            if event.key == pygame.K_RIGHT:
                movingRight = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_UP:
                movingUP = True
            if event.key == pygame.K_DOWN:
                movingDOWN =  True
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                movingLeft = False
            if event.key == pygame.K_RIGHT:
                movingRight = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_UP:
                movingUP = False
            if event.key == pygame.K_DOWN:
                movingDOWN =  False
        
    #bullet.update()
    pygame.display.update()
pygame.quit()


