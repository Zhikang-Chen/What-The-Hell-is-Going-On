import State
import GameState
import TutorialState
import pygame
import Config as config
import Utility as utility
import os

from pygame.locals import *

class Start_State(State.State):
    def __init__(self, windowSurface, PlayMusic):
            self.windowSurface = windowSurface
            self.windowSurface.fill(config.WHITE)
            self.image = utility.load_image("the hack is going on v7.png")

            pygame.mixer.music.load(config.SOUNDPATH +'Kahoot Lobby Music.ogg')
            self.PlayMusic = PlayMusic
            self.Music_on = utility.load_image("sound on.png")
            self.Music_off = utility.load_image("sound off.png")
            self.music_rect = self.Music_on.get_rect()
            self.music_rect.topleft = (900,500)
            self.mouse_rect = Rect((0,0),(1,1))

            self.rect1 = utility.drawText("1. Start game", "comicsansms", 40, self.windowSurface, self.windowSurface.get_rect().left+20, self.windowSurface.get_rect().top+150, config.BLACK,False)
            self.rect2 = utility.drawText("2. Tutorial", "comicsansms", 40, self.windowSurface, self.windowSurface.get_rect().left+20, self.windowSurface.get_rect().top+225, config.BLACK,False)
            self.rect3 = utility.drawText("3. Setting", "comicsansms", 40, self.windowSurface, self.windowSurface.get_rect().left+20, self.windowSurface.get_rect().top+300, config.BLACK,False)
            self.rect4 = utility.drawText("4. Exit", "comicsansms", 40, self.windowSurface, self.windowSurface.get_rect().left+20, self.windowSurface.get_rect().top+375, config.BLACK,False)
            #self.change_state(Game_State(windowSurface,PlayMusic))

    def display_frame(self):
        self.windowSurface.blit(self.image, self.windowSurface.get_rect())
        utility.drawText("What The H*ck Is Going On", "comicsansms", 50, self.windowSurface, self.windowSurface.get_rect().centerx-170, self.windowSurface.get_rect().top+60, config.BLACK)
        utility.drawText("A mostly text base bullet hell dungeon crawl game without the fun part", "comicsansms", 20, self.windowSurface, self.windowSurface.get_rect().centerx-170, self.windowSurface.get_rect().top+105, config.BLACK)
        utility.drawText("1. Start game", "comicsansms", 40, self.windowSurface, self.windowSurface.get_rect().left+20, self.windowSurface.get_rect().top+150, config.BLACK,False)
        utility.drawText("2. Tutorial", "comicsansms", 40, self.windowSurface, self.windowSurface.get_rect().left+20, self.windowSurface.get_rect().top+225, config.BLACK,False)
        utility.drawText("3. Setting", "comicsansms", 40, self.windowSurface, self.windowSurface.get_rect().left+20, self.windowSurface.get_rect().top+300, config.BLACK,False)
        utility.drawText("4. Exit", "comicsansms", 40, self.windowSurface, self.windowSurface.get_rect().left+20, self.windowSurface.get_rect().top+375, config.BLACK,False)

        if self.PlayMusic:
            self.windowSurface.blit(self.Music_on, self.music_rect)
        else:
            self.windowSurface.blit(self.Music_off, self.music_rect)

        sel = pygame.Surface((260,60))
        sel.set_alpha(128) 
        sel.fill(config.WHITE)  

        if self.mouse_rect.colliderect(self.rect1):
            self.windowSurface.blit(sel, self.rect1)
        elif self.mouse_rect.colliderect(self.rect2):
            self.windowSurface.blit(sel, self.rect2)
        elif self.mouse_rect.colliderect(self.rect3):
            self.windowSurface.blit(sel, self.rect3)
        elif self.mouse_rect.colliderect(self.rect4):
            self.windowSurface.blit(sel, self.rect4)

        pygame.display.update()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                utility.terminate()
            elif event.type == KEYUP:
                if event.key == ord('1'):
                     #Change State here
                     self.change_state(GameState.Game_State(self.windowSurface, self.PlayMusic))
                     pass
                elif event.key == ord('2'):
                     #Change State here
                     self.change_state(TutorialState.Tutorial_State(self.windowSurface, self.PlayMusic))
                     pass
                elif event.key == ord('3'):
                    utility.terminate()
                elif event.key == ord('m'):
                    if self.PlayMusic:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    self.PlayMusic = not self.PlayMusic
            elif event.type == MOUSEBUTTONDOWN:
                if self.mouse_rect.colliderect(self.rect1):
                    if pygame.mouse.get_pressed()[0]:
                        #Change State here
                        self.change_state(GameState.Game_State(self.windowSurface, self.PlayMusic))
                        pass
                elif self.mouse_rect.colliderect(self.rect2):
                    if pygame.mouse.get_pressed()[0]:
                        #Change State here
                        self.change_state(TutorialState.Tutorial_State(self.windowSurface, self.PlayMusic))
                        pass
                elif self.mouse_rect.colliderect(self.rect3):
                    if pygame.mouse.get_pressed()[0]:
                        pass
                elif self.mouse_rect.colliderect(self.rect4):
                    if pygame.mouse.get_pressed()[0]:
                        utility.terminate()
                elif self.mouse_rect.colliderect(self.music_rect):
                    if pygame.mouse.get_pressed()[0]:
                        if self.PlayMusic:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                        self.PlayMusic = not self.PlayMusic

    def run_logic(self):
        #Get location for the mouse and check if it's colliding with the text, if so change colour of the text
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_rect.center = mouse_pos

        if not pygame.mixer.music.get_busy() and self.PlayMusic: 
            pygame.mixer.music.play(-1, 0.0)

    def start_screen(self):
        '''The start screen for the game'''
        self.windowSurface.fill(config.WHITE)
        image = utility.load_image("the hack is going on v6.png")
        self.windowSurface.blit(image,  self.windowSurface.get_rect())
        utility.drawText("Press anything to begin", "comicsansms", 40,  self.windowSurface,  self.windowSurface.get_rect().centerx-175,  self.windowSurface.get_rect().centery-40, config.BLACK)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    utility.terminate()
                elif event.type == KEYUP:
                    return()
