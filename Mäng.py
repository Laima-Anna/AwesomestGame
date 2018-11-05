import pygame
import os
import time
from random import randrange
from random import randint

os.environ['SDL_VIDEO_CENTERED']='1'
pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Mäng')


clock = pygame.time.Clock()

#update specific area, if no parameters then all
#pygame.display.update()
#update all display at once
#pygame.display.flip()

flag=False
   

def message(msg,color):
    font= pygame.font.SysFont(None, 25)
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [display_width/2,display_height/2])

def gameLoop():
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height-50
    lead_x_change = 0
    lead_y_change = 0
    size=20
    
    start_time=time.time()
    numb=0
    blocks=[]
    
    
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
                    lead_x_change = -size
                if event.key == pygame.K_RIGHT:
                    lead_x_change = size
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                    lead_x_change = 0
            
            #Add player movement with mouse/touchpad
            if event.type == pygame.MOUSEMOTION:
                lead_x = event.pos[0]

        lead_x += lead_x_change
 
        #moment after 5 sec
        if time.time() -start_time > 2:
            start_time=time.time()
            
            s = randint(10,100)
            x=randrange(0,display_width-s)
            speed=randint(5,20)
            y=0-s
            blocks+=[[x,y,s,speed]]
            
            
        #random falling   
##        if block_y<display_height:
##            #block speed
##            block_y+=10
##        else:
##            block_y=0-block
##            block = randint(10,100)
##            block_x=randrange(0,display_width-block)

        
        #Make sure that player cannot move outside the edge of the screen
        if lead_x >= display_width-size:
            lead_x = display_width - size
            lead_x_change=0   
        if lead_x < 0+size:
            lead_x = 0
            lead_x_change = 0

            
        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, black, [lead_x,lead_y,size,size])
        #pygame.draw.rect(gameDisplay, red, [block_x,block_y,block,block])
        for i in blocks:
            i[1]+=i[3]
            pygame.draw.rect(gameDisplay, red, [i[0],i[1],i[2],i[2]])
            if i[1]>display_height:
                blocks.remove(i)
            print(blocks)
        
            if lead_x>i[0] and lead_x<i[0]+i[2] or lead_x+size>i[0] and lead_x+size<i[0]+i[2]:
                if lead_y>i[1] and lead_y<i[1]+i[2] or lead_y+size>i[1] and lead_y+size<i[1]+i[2]:
                    print(numb)
                    numb+=1
                    #gameOver=True
                
                
        pygame.display.update()
        
        #collision
##        if lead_x>block_x and lead_x<block_x+block or lead_x+size>block_x and lead_x+size<block_x+block:
##            if lead_y>block_y and lead_y<block_y+block or lead_y+size>block_y and lead_y+size<block_y+block:
##                print(i)
##                i+=1
##                #gameOver=True
        
        

        
            
        
        clock.tick(30)
            
    pygame.quit()

gameLoop()
