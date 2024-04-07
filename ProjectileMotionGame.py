#the 'main' simulation environment 

import pygame, sys
import numpy as np
from scipy.integrate import ode
import random

import bullet
import tank
import brick


# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# clock object that ensure that animation has the same
# on all machines, regardless of the actual machine speed.
clock = pygame.time.Clock()

def load_image(name):
    image = pygame.image.load(name)
    return image

class MyCircle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.image.fill(WHITE)
        cx = self.rect.centerx
        cy = self.rect.centery
        pygame.draw.circle(self.image, color, (width//2, height//2), cx, cy)
        self.rect = self.image.get_rect()

    def update(self):
        pass

'''
#don't need this...
# def sim_to_screen(win_height, x, y):

#     # x += 10
#     # y += 10

#     return x, win_height - y
'''

def main():
    #a lot of this will have to be changed so that we have different bullets and can create them when we want to shoot

    #game controls
    print('--------------------------------')
    print('Use A & D to move')
    print('Use W & D to change shot power')
    print('Use Q & E to change shot direction')
    print('Press R to cycle through avaiable bullets')
    print('Press Space to shoot')
    print('Press P to pause and K to resume')
    print('--------------------------------')

    # initializing pygame
    pygame.init()

    #set up window and game border
    #note: top left corner is (0,0), positive x is right (i.e. going right by 10 = (10, 0)), positive y is down (i.e. going down by 10 = (0, 10))
        #important to keep in mind that increasing y means going down, especially when it comes to gravity stuff 
        #there was some function from the labs that 'flipped' this, but I think it was messing with some things so I just removed it...
    
    windowWidth = 1000
    windowHeight = 600
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    background = pygame.image.load('terrain.png')
    background = pygame.transform.scale(background, (windowWidth, windowHeight))
    pygame.display.set_caption('Tank Game')

    #windSpeed = 0 #can represent this with two bars horizontally (only 1 bar will be filled; left bar meaens wind blowing left, same for right), or just use a number

    #set up terrain (start with simple flat floor)

    #set up obstacles (bricks to block bullets)


    #set up a sprite group which will be drawn on the screen
        #essentially every object that will be drawn should be stored here
    #...sike this bad (?) just call the object's draw method for each object that needs to be drawn, or instead of creating a sprite group, create an objects list and loop through that to call each object's draw
    # spriteGroup = pygame.sprite.Group()

    #create tank for p1
    tank1 = tank.Tank(100, windowHeight - 100, 1, 40, 20, 5, GREEN)
    #create tank for p2
    tank2 = tank.Tank(windowWidth - 140, windowHeight - 100, -1, 40, 20, 5, BLUE)

    tanks = [tank1, tank2]

    #generate the bricks (obstacles) 
    brickManager = brick.BrickManager()
    bricks = brickManager.create_bricks(300, 20, 30, 10, 25)        #obstacle (divider in middle)
    bricks.extend(brickManager.create_bricks(100, 0, 50, 0, 10))    #obstacles in sky

    powerUp = brickManager.createPowerUp()

    #not sure how to add bullets right now (since they have to be created and deleted)
    #one option is to to create these sprites (circles) and then update their
        #position using the positions of the actual bullets, but that doesn't seem right...
    
    '''
    #main loop of the game (infinite loop while both tanks are alive)
        #basic rundown: 
            #determine who has control (who's turn it is), 
            #check for key presses 
                #update position of tank (A & D)
                #update position / size (or color?) of arrow showing where bullet would go (Q & E for turning left/right, W & S for speed/power of bullet) 
                #update bullet selection (R? loops through bullet list each time it's pressed)
                #if fire button pressed (space for fire?), create and add new bullet 
            #if there are bullet(s), update bullets' position
                #check for collisions
                #update things accordingly; break bullets, break blocks/terrain, damage tanks
            #check hp of tanks, if one is 0, other wins
            #draw everything (spriteGroup (tank, bullet), terrain, hp, aim trajectory arrow, numbers (power (and angle) of shot))
    '''
    #int control variable that determines who is currently in control (since we want turn based)
        #start with letting p1 have control
        #i.e. pressing keys will affect tank1
    control = 0
    paused = False

    while True:
        # 30 fps (this is from lab... not sure what to do with it)
        clock.tick(30)

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        currentTank = tanks[control] #get the tank corresponding to current control from list of tanks
            
        #get key presses
        keys = pygame.key.get_pressed()

        #controls for pausing and resuming the game
        if keys[pygame.K_p]:
            paused = True
        elif keys[pygame.K_k]:
            paused = False
        
        #clear the background (to re-draw the sprites) 
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        
        if not paused:

            # #check for tank controls (need to implement these properly after tank class is done)
            if keys[pygame.K_a]:
                # print(control, 'left')
                currentTank.move(-1)
            elif keys[pygame.K_d]:
                # print(control, 'right')
                currentTank.move(1)

            #controls for changing shot power of bullet(s) (could either pass a number to method or have no parameter and just have a fixed number in the method itself)
                #*make sure power is between 10 to 100 (10 might be too high? definitely don't want 0)
            if keys[pygame.K_w]:
                # print(control, 'increase shot power')
                currentTank.changePower(1)
            elif keys[pygame.K_s]:
                # print(control, 'decrease shot power')
                currentTank.changePower(-1)

            #controls for aiming tank barrel / bullet (change 1 degree at a time?)
                #*make sure angle is between 0 to 180 (the upper side of the tank)
            if keys[pygame.K_q]:
                # print(control, 'shift aim left')
                currentTank.shiftAimAngle(1)
            elif keys[pygame.K_e]:
                # print(control, 'shift aim right')
                currentTank.shiftAimAngle(-1)

            #control for cycling bullet type 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # print(control, 'cycle bullet')
                currentTank.nextBullet()

            if keys[pygame.K_SPACE]:
                # print(control, 'shoot')

                shotBullet = currentTank.shoot() #this will simply remove the selected bullet from the tank's bullet list and return it

                #while the bullet is still 'alive', only update the bullet and don't let anything else have control
                while shotBullet.isActive:
                    clock.tick(30)
                    #clear everything and re-fill with background
                    screen.fill(WHITE)
                    screen.blit(background, (0, 0))

                    #update bullet
                    shotBullet.step()

                    #re-draw everything
                    for drawTank in tanks:
                        drawTank.draw(screen)
                    for brick1 in bricks:
                        brick1.draw(screen)
                    if not powerUp == None:     
                        powerUp.draw(screen)
                    shotBullet.draw(screen)

                    #check for collision
                    for brick1 in bricks:
                        if shotBullet.isCollide(brick1):
                            bricks.remove(brick1)
                    if not powerUp == None and shotBullet.isCollide(powerUp):
                        #currentTank.addPowerUp() #simply generate a random bullet (powerUp) and add to the list of bullets
                            #show powerup (text saying powerUp acquired)
                            #make sure to 'draw' currentTank's current bullet to show what bullet is currently equiped 
                        currentTank.addPowerUp()
                        powerUp = None
                    for tank1 in tanks:
                        if not currentTank == tank1:
                            if shotBullet.isCollide(tank1):
                                print('hit')
                                tank1.hp = tank1.hp - 25

                                #check win condition
                                if tank1.hp <= 0:
                                    print('Game Over')
                                    print('Player', control + 1, 'wins!')
                                    pygame.quit()
                                    sys.exit(0)
                                shotBullet.step()

                    pygame.display.flip()
                #end of bullet loop

                #next turn; swap controls
                if control == len(tanks) - 1:
                    control = 0
                    currentTank.fuel = 100
                    powerUp = brickManager.createPowerUp()
                else:
                    control = control + 1
                    currentTank.fuel = 100
                    powerUp = brickManager.createPowerUp()

     #display procedure (re-draw everything)
        for drawTank in tanks:
            drawTank.draw(screen)
        for brick1 in bricks:
            brick1.draw(screen)
        powerUp.draw(screen)

        pygame.display.flip()

    # print("r: %10.2f" % sim.trace_x[-1])

if __name__ == '__main__':
    main()