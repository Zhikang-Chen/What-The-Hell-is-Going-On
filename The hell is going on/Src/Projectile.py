import pygame, time, math, Config, Utility as u

class Bullet(pygame.sprite.Sprite):
    '''Spawn a bullet object'''
    def __init__(self, loc, target, speed ,damage, image, rotate = False):
        pygame.sprite.Sprite.__init__(self)
        if type(image) is pygame.Surface:
            self.image = image                      #Sprite for the bullet
        else:
            self.image = u.load_image(image)        #Sprite for the bullet
        self.rect = self.image.get_rect()           #Rect for the bullet
        self.rect.center = loc.center
        self.speed = speed                          #Speed for the bullet
        self.damage = damage                        #Damage the bullet will deal to the target
        self.dx = target[0]-self.rect.centerx       #X for the target
        self.dy = target[1]-self.rect.centery       #Y for the target
        self.currentx = float(self.rect.centerx)    #The current X for the bullet
        self.currenty = float(self.rect.centery)    #The current Y for the bullet
        self.angle = math.atan2(self.dy,self.dx)    #The angle the bullet is heading

        #Rotate the bullet to face the target
        if rotate:
            self.image = pygame.transform.rotate(self.image, 180-math.degrees(self.angle))
            self.rect = self.image.get_rect()
            self.rect.centerx = self.currentx 
            self.rect.centery = self.currenty

    def move(self):
        #Move to the target given
        self.currentx += self.speed*math.cos(self.angle)
        self.currenty += self.speed*math.sin(self.angle)
        self.rect.centerx = self.currentx
        self.rect.centery = self.currenty
        if self.rect.bottom > Config.WINDOWHEIGHT -25 or self.rect.top < 25 or self.rect.left < 25 or self.rect.right > Config.WINDOWWIDTH-25:
            self.kill()


class laser(pygame.sprite.Sprite):
    def __init__(self, loc, target, speed ,damage,windowSurface):
        pygame.sprite.Sprite.__init__(self)
        self.damage = damage
        self.killtimer = time.time()
        self.angle = math.atan2(target[1]-loc.centery,target[0]-loc.centerx)
        self.windowSurface = windowSurface
        self.target = target

        self.currentx = loc.centerx
        self.currenty = loc.centery
        keepgoing = True
        while keepgoing:
            self.currentx += speed*math.cos(self.angle)
            self.currenty += speed*math.sin(self.angle)
            if self.currentx > Config.WINDOWWIDTH-25 or self.currentx < 25:
                keepgoing = False

            if self.currenty > Config.WINDOWHEIGHT-25 or self.currenty < 25:
                keepgoing = False
        endpos = (self.currentx,self.currenty)

        self.rect = pygame.draw.line(windowSurface, (255,0,0),(loc.centerx,loc.centery), endpos, 5)
        self.image = pygame.Surface(self.rect.size)
        self.image.set_colorkey((0,0,0))

        if endpos[1] > loc.centery:
            self.rect.top = loc.centery
            starty = 5
            endy = self.image.get_height()-5
        else:
            self.rect.bottom = loc.centery
            starty = self.image.get_height()-5
            endy = 5

        if endpos[0] > loc.centerx:
            self.rect.left = loc.centerx
            startx = 5
            endx = self.image.get_width()-5
        else:
            self.rect.right = loc.centerx
            startx = self.image.get_width()-5
            endx = 5

        pygame.draw.line(self.image, (255,0,0),(startx,starty), (endx,endy), 5)

    def move(self):

        current = time.time()
        if current - self.killtimer > 0.5:
            self.kill()


#------------------------------unused code----------------------------------------------
#code that might be useful 
class Explosive(Bullet):
    def __init__(self, loc, target):
        super().__init__(loc, target, 10, 0, 'player_bullet.png')
        self.flytime = 1
        self.radius = 10
        self.explosion = False
        self.currentsize = self.image.get_rect().size
        self.endsize = (self.currentsize[0] + self.radius ,self.currentsize[1] + self.radius)
        self.starttime = time.time()

    def move(self):
        currenttime = time.time()

        if self.explosion:

            pass

        elif currenttime-self.starttime < self.flytime:
            self.currentx += self.speed*math.cos(self.angle)
            self.currenty += self.speed*math.sin(self.angle)
            self.rect.centerx = self.currentx
            self.rect.centery = self.currenty
            if self.rect.bottom > config.WINDOWHEIGHT -25 or self.rect.top < 25 or self.rect.left < 25 or self.rect.right > config.WINDOWWIDTH-25:
                self.explosion = True
        else:
            self.explosion = True
            self.kill()
