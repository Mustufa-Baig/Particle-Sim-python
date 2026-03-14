import pygame,random,math
pygame.init()

size=700,500
win=pygame.display.set_mode((size))
pygame.display.set_caption('Particle Sim')

clock=pygame.time.Clock()
font = pygame.font.SysFont("Arial Black", 32)
run=True

gravityMode=False


class Partical():
    def __init__(self,color=((255,255,255))):
        self.pos=[random.randrange(0,size[0]),random.randrange(0,size[1])]
        self.velx=random.randrange(-2,2)
        self.vely=random.randrange(-2,2)
        self.drag=0.999
        self.speed=0.05
        self.radius=random.randrange(2,6)
        self.mass=self.radius/2
        self.color=color

    
    def physics(self):
        if gravityMode:
            mp=pygame.mouse.get_pos()
            dx=mp[0]-self.pos[0]
            dy=mp[1]-self.pos[1]
            dist=((dx**2)+(dy**2))**0.5
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
        if self.radius==1:
            pygame.draw.rect(win,self.color,((self.pos),(1,1)))
        else:
            pygame.draw.circle(win,self.color,(self.pos),self.radius)



class BoundingBox():
    def __init__(self,particals,rDepth=0):
        self.pos=[0,0]
        self.size=[0,0]
        self.rDepth=rDepth
        self.particals=particals
        self.childA=None
        self.childB=None

    def calculate(self):
        self.pos[0]=min(partical.pos[0] for partical in self.particals)
        self.pos[1]=min(partical.pos[1] for partical in self.particals)

        self.size[0]=max(partical.pos[0] for partical in self.particals) - self.pos[0]
        self.size[1]=max(partical.pos[1] for partical in self.particals) - self.pos[1]

    def collideParticles(self):
        for particalA in self.particals:
            for particalB in self.particals:
                if particalA==particalB:
                    continue
                dx=particalA.pos[0]-particalB.pos[0]
                dy=particalA.pos[1]-particalB.pos[1]
                dist=((dx**2)+(dy**2))**0.5
                depth=(particalA.radius+particalB.radius)-dist

                if depth>0 and not(dist==0):
                    particalA.pos[0]+=(dx/dist)*(depth/2)
                    particalA.pos[1]+=(dy/dist)*(depth/2)

                    particalB.pos[0]-=(dx/dist)*(depth/2)
                    particalB.pos[1]-=(dy/dist)*(depth/2)

                    p1,p2=particalA.pos,particalB.pos
                    v1=[particalA.velx,particalA.vely]
                    v2=[particalB.velx,particalB.vely]
                    m1,m2=particalA.mass,particalB.mass
                    e=0.99


                    nx = p1[0] - p2[0]
                    ny = p1[1] - p2[1]

                    dist = math.sqrt(nx*nx + ny*ny)
                    if dist == 0:
                        return v1, v2

                    # normalize
                    nx /= dist
                    ny /= dist

                    # relative velocity
                    rvx = v1[0] - v2[0]
                    rvy = v1[1] - v2[1]

                    vel_along_normal = rvx*nx + rvy*ny

                    # already separating
                    if vel_along_normal > 0:
                        return v1, v2

                    # impulse scalar
                    j = -(1 + e) * vel_along_normal
                    j /= (1/m1 + 1/m2)

                    # impulse vector
                    ix = j * nx
                    iy = j * ny

                    # new velocities
                    v1_new = (v1[0] + ix/m1, v1[1] + iy/m1)
                    v2_new = (v2[0] - ix/m2, v2[1] - iy/m2)

                    particalA.velx=v1_new[0]
                    particalA.vely=v1_new[1]

                    particalB.velx=v2_new[0]
                    particalB.vely=v2_new[1]



    def split(self):
        if len(self.particals)<=25 or self.rDepth>20:
            self.collideParticles()
            return None


        majorAxis=0
        if self.size[0]<self.size[1]:
            majorAxis=1

        splitPos=self.pos[majorAxis]+(self.size[majorAxis]/2)

        childParticlesA=[partical for partical in self.particals if partical.pos[majorAxis]-partical.radius<splitPos]
        childParticlesB=[partical for partical in self.particals if partical.pos[majorAxis]+partical.radius>=splitPos]

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
            




def Update_partical(partical):
    partical.physics()
    partical.move()
    partical.draw()




particals=[]
for i in range(1000):
    particals.append(Partical())


while run:
    rootBox=None
    rootBox=BoundingBox(particals)
    
    win.fill((50,50,50))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.MOUSEBUTTONUP:
            gravityMode=not(gravityMode)

    for partical in particals:
        Update_partical(partical)

    rootBox.calculate()
    rootBox.split()
    rootBox.draw()


    fps = clock.get_fps()
    fps_text = font.render(f"{fps:.2f}", True, (255, 0, 0))

    win.blit(fps_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
