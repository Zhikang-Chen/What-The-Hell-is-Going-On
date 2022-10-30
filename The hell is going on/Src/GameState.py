import State
import pygame
import Config as config
import PlayerClass as Player
import math
import random
import WeaponStat as weapons
import EnemyClass as enemy
import Utility as utility
import RoomsDatas
import Projectile as projectile
import Items
import RoomClass
import os


from pygame.locals import *

TIP_LIST = ["You can shut this annoying music off by pressing 'M'",
            "Insert motivational quote here",
            "I created this loading screen just to annoy people",
            "Dash is overpower",
            "The best way to win is just to spam mouse 1",
            "No cats were harmed in the making of this game",
            "Yes, the bgm is kahoot music",
            "You can beat this game within 9 minutes",
            "First aid kit can heal you",
            "Shoot at the cats until they are dead. I mean gone",
            "Use W A S D to move",
            "Use mouse to shoot",
            "Another one bits the dust",
            "Use space to dash",
            "Non-drug substance(syringe thingy) can increase your damage (no longer work)",
            "Painkiller can increase your max health",
            "Remember to buy the nonexistent weapon DLC which only cost $2.99",
            "YOU WON'T LAST 5 MINUTES PLAYING THIS!",
            "We all live in a yellow subarine. *submarine"] #A list of tip that will be display on loading screen

class Game_State(State.State):
    '''The game class'''
    def __init__(self, windowSurface, PlayMusic):
        self.windowSurface = windowSurface                           
        #-----------------------Music-----------------------------
        self.halfhealth = False                                      #If the player is at helf health
        self.playsound = PlayMusic                                   #Play sound and music
        pygame.mixer.music.load(config.SOUNDPATH +'Kahoot! 20 Second Countdown #3 Music.ogg')
        #------------------------Sound----------------------------
        #Pre-loaded sound
        self.record_scratch = utility.load_sound('record scratch sound.wav')
        self.catdeath = utility.load_sound('dead.wav')
        self.soundlist = [self.record_scratch,self.catdeath ]
        #--------------------------sprite--------------------------
        #Pre-loaded sprite
        self.firstaid = utility.load_image("First aid.png")
        self.painkiller = utility.load_image("painkiller.png")
        self.notdrug = utility.load_image("not drug.png")
        self.bullet = utility.load_image("player_bullet.png")
        self.healthbar = utility.load_image('health bar.png')
        self.healthbar2 = utility.load_image('empty health.png')
        #--------------------------Player--------------------------
        self.player = Player.player(self.windowSurface)               #The player
        #--------------------------Group--------------------------
        self.bullets = pygame.sprite.Group()                          #Group for player's bullet
        self.enemybullets = pygame.sprite.Group()                     #Group for enemies' bullet
        #---------------------------Maps & room------------------
        self.allmaps = RoomsDatas.MAPS                                #A list contain all the map
        self.currentmap = 0                                           #The current map the player is in
        mapdata = self.readmap(self.allmaps[self.currentmap])         #Date from readmap
        self.roomlist = mapdata[0]                                    #All the room in the maps
        self.loc = mapdata[1]                                         #The current location for the player
        self.CurrentRoom = self.roomlist[self.loc[0]][self.loc[1]]    #The room plyer is in
        #---------------------------Game loop--------------------------
        self.gameOver = False                                         #Is the game over

    def display_frame(self):
        '''Display the current frame in the game'''
        #---------------------------Backgound--------------------------
        self.windowSurface.fill(config.WHITE)
        self.CurrentRoom.draw_room(self.windowSurface)

        #print(config.volume)
        if self.playsound:
            text = 'Volume: ' + str(int(config.volume*100))
        else:
            text = 'Volume: 0'

        utility.drawText(text, 'comicsansms', 20, self.windowSurface, self.windowSurface.get_rect().right-100, self.windowSurface.get_rect().bottom-50 ,config.BLACK)

        #-----------------------------player, and enemies--------------
        #pygame.draw.rect(self.windowSurface, config.RED, self.player.rect) #Hit box
        #self.windowSurface.blit(self.player.image, self.player.rect)
        self.player.draw()
        for item in self.CurrentRoom.object:
            if item.rect.colliderect(self.player.rect):
                utility.drawText("E", 'comicsansms', 30, self.windowSurface,self.player.rect.centerx, self.player.rect.centery - 35,config.BLACK)
        #--------------------------Bullet--------------------------------
        self.bullets.draw(self.windowSurface)
        self.enemybullets.draw(self.windowSurface)
        #for bullet in self.bullets:
            #pygame.draw.rect(self.windowSurface, config.RED, bullet.rect)

        #for baddy in self.CurrentRoom.enemies:
            #pygame.draw.rect(windowSurface, config.RED, baddy.rect)
            #pygame.draw.rect(windowSurface, config.RED, baddy.wavepoint)
        #---------------------------Health and shield------------------
        self.player.hud()
        #text = "Health: " + str(self.player.max_health) + "/" + str(float(self.player.health)) 
        #u.drawText(text, 'comicsansms', 20, self.windowSurface, self.windowSurface.get_rect().left+100,self.windowSurface.get_rect().top+50,config.BLACK)
        #text = "Shield: " + str(self.player.max_shield) + "/" + str(float(self.player.shield))
        #u.drawText(text, 'comicsansms', 20, self.windowSurface, self.windowSurface.get_rect().left+100,self.windowSurface.get_rect().top+75,config.BLACK)
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
                        self.player.move_left = True
                        #self.player.moveRight = False
                    elif event.key == K_RIGHT or event.key == ord('d'):
                        self.player.move_right = True
                        #self.player.moveLeft = False
                    elif event.key == K_UP or event.key == ord('w'):
                        self.player.move_up = True
                        #self.player.moveDown=False
                    elif event.key == K_DOWN or event.key == ord('s'):
                        self.player.move_down = True
                        #self.player.moveUp = False 
                    elif event.key == K_SPACE or event.key == ord(' '):
                        self.player.dash = True
                    elif event.key == K_e or event.key == ord('e'):
                        self.player.use = True
                    elif event.key == K_c or event.key == ord('c'):
                        self.player.change_weapon()

                    elif event.key == K_EQUALS or event.key == ord('='):
                        if config.volume < 1:
                            config.volume =  round(config.volume + 0.1,1)
                            self.playsound = True
                            self.update_voulme()
                    elif event.key == K_MINUS or event.key == ord('-'):
                        if config.volume > 0:
                            config.volume =  round(config.volume - 0.1,1)
                            self.playsound = True
                            self.update_voulme()


            elif event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        os._exit(1)
                    # the player has stopped moving
                    elif event.key == K_LEFT or event.key == ord('a'):
                        self.player.move_left = False
                    elif event.key == K_RIGHT or event.key == ord('d'):
                        self.player.move_right = False
                    elif event.key == K_UP or event.key == ord('w'):
                        self.player.move_up = False
                    elif event.key == K_DOWN or event.key == ord('s'):
                        self.player.move_down = False
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
                elif event.button == 4:
                    #print('up')
                    self.player.change_weapon(False)
                elif event.button == 5:
                    #print('down')
                    self.player.change_weapon(True)

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.player.fire = False

    def run_logic(self):
        '''Game logic'''
        if not self.gameOver:
            #try:
                #---------------------------------------------------Music and sound---------------------------------------------------
                #Change music depend on player's health
                if self.player.health < self.player.max_health/2 and not self.halfhealth:
                    if self.playsound:
                        self.record_scratch.play()
                    pygame.mixer.music.load(config.SOUNDPATH +'Kahoot! 30 Second Countdown #1 Music (extended).ogg')
                    self.halfhealth = True
                elif self.player.health >= self.player.max_health/2 and self.halfhealth:
                    if self.playsound:
                        self.record_scratch.play()
                    self.record_scratch.play()
                    pygame.mixer.music.load(config.SOUNDPATH +'Kahoot! 20 Second Countdown #3 Music.ogg')
                    self.halfhealth = False
                #Play music if the music isn't playing and playsound is true
                if not pygame.mixer.music.get_busy() and self.playsound: 
                    pygame.mixer.music.play(-1, 0.0)


                #---------------------------------------------------Change room check---------------------------------------
                #Check if the player has collide with the exit and change room if the player does collide with the exit
                self.CurrentRoom.doorlogic()
                if self.CurrentRoom.open:
                    self.player.shield_regen_time = 1
                    exitcollide = self.player.rect.collidedict(self.CurrentRoom.exits,1)
                    if exitcollide is not None:
                        if exitcollide[0] == "upexit":
                            self.loc[0]-=1
                            self.player.rect.centery = config.WINDOWHEIGHT-75
                        if exitcollide[0] == "downexit":
                            self.loc[0]+=1
                            self.player.rect.centery = 75
                        if exitcollide[0] == "rightexit":
                            self.loc[1]+=1
                            self.player.rect.centerx = 75
                        if exitcollide[0] == "leftexit":
                            self.loc[1]-=1
                            self.player.rect.centerx = config.WINDOWWIDTH - 75
                        #Change room and clear out all the bullet
                        self.CurrentRoom = self.roomlist[self.loc[0]][self.loc[1]]
                        self.bullets.empty()
                        self.enemybullets.empty()
                        self.player.shield_regen_time = 8
                #-----------------------------------------------------Enemy logic------------------------------------------
                for enemy in self.CurrentRoom.enemies:
                    if enemy.health <= 0:
                        #Spawn and random object when they die
                        if self.playsound:
                            self.catdeath.play()
                        number = random.randrange(0,100)
                        if number <= 10:
                            self.CurrentRoom.object.add(Items.firstaid(self.firstaid,enemy.rect.center))
                        elif number >= 90 and number <= 93:
                            self.CurrentRoom.object.add(Items.painkiller(self.painkiller,enemy.rect.center))
                        elif number >= 80 and number <= 83:
                            self.CurrentRoom.object.add(Items.notdrug(self.notdrug,enemy.rect.center))
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
                            if type(bullet) is projectile.Bullet:
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

            #except:
               #print("error")

    def reset(self):
        '''Reset the game'''
        #Unuse code due to poor planning
        print("reset")
        self.player = Player.Player()
        self.currentmap = 0
        mapdata = self.readmap(self.allmaps[self.currentmap])
        self.roomlist = mapdata[0]    
        self.loc = mapdata[1]
        self.CurrentRoom = self.roomlist[self.loc[0]][self.loc[1]]
        self.gameOver = False

    def loading(self,windowSurface):
        '''A loading screen'''
        #Display a random text from the tip list
        self.windowSurface.fill(config.BLACK)
        num = random.randrange(0, len(TIP_LIST))
        utility.drawText(TIP_LIST[num], "comicsansms", 20, windowSurface, windowSurface.get_rect().centerx, windowSurface.get_rect().bottom-40, config.WHITE)
        utility.drawText("loading...", "comicsansms", 15, windowSurface, windowSurface.get_rect().right-30, windowSurface.get_rect().bottom-20, config.WHITE)
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

                    if Map[index][index2] in RoomsDatas.ROOM_DICT:
                        r.append(RoomClass.Room(up,down,left,right,RoomsDatas.ROOM_DICT[Map[index][index2]]))
                        if Map[index][index2] == "S":
                            begining = [index,index2]
                else:
                    r.append(0)
            list.append(r)
        return([list,begining])

    def update_voulme(self):
        pygame.mixer.music.set_volume(config.volume)
        for sound in self.soundlist:
            sound.set_volume(config.volume)

        for sound in self.player.stored_sound.values():
            sound.set_volume(config.volume)
