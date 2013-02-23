import logging
log = logging.getLogger(__name__)

import pyglet
from prop import *
from actor import *


# Props


HITBOX_ROCK = Vector(1, 1)
HITBOX_STONE = Vector(1, 1)
HITBOX_HOUSE = Vector(1, 1)
HITBOX_CHURCH = Vector(1, 1)
HITBOX_CREEK = Vector(1, 1)
HITBOX_SKELETON = Vector(1, 1)
OFFSET_ROCK = Vector(1, 1)
OFFSET_STONE = Vector(1, 1)
OFFSET_HOUSE = Vector(1, 1)
OFFSET_CHURCH = Vector(1, 1)
OFFSET_CREEK = Vector(1, 1)
OFFSET_SKELETON = Vector(1, 1)


class Rock(Prop):
    # Collision effect: Stun 0.5 s
    image = pyglet.resource.image('img/sprites/rock.png')
    builder_data = {'width': 2, 'height': 2, 'max_y': 7,
            'x_variance': 31, 'y_variance': 55}

    def __init__(self, position, **kwargs):
        super(Rock, self).__init__(position, HITBOX_ROCK, **kwargs)


class Stone(Prop):
    BUILDER_NAME = 'PROP_STONE'
    # Collision effect: Trip 0.75 s
    image = pyglet.resource.image('img/sprites/stone.png')
    builder_data = {'width':1, 'height':1, 'max_y':7,
            'x_variance': 11, 'y_variance': 24}

    def __init__(self, position, **kwargs):
        super(Stone, self).__init__(position, HITBOX_STONE, **kwargs)


class House(Prop):
    num = 0
    # Collision effect: Stun 0.5 s
    images = pyglet.image.ImageGrid(
            pyglet.resource.image('img/sprites/house.png'),
            1, 3)
    builder_data = {'width':5, 'height':5, 'min_y':2, 'max_y': 7,
            'x_variance': 20, 'y_variance': 19}

    def __init__(self, position, **kwargs):
        super(House, self).__init__(position, HITBOX_HOUSE, **kwargs)
        House.num += 1

    @property
    def image(self):
        return self.images[self.num % 3]


class HeroHouse(House):
    # Collision effect: Stun 0.5 s
    image = pyglet.resource.image('img/sprites/herohouse.png')

    def __init__(self, position, **kwargs):
        super(HeroHouse, self).__init__(position, **kwargs)


class Church(Prop):
    # Collision effect: Stun 0.5 s
    image = pyglet.resource.image('img/sprites/church.png')
    builder_data = {'width':10, 'height':8, 'min_y':1,
            'x_variance': 5, 'y_variance': 23}

    def __init__(self, position, **kwargs):
        super(Church, self).__init__(position, HITBOX_CHURCH, **kwargs)


class Creek(Prop):
    # Collision effect: Drown
    image = pyglet.resource.image('img/sprites/creek.png')
    builder_data = {'width':5, 'height':9,
            'x_variance': 20}

    def __init__(self, position, **kwargs):
        super(Creek, self).__init__(position, HITBOX_CREEK, **kwargs)


class Skeleton(Prop):
    # Collision effect: None
    image = pyglet.resource.image('img/sprites/skeleton.png')
    builder_data = {'width':1, 'height':1,
            'x_variance': 14, 'y_variance': 4}

    def __init__(self, position, **kwargs):
        super(Skeleton, self).__init__(position, HITBOX_SKELETON, **kwargs)


# Actors


HITBOX_PEBBLE = Vector(1, 1)
HITBOX_PEASANT = Vector(1, 1)
HITBOX_PREACHER = Vector(1, 1)


class Pebble(Projectile):
    image = pyglet.resource.image('img/sprites/pebble.png')
    # Collision effect: Trip 0.2 s

    def __init__(self):
        super(Pebble, self).__init__()


class Peasant(Actor):
    _anim_set = "ANIMSET_PEASANT"
    required_classes = [Pebble]

    max_speed = 60.0
    acceleration = (100, 100)
    # Collision effect: Trip 0.5 s

    FIRST_AIM_DELAY = 1.2
    AIM_DELAY = 0.6
    THROW_DELAY = 0.3
    LEAP_SPEED = (220, 0)
    LEAP_TIME = 0.4

    def __init__(self, position, **kwargs):
        super(Peasant, self).__init__(position, HITBOX_PEASANT, **kwargs)
        self.speed = VECTOR_NULL
        self.target = None
        self.next_action_delay = 0.0

    def update_speed(self, dt):
        pass

    def behave(self, dt):
        self.next_action_delay -= dt
        self.behavior(dt)

    def reset(self, x, y):
        Actor.reset(self, x, y)
        self.target = None
        self.frustration = 0
        self.behavior = self.behave_idle

    def behave_idle(self, dt):
        self.play('idle')
        self.speed = VECTOR_NULL
        if self.target is not None:
            self.play('notice')
            self.next_action_delay = 0.4
            self.behavior = self.behave_notice

    def behave_notice(self, dt):
        self.play('notice')
        if self.next_action_delay <= 0:
            self.next_action_delay = 5.0
            self.behavior = self.behave_charge_ahead  # self.behave_pursue

    def behave_pursue(self, dt):
        self.play('run')
        self.pursue(self.target, dt)
        dist_x = self.target.x - 60 - self.x
        if dist_x > 300:
            self.frustration += dt + dt
        elif dist_x < 70:
            dist_y = abs(self.target.y - self.y)
            if dist_y < 10:
                self.speed = self.LEAP_SPEED
                self.next_action_delay = self.LEAP_TIME
                self.behavior = self.behave_leap
        else:
            self.frustration += dt
        if self.frustration >= 5:
            self.throwing = False
            self.aiming = False
            self.behavior = self.behave_throw

    def behave_throw(self, dt):
        if self.aiming:
            self.play('aim')
            self.approach_target_speed(dt,
                    ((100 + self.max_speed) * 0.6, 0))
            if self.next_action_delay <= 0:
                self.throwing = True
                self.fire_projectile(Pebble, 250, target=self.target)
                self.aiming = False
                self.next_action_delay = self.THROW_DELAY
        elif self.throwing:
            self.play('throw')
            self.speed = VECTOR_NULL
            if self.next_action_delay <= 0:
                self.throwing = False
                self.aiming = True
                self.next_action_delay = self.AIM_DELAY
        else:
            self.aiming = True
            self.next_action_delay = self.FIRST_AIM_DELAY


    def behave_leap(self, dt):
        self.play('leap')
        self.approach_target_speed(dt, (0, 0))
        if self.next_action_delay <= 0:
            self.speed = VECTOR_NULL
            self.behavior = self.behave_down


    def behave_trip(self, dt):
        self.play('trip')
        self.approach_target_speed(dt, (0, 0))
        if self.speed[0] < 20:
            self.speed = VECTOR_NULL
            self.behavior = self.behave_down


    def behave_down(self, dt):
        self.play('down')

    def behave_charge_ahead(self, dt, speed=110):  #TODO magic number
        if self.next_action_delay <= 0:
            self.throwing = False
            self.aiming = False
            self.behavior = self.behave_throw
        self.play('run')
        final_speed = speed
        if self.target is not None:
            dist_x = self.target.x - self.x
            dist_y = self.target.y - self.y
            if abs(dist_y) < 15:
                if 0 < dist_x < 70:
                    self.speed = self.LEAP_SPEED
                    self.next_action_delay = self.LEAP_TIME
                    self.behavior = self.behave_leap
                else:
                    final_speed = self.LEAP_SPEED
        self.approach_target_speed(dt, (final_speed, 0))

    def pursue(self, target, dt, speed=60):
        dist_x = target.x - 60 - self.x
        dist_y = target.y - self.y
        if dist_x <= 0:
            self.direction = (0,0)
        else:
            if dist_y < -100:
                self.direction = (1, -1)
            elif dist_y > 100:
                self.direction = (1, 1)
            elif abs(dist_y) < 10:
                self.direction = (1, 0)
        dirx, diry = self.direction
        tx, ty = dirx * (100 + speed), diry * (100 + speed)
        self.approach_target_speed(dt, (tx, ty))

    def on_detection(self, target):
        if self.target is None and type(target) is Hero:
            if abs(self.y - target.y) < 200:
                self.target = target


class PeasantB(Peasant):

    max_speed = 60.0
    acceleration = (100, 100)
    # Collision effect: Trip 0.5 s

    FIRST_AIM_DELAY = 0.6
    AIM_DELAY = 0.3
    NUMBER_OF_THROWS = 4

    def update_speed(self, dt):
        pass

    def behave(self, dt):
        self.next_action_delay -= dt
        self.behavior(dt)

    def reset(self, x, y):
        Actor.reset(self, x, y)
        self.target = None
        self.frustration = 0
        self.behavior = self.behave_idle
        self.aiming = False
        self.throwing = False
        self.sprite.color = (255, 191, 191)

    def behave_idle(self, dt):
        self.play('idle')
        if self.target is not None:
            self.play('notice')
            self.next_action_delay = 0.4
            self.behavior = self.behave_notice

    def behave_notice(self, dt):
        self.play('notice')
        if self.next_action_delay <= 0:
            self.behavior = self.behave_throw

    def behave_pursue(self, dt):
        self.play('run')
        self.pursue(self.target, dt)

    def behave_throw(self, dt):
        if self.aiming:
            self.play('aim')
            self.approach_target_speed(dt,
                    ((100 + self.max_speed) * 0.6, 0))
            if self.next_action_delay <= 0:
                self.throwing = True
                self.fire_projectile(Pebble, 300, target=self.target)
                self.frustration += 1
                self.aiming = False
                self.next_action_delay = self.THROW_DELAY
        elif self.throwing:
            self.play('throw')
            self.speed = VECTOR_NULL
            if self.next_action_delay <= 0:
                if self.frustration < self.NUMBER_OF_THROWS:
                    self.throwing = False
                    self.aiming = True
                    self.next_action_delay = self.AIM_DELAY
                else:
                    self.throwing = False
                    self.frustration = 0
                    self.behavior = self.behave_pursue
        else:
            self.aiming = True
            self.next_action_delay = self.FIRST_AIM_DELAY


    def pursue(self, target, dt):
        dist_x = target.x - 60 - self.x
        dist_y = target.y - self.y
        if dist_x <= 0:
            self.direction = (0,0)
            self.behavior = self.behave_notice
        else:
            if dist_y < -20:
                self.direction = (1, -1)
            elif dist_y > 20:
                self.direction = (1, 1)
            elif abs(dist_y) < 10:
                self.direction = (1, 0)
            elif self.direction == (0, 0):
                self.direction = (1, 0)
        dirx, diry = self.direction
        tx, ty = dirx * (100 + self.max_speed), diry * (100 + self.max_speed)
        self.approach_target_speed(dt, (tx, ty))


    def on_detection(self, target):
        if self.target is None and type(target) is Hero:
            if abs(self.y - target.y) < 200:
                self.target = target

    def on_collision(self, other, rect, speed, effect):
        if effect:
            self.apply_status(**effect)


class Preacher(Actor):
    _anim_set = "ANIMSET_PREACHER"

    max_speed = 120.0
    acceleration = Vector(100, 100)
    collision_effect = ('trip', 0.5)

    def __init__(self, position, **kwargs):
        super(Preacher, self).__init__(position, HITBOX_PREACHER, **kwargs)
        self.speed = VECTOR_NULL
        self.target = None
        self.next_action_delay = 0.0


BUILDER_NAMES = {
    'PROP_CHURCH': Church,
    'PROP_CREEK': Creek,
    'PROP_HEROHOUSE': HeroHouse,
    'PROP_HOUSE': House,
    'PROP_ROCK': Rock,
    'PROP_SKELETON': Skeleton,
    'PROP_STONE': Stone,
    'ACTOR_PEASANT': Peasant,
    'ACTOR_PREACHER': Preacher
}
