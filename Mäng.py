import pygame

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

def message(msg,color):
    font= pygame.font.SysFont(None, 25)
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [display_width/2,display_height/2])

def gameLoop():
    gameExit = False
    gameOver = False

    lead_x = 300
    lead_y = 300
    lead_x_change = 0
    lead_y_change = 0
    size=20
    
    
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

        lead_x += lead_x_change
        if lead_x >= display_width-size or lead_x < 0+size:
            lead_x_change=0
            
        
        
        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, black, [lead_x,lead_y,size,size])
        pygame.display.update()
            
        clock.tick(15)
            
    pygame.quit()

gameLoop()