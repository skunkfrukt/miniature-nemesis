import math
import pyglet
from constants import *


class AnimatedSprite(pyglet.sprite.Sprite):
    def __init__(self, animations=None, default=None):
        self.animations = animations
        if default is None:
            default = self.animations.keys()[0]
            print("No default anim; using %s" % default)
        pyglet.sprite.Sprite.__init__(self, self.animations[default])
        self.current_animation = default

    def play(self, animation):
        if animation == self.current_animation:
            return
        elif animation in self.animations:
            self.image = self.animations[animation]
            self.current_animation = animation
        else:
            print("WARNING: %s tried to play invalid animation %s" %
                  (self, animation))


class GameObject(pyglet.event.EventDispatcher):
    '''Superclass of all objects that are drawn on stage.'''
    preferred_rendering_group_index = None
    required_classes = []

    def __init__(self):
        self.kill()
        self.behavior = None
        self.width = 1
        self.height = 1
        self.speed = None
        self.sprite = None
        self.collider = None
        self.colliders = None

    def kill(self):
        self.x = 0
        self.y = WIN_HEIGHT
        self.dead = True

    def reset(self, x, y):
        self.x, self.y = x, y
        self.dead = False

    def set_sprite(self, sprite):
        self.sprite = sprite
        self.width = self.sprite.width
        self.height = self.sprite.height

    def setup_sprite(self, batch, group):
        assert self.sprite is not None, "%s setting up None-sprite." % self
        self.sprite.batch = batch
        self.sprite.group = group

    def update_sprite(self, stage_offset):
        self.sprite.set_position(self.x - stage_offset, self.y)

    def check_despawn(self, stage_offset):
        if self.right <= stage_offset:
            return True
        return False

    def despawn(self):
        self.kill()
        self.dispatch_event('on_despawn', self)

    def move(self, dt, stage_offset):
        if self.speed is not None:
            dx, dy = (spd * dt for spd in self.speed)
            self.x += dx
            self.y += dy
        else:
            dx, dy = 0, 0
        if self.colliders is not None:
            for collider in self.colliders:
                collider.move(self.x, self.y, (dx, dy))
        if self.sprite is not None:
            self.update_sprite(stage_offset)
        if self.check_despawn(stage_offset):
            self.despawn()

    def behave(self, time):
        if self.behavior is not None:
            self.behavior(time)

    def add_collider(self, collider):
        if collider is None:
            return
        if self.colliders is None:
            self.colliders = []
        self.colliders.append(collider)
        collider.move(self.x, self.y)
        collider.push_handlers(self)

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, value):
        self.x = value

    @property
    def right(self):
        return self.x + self.width

    @right.setter
    def right(self, value):
        self.x = value - self.width

    @property
    def bottom(self):
        return self.y

    @bottom.setter
    def bottom(self, value):
        self.y = value

    @property
    def top(self):
        return self.y + self.height

    @top.setter
    def top(self, value):
        self.y = value - self.height

    @property
    def rect(self):
        return (self.left, self.bottom, self.right, self.top)

    def on_collision(self, other, rect, speed, effect):
        pass

GameObject.register_event_type('on_despawn')


class Point(object):
    '''A point in 2D space.'''
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Projectile(GameObject):
    preferred_rendering_group_index = R_GROUP_PROJECTILES

    def launch(self, origin_x, origin_y, target_x, target_y, speed):
        print("Launching %s." % self)
        self.x = origin_x
        self.y = origin_y
        delta_x = target_x - origin_x
        delta_y = target_y - origin_y
        delta_x_squared = delta_x ** 2
        delta_y_squared = delta_y ** 2
        speed_squared = speed ** 2
        speed_squared_from_deltas = delta_x_squared + delta_y_squared
        speed_factor = math.sqrt(speed_squared / speed_squared_from_deltas)
        dx = delta_x * speed_factor
        dy = delta_y * speed_factor
        self.speed = (dx, dy)
        self.dead = False;
        self.width = 1
