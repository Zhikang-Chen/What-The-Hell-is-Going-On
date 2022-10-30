import pygame, time, utility as u, weaponstat as weapons, projectile, config, math
from pygame.locals import *

class player():
    '''Character the user control'''
    def __init__(self,windowSurface):
        self.windowSurface = windowSurface
        self.healthbar = u.load_image('health bar.png')           #sprite for health
        self.healthbar2 = u.load_image('empty health.png')        #sprite for empty health
        self.unchage_image = u.load_image("play_hand_handgun v3.png")     #The unrotated image
        self.image = self.unchage_image.copy()                  #Sprite for the player
        self.rect = self.image.get_rect()                       #A Rect from the sprite
        self.rect.center = (config.WINDOWWIDTH//2, config.WINDOWHEIGHT//2)    
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
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
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
                bulletgroup.add(projectile.Bullet(self.rect, pygame.mouse.get_pos(),self.currentweapon['bulletspeed'],self.currentweapon['damage'],self.currentweapon['bulletsprite']))
            
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
        u.drawText(self.currentweapon['name'], 'comicsansms', 20, self.windowSurface, 50,vpos,config.BLACK,False)

    def change(self):
        self.num += 1
        if self.num == len(self.weapons):
            self.num = 0
        self.currentweapon = weapons.stats[self.weapons[self.num]]

    def draw(self):
        #Draw player and their bullet 
        pygame.draw.rect(self.windowSurface, config.RED, self.rect)
        self.windowSurface.blit(self.image, self.rect)
 
