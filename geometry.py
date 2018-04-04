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

    def __mul__(self,other):
        return Vector(self.x*other,self.y*other)

    def __str__(self):
        return str(self.x) + " "+str(self.y)

    def __eq__(self,other):
        return self.x==other.x and self.y==other.y

    def __str__(self):
        return "("+str(self.x) + ","+str(self.y)+")"

def intersect(point,rect):
    return rect.x<=point[0]<=rect.x+rect.width and rect.y<=point[1]<=rect.y+rect.height


def dot(v1,v2):
    return v1.x*v2.x + v1.y*v2.y

right = Vector(1,0)
left = Vector(-1,0)
up = Vector(0,-1)
down = Vector(0,1)
