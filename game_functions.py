#-*-coding=utf-8-*-
#这个模块中导入了事件检查循环要使用的sys 和pygame 。
#当前，函数check_events() 不需要任何形参，其函数体复制了alien_invasion.py的事件循环。 
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """响应按键"""
    if event.key==pygame.K_RIGHT:
        ship.moving_right=True
        #print "K_RIGHT",pygame.K_RIGHT
       # print "RIGHTde ",event.key
    elif event.key==pygame.K_LEFT:
        ship.moving_left=True
       # print "LEFTde :",event.key
    elif event.key==pygame.K_SPACE:
     # 创建一颗子弹，并将其加入到编组bullets中
        fire_bullet(ai_settings,screen,ship,bullets)
 #    if len(bullets)<ai_settings.bullets_allowed:
 #        new_bullet=Bullet(ai_settings,screen,ship)
 #        bullets.add(new_bullet)#add() 方法用于给集合添加元素，如果添加的元素在集合中已存在，则不执行任何操作。
 #        print new_bullet
    elif event.key==pygame.K_q:#玩家按Q时结束游戏,设置成e也行键盘
        sys.exit()
def fire_bullet(ai_settings,screen,ship,bullets):
    """如果还没有达到限制，就发射一颗子弹"""
    #创建新子弹，并将其加入到编组bullets中
    if len(bullets)<ai_settings.bullets_allowed:
        new_bullet=Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
def check_keyup_events(event,ship):
    """响应松开"""
    if event.key==pygame.K_RIGHT:
        ship.moving_right=False
    elif event.key==pygame.K_LEFT:
        ship.moving_left=False
def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    """在玩家单机play按钮时开始新游戏"""
    button_cliked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_cliked and not stats.game_active:#test if a point is inside a rectangle
        #重置游戏统计信息 #Returns true if the given point is inside the rectangle
        stats.reset_stats()
        stats.game_active=  True
        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        #清空外星人列表和子弹列表
        # 重置游戏设置   
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        #隐藏光标
        stats.reset_stats()#单击了Play按钮且 且 游戏当前处于非活动状态
        stats.game_active=True
    #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
    #创建一群新的外星人，并将飞船居中
    create_fleet(ai_settings,screen,ship,aliens)
    ship.center_ship()
        
#def check_events(ship): 
#    for event in pygame.event.get():#从队列中获取事件get events from the queue这是一个pygame的事件
#        if event.type ==pygame.QUIT:#，并将事件循环替换为对函数check_events() 调用
#            sys.exit()
#        elif event.type==pygame.KEYDOWN:#KEYDOWN是个事件
#            if event.key==pygame.K_RIGHT:
#                ship.moving_right=True
#            elif event.key==pygame.K_LEFT:
#                ship.moving_left=True
#        elif event.type==pygame.KEYUP:
#            if event.key==pygame.K_RIGHT:#如果因玩家按下K_LEFT 键而触发了KEYDOWN 事件，我们就将moving_left 设置为True 
#                ship.moving_right=False
#            elif event.key==pygame.K_LEFT:#如果因玩家松开K_LEFT 而触发了KEYUP 事件，我们就将moving_left 设置 为False 
#                ship.moving_left=False
#            #向右移动飞船
#                ship.rect.centerx+=1
#
#
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    #每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)#screen.fill() 用背景色填充屏
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()  
    ship.blitme()#填充背景后，我们调 用ship.blitme() 将飞船绘制到屏幕上，确保它出现在背景前面
    aliens.draw(screen)#在屏幕上绘制编组中的每个外星人
    #alien.blitme()
    # 显示得分
    sb.show_score()
    # 如果游戏处于非活动状态，就显示Play按钮
    if not stats.game_active:
        play_button.draw_button()
    #让最近绘制的屏幕可见
    pygame.display.flip()
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """更新子弹的位置，并删已消失的子弹"""
    #更新子弹的位置
    bullets.update()
    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
        # 检查是否有子弹击中了外星人  
        # 如果是这样，就删除相应的子弹和外星  
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)
   # collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    #if len(aliens)==0:
        #删除现有的子弹并新建一群外星人
     #   bullets.empty()
     #   create_fleet(ai_settings,screen,ship,aliens)
def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """响应子弹和外星人的碰撞"""
    #删除发生碰撞的子弹和外星人
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)#当为True的时候，会删除组中所有冲突的精灵，False的时候不会删除冲突的精灵
    if collisions: 
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points*len(aliens)      
            sb.prep_score() 
        check_high_score(stats,sb)
    if len(aliens)==0:
        #删除现有的子弹，并创建一个新的外星人群
        # 如果整群外星人都被消灭，就提高一个等级
        bullets.empty()
        ai_settings.increase_speed()
          # 提高等级 ❶  
        stats.level += 1 
        sb.prep_level()   
        create_fleet(ai_settings, screen, ship, aliens)
#def create_fleet(ai_settings, screen, aliens):     
#    """创建外星人群"""     
#    # 创建一个外星人，并计算一行可容纳多少个外星人     
#    # 外星人间距为外星人宽度 ❶     
#    alien = Alien(ai_settings, screen)    
#    alien_width = alien.rect.width 
#    available_space_x = ai_settings.screen_width - alien_width 
#    number_aliens_x = int(available_space_x / (1.5* alien_width))   
#    # 创建第一行外星人 ❺     
#    for alien_number in range(number_aliens_x):     
#    # 创建一个外星人并将其加入当前行 ❻     
#        alien = Alien(ai_settings, screen)
#        alien.x = alien_width + 1.5* alien_width * alien_number     
#        alien.rect.x = alien.x       
#        aliens.add(alien)
#def create_fleet(ai_settings,screen,aliens):
#    """创建外星人群"""
#    #创建一个外星人，并计算一行可容纳多少个外星人
#    #外星人间距为外星人宽度的1/2
#    alien=Alien(ai_settings,screen)
#    alien_width=alien.rect.width
#    available_space_x=ai_settings.screen_width-2*alien_width
#    number_aliens_x=int(available_sapce_x/(1.5*alien_width)
#    #创建第一行外星人
#    for alien_number in range(number_aliens_x):     
#   # 创建一个外星人并将其加入当前行 ❻     
#        alien = Alien(ai_settings, screen)
#        alien.x=alien_width+1.5*alien_width*alien_number
#        alien.rect.x=alien.x
#        aliens.add(alien)
def get_number_aliens_x(ai_settings,alien_width):
    """计算每行可容纳多少个外星人"""
    available_sapce_x=ai_settings.screen_width-0.5*alien_width
    number_aliens_x=int(available_sapce_x/(1.5*alien_width))
    return number_aliens_x
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其加入当前行"""
    alien=Alien(ai_settings,screen)
    alien_width=alien.rect.width
    alien.x=alien_width+1.5*alien_width*alien_number
    alien.rect.x=alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)
def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    #创建一个外星人，并计算每行可容纳多少个外星人
    alien=Alien(ai_settings,screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width) 
    number_rows=get_number_rows(ai_settings,ship.rect.height,
    alien.rect.height)
    #创建第一行外星人
   # for alien_number in range(number_aliens_x):
  #      create_alien(ai_settings,screen,aliens,alien_number,row_number)
    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,
            row_number)
def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y=(ai_settings.screen_height-(2*alien_height)-ship_height)
    number_rows=int(available_space_y/(3*alien_height))
    return number_rows
def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """响应被外星人撞到的飞船"""
    #将ships_left减1
    if stats.ships_left>0:
        #将ships_left减1
        stats.ships_left-=1
         # 更新记分牌 ❺      
        sb.prep_ships()
    #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
     # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
     #暂停
        sleep(1)
    else :
        stats.game_active=False
        pygame.mouse.set_visible(True)
    
def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """检查是否有外星人到达屏幕边缘        
    然后更新所有外星人的位置
    检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    """
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
        print("Ship hit!!!")
    #方法spritecollideany() 接受两个实参：一个精灵和一个编组。它检查编组是否有成员与精灵发生了碰撞，
    #并在找到与精灵发生了碰撞的成员后就停止遍历编组
    # 检查是否有外星人到达屏幕底端 
    check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)
    
def check_fleet_edges(ai_settings,aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
def change_fleet_direction(ai_settings,aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1

def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """检查是否有外星人位于屏幕底端"""
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
        # 像飞船被撞到一样进行处理
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
            break
def check_high_score(stats, sb):      
    """检查是否诞生了新的最高得分"""      
    if stats.score > stats.high_score:     
        stats.high_score = stats.score         
        sb.prep_high_score()
           
    
