import random
import geometry
import copy
import setup

class Node:
    def __init__(self,depth,maxDepth,state,player):
        self.depth = depth
        self.maxDepth = maxDepth
        self.state = state
        self.value = 0
        self.player = player
        self.direction = self.state.players[player].direction

        if(depth == maxDepth):
            self.value = self.state.players[player].pos.x

        else:
            self.propagateDown()
            if(depth%2==1):
                self.value = 0
                for i in range(len(self.newState)):
                    self.value = max(self.value,self.newState[i][0].value)
            else:
                self.value = 1000000
                for i in range(len(self.newState)):
                    self.value = min(self.value,self.newState[i][0].value)


            if(self.depth == 1):
                i = 0
                for d in geometry.directions:
                    if(geometry.dot(self.state.players[player].direction,d)!=-1):
                        if(self.newState[i][0].value==self.value):
                            self.direction= d
                        i+=1

    def propagateDown(self):
        self.newState = []
        currentPlayer = self.state.players[self.player]

        for i in geometry.directions:
            if geometry.dot(currentPlayer.direction,i)!=-1:

                tempState = copy.deepcopy(self.state)
                newPlayer = tempState.players[self.player]
                newPlayer.direction = i
                dead = False

                for j in range(1,newPlayer.speed+1):
                    newPos = newPlayer.pos+newPlayer.direction*j
                    if(newPos.x<0 or newPos.x>setup.gameWidth
                    or newPos.y<0 or newPos.y>setup.height):
                        dead = True
                    else:
                        for r in range(setup.players):
                            for line in self.state.players[r].lines:
                                end = line.direction*line.length+line.start
                                if(geometry.colinear(newPos,line.start,end)
                                   and min(line.start.x,end.x)<=newPos.x<=max(line.start.x,end.x)
                                   and max(line.start.y,end.y)<=newPos.y<=max(line.start.y,end.y)):
                                    dead = True
                    

                if(len(newPlayer.lines)==0
                   or newPlayer.lines[-1].direction!=newPlayer.direction):
                    l = geometry.Line(newPlayer.pos,newPlayer.direction,newPlayer.speed)
                    newPlayer.lines.append(l)
                else:
                    newPlayer.lines[-1].length+=newPlayer.speed
                newPlayer.pos+=newPlayer.direction*newPlayer.speed
                self.newState.append((Node(self.depth+1,self.maxDepth,tempState,self.player),dead))


    def __gt__(self,other):
        return self.value>other.value

def basic(state,player):
    currentPlayer = state.players[player]
    currentPlayer.speed = random.randint(1,10)
    currentPlayer.direction = geometry.up

def minMax(state,player):
    currentPlayer = state.players[player]
    currentPlayer.direction = Node(1,5,state,player).direction
