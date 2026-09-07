import pygame
import random
from playerMovement import playerMovement
import math 
from gen_game_func import widtovec
from food import circleobj
class sneks(playerMovement):
    def __init__(self,screen,position,isplayer,color,point=50):
        super().__init__(position,isplayer)
        self.count = point
        self.point = self.count
        self.width=10 + int(0.2*math.log(self.point)+0.1*math.sqrt(self.point))
        self.size = self.width*2
        #self.headsurface.fill("yellow")
        self.arrowsurface = pygame.Surface((self.width*2,self.width*2), pygame.SRCALPHA)
        self.color=color
        self.screen = screen
        self.bodyrects =[]
        self.pos_for_circles=[]

        self.yvec = pygame.Vector2((0,1))
        for i in range(self.count+20):
            self.pos_for_circles.append(self.position.copy()-self.yvec*i*self.width/2)
        self.drawhead()
        self.drawarrow()


    


    def drawhead(self):
        self.headsurface = pygame.Surface((self.width*5,self.width*3.5), pygame.SRCALPHA)
        self.headrect = self.headsurface.get_rect(center=self.position)
        self.position1= (self.width*2.5,self.width)
        angles =[0,180,-90]
        angleeye=[-30,-150]
       # p =[(self.width/2,self.width),(-self.width/2,self.width),(-self.width,self.width/2),(-self.width,-self.width/2),(+self.width,-self.width/2),(+self.width,self.width/2)]       
        centers=[]
        def rectangles(i):
            j= (i+1)%3
            unit1 = (centers[i]-centers[j]).normalize()
            unit2=(centers[j]-centers[i]).normalize()
            return[((unit1).rotate(90))*self.width/2+centers[i],((unit1).rotate(270))*self.width/2+centers[i],((unit2).rotate(90))*self.width/2+centers[j],((unit2).rotate(270))*self.width/2+centers[j]]
        reclist = []
        for i in angles:
            centers.append((self.position1-widtovec(self.width/1.5,i)))
            pygame.draw.aacircle(self.headsurface, self.color,(self.position1-widtovec(self.width/1.5,i)), self.width/2)
        for i in range(3):
            pygame.draw.polygon(self.headsurface,self.color,rectangles(i))
        for i in angleeye:
            pygame.draw.aacircle(self.headsurface,"white",self.position1-widtovec(self.width/1.5,i),self.width/3)
            pygame.draw.aacircle(self.headsurface,"black",self.position1-widtovec(self.width/1.5,i),self.width/4)
       # return self.headsurface

    def drawbody(self,position,last=False):
        snakebody =pygame.Surface((self.width*2,self.width*2), pygame.SRCALPHA)
        bodyradius= self.width -2 if not last else self.width/1.5
        pygame.draw.aacircle(snakebody, self.color,(self.width,self.width), bodyradius)
        snakebody_rect = snakebody.get_rect(center=position)
        self.bodyrects.append(snakebody_rect)
        #snakebody_rect=snakebody_rect.move_to(left=position,size=(20,20)) 
        self.screen.blit(snakebody,snakebody_rect)
        #pygame.draw.rect(self.screen, 'red',snakebody_rect , width=3)
        if len(self.bodyrects)>self.count:
            self.bodyrects.pop(0)
    def drawarrow(self):
        angles =[0,180,-90]
        centers =[]
        def rectangles(i):
            j= (i+1)%3
            unit1 = (centers[i]-centers[j]).normalize()
            unit2=(centers[j]-centers[i]).normalize()
            return[((unit1).rotate(90))*self.width/10+centers[i],((unit1).rotate(270))*self.width/10+centers[i],((unit2).rotate(90))*self.width/10+centers[j],((unit2).rotate(270))*self.width/10+centers[j]]
        reclist = []
        for i in angles:
            centers.append((10,10)-widtovec(self.width/3,i))
            pygame.draw.aacircle(self.arrowsurface, "white",(centers[-1]), self.width/10)
        for i in range(2):
            i=i+1
            pygame.draw.polygon(self.arrowsurface,"white",rectangles(i))
    

    def updatebody(self):
        while self.count+1 > len(self.pos_for_circles):
            self.pos_for_circles.append(self.pos_for_circles[-1].copy())


        #print((self.pos_for_circles[0]-position).magnitude())

        self.drawbody(self.pos_for_circles[self.count],last=True)
        for i in range(self.count-1,0,-1):
            #print(pos_for_circles[i])
            #print(i)       
            self.drawbody(self.pos_for_circles[i])
 
        if abs((self.pos_for_circles[0]-self.position).magnitude()) > float(self.width/2):
                #print("hi")
            self.pos_for_circles.insert(0,self.position.copy())
        if len(self.pos_for_circles)> self.count+20:
            self.pos_for_circles = self.pos_for_circles[:self.count+20]
                #pos_for_circles.pop(0)


    def showsnek(self):
        self.updatepos_angle()
        self.updatebody()
        if self.isplayer=="key" or self.isplayer == "mouse":
            rotatedarrow = pygame.transform.rotate(self.arrowsurface,self.angle)
            snakearrow_rect = rotatedarrow.get_rect(center=self.position+(-widtovec(self.width*1.5,self.angle+90).x,+widtovec(self.width*1.5,self.angle+90).y))
            #pygame.draw.rect(self.screen, 'red',snakearrow_rect , width=3)
            self.screen.blit(rotatedarrow,snakearrow_rect)
        
        rotatedhead = pygame.transform.rotate(self.headsurface,self.angle)
        snakehead_rect = rotatedhead.get_rect(center=self.position)
        #pygame.draw.rect(self.screen, 'red',snakehead_rect , width=3)
        self.screen.blit(rotatedhead,snakehead_rect)
        self.headrect=snakehead_rect
        return snakehead_rect

    def increasecount(self,rad):
        self.count+=1
        self.point+= (rad/3)
        self.width=10 + int(math.log(self.point)+0.1*math.sqrt(self.point))
        self.drawhead()

    def deadparticles(self):
        particlespersegment = int(self.point/self.count)
        for body in self.bodyrects:
            for i in range(particlespersegment):

                color1 = [random.randint(0,255) for i in range(3)]
                x = random.randint(body.left,body.right)
                y = random.randint(body.top,body.bottom)
                radiuses = [6, 9,12]
                weights = [7, 2, 1]
                rad = random.choices(radiuses,weights=weights)[0]
                circleobject = circleobj(x,y,rad-1,color1)
                circle = circleobject.rect
                yield circle,circleobject 

                     



