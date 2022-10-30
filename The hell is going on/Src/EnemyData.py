#------------------------------Enemies-------------------------------
#A tuple cotaining stat for each enemy
#enemy sprite, health, speed, damage, movement, spwan locaction
#sprite, health, speed, damage, movement, firetime ,bullet ,bulletspeed,spwan locaction
NORMAL_CAT = ("cat.png",1,5,0.5,2)
ARMOR = ("cat with bullet proof vest.png",5,1,0.5,2)

CAT_WITH_KNIFE = ("cat_with_knife.png",2,6,1,2)
SHIELD = ("cat with shield.png",8,1,0.5,2)

GUNNER = ("cat with a gun.png",2,3,1,1,1,"cat_bullet.png",10)
SMGER = ("cat with a smg.png",2,4,0.5,1,0.2,"cat_bullet.png",15)

CAT_SOLDIER = ("cat soldier.png", 5,2,1.5,1,0.4,"cat_bullet.png",12)
CAT_M1 = ("cat with m1 garand.png", 3,3,3,1,0.75,"cat_bullet.png",20)
CAT_PYTHON = ("cat with python.png", 3,5,5,1,1.5,"cat_bullet.png",10)

ENEMY_DICT = {'N':NORMAL_CAT, 
              'A':ARMOR, 
              'G':GUNNER,
              'K':CAT_WITH_KNIFE,
              'S':SMGER,
              'SH':SHIELD,
              'CS':CAT_SOLDIER,
              'CM':CAT_M1,
              'CP':CAT_PYTHON} #A dictionary cotaining all the enemies


enemy_dict = {
    
              '.':{'name':'cat name',
                   'sprite':'cat.png',
                   'type':'melee',
                   'health':1,
                   'speed':0,
                   'melee damage':0,
                   'movement':0},

              'N':{'name':'normal cat',
                   'sprite':'cat.png',
                   'type':'melee',
                   'health':1,
                   'speed':5,
                   'melee damage':0.5,
                   'movement':2},

              'A':{'name':'armor cat',
                   'sprite':'cat with bullet proof vest.png',
                   'type':'melee',
                   'health':4,
                   'speed':3,
                   'melee damage':0.5,
                   'movement':2},

              'K':{'name':'cat with a knife',
                   'sprite':'cat_with_knife.png',
                   'type':'melee',
                   'health':2,
                   'speed':6,
                   'melee damage':2,
                   'movement':2},

              'SH':{'name':'shield cat',
                   'sprite':'cat with shield.png',
                   'type':'melee',
                   'health':8,
                   'speed':1,
                   'melee damage':1,
                   'movement':2},
              #----------------------------------------Range-----------------------------------
              'G':{'name':'gunner cat',
                   'sprite':'cat with a gun.png',
                   'type':'range',
                   'health':2,
                   'speed':3,
                   'melee damage':0.5,
                   'movement':1,
                   'bullet sprite':'cat_bullet.png',
                   'range damage': 1,
                   'fire speed':1,
                   'fire time':0,
                   'cool down':0,
                   'bullet speed':10},

              'S':{'name':'smg cat',
                   'sprite':'cat with a smg.png',
                   'type':'range',
                   'health':2,
                   'speed':4,
                   'melee damage':0.5,
                   'movement':1,
                   'bullet sprite':'cat_bullet.png',
                   'range damage': 0.5,
                   'fire speed':0.1,
                   'fire time':1,
                   'cool down':2,
                   'bullet speed':15},

              'CS':{'name':'cat soldier',
                   'sprite':'cat soldier.png',
                   'type':'range',
                   'health':4,
                   'speed':2,
                   'melee damage':1,
                   'movement':1,
                   'bullet sprite':'cat_bullet.png',
                   'range damage': 1.5,
                   'fire speed':0.15,
                   'fire time':4,
                   'cool down':2,
                   'bullet speed':12},

              'CM':{'name':'garand cat',
                   'sprite':'cat with m1 garand.png',
                   'type':'range',
                   'health':2,
                   'speed':1,
                   'melee damage':0.5,
                   'movement':1,
                   'bullet sprite':'cat_bullet.png',
                   'range damage': 1,
                   'fire speed':0.5,
                   'fire time':3,
                   'cool down':2,
                   'bullet speed':20},

              'CP':{'name':'python cat',
                   'sprite':'cat with python.png',
                   'type':'range',
                   'health':2,
                   'speed':3,
                   'melee damage':0.5,
                   'movement':1,
                   'bullet sprite':'cat_bullet.png',
                   'range damage': 2.5,
                   'fire speed':0.25,
                   'fire time':1.5,
                   'cool down':6,
                   'bullet speed':10}
              
              }
