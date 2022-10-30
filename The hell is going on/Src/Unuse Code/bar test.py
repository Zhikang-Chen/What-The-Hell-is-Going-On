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

class bar(pygame.sprite.Sprite):
    def __init__(self,windowSurface,location,size,difference,max_value,value):
        self.windowSurface = windowSurface
        self.value = value
        self.max_value = max_value
        self.location = location
        self.size = size
        self.difference = difference
        self.bar_background = pygame.Rect(self.location,self.size)
        self.current_bar = pygame.Rect((self.location[0]+1,self.location[1]+1),(self.value*((self.size[0]-self.difference)/self.max_value),self.size[1]-self.difference))

    def draw(self):
        pygame.draw.rect(self.windowSurface,(96,96,96),self.bar_background)
        pygame.draw.rect(self.windowSurface,(0,148,255),self.current_bar)

    def update(self):
        self.bar_background = pygame.Rect(self.location,self.size)
        self.current_bar = pygame.Rect((self.location[0]+1,self.location[1]+1),(self.value*((self.size[0]-self.difference)/self.max_value),self.size[1]-self.difference))





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
      stuff = bar(windowSurface,(500,300),(200,12),2,50,25)
      
      #---------------------loop---------------------------------------
      while True:
            windowSurface.fill(WHITE)
            stuff.draw()
            stuff.update()
            pygame.display.update()


            
            process_event()
            mainClock.tick(FRAMERATE)
main()
