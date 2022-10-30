import GameState
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

class Tutorial_State(GameState.Game_State):
    '''A sub class inherited from game class'''
    def __init__(self,windowSurface,PlayMusic):
        self.windowSurface = windowSurface                           
        #-----------------------Music-----------------------------
        self.halfhealth = False                                      #If the player is at helf health
        self.playsound = PlayMusic                                   #Play sound and music
        pygame.mixer.music.load(Config.SOUNDPATH +'Kahoot! 20 Second Countdown #3 Music.ogg')
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
        self.allmaps = [RoomsDatas.TUTORIAL]                          #A list contain all the map
        self.currentmap = 0                                           #The current map the player is in
        mapdata = self.readmap(self.allmaps[self.currentmap])         #Date from readmap
        self.roomlist = mapdata[0]                                    #All the room in the maps
        self.loc = mapdata[1]                                         #The current location for the player
        self.CurrentRoom = self.roomlist[self.loc[0]][self.loc[1]]    #The room plyer is in
        #---------------------------Game loop--------------------------
        self.gameOver = False                                         #Is the game over

        #Add object to the room
        self.roomlist[1][3].object.add(Items.firstaid(self.firstaid,(400,300)))
        self.roomlist[1][3].object.add(Items.painkiller(self.painkiller,(500,300)))
        self.roomlist[1][3].object.add(Items.notdrug(self.notdrug,(600,300)))

    def display_frame(self):
        #---------------------------Backgound--------------------------
        self.windowSurface.fill(Config.WHITE)
        self.CurrentRoom.draw_room(self.windowSurface)
        #---------------------------info---------------------------------
        #Display tutorial text
        if self.loc == [1,1]:
            utility.drawText("Use W A S D to move", 'comicsansms', 20, self.windowSurface, 500,100,Config.BLACK)
            utility.drawText("Use Mouse to aim and Mouse 1 to shoot", 'comicsansms', 20, self.windowSurface, 500, 125,Config.BLACK)
            utility.drawText("Head to the white space between the 'walls' to get to the next room", 'comicsansms', 20, self.windowSurface, 500,150,Config.BLACK)
        if self.loc == [1,2]:
            utility.drawText("The red bar respresent your health", 'comicsansms', 20, self.windowSurface, 500, 100,Config.BLACK)
            utility.drawText("The blue bar respresent your shield", 'comicsansms', 20, self.windowSurface, 500, 125,Config.BLACK)
            utility.drawText("The light blue bar respresent your current shield", 'comicsansms', 20, self.windowSurface, 500, 150,Config.BLACK)
        if self.loc == [1,3]:
            utility.drawText("Press E to interact with object once you get close enough", 'comicsansms', 20, self.windowSurface, 500,100,Config.BLACK)
            utility.drawText("First aid restore your health by 1. your health can't be larger than maxhealth", 'comicsansms', 20, self.windowSurface, 500,125,Config.BLACK)
            utility.drawText("Painkiller increase your maximum health by 1", 'comicsansms', 20, self.windowSurface, 500,150,Config.BLACK)
            utility.drawText("Non-drug substance does nothing", 'comicsansms', 20, self.windowSurface, 500,175,Config.BLACK)
        if self.loc == [1,4]:
            utility.drawText("Cats are your enemy, you have to shoot them in order to kil- make them disappear", 'comicsansms', 20, self.windowSurface, 500,100,Config.BLACK)
            utility.drawText("Your shield will regenerate over time", 'comicsansms', 20, self.windowSurface, 500,125,Config.BLACK)
            utility.drawText("The next room has some enemy", 'comicsansms', 20, self.windowSurface, 500,150,Config.BLACK)
        if self.loc == [1,5]:
            utility.drawText("You can not leave the room until you kil- make every cat in the room disappear", 'comicsansms', 20, self.windowSurface, 500,100,Config.BLACK)
        if self.loc == [1,6]:
            utility.drawText("Interact with the button to end tutorial", 'comicsansms', 20, self.windowSurface, 500,100,Config.BLACK)
            utility.drawText("Also ignore the text on the button", 'comicsansms', 20, self.windowSurface, 500,125,Config.BLACK)
        #-----------------------------player, and enemies--------------
        #pygame.draw.rect(self.windowSurface, config.RED, self.player.rect) #Hit box
        self.player.draw()
        for item in self.CurrentRoom.object:
            if item.rect.colliderect(self.player.rect):
                utility.drawText("E", 'comicsansms', 30, self.windowSurface,self.player.rect.centerx, self.player.rect.centery - 35,Config.BLACK)
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
