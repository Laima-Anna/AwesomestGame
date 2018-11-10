import pygame
import os
import time
from random import randrange
from random import randint

#Always displays game screen in the middle of the computer screen
os.environ['SDL_VIDEO_CENTERED']='1'
pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
grey = (220,220,220)

FPS = 30

display_width = 800
display_height = 600

bg = pygame.image.load("space.jpg")
gameDisplay = pygame.display.set_mode((display_width,display_height))
player = pygame.image.load("spaceship.png").convert_alpha()

#Our player width and height
size_x = int(player.get_size()[0]/10)
size_y = int(player.get_size()[1]/10)
player = pygame.transform.scale(player, (size_x, size_y))

pygame.display.set_caption('Mäng')

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 25)

#Variables for displaying text in center of screen
center_x = display_width/2
center_y = display_height/2

#Two functions for displaying text on screen
def textObjects(text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message(msg, color, y_displace=0, center_x=center_x, center_y=center_y):
    textSurf, textRect = textObjects(msg, color)
    textRect.center = (center_x), (center_y)+y_displace
    gameDisplay.blit(textSurf, textRect)

#Start screen
def gameIntro():
    intro = True
    
    #Button dimensions
    button_x = 100
    button_y = 50
    button_loc_y = display_height/2+100
    mediumButton_x = display_width/2-button_x/2
    easyButton_x = mediumButton_x-200
    hardButton_x = mediumButton_x+200
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    intro = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                if (easyButton_x < mouse_x < easyButton_x + button_x) and (button_loc_y < mouse_y < button_loc_y + button_y):
                    intro = False
        
        gameDisplay.fill(white)

        message("Mängu eesmärgiks on hoida oma kosmoselaev tervena.", red, -100)
        message("""Palun vajuta klahvi "e", et mängu alustada või vali tase.""", black)
        
        easyButton = pygame.draw.rect(gameDisplay, grey,
                                      (easyButton_x,button_loc_y, button_x, button_y))
        mediumButton = pygame.draw.rect(gameDisplay, grey,
                                        (mediumButton_x,button_loc_y, button_x, button_y))
        hardButton = pygame.draw.rect(gameDisplay, grey,
                                      (hardButton_x,button_loc_y, button_x, button_y))
        
        message("Lihtne", black, 0, easyButton_x+button_x/2, button_loc_y+button_y/2)
        message("Keskmine", black, 0, mediumButton_x+button_x/2, button_loc_y+button_y/2)
        message("Raske", black, 0, hardButton_x+button_x/2, button_loc_y+button_y/2)
        
        pygame.display.update()
        clock.tick(FPS)
    
def gameLoop():
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height-50
    lead_x_change = 0
    lead_y_change = 0  
    
    start_time=time.time()
    numb=0
    blocks=[]
    
    fireball = pygame.image.load("fireball.png").convert_alpha()
    fireball_width = fireball.get_size()[0]
    fireball_height = fireball.get_size()[1]
    
    while not gameExit:
        while gameOver:
            gameDisplay.fill(white)
            message('Game over, press C to play again or Q to quit', red)
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
                        gameLoop()
            
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
 
        #A new fireball appears after every two seconds
        if time.time() -start_time > 2:
            start_time=time.time()
            #make fireball dimensions correct
            s = randint(5, 25)
            fireball_x = int(fireball_width/s)
            fireball_y = int(fireball_height/s)
            x=randrange(0,display_width - fireball_x)
            speed=randint(5,20)
            y=0-fireball_y
            blocks+=[[x,y, fireball_x, fireball_y,speed]]
             
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
            i[1]+=i[4]  #x + speed
            fireball_icon = pygame.transform.scale(fireball, (i[2], i[3]))
            gameDisplay.blit(fireball_icon, [i[0], i[1]])
            
            if i[1]>display_height:
                blocks.remove(i)
            print(blocks)
            
            #collision
            if lead_x>i[0] and lead_x<i[0]+i[2] or lead_x+size_x>i[0] and lead_x+size_x<i[0]+i[2] or lead_x<i[0] and lead_x+size_x>i[0]+i[2]:
                if lead_y>i[1] and lead_y<i[1]+i[2] or lead_y+size_y>i[1] and lead_y+size_y<i[1]+i[2]:
                    #print(numb)
                    #numb+=1
                    gameOver=True
                
        pygame.display.update()
        clock.tick(FPS)
            
    pygame.quit()
    
gameIntro()
gameLoop()
