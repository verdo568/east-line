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
    ui = 5

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

class EventText:
    #text = [標題, 副標題, 選項1按鈕, 選項1標題, 選項1敘述, 選項2按鈕, 選項2標題, 選項2敘述]
    text = [['突發事件:', '你是值日生被老師叫去倒垃圾', '好!我去', '值日之神', '放下遊戲進度，衝出去倒垃圾; 效果: 1.遊戲進度倒退', '不要!垃圾還沒滿', '但是我拒絕', '不去倒垃圾; 效果: 老師放下粉筆機率增加']
            ,['突發事件:', '你被老師刁難了', '學分送你啦!乞丐!', '學分戰士', '直接嗆他; 效果: 1.遊戲速度加快 2.老師放下粉筆機率增加', '......', '沉默', '無效果']
            ,['突發事件:', '老師解不出題目要你幫忙', '老師好菜喔!', '菜就多練', '老師被激怒; 效果: 趕課Level加一', '這題簡單!', '數學電神', '放下遊戲，快速找到老師算錯的地方; 效果: 遊戲進度倒退']]

class SpecialEvent:
    def buff(progressBar, eastLine, choice, eventId):
        match eventId:
            case 0:
                if choice == 1:
                    progressBar.step -= 80
                else:
                    eastLine.timeBuff *= 0.75
            case 1:
                if choice == 1:
                    progressBar.delayTime -= 50
                    eastLine.timeBuff *= 0.75
                else:
                    pass
            case 2:
                if choice == 1:
                    progressBar.addLevel += 1
                else:
                    progressBar.step -= 160
                    
    def type(progressBar, eastLine, eventId):
        textList = EventText.text[eventId]
        onEvent = True
        while onEvent:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    EventType.mouseLeftButtonDown = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    EventType.mouseLeftButtonDown = False
            screen.fill((255, 255, 255))

            #標題
            text = font72.render(textList[0] ,True, '#000000')
            screen.blit(text, text.get_rect(center=(screen_rect.centerx, screen_rect.centery-200)))

            #副標題
            text = font24.render(textList[1], True, '#000000')
            screen.blit(text, text.get_rect(center=(screen_rect.centerx, screen_rect.centery-100)))

            #選項1按鈕
            button1_text = font48.render(textList[2], True, "#000000", "#c0c0c0")
            button1_rect = button1_text.get_rect(center=(screen_rect.centerx-300, screen_rect.centery+300))
            screen.blit(button1_text, button1_rect)

            #選項1標題
            text = font24.render(textList[3], True, "#000000")
            screen.blit(text, text.get_rect(center=(screen_rect.centerx-300, screen_rect.centery+200)))

            #選項1技能敘述
            text = font24.render(textList[4], True, '#000000')
            screen.blit(text, text.get_rect(center=(screen_rect.centerx-300, screen_rect.centery+240)))

            #選項2按鈕
            button2_text = font48.render(textList[5], True, "#000000", "#c0c0c0")
            button2_rect = button2_text.get_rect(center=(screen_rect.centerx+300, screen_rect.centery+300))
            screen.blit(button2_text, button2_rect)

            #選項2標題
            text = font24.render(textList[6], True, "#000000")
            screen.blit(text, text.get_rect(center=(screen_rect.centerx+300, screen_rect.centery+200)))

            #選項2技能敘述
            text = font24.render(textList[7], True, '#000000')
            screen.blit(text, text.get_rect(center=(screen_rect.centerx+300, screen_rect.centery+240)))

            pygame.display.update()
            if EventType.mouseLeftButtonDown and button1_rect.collidepoint(pygame.mouse.get_pos()):
                SpecialEvent.buff(progressBar, eastLine, 1, eventId)
                onEvent = False
            if EventType.mouseLeftButtonDown and button2_rect.collidepoint(pygame.mouse.get_pos()):
                SpecialEvent.buff(progressBar, eastLine, 2, eventId)
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
        self.timeBuff = 1
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
                    self.statusTimer = pygame.time.get_ticks() + random.randint(int(3000 * fixTime * self.timeBuff), int(6000 * fixTime * self.timeBuff))
                #切換
                if pygame.time.get_ticks() > self.statusTimer:
                    self.status = self.down
                    self.firstSwitch = True
            #放下粉筆
            case self.down:
                self.image = Image.EastLine_down
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
        self.addLevel = 0
        self.event = [0, 0, 0]
    def update(self, eastLine):
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
        self.level = self.step//80 + 1 + self.addLevel
        pygame.draw.rect(screen, "#c0c0c0", (left, buttom - 50, width, height))
        if self.lookUp:
            pygame.draw.rect(screen, "#ff0000", (left, buttom - 50, min(self.step, width), height))
        else:
            pygame.draw.rect(screen, "#0000ff", (left, buttom - 50, min(self.step, width), height))
        progress = min(float(self.step/8), 100)
        if progress >= 100:
            Scene.nowScene = Scene.success

        if progress >= 30 and self.event[0] == False:
            self.event[0] = True
            SpecialEvent.type(self, eastLine, 0)
            eastLine.firstSwitch = True
            eastLine.status = eastLine.write
        if progress >= 50 and self.event[1] == False:
            self.event[1] = True
            SpecialEvent.type(self, eastLine, 1)
            eastLine.firstSwitch = True
            eastLine.status = eastLine.write
        if progress >= 80 and self.event[2] == False:
            self.event[2] = True
            SpecialEvent.type(self, eastLine, 2)
            eastLine.firstSwitch = True
            eastLine.status = eastLine.write

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
        howPlay_button_text = font48.render("操作方法", True, "#000000", "#c0c0c0")
        howPlay_button_rect = howPlay_button_text.get_rect(center=screen_rect.center)
        screen.blit(howPlay_button_text, howPlay_button_rect)
        if EventType.mouseLeftButtonDown and howPlay_button_rect.collidepoint(pygame.mouse.get_pos()):
            howPlay = True
            while howPlay:
                screen.fill((255, 255, 255))
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        EventType.mouseLeftButtonDown = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        EventType.mouseLeftButtonDown = False
                text = font72.render("操作方法" ,True, '#000000')
                screen.blit(text, text.get_rect(center=(screen_rect.centerx, screen_rect.centery-200)))
                text = font24.render("按住空白鍵切換上課姿勢", True, '#000000')
                screen.blit(text, text.get_rect(center=(screen_rect.centerx, screen_rect.centery-100)))
                button_text = font48.render("返回", True, "#000000", "#c0c0c0")
                button_rect = button_text.get_rect(center=(screen_rect.centerx, screen_rect.centery+300))
                screen.blit(button_text, button_rect)
                pygame.display.update()
                if EventType.mouseLeftButtonDown and button_rect.collidepoint(pygame.mouse.get_pos()):
                    howPlay = False
        
        ad_button_text = font48.render("觀看廣告", True, "#000000", "#c0c0c0")
        ad_button_rect = ad_button_text.get_rect(center=(screen_rect.centerx, screen_rect.centery+100))
        screen.blit(ad_button_text, ad_button_rect)
        if EventType.mouseLeftButtonDown and ad_button_rect.collidepoint(pygame.mouse.get_pos()):
            ad = True
            while ad:
                screen.fill((255, 255, 255))
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        EventType.mouseLeftButtonDown = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        EventType.mouseLeftButtonDown = False

                text = font48.render("同作者遊戲: 光照窮途End of Light DEMO版已推出" ,True, '#000000')
                text_rect = text.get_rect(center=(screen_rect.centerx, screen_rect.centery-100))
                screen.blit(text, text_rect)

                button_text = font48.render("遊玩連結", True, "#000000", "#c0c0c0")
                button_rect = button_text.get_rect(center=(screen_rect.centerx, screen_rect.centery+200))
                screen.blit(button_text, button_rect)
                if EventType.mouseLeftButtonDown and button_rect.collidepoint(pygame.mouse.get_pos()):
                    webbrowser.open("https://csy-games.itch.io/end-of-light")
                    pygame.time.delay(1000)

                button_text = font48.render("返回", True, "#000000", "#c0c0c0")
                button_rect = button_text.get_rect(center=(screen_rect.centerx, screen_rect.centery+300))
                screen.blit(button_text, button_rect)

                pygame.display.update()
                if EventType.mouseLeftButtonDown and button_rect.collidepoint(pygame.mouse.get_pos()):
                    ad = False

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
                progressBar.update(eastline)
            case Scene.gameOver:
                screen.fill((255, 255, 255))
                gameOver.update()
            case Scene.success:
                screen.fill((255, 255, 255))
                success.update()
        pygame.display.update()
main()