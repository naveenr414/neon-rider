import setup
import pygame
import inputControl
from geometry import intersect, Rectangle
import copy

#Create a font
pygame.font.init()
titleFont = pygame.font.SysFont('arial',40)

#Buttons
startButton = Rectangle(500,100,200,100)
galleryButton = Rectangle(500,250,200,100)
quitButton = Rectangle(500,400,200,100)
buttons = [(startButton,setup.green),(galleryButton,setup.yellow),(quitButton,setup.red)] 

#Number of players buttons
onePlayer = Rectangle(800, 100, 50, 50)
twoPlayers = Rectangle(800, 200, 50, 50)
threePlayers = Rectangle(800, 300, 50, 50)
fourPlayers = Rectangle(800,400,50,50)
numberPlayerRectangles = [onePlayer,twoPlayers,threePlayers,fourPlayers]
numberPlayers = []

#The texts
playersText = []
humanText = []
aiText = []

#The Buttons for AI/Human
humanAIRectangles = [[Rectangle(900, 100, 150, 50),Rectangle(1100, 100, 50, 50)],
			[Rectangle(900, 200, 150, 50),Rectangle(1100, 200, 50, 50)],
			[Rectangle(900, 300, 150, 50),Rectangle(1100, 300, 50, 50)],
			[Rectangle(900, 400, 150, 50),Rectangle(1100, 400, 50, 50)]]

#Text
textList = [['Welcome to NEON RIDER',setup.white,(370,20)],
            ['S T A R T',setup.black,(startButton.x+15,startButton.y+25)],
            ['GALLERY',setup.black,(galleryButton.x+2, galleryButton.y+25)],
            ['Q U I T',setup.black,(quitButton.x+35,quitButton.y+25)]]


for i, text in enumerate(textList):
    textList[i] = [titleFont.render(text[0],False,text[1]),text[2]]

#Create the boxes for the number of players
for i in range(setup.players):
    playersText.append((titleFont.render(str(i+1),False,setup.black),(numberPlayerRectangles[i].x+15,numberPlayerRectangles[i].y+4)))

    #We use green boxes for human players 
    if(setup.humanList[i]):
        numberPlayers.append([numberPlayerRectangles[i],setup.green])
    else:
        numberPlayers.append([numberPlayerRectangles[i],setup.red])

for i in range(setup.players):
    humanText.append((titleFont.render("Human",False,setup.black),(humanAIRectangles[i][0].x+12,humanAIRectangles[i][0].y+4)))
    aiText.append((titleFont.render("AI",False,setup.black),(humanAIRectangles[i][1].x+3,humanAIRectangles[i][1].y+4)))

def menuSetup(screen):
    for i in range(setup.maxPlayers):
        pygame.draw.rect(screen,numberPlayers[i][1],numberPlayers[i][0].getSize())

    for i in buttons:
        pygame.draw.rect(screen,i[1],i[0].getSize())

    for i in range(setup.maxPlayers):
        screen.blit(playersText[i][0],playersText[i][1])

    for i in textList:
        screen.blit(i[0],i[1])

    for i in range(setup.players):
        if(setup.humanList[i]):
            pygame.draw.rect(screen,setup.green,humanAIRectangles[i][0].getSize())
            pygame.draw.rect(screen,setup.red,humanAIRectangles[i][1].getSize())
        else:
            pygame.draw.rect(screen,setup.red,humanAIRectangles[i][0].getSize())
            pygame.draw.rect(screen,setup.green,humanAIRectangles[i][1].getSize())
            
        screen.blit(humanText[i][0],humanText[i][1])
        screen.blit(aiText[i][0],aiText[i][1])  


    #Draw the mouse
    pygame.draw.circle(screen,setup.white,pygame.mouse.get_pos(),10)

    
    if(inputControl.mouseDown):
        if(intersect(pygame.mouse.get_pos(),quitButton)):
            return -1
        if(intersect(pygame.mouse.get_pos(),startButton)):
            return 1
        if(intersect(pygame.mouse.get_pos(),galleryButton)):
            return 3
        for i in range(len(numberPlayerRectangles)):
            if(intersect(pygame.mouse.get_pos(),numberPlayerRectangles[i])):
                #Change the color, so that green background for current num players
                numberPlayers[setup.players-1][1] = setup.red
                setup.players = i+1
                numberPlayers[setup.players-1][1] = setup.green
        for i in range(0,setup.players):
            if(intersect(pygame.mouse.get_pos(),humanAIRectangles[i][0])):
                setup.humanList[i] = True
            if(intersect(pygame.mouse.get_pos(),humanAIRectangles[i][1])):
                setup.humanList[i] = False
               
    return 0
