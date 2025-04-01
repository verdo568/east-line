import pygame
import random
import os
import time

pygame.init()
screen = pygame.display.set_mode((1600, 900))

write = 1
turnHead = 2
minTime = 5
maxTime = 15
status = write

def EastLineStatus():
    if(static == write):
        time.sleep(random.randint(minTime, maxTime))
        static = turnHead
    elif(static == turnHead):
        #12321231231123