import pygame,random,math
pygame.init()

size=700,500
win=pygame.display.set_mode((size))
pygame.display.set_caption('Particle Sim')

clock=pygame.time.Clock()
font = pygame.font.SysFont("Arial Black", 32)
run=True

gravityMode=False
mp=pygame.mouse.get_pos()

class Partical():
    def __init__(self,color=((255,255,255))):
        self.pos=[random.randrange(0,size[0]),random.randrange(0,size[1])]
        self.velx=random.randrange(-2,2)
        self.vely=random.randrange(-2,2)
        self.drag=0.999
        self.speed=0.05
        self.radius=random.randrange(2,4)
        self.mass=self.radius/2
        self.color=color

    
    def physics(self):
        if gravityMode:
            
            dx=mp[0]-self.pos[0]
            dy=mp[1]-self.pos[1]
            dist=math.sqrt((dx*dx)+(dy*dy))
            if dist!=0:
                self.velx+=dx*self.speed/dist
                self.vely+=dy*self.speed/dist
        
        

        #drag
        self.velx*=self.drag
        self.vely*=self.drag

        #wall collision
        elasticity=0.98
        if self.pos[0]+self.radius>size[0]:
            self.pos[0]=size[0]-self.radius
            self.velx=-abs(self.velx)*elasticity

        elif self.pos[0]<self.radius:
            self.pos[0]=self.radius
            self.velx=abs(self.velx)*elasticity
            

        if self.pos[1]+self.radius>size[1]:
            self.pos[1]=size[1]-self.radius
            self.vely=-abs(self.vely)*elasticity
            
        elif self.pos[1]<self.radius:
            self.pos[1]=self.radius
            self.vely=abs(self.vely)*elasticity
        
    def move(self):
        self.pos[0]+=self.velx
        self.pos[1]+=self.vely


    def draw(self):
        pygame.draw.circle(win,self.color,(self.pos),self.radius)



class BoundingBox():
    def __init__(self,particals,rDepth=0):
        self.pos=[0,0]
        self.size=[0,0]
        self.rDepth=rDepth
        self.particals=particals
        self.childA=None
        self.childB=None

    
    def collideParticles(self):
        for i in range(len(self.particals)):
            particalA = particals[self.particals[i]]
            for j in range(i+1, len(self.particals)):
                particalB = particals[self.particals[j]]

                pA,pB=particalA.pos,particalB.pos

                vAx,vAy=particalA.velx,particalA.vely
                vBx,vBy=particalB.velx,particalB.vely
                
                rA,rB=particalA.radius,particalB.radius
                mA,mB=particalA.mass,particalB.mass
                
                dx=pA[0]-pB[0]
                dy=pA[1]-pB[1]
                dist2=(dx*dx)+(dy*dy)
                rad2=rA+rB

                if dist2<(rad2*rad2):
                    dist=math.sqrt(dist2)
                    depth=(rA+rB)-dist
                    if dist==0:
                        continue

                    pA[0]+=(dx/dist)*(depth/2)
                    pA[1]+=(dy/dist)*(depth/2)

                    pB[0]-=(dx/dist)*(depth/2)
                    pB[1]-=(dy/dist)*(depth/2)




                    e=0.99

                    # normalize
                    dx /= dist
                    dy /= dist

                    # relative velocity
                    rvx = vAx - vBx
                    rvy = vAy - vBy

                    vel_along_normal = rvx*dx + rvy*dy

                    # already separating
                    if vel_along_normal > 0:
                        continue

                    # impulse scalar
                    j = -(1 + e) * vel_along_normal
                    j /= (1/mA + 1/mB)

                    # impulse vector
                    ix = j * dx
                    iy = j * dy

                    # new velocities
                    particalA.velx+= ix/mA
                    particalA.vely+= iy/mA

                    particalB.velx-= ix/mB
                    particalB.vely-= iy/mB

    def calculate(self):
        minx=miny=float("inf")
        maxx=maxy=float("-inf")

        particles=self.particals
        for p in particles:
            x,y=particals[p].pos
            if x < minx: minx = x
            if x > maxx: maxx = x
            if y < miny: miny = y
            if y > maxy: maxy = y


        self.pos=[minx,miny]
        self.size=[maxx-minx,maxy-miny]


    def split(self):
        if len(self.particals)<=10 or self.rDepth>10:
            self.collideParticles()
            return None


        majorAxis=0
        if self.size[0]<self.size[1]:
            majorAxis=1

        splitPos=self.pos[majorAxis]+(self.size[majorAxis]/2)

        childParticlesA=[]
        childParticlesB=[]

        for p in self.particals:
            if particals[p].pos[majorAxis]-particals[p].radius<splitPos:
                childParticlesA.append(p)
            elif particals[p].pos[majorAxis]+particals[p].radius>=splitPos:
                childParticlesB.append(p)

        self.childA=BoundingBox(childParticlesA,self.rDepth+1)
        self.childB=BoundingBox(childParticlesB,self.rDepth+1)
        
        self.childA.calculate()
        self.childA.split()

        self.childB.calculate()
        self.childB.split()

    def draw(self):
        if self.childA:
            self.childA.draw()
            self.childB.draw()
        else:
            pygame.draw.rect(win,((100,100,100)),((self.pos),(self.size)),2)
            




particalsCount=2000

particals=[]
pList=list(range(particalsCount))
for i in range(particalsCount):
    particals.append(Partical())


while run:
    rootBox=BoundingBox(pList)
    mp=pygame.mouse.get_pos()

    win.fill((50,50,50))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.MOUSEBUTTONUP:
            gravityMode=not(gravityMode)

    for partical in particals:        
        partical.physics()
        partical.move()
        partical.draw()


    rootBox.calculate()
    rootBox.split()
    rootBox.draw()


    fps = clock.get_fps()
    fps_text = font.render(f"{fps:.2f}", True, (255, 0, 0))

    win.blit(fps_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
