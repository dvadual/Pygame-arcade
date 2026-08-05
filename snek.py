import pygame  
import math
import random
# pygame setup
pygame.init()
#screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0



screen = pygame.display.set_mode((640,640))
#player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

def widtovec(width,angle):
    angle_rad = math.radians(angle)
    return pygame.math.Vector2((width*math.cos(angle_rad),width*math.sin(angle_rad)))

class playerMovement():
    def __init__(self,position:tuple,isplayer="random",maxspeed=200,acc=500,angularvelocity=15):
        self.dt = dt
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
            self.speed[i] = self.speed[i]+ self.acc*dt 
    def decelmove(self,i):
        #self.speed[k] -=  self.acc*dt if not j else -(self.acc*dt)

        if self.speed[i] <= 0 or self.acc == 0 :
            self.speed[i] = 0           
        else: 
            #print("yoo")
            self.speed[i] =  self.speed[i]- self.acc*dt 
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
            self.position.x += speed[0]*dt
            self.position.y += speed[1]*dt
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

                     




class gameboard():
    def __init__(self,screen:pygame.Surface,no_sneks:int,no_circles:int):
        self.screen = screen
        self.width,self.height= (2560,2560)
        self.board = pygame.Surface((self.width,self.height))
        self.board.fill("black")
        self.sneks:list[sneks]=[]
        self.initplayer_pos = pygame.Vector2(self.width/2, self.height/2)
        self.no_sneks= no_sneks
        self.no_circles=no_circles
        #self.makeplayer()
        #self.makesneks("random",6)
        self.makesneks("simplevectorai",15)
        self.makecircles()
        self.makeboarders()
    def makeboarders(self):

        self.borders= [
            pygame.Rect(0,0,100,self.height),
            pygame.Rect(0,0,self.width,100),
            pygame.Rect(0,self.height,self.width,100),
            pygame.Rect(self.width,0,100,self.height)        

        ]


            
    def makeplayer(self):
        playersnek = sneks(self.board,self.initplayer_pos,"key",[random.randint(0,255) for i in range(3)],10)
        self.sneks.insert(0,playersnek)
    def makesneks(self,move,no=None):
        if no :
            number = no
            self.no_sneks+=no
        else:
            number=self.no_sneks
        for i in range(number):
            color = [random.randint(0,255) for i in range(3)]
            while True:
                x = random.randint(0,self.width)
                y = random.randint(0,self.height)
                point = int(abs(random.gauss(50,25)))  
                if point ==0: point = 1
                snake = sneks(self.board,(x,y),move,color,point)
                snakerect = snake.headrect.unionall(snake.bodyrects)
                othersnakebodies = []
                for othersnake in self.sneks:
                    othersnakebodies.append(othersnake.headrect.unionall(othersnake.bodyrects))
                if len(snakerect.collidelistall(othersnakebodies)) ==0:
                    self.sneks.append(snake)
                    break
    def makecircles(self):           
        self.circles = []
        self.cirobjects:list[circleobj]=[]
        self.deadcirobjects={}
        for i in range(self.no_circles):
            color1 = [random.randint(0,255) for i in range(3)]
            while True:
                x = random.randint(0,self.width)
                y = random.randint(0,self.height)
                radiuses = [6, 9,12]
                weights = [7, 2, 1]
                rad = random.choices(radiuses,weights=weights)[0]
                circleobject = circleobj(x,y,rad-1,color1)
                circle = circleobject.rect
                if len(circle.collidelistall(self.circles)) ==0:
                    self.circles.append(circle)
                    self.cirobjects.append(circleobject)                        
                    break
    def updateboard(self):
        self.screen.fill("black")
        self.board.fill("black")
        for i in self.cirobjects:
            i.drawparticle(self.board)
        self.pointsurf = render_outlined(default_font,str(int(self.sneks[0].point)),"white","black",3)
    def particlemovement(self):
        for deadobj,snake in list(self.deadcirobjects.items()):
            relpos=deadobj.rect.center-snake.position
            if abs(relpos.x) < 4 and abs(relpos.y) < 4:
                #print("yes")
                self.deadcirobjects.pop(deadobj)
            else:
                direction = -relpos.normalize() 
                deadobj.rect.move_ip(direction*10)
                deadobj.drawparticle(self.board)

                

    def snekaction(self,snake:sneks):

        snakeheads=[]
        snakebodies =[]

        for othersnake in self.sneks:
            if othersnake == snake: continue
            snakebodies+= othersnake.bodyrects
            snakeheads.append(othersnake.headrect)
        if snake.isplayer =="simplevectorai":
            snake.environment["circles"]=self.circles
            snake.environment["bodies"]= snakebodies
            snake.environment["heads"]= snakeheads
            snake.environment["border"]= self.borders


        snake.showsnek()

        indofcoll= snake.headrect.collidelistall(self.circles)
        if indofcoll:
            indofcoll.sort(reverse=True)
            for ind in indofcoll:
                snake.increasecount(self.cirobjects[ind].radius)
                self.deadcirobjects[self.cirobjects[ind]] = snake
                self.cirobjects.remove(self.cirobjects[ind])
                self.circles.remove(self.circles[ind])

        bodycoll= snake.bodyrects[-1].collidelistall(snakebodies)  
        if bodycoll:
            bodycoll.sort()
            for circle,circleobj in snake.deadparticles():
                self.circles.append(circle)
                self.cirobjects.append(circleobj)
            self.sneks.remove(snake)
    def updategame(self):
        self.updateboard()
        self.particlemovement()
        for snek in self.sneks:
            self.snekaction(snek)
        pointrect= self.pointsurf.get_rect(center=(320,50))
        for border in self.borders:
            print(border)
            pygame.draw.rect(self.board,"red",border)


        self.screen.blit(self.board,(screen.get_width()/2,screen.get_height()/2)-self.sneks[0].position)
        self.screen.blit(self.pointsurf,pointrect)




    




default_font = pygame.font.Font(None, 48)
def render_outlined(
    font: pygame.Font,
    text: str,
    text_color: pygame.typing.ColorLike,
    outline_color: pygame.typing.ColorLike,
    outline_width: int,) -> pygame.Surface:
    old_outline = font.outline
    if old_outline != 0:
        font.outline = 0
    base_text_surf = font.render(text, True, text_color)
    font.outline = outline_width
    outlined_text_surf = font.render(text, True, outline_color)

    outlined_text_surf.blit(base_text_surf, (outline_width, outline_width))
    font.outline = old_outline
    return outlined_text_surf

        
#movement = playerMovement(maxspeed=200,acc=500) 
  
class circleobj():
    def __init__(self,x,y,rad,innercolor):
        self.innercolor = innercolor
        self.radius= rad
        self.surf = pygame.Surface((rad*2,rad*2), pygame.SRCALPHA)
        self.center =(x,y)
        self.rect = self.surf.get_rect(center=(x,y))
        center = (self.surf.get_height()/2,self.surf.get_width()/2)
        radius = self.rect.width/2
        gradientwid= radius/2
        pygame.draw.aacircle(self.surf,self.innercolor,center,radius-2)
        r=int(self.innercolor[0])
        g=int(self.innercolor[1])
        b=int(self.innercolor[2])
        a=255
        t= int(255/(radius-gradientwid))
        for i in range(int(radius-gradientwid)):
            a-= t
            pygame.draw.aacircle(self.surf,(r,g,b,a),center,gradientwid+i,1)
    def drawparticle(self,surface,rel= 0):
        surface.blit(self.surf,self.rect)

game = gameboard(screen,20,800)
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.updategame()

    pygame.display.flip()
    
    dt = clock.tick(60) / 1000
pygame.quit()