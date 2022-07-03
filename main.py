import pygame as p
import random as r


class Dung(p.sprite.Sprite):
    xpos=0.0
    ypos=0.0
    color='b'
    def __init__(self, tillnextdung):
        super().__init__()
        self.xpos = r.randint(10,w-10) # 무작위 x좌표

        if r.randint(0,1): # 검정 혹은 하양 탄
            self.color = 'b'
            self.image=p.image.load('resources/blackbullet1.png')
        else:
            self.color = 'w'
            self.image=p.image.load('resources/whitebullet1.png')

        self.rect = self.image.get_rect() #스프라이트 설정
        self.rect.center = (self.xpos, self.ypos)

    def update(self):
        self.ypos += 2+min(23,score/500) # 점수에 비례해 빨라지는 속도
        if self.ypos>799: # 화면 끝에 도달하면 제거
            self.kill()
        self.rect = self.image.get_rect() # 스프라이트 업데이트
        self.rect.center = (self.xpos, self.ypos)


class Sco(p.sprite.Sprite):
    xpos = 30
    ypos = 20
    def __init__(self):
        super().__init__()
        self.fnt = p.font.Font('resources/vitamin.ttf', 20)
        self.image = self.fnt.render('점수: ', True, 'white')
        self.rect = self.image.get_rect()
        self.rect.center = (self.xpos, self.ypos)

    def update(self,s):
        self.image = self.fnt.render('점수: '+str(s), True, 'white')


class Res(p.sprite.Sprite):
    xpos = 100
    ypos = 200

    def __init__(self,s,x,y):
        super().__init__()
        self.fnt = p.font.Font('resources/vitamin.ttf', 20)
        self.image = self.fnt.render(s, True, 'white')
        self.xpos=x
        self.ypos=y
        self.rect = self.image.get_rect()
        self.rect.center = (self.xpos, self.ypos)

    def show(self, s): # 이번 판 점수
        self.image = self.fnt.render('점수: ' + str(s), True, 'white')
        self.rect = self.image.get_rect()
        self.rect.center = (self.xpos, self.ypos)
    def best(self,s): # 최고 점수
        self.image = self.fnt.render('최고 점수: ' + str(s), True, 'white')
        self.rect = self.image.get_rect()
        self.rect.center = (self.xpos, self.ypos)

class Me(p.sprite.Sprite):
    xpos=0
    ypos=0
    color='b'
    black=p.image.load('resources/blackship2.png')
    white=p.image.load('resources/whiteship2.png')
    def __init__(self):
        super().__init__()
        self.xpos=200
        self.ypos=500
        if r.randint(0,1):
            self.color = 'b'
            self.image=self.black
        else:
            self.color = 'w'
            self.image=self.white

    def update(self,vx,vy,change,mouse):
        self.xpos += vx
        self.ypos += vy

        #스크린 이탈 방지
        if self.xpos>400:
            self.xpos=400
        elif self.xpos<0:
            self.xpos=0
        if self.ypos>800:
            self.ypos=800
        elif self.ypos<0:
            self.ypos=0

        if change: # 흑백 변환
            if self.color == 'b':
                self.color = 'w'
                self.image=self.white
            else:
                self.color = 'b'
                self.image=self.black
        if mouse: # 마우스 조작시
            self.xpos = p.mouse.get_pos()[0]
            self.ypos = p.mouse.get_pos()[1]

        # 스프라이트 업데이트
        self.rect = self.image.get_rect()
        self.rect.center = (self.xpos, self.ypos)


# 초기화 및 창 세팅
p.init()

clock = p.time.Clock()
w=400
h=800
tillnextdung=10
screen = p.display.set_mode((w,h))
p.display.set_caption("흑과백")

# 탄 스프라이트 그룹
allsprites=p.sprite.Group()

# 플레이어 객체
me=Me()
mysprite=p.sprite.Group()
mysprite.add(me)

# 현재 점수
sco = Sco()
scosprite=p.sprite.Group()
scosprite.add(sco)

# 결과창
end=Res('게임 끝',200,200)
res = Res('',200,250)
cont = Res('재시작: space',200,300)
qui = Res('종료: 닫기',200,350)
best = Res('',200,400)

ressprite = p.sprite.Group()
ressprite.add(res)
ressprite.add(end)
ressprite.add(cont)
ressprite.add(qui)
ressprite.add(best)

# 배경화면 세팅
b=p.image.load('resources/background.jpg')
screen.blit(b,(0,0))

while True:

    # 게임 내 객체 초기화
    run = True
    change=False
    mouse=False
    score = 0
    vx=0
    vy=0
    for a in allsprites:
        allsprites.remove(a)

    while run: # 인게임
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
                exit()

            # 키보드입력 혹은 마우스 움직임 (동시 구현)
            if event.type == p.KEYDOWN:
                if event.key == p.K_LEFT:
                    vx = -6
                if event.key == p.K_RIGHT:
                    vx = 6
                if event.key == p.K_UP:
                    vy = -6
                if event.key == p.K_DOWN:
                    vy = 6
                if event.key == p.K_SPACE:
                    change = True
            if event.type == p.KEYUP:
                if event.key == p.K_LEFT or event.key == p.K_RIGHT:
                    vx = 0
                if event.key == p.K_UP or event.key == p.K_DOWN:
                    vy = 0
            if event.type == p.MOUSEMOTION:
                mouse = True

        # 1틱마다 점수+, 일정 틱마다 탄 생성
        clock.tick(60)
        score+=1
        tillnextdung-=1
        if tillnextdung<0:
            allsprites.add(Dung(tillnextdung))
            tillnextdung= max(1,10-score//1000)

        # 상태 업데이트
        sco.update(score)
        me.update(vx,vy,change,mouse)
        change = False
        mouse = False
        for d in allsprites:
            d.update()

        # 충돌 시 처리 - 같은 색이면 +100, 다른 색이면 게임오버
        collides = p.sprite.spritecollide(me,allsprites,True,p.sprite.collide_circle)
        for i in collides:
            if i.color == me.color:
                score+=100
            else:
                run = False


        # 화면 갱신
        allsprites.clear(screen,b)
        mysprite.clear(screen,b)
        scosprite.clear(screen,b)

        allsprites.draw(screen)
        mysprite.draw(screen)
        scosprite.draw(screen)

        p.display.update()


    # 점수 기록
    with open('resources/scores.txt','a') as f:
        f.write(str(score)+'\n')

    # 최고 점수
    top=0
    with open('resources/scores.txt','r') as f:
        lines = f.readlines()
        for l in lines:
            if int(l)>top:
                top = int(l)

    # 점수 표시
    best.best(top)
    res.show(score)
    ressprite.draw(screen)

    # 재실행 대기
    conf = True
    while conf:
        clock.tick(10)
        for event in p.event.get():
            if event.type == p.QUIT:
                conf = False
            if event.type == p.KEYDOWN:
                if event.key == p.K_SPACE:
                    run = True
                    ressprite.clear(screen,b)
                if event.type == p.K_x:
                    quit()
        p.display.update()
        if run == True:
            break
    if conf == False:
        break



p.quit()