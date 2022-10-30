import pygame , EnemyClass as enemy, Utility as u, Items, EnemyData, Config
from pygame.locals import *

class Room(pygame.sprite.Sprite):
    '''Read blue print and create a room with it'''
    def __init__(self, upexit,downexit,leftexit,rightexit, blueprint):

        #200*50
        #-------------walls----------------------
        self.wall = u.load_image("wall side.png")                 #Sprite for the wall
        self.wall2 = u.load_image("other wall.png")               #Sprite for the wall

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
        door = u.load_image("door.png")                           #Sprite for the door
        door2 = u.load_image("door2.png")                         #Sprite for the door
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
                self.enemies.add(enemy.Boss())
            elif idk[0] == 'B':
                self.object.add(Items.button("button.png",idk[1]))
            else:
                self.spawn(EnemyData.enemy_dict[idk[0]],idk[1])

    def draw_room(self, windowSurface):
        #Draw everything in the room

        #Draw the four walls
        windowSurface.blit(self.wall2, self.leftwall)
        windowSurface.blit(self.wall2, self.rightwall)
        windowSurface.blit(self.wall, self.topwall)
        windowSurface.blit(self.wall, self.bottomwall)

        #Draw each exit 
        for exit in self.exits.values():
            pygame.draw.rect(windowSurface,Config.WHITE,exit)

        #Draw each doors
        for door in self.doors.values():
            windowSurface.blit(door[0], door[1])


        self.object.draw(windowSurface)                 #Draw all the object in the room
        #for enemy in self.enemies:
            #pygame.draw.rect(windowSurface,Config.RED,enemy.rect)
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

    def spawn(self, id, loc = None):
        '''Read a list and spwan enemy with the stat from the list'''
        try:
            if id['type'] == 'melee':
                an_enemy = enemy.Enemy(id['sprite'],id['health'],id['speed'],id['melee damage'],id['movement'],loc)
            elif id['type'] == 'range':
                an_enemy = enemy.Range_enemy(id['sprite'],id['health'],id['speed'],id['melee damage'],id['movement'],id['bullet sprite']
                                                ,id['range damage'],id['fire speed'],id['fire time'],id['cool down'],id['bullet speed'],loc)

            self.enemies.add(an_enemy)
        except:
            print('Error happen on spawn')
