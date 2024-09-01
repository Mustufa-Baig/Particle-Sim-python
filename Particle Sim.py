import pygame,random
pygame.init()

size=500,500
win=pygame.display.set_mode((size))
pygame.display.set_caption('Particle Sim')

clock=pygame.time.Clock()
run=True


class partical():
    def __init__(self,x,y,radius,color=((255,255,255))):
        self.x,self.y=x,y
        self.velx=0
        self.vely=0
        self.drag=0.99
        self.speed=0.15
        self.radius=radius
        self.color=color

    
    def physics(self):
        #move to cursor
        mp=pygame.mouse.get_pos()
        dx=mp[0]-self.x
        dy=mp[1]-self.y
        dist=((dx**2)+(dy**2))**0.5

        self.velx+=dx*self.speed/dist
        self.vely+=dy*self.speed/dist

        #drag
        self.velx*=self.drag
        self.vely*=self.drag

    def move(self):
        self.x+=self.velx
        self.y+=self.vely


    def draw(self,win):
        if self.radius==1:
            pygame.draw.rect(win,self.color,((self.x,self.y),(1,1)))
        else:
            pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)


def Update_partical(partical,window):
    partical.physics()
    partical.move()
    partical.draw(window)




particals=[]
for i in range(10000):
    particals.append(partical(random.randrange(0,size[0]),random.randrange(0,size[1]),1))

while run:
    win.fill((50,50,50))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    for p in particals:
        Update_partical(p,win)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
