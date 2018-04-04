import setup
from geometry import Rectangle, Vector, dot
import geometry
import copy
import pygame
import inputControl
import time

class Player:
    def __init__(self,pos,color,direction,number,isHuman):
        self.speed = 1
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
smallFont = pygame.font.SysFont('arial',15)
textList = []

for i in range(0,4):
    if(i==0):
        textList.append((textFont.render("GO!",False,setup.white),(590,300)))
    else:
        textList.append((textFont.render(str(i),False,setup.white),(590,300)))

class State:
    def __init__(self):
        self.players = []
        for i in range(0,setup.players):
            self.players.append(copy.copy(initialPlayers[i]))
        self.board = []
        self.startFlag = 3
        self.deathResults = []
        self.deathTexts = []

def killPlayer(state,i,j):
    yPos = len(state.deathResults)*40/3 + 20
    state.players[i].alive = False
    state.deathResults.append((i,i))
    state.deathTexts.append((smallFont.render("Player "+str(i+1),
    False,state.players[i].color),(10,yPos)))
    state.deathTexts.append((smallFont.render(" killed by ",
    False,setup.white),(60,yPos)))
    state.deathTexts.append((smallFont.render("Player "+str(j+1),
    False,state.players[j].color),(110,yPos)))


def update(screen,state):
    if(state.startFlag>-2):
        screen.blit(textList[state.startFlag][0],textList[state.startFlag][1])
        state.startFlag-=1

        #Create the player texts if its not created yet
        if(len(playerTexts)==0):
            for i in range(0,setup.players):
                playerTexts.append((textFont.render(str(i+1)+": "+playerKeys[i],False,state.players[i].color),
                                    (state.players[i].pos.x-50,state.players[i].pos.y+10)))


        #Draw the players and the instructions
        for i in range(0,setup.players):
            currentPlayer = state.players[i]
            pygame.draw.rect(screen,currentPlayer.color,(currentPlayer.pos.x,currentPlayer.pos.y,1,1))
            screen.blit(playerTexts[i][0],playerTexts[i][1])
            
        
        if(state.startFlag!=2):
            time.sleep(1)
        return 1
    
    #Update the players
    for i in range(setup.players):
        currentPlayer = state.players[i]
        if(currentPlayer.alive):

            #Update the players positions
            for j in range(1,currentPlayer.speed+1):
                newPos = currentPlayer.pos+currentPlayer.direction*j
                if(newPos.x<0 or newPos.x>setup.width
                or newPos.y<0 or newPos.y>setup.height
                or newPos in [x[0] for x in state.board]):
                    currentPlayer.alive = False

                    #Check if they were killed by going outside the box, or by another player
                    if(newPos.x<0 or newPos.x>setup.width
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

    #Draw the death board
    for i in state.deathTexts:
        screen.blit(i[0],i[1])

    #Get key input
    for j in range(setup.players):
        if(state.players[j].alive and setup.humanList[j]):
            for i in range(0,len(keyDirections[0])):
                if(inputControl.keys[keyDirections[j][i]]):
                    if(dot(keyVectors[i],state.players[j].direction)==0):
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
