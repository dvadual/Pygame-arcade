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
    def __init__(self,position,isplayer="random",maxspeed=200,acc=500,angularvelocity=15):
        self.dt = dt
        self.speed = [0,0,0,0]
        self.maxspeed= maxspeed
        self.acc = acc
        self.anglevelocity = angularvelocity
        self.ifpressed=[]
        self.position = position
        self.angle =0
        self.isplayer = isplayer
        self.frame =0

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
        elif self.isplayer == "random":        
            self.frame+=1
            if self.frame%10 ==0:
                self.ifpressed = [random.choice([0,1]) for i in range(4)]


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
        #print(yvalue,xvalue)
        angle_radians = math.atan2(yvalue,xvalue)
       # print(math.degrees(angle_radians))
        degrees = math.degrees(angle_radians)
        if (True in self.ifpressed): 
 
            self.angle= degrees             
            # if abs(oldangle - degrees) <= self.anglevelocity:
            #     return degrees
            # elif(oldangle<degrees):
            #     print("reducing")
            #     oldangle+= self.anglevelocity
            #     return oldangle
            # elif(oldangle>degrees):
            #     print("uincreasing")
            #     oldangle-=self.anglevelocity
            #     return oldangle
        else: self.angle= self.angle
    def updatepos_angle(self):
            speed = self.move()
            self.position.x += speed[0]*dt
            self.position.y += speed[1]*dt
            self.angleturn()


class sneks(playerMovement):
    def __init__(self,screen,position,isplayer,color,count=50):
        super().__init__(position,isplayer)
        self.point = 0
        self.width=10
        self.size = self.width*2
        

        #self.headsurface.fill("yellow")
        self.arrowsurface = pygame.Surface((self.width*2,self.width*2), pygame.SRCALPHA)
        self.color=color
        self.screen = screen
        self.bodyrects =[]
        self.pos_for_circles=[]
        self.count = count
        self.yvec = pygame.Vector2((0,1))
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
        #pygame.draw.polygon(self.headsurface,color,((self.position-widtovec(self.width,0),player_pos-widtovec(self.width,180),player_pos- widtovec(self.width,-90))))
       # veclist = list(map(lambda x : self.position+ pygame.Vector2(x),p))

        #pygame.draw.polygon(self.headsurface,color,veclist)
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
        #pygame.draw.rect(screen, 'red',snakebody_rect , width=3)
        if len(self.bodyrects)>count:
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
        if len(self.pos_for_circles) ==0:
            for i in range(self.count+20):
                self.pos_for_circles.append(self.position.copy()-self.yvec*i*self.width/2)

        #print((self.pos_for_circles[0]-position).magnitude())
        #print(self.count)
        self.drawbody(self.pos_for_circles[self.count],last=True)
        for i in range(self.count-1,0,-1):
            #print(pos_for_circles[i])
            #print(i)       
            self.drawbody(self.pos_for_circles[i])
        
 
        if abs((self.pos_for_circles[0]-self.position).magnitude()) > float(self.width/2):
                #print("hi")
                self.pos_for_circles.insert(0,self.position.copy())
                if len(self.pos_for_circles)> self.count+20:
                    del self.pos_for_circles[-1]
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
        if self.count%10 ==0:
            self.width+=2
            self.drawhead()


class gameboard():
    def __init__(self):
        self.screen=pygame.display.set_mode((640,640))
        self.sneks=[]


def drawparticle(surface,center,radius,innercolor,outercolor):
    innerrgb =pygame.Color(innercolor)
    inrgb =(innerrgb.r,innerrgb.g,innerrgb.a)
    outerrgb =pygame.Color(outercolor)
    outrgb =(outerrgb.r,outerrgb.g,outerrgb.a)
    gradientwid= radius/2
    pygame.draw.aacircle(surface,innercolor,center,gradientwid+i,1)
    for i in range(int(gradientwid)):
        t= i/gradientwid
        r=int(innercolor[0]+(outercolor[0]-innercolor[0])*t)
        g=int(innercolor[1]+(outercolor[1]-innercolor[1])*t)
        b=int(innercolor[2]+(outercolor[2]-innercolor[2])*t)
        pygame.draw.aacircle(surface,(r,g,b),center,gradientwid+i,1)
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
    def __init__(self,x,y,rad,innercolor,outercolor):
        self.innercolor = innercolor
        self.outercolor = outercolor
        self.radius= rad
        self.surf = pygame.Surface((rad*2,rad*2), pygame.SRCALPHA)
        self.center =(x,y)
        self.rect = self.surf.get_rect(center=(x,y))
    # innerrgb =pygame.Color(innercolor)
    # inrgb =(innerrgb.r,innerrgb.g,innerrgb.a)
    # outerrgb =pygame.Color(outercolor)
    # outrgb =(outerrgb.r,outerrgb.g,outerrgb.a)
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
        #self.rect =self.rect.move_to(center=self.center)
        surface.blit(self.surf,self.rect)

count = 10
width,height= (2560,2560)
player_pos = pygame.Vector2(width/2, height/2)
board = pygame.Surface((width,height))
board.fill("black")

circles = []
cirobjects=[]
deadcirobjects={}
for i in range(500):

    color1 = [random.randint(0,255) for i in range(3)]
    color2 = [random.randint(0,255) for i in range(3)]
    while True:
        x = random.randint(0,width)
        y = random.randint(0,height)
        radiuses = [6, 9,12]
        weights = [7, 2, 1]
        rad = random.choices(radiuses,weights=weights)[0]
        circleobject = circleobj(x,y,rad-1,color1,color2)
        circle = circleobject.rect
        if len(circle.collidelistall(circles)) ==0:
            circles.append(circle)
            cirobjects.append(circleobject)
            
            break


snakes =[
sneks(board,player_pos,"key","blue",count),
sneks(board,player_pos.copy(),"random","gold",50),
sneks(board,player_pos.copy(),"random","gray",40),
sneks(board,player_pos.copy(),"random","white",30),
sneks(board,player_pos.copy(),"random","orange",20)
]

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    board.fill("black")
    screen.fill("black")
    for i in cirobjects:
        i.drawparticle(board)
    points = render_outlined(default_font,str(int(snakes[0].point)),"white","black",3)

    dictcleanup=[]
    for deadobj,snake in list(deadcirobjects.items()):
        relpos=deadobj.rect.center-snake.position
        direction = -relpos.normalize() if relpos.magnitude() != 0 else [0,0]
        print(direction)
        deadobj.rect.move_ip(direction*5)
        deadobj.drawparticle(board)
        if abs(relpos.x) < 3 and abs(relpos.y) < 3:
            print("yes")
            deadcirobjects.pop(deadobj)
    #map(lambda x: deadcirobjects.pop(x),dictcleanup)

            
    
    for i,snake in enumerate(snakes):
        snake.showsnek()
        snakebodies =[]
        for othersnake in snakes:
            if othersnake == snake: continue
            snakebodies+= othersnake.bodyrects


        indofcoll= snake.headrect.collidelistall(circles)
        if indofcoll:
            indofcoll.sort(reverse=True)
            for ind in indofcoll:
                snake.increasecount(cirobjects[ind].radius)
                # relpos=cirobjects[ind].rect.center-snake.position
                # direction = -relpos.normalize()
                # cirobjects[ind].rect.move_ip(direction*10)
                # print(relpos,ind)
                # if abs(relpos.x) < 2 and abs(relpos.y) < 2:
                deadcirobjects[cirobjects[ind]] = snake
                cirobjects.remove(cirobjects[ind])
                circles.remove(circles[ind])
        bodycoll= snake.headrect.collidelistall(snakebodies)  
        if bodycoll:
            bodycoll.sort()
            # print(bodycoll)
            # print(snake.color)

        


        #cirobjects[ind].drawparticle(board)
        #screen.blit(board)
            
    pointrect= points.get_rect(center=(320,50))
    screen.blit(board,(screen.get_width()/2,screen.get_height()/2)-snakes[0].position)
    screen.blit(points,pointrect)

    pygame.display.flip()
    
    dt = clock.tick(60) / 1000
pygame.quit()