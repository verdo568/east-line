import pygame
import random
import time

const write = 1
const turnHead = 2
const minTime = 5
const maxTime = 15
static = write

def EastLineStatic:
    if(static == write){
        time.sleep(random.randint(minTime, maxTime))
        static = turnHead
    }
    elif(static == turnHead){
        
    }
