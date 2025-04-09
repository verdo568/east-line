import pygame
import random
import time

pygame.init()
screen = pygame.display.set_mode((1600, 900))
screen.fill((255, 255, 255))
screen_rect = screen.get_rect()
font = pygame.font.Font(('font\JasonHandwriting1.ttf'), 24)

class Player:
    def __init__(self, pb):
        self.pb = pb
    def update(self):
        userInput = pygame.key.get_pressed()
        if userInput[pygame.K_SPACE]:
            self.pb.lookUp = True
        else:
            self.pb.lookUp = False
            

class EastLine:
    def __init__(self):
        self.write = 1
        self.turnHead = 2
        self.minTime = 5
        self.maxTime = 15
        self.status = self.write
    def eastLineStatus(self):
        if(self.status == self.write):
            time.sleep(random.randint(self.minTime, self.maxTime))
            self.status = self.turnHead
        elif(self.status == self.turnHead):
            pass

class ProgressBar:
    def __init__(self):
        self.step = 0
        self.timer = pygame.time.get_ticks()
        self.delayTime = 200
        self.lookUp = False
    def progressBar(self):
        if pygame.time.get_ticks() > self.timer and self.lookUp == False:
            self.step += 1
            self.timer = pygame.time.get_ticks() + self.delayTime
        left = screen_rect.centerx - 400
        width = 800
        height = 20
        buttom = screen_rect.bottom
        pygame.draw.rect(screen, (192, 192, 192), (left, buttom - 50, width, height))
        if self.lookUp:
            pygame.draw.rect(screen, (255, 0, 0), (left, buttom - 50, min(self.step, width), height))
        else:
            pygame.draw.rect(screen, (0, 0, 255), (left, buttom - 50, min(self.step, width), height))
        text = font.render(f'進度: {float(self.step/8):.1f}%', True, '#000000')
        screen.blit(text, (left + width + 5, buttom - 55))
    def update(self):
        ProgressBar.progressBar(self)

def main():
    eastline = EastLine()
    progressBar = ProgressBar()
    player = Player(progressBar)
    run = True
    while run:
        for event in pygame.event.get():
              if event.type == pygame.QUIT:
                 run = False;
        screen.fill((255, 255, 255))
        player.update()
        progressBar.update()
        pygame.display.update()

pygame.display.update()
main()