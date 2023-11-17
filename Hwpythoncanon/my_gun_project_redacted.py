import math
from random import choice
import random
import pygame
from time import sleep
FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
WIDTH = 800
HEIGHT = 600

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=500):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 70
        self.ax = 0
        self.ay = 10
        self.T = 0.4
        self.ver = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        self.vy += self.ay * self.T
        self.x += self.vx *self.T
        self.y += self.vy *self.T
        
        if (self.x > 740) or (self.x < 20) :
      
            self.vx = self.vx*(-1)
        if self.y > 550 or (self.y < 20):
            self.vy = self.vy*(-1)
        if self.x < 20 :
            self.x = 20
        if self.y < 20 :
            self.y = 20
        if self.x > 740 :
            self.x = 740
        if self.y > 550 :
            self.y = 550 
        if self.live < 0:
            balls.pop(balls.index(self))
        else:
            self.live -= 1  
       

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # fIXME
        if  (self.x-obj.x)**2 + (self.y-obj.y)**2 < (self.r + obj.r)**2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen,ver = 0):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.ver = ver  

        self.cx = 40 if ver == 1 else 500
        self.cy = 550
        self.bx = 0

        self.vx=0
        self.hp = 100
        self.sign = 0
        self.points = 0
        self.switch = False

    def fire2_start(self, event):
        self.f2_on = 1
    def move(self):
        if self.hp>5:
            self.cx+=self.vx
    def mover(self,event):
        if event.type == pygame.KEYDOWN:
            self.vx=10
        elif event.type == pygame.KEYUP:
            self.vx=0
    def movel(self,event):
        if event.type == pygame.KEYDOWN:
            self.vx=-10
        elif event.type == pygame.KEYUP:
            self.vx=0
    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        if self.hp>5:
            global balls, bullet
            bullet += 1

            new_ball = Ball(self.screen,self.cx+10,self.cy-10) 
            new_ball.ver = self.ver
            self.nby = new_ball.y
            new_ball.r += 5
            self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
            new_ball.vx = self.f2_power * math.cos(self.an)
            new_ball.vy =  self.f2_power * math.sin(self.an)
            balls.append(new_ball)
            self.f2_on = 0
            self.f2_power = 10
    def splitshot(self):
        nbx = balls[len(balls)-1].x
        nby = balls[len(balls)-1].y
        nbvx = balls[len(balls)-1].vx
        nbvy = balls[len(balls)-1].vy
        b1,b2,b3,b4,b5,b6,b7,b8 = 0,0,0,0,0,0,0,0
        b = [b1,b2,b3,b4,b5,b6,b7,b8]
        x = [20,40,20,0,0,-20,-40,-20]
        y = [20,0,-20,40,-40,20,0,-20]
        for i in range(len(b)):
            b[i] = Ball(self.screen,nbx,nby)
            b[i].r = 20
            b[i].vx = nbvx + x[i]*2
            b[i].vy = nbvy + y[i]*2
            balls.append(b[i])
            print('Second deployed')

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-self.cy) / (event.pos[0]-self.cx if event.pos[0]-self.cx !=0 else 0.01))
            if (event.pos[1]-self.cy)>0:
                self.sign = -(event.pos[0]-self.cx if event.pos[0]-self.cx !=0 else 0.01)/abs(event.pos[0]-self.cx if event.pos[0]-self.cx !=0 else 0.01)
            else:
                self.sign = 0
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # FIXIT don't know how to do it
        if self.hp>5:
            if self.ver == 1:
                print (self.an)


            if self.sign ==1:
                self.an = 0.001
            elif self.sign == -1:
                self.an = math.pi-0.001
            else:
                pass
            lx =(math.cos(self.an)*max(self.f2_power*0.7,20) if self.an<0 else -math.cos(self.an)*max(self.f2_power*0.7,20))
            ly =math.sin(self.an)*max(self.f2_power*0.7,20) if self.an<0 else -math.sin(self.an)*max(self.f2_power*0.7,20)
            dx=-math.sin(self.an)*5
            dy=math.cos(self.an)*5
            pygame.draw.polygon(screen, BLACK, 

                    [[self.cx-dx,self.cy-dy],[self.cx+lx-dx,self.cy+ly-dy],[self.cx+lx+dx,self.cy+ly+dy],[self.cx+dx,self.cy+dy]])
                   # [[self.cx, self.cy], 
                     #[self.cx+math.cos(self.an)*max(self.f2_power*0.7,20), self.cy + math.sin(self.an)*max(self.f2_power*0.7,20)], 
                     #[self.cx-math.sin(self.an)*10+math.cos(self.an)*max(self.f2_power*0.7,20), self.cy + math.cos(self.an)*10+ math.sin(self.an)*max(self.f2_power*0.7,20)],
                       #[self.cx-math.sin(self.an)*10, self.cy + math.cos(self.an)*10]])
            #pygame.draw.line(screen, self.color, [self.cx, self.cy], [self.cx+math.cos(self.an)*max(self.f2_power*0.7,20), self.cy + math.sin(self.an)*max(self.f2_power*0.7,20)], 10)
        else:
            play = True
        pygame.draw.rect(screen,BLACK, pygame.Rect(self.cx-5,self.cy-5,30,12))
        
        pygame.draw.rect(screen,RED, pygame.Rect(self.cx,self.cy-50,30,3))
        pygame.draw.rect(screen,GREEN, pygame.Rect(self.cx,self.cy-50,math.ceil(self.hp*0.3),3))
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self,ver=0):
        self.points = 0
      
        x = self.x = 0
        y = self.y = 0
        r = self.r = 0
        self.ver = ver
        self.vx = random.randint(-40,40)
        self.vy = random.randint(-40,40)
        pygame.draw.circle(screen, BLUE, (self.x,self.y), self.r)
        self.new_target()
        self.live = 1
        
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.live = 1
        x = self.x = random.randint(600, 740)
        y = self.y = random.randint(300, 550)
        r = self.r = random.randint(20, 50)
        color = self.color = RED
        self.ver = random.randint(0,2)

    def hit(self,ver, points=1):
        """Попадание шарика в цель."""
        gun.points += points if ver == 1 else 0
        gun1.points += points if ver == 2 else 0
        self.x = -10
        self.y = -10
        self.r = -10
        self.draw()
    def move(self):
        if self.ver == 0:
            self.x += random.randint(-5, 5)
            self.y += random.randint(-5, 5)
        if self.ver == 1:
            if (self.vx or self.vy) ==0:
                self.vx = random.randint(-40,40)
                self.vy = random.randint(-40,40)
            self.x +=self.vx
            self.y +=self.vy
        if self.ver == 2:
            if (self.vx or self.vy) ==0:
                self.vx = random.randint(-40,40)
                self.vy = random.randint(-40,40)
            self.x +=self.vx*0.2+random.randint(-5, 5)
            self.y +=self.vy*0.2+random.randint(-5, 5)
        if self.x < 20 :
            self.x = 20
        if self.y < 20 :
            self.y = 20
        if self.x > 740 :
            self.x = 740
        if self.y > 590 :
            self.y = 590 
        if (self.x > 730) or (self.x < 40) :
            self.vx = self.vx*(-1)
        if self.y > 540 or (self.y < 40):
            self.vy = self.vy*(-1)
        self.draw()
    def draw(self):
        if self.ver == 0:
            pygame.draw.circle(screen, BLUE, (self.x,self.y), self.r)
        elif self.ver == 1:
            pygame.draw.circle(screen, RED, (self.x,self.y), self.r)
        elif self.ver == 2:
            pygame.draw.circle(screen, GREEN, (self.x,self.y), self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


clock = pygame.time.Clock()
finished = False

def scene1():
    textsize = 100
    finished = False
    while(finished == False):
        bgim = pygame.image.load("background.png")
        screen.blit(bgim,(0,0))
        pygame.draw.rect(screen,GREY,(100,100,600,400))

        f1 = pygame.font.Font(None, textsize)
        text = f1.render("PLAY", 100, (180, 0, 0))
        screen.blit(text, (200, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                switch_scene(None)
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if (event.pos[0]>100) and (event.pos[0]<700):
                    if (event.pos[1]>100) and (event.pos[1]<500):
                        switch_scene(scene2)
                        finished = True
        pygame.display.update()
        clock.tick(FPS)
bullet = 0
balls = []
gun = Gun(screen,1)
gun1 = Gun(screen,2)
target1 = Target(random.randint(0,2))
target2 = Target(random.randint(0,2))
target3 = Target(random.randint(0,2))
finished = False
target1.new_target()
target2.new_target()
target3.new_target()
def scene2():
    for b in balls:
        b.live =0
    gun.hp = 100
    gun1.hp = 100
    finished = False
    a=pygame.time.Clock()
    while (finished == False):
        bgim = pygame.image.load("background.png")
        screen.blit(bgim,(0,0))
        gun.draw()
        gun1.draw()
        a.tick()
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render(str(gun.points), 1, (180, 0, 0))
        text2 = f1.render(str(gun1.points), 1, (180, 0, 0))
        screen.blit(text1, (10, 50))
        screen.blit(text2, (760, 50))
        target1.draw()
        target2.draw()
        target3.draw()
        target1.move()
        target2.move()
        target3.move()
        if gun1.hp>5:
            gun1.move()
        else:
            switch_scene(scene1)
            finished = True
        if gun.hp>5:
            gun.move()
        for b in balls:
            b.draw()
            if b.r**2>((b.x-gun1.cx)**2+(b.y-gun1.cy)**2):
                b.live = 0
                pygame.mixer.music.load('jazz.wav')
                pygame.mixer.music.play(1)
                gun1.hp-=10
            if b.r**2>((b.x-gun.cx)**2+(b.y-gun.cy)**2):
                b.live = 0
                pygame.mixer.music.load('jazz.wav')
                pygame.mixer.music.play(1)
                gun.hp-=10
        
        pygame.display.update()

        clock.tick(FPS)
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN) :
                # если была нажата стрелка влев# если была нажата стрелка вверхо
                if event.key == pygame.K_a:
                    gun1.movel(event)
                # если была нажата стрелка вправо
                if event.key == pygame.K_d:
                    gun1.mover(event)
                if event.key == pygame.K_LEFT:
                    gun.movel(event)
                    print(event.type)
                # если была нажата стрелка вправо
                if event.key == pygame.K_RIGHT:
                    gun.mover(event)
                if event.key == pygame.K_x :
                    gun.switch=not gun.switch
                if event.key == pygame.K_c :
                    gun1.switch=not gun1.switch
                # если была нажата стрелка влев# если была нажата стрелка вверхо
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    gun1.movel(event)
                # если была нажата стрелка вправо
                if event.key == pygame.K_d:
                    gun1.mover(event)
                if event.key == pygame.K_LEFT:
                    gun.movel(event)
                    print(event.type)
                # если была нажата стрелка вправо
                if event.key == pygame.K_RIGHT:
                    gun.mover(event)
                if event.key == pygame.K_x :
                    pass
                #if event.key == pygame.K_c :
                    #gun1.splitshot(event)
            if event.type == pygame.QUIT:
                switch_scene(None)
                finished = True
            elif (event.type == pygame.MOUSEBUTTONDOWN) and (a.get_time()>5):
                gun.fire2_start(event)
                gun1.fire2_start(event)

            elif (event.type == pygame.MOUSEBUTTONUP)and (a.get_time()>5):
                gun.fire2_end(event)
                gun1.fire2_end(event)
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)
                gun1.targetting(event)
        for b in balls:
            b.move()
            if b.hittest(target1) and target1.live:
                target1.live = 0
                target1.hit(b.ver)
                if gun1.ver==b.ver:
                    if gun1.switch == True:
                        gun1.splitshot()
                if gun.ver==b.ver:
                    if gun.switch == True:
                        gun.splitshot()
                target1.new_target()
            if b.hittest(target2) and target2.live:
                target2.live = 0
                target2.hit(b.ver)
                if gun1.ver==b.ver:
                    if gun1.switch == True:
                        gun1.splitshot()
                if gun.ver==b.ver:
                    if gun.switch == True:
                        gun.splitshot()
                target2.new_target()
            if b.hittest(target3) and target3.live:
                target3.live = 0
                target3.hit(b.ver)
                if gun1.ver==b.ver:
                    if gun1.switch == True:
                        gun1.splitshot()
                if gun.ver==b.ver:
                    if gun.switch == True:
                        gun.splitshot()
                target3.new_target()
        gun.power_up()
        gun1.power_up()
def switch_scene(scene):
    global current_scene
    current_scene = scene
switch_scene(scene1)
while current_scene is not None:
    current_scene()
    
pygame.quit()