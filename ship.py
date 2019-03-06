#-*- coding=utf-8 -*-
import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        """初始化飞船并设置其初始位置"""
        super(Ship,self).__init__()
        self.screen=screen
        self.ai_setting=ai_settings
        self.image=pygame.image.load(r'images\ship2.bmp')
        self.rect=self.image.get_rect()#处理矩形（rect 对象）
        self.screen_rect=screen.get_rect()
        #将每艘飞船放在屏幕底部中央
        self.rect.centerx=self.screen_rect.centerx#要将游戏元素居中，可设置相应rect 对象的属性center 、centerx 或centery 
        self.rect.bottom=self.screen_rect.bottom
        #在飞船的属性center中存储小数值
        self.center=float(self.rect.centerx)#因为centerx只能存储整数
        #移动标志
        self.moving_right=False#为Ship类添加一个名为moving_right的属性
        self.moving_left=False
    def update(self):           #和一个名为update的方法    
        """根据移动标志调整飞船的位置"""
        #更新飞船的center值，而不是rect    #self.rect.right返回飞船外接矩形的右边缘的 x 坐标
        if self.moving_right and self.rect.right<self.screen_rect.right:    #为什么用两个if是因为防止同时按住左键和右键
            self.center+=self.ai_setting.ship_speed_factor
        if self.moving_left and self.rect.left>0:#飞船将在触及屏幕左边缘或右边缘后停止移动
            self.center-=self.ai_setting.ship_speed_factor
        self.rect.centerx=self.center
    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)
    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center=self.screen_rect.centerx
