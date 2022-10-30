import pygame, time, Utility as u, WeaponStat as weapons, Projectile as projectile, Config, math
from pygame.locals import *

class player():
    '''Character the user control'''
    def __init__(self,windowSurface):
        self.windowSurface = windowSurface
        self.healthbar = u.load_image('health bar.png')           #sprite for health
        self.healthbar2 = u.load_image('empty health.png')        #sprite for empty health

        self.image = u.load_image("player.png")         
        self.weapon = u.load_image("weapon.png")      
        self.unchange_weapon = self.weapon.copy()

        self.rect = self.image.get_rect()                       #A Rect from the sprite
        self.rect.center = (Config.WINDOWWIDTH//2, Config.WINDOWHEIGHT//2)   
        
        self.weaponrect = self.weapon.get_rect()                #A rect indicate where the bullet will spawn
        self.weaponrect.center = (self.rect.centerx,self.rect.centery-30)

        self.move_left = False                                   #The direction the player is moving in
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.dash = False                                       #Dash 
        self.use = False                                        #E
        self.dash_distance = 150                                 #The distance of the dash
        self.dash_cooldown = time.time()                         #A cool down timer for the dash
        self.speed = 10                                         #Number of pixel the player will move in
        self.max_health = 5                                     #Maxium amount of health the player can have
        self.health = 5.0                                       #The current health the play has
        self.max_shield = 5                                     #Maxium amount of shield the player can have
        self.shield = 5.0                                       #The current shield the play has
        self.shield_cooldown = time.time()                      #A cool down timer for the resignation of shield
        self.shield_regen_time = 8                              #The amount of time for shield to regen
        self.damage_cooldown = time.time()                       #A cool down timer for player to take damage
        self.shoot_timer = time.time()                           #A timer for player to shoot
        self.damage = 1                                         #Damage the player will deal
        self.change_level = False                               #Change lever
        self.fire = False                                       #Shoot a bullet use for auto weapons

        self.weapons = ['pistol','spas','m16','python','m1','machina']
        #self.weapons = ['pistol']
        self.weapon_index = 0
        self.current_weapon = weapons.stats[self.weapons[self.weapon_index]]
        self.stored_sound = {}

    def update(self, room):
        #Update the position and the direction player is facing
        cooldown = time.time()

        if self.move_up and self.rect.top > room.topwall.bottom:
            self.rect.top -= self.speed
            if self.dash and cooldown - self.dash_cooldown  >= 0.5:
                self.rect.top -= self.dash_distance
                self.dash_cooldown = time.time()
            while self.rect.top < room.topwall.bottom:
                self.rect.bottom += 1

        if self.move_down and self.rect.bottom < room.bottomwall.top:
            self.rect.bottom += self.speed
            if self.dash and cooldown - self.dash_cooldown  >= 0.5:
                self.rect.bottom += self.dash_distance
                self.dash_cooldown = time.time()
            while self.rect.bottom > room.bottomwall.top:
                self.rect.bottom -= 1

        if self.move_left and self.rect.left > room.leftwall.right:
            self.rect.left -= self.speed
            if self.dash and cooldown - self.dash_cooldown  >= 0.5:
                self.rect.left -= self.dash_distance
                self.dash_cooldown = time.time()
            while self.rect.left < room.leftwall.right:
                self.rect.left += 1

        if self.move_right and self.rect.right < room.rightwall.left:
            self.rect.right += self.speed
            if self.dash and cooldown - self.dash_cooldown  >= 0.5:
                self.rect.right += self.dash_distance
                self.dash_cooldown = time.time()
            while self.rect.right > room.rightwall.left:
                self.rect.right -= 1

        #Regenerate the shield each 8 second, the timer will reset when the player get hurt
        if cooldown - self.shield_cooldown >= self.shield_regen_time and self.shield < self.max_shield:
            self.shield += 1
            self.shield_cooldown = time.time()
            if self.shield > self.max_shield:
                self.shield -= self.shield - self.max_shield

        #Rotate the spite to where the mouse is
        currentx = self.rect.centerx
        currenty = self.rect.centery
        dx, dy = pygame.mouse.get_pos()
        angle = 270- math.degrees(math.atan2(dy-currenty,dx-currentx))

        r = 30
        cx, cy = self.rect.center
        x = cx + r*math.cos(math.atan2(dy-currenty,dx-currentx))
        y = cy + r*math.sin(math.atan2(dy-currenty,dx-currentx))

        self.weapon = pygame.transform.rotate(self.unchange_weapon, angle)
        self.weaponrect = self.weapon.get_rect()
        self.weaponrect.center = (x,y)

        #Reset the dash and use key
        self.dash = False
        self.use = False

    def take_damage(self, damage_taken):
        #Reduce player's shield or health when called
        cooldown = time.time()
        if cooldown - self.damage_cooldown >= 0.5:
            if self.shield > 0:
                self.shield -= damage_taken
                if self.shield < 0:
                    self.shield = 0
                self.damage_cooldown = time.time()
            else:
                self.health -= damage_taken
                self.damage_cooldown = time.time()
            self.shield_cooldown = time.time()

    def shoot(self, bulletgroup,playsound = False):
        #shoot a bullet base on the current weapon
        currenttime = time.time()
        if currenttime - self.shoot_timer >= self.current_weapon['firespeed']:
            self.shoot_timer = time.time()
            if 'special' in self.current_weapon:
                self.current_weapon['special'](bulletgroup,self,self.windowSurface)
            else:
                bulletgroup.add(projectile.Bullet(self.weaponrect, pygame.mouse.get_pos(),self.current_weapon['bulletspeed'],self.current_weapon['damage'],self.current_weapon['bulletsprite']))
            
            if not self.current_weapon['auto']:
                self.fire = False

            if playsound:
                #pygame.mixer.Sound(self.currentweapon['firesound']).play()
                if self.current_weapon['firesound'] not in self.stored_sound:
                    sound = u.load_sound(self.current_weapon['firesound'])
                    sound.play()
                    self.stored_sound.update({self.current_weapon['firesound']:sound})

                else:
                    self.stored_sound[self.current_weapon['firesound']].play()

    def hud(self):
        #Display player's health, shield and cool down for the shield
        hpos = 50   #Location for the hud
        vpos = 40   #Location for the hud
        mouse_rect = Rect((0,0),(1,1)) #The current location of mouse
        mouse_pos = pygame.mouse.get_pos()
        mouse_rect.center = mouse_pos
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
            if mouse_rect.colliderect(armorbar):
                u.drawText(str(self.shield), 'comicsansms', 12, self.windowSurface, 53,vpos-3,Config.BLACK,False)
                pass

        if self.shield < self.max_shield:
            currenttime = time.time()
            vpos += 12
            armorcooldown = pygame.Rect((50,vpos),(158,4))
            cooldownbar = pygame.Rect((51,vpos+1),((currenttime - self.shield_cooldown)*(156/self.shield_regen_time),2))
            pygame.draw.rect(self.windowSurface,(96,96,96),armorcooldown)
            pygame.draw.rect(self.windowSurface,(135,135,135),cooldownbar)


        vpos += 15
        u.drawText(self.current_weapon['name'], 'comicsansms', 20, self.windowSurface, 50,vpos,Config.BLACK,False)

    def change_weapon(self,stuff = True):
        '''Change player's current weapon base on the value given'''
        if stuff:
            self.weapon_index += 1
            if self.weapon_index > len(self.weapons)-1:
                self.weapon_index = 0
        else:
            self.weapon_index -= 1
            if self.weapon_index < 0:
                self.weapon_index = len(self.weapons)-1

        self.current_weapon = weapons.stats[self.weapons[self.weapon_index]]

    def equip_weapon(self, weapon_id):
        '''Equip weapon base on the id given'''
        if weapon_id in weapons.stats:
            self.weapons.append(weapon_id)
        else:
            print('Invalid weapon id')

    def draw(self):
        #Draw player and their weapon
        #pygame.draw.rect(self.windowSurface, Config.RED, self.rect)
        self.windowSurface.blit(self.weapon, self.weaponrect)
        self.windowSurface.blit(self.image, self.rect)
 
