import pygame
pygame.init()

import gui
import setup
import inputControl
import game

WIDTH = setup.width
HEIGHT = setup.height

screen = pygame.display.set_mode((WIDTH,HEIGHT))
done = False

#Mouse setup
pygame.mouse.set_visible(False)

#Different Game Stages
Menu = 0
Game = 1
stage = Menu

#Current board, player state
state = 0

#Set fps
clock = pygame.time.Clock()
    
while not done:
    clock.tick(2)

    inputControl.keyTap = [False for i in range(0,300)]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if(event.type == pygame.MOUSEBUTTONDOWN):
            inputControl.mouseDown = True
    
        if(event.type == pygame.MOUSEBUTTONUP):
            inputControl.mouseDown = False

        if(event.type==pygame.KEYDOWN):
            if(event.key<300):
                inputControl.keys[event.key] = True

        if(event.type==pygame.KEYUP):
            if(event.key<300):
                if(inputControl.keys[event.key]):
                    inputControl.keyTap[event.key] = True
                inputControl.keys[event.key] = False
    
    screen.fill(setup.black)

    if stage == Menu:
        stage = gui.menuSetup(screen)
    elif stage == Game:
        if(state==0):
            #Create a new game state
            state = game.State()
            print(state.startFlag)
        stage = game.update(screen,state)
    
    if(stage!=Game):
        state = 0

    #If we've reached stage -1, quit
    done = done or stage==-1

    pygame.display.flip()
    pygame.display.update()

pygame.display.quit()
pygame.quit()
print("Done")
