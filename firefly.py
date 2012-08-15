import pygame, sys
import math
import random
import time
from pygame.locals import*

pygame.init()
screen = pygame.display.set_mode((1200,800),0,32)
ffList = []

class Firefly:

    def __init__(self, x, y, brightness):
        self.x = x
        self.y = y
        self.brightness = brightness
        self.r = int(math.sqrt((self.brightness)/math.pi))
        if self.r < 1:
            self.r = 1  

    def DrawOnScreen(self):
        pygame.draw.circle(screen, pygame.Color(131, 245, 44,255), (self.x, self.y), self.r, 0)

    def Calculations(self):
        deltaX = 0
        deltaY = 0
        for f in ffList:
            if f != self:                                                  #the firefly "f" cannot attract to "g" (itself)
                vectorX = (f.x - self.x)
                vectorY = (f.y - self.y)
                currentLen = math.sqrt(vectorX**2 + vectorY**2)         #euclidean distance between the 2 fireflies

                if currentLen > 50:                                     #fireflies attract each other if their distance is more than 50 pixels apart
                    relBrightness = (f.brightness/currentLen)           #relative brightness of the fireflies is inversely proportional to the currentLen
                    vectorX = vectorX/currentLen                        #normalizing the x vector
                    vectorY = vectorY/currentLen                        #normalizing the y vector
                    deltaX += relBrightness * vectorX
                    deltaY += relBrightness * vectorY
                else:                                                   #fireflies repel each other if their distance is between 1 to 50 pixels
                    deltaX = random.randrange(-3,4)
                    deltaY = random.randrange(-3,4)

        #generate random movement if there is not enough pull from other fireflies
        if abs(deltaX) < 5 and abs(deltaY) < 5:
            self.x += random.randrange(-4,5)
            self.y += random.randrange(-4,5)
        #if there is enough pull from other fireflies, add noise to movement
        else:
            self.x += int(deltaX) + random.randrange(-1,2)
            self.y += int(deltaY) + random.randrange(-1,2)
        
        #Handle boundary here so fireflies can't move outside of window
        if self.x > 1200:
            self.x = 1200
        if self.x < 0:
            self.x = 0
        if self.y > 800:
            self.y = 800
        if self.y < 0:
            self.y = 0

class Mouse:
    def __init__(self):
        (self.x, self.y) = pygame.mouse.get_pos()
        self.brightness = 600
        self.r = int(math.sqrt((self.brightness)/math.pi))
        if self.r < 1:
            self.r = 1

    def DrawOnScreen(self):
        pygame.draw.circle(screen, pygame.Color(255,255,255,255), (self.x, self.y), self.r, 0)

for i in range(150):                                                    #this loop generates the fireflies
    x = int(random.randrange(0,1200))                                   #random x coord
    y = int(random.randrange(0,800))                                    #random y coord
    brightness = random.randrange(1,65)
    ffList.append(Firefly(x,y, brightness))
ffList.append(Mouse())

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill(pygame.Color(0,0,0,255))
    for g in ffList:
        if not isinstance(g, Mouse):
            g.Calculations()
            g.DrawOnScreen()
        else:
            (g.x, g.y) = pygame.mouse.get_pos()
            g.DrawOnScreen()

    pygame.display.update()