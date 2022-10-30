import pygame, Utility as u

class Item(pygame.sprite.Sprite):
    '''Items the player can interact with'''
    def __init__(self,image,location):
        pygame.sprite.Sprite.__init__(self)
        if type(image) is str:
            self.image = u.load_image(image) #Sprit for the object
        elif type(image) is pygame.Surface:
            self.image = image
        self.rect = self.image.get_rect()   #Rect for the object
        self.rect.center = location         #The location the object will spwan in

    def reaction(self, player):
        pass

class button(Item):
    def __init__(self, image, location):
        super().__init__(image, location)

    def reaction(self, player):
        #change level
        if self.rect.colliderect(player.rect) and player.use:
            player.change_level = True

class firstaid(Item):
    def __init__(self, image, location):
        super().__init__(image, location)

    def reaction(self, player):
        #Heals player when their current health is lower than the max health
        if self.rect.colliderect(player.rect) and player.use:
            if player.health < player.max_health:
                player.health += 1
                if player.health > player.max_health:
                    player.health -= player.health - player.max_health
                self.kill()

class painkiller(Item):
    def __init__(self, image, location):
        super().__init__(image, location)

    def reaction(self, player):
        if self.rect.colliderect(player.rect) and player.use:
            player.max_health +=1
            player.health += 1
            self.kill()

class notdrug(Item):
    def __init__(self, image, location):
        super().__init__(image, location)

    def reaction(self, player):
        if self.rect.colliderect(player.rect) and player.use:
            self.kill()

class weapon(Item):
    def __init__(self, image, location):
        super().__init__(image, location)

    def reaction(self, player):
        if self.rect.colliderect(player.rect) and player.use:
            player.equip_weapon('spas')
            self.kill()