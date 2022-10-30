import pygame, os, random, time, math, Utility as u, Config, Projectile
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
    '''Spawn an Enemy'''
    def __init__(self, image, health = 1, speed = 0, damage = 0, movement = 0, locaction = None):
        pygame.sprite.Sprite.__init__(self)
        if type(image) is pygame.Surface:
            self.unchage_sprite = image                             #unchange sprit for the enemy
        else:
            self.unchage_sprite = u.load_image(image)                 #unchange sprit for the enemy
        self.image = self.unchage_sprite                            #Sprit for the enemy
        self.rect = self.image.get_rect()                           #Rect for the enemy
        self.damage = damage                                        #The damage enemy will deal to the player
        self.health = health                                        #Health for the enemy
        self.speed = speed                                          #Speed for the enemy
        self.damageCooldown = time.time()

        if locaction is None:
            self.rect.left = random.randrange(0, Config.WINDOWWIDTH)
            self.rect.top = random.randrange(0, Config.WINDOWHEIGHT)
        else:
            self.rect.center = locaction                            #The locaction the enemy will be spwan in
        self.movement = movement                                    #The type of movement the enemy has
        #0 = no movement
        #1 = random movement
        #2 = move to player
        if movement == 1:
            self.wavepoint = Rect((random.randrange(25, Config.WINDOWWIDTH-25),random.randrange(25, Config.WINDOWHEIGHT-25)), (5,5))

    def attack(self,player = None,bullet = None):
        #An empty function for range enemy
        pass

    def rotate(self, player):
        #Rotate the sprite to face the player
        currentx = self.rect.centerx
        currenty = self.rect.centery
        dx, dy = player.rect.centerx, player.rect.centery
        angle = 180-  math.degrees(math.atan2(dy-currenty,dx-currentx))
        self.image = pygame.transform.rotate(self.unchage_sprite, angle)
        x = self.rect.left
        y = self.rect.top

        #self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def moverandom(self, player, room):
        #Move to a random wave point

        if self.rect.centerx > self.wavepoint.centerx:
            self.rect.centerx -= self.speed
            if pygame.sprite.collide_mask(self,player) is not None or self.rect.colliderect(room.leftwall):
                self.rect.centerx += self.speed + 2
                self.wavepoint.center = (random.randrange(50, Config.WINDOWWIDTH-50),random.randrange(50, Config.WINDOWHEIGHT-50))

        elif self.rect.centerx < self.wavepoint.centerx:
            self.rect.centerx += self.speed
            if pygame.sprite.collide_mask(self,player) is not None or self.rect.colliderect(room.rightwall):
                self.rect.centerx -= self.speed + 2
                self.wavepoint.center = (random.randrange(50, Config.WINDOWWIDTH-50),random.randrange(50, Config.WINDOWHEIGHT-50))

        if self.rect.centery > self.wavepoint.centery:
            self.rect.centery -= self.speed
            if pygame.sprite.collide_mask(self,player) is not None or self.rect.colliderect(room.topwall):
                self.rect.centery += self.speed + 2
                self.wavepoint.center = (random.randrange(50, Config.WINDOWWIDTH-50),random.randrange(50, Config.WINDOWHEIGHT-50))

        elif self.rect.centery < self.wavepoint.centery:
            self.rect.centery += self.speed
            if pygame.sprite.collide_mask(self,player) is not None or self.rect.colliderect(room.bottomwall):
                self.rect.centery -= self.speed + 2
                self.wavepoint.center = (random.randrange(50, Config.WINDOWWIDTH-50),random.randrange(50, Config.WINDOWHEIGHT-50))

        if self.rect.colliderect(self.wavepoint):
            self.wavepoint.center = (random.randrange(50, Config.WINDOWWIDTH-50),random.randrange(50, Config.WINDOWHEIGHT-50))

    def moveplayer(self,player, room):
        #Move to player
        mask_collide = pygame.sprite.collide_mask(self,player) is not None
        if self.rect.centerx > player.rect.centerx:
            self.rect.centerx -= self.speed 
            if mask_collide or self.rect.colliderect(room.leftwall):
                self.rect.centerx += self.speed  + 2
            
        elif self.rect.centerx < player.rect.centerx:
            self.rect.centerx += self.speed
            if mask_collide or self.rect.colliderect(room.rightwall):
                self.rect.centerx -= self.speed  + 2

        if self.rect.centery > player.rect.centery:
            self.rect.centery -= self.speed
            if mask_collide or self.rect.colliderect(room.topwall):
                self.rect.centery += self.speed  + 2

        elif self.rect.centery < player.rect.centery:
            self.rect.centery += self.speed
            if mask_collide or self.rect.colliderect(room.bottomwall):
                self.rect.centery -= self.speed  + 2

    def stayaway(self):
        #Stop enemies from coliding with eachother 
        group = self.groups()
        colide = pygame.sprite.spritecollideany(self, group[0], collided = None)
        if colide is not self:
            if self.rect.centerx > colide.rect.centerx:
                self.rect.centerx += self.speed + 2
            elif self.rect.centerx < colide.rect.centerx:
                self.rect.centerx -= self.speed + 2
            if self.rect.centery > colide.rect.centery:
                self.rect.centery += self.speed + 2
            elif self.rect.centery < colide.rect.centery:
                self.rect.centery -= self.speed + 2

    def take_damage(self, damage_taken):
        #Reduce player's shield or health when called
        cooldown = time.time()
        if cooldown - self.damageCooldown >= 0.5:
                self.health -= damage_taken
                self.damageCooldown = time.time()

class Range_enemy(Enemy):
    def __init__(self, image, health, speed, damage, movement, bullet, range_damage, fire_speed, fire_time, cool_down, bullet_speed ,locaction=None):
        super().__init__(image, health=health, speed=speed, damage=damage, movement=movement, locaction=locaction)

        self.bullet = bullet
        self.bulletspeed = bullet_speed

        self.range_damage = range_damage

        self.fire_speed = fire_speed
        self.fire_speed_timer = time.time()

        self.fire_time = fire_time
        self.fire_timer = time.time()

        self.cool_down = cool_down
        self.cool_down_timer = time.time()

    def attack(self,player,bullets):
        #An empty function for range enemy
        try:
            current_time = time.time()
            if current_time-self.fire_timer < self.fire_time or self.fire_time == 0:
                if current_time-self.fire_speed_timer > self.fire_speed:
                    bullets.add(Projectile.Bullet(self.rect,(player.rect.centerx,player.rect.centery),self.bulletspeed,self.damage ,self.bullet))
                    self.fire_speed_timer = time.time()
                    self.cool_down_timer = time.time()
            else:
                if current_time-self.cool_down_timer > self.cool_down:
                    self.cool_down_timer = time.time()
                    self.fire_timer = time.time()
        except:
            print('range enemy attack error')

class Boss(Range_enemy):
    '''FINAL Boss for the game'''
    def __init__(self):
        super().__init__('final boss.png', 200, 1, 1.5, 1, 'cat_bullet.png',5,0.1,0,0, 10, (500,300))
        self.laser = u.load_image('lazer.png')
        self.stage = 1
        self.angle = 0

    def attack(self, player, bullets):
        endtime = time.time()
        if self.stage == 1:
            if endtime-self.fire_speed_timer > self.fire_speed:
                bullets.add(Projectile.Bullet(self.rect,(player.rect.centerx,player.rect.centery),self.bulletspeed,self.damage ,self.bullet))
                self.fire_speed_timer = time.time()
            if self.health < 150:
                self.stage = 2
                self.fire_speed = 1
        if self.stage == 2:
            bullets.add(Projectile.Bullet(self.rect,(0,0),30,self.damage ,self.laser,True))
            bullets.add(Projectile.Bullet(self.rect,(0,600),30,self.damage ,self.laser,True))
            bullets.add(Projectile.Bullet(self.rect,(1000,0),30,self.damage ,self.laser,True))
            bullets.add(Projectile.Bullet(self.rect,(1000,600),30,self.damage ,self.laser,True))

            if endtime-self.fire_speed_timer > 1:
                bullets.add(Projectile.Bullet(self.rect,(player.rect.centerx,player.rect.centery),10,2.5 ,self.bullet))
                self.fire_speed_timer = time.time()

            if self.health < 100:
                self.stage = 3
                self.movement = 2
                self.speed = 3
        if self.stage == 3:
            if self.health < 50:
                self.speed = 5

    def rotate(self, player):
        #Rotate the sprite to face the player
        if self.stage == 1:
            currentx = self.rect.centerx
            currenty = self.rect.centery
            dx, dy = player.rect.centerx, player.rect.centery
            self.angle = 180-  math.degrees(math.atan2(dy-currenty,dx-currentx))
            self.image = pygame.transform.rotate(self.unchage_sprite, self.angle)
            x = self.rect.left
            y = self.rect.top

            #self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.top = y
        elif self.stage == 2 and int(self.angle) != 90:
            if int(self.angle) > 90:
                self.angle = int(self.angle) - 1
            elif int(self.angle) < 90:
                self.angle = int(self.angle) + 1
            currentx = self.rect.centerx
            currenty = self.rect.centery
            dx, dy = player.rect.centerx, player.rect.centery
            self.image = pygame.transform.rotate(self.unchage_sprite, self.angle)
            x = self.rect.left
            y = self.rect.top
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.top = y
