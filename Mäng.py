import pygame
import os
import time
from random import randrange
from random import randint

#Always displays game screen in the middle of the computer screen
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
grey = (220, 220, 220)
darkgrey = (119,136,153)

FPS = 30

display_width = 800
display_height = 600

bg = pygame.image.load("space.jpg")
gameDisplay = pygame.display.set_mode((display_width,display_height))
helpDisplay = pygame.display.set_mode((display_width,display_height))

def picture_resize(image_name, divider):
    picture = pygame.image.load(image_name).convert_alpha()
    width = int(picture.get_size()[0]/divider)
    height = int(picture.get_size()[1]/divider)
    pic_icon = pygame.transform.scale(picture, (width, height))
    
    return pic_icon, width, height

player, size_x, size_y = picture_resize("spaceship.png", 10)
angry, angry_width, angry_height = picture_resize("angryface.png", 1.5)
minus, minus_width, minus_height = picture_resize("minus.png", 1.5)
plus, plus_width, plus_height = picture_resize("plus.png", 1.5)
gift, gift_width, gift_height = picture_resize("gift.png", 12.6)
ghost, ghost_width, ghost_height = picture_resize("ghost.png", 7)

pygame.display.set_caption('Mäng')

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 40)

#Variables for displaying text in center of screen
center_x = display_width/2
center_y = display_height/2



def drawing_by_level(blocks, fireball_width,fireball_height, speed_min, speed_max):
    s = randint(5, 25)
    fireball_x = int(fireball_width/s)
    fireball_y = int(fireball_height/s)
    x=randrange(0,display_width - fireball_x)
    speed=randint(speed_min,speed_max)
    y=0-fireball_y
    blocks+=[[x,y, fireball_x, fireball_y,speed]]
    return blocks

def show_time(start):
    new_time=time.time()-start
    text=str(round(new_time))
    text_width, text_height = font.size(text)
    message(display_width-text_width-20, 20, text, white)
    return new_time

def show_score(count):
    text=str(count)
    text_width, text_height = font.size(text)
    message(display_width-text_width-20, 20, text, white)
    return count

def show_bonus(bonus_list,bonus_max_time):
    text=''
    for j in bonus_list:
        text=text+' '+j+' '+str(bonus_max_time-round(time.time()-bonus_list[j]))
    message(20,20,text,white)
    
def message(x,y,tekst,color):
    textsurface = font.render(tekst, True, color)
    gameDisplay.blit(textsurface,(x,y))

#Two functions for displaying text on center of screen
def textObjects (text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
def message_center(msg, color, y_displace=0, center_x=center_x, center_y=center_y,a=1):
    textSurf, textRect = textObjects(msg, color)
    textRect.center = (center_x), (center_y)+y_displace
    gameDisplay.blit(textSurf, textRect)
    
def button(text, color, x, y, width, height):
    pygame.draw.rect(gameDisplay, color, (x, y, width, height))
    message_center(text, black, 0, x+width/2, y+height/2)
    
#Start screen
def gameIntro():
    intro = True
    level = ''
    mode = 'time'
    
    button_x = 140
    button_y = 50
    
    button_loc_y = display_height/2+200
    mediumButton_x = display_width/2-button_x/2
    easyButton_x = mediumButton_x-200
    hardButton_x = mediumButton_x+200
    
    help_x = display_width-200
    help_y = display_height-550
    
    timeMode_x = display_width/2 -200
    scoreMode_x = display_width/2 + 50
    modeButton_y = display_height/2
    
    scorecolor = grey
    timecolor = darkgrey
    
    print(intro)
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                
                #when one of the mode buttons is clicked, it changes color + mode is chosen
                if (timeMode_x < mouse_x < timeMode_x+button_x) and (modeButton_y < mouse_y < modeButton_y + button_y):
                    timecolor = darkgrey
                    scorecolor = grey
                    mode = 'time'
                    
                if (scoreMode_x < mouse_x < scoreMode_x+button_x) and (modeButton_y < mouse_y < modeButton_y + button_y):
                    timecolor = grey
                    scorecolor = darkgrey
                    mode = 'score'
                    
                #Choose which level you want to play     
                if (easyButton_x < mouse_x < easyButton_x + button_x) and (button_loc_y < mouse_y < button_loc_y + button_y):
                    level = 'easy'
                    intro = False
                if (mediumButton_x < mouse_x < mediumButton_x + button_x) and (button_loc_y < mouse_y < button_loc_y + button_y):
                    level = 'medium'
                    intro = False
                if (hardButton_x < mouse_x < hardButton_x + button_x) and (button_loc_y < mouse_y < button_loc_y + button_y):
                    level = 'hard'
                    intro = False
                       
                #What happens when you click Help button
                if (help_x < mouse_x < help_x + button_x) and (help_y < mouse_y < help_y + button_y):
                    helpScreen()
                    intro = False
                    
        gameDisplay.blit(bg, (0,0))

        message_center("The aim of the game is to avoid fireballs", white, -100)
        message_center("Choose your game mode", white, -50)

        button("Time", timecolor, timeMode_x, modeButton_y, button_x, button_y)
        button("Score", scorecolor, scoreMode_x, modeButton_y, button_x, button_y)
        
        message_center("Choose your level", white, +150)
        
        button("Easy", grey, easyButton_x, button_loc_y, button_x, button_y)
        button("Medium", grey, mediumButton_x, button_loc_y, button_x, button_y)
        button("Hard", grey, hardButton_x, button_loc_y, button_x, button_y)
        
        button("Help", grey, help_x, help_y, button_x, button_y)
        
        pygame.display.update()
        clock.tick(FPS)
        
    #return level, mode
    gameLoop(level, mode)

def helpScreen():
    
    
    exit = False
    
    x = 50
    y = 50
    
    button_x = 140
    button_y = 50
    go_back_x = display_width - 750
    go_back_y = display_height - 550
    
    while exit == False:
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                
                if (go_back_x < mouse_x < go_back_x + button_x) and \
                (go_back_y < mouse_y < go_back_y + button_y):
                    exit = True
                    
        helpDisplay.blit(bg, (0,0))
        
        button("Go back", grey, go_back_x, go_back_y, button_x, button_y)
        
        message(x, y*2+10, "The game has two modes: time and score.", white)
        message(x, y*3, "You can play each level a certain amount of time", white)
        message(x, y*4-10, "or collect as many points as possible on each level.", white)
        message(x*2, y*5, "There are some bonuses which you can collect:", white)
        
        helpDisplay.blit(plus, (x, y*6))
        message(x*2, y*6, "Makes the speed of fireballs faster for 5 seconds", white)
        
        helpDisplay.blit(minus, (x, y*7))
        message(x*2, y*7, "Makes the speed of fireballs slower for 5 seconds", white)
        
        helpDisplay.blit(ghost, (x, y*8))
        message(x*2, y*8, "Gives you immunity from fireballs for 5 seconds", white)
        
        message(x*2, y*9, "Score mode has two extra bonuses: ", white)
        
        helpDisplay.blit(angry, (x, y*10))
        message(x*2, y*10, "Takes off 5 points from your score", white)
        
        helpDisplay.blit(gift, (x, y*11))
        message(x*2, y*11, "Adds 5 points to your score", white)
        
        pygame.display.update()
    
    
        clock.tick(FPS)
    
    gameIntro()
    
def gameLoop(level, mode):
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height-50
    lead_x_change = 0
    lead_y_change = 0  
    
    start_time=time.time()
    blocks=[]
    block_count = 0
    
    fireball, fireball_width, fireball_height = picture_resize("fireball.png", 1)
    
    state='Game Over'
    start=time.time()
    
    plus_frequency = randint(10,20)
    plus_time=time.time() #ghost start time
    plus_x = randrange(0,display_width - plus_width)
    plus_y = 0 - plus_width - randint(500,5000)
    #plus_y = 0 - plus_width 
    faster_speed= False
    plus_immunity_time = time.time()

    minus_frequency = randint(10,20)
    minus_time=time.time() #ghost start time
    minus_x = randrange(0,display_width - minus_width)
    minus_y = 0 - minus_width - randint(500,5000)
    #minus_y = 0 - minus_width -200
    slower_speed= False
    minus_immunity_time = time.time()
    
    #variable for how long immunity lasts
    ghost_immunity_time = time.time()
    ghost_immunity = False
    ghost_frequency = randint(10,20)
    ghost_time=time.time() #ghost start time
    ghost_x = randrange(0,display_width - ghost_width)
    ghost_y = 0 - ghost_width - randint(500,5000)
    
    angry_frequency = randint(10,20)
    angry_time=time.time() 
    angry_x = randrange(0,display_width - angry_width)
    angry_y = 0 - angry_width - randint(500,5000)
    angry_appearance_time = time.time()
    angry_appearance = False
    
    gift_frequency = randint(10,20)
    gift_time=time.time() 
    gift_x = randrange(0,display_width - gift_width)
    gift_y = 0 - gift_width - randint(500,5000)
    gift_appearance_time = time.time()
    gift_appearance = False
    
    bonus_visibility=False
    bonus_type=''
    bonus_time=0
    bonus_start_time=0
    bonus_max_time=0
    bonus_list={}
    all_bonuses=set()
    all_bonuses_text=''
    
    print("levelmode " + mode)
    print("level " + level)
    
    while not gameExit:
        while gameOver:
            message_center(state+', press C to play again or Q to quit', white)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        start=time.time()
                        gameLoop(level, mode)       
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -size_x/2
                if event.key == pygame.K_RIGHT:
                    lead_x_change = size_x/2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                    lead_x_change = 0
            
            #Add player movement with mouse/touchpad
            if event.type == pygame.MOUSEMOTION:
                lead_x = event.pos[0]-(size_x/2) #cursor in the middle of spaceship
        
        lead_x += lead_x_change

        if level=='easy':
            #A new fireball appears after every n seconds
            if time.time() -start_time > 2:
                start_time=time.time()
                drawing_by_level(blocks, fireball_width,fireball_height, 5, 20)
            
        elif level=='medium':
            #A new fireball appears after every 1 second
            if time.time() -start_time > 1:
                start_time=time.time()
                drawing_by_level(blocks, fireball_width,fireball_height, 10, 30)
               
        elif level=='hard':
            #A new fireball appears after every two seconds
            if time.time() -start_time > 0.5:
                start_time=time.time()
                drawing_by_level(blocks, fireball_width,fireball_height, 15, 40)

        #Make sure that player cannot move outside the edge of the screen
        if lead_x >= display_width - size_x:
            lead_x = display_width - size_x
            lead_x_change=0   
        if lead_x < 0:
            lead_x = 0
            lead_x_change = 0

        gameDisplay.blit(bg, (0,0))
        gameDisplay.blit(player, [lead_x,lead_y])
        
        #drawing every figure in blocks list (fireball info)
        for i in blocks:
            if faster_speed==True and slower_speed==True or slower_speed==False and faster_speed==False:
                i[1]+=i[4]
            elif faster_speed==True and slower_speed==False:
                i[1]=i[1]+i[4]*1.1
            elif slower_speed==True and faster_speed==False:
                i[1]=i[1]+i[4]/2          
                
            fireball_icon = pygame.transform.scale(fireball, (i[2], i[3]))
            gameDisplay.blit(fireball_icon, [i[0], i[1]])
            
            if i[1]>display_height:
                blocks.remove(i)
                block_count+=1
            #print(blocks)
               
            #collision
            if ghost_immunity == False:
                if lead_x>i[0] and lead_x<i[0]+i[2] or lead_x+size_x>i[0] and \
                lead_x+size_x<i[0]+i[2] or lead_x<i[0] and lead_x+size_x>i[0]+i[2]:
                    if lead_y>i[1] and lead_y<i[1]+i[3] or lead_y+size_y>i[1] and \
                    lead_y+size_y<i[1]+i[3]:
                        #print(numb)
                        #numb+=1
                        gameOver=True
        
        #-------------------plus-------------------------
        #plus appears after random amount of time
        if time.time() - plus_time > plus_frequency:
            plus_frequency = randint(10,20)
            plus_time=time.time()
            plus_x = randrange(0,display_width - plus_width)
            plus_y = 0 - plus_width
                
        gameDisplay.blit(plus, (plus_x,plus_y))
        plus_y += 10
        
        #Plus collision makes everything faster
        if lead_x>plus_x and lead_x<plus_x+plus_width or lead_x+size_x>plus_x and \
        lead_x+size_x<plus_x+plus_width or lead_x<plus_x and lead_x+size_x>plus_x+plus_width:
                if lead_y>plus_y and lead_y<plus_y+plus_height or lead_y+size_y>plus_y and \
                lead_y+size_y<plus_y+plus_height:
                    plus_immunity_time = time.time()
                    faster_speed = True
                    plus_y = display_height
                    bonus_visibility=True
                    bonus_list['Speed ++ ']=time.time()
                    bonus_max_time=5
        
        if faster_speed == True:  
            if time.time() - plus_immunity_time > 5:
                faster_speed = False
                del bonus_list['Speed ++ ']
                #Check if bonus_list dict is empty
                if not bonus_list:
                    bonus_visibility= False
        
        #-------------------minus-------------------------       
        #minus appears after random amount of time
        if time.time() - minus_time > minus_frequency:
            minus_frequency = randint(10,20)
            minus_time=time.time()
            minus_x = randrange(0,display_width - minus_width)
            minus_y = 0 - minus_width
                
        gameDisplay.blit(minus, (minus_x,minus_y))
        minus_y += 10
        
        #minus collision makes everything slower
        if lead_x>minus_x and lead_x<minus_x+minus_width or lead_x+size_x>minus_x and \
        lead_x+size_x<minus_x+minus_width or lead_x<minus_x and lead_x+size_x>minus_x+minus_width:
                if lead_y>minus_y and lead_y<minus_y+minus_height or lead_y+size_y>minus_y and \
                lead_y+size_y<minus_y+minus_height:
                    minus_immunity_time = time.time()
                    slower_speed = True
                    minus_y = display_height
                    bonus_visibility=True
                    bonus_list['Speed -- ']=time.time()
                    bonus_max_time=5
        
        if slower_speed == True:  
            if time.time() - minus_immunity_time > 5:
                slower_speed = False
                del bonus_list['Speed -- ']
                
                if not bonus_list:
                    bonus_visibility= False
        
        #if for making it not appear again if the ghost or plus or minus is already on the screen!!!
        
        #-------------------ghost-------------------------
        #ghost appears and offers immunity
        if time.time() - ghost_time > ghost_frequency:
            ghost_frequency = randint(10,20)
            ghost_time=time.time()
            ghost_x = randrange(0,display_width - ghost_width)
            ghost_y = 0 - ghost_width
        
        gameDisplay.blit(ghost, (ghost_x,ghost_y))
        ghost_y += 10
        
        #Ghost collision gives player immunity for five seconds
        if lead_x>ghost_x and lead_x<ghost_x+ghost_width or lead_x+size_x>ghost_x and \
        lead_x+size_x<ghost_x+ghost_width or lead_x<ghost_x and lead_x+size_x>ghost_x+ghost_width:
                if lead_y>ghost_y and lead_y<ghost_y+ghost_height or lead_y+size_y>ghost_y and \
                lead_y+size_y<ghost_y+ghost_height:
                    ghost_immunity = True
                    ghost_immunity_time = time.time()
                    ghost_y = display_height
                    bonus_visibility=True
                    bonus_list['Immunity: ']=time.time()
                    bonus_max_time=5
        
        if ghost_immunity == True:  
            if time.time() - ghost_immunity_time > 5:
                ghost_immunity = False
                del bonus_list['Immunity: ']
                
                if not bonus_list:
                    bonus_visibility= False
        
        #------------------------------------------------
                
        #now the bonus max time is the same for every bonus!!!
                
        if bonus_visibility==True:
            show_bonus(bonus_list, bonus_max_time)
            
            
        #If chosen mode is 'score', show two more bonuses    
        if mode == 'score':
            
            #-------------------angryface-------------------------
            if time.time() - angry_time > angry_frequency:
                angry_frequency = randint(10,20)
                angry_time=time.time()
                angry_x = randrange(0,display_width - angry_width)
                angry_y = 0 - angry_width
                
            gameDisplay.blit(angry, (angry_x, angry_y))
            angry_y += 10
            
            #Colliding with angry face decreases score points
            if lead_x>angry_x and lead_x<angry_x+angry_width or lead_x+size_x>angry_x and \
            lead_x+size_x<angry_x+angry_width or lead_x<angry_x and lead_x+size_x>angry_x+angry_width:
                if lead_y>angry_y and lead_y<angry_y+angry_height or lead_y+size_y>angry_y and \
                lead_y+size_y<angry_y+angry_height:
                    
                    angry_appearance = True
                    angry_appearance_time = time.time()
                    angry_y = display_height
                    block_count = block_count-5
                    
            if angry_appearance == True:
                message(display_width-200, display_height-580, 'Score: -5', white)
                
                if time.time() - angry_appearance_time > 3:
                    angry_appearance = False
                    
            #-------------------gift-------------------------   
            if time.time() - gift_time > gift_frequency:
                gift_frequency = randint(10,20)
                gift_time=time.time()
                gift_x = randrange(0,display_width - gift_width)
                gift_y = 0 - gift_width
                
            gameDisplay.blit(gift, (gift_x, gift_y))
            gift_y += 10
        
            #Gift increases score by 5 points
            if lead_x > gift_x and lead_x < gift_x + gift_width or lead_x+size_x > gift_x and \
            lead_x+size_x < gift_x+gift_width or lead_x < gift_x and lead_x+size_x > gift_x+gift_width:
                if lead_y>gift_y and lead_y<gift_y+gift_height or lead_y+size_y>gift_y and \
                lead_y+size_y<gift_y+gift_height:
                    
                    gift_appearance = True
                    gift_appearance_time = time.time()
                    gift_y = display_height
                    block_count = block_count+5
                    
            if gift_appearance == True:
                message(display_width-200, display_height-580, 'Score: +5', white)
                
                if time.time() - gift_appearance_time > 3:
                    gift_appearance = False
                    
        #Show score according to chosen mode
        if mode == 'score':
            score=show_score(block_count)
            state='Your score: '+str(score)
        elif mode == 'time':
            score=show_time(start)
            if score>30:
                state='You won'
                gameOver=True
        #print(bonus_list)
        
        pygame.display.update()
        clock.tick(FPS)
            
    pygame.quit()

gameIntro()
#gameLoop(level, mode)
