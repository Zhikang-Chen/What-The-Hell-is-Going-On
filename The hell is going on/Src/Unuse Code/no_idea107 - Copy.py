#This game was written by Ken Chen
#The game is a text base top side view shooter
#TD: improve Weapon, timer for dash, buff the enemy, display the current level
#random level, more music
import pygame, os, random, time, math, weaponstat as weapons
from pygame.locals import *


#Size of the screen
WINDOWWIDTH = 1000 
WINDOWHEIGHT = 600

#Colours
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255,000,000)


FRAMERATE = 60

#------------------------------Enemies-------------------------------
#A tuple cotaining stat for each enemy
#enemy sprite, health, speed, damage, movement, spwan locaction
#sprite, health, speed, damage, movement, firetime ,bullet ,bulletspeed,spwan locaction
NORMAL_CAT = ("cat.png",1,5,0.5,2)
ARMOR = ("cat with bullet proof vest.png",5,1,0.5,2)

CAT_WITH_KNIFE = ("cat_with_knife.png",2,6,1,2)
SHIELD = ("cat with shield.png",8,1,0.5,2)

GUNNER = ("cat with a gun.png",2,3,1,1,1,"cat_bullet.png",10)
SMGER = ("cat with a smg.png",2,4,0.5,1,0.2,"cat_bullet.png",15)

CAT_SOLDIER = ("cat soldier.png", 5,2,1.5,1,0.4,"cat_bullet.png",12)
CAT_M1 = ("cat with m1 garand.png", 3,3,3,1,0.75,"cat_bullet.png",20)
CAT_PYTHON = ("cat with python.png", 3,5,5,1,1.5,"cat_bullet.png",10)

ENEMY_DICT = {'N':NORMAL_CAT, 
              'A':ARMOR, 
              'G':GUNNER,
              'K':CAT_WITH_KNIFE,
              'S':SMGER,
              'SH':SHIELD,
              'CS':CAT_SOLDIER,
              'CM':CAT_M1,
              'CP':CAT_PYTHON} #A dictionary cotaining all the enemies
#--------------------------Rooms------------------------
#10x6 list containing location of the enemies
ROOM1 =  [['A', (250,150)],
         ['A', (750,150)],
         ['N', (550,250)],
         ['N', (450,350)],
         ['G', (250,450)],
         ['G', (750,450)]]

ROOM2 =  [['N', (150,150)],
        ['N', (850,150)],
        ['N', (450,250)],
        ['N', (550,250)],
        ['N', (450,350)],
        ['N', (550,350)],
        ['N', (150,450)],
        ['N', (850,450)]]

ROOM3 =  [['G', (150,150)],
        ['G', (850,150)],
        ['G', (150,450)],
        ['G', (850,450)]]

ROOM4 =  [['A', (150,150)],
        ['N', (850,150)],
        ['N', (350,250)],
        ['A', (650,350)],
        ['A', (150,450)],
        ['N', (850,450)]]
#after the second map
ROOM5 =  [['S' ,(150,150)],
        ['N' ,(250,250)],
        ['K' ,(850,250)],
        ['A' ,(250,350)],
        ['S' ,(850,450)]]

ROOM6 =  [['G' ,(150,150)],
        ['SH' ,(450,350)],
        ['SH' ,(650,350)],
        ['G' ,(850,450)]]

ROOM7 =  [['N' ,(850,150)],
        ['K' ,(450,250)],
        ['K' ,(550,350)],
        ['N' ,(150,450)]]
#after the 4th map
ROOM8 =  [['SH' ,(850,150)],
        ['CS' ,(450,250)],
        ['SH' ,(350,350)],
        ['K' ,(150,450)]]

ROOM9 =  [['S' ,(150,150)],
        ['S' ,(850,150)],
        ['CS' ,(450,250)],
        ['CS' ,(550,350)],
        ['S' ,(150,450)],
        ['S' ,(850,450)]]

ROOM10 = [['K' ,(150,150)],
        ['K' ,(850,150)],
        ['CS' ,(450,250)],
        ['K' ,(550,250)],
        ['K' ,(450,350)],
        ['K' ,(550,350)],
        ['K' ,(150,450)],
        ['K' ,(850,450)]]

ROOM11 = [['CS' ,(250,150)],
        ['CS' ,(750,150)],
        ['CS' ,(250,450)],
        ['CS' ,(750,450)]]
#After the 6th map
ROOM12 = [['CS' ,(450,250)],
            ['CM' ,(550,250)],
            ['CM' ,(450,350)],
            ['CS' ,(550,350)]]

ROOM13 = [['CP' ,(150,150)],
            ['K' ,(850,150)],
            ['CS' ,(550,250)],
            ['CP' ,(150,450)],
            ['K' ,(850,450)]]

ROOM14 = [['CP' ,(450,150)],
            ['CP' ,(550,150)],
            ['CP' ,(450,250)],
            ['CP' ,(550,250)]]

ROOM15 = [['CP' ,(350,250)],
            ['CS' ,(450,350)],
            ['CS' ,(550,350)],
            ['CM' ,(350,450)],
            ['CM' ,(650,450)]]

ROOM16 = [['CM' ,(150,150)],
            ['CM' ,(150,250)],
            ['SH' ,(250,250)],
            ['CM' ,(150,350)],
            ['SH' ,(250,350)],
            ['CM' ,(150,450)]]
#---------------------------Sepical rooms--------------------------
EMPTY_ROOM = []

NEXT = [['B', (500,300)]]

BOSSROOM = [['BO', (500,300)]]

TESTROOM = [['A' ,(300-50,100+50)],
            ['A' ,(800-50,100+50)],
            ['N' ,(600-50,200+50)],
            ['N' ,(500-50,300+50)],
            ['G' ,(300-50,400+50)],
            ['G' ,(800-50,400+50)]]

TUTORIAL_ROOM = [['G', (500,300)]]

ROOM_DICT = {'TR':TUTORIAL_ROOM ,
             'T':TESTROOM,
             'B':BOSSROOM,
             'N':NEXT,
             'E':EMPTY_ROOM,
             'S':EMPTY_ROOM,
             'R1':ROOM1,
             'R2':ROOM2,
             'R3':ROOM3,
             'R4':ROOM4,
             'R5':ROOM5,
             'R6':ROOM6,
             'R7':ROOM7,
             'R8':ROOM8,
             'R9':ROOM9,
             'R10':ROOM10,
             'R11':ROOM11,
             'R12':ROOM12,
             'R13':ROOM13,
             'R14':ROOM14,
             'R15':ROOM15,
             'R16':ROOM16} #A dictionary cotaining all the rooms
#------------------------------Maps-----------------------------------
#List cotaining location of each room 
TESTMAP = [ ['','','','',''],
           ['','','T','',''],
           ['','','S','',''],
           ['','','',''],
           ['','',''] ]

TUTORIAL = [['','','','','','',''],
            ['','S','E','E','E','TR','N',''],
            ['','','','','','','']]

MAP1 = [['','',''],
       ['N','R2',''],
       ['','R1',''],
       ['R3','R4',''],
       ['','E','R1',''],
       ['','S',''],
       ['','','']]

MAP2 = [ ['','','','','','',''],
        ['','','R1','R2','E','N',''],
        ['','S','R3','','','E',''],
        ['','','E','R3','R2','R1',''],
        ['','','R4','','','',''],
        ['','','','','','',''] ]

MAP3 = [ ['','','','',''],
        ['','S','R6','R1',''],
        ['','','R2','',''],
        ['','R4','R7','R5',''],
        ['','E','R3','',''],
        ['','','R5','E','N',''],
        ['','','','',''] ]

MAP4 = [ ['','','','',''],
        ['','R1','','S',''],
        ['','R4','R5','E','R3',''],
        ['','R6','','','R7',''],
        ['','N','','','R2',''],
        ['','','','E','R1',''],
        ['','','','',''] ]

MAP5 = [ ['','','','','','',''],
        ['','R8','R7','E','','',''],
        ['','R11','','R7','S','R10',''],
        ['','R5','','','','R5',''],
        ['','R6','R9','','','R9',''],
        ['','','N','R6','','E',''],
        ['','','','R11','R7','R6',''],
        ['','','','','','',''] ]

MAP6 = [['','','','','','','','',''],
        ['','','','S','R10','','','',''],
        ['','N','R10','','E','R7','R11','',''],
        ['','','R11','R7','R9','','','',''],
        ['','','','','','','','','']]

MAP7 = [['','','','','','','','','',''],
        ['','','','','S','','','','',''],
        ['','','R12','R16','R15','R14','R12','','',''],
        ['','R13','R15','','R13','','R15','R14','',''],
        ['','E','','R14','R16','','','R13','',''],
        ['','R15','R12','E','','','','R16','N',''],
        ['','N','','','','','','','',''],
        ['','','','','','','','','','']]

MAP8 = [['','',''],
       ['N','R16',''],
       ['','R12',''],
       ['R5','R13',''],
       ['','R16','R14',''],
       ['','S',''],
       ['','','']]

FINALMAP = [ ['','',''],
         ['','N',''],
         ['','B',''],
         ['','E',''],
         ['','S',''],
         ['','',''] ]

MAPS = [MAP1,MAP2,MAP3,MAP4,MAP5,MAP6,MAP7,MAP8,FINALMAP]

TIP_LIST = ["You can shut this annoying music off by pressing 'M'",
            "Insert motivational quote here",
            "I created this loading screen just to annoy people",
            "Dash is overpower",
            "The best way to win is just to spam mouse 1",
            "No cats were harmed in the making of this game",
            "Yes, the bgm is kahoot music",
            "You can beat this game within 5 minutes",
            "First aid kit can heal you",
            "Shoot at the cats until they are dead. I mean gone",
            "Use W A S D to move",
            "Use mouse to shoot",
            "Another one bits the dust",
            "Use space to dash",
            "Non-drug substance(syringe thingy) can increase your damage",
            "Painkiller can increase your max health",
            "Remember to buy the nonexistent weapon DLC which only cost $2.99",
            "YOU WON'T LAST 5 MINUTES PLAYING THIS!",
            "We all live in a yellow subarine"] #A list of tip that will be display on loading screen

def terminate():
    '''Terminate program '''
    pygame.quit()
    os._exit(1)
def load_image(filename):
    '''Load an image from the file name given'''
    #This is just to annoy people
    image = pygame.image.load(filename)
    #image = image.convert()
    image = image.convert_alpha()
    return image
def drawText(text, font_name, size, surface, x, y, textcolour,center = True):
    '''Draw a text'''
    font= pygame.font.SysFont(font_name , size)
    textobj = font.render(text, 1, textcolour)
    textrect = textobj.get_rect()
    if center:
        textrect.centerx = x
        textrect.centery = y
    else:
        textrect.topleft = (x,y)
    surface.blit(textobj, textrect)
    return(textrect)

def start_screen(windowSurface):
    '''The start screen for the game'''
    windowSurface.fill(WHITE)
    image = load_image("the hack is going on v6.png")
    windowSurface.blit(image, windowSurface.get_rect())
    drawText("Press anything to begin", "comicsansms", 40, windowSurface, windowSurface.get_rect().centerx-175, windowSurface.get_rect().centery-40, BLACK)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP:
                return()
def main_manual(windowSurface, PlayMusic):
    '''The main manual'''
    windowSurface.fill(WHITE)
    image = load_image("the hack is going on v7.png")
    #rect1 = drawText("1. Start game", "comicsansms", 40, windowSurface, windowSurface.get_rect().left+145, windowSurface.get_rect().top+150, BLACK)
    #rect2 = drawText("2. Tutorial", "comicsansms", 40, windowSurface, windowSurface.get_rect().left+115, windowSurface.get_rect().top+250, BLACK)
    #rect3 = drawText("3. Exit", "comicsansms", 40, windowSurface, windowSurface.get_rect().left+80, windowSurface.get_rect().top+350, BLACK)

    Music_on = load_image("sound on.png")
    Music_off = load_image("sound off.png")
    music_rect = Music_on.get_rect()
    music_rect.topleft = (900,500)

    sel = pygame.Surface((260,60))
    sel.set_alpha(128) 
    sel.fill(WHITE)  
    
    mouse_rect = Rect((0,0),(1,1))

    while True:
        if not pygame.mixer.music.get_busy() and PlayMusic:
            pygame.mixer.music.play(-1, 0.0)
        windowSurface.blit(image, windowSurface.get_rect())
        drawText("What The H*ck Is Going On", "comicsansms", 50, windowSurface, windowSurface.get_rect().centerx-170, windowSurface.get_rect().top+60, BLACK)
        drawText("A mostly text base bullet hell dungeon crawl game without the fun part", "comicsansms", 20, windowSurface, windowSurface.get_rect().centerx-170, windowSurface.get_rect().top+105, BLACK)
        rect1 = drawText("1. Start game", "comicsansms", 40, windowSurface, windowSurface.get_rect().left+145, windowSurface.get_rect().top+150, BLACK)
        rect2 = drawText("2. Tutorial", "comicsansms", 40, windowSurface, windowSurface.get_rect().left+115, windowSurface.get_rect().top+250, BLACK)
        rect3 = drawText("3. Exit", "comicsansms", 40, windowSurface, windowSurface.get_rect().left+80, windowSurface.get_rect().top+350, BLACK)
        
        if PlayMusic:
            windowSurface.blit(Music_on, music_rect)
        else:
            windowSurface.blit(Music_off, music_rect)
        #Get location for the mouse and check if it's colliding with the text, if so change colour of the text
        mouse_pos = pygame.mouse.get_pos()
        mouse_rect.center = mouse_pos
        #sel.fill(RED)  

        if mouse_rect.colliderect(rect1):
            windowSurface.blit(sel, rect1)
        elif mouse_rect.colliderect(rect2):
            windowSurface.blit(sel, rect2)
        elif mouse_rect.colliderect(rect3):
            windowSurface.blit(sel, rect3)

        #React when player press any number
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP:
                if event.key == ord('1'):
                    return(1,PlayMusic)
                elif event.key == ord('2'):
                    return(2,PlayMusic)
                elif event.key == ord('3'):
                    terminate()
                elif event.key == ord('m'):
                    if PlayMusic:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    PlayMusic = not PlayMusic
            elif event.type == MOUSEBUTTONDOWN:
                if mouse_rect.colliderect(rect1):
                    if pygame.mouse.get_pressed()[0]:
                        return(1,PlayMusic)
                elif mouse_rect.colliderect(rect2):
                    if pygame.mouse.get_pressed()[0]:
                        return(2,PlayMusic)
                elif mouse_rect.colliderect(rect3):
                    if pygame.mouse.get_pressed()[0]:
                        terminate()
                elif mouse_rect.colliderect(music_rect):
                    if pygame.mouse.get_pressed()[0]:
                        if PlayMusic:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                        PlayMusic = not PlayMusic
        pygame.display.update()


class Object(pygame.sprite.Sprite):
    '''Object the player can interact with'''
    def __init__(self, image,location,function):
        pygame.sprite.Sprite.__init__(self)
        if type(image) is str:
            self.image = load_image(image) #Sprit for the object
        elif type(image) is pygame.Surface:
            self.image = image
        self.rect = self.image.get_rect()   #Rect for the object
        self.rect.center = location         #The location the object will spwan in
        self.function = function            #Functionality of the object

    def reaction(self, player):
        #Reaction of the object when player interact with it
        if self.rect.colliderect(player.rect) and player.use:
            if self.function == 1:
                #Heals player when their current health is lower than the max health
                if player.health < player.max_health:
                    player.health += 1
                    if player.health > player.max_health:
                        player.health -= player.health - player.max_health
                    self.kill()
            elif self.function == 2:
                #Increase max health by 1
                player.max_health +=1
                self.kill()
            elif self.function == 3:
                #Increase damage by 0.25
                player.damage += 0.25
                self.kill()
            elif self.function == 4:
                #Change room
                player.change_level = True

class Room(pygame.sprite.Sprite):
    '''Read blue print and create a room with it'''
    def __init__(self, upexit,downexit,leftexit,rightexit, blueprint):

        #200*50
        #-------------walls----------------------
        self.wall = load_image("wall side.png")                 #Sprite for the wall
        self.wall2 = load_image("other wall.png")               #Sprite for the wall

        self.topwall = Rect((0,0), (1000,25))                   #Rect for the top wall
        self.topwall.center = (1000//2,12)

        self.bottomwall = Rect((0,0), (1000,25))                #Rect for the bottom wall
        self.bottomwall.center = (1000//2, 600-13)

        self.leftwall = Rect((0,0),(25,600))                    #Rect for the left wall
        self.leftwall.center = (12,600//2)

        self.rightwall = Rect((0,0),(25,600))                   #Rect for the right wall
        self.rightwall.center = (1000-13,600// 2)

        #------------EXits----------------------
        self.open = True                                        #If the player is allow leave the room or not
        door = load_image("door.png")                           #Sprite for the door
        door2 = load_image("door2.png")                         #Sprite for the door
        self.exits = {}                                         #A dictionary store info for the exits
        self.doors = {}                                         #A dictionary store info for the doors
        #Creat an exit and a door
        if upexit:
            upexitRect = Rect((0,0),(175,26))
            upexitRect.center = (500,13)
            topdoor = upexitRect.copy()
            topdoor.centerx = 675
            self.doors["up"] = [door.copy(),topdoor]
            self.exits["upexit"] = upexitRect

        if downexit:
            downexitRect = Rect((0,0),(175,26))
            downexitRect.center = (500, 600-13)
            bottomdoor = downexitRect.copy()
            bottomdoor.centerx = 675
            self.doors["down"] = [door.copy(),bottomdoor]
            self.exits["downexit"] = downexitRect

        if leftexit:
            leftexitRect = Rect((0,0),(26,175))
            leftexitRect.center = (13,300)
            leftdoor = leftexitRect.copy()
            leftdoor.centery = 475
            self.doors["left"] = [door2.copy(),leftdoor]
            self.exits["leftexit"] = leftexitRect

        if rightexit:
            rightexitRect = Rect((0,0),(26,175))
            rightexitRect.center = (1000-13,300)
            rightdoor = rightexitRect.copy()
            rightdoor.centery = 475
            self.doors["right"] = [door2.copy(),rightdoor]
            self.exits["rightexit"] = rightexitRect

        self.enemies = pygame.sprite.Group()                    #All the ememies in the room
        self.object = pygame.sprite.Group()                     #All the object in the room

        #Read the blue print and put the ememies in the correspondence location
        for idk in blueprint:
            if idk[0] == 'BO':
                self.enemies.add(Boss())
            elif idk[0] == 'B':
                self.object.add(Object("button.png",idk[1],4))
            else:
                self.spawn(ENEMY_DICT[idk[0]],idk[1])

    def draw_room(self, windowSurface):
        #Draw everything in the room

        #Draw the four walls
        windowSurface.blit(self.wall2, self.leftwall)
        windowSurface.blit(self.wall2, self.rightwall)
        windowSurface.blit(self.wall, self.topwall)
        windowSurface.blit(self.wall, self.bottomwall)

        #Draw each exit 
        for exit in self.exits.values():
            pygame.draw.rect(windowSurface,WHITE,exit)

        #Draw each doors
        for door in self.doors.values():
            windowSurface.blit(door[0], door[1])


        self.object.draw(windowSurface)                 #Draw all the object in the room
        #for enemy in self.enemies:
            #pygame.draw.rect(windowSurface,RED,enemy.rect)
        self.enemies.draw(windowSurface)                #Draw all the enemies in the room

    def doorlogic(self):
        #How door will move

        #Open the door
        if len(self.enemies) <= 0:
            self.open = True
            for direction,rect in self.doors.items():
                if direction == "up" or direction == "down":
                    if rect[1].centerx < 675:
                        rect[1].centerx += 5
                        self.open = False
                else:
                    if rect[1].centery < 475:
                        rect[1].centery += 5
                        self.open = False
        else:
        #Close the door
            self.open = False
            for direction,rect in self.doors.items():
                if direction == "up" or direction == "down":
                    if rect[1].centerx > 500:
                        rect[1].centerx -= 5
                else:
                    if rect[1].centery > 300:
                        rect[1].centery -= 5

    def spawn(self, list, loc = None):
        '''Read a list and spwan enemy with the stat from the list'''
        if len(list) == 5:
            an_enemy = Enemy(list[0],list[1],list[2],list[3],list[4],loc)
        elif len(list) == 8:
            an_enemy = Range_enemy(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7],loc)

        self.enemies.add(an_enemy)

class Player():
    '''Character the user control'''
    def __init__(self,windowSurface):
        self.windowSurface = windowSurface
        self.healthbar = load_image('health bar.png')           #sprite for health
        self.healthbar2 = load_image('empty health.png')        #sprite for empty health
        self.unchage_image = load_image("play_handgun.png")     #The unrotated image
        self.image = self.unchage_image.copy()                  #Sprite for the player
        self.rect = self.image.get_rect()                       #A Rect from the sprite
        self.rect.center = (WINDOWWIDTH//2, WINDOWHEIGHT//2)    
        self.moveLeft = False                                   #The direction the player is moving in
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        self.dash = False                                       #Dash 
        self.use = False                                        #E
        self.dashDistance = 150                                 #The distance of the dash
        self.dashCooldown = time.time()                         #A cool down timer for the dash
        self.speed = 10                                         #Number of pixel the player will move in
        self.max_health = 5                                     #Maxium amount of health the player can have
        self.health = 5.0                                       #The current health the play has
        self.max_shield = 5                                     #Maxium amount of shield the player can have
        self.shield = 5.0                                       #The current shield the play has
        self.shield_cooldown = time.time()                      #A cool down timer for the resignation of shield
        self.damageCooldown = time.time()                       #A cool down timer for player to take damage
        self.shoottimer = time.time()                           #A timer for player to shoot
        self.damage = 1                                         #Damage the player will deal
        self.change_level = False
        self.fire = False

        self.weapons = ['pistol','spas','m16','python','m1','machina']
        self.num = 0
        self.currentweapon = weapons.stats[self.weapons[self.num]]

    def update(self, room):
        #Update the position and the direction player is facing
        cooldown = time.time()

        if self.moveUp and self.rect.top > room.topwall.bottom:
            self.rect.top -= self.speed
            if self.dash and cooldown - self.dashCooldown  >= 0.5:
                self.rect.top -= self.dashDistance
                self.dashCooldown = time.time()
            while self.rect.top < room.topwall.bottom:
                self.rect.bottom += 1

        if self.moveDown and self.rect.bottom < room.bottomwall.top:
            self.rect.bottom += self.speed
            if self.dash and cooldown - self.dashCooldown  >= 0.5:
                self.rect.bottom += self.dashDistance
                self.dashCooldown = time.time()
            while self.rect.bottom > room.bottomwall.top:
                self.rect.bottom -= 1

        if self.moveLeft and self.rect.left > room.leftwall.right:
            self.rect.left -= self.speed
            if self.dash and cooldown - self.dashCooldown  >= 0.5:
                self.rect.left -= self.dashDistance
                self.dashCooldown = time.time()
            while self.rect.left < room.leftwall.right:
                self.rect.left += 1

        if self.moveRight and self.rect.right < room.rightwall.left:
            self.rect.right += self.speed
            if self.dash and cooldown - self.dashCooldown  >= 0.5:
                self.rect.right += self.dashDistance
                self.dashCooldown = time.time()
            while self.rect.right > room.rightwall.left:
                self.rect.right -= 1

        #Regenerate the shield each 8 second, the timer will reset when the player get hurt
        if cooldown - self.shield_cooldown >= 8 and self.shield < self.max_shield:
            self.shield += 1
            self.shield_cooldown = time.time()
            if self.shield > self.max_shield:
                self.shield -= self.shield - self.max_shield

        #Rotate the spite to where the mouse is
        currentx = self.rect.centerx
        currenty = self.rect.centery
        dx, dy = pygame.mouse.get_pos()
        angle = 270-  math.degrees(math.atan2(dy-currenty,dx-currentx))
        self.image = pygame.transform.rotate(self.unchage_image, angle)
        x = self.rect.left
        y = self.rect.top
        #self.rect = self.image.get_rect()
        #self.rect.left = x
        #self.rect.top = y
        #Reset the dash and use key
        self.dash = False
        self.use = False

    def take_damage(self, damage_taken):
        #Reduce player's shield or health when called
        cooldown = time.time()
        if cooldown - self.damageCooldown >= 0.5:
            if self.shield > 0:
                self.shield -= damage_taken
                if self.shield < 0:
                    self.shield = 0
                self.damageCooldown = time.time()
            else:
                self.health -= damage_taken
                self.damageCooldown = time.time()
            self.shield_cooldown = time.time()

    def shoot(self, bulletgroup,playsound = False):
        #shoot a bullet
        currenttime = time.time()
        if currenttime - self.shoottimer >= self.currentweapon['firespeed']:
            self.shoottimer = time.time()
            if 'special' in self.currentweapon:
                self.currentweapon['special'](bulletgroup,self,self.windowSurface)
            else:
                bulletgroup.add(Bullet(self.rect, pygame.mouse.get_pos(),self.currentweapon['bulletspeed'],self.currentweapon['damage'],self.currentweapon['bulletsprite']))
            
            if not self.currentweapon['auto']:
                self.fire = False

            if playsound:
                pygame.mixer.Sound(self.currentweapon['firesound']).play()

    def hud(self):
        #Display player's health, shield and cool down for the shield
        hpos = 50   #Location for the hud
        vpos = 40   #Location for the hud
        #---------------------Health----------------------------------
        for index in range(self.max_health):
            if index+1 >= 11 and vpos == 40:
                vpos += 27
                hpos = 50

            if index < self.health:
                self.windowSurface.blit(self.healthbar,(hpos,vpos))
            else:
                self.windowSurface.blit(self.healthbar2,(hpos,vpos))
            hpos += 16
        vpos += 27
        #---------------------Shield----------------------------------
        armorbar = pygame.Rect((50,vpos),(158,12))
        currentarmor = pygame.Rect((51,vpos+1),(self.shield*31.2,10))
        pygame.draw.rect(self.windowSurface,(0,74,127),armorbar)
        if self.shield > 0:
            pygame.draw.rect(self.windowSurface,(0,148,255),currentarmor)

        if self.shield < self.max_shield:
            currenttime = time.time()
            vpos += 12
            armorcooldown = pygame.Rect((50,vpos),(158,4))
            cooldownbar = pygame.Rect((51,vpos+1),((currenttime - self.shield_cooldown)*19.5,2))
            pygame.draw.rect(self.windowSurface,(96,96,96),armorcooldown)
            pygame.draw.rect(self.windowSurface,(135,135,135),cooldownbar)

        vpos += 15
        drawText(self.currentweapon['name'], 'comicsansms', 20, self.windowSurface, 50,vpos,BLACK,False)

    def change(self):
        self.num += 1
        if self.num == len(self.weapons):
            self.num = 0
        self.currentweapon = weapons.stats[self.weapons[self.num]]

    def draw(self):
        #Draw player and their bullet 
        self.windowSurface.blit(self.image, self.rect)
        pass

class Bullet(pygame.sprite.Sprite):
    '''Spawn a bullet object'''
    def __init__(self, loc, target, speed ,damage, image, rotate = False):
        pygame.sprite.Sprite.__init__(self)
        if type(image) is pygame.Surface:
            self.image = image                      #Sprit for the bullet
        else:
            self.image = load_image(image)          #Sprit for the bullet
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
        if self.rect.bottom > WINDOWHEIGHT -25 or self.rect.top < 25 or self.rect.left < 25 or self.rect.right > WINDOWWIDTH-25:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    '''Spawn an Enemy'''
    def __init__(self, image, health = 1, speed = 0, damage = 0, movement = 0, locaction = None):
        pygame.sprite.Sprite.__init__(self)
        if type(image) is pygame.Surface:
            self.unchage_sprite = image                             #unchange sprit for the enemy
        else:
            self.unchage_sprite = load_image(image)                 #unchange sprit for the enemy
        self.image = self.unchage_sprite                            #Sprit for the enemy
        self.rect = self.image.get_rect()                           #Rect for the enemy
        self.damage = damage                                        #The damage enemy will deal to the player
        self.health = health                                        #Health for the enemy
        self.speed = speed                                          #Speed for the enemy
        self.damageCooldown = time.time()

        if locaction is None:
            self.rect.left = random.randrange(0, WINDOWWIDTH)
            self.rect.top = random.randrange(0, WINDOWHEIGHT)
        else:
            self.rect.center = locaction                            #The locaction the enemy will be spwan in
        self.movement = movement                                    #The type of movement the enemy has
        #0 = no movement
        #1 = random movement
        #2 = move to player
        if movement == 1:
            self.wavepoint = Rect((random.randrange(25, WINDOWWIDTH-25),random.randrange(25, WINDOWHEIGHT-25)), (5,5))

    def attack(self,player = None,bullet = None):
        #An empty function for range enemy
        pass

    def rotate(self, player):
        #Rotate the sprite to face the player
        currentx = self.rect.centerx
        currenty = self.rect.centery
        dx, dy = player.rect.centerx, player.rect.centery
        angle = 180-  math.degrees(math.atan2(dy-currenty,dx-currentx))
        self.image = pygame.transform.rotate(self.unchage_sprite, angle)
        x = self.rect.left
        y = self.rect.top

        #self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def moverandom(self, player, room):
        #Move to a random wave point

        if self.rect.centerx > self.wavepoint.centerx:
            self.rect.centerx -= self.speed
            if pygame.sprite.collide_mask(self,player) is not None or self.rect.colliderect(room.leftwall):
                self.rect.centerx += self.speed + 2
                self.wavepoint.center = (random.randrange(50, WINDOWWIDTH-50),random.randrange(50, WINDOWHEIGHT-50))

        elif self.rect.centerx < self.wavepoint.centerx:
            self.rect.centerx += self.speed
            if pygame.sprite.collide_mask(self,player) is not None or self.rect.colliderect(room.rightwall):
                self.rect.centerx -= self.speed + 2
                self.wavepoint.center = (random.randrange(50, WINDOWWIDTH-50),random.randrange(50, WINDOWHEIGHT-50))

        if self.rect.centery > self.wavepoint.centery:
            self.rect.centery -= self.speed
            if pygame.sprite.collide_mask(self,player) is not None or self.rect.colliderect(room.topwall):
                self.rect.centery += self.speed + 2
                self.wavepoint.center = (random.randrange(50, WINDOWWIDTH-50),random.randrange(50, WINDOWHEIGHT-50))

        elif self.rect.centery < self.wavepoint.centery:
            self.rect.centery += self.speed
            if pygame.sprite.collide_mask(self,player) is not None or self.rect.colliderect(room.bottomwall):
                self.rect.centery -= self.speed + 2
                self.wavepoint.center = (random.randrange(50, WINDOWWIDTH-50),random.randrange(50, WINDOWHEIGHT-50))

        if self.rect.colliderect(self.wavepoint):
            self.wavepoint.center = (random.randrange(50, WINDOWWIDTH-50),random.randrange(50, WINDOWHEIGHT-50))

    def moveplayer(self,player, room):
        #Move to player
        mask_collide = pygame.sprite.collide_mask(self,player) is not None
        if self.rect.centerx > player.rect.centerx:
            self.rect.centerx -= self.speed 
            if mask_collide or self.rect.colliderect(room.leftwall):
                self.rect.centerx += self.speed  + 2
            
        elif self.rect.centerx < player.rect.centerx:
            self.rect.centerx += self.speed
            if mask_collide or self.rect.colliderect(room.rightwall):
                self.rect.centerx -= self.speed  + 2

        if self.rect.centery > player.rect.centery:
            self.rect.centery -= self.speed
            if mask_collide or self.rect.colliderect(room.topwall):
                self.rect.centery += self.speed  + 2

        elif self.rect.centery < player.rect.centery:
            self.rect.centery += self.speed
            if mask_collide or self.rect.colliderect(room.bottomwall):
                self.rect.centery -= self.speed  + 2

    def stayaway(self):
        #Stop enemies from coliding with eachother 
        group = self.groups()
        colide = pygame.sprite.spritecollideany(self, group[0], collided = None)
        if colide is not self:
            if self.rect.centerx > colide.rect.centerx:
                self.rect.centerx += self.speed + 2
            elif self.rect.centerx < colide.rect.centerx:
                self.rect.centerx -= self.speed + 2
            if self.rect.centery > colide.rect.centery:
                self.rect.centery += self.speed + 2
            elif self.rect.centery < colide.rect.centery:
                self.rect.centery -= self.speed + 2

    def take_damage(self, damage_taken):
        #Reduce player's shield or health when called
        cooldown = time.time()
        if cooldown - self.damageCooldown >= 0.5:
                self.health -= damage_taken
                self.damageCooldown = time.time()

class Range_enemy(Enemy):
    def __init__(self, image, health, speed, damage, movement, firetime ,bullet ,bulletspeed ,locaction=None):
        super().__init__(image, health=health, speed=speed, damage=damage, movement=movement, locaction=locaction)
        self.firetime = firetime
        self.bullettime = time.time()
        self.bullet = bullet
        self.bulletspeed = bulletspeed

    def attack(self,player,bullets):
        #An empty function for range enemy
        endtime = time.time()
        if endtime-self.bullettime > self.firetime:
            bullets.add(Bullet(self.rect,(player.rect.centerx,player.rect.centery),self.bulletspeed,self.damage ,self.bullet))
            self.bullettime = time.time()

class Boss(Range_enemy):
    '''FINAL Boss for the game'''
    def __init__(self):
        super().__init__('final boss.png', 200, 1, 2.5, 1, 0.1, 'cat_bullet.png', 10, (500,300))
        self.laser = load_image('lazer.png')
        self.stage = 1
        self.angle = 0

    def attack(self, player, bullets):
        endtime = time.time()
        if self.stage == 1:
            if endtime-self.bullettime > self.firetime:
                bullets.add(Bullet(self.rect,(player.rect.centerx,player.rect.centery),self.bulletspeed,self.damage ,self.bullet))
                self.bullettime = time.time()
            if self.health < 150:
                self.stage = 2
                self.firetime = 1
        if self.stage == 2:
            bullets.add(Bullet(self.rect,(0,0),30,self.damage ,self.laser,True))
            bullets.add(Bullet(self.rect,(0,600),30,self.damage ,self.laser,True))
            bullets.add(Bullet(self.rect,(1000,0),30,self.damage ,self.laser,True))
            bullets.add(Bullet(self.rect,(1000,600),30,self.damage ,self.laser,True))

            if endtime-self.bullettime > 1:
                bullets.add(Bullet(self.rect,(player.rect.centerx,player.rect.centery),10,5 ,self.bullet))
                self.bullettime = time.time()

            if self.health < 100:
                self.stage = 3
                self.movement = 2
                self.speed = 5
        if self.stage == 3:
            if self.health < 50:
                self.speed = 7

    def rotate(self, player):
        #Rotate the sprite to face the player
        if self.stage == 1:
            currentx = self.rect.centerx
            currenty = self.rect.centery
            dx, dy = player.rect.centerx, player.rect.centery
            self.angle = 180-  math.degrees(math.atan2(dy-currenty,dx-currentx))
            self.image = pygame.transform.rotate(self.unchage_sprite, self.angle)
            x = self.rect.left
            y = self.rect.top

            #self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.top = y
        elif self.stage == 2 and int(self.angle) != 90:
            if int(self.angle) > 90:
                self.angle = int(self.angle) - 1
            elif int(self.angle) < 90:
                self.angle = int(self.angle) + 1
            currentx = self.rect.centerx
            currenty = self.rect.centery
            dx, dy = player.rect.centerx, player.rect.centery
            self.image = pygame.transform.rotate(self.unchage_sprite, self.angle)
            x = self.rect.left
            y = self.rect.top
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.top = y

class Game():
    '''The game class'''
    def __init__(self, maplist ,windowSurface, PlayMusic):
        self.windowSurface = windowSurface                           
        #-----------------------Music-----------------------------
        self.halfhealth = False                                      #If the player is at helf health
        self.playsound = PlayMusic                                   #Play sound and music
        pygame.mixer.music.load('Kahoot! 20 Second Countdown #3 Music.ogg')
        #------------------------Sound----------------------------
        #Pre-loaded sound
        self.record_scratch = pygame.mixer.Sound('record scratch sound.wav')
        self.gunfire = pygame.mixer.Sound('bang.wav')
        self.catdeath = pygame.mixer.Sound('dead.wav')
        #--------------------------sprite--------------------------
        #Pre-loaded sprite
        self.firstaid = load_image("First aid.png")
        self.painkiller = load_image("painkiller.png")
        self.notdrug = load_image("not drug.png")
        self.bullet = load_image("player_bullet.png")
        self.healthbar = load_image('health bar.png')
        self.healthbar2 = load_image('empty health.png')
        #--------------------------Player--------------------------
        self.player = Player(self.windowSurface)                                        #The player
        #--------------------------Group--------------------------
        self.bullets = pygame.sprite.Group()                          #Group for player's bullet
        self.enemybullets = pygame.sprite.Group()                     #Group for enemies' bullet
        #---------------------------Maps & room------------------
        self.allmaps = maplist                                        #A list contain all the map
        self.currentmap = 0                                           #The current map the player is in
        mapdata = self.readmap(self.allmaps[self.currentmap])              #Date from readmap
        #mapdata = readmap(MAP6)
        self.roomlist = mapdata[0]                                    #All the room in the maps
        self.loc = mapdata[1]                                         #The current location for the player
        self.CurrentRoom = self.roomlist[self.loc[0]][self.loc[1]]    #The room plyer is in
        #---------------------------Game loop--------------------------
        self.gameOver = False                                         #Is the game over

    def display_frame(self):
        '''Display the current frame in the game'''
        #---------------------------Backgound--------------------------
        self.windowSurface.fill(WHITE)
        self.CurrentRoom.draw_room(self.windowSurface)
        #-----------------------------player, and enemies--------------
        #pygame.draw.rect(self.windowSurface, RED, self.player.rect) #Hit box
        self.windowSurface.blit(self.player.image, self.player.rect)
        for item in self.CurrentRoom.object:
            if item.rect.colliderect(self.player.rect):
                drawText("E", 'comicsansms', 30, self.windowSurface,self.player.rect.centerx, self.player.rect.centery - 35,BLACK)
        #--------------------------Bullet--------------------------------
        self.bullets.draw(self.windowSurface)
        self.enemybullets.draw(self.windowSurface)
        #for bullet in self.bullets:
            #pygame.draw.rect(self.windowSurface, RED, bullet.rect)

        #for baddy in self.CurrentRoom.enemies:
            #pygame.draw.rect(windowSurface, RED, baddy.rect)
            #pygame.draw.rect(windowSurface, RED, baddy.wavepoint)
        #---------------------------Health and shield------------------
        self.player.hud()
        #text = "Health: " + str(self.player.max_health) + "/" + str(float(self.player.health)) 
        #drawText(text, 'comicsansms', 20, self.windowSurface, self.windowSurface.get_rect().left+100,self.windowSurface.get_rect().top+50,BLACK)
        #text = "Shield: " + str(self.player.max_shield) + "/" + str(float(self.player.shield))
        #drawText(text, 'comicsansms', 20, self.windowSurface, self.windowSurface.get_rect().left+100,self.windowSurface.get_rect().top+75,BLACK)
        pygame.display.update()

    def process_events(self):
        '''Process player input'''
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    os._exit(1)
            elif event.type == KEYDOWN: 
                    # update the direction of the player
                    if event.key == K_LEFT or event.key == ord('a'):
                        self.player.moveLeft = True
                        #self.player.moveRight = False
                    elif event.key == K_RIGHT or event.key == ord('d'):
                         self.player.moveRight = True
                         #self.player.moveLeft = False
                    elif event.key == K_UP or event.key == ord('w'):
                        self.player.moveUp = True
                        #self.player.moveDown=False
                    elif event.key == K_DOWN or event.key == ord('s'):
                        self.player.moveDown = True
                        #self.player.moveUp = False 
                    elif event.key == K_SPACE or event.key == ord(' '):
                        self.player.dash = True
                    elif event.key == K_e or event.key == ord('e'):
                        self.player.use = True
                    elif event.key == K_c or event.key == ord('c'):
                        self.player.change()

            elif event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        os._exit(1)
                    # the player has stopped moving
                    elif event.key == K_LEFT or event.key == ord('a'):
                        self.player.moveLeft = False
                    elif event.key == K_RIGHT or event.key == ord('d'):
                        self.player.moveRight = False
                    elif event.key == K_UP or event.key == ord('w'):
                        self.player.moveUp = False
                    elif event.key == K_DOWN or event.key == ord('s'):
                        self.player.moveDown=False
                    elif event.key == K_m or event.key == ord('m'):
                        if self.playsound:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                        self.playsound = not self.playsound
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.player.fire = True
                    #self.bullets.add(Bullet(self.player.rect, pygame.mouse.get_pos(),30,self.player.damage,self.bullet))
                    #self.bullets.add(Explosive(self.player.rect, pygame.mouse.get_pos()))
                    #if self.playsound:
                        #self.gunfire.play()
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.player.fire = False
                
    def run_logic(self):
        '''Game logic'''
        if not self.gameOver:
            try:
                endtime = time.time()
                #---------------------------------------------------Music---------------------------------------------------
                #Change music depend on player's health
                if self.player.health < self.player.max_health/2 and not self.halfhealth:
                    if self.playsound:
                        self.record_scratch.play()
                    pygame.mixer.music.load('Kahoot! 30 Second Countdown #1 Music (extended).ogg')
                    self.halfhealth = True
                elif self.player.health >= self.player.max_health/2 and self.halfhealth:
                    if self.playsound:
                        self.record_scratch.play()
                    self.record_scratch.play()
                    pygame.mixer.music.load('Kahoot! 20 Second Countdown #3 Music.ogg')
                    self.halfhealth = False
                #Play music if the music isn't playing and playsound is true
                if not pygame.mixer.music.get_busy() and self.playsound: 
                    pygame.mixer.music.play(-1, 0.0)
                #---------------------------------------------------Change room check---------------------------------------
                #Check if the player has collide with the exit and change room if the player does collide with the exit
                self.CurrentRoom.doorlogic()
                exitcollide = self.player.rect.collidedict(self.CurrentRoom.exits,1)
                if exitcollide is not None and self.CurrentRoom.open:
                    if exitcollide[0] == "upexit":
                        self.loc[0]-=1
                        self.player.rect.centery = WINDOWHEIGHT-75
                    if exitcollide[0] == "downexit":
                        self.loc[0]+=1
                        self.player.rect.centery = 75
                    if exitcollide[0] == "rightexit":
                        self.loc[1]+=1
                        self.player.rect.centerx = 75
                    if exitcollide[0] == "leftexit":
                        self.loc[1]-=1
                        self.player.rect.centerx = WINDOWWIDTH - 75
                    #Change room and clear out all the bullet
                    self.CurrentRoom = self.roomlist[self.loc[0]][self.loc[1]]
                    self.bullets.empty()
                    self.enemybullets.empty()
                #-----------------------------------------------------enemy logic------------------------------------------
                for enemy in self.CurrentRoom.enemies:
                    if enemy.health <= 0:
                        #Spawn and random object when they die
                        if self.playsound:
                            self.catdeath.play()
                        number = random.randrange(0,101)
                        if number <= 10:
                            self.CurrentRoom.object.add(Object(self.firstaid,(enemy.rect.centerx,enemy.rect.centery),1))
                        elif number >= 90 and number <= 93:
                            self.CurrentRoom.object.add(Object(self.painkiller,(enemy.rect.centerx,enemy.rect.centery),2))
                        elif number >= 80 and number <= 83:
                            self.CurrentRoom.object.add(Object(self.notdrug,(enemy.rect.centerx,enemy.rect.centery),3))
                        enemy.kill()
                    else:
                        if enemy.movement == 1:
                            enemy.moverandom(self.player,self.CurrentRoom)
                        elif enemy.movement == 2:
                            enemy.moveplayer(self.player, self.CurrentRoom)
                        enemy.rotate(self.player)

                        enemy.stayaway()

                        enemy.attack(self.player,self.enemybullets)

                        if enemy.rect.colliderect(self.player.rect.inflate(2,2)):
                            if pygame.sprite.collide_mask(enemy,self.player) is not None:
                                self.player.take_damage(enemy.damage)

                #-----------------------------------------Bullet logic--------------------------------------------
                for enemybullet in self.enemybullets:
                    enemybullet.move()
                    colide = enemybullet.rect.colliderect(self.player.rect)
                    if colide:
                        hit = pygame.sprite.collide_mask(enemybullet,self.player)
                        if hit is not None:
                            self.player.take_damage(enemybullet.damage)
                            enemybullet.kill()

                for bullet in self.bullets:
                    bullet.move()
                    colide = pygame.sprite.spritecollideany(bullet, self.CurrentRoom.enemies)
                    if colide is not None:
                        hit = pygame.sprite.collide_mask(bullet,colide)
                        if hit is not None:
                            colide.take_damage(bullet.damage)
                            if type(bullet) is Bullet:
                                self.bullets.remove(bullet)
                #------------------------------------------Item logic------------------------------------------------
                #If the player is interacting the button object change room
                for item in self.CurrentRoom.object:
                    item.reaction(self.player)

                    if self.player.change_level:
                        self.player.change_level = False
                        self.currentmap += 1
                        if self.currentmap <= len(self.allmaps)-1:
                            self.loading(self.windowSurface)
                            mapdata = self.readmap(self.allmaps[self.currentmap])
                            self.roomlist = mapdata[0]
                            self.loc = mapdata[1]
                            self.CurrentRoom = self.roomlist[self.loc[0]][self.loc[1]]
                            self.player.shield = self.player.max_shield
                        else:
                            self.gameOver = True
                #-----------------------------------------Player----------------------------------------------------
                self.player.update(self.CurrentRoom)
                if self.player.fire:
                    self.player.shoot(self.bullets,self.playsound)

                if self.player.health <= 0:
                    self.gameOver = True


            except:
               print("error")

    def end(self):
        '''Display a screen when the game is over and return playsound'''
        if self.player.health <= 0:
            self.windowSurface.fill(BLACK)
            drawText("You Died, Game over", "comicsansms", 40, self.windowSurface, self.windowSurface.get_rect().centerx, self.windowSurface.get_rect().centery, WHITE)
        else:
            image = load_image("win.png")
            self.windowSurface.blit(image, self.windowSurface.get_rect())
        pygame.display.update()
        pygame.time.wait(1000)
        return(self.playsound)

    def reset(self):
        '''Reset the game'''
        #Unuse code due to poor planning
        print("reset")
        self.player = Player()  
        self.currentmap = 0
        mapdata = readmap(self.allmaps[self.currentmap])
        self.roomlist = mapdata[0]    
        self.loc = mapdata[1]
        self.CurrentRoom = self.roomlist[self.loc[0]][self.loc[1]]
        self.gameOver = False

    def loading(self,windowSurface):
        '''A loading screen'''
        #Display a random text from the tip list
        self.windowSurface.fill(BLACK)
        num = random.randrange(0, len(TIP_LIST))
        drawText(TIP_LIST[num], "comicsansms", 20, windowSurface, windowSurface.get_rect().centerx, windowSurface.get_rect().bottom-40, WHITE)
        drawText("loading...", "comicsansms", 15, windowSurface, windowSurface.get_rect().right-30, windowSurface.get_rect().bottom-20, WHITE)
        pygame.display.update()
        pygame.time.wait(3000)

    def readmap(self, Map):
        '''Read a blue print for the map, and return the layout for the map and the starting location '''
        list = []
        for index in range(len(Map)):
            r = []
            for index2 in range(len(Map[index])):
                #Check if there are anyroom surrounding it
                up = False
                down = False
                left = False
                right = False
                if Map[index][index2] != "":
                    if Map[index+1][index2] != "":
                        down = True
                    if Map[index-1][index2] != "":
                        up = True
                    if Map[index][index2+1] != "":
                        right = True
                    if Map[index][index2-1] != "":
                        left = True

                    if Map[index][index2] in ROOM_DICT:
                        r.append(Room(up,down,left,right,ROOM_DICT[Map[index][index2]]))
                        if Map[index][index2] == "S":
                            begining = [index,index2]
                else:
                    r.append(0)
            list.append(r)
        return([list,begining])

class Tutorial(Game):
    '''A sub class inherited from game class'''
    def __init__(self, maplist,windowSurface,PlayMusic):
        super().__init__(maplist,windowSurface,PlayMusic)
        #Add object to the room
        self.roomlist[1][3].object.add(Object(self.firstaid,(400,300),1))
        self.roomlist[1][3].object.add(Object(self.painkiller,(500,300),2))
        self.roomlist[1][3].object.add(Object(self.notdrug,(600,300),3))
    def display_frame(self):
        #---------------------------Backgound--------------------------
        self.windowSurface.fill(WHITE)
        self.CurrentRoom.draw_room(self.windowSurface)
        #-----------------------------player, and enemies--------------
        self.windowSurface.blit(self.player.image, self.player.rect)
        for item in self.CurrentRoom.object:
            if item.rect.colliderect(self.player.rect):
                drawText("E", 'comicsansms', 30, self.windowSurface,self.player.rect.centerx, self.player.rect.centery - 35,BLACK)
        #--------------------------Bullet--------------------------------
        self.bullets.draw(self.windowSurface)
        self.enemybullets.draw(self.windowSurface)
        #-----------------------------info--------------------------------
        #Display tutorial text
        if self.loc == [1,1]:
            drawText("Use W A S D to move", 'comicsansms', 20, self.windowSurface, 500,100,BLACK)
            drawText("Use Mouse to aim and Mouse 1 to shoot", 'comicsansms', 20, self.windowSurface, 500,125,BLACK)
            drawText("Head to the white space between the 'walls' to get to the next room", 'comicsansms', 20, self.windowSurface, 500,150,BLACK)
        if self.loc == [1,2]:
            drawText("The red bar respresent your health", 'comicsansms', 20, self.windowSurface, 500,100,BLACK)
            drawText("The blue bar respresent your shield", 'comicsansms', 20, self.windowSurface, 500,125,BLACK)
            drawText("The light blue bar respresent your current shield", 'comicsansms', 20, self.windowSurface, 500,150,BLACK)
        if self.loc == [1,3]:
            drawText("Press E to interact with object once you get close enough", 'comicsansms', 20, self.windowSurface, 500,100,BLACK)
            drawText("First aid restore your health by 1. your health can't be larger than maxhealth", 'comicsansms', 20, self.windowSurface, 500,125,BLACK)
            drawText("Painkiller increase your maximum health by 1", 'comicsansms', 20, self.windowSurface, 500,150,BLACK)
            drawText("Non-drug substance increase your damage by 0.25", 'comicsansms', 20, self.windowSurface, 500,175,BLACK)
        if self.loc == [1,4]:
            drawText("Cats are your enemy, you have to shoot them in order to kil- make them disappear", 'comicsansms', 20, self.windowSurface, 500,100,BLACK)
            drawText("Your shield will regenerate over time", 'comicsansms', 20, self.windowSurface, 500,125,BLACK)
            drawText("The next room has some enemy", 'comicsansms', 20, self.windowSurface, 500,150,BLACK)
        if self.loc == [1,5]:
            drawText("You can not leave the room until you kil- make every cat in the room disappear", 'comicsansms', 20, self.windowSurface, 500,100,BLACK)
        if self.loc == [1,6]:
            drawText("Interact with the button to end tutorial", 'comicsansms', 20, self.windowSurface, 500,100,BLACK)
            drawText("Also ignore the text on the button", 'comicsansms', 20, self.windowSurface, 500,125,BLACK)
        #---------------------------Health and shield------------------
        self.player.hud(self.windowSurface)
        #text = "Health: " + str(self.player.max_health) + "/" + str(float(self.player.health)) 
        #drawText(text, 'comicsansms', 20, self.windowSurface, self.windowSurface.get_rect().left+100,self.windowSurface.get_rect().top+50,BLACK)
        #text = "Shield: " + str(self.player.max_shield) + "/" + str(float(self.player.shield))
        #drawText(text, 'comicsansms', 20, self.windowSurface, self.windowSurface.get_rect().left+100,self.windowSurface.get_rect().top+75,BLACK)
        pygame.display.update()
    def end(self):
        #Return playsound
        return(self.playsound)

def main():
    '''The main program'''
    #--------------------------Initialize the window------------------------------
    print('no idea v1.0.6')
    pygame.init()
    mainClock = pygame.time.Clock()
    #Set up the windowSurface
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('HELP!!')

    #--------------------------Start screen--------------------------------
    PlayMusic = True                                            #Play music
    start_screen(windowSurface)
    #---------------------------Main manual--------------------------------
    while True:
        output = 0                                              #Output from main_manual
        pygame.mixer.music.load('Kahoot Lobby Music.ogg')       #Main manual music
        pygame.display.set_caption('Main manual')

        output = main_manual(windowSurface, PlayMusic)

        user = output[0]
        PlayMusic = output[1]
        if user == 1:
            pygame.display.set_caption('Game')
            game = Game(MAPS,windowSurface,PlayMusic)
        elif user == 2:
            pygame.display.set_caption('Tutorial')
            game = Tutorial([TUTORIAL],windowSurface,PlayMusic)
        game.loading(windowSurface)
    #---------------------------Game loop--------------------------------
        while not game.gameOver:
            game.process_events()
            game.run_logic()
            game.display_frame()
            mainClock.tick(FRAMERATE)
        PlayMusic = game.end()

if __name__ == '__main__':
    main()






#------------------------------unuse code----------------------------------------------
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

        if explosion:

            pass

        elif currenttime-self.starttime < self.flytime:
            self.currentx += self.speed*math.cos(self.angle)
            self.currenty += self.speed*math.sin(self.angle)
            self.rect.centerx = self.currentx
            self.rect.centery = self.currenty
            if self.rect.bottom > WINDOWHEIGHT -25 or self.rect.top < 25 or self.rect.left < 25 or self.rect.right > WINDOWWIDTH-25:
                self.explosion = True
        else:
            self.explosion = True
            self.kill()
