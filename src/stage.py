import pyglet
import gui
import collider
import actor

class Stage:
    def __init__(self, id, color=(0,0,0,0), obstacles={}):
        self.id = id
        self.offset = 0
        self.obstacles = obstacles
        background_image = pyglet.image.SolidColorImagePattern(color)
        self.background = background_image.create_image(640,360)
        self.graveyard = {}
        

class Prop(object):
    collision_effect = None
    
    def __init__(self, image):
        self.sprite = pyglet.sprite.Sprite(image, x=-100, y=-100)
        self.collider = None
        self.x, self.y = (0, 0)
        
    def move(self, dt, stage_offset):
        self.sprite.x = self.x - stage_offset
        self.sprite.y = self.y
        self.collider.x = self.x + 5
        self.collider.y = self.y + 10
        
    def setup_sprite(self, batch, group):
        if self.sprite is not None:
            if batch is not None:
                self.sprite.batch = batch
            if group is not None:
                self.sprite.group = group
        
    @property
    def width(self):
        return self.sprite.width


class Rock(Prop):
    collision_effect = ('stun', 0.5)
    _image = pyglet.resource.image('img/sprites/rock__sprite.png')

    def __init__(self):
        Prop.__init__(self, self._image)
        self.collider = collider.Collider(5, 10, 20, 20)
        
        
village_stage = {
        'props': []
}

import random

prop_classes = [Rock, actor.Peasant]

for x in range(0, 60001, 75):
    village_stage['props'].append((prop_classes[random.randint(0,1)], x, random.randint(0,300)))