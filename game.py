import setup
from geometry import Rectangle, Vector, dot
import geometry
import copy
import pygame
import inputControl
import time
from gui import Text

class Player:
    def __init__(self,pos,color,direction,number,isHuman):
        self.speed = 10
        self.pos = pos
        self.color = color
        self.direction = direction
        self.number = number
        self.isHuman = isHuman
        self.alive = True

initialPlayers = [
Player(Vector(120, 120), setup.blue, geometry.right, 1, True),
Player(Vector(900, 420), setup.green, geometry.left, 3, False),
Player(Vector(900, 120), setup.red, geometry.down, 2, False),
Player(Vector(120, 420), setup.yellow, geometry.up, 4, False),
    ]

keyDirections = [[pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d],
                 [pygame.K_UP,pygame.K_LEFT,pygame.K_DOWN,pygame.K_RIGHT],
                 [pygame.K_y,pygame.K_g,pygame.K_h,pygame.K_j],
                 [pygame.K_p,pygame.K_l,pygame.K_SEMICOLON,pygame.K_QUOTE]]
keyVectors = [Vector(0,-1),Vector(-1,0),Vector(0,1),Vector(1,0)]

playerKeys = ["W, A, S, D", "Arrow Keys", "Y, G, H, J", "P, L, ;, '"]
playerTexts = []

textFont = pygame.font.SysFont('arial',25)
smallFont = pygame.font.SysFont('Comic Sans MS',15)
smallFont.set_bold(True)
textList = []

for i in range(0,4):
    if(i==0):
        textList.append((textFont.render("GO!",False,setup.white),(setup.width//2,setup.height//2)))
    else:
        textList.append((textFont.render(str(i),False,setup.white),(setup.width//2,setup.height//2)))

x = 5*setup.width//6
hudText = []
playerText = []
statusText = []

for i in range(-1,setup.players):
    y = setup.height//10+smallFont.get_height()*(i+1)

    if(i==-1):
        hudText.append(Text("Status:",(x,y),setup.white,f=smallFont))
    else:
        text = "Player "+str(i+1)+": "
        playerText.append(Text(text,(x,y),setup.colors[i],f=smallFont))
        
        statusText.append(Text("Not Ready",(x+smallFont.size(text)[0],y),
                              setup.red,f=smallFont))


scoresText = []
for i in range(-1,setup.players):
    temp = []
    y = setup.height//3+smallFont.get_height()*(i+1)

    if(i==-1):
        hudText.append(Text("Scores:",(x,y),setup.white,f=smallFont))
    else:
        text = "Player "+str(i+1)+ ": "
        temp.append(Text("Player "+str(i+1)+": ",(x,y),
                         setup.colors[i],f=smallFont))
        temp.append(Text(str(setup.scores[i]),(x+smallFont.size(text)[0],y),
                         setup.white,f=smallFont))
        scoresText.append(temp)


controlText = []
for i in range(-1,setup.players):
    y = 3*setup.height//5+smallFont.get_height()*(i+1)
    if(i==-1):
        hudText.append(Text("Controls:",(x,y),setup.white,f=smallFont))
    else:
        controlText.append(Text("Player "+str(i+1)+": "+playerKeys[i],(x,y),setup.colors[i],f=smallFont))

class State:
    def __init__(self):
        self.players = []
        for i in range(0,setup.players):
            self.players.append(copy.copy(initialPlayers[i]))
        self.board = []
        self.startFlag = 3
        self.deathResults = []
        self.ready = [False]*setup.players
        self.statusText = []

def killPlayer(state,i,j):
    yPos = len(state.deathResults)*40/3 + 20
    state.players[i].alive = False
    if(i!=j):
        state.statusText[i].surface = smallFont.render("Killed by Player "+str(j+1),False,setup.colors[j])
    else:
        state.statusText[i].surface = smallFont.render("Killed Themself",False,setup.white)
    state.deathResults.append((i,j))

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

def update(screen,state):
    drawHud(screen,state)
    state.statusText = statusText
    
    if(state.startFlag>-1):

        if(False not in state.ready):
            screen.blit(textList[state.startFlag][0],textList[state.startFlag][1])
            state.startFlag-=1
            
            if(state.startFlag!=2):
                time.sleep(1)
                
        for j in range(setup.players):
            if(state.players[j].alive and setup.humanList[j]):
                for i in range(0,len(keyDirections[0])):
                    if(inputControl.keys[keyDirections[j][i]]):
                        if(state.startFlag>0):
                            state.ready[j] = True
                            statusText[j].surface = smallFont.render("Ready",False,setup.green)

        return 1
        
    #Update the players
    for i in range(setup.players):
        currentPlayer = state.players[i]
        if(currentPlayer.alive):
            #Update the players positions
            for j in range(1,currentPlayer.speed+1):
                newPos = currentPlayer.pos+currentPlayer.direction*j
                if(newPos.x<0 or newPos.x>setup.gameWidth
                or newPos.y<0 or newPos.y>setup.height
                or newPos in [x[0] for x in state.board]):
                    currentPlayer.alive = False

                    #Check if they were killed by going outside the box, or by another player
                    if(newPos.x<0 or newPos.x>setup.gameWidth
                    or newPos.y<0 or newPos.y>setup.height):
                        killPlayer(state,i,i)
                    else:
                        for loc in state.board:
                            if(loc[0]==newPos):
                                killPlayer(state,i,loc[1])
                    break

                
                else:
                    #Add the tuple (position,player number) to the board
                    state.board.append([newPos,i])
            currentPlayer.pos+=currentPlayer.direction*currentPlayer.speed

    #Draw the board
    for i in range(0,len(state.board)):
        pygame.draw.rect(screen,state.players[state.board[i][1]].color,(state.board[i][0].x,
                                                   state.board[i][0].y,1,1))


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

    #Check if any players are alive, if not, exit
    for i in range(0,setup.players):
        if(state.players[i].alive):
            break
    else:
        return 0
    return 1
