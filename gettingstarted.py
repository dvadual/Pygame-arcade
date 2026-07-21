import pygame 

pygame.init()

screen = pygame.display.set_mode((640,640))

img = pygame.image.load("exanpleimage.jpeg").convert()
img = pygame.transform.scale(img,(img.get_width()*0.2,img.get_height()*0.1))
x=0
y=30
font = pygame.font.Font(None,size=30)
clock = pygame.time.Clock()
something= pygame.Surface((64,64),pygame.SRCALPHA)
something.blit(img,(0,0))
something.blit(img,(20,0))
something.blit(img,(10,10))
running = True 
delta_time = 0.1
img.set_colorkey((0,0,0))
mpos =pygame.mouse.get_pos()
moving = False
moving_y= False
while running:
    screen.fill((255,255,255))
    screen.blit(img,(x,y))
    hitbox = pygame.Rect(x,y,img.get_width(),img.get_height())
    target = pygame.Rect(300,0,160,280)
    colision = hitbox.colliderect(target)
    m_collision = target.collidepoint(mpos)
    pygame.draw.rect(screen,(255*colision,255* (not m_collision),0),target)
    img.set_alpha(max(0, x*3 if x < 320  else 255-(x-320)))
    if  moving:
        x+= 50*delta_time
    if moving_y:
        y+= 30*delta_time
    text = font.render("Hello world",True,(0,0,0))
    screen.blit(text,(300,100))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving = True
            if event.key == pygame.K_s:
                moving_y = True if not moving_y else False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moving = False




        
    pygame.display.flip()
    delta_time = clock.tick(60)/1000
    delta_time = max(0.001,min(0.1,delta_time))
        
pygame.quit()

