import pygame
from pygame.locals import *
import time
import random

class Plane(object):
    def __init__(self,screen,imageName):

        self.screen = screen
        self.image = pygame.image.load(imageName)
        '''飞机发射的所有子弹'''
        self.bulletList = []

        '''对象显示'''
    def display(self):
        # 删除列表
        needDelItemList = []
        self.screen.blit(self.image,(self.x,self.y))
        # 删除多余子弹
        for i in self.bulletList:
            if i.judge():
                needDelItemList.append(i)

        for i in needDelItemList:
            self.bulletList.remove(i)

        # 显示、移动列表中的子弹
        for bullet in self.bulletList:
            bullet.display()
            bullet.move()


class HeroPlane(Plane):
    def __init__(self,screen,x):
        # 调用基类super括号中的参数不理解
        super().__init__(screen,'E:\python project\media\plane_hero.png')
        self.x = x
        self.y = 700

    def moveRight(self):
        if self.x < 379:
            self.x += 25

    def moveLeft(self):
        if self.x > 0:
            self.x -= 25

    def moveUp(self):
        if self.y > 0:
            self.y -= 32

    def moveDown(self):
        if self.y < 700:
            self.y += 32

    def sheBullet(self):
        newBellet = Bullet(self.x,self.y,self.screen,'Hero')
        self.bulletList.append(newBellet)


class EnemyPlane(Plane):
    def __init__(self,screen):
        # 调用基类super括号中的参数不理解
        super().__init__(screen,'E:\python project\media\enemy_plane.png')
        # 设置飞机默认的位置
        self.x = 0
        self.y = 0

        # 敌机移动方向
        self.direction = 'right'

    def move(self):
        if self.direction == "right":
            self.x += 3
        elif self.direction == "left":
            self.x -= 3

        if self.x>480-50:
            self.direction = "left"
        elif self.x<0:
            self.direction = "right"

    def sheBullet(self):
        num = random.randint(1, 100)
        if num <= 3:
            newBullet = Bullet(self.x,self.y,self.screen,'Enemy')
            self.bulletList.append(newBullet)


class Bullet(object):
    def __init__(self,x,y,screen,name):

        self.screen = screen
        self.name = name

        if self.name == 'Hero':
            self.x = x + 40
            self.y = y - 20
            imageName = 'E:\python project\media\\bullet.png'

        elif self.name == 'Enemy':
            self.x = x + 30
            self.y = y + 30
            imageName = 'E:\python project\media\enemy_bullet.png'
        self.image = pygame.image.load(imageName)

    def move(self):
        if self.name == 'Hero':
            self.y -= 4
        elif self.name == 'Enemy':
            self.y += 4
            num = random.randint(1, 66)
            if num %2 <= 5 and (self.x >0 and self.x < 480):
                self.x += 1
            elif num %2 >=62 and (self.x >0 and self.x < 480):
                self.x -= 1

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def judge(self):
        # 子弹出界判断方法
        if self.y>852 or self.y<0:
            return True
        else:
            return False


def key_control(heroPlane,heroPlane2):
    for event in pygame.event.get():
        if event.type == QUIT:
            print("exit")
            exit()
        elif event.type == KEYDOWN:
            if event.key ==K_LEFT:
                print('left')
                heroPlane.moveLeft()
            elif event.key == K_a:
                heroPlane2.moveLeft()
            elif event.key ==K_RIGHT:
                print('right')
                heroPlane.moveRight()
            elif event.key == K_d:
                # print('right')
                heroPlane2.moveRight()
            elif event.key == K_w:
                # print('up')
                heroPlane2.moveUp()
            elif event.key ==K_UP:
                print('up')
                heroPlane.moveUp()
            elif event.key == K_s:
                # print('down')
                heroPlane2.moveDown()
            elif event.key ==K_DOWN:
                print('down')
                heroPlane.moveDown()
            elif event.key == K_SPACE:
                print('space')
                heroPlane.sheBullet()
            elif event.key == K_q:
                # print('space')
                heroPlane2.sheBullet()


def main():
    # 1. 创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((480, 852), 0, 32)

    #2. 创建一个和窗口大小的图片，用来充当背景
    background = pygame.image.load("E:\python project\media\project_plane.png")

    # 3.1 创建一个飞机对象
    heroPlane = HeroPlane(screen,180)
    heroPlane2 = HeroPlane(screen,280)
    # 3.2 创建一个敌人飞机
    enemyPlane = EnemyPlane(screen)

    # 4. 把背景图片放到窗口中显示
    while True:
        screen.blit(background, (0, 0))

        heroPlane.display()
        heroPlane2.display()

        enemyPlane.move()
        enemyPlane.display()
        enemyPlane.sheBullet()

        key_control(heroPlane,heroPlane2)

        pygame.display.update()

        # 通过延时的方式，来降低这个while循环的循环速度，从而降低了cpu占用率
        time.sleep(0.01)


if __name__ == "__main__":
    main()