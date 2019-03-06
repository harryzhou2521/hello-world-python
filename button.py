#-*-coding=utf-8-*-
import pygame.font#Pygame能够将文本渲染到屏幕
class Button():
    def __init__(self,ai_settings,screen,msg):   #，其中msg 是 要在按钮中显示的文本
        """初始化按钮的属性"""       
        self.screen = screen        
        self.screen_rect = screen.get_rect() 
        # 设置按钮的尺寸和其他属性
        self.width,self.height=200,50
        self.button_color=(0,255,0)#设置button_color 让按钮的rect 对象为亮绿色
        self.text_color=(255,255,255)#置text_color 让文本为白色
        self.font=pygame.font.SysFont(None,48)#实参None 让Pygame 使用默认字体，而48 指定了文本的字号
        #创建按钮的rect对象，并使其居中#为让按钮在屏幕上居中，我们创建一个表示按钮的rect 
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=self.screen_rect.center#，并将其center 属性设置为屏幕的center 属性
        #按钮的标签只需创建一次
        self.prep_msg(msg)
    def prep_msg(self,msg):#方法prep_msg() 接受实参self 以及要渲染为图像的文本（msg ）。
        """将msg渲染为图像，并使其在按钮上居中"""
        self.msg_image=self.font.render(msg,True,self.text_color,
        self.button_color)#方法font.render() 还接受一个布尔实参，该实参指定开启还是关闭反锯齿功能（反锯齿让文本的边缘更平滑
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center
    def draw_button(self):
    # 绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color,self.rect)#调用screen.fill() 来绘制表示按钮的矩形
        self.screen.blit(self.msg_image,self.msg_image_rect)#再调用screen.blit() ，并向它传递一幅图像以及与该图像相关联的rect 对象
