import pygame
import numpy as np
import random

import bullet

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

windowWidth = 1000
windowHeight = 600

class Tank():
    def __init__(self, xPos, yPos, orientation = 1, tankWidth = 40, tankHeight = 20, barrelLength = 5, color = RED):
        
        #values for drawing tank
        self.color = color
        self.tankWidth = tankWidth
        self.tankHeight = tankHeight
        self.barrelLength = barrelLength

        self.state = [xPos, yPos]       #no velocity because not adding physics to tank 
        self.orientation = orientation  #orientation: 1 = facing right, -1 = facing left

        self.rect = pygame.Rect(self.state[0], self.state[1], self.tankWidth, self.tankHeight)
        
        self.hp = 100
        self.fuel = 100
        self.objectType = 'tank'

        #default values for bullet
        self.aimSpeed = 20
        self.aimAngle = 45

        self.bullets = ['shell'] #maybe just use ints? 0 = normal, 1 = bouncy, 2 = reflecting...
        self.currentBullet = 0
    
    def move(self, direction = 0):
        #direction can be -1 (left), or +1 (right)
        if self.fuel <= 0:
            pass
        elif self.state[0] < 0:
            self.state[0] = 0
        elif self.state[0] > windowWidth - self.tankWidth:
            self.state[0] = windowWidth - self.tankWidth
        elif self.state[0] > 400 -self.tankWidth and self.state[0] < 410:
            self.state[0] = 400 - self.tankWidth
        elif self.state[0] < 620 and self.state[0] > 590:
            self.state[0] = 620
        else:
            self.state[0] = self.state[0] + direction
            # print(self.state[0])
            self.fuel = self.fuel - 1

        self.rect.x, self.rect.y = self.state[0], self.state[1]
    
    def changePower(self, power = 0):
        if self.aimSpeed <= 0 and power < 0:
            pass
        elif self.aimSpeed >= 100 and power > 0:
            pass
        else:
            self.aimSpeed = self.aimSpeed + power

    def shiftAimAngle(self, angle):
        if self.aimAngle <= 0 and angle * self.orientation < 0:
            pass
        elif self.aimAngle >= 90 and angle * self.orientation > 0:
            pass
        else:
            self.aimAngle = self.aimAngle + angle * self.orientation

    def addPowerUp(self):
        bulletNumber = random.randint(2, 7)
        print(bulletNumber)
        if bulletNumber == 2:
            self.bullets.append('pierce')
        elif bulletNumber == 3:
            self.bullets.append('bouncy')
        elif bulletNumber == 4:
            self.bullets.append('reflect')
        elif bulletNumber == 5:
            self.bullets.append('firework')
        elif bulletNumber == 6:
            self.bullets.append('volley')
        elif bulletNumber == 7:
            self.bullets.append('rapid')

    def nextBullet(self):
        #in 'main' method where environemnt is run, we can use tank.bullets[self.currentBullet] to get info on the current bullet (to display)
            #quite 'hard-coded' and naive but simple...
        if self.currentBullet >= len(self.bullets) - 1:
            self.currentBullet = 0
        else:
            self.currentBullet = self.currentBullet + 1 
        print('bullet: ', self.bullets[self.currentBullet])
    
    def shoot(self):
        bulletType = self.bullets[self.currentBullet]
        bulletType = 'volley'
        self.bullets.append(bulletType)

        if self.orientation == -1:
            aimAngle = 180 - self.aimAngle
        else: 
            aimAngle = self.aimAngle
        
        aimSpeed = self.aimSpeed + 30

        xPos = self.state[0] + self.tankWidth // 2
        yPos = self.state[1]

        #check what bullet (just multiple if statements... i got lazy)
        if bulletType == 'pierce':
            self.bullets.remove(bulletType)
            newBullet = bullet.Shell()
            newBullet.setup(xPos, yPos, aimSpeed, aimAngle, 3)
        elif bulletType == 'bouncy':
            self.bullets.remove(bulletType)
            newBullet = bullet.BouncyBullet()
            newBullet.setup(xPos, yPos, aimSpeed, aimAngle, 3)
        elif bulletType == 'reflect':
            self.bullets.remove(bulletType)
            newBullet = bullet.ReflectingBullet()
            newBullet.setup(xPos, yPos, aimSpeed, aimAngle, 3)
        elif bulletType == 'firework':
            self.bullets.remove(bulletType)
            newBullet = bullet.Firework()
            newBullet.setup(xPos, yPos, aimSpeed, aimAngle, 5)
        elif bulletType == 'volley':
            self.bullets.remove(bulletType)
            newBullet = bullet.Volley()
            newBullet.setup(xPos, yPos, aimSpeed, aimAngle, 5)
        elif bulletType == 'rapid':
            self.bullets.remove(bulletType)
            newBullet = bullet.Rapid()
            newBullet.setup(xPos, yPos, aimSpeed, aimAngle, 3)
        else: 
            #it's a normal bullet, don't remove it; bulletType == 'shell'
            newBullet = bullet.Shell()
            newBullet.setup(xPos, yPos, aimSpeed, aimAngle, 1)

        self.currentBullet = 0
        return newBullet

    def draw(self, screen):
            
        #drawing the tank
        pygame.draw.rect(screen, self.color, self.rect)

        #drawing the barrel
        barrelXPos = self.state[0] + self.tankWidth / 2 + np.cos(np.radians(self.aimAngle)) * 20 * self.orientation
        barrelYPos = self.state[1] - np.sin(np.radians(self.aimAngle)) * 20
        pygame.draw.line(screen, self.color, (self.state[0] + self.tankWidth / 2, self.state[1]), (barrelXPos, barrelYPos), self.barrelLength)

        #drawing bars
        BAR_LENGTH = 100  # Adjusted bar length for the display
        BAR_HEIGHT = 10

        #health bar
        if self.hp < 0: 
            self.hp = 0
        #draw health text
        smaller_font = pygame.font.SysFont("comicsansms", 15)
        health_bar_text = smaller_font.render("Health", True, WHITE)
        screen.blit(health_bar_text, (self.state[0], self.state[1] + self.tankHeight))
        #draw health bar
        # The y coordinate is now set to self.y + tankHeight (the bottom of the tank) + a small offset
        outline_rect = pygame.Rect(self.state[0], self.state[1] + self.tankHeight + 20, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(self.state[0], self.state[1] + self.tankHeight + 20, self.hp, BAR_HEIGHT)
        pygame.draw.rect(screen, RED, fill_rect)
        pygame.draw.rect(screen, RED, outline_rect, 2)  # Draw outline

        #power bar
        #draw power text
        power_bar_text = smaller_font.render("Power", True, WHITE)
        screen.blit(power_bar_text, (self.state[0], self.state[1] + self.tankHeight + BAR_HEIGHT + 16))
        #Draw power bar (directly underneath the health bar)
        outline_rect = pygame.Rect(self.state[0], self.state[1] + self.tankHeight + BAR_HEIGHT + 35, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(self.state[0], self.state[1] + self.tankHeight + BAR_HEIGHT + 35, self.aimSpeed, BAR_HEIGHT)
        pygame.draw.rect(screen, BLUE, fill_rect)
        pygame.draw.rect(screen, BLUE, outline_rect, 2) 

        #angle text
        #draw angle text (underneath power bar)
        angle_text = smaller_font.render("Angle: " + str(self.aimAngle) + "°", True, WHITE)
        # Positioning the angle text below the power bar
        screen.blit(angle_text, (self.state[0], self.state[1] + self.tankHeight + 2 * BAR_HEIGHT + 32))
