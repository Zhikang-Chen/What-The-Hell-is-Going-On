#This game was written by Ken Chen
#The game is a text base top side view shooter
#TD: Even more clean up
import pygame
import os
import time

import Config as config
import StartState
import GameState
import TutorialState

from pygame.locals import *
        


def main():
    '''The main program'''
    #--------------------------Initialize the window------------------------------
    print('no idea v1.0.7')
    pygame.init()
    mainClock = pygame.time.Clock()
    dt = pygame.time.Clock()
    #Set up the windowSurface
    windowSurface = pygame.display.set_mode((config.WINDOWWIDTH, config.WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('HELP!!')

    #--------------------------Start screen--------------------------------
    PlayMusic = True                                                             #Play music
    pygame.mixer.music.set_volume(config.volume)                                  
    #start_screen(windowSurface)
    #---------------------------Main manual--------------------------------

    current_state = StartState.Start_State(windowSurface,PlayMusic)
    current_state.start_screen();
    while True:
    #---------------------------Game loop--------------------------------
        while True:
            current_state.process_events()
            current_state.run_logic()
            current_state.display_frame()
            mainClock.tick(config.FRAMERATE)
            if(current_state.change_state == True):
                next_state = current_state.next_state
                current_state = next_state


        PlayMusic = current_state.end()

if __name__ == '__main__':
    main()
