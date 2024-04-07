import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
windowWidth = 1000
windowHeight = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
ORANGE = (255, 140, 0)
COLORS = [RED, GREEN, BLUE, WHITE]  # List of colors for the bricks

class Brick:
    def __init__(self, x, y, brickWidth, brickHeight, color = RED, brickType = 'brick'):

        self.rect = pygame.Rect(x, y, brickWidth, brickHeight)
        self.color = color
        self.objectType = brickType

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class BrickManager:
    def __init__(self):

        self.occupiedPositions = set()

        self.brickWidth = 20
        self.brickHeight = 20
        self.numberOfRows = windowHeight / self.brickHeight  #max number of rows of bricks 
        self.numberOfColumns = windowWidth / self.brickWidth  #max number of columns of bricks 

    def create_bricks(self, numberOfBricks = 0, startColumn = 0, endColumn = 0, startRow = 0, endRow = 0, color = ORANGE):

        bricks = []
        
        for i in range(numberOfBricks):
            column = random.randint(startColumn, endColumn)
            row = random.randint(startRow, endRow)
            newPosition = (column, row)

            if newPosition not in self.occupiedPositions:
                
                self.occupiedPositions.add(newPosition)
                xPos = column * self.brickWidth
                yPos = row * self.brickHeight
                newBrick = Brick(xPos, yPos, self.brickWidth, self.brickHeight, color, 'brick')
                bricks.append(newBrick)

        return bricks
    
    def createPowerUp(self):
        isValidLocation = False
        while not isValidLocation:
            column = random.randint(5, self.numberOfColumns - 5)
            row = random.randint(0, self.numberOfRows - 10)

            newPosition = (column, row)

            if newPosition not in self.occupiedPositions:
                isValidLocation = True
                xPos = column * self.brickWidth
                yPos = row * self.brickHeight
                newBrick = Brick(xPos, yPos, self.brickWidth * 2, self.brickHeight * 2, PURPLE, 'power')

        return newBrick
                
