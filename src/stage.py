import pyglet
import gui
import collider
import actor
from common import GameObject, Point
from constants import *

import logging
log = logging.getLogger(__name__)


class Graveyard(dict):
    def allocate(self, *classes):
        for cls in classes:
            if not cls in self:
                self[cls] = []
                self.allocate(*cls.required_classes)

    def get(self, cls):
        assert cls in self, "%s not in %s." % (cls, self)
        return self[cls].pop()

    def put(self, game_object):
        cls = type(game_object)
        allocate(cls)
        self[cls].append(game_object)


class Stage(pyglet.event.EventDispatcher):
    def __init__(self, id, color=(0,0,0,0), obstacles=[]):
        self.id = id
        self.batch = pyglet.graphics.Batch()
        self.root_rendering_group = pyglet.graphics.OrderedGroup(0)
        self.rendering_groups = []
        self.setup_background(color)
        self.graveyard = Graveyard()
        self.active_objects = []
        self.build_stage(obstacles)
        self.graveyard.allocate(actor.Hero)
        self.checkpoints = [CheckPoint(320, 180)]
        self.width = 6640  #!! Magic number
        self.height = 360
        self.spatial_hashes = {}
        self.spatial_hashes[HASH_GROUND] = collider.SpatialHash(
                self.width, self.height, 60, 60, layer=HASH_GROUND)
        self.spatial_hashes[HASH_AIR] = collider.SpatialHash(
                self.width, self.height, 60, 60, layer=HASH_AIR)
        self.spatial_hashes[HASH_TRIGGER] = collider.SpatialHash(
                self.width, self.height, 60, self.height, layer=HASH_TRIGGER)
        self.setup()

    def setup(self, difficulty=NORMAL, checkpoint_index=0):
        '''Resets the stage to a pristine state, ready to be played.'''
        self.ready = False
        self.clear()
        self.time = 0.0
        self.finished = False
        self.at_end = False
        self.scroll_speed = SPEEDS[difficulty]
        if checkpoint_index in range(len(self.checkpoints)):
            checkpoint = self.checkpoints[checkpoint_index]
        else:
            print("WARNING: Stage %s has no checkpoint %d. Using 0." %
                    (self.id, checkpoint_index))
            checkpoint = self.checkpoints[0]
        self.snap_to_checkpoint(checkpoint)
        self.find_initial_spawn_index()
        self.check_spawns()
        self.hero = self.spawn(checkpoint)
        self.ready = True

    def setup_background(self, color):
        background_pattern = pyglet.image.SolidColorImagePattern(color)
        background_image = background_pattern.create_image(
                WIN_WIDTH, WIN_HEIGHT)
        self.background = pyglet.sprite.Sprite(
                background_image, batch=self.batch,
                group=self.get_rendering_group(R_GROUP_BG))

    def get_rendering_group(self, group_index):
        assert group_index is not None, "Preferred group index is None."
        while group_index >= len(self.rendering_groups):
            new_index = len(self.rendering_groups)
            new_group = pyglet.graphics.OrderedGroup(new_index,
                    parent=self.root_rendering_group)
            self.rendering_groups.append(new_group)
        return self.rendering_groups[group_index]

    def build_stage(self, spawnpoints):
        self.spawns = spawnpoints
        classes = set([spawnpoint.spawned_class for spawnpoint in self.spawns])
        self.graveyard.allocate(*classes)

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
        spawned_object = self.get_game_object_instance(cls)
        spawned_object.reset(x, y)
        self.active_objects.append(spawned_object)
        return spawned_object

    def get_game_object_instance(self, game_object_cls):
        assert game_object_cls in self.graveyard, (
                "%s not in %s graveyard." % (game_object_cls, self.id))
        if len(self.graveyard[game_object_cls]) > 0:
            obj = self.graveyard[game_object_cls].pop()
        else:
            obj = game_object_cls()
            rendering_group = self.get_rendering_group(
                    obj.preferred_rendering_group_index)
            obj.setup_sprite(self.batch, rendering_group)
            if hasattr(obj, 'event_types'):
                obj.push_handlers(self)
        return obj

    def find_initial_spawn_index(self):
        spawn_index = 0
        num_spawns = len(self.spawns)
        left_edge = self.offset - SCREEN_MARGIN
        while self.spawns[spawn_index].x <= left_edge:  # .right
            spawn_index += 1
        self.next_spawn_index = spawn_index

    def check_spawns(self):
        spawn_index = self.next_spawn_index
        num_spawns = len(self.spawns)
        right_edge = self.offset + WIN_WIDTH + SCREEN_MARGIN
        while (spawn_index < num_spawns) and (
                self.spawns[spawn_index].x < right_edge):  # .left
            spawnpoint = self.spawns[spawn_index]
            assert spawnpoint.x > self.offset  # .right
            self.spawn(spawnpoint)
            spawn_index += 1
        self.next_spawn_index = spawn_index

    def update(self, dt):
        self.time += dt
        self.update_stage_offset(dt)
        self.check_spawns()
        self.move_active_objects(dt)
        self.check_collisions()

    def update_stage_offset(self, dt):
        if not self.at_end:
            self.offset += self.scroll_speed * dt
            if self.offset + WIN_WIDTH >= self.width:
                self.snap_to_right_edge()
                self.at_end = True
                print("End of stage...")
        elif not self.finished:
            if self.hero.x > self.width:
                self.finished = True
                print("Finished!")
                self.dispatch_event("on_stage_end", self.id)

    def snap_to_right_edge(self):
        self.offset = self.width - WIN_WIDTH

    def snap_to_left_edge(self):
        self.offset = 0

    def snap_to_checkpoint(self, checkpoint):
        self.offset = min(max(0, checkpoint.x - WIN_WIDTH // 2),
                self.width - WIN_WIDTH)

    def move_active_objects(self, dt):
        for obj in self.active_objects:
            obj.behave(dt)
            obj.move(dt, self.offset)

    def check_collisions(self):
        self.hero.colliding = False
        colliders = reduce(
                lambda ary, obj: ary + obj.colliders,
                self.active_objects, [])
        for hash_key in self.spatial_hashes:
            self.spatial_hashes[hash_key].collide(self.visible_rect, colliders)

    def send_keys_to_hero(self, keys, pressed=None, released=None):
        if self.hero is not None:
            self.hero.fixSpeed(keys)
            if pressed == pyglet.window.key.X:
                self.hero.fire_projectile(actor.Pebble, 300)

    def on_projectile_fired(self, projectile_cls, origin_x, origin_y,
            target_x, target_y, speed,
            source=None, valid_targets=None):
        fired_projectile = self.get_game_object_instance(projectile_cls)
        # fired_projectile.set_source(source)
        # fired_projectile.set_valid_targets(valid_targets)
        fired_projectile.launch(origin_x, origin_y, target_x, target_y, speed)
        self.active_objects.append(fired_projectile)

    def on_despawn(self, despawned_object):
        assert despawned_object in self.active_objects
        self.graveyard[type(despawned_object)].append(despawned_object)
        self.active_objects.remove(despawned_object)
        if despawned_object is self.hero:
            self.dispatch_event("on_hero_death")

    @property
    def visible_rect(self):
        return (self.offset, 0, self.offset + WIN_WIDTH, 0 + WIN_HEIGHT)

Stage.register_event_type('on_stage_end')
Stage.register_event_type('on_hero_death')


class SpawnPoint(Point):
    def __init__(self, x, y, cls, from_left=False, **kwargs):
        self.x = x
        self.y = y
        self.spawned_class = cls
        self.from_left = from_left
        self.parameters = kwargs


class CheckPoint(SpawnPoint):
    def __init__(self, x, y):
        super(CheckPoint, self).__init__(x, y, actor.Hero)


class Prop(GameObject):
    collision_effect = None
    preferred_rendering_group_index = R_GROUP_PROPS

    def __init__(self):
        super(Prop, self).__init__()
        self.collider = None

    def setup_sprite(self, batch, group):
        if self.sprite is not None:
            if batch is not None:
                self.sprite.batch = batch
            if group is not None:
                self.sprite.group = group


class Rock(Prop):
    collision_effect = ('stun', 0.5)
    _image = pyglet.resource.image('img/sprites/rock__sprite.png')

    def __init__(self):
        super(Rock, self).__init__()
        self.set_sprite(pyglet.sprite.Sprite(self._image))
        self.add_collider(collider.Collider(5, 10, 25, 30,
                effect=self.collision_effect, layer=HASH_GROUND))


class Stone(Prop):
    collision_effect = ('trip', 0.75)
    _image = pyglet.resource.image('img/sprites/pict_stone_temp.png')

    def __init__(self):
        super(Stone, self).__init__()
        self.set_sprite(pyglet.sprite.Sprite(self._image))
        self.add_collider(collider.Collider(0, 0, 10, 10,
                effect=self.collision_effect, layer=HASH_GROUND))


class House(Prop):
    num = 0
    collision_effect = ('stun', 0.5)
    _images = pyglet.image.ImageGrid(
            pyglet.resource.image('img/sprites/pict_houses.png'),
            1, 3)

    def __init__(self):
        super(House, self).__init__()
        self.set_sprite(pyglet.sprite.Sprite(self._images[House.num % 3]))
        self.add_collider(collider.Collider(0, 0, 180, 180,
                effect=self.collision_effect, layer=HASH_GROUND))
        House.num += 1


village_props = []

houses = [
        (395, 266), (600, 289), (981, 297), (1251, 272), (1617, 288),
        (1849, 281), (2137, 260), (2413, 299), (2771, 275), (3060, 283),
        (3316, 290), (3634, 278), (3931, 286), (4248, 268), (4581, 267),
        (4834, 268), (5144, 272), (5469, 292), (5722, 290), (6095, 281),
        (6405, 280)
        ]

rocks = [
        (657, 97), (1168, 128), (1462, 81), (2125, 83), (2452, 119),
        (2856, 158), (3541, 116), (4006, 54), (4368, 151), (4841, 208),
        (5388, 158), (5987, 168), (6564, 144)
        ]

for i, h in enumerate(houses):
    village_props.append(SpawnPoint(h[0], h[1], House))
    if i % 3 == 1:
        village_props.append(SpawnPoint(h[0] + 95, h[1] - 20,
                actor.PeasantC))

for r in rocks:
    village_props.append(SpawnPoint(r[0], r[1], Rock))

for p in [(400, 200), (450, 110), (500, 40), (550, 300)]:
    village_props.append(SpawnPoint(p[0], p[1], actor.Peasant))

village_props.sort(lambda a, b: a.x - b.x)
