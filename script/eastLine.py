import pygame
import random
import time

#初始化
pygame.init()
screen = pygame.display.set_mode((1600, 900))
screen.fill((255, 255, 255))
screen_rect = screen.get_rect()
#載入字體
font = pygame.font.Font(('font\JasonHandwriting1.ttf'), 24)
#載入動畫
EastLine_writting = [pygame.image.load("Image\writting.png"), pygame.image.load("Image\writting2.png")]
EastLine_look = pygame.image.load("Image\look.png")
EastLine_find = pygame.image.load("Image\\find.png")
EastLine_down = pygame.image.load("Image\down.png")
#場景管理


#東線
class EastLine:
    def __init__(self):
        self.image = EastLine_writting[0]
        self.write = 1
        self.down = 2
        self.look = 3
        self.find = 4
        self.minTime = 5
        self.maxTime = 15
        self.status = self.write
        self.WriteId = 0
        self.animationTimer = pygame.time.get_ticks()
        self.statusTimer = pygame.time.get_ticks()
        self.animationDelayTime = 200
        self.firstSwitch = True
    #切換狀態
    def update(self):
        match self.status:
            #寫
            case self.write:
                if pygame.time.get_ticks() > self.animationTimer:
                    self.animationTimer = pygame.time.get_ticks() + self.animationDelayTime
                    self.WriteId = (self.WriteId + 1) % 2
                    self.image = EastLine_writting[self.WriteId]
                if self.firstSwitch:
                    self.firstSwitch = False
                    self.statusTimer = pygame.time.get_ticks() + random.randint(3000, 6000)
                #切換
                if pygame.time.get_ticks() > self.statusTimer:
                    self.status = self.down
                    self.firstSwitch = True
            #放下粉筆
            case self.down:
                self.image = EastLine_down
                if self.firstSwitch:
                    self.firstSwitch = False
                    self.statusTimer = pygame.time.get_ticks() + random.randint(1000, 2000)
                #切換
                if pygame.time.get_ticks() > self.statusTimer:
                    #1/3的機率回頭
                    nextStatus = random.randint(1, 3)
                    if nextStatus == 1:
                        self.status = self.look
                    else:
                        self.status = self.write
                    self.firstSwitch = True
            #觀察
            case self.look:
                self.image = EastLine_look
                if self.firstSwitch:
                    self.firstSwitch = False
                    self.statusTimer = pygame.time.get_ticks() + random.randint(1000, 3000)
                #切換
                if pygame.key.get_pressed()[pygame.K_SPACE] == False:
                    self.status = self.find
                    self.firstSwitch = True
                if pygame.time.get_ticks() > self.statusTimer:
                    self.status = self.write
                    self.firstSwitch = True
                #找到
            case self.find:
                self.image = EastLine_find
                pygame.time.wait(2000)
                
        screen.blit(self.image, screen_rect.center)
                


#進度條
class ProgressBar:
    def __init__(self):
        self.step = 0
        self.timer = pygame.time.get_ticks()
        self.delayTime = 200
        self.lookUp = False
    def update(self):
        userInput = pygame.key.get_pressed()
        if userInput[pygame.K_SPACE] == True:
            self.lookUp = True
        elif userInput[pygame.K_SPACE] == False:
            self.lookUp = False
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

def main():
    eastline = EastLine()
    progressBar = ProgressBar()
    run = True
    while run:
        for event in pygame.event.get():
              if event.type == pygame.QUIT:
                 run = False;
        screen.fill((255, 255, 255))
        eastline.update()
        progressBar.update()
        pygame.display.update()

pygame.display.update()
main()