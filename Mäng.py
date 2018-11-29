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
grey = (220, 220, 220)
darkgrey = (119,136,153)

display_width = 800
display_height = 600

bg = pygame.image.load("space.jpg") #background picture
gameDisplay = pygame.display.set_mode((display_width,display_height))
helpDisplay = pygame.display.set_mode((display_width,display_height))

#function for loading and resizing pictures
def picture_resize(image_name, divider):
    picture = pygame.image.load(image_name).convert_alpha()
    width = int(picture.get_size()[0]/divider)
    height = int(picture.get_size()[1]/divider)
    pic_icon = pygame.transform.scale(picture, (width, height))
    
    return pic_icon, width, height

#load all necessary pictures and picture variables
player, size_x, size_y = picture_resize("spaceship.png", 10)
angry, angry_width, angry_height = picture_resize("angryface.png", 1.5)
minus, minus_width, minus_height = picture_resize("minus.png", 1.5)
plus, plus_width, plus_height = picture_resize("plus.png", 1.5)
gift, gift_width, gift_height = picture_resize("gift.png", 12.6)
ghost, ghost_width, ghost_height = picture_resize("ghost.png", 7)

pygame.display.set_caption('Mäng') #title of the screen

clock = pygame.time.Clock() #necessary for slowing down the game
FPS = 30

font = pygame.font.SysFont(None, 40) #general variable for font (size 40)

#Variables for displaying text in center of screen
center_x = display_width/2
center_y = display_height/2

#draws fireballs according to chosen level (different speed etc)
def drawing_by_level(blocks, fireball_width,fireball_height, speed_min, speed_max):
    s = randint(5, 25)
    fireball_x = int(fireball_width/s)
    fireball_y = int(fireball_height/s)
    x=randrange(0,display_width - fireball_x)
    speed=randint(speed_min,speed_max)
    y=0-fireball_y
    blocks+=[[x,y, fireball_x, fireball_y,speed]]
    return blocks

#when mode is 'time', shows elapsed time in the upper right corner
def show_time(start):
    new_time=time.time()-start
    text=str(round(new_time))
    text_width, text_height = font.size(text)
    message(display_width-text_width-20, 20, text, white)
    return new_time

#when mode is 'score', shows score in the corner (score increases when you dodge a fireball successfully)
def show_score(count):
    text=str(count)
    text_width, text_height = font.size(text)
    message(display_width-text_width-20, 20, text, white)
    return count

#If you get a bonus, shows what bonus and how much time you have left in the corner
def show_bonus(bonus_list,bonus_max_time):
    text=''
    for j in bonus_list:
        if j == 'Score: -' or j == 'Score: +':
            text=text+' '+j+' '+str(5)
        else:
            text=text+' '+j+' '+str(bonus_max_time-round(time.time()-bonus_list[j]))
    message(20,20,text,white)

#general function for displaying text
def message(x,y,tekst,color):
    textsurface = font.render(tekst, True, color)
    gameDisplay.blit(textsurface,(x,y))

#Two functions for displaying text in center of screen
def textObjects (text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
def message_center(msg, color, y_displace=0, center_x=center_x, center_y=center_y,a=1):
    textSurf, textRect = textObjects(msg, color)
    textRect.center = (center_x), (center_y)+y_displace
    gameDisplay.blit(textSurf, textRect)
    
#function for drawing buttons with text in the center
def button(text, color, x, y, width, height):
    pygame.draw.rect(gameDisplay, color, (x, y, width, height))
    message_center(text, black, 0, x+width/2, y+height/2)
    
#Start screen
def gameIntro():
    intro = True
    level = ''
    mode = 'time' #chosen by default
    
    #different variables for different buttons
    button_x = 140
    button_y = 50
    
    loc_y = display_height/2+200
    mediumButton_x = display_width/2-button_x/2
    easyButton_x = mediumButton_x-200
    hardButton_x = mediumButton_x+200
    
    help_x = display_width-button_x-50
    help_y = display_height-550
    quit_x = display_width-750
    quit_y = display_height-550
    
    timeMode_x = display_width/2 -200
    scoreMode_x = display_width/2 + 50
    modeButton_y = display_height/2
    
    #default colors for 'Time' and 'Score' buttons
    scorecolor = grey
    timecolor = darkgrey
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                
                #when one of the mode buttons is clicked, it changes color + mode is chosen
                if (timeMode_x < mouse_x < timeMode_x+button_x) and  (modeButton_y < mouse_y < modeButton_y + button_y):
                    timecolor = darkgrey
                    scorecolor = grey
                    mode = 'time'
                    
                if (scoreMode_x < mouse_x < scoreMode_x+button_x) and (modeButton_y < mouse_y < modeButton_y + button_y):
                    timecolor = grey
                    scorecolor = darkgrey
                    mode = 'score'
                    
                #Choose which level you want to play     
                if (easyButton_x < mouse_x < easyButton_x + button_x) and (loc_y < mouse_y < loc_y + button_y):
                    level = 'easy'
                    intro = False
                if (mediumButton_x < mouse_x < mediumButton_x + button_x) and (loc_y < mouse_y < loc_y + button_y):
                    level = 'medium'
                    intro = False
                if (hardButton_x < mouse_x < hardButton_x + button_x) and (loc_y < mouse_y < loc_y + button_y):
                    level = 'hard'
                    intro = False
                       
                #What happens when you click Help button
                if (help_x < mouse_x < help_x + button_x) and (help_y < mouse_y < help_y + button_y):
                    helpScreen()
                    intro = False
                    
                if (quit_x < mouse_x < quit_x + button_x) and (quit_y < mouse_y < quit_y + button_y):
                    pygame.quit()
                    
        gameDisplay.blit(bg, (0,0))

        message_center("The aim of the game is to avoid fireballs", white, -100)
        message_center("Choose your game mode", white, -50)

        button("Time", timecolor, timeMode_x, modeButton_y, button_x, button_y)
        button("Score", scorecolor, scoreMode_x, modeButton_y, button_x, button_y)
        
        message_center("Choose your level", white, +150)
        
        button("Easy", grey, easyButton_x, loc_y, button_x, button_y)
        button("Medium", grey, mediumButton_x, loc_y, button_x, button_y)
        button("Hard", grey, hardButton_x, loc_y, button_x, button_y)
        
        button("Help", grey, help_x, help_y, button_x, button_y)
        button("Quit", grey, quit_x, quit_y, button_x, button_y)
        
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
        message(x, y*3, "You can play each level for 30 sec or collect as many", white)
        message(x, y*4-10, "points as possible on each level.", white)
        message(x*2, y*5, "There are some bonuses which you can collect:", white)
        
        helpDisplay.blit(angry, (x, y*6-4))
        message(x*2, y*6, "Makes the speed of fireballs faster for 5 seconds", white)
        
        helpDisplay.blit(gift, (x, y*7-4))
        message(x*2, y*7, "Makes the speed of fireballs slower for 5 seconds", white)
        
        helpDisplay.blit(ghost, (x, y*8-3))
        message(x*2, y*8, "Gives you immunity from fireballs for 5 seconds", white)
        
        message(x*2, y*9, "Score mode has two extra bonuses: ", white)
        
        helpDisplay.blit(plus, (x, y*10-4))
        message(x*2, y*10, "Adds 5 points to your score", white)
        
        helpDisplay.blit(minus, (x, y*11-4))
        message(x*2, y*11, "Takes off 5 points from your score", white)
        
        
        pygame.display.update()
    
        clock.tick(FPS)
    
    gameIntro()
    
def gameLoop(level, mode):
    gameExit = False
    gameOver = False
    won = False

    lead_x = display_width/2
    lead_y = display_height-50
    lead_x_change = 0
    
    start_time=time.time()
    state='Game Over'
    start=time.time()
    blocks=[]
    block_count = 0
    
    fireball, fireball_width, fireball_height = picture_resize("fireball.png", 1)

    plus_frequency = randint(10,20)
    plus_time=time.time() #plus start time
    plus_x = randrange(0,display_width - plus_width)
    plus_y = 0 - plus_width - randint(500,5000)
    plus_immunity_time = time.time()
    plus_appearance = False

    minus_frequency = randint(10,20)
    minus_time=time.time() #minus start time
    minus_x = randrange(0,display_width - minus_width)
    minus_y = 0 - minus_width - randint(500,5000)
    minus_immunity_time = time.time()
    minus_appearance = False
    
    #variable for how long immunity lasts
    ghost_frequency = randint(10,20)
    ghost_time=time.time() #ghost start time
    ghost_x = randrange(0,display_width - ghost_width)
    ghost_y = 0 - ghost_width - randint(500,5000)
    ghost_immunity_time = time.time()
    ghost_immunity = False
    
    angry_frequency = randint(10,20)
    angry_time=time.time() 
    angry_x = randrange(0,display_width - angry_width)
    angry_y = 0 - angry_width - randint(500,5000)
    angry_immunity_time = time.time()
    faster_speed= False
    
    gift_frequency = randint(10,20)
    gift_time=time.time() 
    gift_x = randrange(0,display_width - gift_width)
    gift_y = 0 - gift_width - randint(500,5000)
    gift_immunity_time = time.time()
    slower_speed= False
    
    bonus_visibility=False
    bonus_max_time=5
    bonus_list={}

    while not gameExit:
        while gameOver:
            message_center(state+', press C to play again or Q to go back', white)
            if won == True:
                message_center('Press L to go to next level', white, 100)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameIntro()
                    if event.key == pygame.K_c:
                        gameLoop(level, mode)
                    if event.key == pygame.K_l:
                        if won == True: 
                            if level == 'easy':
                                level = 'medium'
                                won = False
                                gameLoop(level, mode)
                            elif level == 'medium':
                                level = 'hard'
                                won = False
                                gameLoop(level, mode)
                            elif level == 'hard':
                                level = 'ultra-hard'
                                won = False
                                gameLoop(level, mode)
                            elif level == 'ultra-hard':
                                message_center('You already played the hardest level!', white, 150)
                    
                        
                        
                        
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -size_x/2
                if event.key == pygame.K_RIGHT:
                    lead_x_change = size_x/2
                
                #if event.key == pygame.K_SPACE:
##                    print('aa')
##                    while True:
##                        n = input('')
##                        if n==' ':
##                            break
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
                
        elif level=='ultra-hard':
            #A new fireball appears after every two seconds
            if time.time() -start_time > 0.3:
                start_time=time.time()
                drawing_by_level(blocks, fireball_width,fireball_height, 30, 50)

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
                i[1]=i[1]+i[4]*1.5
            elif slower_speed==True and faster_speed==False:
                i[1]=i[1]+i[4]/2        
                
            fireball_icon = pygame.transform.scale(fireball, (i[2], i[3]))
            gameDisplay.blit(fireball_icon, [i[0], i[1]])
            
            if i[1]>display_height:
                blocks.remove(i)
                block_count+=1
               
            #collision
            if ghost_immunity == False:
                if lead_x>i[0] and lead_x<i[0]+i[2] or lead_x+size_x>i[0] and \
                lead_x+size_x<i[0]+i[2] or lead_x<i[0] and lead_x+size_x>i[0]+i[2]:
                    if lead_y>i[1] and lead_y<i[1]+i[3] or lead_y+size_y>i[1] and \
                    lead_y+size_y<i[1]+i[3]:
                        gameOver=True
        
        #-------------------angry-------------------------
        #angry appears after random amount of time
        if time.time() - angry_time > angry_frequency:
            if angry_y < 0 or angry_y > display_height: # checks whether angry is on the screen already or not
                angry_frequency = randint(10,20)
                angry_time=time.time()
                angry_x = randrange(0,display_width - angry_width)
                angry_y = 0 - angry_width
                
        gameDisplay.blit(angry, (angry_x,angry_y))
        angry_y += 10
        
        #angry collision makes everything faster
        if lead_x>angry_x and lead_x<angry_x+angry_width or lead_x+size_x>angry_x and \
        lead_x+size_x<angry_x+angry_width or lead_x<angry_x and lead_x+size_x>angry_x+angry_width:
                if lead_y>angry_y and lead_y<angry_y+angry_height or lead_y+size_y>angry_y and \
                lead_y+size_y<angry_y+angry_height:
                    angry_immunity_time = time.time()
                    faster_speed = True
                    angry_y = display_height
                    bonus_visibility=True
                    bonus_list['Speed ++ ']=time.time()     
        
        if faster_speed == True:  
            if time.time() - angry_immunity_time > 5:
                faster_speed = False
                del bonus_list['Speed ++ ']
                #Check if bonus_list dict is empty
                if not bonus_list:
                    bonus_visibility= False
        
        #-------------------gift-------------------------       
        #gift appears after random amount of time
        if time.time() - gift_time > gift_frequency:
            if gift_y < 0 or gift_y > display_height: # checks whether gift is on the screen already or not
                gift_frequency = randint(10,20)
                gift_time=time.time()
                gift_x = randrange(0,display_width - gift_width)
                gift_y = 0 - gift_width
                
        gameDisplay.blit(gift, (gift_x,gift_y))
        gift_y += 10
        
        #gift collision makes everything slower
        if lead_x>gift_x and lead_x<gift_x+gift_width or lead_x+size_x>gift_x and \
        lead_x+size_x<gift_x+gift_width or lead_x<gift_x and lead_x+size_x>gift_x+gift_width:
                if lead_y>gift_y and lead_y<gift_y+gift_height or lead_y+size_y>gift_y and \
                lead_y+size_y<gift_y+gift_height:
                    gift_immunity_time = time.time()
                    slower_speed = True
                    gift_y = display_height
                    bonus_visibility=True
                    bonus_list['Speed -- ']=time.time()
                    
        if slower_speed == True:  
            if time.time() - gift_immunity_time > 5:
                slower_speed = False
                del bonus_list['Speed -- ']
                if not bonus_list:
                    bonus_visibility= False
        
        #-------------------ghost-------------------------
        #ghost appears and offers immunity
        if time.time() - ghost_time > ghost_frequency:
            if ghost_y < 0 or ghost_y > display_height: # checks whether ghost is on the screen already or not
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
        
        if ghost_immunity == True:  
            if time.time() - ghost_immunity_time > 5:
                ghost_immunity = False
                del bonus_list['Immunity: ']
                
                if not bonus_list:
                    bonus_visibility= False
                           
        if bonus_visibility==True:
            show_bonus(bonus_list, bonus_max_time)
               
        #If chosen mode is 'score', show two more bonuses    
        if mode == 'score':
            
            #-------------------minus-------------------------
            if time.time() - minus_time > minus_frequency:
                if minus_y < 0 or minus_y > display_height: # checks whether minus is on the screen already or not
                    minus_frequency = randint(10,20)
                    minus_time=time.time()
                    minus_x = randrange(0,display_width - minus_width)
                    minus_y = 0 - minus_width
                
            gameDisplay.blit(minus, (minus_x, minus_y))
            minus_y += 10
            
            #Colliding with minus face decreases score points
            if lead_x>minus_x and lead_x<minus_x+minus_width or lead_x+size_x>minus_x and \
            lead_x+size_x<minus_x+minus_width or lead_x<minus_x and lead_x+size_x>minus_x+minus_width:
                if lead_y>minus_y and lead_y<minus_y+minus_height or lead_y+size_y>minus_y and \
                lead_y+size_y<minus_y+minus_height:
                    minus_appearance = True
                    minus_immunity_time = time.time()
                    minus_y = display_height
                    block_count = block_count-5
                    bonus_list['Score: -'] = 5
                    bonus_visibility = True
            
            if minus_appearance == True:
                if time.time() - minus_immunity_time > 3:
                    minus_appearance = False
                    del bonus_list['Score: -']
                    if not bonus_list:
                        bonus_visibility=False
                    
            #-------------------plus-------------------------   
            if time.time() - plus_time > plus_frequency:
                if plus_y < 0 or plus_y > display_height: # checks whether plus is on the screen already or not
                    plus_frequency = randint(10,20)
                    plus_time=time.time()
                    plus_x = randrange(0,display_width - plus_width)
                    plus_y = 0 - plus_width
                
            gameDisplay.blit(plus, (plus_x, plus_y))
            plus_y += 10
        
            #plus increases score by 5 points
            if lead_x > plus_x and lead_x < plus_x + plus_width or lead_x+size_x > plus_x and \
            lead_x+size_x < plus_x+plus_width or lead_x < plus_x and lead_x+size_x > plus_x+plus_width:
                if lead_y>plus_y and lead_y<plus_y+plus_height or lead_y+size_y>plus_y and \
                lead_y+size_y<plus_y+plus_height:
                    plus_appearance = True
                    plus_immunity_time = time.time()
                    plus_y = display_height
                    block_count = block_count+5
                    bonus_list['Score: +'] = 5
                    bonus_visibility = True
                    
            if plus_appearance == True:
                if time.time() - plus_immunity_time > 3:
                    plus_appearance = False
                    del bonus_list['Score: +']
                    if not bonus_list:
                        bonus_visibility=False
                    
        #Show score according to chosen mode
        if mode == 'score':
            score=show_score(block_count)
            state='Your score: '+str(score)
        elif mode == 'time':
            score=show_time(start)
            if score>30:
                state='You won'
                gameOver=True
                won = True
        
        pygame.display.update()
        clock.tick(FPS)
            
    pygame.quit()

gameIntro()
