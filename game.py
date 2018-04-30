import setup
from geometry import Rectangle, Vector, Line, dot, colinear
import geometry
import copy
import pygame
import inputControl
import time
from gui import Text
from player import *
import font
import ai

startText = []

for i in range(0,4):
    x = setup.gameWidth//2
    y = setup.height//2
    if(i==0):
        startText.append((font.largeFont.render("GO!",False,setup.white),(x,y)))
    else:
        startText.append((font.largeFont.render(str(i),False,setup.white),(x,y)))

x = 5*setup.width//6
hudText = []
playerText = []
statusText = []

for i in range(-1,setup.players):
    y = setup.height//10+font.smallFont.get_height()*(i+1)

    if(i==-1):
        hudText.append(Text("Status:",(x,y),setup.white,f=font.smallFont))
    else:
        text = "Player "+str(i+1)+": "
        playerText.append(Text(text,(x,y),setup.colors[i],f=font.smallFont))
        
        statusText.append(Text("Not Ready",(x+font.smallFont.size(text)[0],y),
                              setup.red,f=font.smallFont))


scoresText = []
for i in range(-1,setup.players):
    temp = []
    y = setup.height//3+font.smallFont.get_height()*(i+1)

    if(i==-1):
        hudText.append(Text("Scores:",(x,y),setup.white,f=font.smallFont))
    else:
        text = "Player "+str(i+1)+ ": "
        temp.append(Text("Player "+str(i+1)+": ",(x,y),
                         setup.colors[i],f=font.smallFont))
        temp.append(Text(str(setup.scores[i]),(x+font.smallFont.size(text)[0],y),
                         setup.white,f=font.smallFont))
        scoresText.append(temp)


controlText = []
for i in range(-1,setup.players):
    y = 3*setup.height//5+font.smallFont.get_height()*(i+1)
    if(i==-1):
        hudText.append(Text("Controls:",(x,y),setup.white,f=font.smallFont))
    else:
        controlText.append(Text("Player "+str(i+1)+": "+playerKeys[i],(x,y),setup.colors[i],f=font.smallFont))

class State:
    def __init__(self):
        self.players = []
        for i in range(0,setup.players):
            self.players.append(copy.deepcopy(initialPlayers[i]))
        self.board = []
        self.startFlag = 3
        self.deathResults = []
        self.ready = [False]*setup.players
        self.statusText = []
        self.time = 0

        #GUI Things
        self.controlText = []
        self.scoresText = []
        self.hudText = []
        self.playerText = []
        self.statusText = []

def killPlayer(state,i,j):
    yPos = len(state.deathResults)*40/3 + 20
    state.players[i].alive = False
    if(i!=j):
        state.statusText[i].surface = font.smallFont.render("Killed by Player "+str(j+1),False,setup.colors[j])
    else:
        state.statusText[i].surface = font.smallFont.render("Killed Themself",False,setup.white)
    state.deathResults.append(Death(i,j,state.time,state.players[i].pos))

def drawHud(screen,state):
    x = 5*setup.width//6-10
    pygame.draw.line(screen,setup.white,(x,0),(x,setup.height))

    for i in hudText:
        screen.blit(i.surface,i.pos)

    for i in range(setup.players):
        screen.blit(playerText[i].surface,playerText[i].pos)
        screen.blit(statusText[i].surface,statusText[i].pos)

    for i in scoresText[:setup.players]:
        for button in i:
            screen.blit(button.surface,button.pos)

    for i in controlText[:setup.players]:
        screen.blit(i.surface,i.pos)

def processInput(screen,state):
    #Get key input
    for j in range(setup.players):
        if(state.players[j].alive and setup.humanList[j]):
            for i in range(0,len(keyDirections[0])):
                if(inputControl.keyTap[keyDirections[j][i]] and dot(keyVectors[i],state.players[j].direction)==0):
                    state.players[j].direction = keyVectors[i]

    #If a player presses space, kill off someone
    if(inputControl.keyTap[pygame.K_SPACE]):
        for j in range(setup.players):
            if(state.players[j].alive):
                    killPlayer(state,j,j)
                    break

def pregame(screen,state):
    if(False not in state.ready):
        screen.blit(startText[state.startFlag][0],startText[state.startFlag][1])
        state.startFlag-=1
        
        if(state.startFlag!=2):
            time.sleep(1)
            
    for j in range(setup.players):
        if(state.players[j].alive):
            for i in range(0,len(keyDirections[0])):
                if(inputControl.keys[keyDirections[j][i]]):
                    if(state.startFlag>0):
                        state.ready[j] = True
                        statusText[j].surface = font.smallFont.render("Ready",False,setup.green)


def update(screen,state):
    drawHud(screen,state)
    state.statusText = statusText
    
    if(state.startFlag>-1):
        pregame(screen,state)
        return 1

    processInput(screen,state)
 
    #Update the players
    for i in range(setup.players):
        currentPlayer = state.players[i]
        if(currentPlayer.alive):
            #Update the players positions
            for j in range(1,currentPlayer.speed+1):
                newPos = currentPlayer.pos+currentPlayer.direction*j
                #Check if they were killed by going outside the box, or by another player
                if(newPos.x<0 or newPos.x>setup.gameWidth//setup.blockSize
                or newPos.y<0 or newPos.y>setup.height//setup.blockSize):
                    killPlayer(state,i,i)
                else:
                    for r in range(setup.players):
                        for line in state.players[r].lines:
                            end = line.direction*line.length+line.start
                            if(colinear(newPos,line.start,end)
                               and min(line.start.x,end.x)<=newPos.x<=max(line.start.x,end.x)
                               and max(line.start.y,end.y)<=newPos.y<=max(line.start.y,end.y)):
                                killPlayer(state,i,r)

            if(len(currentPlayer.lines)==0
               or currentPlayer.lines[-1].direction!=currentPlayer.direction):
                l = Line(currentPlayer.pos,currentPlayer.direction,currentPlayer.speed)
                currentPlayer.lines.append(l)
            else:
                currentPlayer.lines[-1].length+=currentPlayer.speed
            
            currentPlayer.pos+=currentPlayer.direction*currentPlayer.speed

    #Draw the board
    for i in range(setup.players):
        currentPlayer = state.players[i]
        for j in currentPlayer.lines:
            end = j.start+j.direction*j.length
            left = min(j.start.x,end.x)
            top = min(j.start.y,end.y)  
            width = max(abs(end.x-j.start.x)*setup.blockSize,setup.blockSize)
            height = max(abs(end.y-j.start.y)*setup.blockSize,setup.blockSize)
                        
            r = pygame.Rect(left*setup.blockSize,top*setup.blockSize,width,height)
            pygame.draw.rect(screen,currentPlayer.color,r)

    for i in range(setup.players):
        if(state.players[i].alive and not(setup.humanList[i])):
            ai.minMax(state,i)


    state.time+=1

    #Check if any players are alive, if not, exit
    for i in range(0,setup.players):
        if(state.players[i].alive):
            break
    else:
        return 0
    return 1
