import pygame,random
pygame.init()

size=500,500
win=pygame.display.set_mode((size))
pygame.display.set_caption('Particle Sim')

clock=pygame.time.Clock()
run=True


class Partical():
    def __init__(self,x,y,radius,color=((255,255,255))):
        self.pos=[x,y]
        self.velx=0
        self.vely=0
        self.drag=0.995
        self.speed=0.15
        self.radius=radius
        self.color=color

    
    def physics(self):
        
        #move to cursor
        
        mp=pygame.mouse.get_pos()
        dx=mp[0]-self.pos[0]
        dy=mp[1]-self.pos[1]
        dist=((dx**2)+(dy**2))**0.5

        self.velx+=dx*self.speed/dist
        self.vely+=dy*self.speed/dist
        

        #drag
        self.velx*=self.drag
        self.vely*=self.drag

    def move(self):
        self.pos[0]+=self.velx
        self.pos[1]+=self.vely


    def draw(self):
        if self.radius==1:
            pygame.draw.rect(win,self.color,((self.pos),(1,1)))
        else:
            pygame.draw.circle(win,self.color,(self.pos),self.radius)



class BoundingBox():
    def __init__(self,particals):
        self.pos=[0,0]
        self.size=[0,0]
        self.particals=particals
        self.childA=None
        self.childB=None

    def calculate(self):
        self.pos[0]=min(partical.pos[0] for partical in self.particals)
        self.pos[1]=min(partical.pos[1] for partical in self.particals)

        self.size[0]=max(partical.pos[0] for partical in self.particals) - self.pos[0]
        self.size[1]=max(partical.pos[1] for partical in self.particals) - self.pos[1]

    def split(self):
        if len(self.particals)<50:
            return None

        majorAxis=0
        if self.size[0]<self.size[1]:
            majorAxis=1

        splitPos=self.pos[majorAxis]+(self.size[majorAxis]/2)

        childParticlesA=[partical for partical in self.particals if partical.pos[majorAxis]<splitPos]
        childParticlesB=[partical for partical in self.particals if partical.pos[majorAxis]>=splitPos]

        self.childA=BoundingBox(childParticlesA)
        self.childB=BoundingBox(childParticlesB)
        
        self.childA.calculate()
        self.childA.split()

        self.childB.calculate()
        self.childB.split()

    def draw(self):
        if self.childA:
            self.childA.draw()
            self.childB.draw()
        else:
            pygame.draw.rect(win,((230,0,0)),((self.pos),(self.size)),2)




def Update_partical(partical):
    partical.physics()
    partical.move()
    partical.draw()




particals=[]
for i in range(400):
    particals.append(Partical(random.randrange(0,size[0]),random.randrange(0,size[1]),3))

rootBox=BoundingBox(particals)

while run:
    win.fill((50,50,50))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    for partical in particals:
        Update_partical(partical)

    rootBox.calculate()
    rootBox.split()
    rootBox.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
