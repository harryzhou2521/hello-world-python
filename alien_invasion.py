#coding=utf-8
import sys
import pygame
from setting import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
#from alien import Alien
import game_functions as gf#名称太长，想要给它取个别名，以后每次用到它的时候都用它的别名代替它

def run_game():
    #初始化pygame、设置和屏幕对象
    pygame.init()#初始化所有导入的 pygame 模块#返回的一个pygame.Surface对象，而元组（1200,800）代表屏幕设置的长宽
    ai_settings=Settings()#调用类使用
    #这里的ai_注意这个写法是上面被调用的
    screen=pygame.display.set_mode(#创建一个长宽的窗口
        (ai_settings.screen_width,ai_settings.screen_height))#pygame.display.set_mode(resolution=(0,0),flags=0,depth=0)
    pygame.display.set_caption("Alien Invasion")
    #创建一个用于存储游戏统计信息的实例
    # 创建存储游戏统计信息的实例，并创建记分牌
    stats=GameStats(ai_settings)
    sb=Scoreboard(ai_settings,screen,stats)
    #print stats
     # 创建一艘飞船
    ship=Ship(ai_settings,screen)
     # 创建Play按钮 
    play_button = Button(ai_settings,screen,"Play")
   # print play_button
    #创建一个外星人
   # alien=Alien(ai_settings,screen)
    # bg_color=(230,230,100)#设置背景色
    #创建一个用于存储子弹的编组
    bullets=Group()
    aliens=Group()#创建了一个空编组
    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)
    # 开始游戏主循环
    while True:
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)#我们需要更新调用的check_events() 代码，将ship 作为实参传递给它
        ship.update()
        #删除已消失的子弹
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            #print(len(bullets))
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)    
        # 每次循环时都重绘屏
        # 让最近绘制的屏幕可见
run_game()

    
