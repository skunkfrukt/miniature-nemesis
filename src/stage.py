import pyglet
import gui
import collider
import actor
from constants import *

class Stage:
    def __init__(self, id, color=(0,0,0,0), obstacles={}):
        self.id = id
        self.obstacles = obstacles
        background_image = pyglet.image.SolidColorImagePattern(color)
        self.background = background_image.create_image(640,360)
        self.graveyard = {}
        self.active_objects = []
        self.props = []
        self.checkpoints = [Checkpoint(320, 180)]
        self.hero = actor.Hero()
        self.setup()
        
    def setup(self, difficulty=NORMAL, checkpoint_index=0):
        '''Resets the stage to a pristine state, ready to be played.'''
        if checkpoint_index in range(len(self.checkpoints)):
            checkpoint = self.checkpoints[checkpoint_index]
        else:
            print("WARNING: Stage %s has no checkpoint %d. Using 0." %
                    (self.id, checkpoint_index))
            checkpoint = self.checkpoints[0]
        self.offset = max(0, checkpoint.x - WIN_WIDTH // 2)
        self.scroll_speed = SPEED_BASE * SPEED_FACTORS[difficulty]
        self.clear()
        
        self.hero.reset(checkpoint, difficulty=difficulty)
        
    def clear(self):
        '''Kills all active objects.'''
        while len(self.active_objects) > 0:
            item = self.active_objects.pop()
            item.kill()
            cls = type(item)
            self.graveyard[cls].append(item)


class Checkpoint(object):
    def __init__(self, x, y):
        self.x, self.y = x, y


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


class House(Prop):
    collision_effect = ('stun', 0.5)
    _image = pyglet.resource.image('img/sprites/pict_house_temp.png')
    
    def __init__(self):
        Prop.__init__(self, self._image)
        self.collider = collider.Collider(0, 0, 180, 180)


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
        'props': []
}

import random

prop_classes = [Rock, Stone, actor.Peasant, None, None, None]

for x in range(180, 30001, 30):
    prop_index = random.randint(0,5)
    if prop_classes[prop_index]:
        village_stage['props'].append((prop_classes[prop_index],
                    x, random.randint(0,300)))
    if x % 180 == 0:
        village_stage['props'].append((House,
                x + random.randint(-5, 5), random.randint(275,325)))
    if x % 60 == 0:
        village_stage['props'].append((Rock,
                x + random.randint(-3, 3), random.randint(-15,10)))