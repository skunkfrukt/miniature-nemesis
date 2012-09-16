import pyglet
import gui

class Stage:
    
    def __init__(self, id, color=(0,0,0,0), obstacles={}):
        self.id = id
        self.offset = 0
        self.obstacles = obstacles
        background_image = pyglet.image.SolidColorImagePattern(color)
        self.background = background_image.create_image(640,360)
        self.graveyard = {}
        

class Prop(pyglet.sprite.Sprite):
    collision_effect = None
    
    def __init__(self, image):
        pyglet.sprite.Sprite.__init__(self, image, x=-100, y=-100)
        self.stage_x = 0


class Rock(Prop):
    collision_effect = ('stun', 0.5)
    _image = pyglet.resource.image('img/sprites/rock__sprite.png')

    def __init__(self):
        Prop.__init__(self, self._image)
        
        
village_stage = {
        'props': []
}

import random

for x in range(0, 60001, 75):
    village_stage['props'].append((Rock, x, random.randint(0,300)))