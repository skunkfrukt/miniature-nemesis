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
        if self.collider:
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
        
        
class Stone(Prop):
    collision_effect = ('trip', 0.75)
    _image = pyglet.resource.image('img/sprites/pict_stone_temp.png')
    
    def __init__(self):
        Prop.__init__(self, self._image)
        self.collider = collider.Collider(0, 0, 20, 10);


class SkyBackground(Prop):
    collision_effect = None
    _image = pyglet.resource.image('img/sprites/sky.png')
    never_die = True
    
    def __init__(self):
        Prop.__init__(self, self._image)
        self.collider = None
        self._x, self._y = 0, 0
        
    def move(self, dt, stage_offset):
        self.sprite.x = -stage_offset * 0.1
        self.sprite.y = self.y
        

village_stage = {
        'props': [(SkyBackground, 0, 300)]
}

import random

prop_classes = [Rock, Stone, actor.Peasant, None, None, None]

for x in range(200, 30001, 30):
    prop_index = random.randint(0,5)
    if prop_classes[prop_index]:
        village_stage['props'].append((prop_classes[prop_index],
                x, random.randint(0,250)))
            