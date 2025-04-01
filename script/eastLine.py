import pygame
import random
import os
import time

pygame.init()
screen = pygame.display.set_mode((1600, 900))

class Player:
    def __init__(self):
        pass
    

class EastLine:
    def __init__(self):
        global write, turnHead, minTime, maxTime, status
        write = 1
        turnHead = 2
        minTime = 5
        maxTime = 15
        status = write

    def eastLineStatus():
        if(static == write):
            time.sleep(random.randint(minTime, maxTime))
            static = turnHead
        elif(static == turnHead):
            pass
    
    def update(self, userInput):
        if userInput[pygame.K_SPACE]:
            pass

def main():
    player = Player()
    run = True;
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False;
        screen.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
        player.updata(userInput)
        pygame.display.update()
main()
screen.fill((255, 255, 255))