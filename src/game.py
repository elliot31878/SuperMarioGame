import pygame
import time
import random
import os
import ctypes
import pyautogui
import sqlite3
#-----------------------------------------------------------------
#global  varible and init Form
display_width=800
display_height=600
username=""
sex=2
#--------------------For Center Form in Desktop----------------------------------------------------
width,height=pyautogui.size()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((width-display_width)/2,(height-display_height)/2)
pygame.init()
#--------------------------Sounds-------------------------------
world_sound=pygame.mixer.Sound(r"assets\audio\world-m.ogg")
lose_sound=pygame.mixer.Sound(r"assets\audio\lose-m.wav")
win_sound=pygame.mixer.Sound(r"assets\audio\win-m.wav")
price_sound=pygame.mixer.Sound(r"assets\audio\price-m.wav")
jump_sound=pygame.mixer.Sound(r"assets\audio\jump-m.wav")
crashe_sound=pygame.mixer.Sound(r"assets\audio\itemdestroy-m.wav")
#-----------------------------------------------------------------
# Colors And Fonts
black=(0,0,0)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = black
FONT = pygame.font.Font(r"assets\font\arial.ttf", 15)
white=(255,255,255)
blue=(0,0,255)
color_btn_go=(66, 103, 178)
color_btn_exit=(255,40,40)
color_btn_go_enter=(45, 103, 178)
color_btn_exit_enter=(230, 40, 40)
#-----------------------------------------------------------------
#Attribute Form
gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("SuperMario")
icon_program=pygame.image.load(r"assets\image\supermario_icon.png")
pygame.display.set_icon(icon_program)
fps=pygame.time.Clock()
user32 = ctypes.windll.user32
#-----------------------------------------------------------------
#Load Image  .... :)
marioImage=pygame.image.load(r"assets\image\supermario.png")
crown_image=pygame.image.load(r"assets\image\crown.png")
coinImage=pygame.image.load(r"assets\image\coin.gif")
enemy_image=pygame.image.load(r"assets\image\mario_enemy.png")
enemy_place_image=pygame.image.load(r"assets\image\mario_enemy_place.png")
heart_1=pygame.image.load(r"assets\image\heart.png")
heart_2=pygame.image.load(r"assets\image\heart.png")
heart_3=pygame.image.load(r"assets\image\heart.png")
user_image=pygame.image.load(r"assets\image\user_smallboy.png")
user_image_boy=pygame.image.load(r"assets\image\user_smallboy.png")
user_image_girl=pygame.image.load(r"assets\image\user_smallgirl.png")
register_bg=pygame.image.load(r"assets\image\register_bg.png")
#-----------------------DatabaseClass-----------------------------
class DataBase(object):
    def __init__(self,database_file_name,sql_command):
        self.sql_command=sql_command
        self.database_file_name=database_file_name
        connction=sqlite3.connect(self.database_file_name)
        cursor=connction.cursor()
        cursor.execute(self.sql_command)
        connction.commit()
        connction.close()
    def INSERT(self,sql_command,database_file_name):
        self.sql_command=sql_command
        self.database_file_name=database_file_name
        connction=sqlite3.connect(self.database_file_name)
        cursor=connction.cursor()
        cursor.execute(self.sql_command)
        connction.commit()
        connction.close()
    @staticmethod
    def Show(sql_command,database_file_name):
        lst_data=[]
        sql_command=sql_command
        database_file_name=database_file_name
        connction=sqlite3.connect(database_file_name)
        cursor=connction.cursor()
        cursor.execute(sql_command)
        rows=cursor.fetchall()
        for row in rows:
            lst_data.append(row)
        connction.commit()
        connction.close()
        return lst_data
    def update(self,sql_command,database_file_name,task):
        self.sql_command=sql_command
        self.database_file_name=database_file_name
        connction=sqlite3.connect(self.database_file_name)
        cur = connction.cursor()
        cur.execute(self.sql_command,task)
        connction.commit()
        connction.close()
#-----------------------------------------------------------------
def set_characters(characters,x,y):
    gameDisplay.blit(characters,(x,y))
#-----------------------------------------------------------------
def crashed():
    world_sound.stop()
    lose_sound.play()
    text="Game Over"
    largeText=pygame.font.Font(r"assets\font\arial.ttf",100)
    TextSurf,TextRect=text_objects(text,largeText,color_btn_exit_enter)
    TextRect.center=((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf,TextRect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                SystemExit
        button("Tryagain",250,100,100,50,color_btn_go,color_btn_go_enter,"p")
        button("Exit",450,100,100,50,color_btn_exit,color_btn_exit_enter,"qmenu")
        pygame.display.update()
    start_game()
def youwin():
    world_sound.stop()
    win_sound.play()
    text="You Win"
    largeText=pygame.font.Font(r"assets\font\arial.ttf",100)
    TextSurf,TextRect=text_objects(text,largeText,color_btn_exit_enter)
    TextRect.center=((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf,TextRect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                SystemExit
        button("Play again",250,100,100,50,color_btn_go,color_btn_go_enter,"p")
        button("Exit",450,100,100,50,color_btn_exit,color_btn_exit_enter,"q")
        pygame.display.update()
    start_game()
def text_objects(text,font,color):
    textSurface=font.render(text,True,color)
    return textSurface,textSurface.get_rect()
#-----------------------------------------------------------------
def intersect(x_object1,y_object1,object1_width,x_object2,y_object2,object2_width):
    #object 1 :mario
    #obhect 2:enemy
    if y_object1<y_object2+object2_width and not(y_object1<y_object2-object2_width):
        if x_object1>x_object2 and  x_object1<x_object2+object2_width or x_object1+object1_width>x_object2 and x_object1+object1_width<x_object2+object2_width:
            return True
    return False
#-----------------------------------------------------------------
def button(text,x,y,w,h,ic,ac,action,txt_user="",txt_pass="",alpha=0):
    global sex
    gender=sex
    mouse_position=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+w>mouse_position[0]>x and y+h>mouse_position[1]>y:
        pygame.draw.rect(gameDisplay,ac,(x,y,w,h),alpha)
        if click[0]==1 and action=="p":
            start_game()
        elif click[0]==1 and action=="q":
            pygame.quit()
            SystemExit
        elif click[0]==1 and action=="qmenu":
            main()
        elif click[0]==1 and action=="r":
            register()       
        elif click[0]==1 and action=="register":
            #register
            if txt_user=="" or txt_pass=="" or gender>1:
                register("error")
            if gender<=1 and txt_user!="" and txt_pass!="":
                command_create="""
                CREATE TABLE IF NOT EXISTS MarioLogin (
                user TEXT PRIMARY KEY,
                password TEXT,
                islogin byte,
                gender byte
                );
                """
                db=DataBase("DbTable_Register",command_create)
                command_insert="INSERT OR REPLACE  INTO MarioLogin VALUES ('"+str(txt_user)+"','"+str(txt_pass)+"','"+str(1)+"','"+str(gender)+"');"
                db.INSERT(command_insert,"DbTable_Register")
                main("r")
        elif click[0]==1 and action=="l":
            
            command_create="""
            CREATE TABLE IF NOT EXISTS MarioLogin (
            user TEXT PRIMARY KEY,
            password TEXT,
            islogin byte,
            gender byte
            );
            """
            db=DataBase("DbTable_Register",command_create)
            command_update="""UPDATE MarioLogin SET islogin = ? WHERE user = ?"""
            user=DataBase.Show("SELECT user FROM MarioLogin WHERE islogin='1'","DbTable_Register")
            data=(0,user[0][0])
            db.update(command_update,"DbTable_Register",data)
            register()
        elif click[0]==1 and action=="man":
            sex=1
        elif click[0]==1 and action=="woman":
            sex=0
    else:
        pygame.draw.rect(gameDisplay,ic,(x,y,w,h),alpha)
    smallText=pygame.font.Font(r"assets\font\arial.ttf",20)
    TextSurf,TextRect=text_objects(text,smallText,white)
    TextRect.center=((x+(w/2)),(y+(h/2)))
    gameDisplay.blit(TextSurf,TextRect)
#-----------------------------------------------------------------
class TextBox:
    def __init__(self, x, y, w, h,ispass, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.ispass=ispass
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                if self.ispass:
                    self.txt_surface = FONT.render("*"*len(self.text), True, self.color)
                elif not self.ispass:
                    self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
    def get_Text(self):
        return self.text
#-----------------------------------------------------------------
def register(msg=""):
    txt_1=TextBox((display_width-180)/2, (display_height-32)/2, 140, 32,False)
    txt_2=TextBox((display_width-180)/2, ((display_height-32)/2)+50, 140, 32,True)
    TextBoxs=[txt_1,txt_2]
    done = False
    while not done:
        set_characters(register_bg,0,0)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
                main()
            for box in TextBoxs:
                box.handle_event(event)
        for box in TextBoxs:
            box.update()
        for box in TextBoxs:
            box.draw(gameDisplay)
        #-----------MakeUsernameLable---------------------------------------------
        if msg=="error":
            text="* username and password is Empty or Not SELECT GENDER :) "
            textsurf,textect=text_objects(text,FONT,(190,40,40))
            textect.center=(((display_width-250)/2)+50, ((display_height-32)/2)-40)
            gameDisplay.blit(textsurf,textect)
        #------------------------------------------------------------------------------
        text="Username : "
        textsurf,textect=text_objects(text,FONT,white)
        textect.center=(((display_width-180)/2)-50, ((display_height-32)/2)+13)
        gameDisplay.blit(textsurf,textect)
        #-------------------------------------------------------------------------
        text_pass="Password : "
        textsurf_pass,textect_pass=text_objects(text_pass,FONT,white)
        textect_pass.center=(((display_width-180)/2)-50, ((display_height-32)/2)+65)
        gameDisplay.blit(textsurf_pass,textect_pass)
        button("Register",display_width*0.45,display_height*0.8,100,45,color_btn_go,color_btn_go_enter,"register",txt_1.get_Text(),txt_2.get_Text())
        button("",((display_width-180)/2)+50, ((display_height-32)/2)+100,45,45,(91,131,218),color_btn_go_enter,"man",2)
        button("",((display_width-180)/2)+100, ((display_height-32)/2)+100,45,45,(91,131,218),color_btn_go_enter,"woman",2)
        set_characters(user_image_boy,((display_width-180)/2)+50, ((display_height-32)/2)+100)
        set_characters(user_image_girl,((display_width-180)/2)+100, ((display_height-32)/2)+100)
        pygame.display.update()
#-----------------------------------------------------------------
def main(isRegister="n"):
    user_xposition,user_yposition=5,70
    coin=0
    coins=0
    username=([" ",])
    inPage=True
    try:
        username=DataBase.Show("SELECT user FROM MarioLogin WHERE islogin='1'","DbTable_Register")
        coins=DataBase.Show("SELECT coin FROM Mario WHERE user='"+username[0][0]+"'","DbTable")
        coin=coins[0][0]
    except Exception as ex:
        pass
    try:
        genders=DataBase.Show("SELECT gender FROM MarioLogin WHERE islogin='1'","DbTable_Register")
        gender=genders[0][0]
    except Exception as ex:
        gender=1
    try:
        isLogin=DataBase.Show("SELECT islogin FROM MarioLogin WHERE islogin='1'","DbTable_Register")
        if isLogin[0][0]==0:
            isRegister="n"
        else:
            isRegister="r"     
    except Exception as identifier:
        pass
    while inPage:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                SystemExit
        backgroundImage=pygame.image.load(r"assets\image\bgmain.png")
        gameDisplay.blit(backgroundImage,[0,0])
        text="WELCOME"
        text2="To"
        text3="MRROBOT GAME :) "
        oneText=pygame.font.Font(r"assets\font\arial.ttf",15)
        TextSurf,TextRect=text_objects(text,oneText,white)
        TextRect.center=(675,400)
        gameDisplay.blit(TextSurf,TextRect)
        TextSurf1,TextRect1=text_objects(text2,oneText,color_btn_go)
        TextRect1.center=(675,425)
        gameDisplay.blit(TextSurf1,TextRect1)
        TextSurf2,TextRect2=text_objects(text3,oneText,color_btn_go_enter)
        TextRect2.center=(680,450)
        gameDisplay.blit(TextSurf2,TextRect2)
        button("Exit",620,330,100,50,color_btn_exit,color_btn_exit_enter,"q")
        if isRegister=="n":
            button("Register",620,150,100,50,(0,200,0),(20,155,20),"r")
            button("Play",620,220,100,50,(192,192,192),(192,192,192),"enabel_p")
        else:
            button("Logout",620,150,100,50,(0,200,0),(20,155,20),"l")
            button("Play",620,220,100,50,color_btn_go,color_btn_go_enter,"p")
        #-----------------------------------------------------
        font=pygame.font.Font(r"assets\font\arial.ttf",20)
        text=font.render(str(coin),True,blue)
        gameDisplay.blit(text,(53,15))
        set_characters(coinImage,5,5)
        #-----------------------------------------------------
        if gender==0:
            set_characters(user_image_girl,user_xposition,user_yposition)
        elif gender==1:
            set_characters(user_image_boy,user_xposition,user_yposition)
        font=pygame.font.Font(r"assets\font\arial.ttf",20)
        text=font.render(str(username[0][0]),True,blue)
        gameDisplay.blit(text,(user_xposition+50,user_yposition+10))
        pygame.display.update()
def start_game():
    filipv=False
    world_sound.play(-1)
    mario_width=45
    move=5
    move_enemy=5
    move_enemy_place=1
    move_coin=5
    enemy_width=45
    x_change=0
    y_change=(display_height*0.8+5)
    right_or_left="r"
    #--------------Positions Characters------------------------
    mario_xposition=(display_width*0.45)
    mario_yposition=(display_height*0.8+5)
    enemy_xposition=random.randint(5,display_width-45)
    enemy_yposition=-600
    coin_xposition=random.randint(5,display_width-45)
    coin_yposition=-600
    enemy_place_xposition=(display_width*2)
    enemy_place_yposition=(display_height*0.8+5)
    heart_1_xposition,heart_2_xposition,heart_3_xposition=5,50,95
    heart_1_yposition,heart_2_yposition,heart_3_yposition=60,60,60
    crown_xposition,crown_yposition=display_width-50,5
    user_xposition,user_yposition=display_width-50,65
    dead=3
    coins=0
    scores=0
    genders=0
    try:
        username=DataBase.Show("SELECT user FROM MarioLogin WHERE islogin='1'","DbTable_Register")
        coins=DataBase.Show("SELECT coin FROM Mario WHERE user='"+username[0][0]+"'","DbTable")
        scores=DataBase.Show("SELECT score FROM Mario WHERE user='"+username[0][0]+"'","DbTable")
        coin=coins[0][0]
        score_max=scores[0][0]
    except Exception as ex:
        #trick ;)
        print("catch",ex)
        coin=0
        score_max=0
       
    try:
        genders=DataBase.Show("SELECT gender FROM MarioLogin WHERE islogin='1'","DbTable_Register")
        gender=genders[0][0]
    except Exception as ex:
        gender=1
    score=0
    #---------------------------------------------------
    quit_game=False
    while not quit_game:   
        #read All Events
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                SystemExit
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    #got to Left
                    x_change=-move
                    right_or_left="l"
                    filipv=True
                elif event.key==pygame.K_RIGHT:
                    #go to Right
                    x_change=move
                    filipv=False
                    right_or_left="r"
                elif event.key==pygame.K_SPACE:
                    y_change=(display_height*0.8+5)-70
                    if right_or_left=="r":
                        x_change=+(move**3)
                    else:
                        x_change=-(move**3)
                    jump_sound.play()
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    #stop
                    x_change=0
        mario_xposition+=x_change
        mario_yposition=y_change
        #stop Out of Form-----------------------------------
        if mario_xposition<=0:
            mario_xposition=5
        if mario_xposition>=display_width-mario_width:
            mario_xposition=display_width-mario_width
        #----------------------setBackground----------------
        backgroundImage=pygame.image.load(r"assets\image\place.png")
        gameDisplay.blit(backgroundImage,[0,0])
        #---------------setLableScoreAnd Coin-----------------------
        font=pygame.font.Font(r"assets\font\arial.ttf",20)
        text=font.render(str(coin),True,blue)
        gameDisplay.blit(text,(53,15))
        set_characters(coinImage,5,5)
        #setCharAndCrown------------------------------------------
        font=pygame.font.Font(r"assets\font\arial.ttf",20)
        text=font.render(str(score),True,blue)
        gameDisplay.blit(text,(display_width-70,15))
        set_characters(crown_image,crown_xposition,crown_yposition)
        #----------------------MaxScore-----------------------
        font_max=pygame.font.Font(r"assets\font\arial.ttf",20)
        text_max=font_max.render(str(score_max),True,blue)
        gameDisplay.blit(text_max,(display_width-70,80))
        if gender==0:
            set_characters(user_image_girl,user_xposition,user_yposition)
        elif gender==1:
            set_characters(user_image_boy,user_xposition,user_yposition)
        #----------setCharacters----------------------------
        surf = pygame.transform.flip(marioImage, filipv, False)
        set_characters(surf,mario_xposition,mario_yposition)
        set_characters(enemy_image,enemy_xposition,enemy_yposition)
        set_characters(coinImage,coin_xposition,coin_yposition)
        set_characters(enemy_place_image,enemy_place_xposition,enemy_place_yposition)
        set_characters(heart_1,heart_1_xposition,heart_1_yposition)
        set_characters(heart_2,heart_2_xposition,heart_2_yposition)
        set_characters(heart_3,heart_3_xposition,heart_3_yposition)
        #----------------------------------------------------
        pygame.display.update()
        if not mario_yposition==(display_height*0.8+5):
            y_change=(display_height*0.8+5)
            x_change=0
            set_characters(marioImage,mario_xposition,mario_yposition)
            pygame.display.update()
            time.sleep(0.03)
        #  set Fps 
        fps.tick(80)
        enemy_yposition+=move_enemy
        coin_yposition+=move_coin
        enemy_place_xposition-=move_enemy_place
        if  score==100:
            youwin()
        if enemy_yposition>display_height:
            enemy_yposition=-200
            enemy_xposition=random.randrange(5,display_width-45)
            if score>1 and score%5==0:
                move_enemy+=1
                move_coin+=1
        if coin_yposition>display_height:
            coin_yposition=-200
            coin_xposition=random.randrange(5,display_width-45)
        if enemy_place_xposition<0:
            enemy_place_xposition=(display_width*2)
            enemy_place_yposition=(display_height*0.8+5)
        #------------------------------Crashed------------------------------------------------------------------
        if intersect(mario_xposition,mario_yposition,mario_width,enemy_xposition,enemy_yposition,enemy_width):
            crashe_sound.play()
            dead=dead-1
            if dead==2:
                heart_1_yposition=-1000
                enemy_yposition=-200
                enemy_xposition=random.randrange(5,display_width-45)
            if dead==1:
                heart_2_yposition=-1000
                enemy_yposition=-200
                enemy_xposition=random.randrange(5,display_width-45)
            if dead==0:
                heart_3_yposition=-1000
                enemy_yposition=-200
                enemy_xposition=random.randrange(5,display_width-45)
                crashed() 
        if intersect(mario_xposition,mario_yposition,mario_width,enemy_place_xposition,enemy_place_yposition,enemy_width):
            crashe_sound.play()
            dead=dead-1
            if dead==2:
                heart_1_yposition=-1000
                enemy_place_xposition=(display_width*2)
            if dead==1:
                heart_2_yposition=-1000
                enemy_place_xposition=(display_width*2)
            if dead==0:
                heart_3_yposition=-1000
                enemy_place_xposition=(display_width*2)
                crashed()  
        if intersect(mario_xposition,mario_yposition,mario_width,coin_xposition,coin_yposition,mario_width):
            coin_yposition=-200
            coin_xposition=random.randrange(5,display_width-45)
            coin=coin+1
            if coin%5==0:
                score=score+1
            command_create="""
            CREATE TABLE IF NOT EXISTS Mario (
            user TEXT PRIMARY KEY,
            coin INTEGER,
            score INTEGER
            );
            """
            username=DataBase.Show("SELECT user FROM MarioLogin WHERE islogin='1'","DbTable_Register")
            db=DataBase("DbTable",command_create)
            if score>score_max:
                command_insert="INSERT OR REPLACE  INTO Mario VALUES ('"+str(username[0][0])+"','"+str(coin)+"','"+str(score)+"');"
            else:
                command_insert="INSERT OR REPLACE  INTO Mario VALUES ('"+str(username[0][0])+"','"+str(coin)+"','"+str(score_max)+"');"
            db.INSERT(command_insert,"DbTable")
            price_sound.play()         
#--------mainFunction---------------------------------------------
try:
    main()
except:
    pass

