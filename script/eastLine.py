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
        self.write = 1
        self.turnHead = 2
        self.minTime = 5
        self.maxTime = 15
        self.status = self.write
    def eastLineStatus(self):
        if(self.status == write):
            time.sleep(random.randint(minTime, maxTime))
            self.status = turnHead
        elif(self.status == turnHead):
            pass

class ProgressBar:
    def __init__(self):
        global step, delayTime, timer
        self.timer = pygame.time.get_ticks()
        self.delayTime = 500
        self.step = 0
    def progressBar(self):
        if(pygame.time.get_ticks() > self.timer):
            self.step += 1
            self.timer = pygame.time.get_ticks() + self.delayTime
        pygame.draw.rect(screen, (192, 192, 192), (5, 100, 490, 20))
        pygame.draw.rect(screen, (0, 0, 255), (5, 100, min(5+self.step, 490), 20))
    def update(self):
        ProgressBar.progressBar(self)

def main():
    player = Player()
    eastline = EastLine()
    progressBar = ProgressBar()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False;
        screen.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
        progressBar.update()
        pygame.display.update()
main()
screen.fill((255, 255, 255))