import pygame
import random
import webbrowser

#初始化
pygame.init()
screen = pygame.display.set_mode((1600, 900))
screen.fill((255, 255, 255))
screen_rect = screen.get_rect()
#載入字體
font24 = pygame.font.Font(('font\JasonHandwriting1.ttf'), 24)
font48 = pygame.font.Font(('font\JasonHandwriting1.ttf'), 48)
font72 = pygame.font.Font(('font\JasonHandwriting1.ttf'), 72)
#載入圖片
class Image:
    EastLine_writting = [pygame.image.load("Image\writting.png"), pygame.image.load("Image\writting2.png")]
    EastLine_look = pygame.image.load("Image\look.png")
    EastLine_find = pygame.image.load("Image\\find.png")
    EastLine_down = pygame.image.load("Image\down.png")
    Player_writting = pygame.image.load("Image\player_writting.png")
    Player_playing = [pygame.image.load("Image\player_playing1.png"), pygame.image.load("Image\player_playing2.png")]
    Blackboard = pygame.image.load("Image\\blackboard.png")

#場景管理
class Scene:
    init = True
    nowScene = 1
    menu = 1
    inGame = 2
    gameOver = 3
    success = 4

class EventType:
    mouseLeftButtonDown = 0

#玩家
class Player:
    def __init__(self):
        self.image = Image.Player_playing[0]
        self.playing = 1
        self.writting = 2
        self.status = self.playing
        self.WriteId = 0
        self.animationTimer = pygame.time.get_ticks()
        self.animationDelayTime = 200
    def update(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.image = Image.Player_writting
        else:
            if pygame.time.get_ticks() > self.animationTimer:
                self.animationTimer = pygame.time.get_ticks() + self.animationDelayTime
                self.WriteId = (self.WriteId + 1) % 2
                self.image = Image.Player_playing[self.WriteId]
        image_rect = self.image.get_rect(center=screen_rect.center)
        screen.blit(self.image, image_rect)

class SpecialEvent:
    def type1():
        onEvent = True
        while onEvent:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    EventType.mouseLeftButtonDown = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    EventType.mouseLeftButtonDown = False
            screen.fill((255, 255, 255))
            text = font72.render("突發事件:" ,True, '#000000')
            screen.blit(text, text.get_rect(center=(screen_rect.centerx, screen_rect.centery-200)))
            text = font24.render("你被老師刁難了", True, '#000000')
            screen.blit(text, text.get_rect(center=(screen_rect.centerx, screen_rect.centery-100)))
            #選項1
            button_text = font48.render("學分戰士", True, "#000000", "#c0c0c0")
            button_rect = button_text.get_rect(center=(screen_rect.centerx-300, screen_rect.centery+300))
            screen.blit(button_text, button_rect)
            text = font24.render("'學分送你啦!乞丐!'", True, "#000000")
            screen.blit(text, text.get_rect(center=(screen_rect.centerx-300, screen_rect.centery+200)))
            text = font24.render("直接嗆他；Buff遊戲進度加快；Debuff獲得老師特別關照", True, '#000000')
            screen.blit(text, text.get_rect(center=(screen_rect.centerx-300, screen_rect.centery+240)))
            #選項2
            button_text = font48.render("保持沉默", True, "#000000", "#c0c0c0")
            button_rect = button_text.get_rect(center=(screen_rect.centerx+300, screen_rect.centery+300))
            screen.blit(button_text, button_rect)
            text = font24.render("無效果", True, '#000000')
            screen.blit(text, text.get_rect(center=(screen_rect.centerx+300, screen_rect.centery+240)))
            pygame.display.update()
            if EventType.mouseLeftButtonDown and button_rect.collidepoint(pygame.mouse.get_pos()):
                onEvent = False
            if EventType.mouseLeftButtonDown and button_rect.collidepoint(pygame.mouse.get_pos()):
                onEvent = False
#東線
class EastLine:
    def __init__(self):
        self.image = Image.EastLine_writting[0]
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
        self.animationDelayTime = 400
        self.firstSwitch = True
    #切換狀態
    def update(self, progressBar):
        fixTime = 1 / (1 + progressBar.level / 4)
        self.animationDelayTime = 200 * fixTime
        screen.blit(Image.Blackboard, Image.Blackboard.get_rect(center=(screen_rect.centerx, screen_rect.centery-300)))
        match self.status:
            #寫
            case self.write:
                if pygame.time.get_ticks() > self.animationTimer:
                    self.animationTimer = pygame.time.get_ticks() + self.animationDelayTime
                    self.WriteId = (self.WriteId + 1) % 2
                    self.image = Image.EastLine_writting[self.WriteId]
                if self.firstSwitch:
                    self.firstSwitch = False
                    self.statusTimer = pygame.time.get_ticks() + random.randint(int(3000 * fixTime), int(6000 * fixTime))
                #切換
                if pygame.time.get_ticks() > self.statusTimer:
                    self.status = self.down
                    self.firstSwitch = True
            #放下粉筆
            case self.down:
                self.image = Image.EastLine_down
                if random.randint(1, 10) == 1:
                    SpecialEvent.type1()
                    self.status = self.write
                    return
                if self.firstSwitch:
                    self.firstSwitch = False
                    self.statusTimer = pygame.time.get_ticks() + random.randint(int(700 * fixTime), int(1500 * fixTime))
                #切換
                if pygame.time.get_ticks() > self.statusTimer:
                    #2/3的機率回頭
                    nextStatus = random.randint(1, 3)
                    if nextStatus == 1:
                        self.status = self.write
                    else:
                        self.status = self.look
                    self.firstSwitch = True
            #觀察
            case self.look:
                self.image = Image.EastLine_look
                if self.firstSwitch:
                    self.firstSwitch = False
                    self.statusTimer = pygame.time.get_ticks() + random.randint(int(1000 * fixTime), int(3000 * fixTime))
                #切換
                if pygame.key.get_pressed()[pygame.K_SPACE] == False:
                    self.status = self.find
                    self.firstSwitch = True
                if pygame.time.get_ticks() > self.statusTimer:
                    self.status = self.write
                    self.firstSwitch = True
            #找到
            case self.find:
                self.image = Image.EastLine_find
                image_rect = self.image.get_rect(center=(screen_rect.centerx, screen_rect.centery - 200))
                screen.blit(self.image, image_rect)
                pygame.display.update()
                pygame.time.delay(2000)
                Scene.nowScene = Scene.gameOver
                return
        image_rect = self.image.get_rect(center=(screen_rect.centerx, screen_rect.centery - 200))
        screen.blit(self.image, image_rect)

#進度條
class ProgressBar:
    def __init__(self):
        self.step = 0
        self.timer = pygame.time.get_ticks()
        self.delayTime = 100
        self.lookUp = False
        self.level = 1
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
        top = screen_rect.top
        self.level = self.step//80 + 1
        pygame.draw.rect(screen, "#c0c0c0", (left, buttom - 50, width, height))
        if self.lookUp:
            pygame.draw.rect(screen, "#ff0000", (left, buttom - 50, min(self.step, width), height))
        else:
            pygame.draw.rect(screen, "#0000ff", (left, buttom - 50, min(self.step, width), height))
        progress = min(float(self.step/8), 100)
        if progress >= 100:
            Scene.nowScene = Scene.success
        text = font24.render(f'進度: {progress:.1f}%', True, '#000000')
        screen.blit(text, (left + width + 5, buttom - 55))
        text = font24.render(f'趕課等級: Level {self.level}', True, '#000000')
        screen.blit(text, (left - 250, top + 55))

class GameOver:
    def __init__(self):
        pass
    def update(self):
        text = font72.render("Game Over" ,True, '#000000')
        screen.blit(text, text.get_rect(center=(screen_rect.centerx, screen_rect.centery-200)))
        text = font24.render("下課跟我去教官室", True, '#000000')
        screen.blit(text, text.get_rect(center=(screen_rect.centerx, screen_rect.centery-100)))
        button_text = font48.render("回主畫面", True, "#000000", "#c0c0c0")
        button_rect = button_text.get_rect(center=(screen_rect.centerx, screen_rect.centery+300))
        screen.blit(button_text, button_rect)
        if EventType.mouseLeftButtonDown and button_rect.collidepoint(pygame.mouse.get_pos()):
            Scene.nowScene = Scene.menu

class Success:
    def __init__(self):
        pass
    def update(self):
        text = font72.render("恭喜過關" ,True, '#000000')
        screen.blit(text, text.get_rect(center=(screen_rect.centerx, screen_rect.centery-200)))
        text = font24.render("這課誰愛上誰上", True, '#000000')
        screen.blit(text, text.get_rect(center=(screen_rect.centerx, screen_rect.centery-100)))
        button_text = font48.render("回主畫面", True, "#000000", "#c0c0c0")
        button_rect = button_text.get_rect(center=(screen_rect.centerx, screen_rect.centery+300))
        screen.blit(button_text, button_rect)
        if EventType.mouseLeftButtonDown and button_rect.collidepoint(pygame.mouse.get_pos()):
            Scene.nowScene = Scene.menu

class Menu:
    def __init__(self):
        pass
    def update(self):
        title_text = font72.render("東線課上玩手機" ,True, '#000000')
        screen.blit(title_text, title_text.get_rect(center=(screen_rect.centerx, 100)))
        button_text = font48.render("開始遊戲", True, "#000000", "#c0c0c0")
        button_rect = button_text.get_rect(center=(screen_rect.centerx, screen_rect.centery-100))
        screen.blit(button_text, button_rect)
        if EventType.mouseLeftButtonDown and button_rect.collidepoint(pygame.mouse.get_pos()):
            Scene.nowScene = Scene.inGame
            Scene.init = True
        ad_button_text = font48.render("教學影片", True, "#000000", "#c0c0c0")
        ad_button_rect = ad_button_text.get_rect(center=screen_rect.center)
        screen.blit(ad_button_text, ad_button_rect)
        if EventType.mouseLeftButtonDown and ad_button_rect.collidepoint(pygame.mouse.get_pos()):
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

def main():
    player = Player()
    progressBar = ProgressBar()
    eastline = EastLine()
    gameOver = GameOver()
    menu = Menu()
    success = Success()
    run = True
    while run:     
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                EventType.mouseLeftButtonDown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                EventType.mouseLeftButtonDown = False
            if event.type == pygame.QUIT:
                run = False
        match Scene.nowScene:
            case Scene.menu:
                screen.fill((255, 255, 255))
                menu.update()
            case Scene.inGame:
                if Scene.init:
                    Scene.init = False
                    player.__init__()
                    eastline.__init__()
                    progressBar.__init__()
                screen.fill((255, 255, 255))
                player.update()
                eastline.update(progressBar)
                progressBar.update()
            case Scene.gameOver:
                screen.fill((255, 255, 255))
                gameOver.update()
            case Scene.success:
                screen.fill((255, 255, 255))
                success.update()
        pygame.display.update()
main()