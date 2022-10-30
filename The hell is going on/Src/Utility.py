#A set of utility use in game
import pygame, os , math, Config

def terminate():
    '''Terminate program '''
    pygame.quit()
    os._exit(1)

def load_image(filename, path = Config.SPRITEPATH):
    '''Load an image from the file name given'''
    try:
        image = pygame.image.load(path + filename)
    except:
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

def load_sound(filename, volume = None, path = Config.SOUNDPATH):
    '''Load a sound from the file name given'''
    try:
        sound = pygame.mixer.Sound(path + filename)
    except:
        sound = pygame.mixer.Sound(filename)

    if volume is None:
        volume = Config.volume

    sound.set_volume(volume)
    return(sound)