#Handles player input and ai movement 
import pygame 
import random
import math

class playerMovement():
    def __init__(self,position:tuple,isplayer="random",maxspeed=200,acc=500,angularvelocity=15):
        self.dt = 0
        self.speed = [0,0,0,0]
        self.maxspeed= maxspeed
        self.acc = acc
        self.anglevelocity = angularvelocity
        self.ifpressed=[]
        self.position = pygame.Vector2(position)
        self.angle =0
        self.isplayer = isplayer
        self.frame =0
        self.environment={}

    def accelmove(self,i):
        if self.speed[i] >= self.maxspeed or self.acc == 0:
            self.speed[i]= self.maxspeed 
        else:          
            self.speed[i] = self.speed[i]+ self.acc*self.dt 
    def decelmove(self,i):
        #self.speed[k] -=  self.acc*dt if not j else -(self.acc*dt)

        if self.speed[i] <= 0 or self.acc == 0 :
            self.speed[i] = 0           
        else: 
            #print("yoo")
            self.speed[i] =  self.speed[i]- self.acc*self.dt 
    def move(self):
        ilist=[0,1,2,3]
        keys = pygame.key.get_pressed()
        if self.isplayer=="key":
            self.ifpressed =[keys[pygame.K_a],keys[pygame.K_d],keys[pygame.K_w],keys[pygame.K_s]]
        elif self.isplayer=="mouse":
            if pygame.mouse.get_pressed()[0]:
                    relpos = self.position.copy() - pygame.mouse.get_pos()
                    self.ifpressed =[relpos.x>0,relpos.x<0,relpos.y>0,relpos.y<0] 
                    print(self.ifpressed)               
        elif self.isplayer == "random":        
            self.frame+=1
            if self.frame%10 ==0:
                self.ifpressed = [random.choice([0,1]) for i in range(4)]
        elif self.isplayer== "simplevectorai":
            self.simpleaimove()

        for i,bool in enumerate(self.ifpressed):
            if bool:
                self.accelmove(i)
            else:
                self.decelmove(i)

        #print(self.speed)
        # print(ifpressed)
        vectoredlist=[self.speed[1]-self.speed[0],self.speed[3]-self.speed[2]]
        #print(self.ifpressed)

        return vectoredlist
    def angleturn(self):

        xvalue = self.speed[3]-self.speed[2]
        yvalue = self.speed[1]-self.speed[0] 
        angle_radians = math.atan2(yvalue,xvalue)
        degrees = math.degrees(angle_radians)
        if (True in self.ifpressed): 
 
            self.angle= degrees             
        else: self.angle= self.angle
    def updatepos_angle(self):
            speed = self.move()
            self.position.x += speed[0]*self.dt
            self.position.y += speed[1]*self.dt
            self.angleturn()
    
    def get_input_tensors(self,key,objlist:list[pygame.Rect]):
        colors = {"circles":"orange","bodies":"red","heads":"indigo","border":"gold"}

        detectrect:pygame.Rect=self.headrect.copy().inflate(300,300)
        pygame.draw.rect(self.screen,"red",detectrect,2)

        objdirection =pygame.Vector2(0,0)

        indofcoll=detectrect.collidelistall(objlist)
        for ind in indofcoll:
            objpos= objlist[ind].center
            objdist =objpos-self.position
            objdirection += (objdist/objdist.magnitude_squared())
            pygame.draw.line(self.screen,colors[key],self.position,self.position+objdist)
        return objdirection



    def simpleaimove(self):
            influences ={key:self.get_input_tensors(key,item) for key,item in self.environment.items()}
            direction =  influences["circles"]-0.025*influences["bodies"]+0.25*influences["heads"]-influences["border"]

            if direction.length_squared()>0:
                direction.normalize_ip()
                self.ifpressed=[direction.x<0,direction.x>0,direction.y<0,direction.y>0]
            pygame.draw.line(self.screen,"green",self.position,self.position+direction)
            self.environment={}
