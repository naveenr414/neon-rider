import pygame
import setup
import geometry

class Player:
    def __init__(self,pos,color,direction,number,isHuman):
        self.speed = 1
        self.pos = pos
        self.color = color
        self.direction = direction
        self.number = number
        self.isHuman = isHuman
        self.alive = True
        self.lines = []

class Death:
    def __init__(self,victim,killer,time,location):
        self.victim = victim
        self.killer = killer
        self.time = time
        self.location = location
 
initialPlayers = [
Player(geometry.Vector(120, 120), setup.colors[0], geometry.right, 1, True),
Player(geometry.Vector(900, 420), setup.colors[1], geometry.left, 3, False),
Player(geometry.Vector(900, 120), setup.colors[2], geometry.down, 2, False),
Player(geometry.Vector(120, 420), setup.colors[3], geometry.up, 4, False),
]

for i in initialPlayers:
    i.pos.x//=setup.blockSize
    i.pos.y//=setup.blockSize

keyDirections = [[pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d],
                 [pygame.K_UP,pygame.K_LEFT,pygame.K_DOWN,pygame.K_RIGHT],
                 [pygame.K_y,pygame.K_g,pygame.K_h,pygame.K_j],
                 [pygame.K_p,pygame.K_l,pygame.K_SEMICOLON,pygame.K_QUOTE]]
keyVectors = [geometry.Vector(0,-1),geometry.Vector(-1,0),
              geometry.Vector(0,1),geometry.Vector(1,0)]
playerKeys = ["W, A, S, D", "Arrow Keys", "Y, G, H, J", "P, L, ;, '"]
