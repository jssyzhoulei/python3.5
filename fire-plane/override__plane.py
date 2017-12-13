import pygame
from pygame.locals import *
import time
import random


class Plane(object):
    def __init__(self,screen,imgName):
        self.screen = screen
        self.bulletList = []
        self.img = pygame.image.load(imgName)

    def display(self):
        needDelItemBullet = []
        self.screen.blit(self.img,(self.x,self.y))

        for i in self.bulletList:
            if i.judge():
                needDelItemBullet.append(i)

        for bullet in needDelItemBullet:
            self.bulletList.remove(bullet)

        for bullet in self.bulletList:
            bullet.display()
            bullet.move()


class HeroPlane(Plane):

    def __init__(self,screen):
        super(HeroPlane, self).__init__(screen,'E:\python project\media\plane_hero.png')
        self.x = 230
        self.y = 540

    def moveRight(self):
        self.x += 10

    def moveLeft(self):
        self.x -= 10

    def sheBullet(self):
        newBullet = Bullet(self.x,self.y,self.screen,'hero')
        self.bulletList.append(newBullet)


class EnemyPlane(Plane):
    def __init__(self,screen):
        super().__init__(screen,'E:\python project\media\enemy_plane.png')
        self.x = 0
        self.y = 0

        self.direction = 'right'

    def move(self):
        if self.direction == 'right':
            self.x += 4
        elif self.direction == 'left':
            self.x -= 4

        if self.x>480-50:
            self.direction = "left"
        elif self.x<0:
            self.direction = "right"

    def sheBullet(self):
        num = random.randint(1, 100)
        if num == 88:
            newBullet = Bullet(self.x,self.y,self.screen,'enemy')
            self.bulletList.append(newBullet)



class Bullet(object):
    def __init__(self,x,y,screen,name):
        self.screen = screen
        self.name = name

        if name == 'hero':
            self.x = x + 40
            self.y = y - 20
            self.imgName = 'E:\python project\media\\bullet.png'
        elif name == 'enemy':
            self.x = x + 30
            self.y = y + 30
            self.imgName = 'E:\python project\media\enemy_bullet.png'
        self.img = pygame.image.load(self.imgName)

    def display(self):
        self.screen.blit(self.img,(self.x,self.y))

    def move(self):
        if self.name == 'hero':
            self.y -= 5
        elif self.name == 'enemy':
            self.y += 5

    def judge(self):
        if self.y > 852 or self.y < 0:
            return True
        else:
            return False


def key_control(heroPlane):
    for event in pygame.event.get():
        if event.type == QUIT:
            print('exit')
            exit()
        elif event.type == KEYDOWN:
            if event.key ==K_a or event.key == K_LEFT:
                print('left')
                heroPlane.moveLeft()
                #控制飞机让其向左移动
            elif event.key == K_d or event.key == K_RIGHT:
                print('right')
                heroPlane.moveRight()
            elif event.key == K_SPACE:
                print('space')
                heroPlane.sheBullet()


def main():
    # 1. 创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((480, 852), 0, 32)
    # 2. 创建一个和窗口大小的图片，用来充当背景
    background = pygame.image.load("E:\python project\media\project_plane.png")
    # 创建hero飞机
    heroPlane = HeroPlane(screen)
    # 创建敌机
    enemyPlane = EnemyPlane(screen)
    while True:
        screen.blit(background, (0, 0))

        heroPlane.display()

        enemyPlane.move()
        enemyPlane.display()
        enemyPlane.sheBullet()

        key_control(heroPlane)

        pygame.display.update()

        time.sleep(0.01)


if __name__ == '__main__':
    main()
