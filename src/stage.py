import pyglet
import gui
import collider
import actor
from common import GameObject, Point
from constants import *

class Stage:
    def __init__(self, id, color=(0,0,0,0), obstacles=[]):
        self.id = id
        self.batch = pyglet.graphics.Batch()
        self.bg_group = pyglet.graphics.OrderedGroup(0)
        self.bg_prop_group = pyglet.graphics.OrderedGroup(1)
        self.actor_group = pyglet.graphics.OrderedGroup(2)
        background_image = pyglet.image.SolidColorImagePattern(color)
        self.background = pyglet.sprite.Sprite(
                background_image.create_image(640,360), batch=self.batch,
                group=self.bg_group)
        self.graveyard = {}
        self.active_objects = []
        self.spawns = obstacles  # .sort(lambda game_object: game_object.x)
        # Temporary, hard-coded graveyard junk:
        for s in self.spawns:
            if not s.spawned_class in self.graveyard:
                self.graveyard[s.spawned_class] = []
        self.graveyard[actor.Hero] = []
        self.next_spawn_index = 0
        self.checkpoints = [CheckPoint(320, 180)]
        self.hero = None
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
        self.check_initial_spawns()
        self.hero = self.spawn(checkpoint)
        
    def clear(self):
        '''Kills all active objects.'''
        while len(self.active_objects) > 0:
            item = self.active_objects.pop()
            item.kill()
            cls = type(item)
            self.graveyard[cls].append(item)
            
    def add_checkpoint(self, x, y):
        self.checkpoints.append(Checkpoint(x, y))
        self.checkpoints.sort(key=lambda ckpt: ckpt.x)
        
    def spawn(self, spawnpoint):
        cls = spawnpoint.spawned_class
        x = spawnpoint.x + spawnpoint.offset_x
        y = spawnpoint.y + spawnpoint.offset_y
        assert cls in self.graveyard, "%s not in %s graveyard." % (cls, self.id)
        if len(self.graveyard[cls]) > 0:
            spawned_object = self.graveyard[cls].pop()
        else:
            spawned_object = cls()
            spawned_object.setup_sprite(self.batch, self.bg_prop_group)
        spawned_object.reset(x, y)
        self.active_objects.append(spawned_object)
        return spawned_object
        
    def check_initial_spawns(self):
        nsi = self.next_spawn_index
        msi = len(self.spawns)
        while nsi < msi and self.spawns[nsi].x < self.offset - 100:
                # Kill magic number
            nsi += 1
        self.check_spawns()
        self.next_spawn_index = nsi
        
    def check_spawns(self):
        nsi = self.next_spawn_index
        msi = len(self.spawns)
        while nsi < msi and self.spawns[nsi].x < self.offset + 740:
            spawnpoint = self.spawns[nsi]
            if spawnpoint.x + 50 > self.offset: # Magic number --> width
                self.spawn(spawnpoint)
            nsi += 1
        self.next_spawn_index = nsi
        
    def update(self, dt):
        self.hero.colliding = False
        bg_movement = SPEED_NORMAL * dt
        self.offset += bg_movement
        
        self.check_spawns()
        self.move_active_objects(dt)
        self.check_collisions()
        
        
                
    def move_active_objects(self, dt):
        for obj in self.active_objects:
            obj.move(dt, self.offset)
            
    def check_despawns(self):
        objects_to_despawn = []
        for obj in self.active_objects:
            if obj.x < self.offset - obj.width:
                obj.kill()
                objects_to_despawn.append(obj)
                self.graveyard[type(obj)].append(obj)
        for obj in objects_to_despawn:
            self.active_objects.remove(obj)
            
    def check_collisions(self):
        for thing in self.active_objects:
            if not self.hero.colliding:
                if thing is not self.hero:
                    self.hero.collide(thing)
                    
    def send_keys_to_hero(self, keys):
        if self.hero is not None:
            self.hero.fixSpeed(keys)


class SpawnPoint(Point):
    def __init__(self, x, y, cls, offset_x=0, offset_y=0):
        Point.__init__(self, x, y)
        self.spawned_class = cls
        self.offset_x, self.offset_y = offset_x, offset_y


class CheckPoint(SpawnPoint):
    def __init__(self, x, y):
        SpawnPoint.__init__(self, x, y, actor.Hero, 0, 0)
    
    
class Prop(GameObject):
    collision_effect = None
    
    def __init__(self, image):
        self.sprite = pyglet.sprite.Sprite(image, x=-100, y=-100)
        self.collider = None
        self.x, self.y = (0, 0)
        
    def move(self, dt, stage_offset):
        self.sprite.x = self.x - stage_offset
        self.sprite.y = self.y
        if self.collider:
            self.collider.move(self.x, self.y)
        
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
        self.collider = collider.Collider(5, 10, 25, 30)
        
        
class Stone(Prop):
    collision_effect = ('trip', 0.75)
    _image = pyglet.resource.image('img/sprites/pict_stone_temp.png')
    
    def __init__(self):
        Prop.__init__(self, self._image)
        self.collider = collider.Collider(0, 0, 10, 10);


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
        

village_props = []

import random

prop_classes = [Rock, Stone, actor.Peasant, None, None, None]

for x in range(180, 30001, 30):
    prop_index = random.randint(0,5)
    if prop_classes[prop_index]:
        village_props.append(SpawnPoint(x, random.randint(0,300),
                prop_classes[prop_index]))
    if x % 180 == 0:
        village_props.append(SpawnPoint(x + random.randint(-5, 5),
                random.randint(275,325), House))
    if x % 60 == 0:
        village_props.append(SpawnPoint(x + random.randint(-3, 3),
                random.randint(-15,10), Rock))
                
