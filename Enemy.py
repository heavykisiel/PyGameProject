import pygame
import random
import Bullets
import Player as player
from Client import screenWidth, screenHeight, screen, red, green
from Bullets import bulletGroupEnemy

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
        
        if self.alive and player.alive:
            if self.randomRun == False and random.randint(1,100) == 1:   #random module losowanie random od 1,100
                self.randomRun = True
                self.randomRunCounter = 500
                self.direction *= -1
                self.velocity *= -1
                

            
            elif self.visibilityLeft.colliderect(player.rect):
                self.direction = -1
                self.shoot()
            elif self.visibilityRight.colliderect(player.rect):
                self.direction = 1
                self.shoot()
            elif self.visibilityTop.colliderect(player.rect):
                self.velocity = -2
                self.direction = 0
                self.shoot()
            elif self.visibilityBottom.colliderect(player.rect):
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
            if player.health <80:
                player.healthMin +=20
                player.health +=20

    def shoot(self):
        
        if self.shootCooldown ==0:
            self.shootCooldown = 30
            if self.direction == 1 or self.direction == -1:
                bullet = Bullets("bullet",self.rect.centerx + (0.75 * self.rect.size[0] * self.direction),self.rect.centery,2, self.direction,self.speedBullet)
                bulletGroupEnemy.add(bullet)
            else:
                if self.velocity == 2: 
                    bullet = Bullets("bullet",self.rect.centerx, self.rect.centery  + (0.5 * self.rect.size[0] * self.velocity) ,2, self.velocity, self.speedBullet)
                    bulletGroupEnemy.add(bullet)
                else:
                    bullet = Bullets("bullet",self.rect.centerx, self.rect.centery +(0.5 * self.rect.size[0] * self.velocity),2, self.velocity, self.speedBullet)
                    bulletGroupEnemy.add(bullet)
    
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
