class Rectangle:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def getSize(self):
        return (self.x,self.y,self.width,self.height)

    def __str__(self):
        return str(self.x) + " "+str(self.y) + " "+str(self.width)+ " "+str(self.height)

class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __add__(self,other):
        return Vector(self.x+other.x,self.y+other.y)

    def __sub__(self,other):
        return Vector(self.x-other.x,self.y-other.y)

    def __mul__(self,other):
        return Vector(self.x*other,self.y*other)

    def __str__(self):
        return str(self.x) + " "+str(self.y)

    def __eq__(self,other):
        return self.x==other.x and self.y==other.y

    def __str__(self):
        return "("+str(self.x) + ","+str(self.y)+")"

    def cross(self, other):
        return (self.x*other.y - self.y*other.x)

    def toArray(self):
        return [self.x,self.y]

class Line:
    def __init__(self,start,direction,length):
        self.start = start
        self.direction = direction
        self.length = length

    def __str__(self):
        return str(self.start) + " " +str(self.direction) + " "+str(self.length)

def intersect(point,rect):
    return rect.x<=point[0]<=rect.x+rect.width and rect.y<=point[1]<=rect.y+rect.height


def colinear(p1,p2,p3):
    v1 = p2-p1
    v2 = p3-p1
    if(v1.cross(v2)==0):
        return True
    else:
        return False

def dot(v1,v2):
    return v1.x*v2.x + v1.y*v2.y

right = Vector(1,0)
left = Vector(-1,0)
up = Vector(0,-1)
down = Vector(0,1)
