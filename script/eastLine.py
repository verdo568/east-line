import pygame
import random
import time

pygame.init()
screen = pygame.display.set_mode((1600, 900))
screen.fill((255, 255, 255))
screen_rect = screen.get_rect()

bg = pygame.Surface(screen.get_size())
bg = bg.convert()
bg.fill((255, 255, 255))
font = pygame.font.Font(('font\JasonHandwriting1.ttf'), 50)

class Player:
    def __init__(self):
        pass
    def update(self):
        userInput = pygame.key.get_pressed()
        if userInput[pygame.K_SPACE]:
            ProgressBar.lookUp = True
            

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
        global step, delayTime, timer, lookUp
        self.step = 0
        self.timer = pygame.time.get_ticks()
        self.delayTime = 200
        self.lookUp = False
    def progressBar(self):
        if pygame.time.get_ticks() > self.timer and self.lookUp == False:
            self.step += 1
            self.timer = pygame.time.get_ticks() + self.delayTime
            text = font.render(str(int(self.step/8)), True, '#000000', '#ffffff')
            screen.blit(text, (0, 0))
        left = screen_rect.centerx - 400
        width = 800
        height = 20
        buttom = screen_rect.bottom
        pygame.draw.rect(screen, (192, 192, 192), (left, buttom - 50, width, height))
        pygame.draw.rect(screen, (0, 0, 255), (left, buttom - 50, min(self.step, width), height))
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
        player.update()
        progressBar.update()
        pygame.display.update()

pygame.display.update()
main()