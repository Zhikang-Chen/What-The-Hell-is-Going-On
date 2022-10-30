#A program use to test stuff
import pygame, os, main
from pygame.locals import *

#Size of the screen
WINDOWWIDTH = 1000 
WINDOWHEIGHT = 600

#Colours
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255,000,000)

FRAMERATE = 40


def process_event():
      for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    os._exit(1)

                    
def main():
      #----------------------init----------------------------------------
      print('blank test')
      pygame.init()
      mainClock = pygame.time.Clock()
      windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
      pygame.display.set_caption('HELP!!')
      #---------------------program------------------------------------

      
      #---------------------loop---------------------------------------
      while True:
            windowSurface.fill(WHITE)

            pygame.display.update()


            
            process_event()
            mainClock.tick(FRAMERATE)
main()
