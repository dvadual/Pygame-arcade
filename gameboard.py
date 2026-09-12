import pygame
from sneks import sneks
import random 
from gen_game_func import render_outlined
from food import circleobj
class gameboard():
    def __init__(self,screen:pygame.Surface,no_sneks:int,no_circles:int):
        self.screen = screen
        self.dt= 1/60
        self.width,self.height= (2560,2560)
        self.board = pygame.Surface((self.width,self.height))
        self.board.fill("black")
        self.sneks:list[sneks]=[]
        self.initplayer_pos = pygame.Vector2(self.width/2, self.height/2)
        self.no_sneks= no_sneks
        self.no_circles=no_circles
        self.default_font = pygame.font.Font(None, 48)
        self.makeagent()
        #self.makeplayer()
        #self.makesneks("random",6)
        self.makesneks("simplevectorai",15)
        self.makecircles()
        self.makeboarders()
    def makeboarders(self):
        no_of_borders= int(self.height/100)
        self.borders=[]
        for i in range(no_of_borders):
            self.borders+= [
                pygame.Rect(-100,100*i,100,100),
                pygame.Rect(100*i,-100,100,100),
                pygame.Rect(100*i,self.height,100,100),
                pygame.Rect(self.width,100*i,100,100)        
            ]
        for border in self.borders: pygame.draw.rect(self.screen,"gold",border,2)
    def makeagent(self):
        self.agent_influences={}
        self.agent_action=[]
        self.agent_point=10
        self.agent_reward=0
        self.has_agent=True
        agentsnek = sneks(self.board,self.initplayer_pos,"agent",[random.randint(0,255) for i in range(3)],10)
        self.sneks.insert(0,agentsnek)
    
            
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
        self.screen.fill("red")
        self.board.fill("black")
        for i in self.cirobjects:
            i.drawparticle(self.board)
        self.pointsurf = render_outlined(self.default_font,str(int(self.sneks[0].point)),"white","black",3)
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
        if  snake.isplayer=="agent":
            snake.environment["circles"]=self.circles
            snake.environment["bodies"]= snakebodies
            snake.environment["heads"]= snakeheads
            snake.environment["border"]= self.borders
            self.agent_influences ={key:snake.get_input_tensors(key,item) for key,item in snake.environment.items()}
            snake.ifpressed=self.agent_action
            self.agent_reward=snake.point-self.agent_point
            self.agent_point=snake.point
            self.has_agent=True



        snake.dt = self.dt
        snake.showsnek()

        indofcoll= snake.headrect.collidelistall(self.circles)
        if indofcoll:
            indofcoll.sort(reverse=True)
            for ind in indofcoll:
                snake.increasecount(self.cirobjects[ind].radius)
                self.deadcirobjects[self.cirobjects[ind]] = snake
                self.cirobjects.remove(self.cirobjects[ind])
                self.circles.remove(self.circles[ind])

        bodycoll= snake.bodyrects[-1].collidelistall(snakebodies+self.borders)  
        if bodycoll:
            bodycoll.sort()
            for circle,circleobj in snake.deadparticles():
                self.circles.append(circle)
                self.cirobjects.append(circleobj)
            self.sneks.remove(snake)
    def updategame(self,action=[]):
        if self.dt>0.1: self.dt=1/60
        self.agent_action=action
        self.updateboard()
        self.particlemovement()
        self.agent_influences ={}
        self.has_agent=False
        for snek in self.sneks:
            self.snekaction(snek)
        pointrect= self.pointsurf.get_rect(center=(320,50))
        # for border in self.borders:
        #     #print(border)
        #     pygame.draw.rect(self.board,"red",border)
        self.screen.blit(self.board,(self.screen.get_width()/2,self.screen.get_height()/2)-self.sneks[0].position)
        self.screen.blit(self.pointsurf,pointrect)
        if self.has_agent:
            if len(self.agent_influences)>0:
                return self.agent_influences,self.agent_reward
            else: return None ,self.agent_reward




    
