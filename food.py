import pygame
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

