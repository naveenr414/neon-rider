import setup
import pygame
import inputControl
from geometry import intersect, Rectangle, Vector
import copy

#Create a font
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS',30)

class Button:
    def __init__(self,imageLocation,location):
        self.image = pygame.image.load(imageLocation)
        self.size = self.image.get_rect().size
        self.location = location
        self.rect = Rectangle(self.location.x,self.location.y,
                              self.size[0],self.size[1])

    def intersect(self,p):
        return intersect(p,self.rect)

class Text:
    def __init__(self,text,pos,color):
        self.surface = font.render(text,False,color)
        self.pos = pos
        
def createScores():
    textS = []
    for i in range(setup.players+1):
        x = setup.width//6-10
        y = setup.height//4+font.get_height() * (i+1)

        text = "Player "+str(i)+": "+str(setup.scores[i-1])
        if(i==0):
            text = "Scores: "
            
        textS.append(Text(text,(x,y),setup.white))

    return textS
    


x = setup.width//4
y = setup.height//10
startButton = Button("images/StartButton.png",Vector(x,y))
galleryButton = Button("images/GalleryButton.png",Vector(2*x,y))
quitButton = Button("images/QuitButton.png",Vector(3*x,y))

mainButtons = [startButton,galleryButton,quitButton]
numberButtons = []

x = setup.width//20
y = setup.height//6

for i in range(setup.maxPlayers):
    num = i+1
    temp = []

    #The Buttons with 1, 2, etc.
    temp.append(Button("images/"+str(num)+"Button.png",
                                Vector(10*x-10,y*num+y)))

    temp.append(Button("images/AIButton.png",
                                Vector(12*x,num*y+y)))
    temp.append(Button("images/HumanButton.png",
                                Vector(16*x,y*num+y)))

    numberButtons.append(temp)

textSurfaces = createScores()
usedScores = setup.scores

resetScore = Button("images/ResetScoreButton.png",Vector(setup.width//6,setup.height*3//4))

def menuSetup(screen):
    pygame.mouse.set_visible(True)

    for i in mainButtons:
        screen.blit(i.image,i.location.toArray())

    for i in numberButtons:
        for j in i:
            screen.blit(j.image,j.location.toArray())

    for i in textSurfaces:
        screen.blit(i.surface,i.pos)

    screen.blit(resetScore.image,resetScore.location.toArray())

    mousePos = pygame.mouse.get_pos()

    if(inputControl.mouseDown):
        if(startButton.intersect(mousePos)):
            return 1
        if(galleryButton.intersect(mousePos)):
            return 4
        if(quitButton.intersect(mousePos)):
            return -1
            

    return 0
