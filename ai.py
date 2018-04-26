import random
import geometry
import copy

def basic(state,player):
    currentPlayer = state.players[player]
    currentPlayer.speed = random.randint(1,10)
    currentPlayer.direction = geometry.up

def minMax(state,player):
    currentPlayer = state.players[player]
    
    #Depth 3
    newStates = []
    for i in geometry.directions:
        if geometry.dot(currentPlayer.direction,i)!=-1:
            tempState = copy.deepcopy(state)
            currentPlayer.direction = i
            dead = False

            for j in range(1,currentPlayer.speed+1):
                newPos = currentPlayer.pos+currentPlayer.direction*j
                if(newPos.x<0 or newPos.x>setup.gameWidth
                or newPos.y<0 or newPos.y>setup.height):
                    dead = True
                else:
                    for r in range(setup.players):
                        for line in state.players[r].lines:
                            end = line.direction*line.length+line.start
                            if(colinear(newPos,line.start,end)
                               and min(line.start.x,end.x)<=newPos.x<=max(line.start.x,end.x)
                               and max(line.start.y,end.y)<=newPos.y<=max(line.start.y,end.y)):
                                dead = True
                

            if(len(currentPlayer.lines)==0
               or currentPlayer.lines[-1].direction!=currentPlayer.direction):
                l = Line(currentPlayer.pos,currentPlayer.direction,currentPlayer.speed)
                currentPlayer.lines.append(l)
            else:
                currentPlayer.lines[-1].length+=currentPlayer.speed
            currentPlaye.rpos+=currentPlayer.direction*currentPlayer.speed
            newStates.append([tempState])
