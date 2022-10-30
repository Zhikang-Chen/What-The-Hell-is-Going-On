#This file contain weapon stat for what the hell is going on
import pygame, math, Projectile
from pygame.locals import *

def shotgun(bulletgroup,player,windowSurface):
    #Function for shot gun
    target = pygame.mouse.get_pos()
    angle = math.atan2(target[1]-player.weaponrect.centery,target[0]-player.weaponrect.centerx) 
    d = 200
    allTarget = [(d*math.cos(angle) + player.weaponrect.centerx , d*math.sin(angle) + player.weaponrect.centery),
                  (d*math.cos(angle+0.12) + player.weaponrect.centerx , d*math.sin(angle+0.12) + player.weaponrect.centery),
                  (d*math.cos(angle-0.12) + player.weaponrect.centerx , d*math.sin(angle-0.12) + player.weaponrect.centery),
                  (d*math.cos(angle+0.24) + player.weaponrect.centerx , d*math.sin(angle+0.24) + player.weaponrect.centery),
                  (d*math.cos(angle-0.24) + player.weaponrect.centerx , d*math.sin(angle-0.24) + player.weaponrect.centery)]

    for target in allTarget:
        bulletgroup.add(Projectile.Bullet(player.weaponrect, target,player.current_weapon['bulletspeed'],player.current_weapon['damage'],player.current_weapon['bulletsprite']))

def machina(bulletgroup,player,windowSurface):
    target = pygame.mouse.get_pos()
    bulletgroup.add(Projectile.laser(player.weaponrect,target,1,10,windowSurface))
    
stats = {
            'weapon':{
                      'name':'full weapon name',
                      'damage':1,
                      'bulletspeed':30,
                      'sprite':'',
                      'bulletsprite':'player_bullet.png',
                      'firespeed':0,
                      'auto':False,
                      'firesound':'bang.wav'},

            'pistol':{
                      'name':'Pistol',
                      'damage':0.25,
                      'bulletspeed':30,
                      'sprite':'',
                      'bulletsprite':'player_bullet.png',
                      'firespeed':0,
                      'auto':False,
                      'firesound':'bang.wav'},

            'spas':{
                      'name':'Spas-12',
                      'damage':0.5,
                      'bulletspeed':15,
                      'sprite':'',
                      'bulletsprite':'player_bullet.png',
                      'firespeed':1,
                      'firesound':'bang.wav',
                      'auto': False,
                      'special': shotgun},

            'm16':{
                      'name':'M16A1',
                      'damage':1.5,
                      'bulletspeed':20,
                      'sprite':'',
                      'bulletsprite':'player_bullet.png',
                      'firespeed':0.25,
                      'auto':True,
                      'firesound':'bang.wav'},

            'python':{
                      'name':'Colt Python',
                      'damage':2.5,
                      'bulletspeed':30,
                      'sprite':'',
                      'bulletsprite':'player_bullet.png',
                      'firespeed':1,
                      'auto':False,
                      'firesound':'bang.wav'},

            'm1':{
                      'name':'M1 Garand',
                      'damage':2,
                      'bulletspeed':30,
                      'sprite':'',
                      'bulletsprite':'player_bullet.png',
                      'firespeed':0.25,
                      'auto':False,
                      'firesound': 'bang.wav'},

            'machina':{
                      'name':'Machina',
                      'damage':5,
                      'bulletspeed':30,
                      'sprite':'',
                      'bulletsprite':'lazer.png',
                      'firespeed':2,
                      'auto':False,
                      'firesound':'PEW.wav',
                      'special':machina}
            }
