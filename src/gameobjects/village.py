import logging
log = logging.getLogger(__name__)

import pyglet
from _baseclasses.prop import *
from _baseclasses.actor import *


# Props


class Rock(Prop):
    collision_effect = {'effect_type': 'stun', 'duration': 0.5}
    _image = pyglet.resource.image('img/sprites/rock.png')
    builder_data = {'width': 2, 'height': 2, 'max_y': 7,
            'x_variance': 31, 'y_variance': 55}

    def __init__(self, x, y, **kwargs):
        super(Rock, self).__init__(x, y, **kwargs)
        self.set_sprite(pyglet.sprite.Sprite(self._image))
        '''self.add_collider(collider.Collider(5, 10, 25, 30,
                effect=self.collision_effect, layer=1))'''


class Stone(Prop):
    BUILDER_NAME = 'PROP_STONE'
    collision_effect = {'effect_type': 'trip', 'duration': 0.75}
    _image = pyglet.resource.image('img/sprites/stone.png')
    builder_data = {'width':1, 'height':1, 'max_y':7,
            'x_variance': 11, 'y_variance': 24}

    def __init__(self, x, y, **kwargs):
        super(Stone, self).__init__(x, y, **kwargs)
        self.set_sprite(pyglet.sprite.Sprite(self._image))
        '''self.add_collider(collider.Collider(0, 0, 10, 10,
                effect=self.collision_effect, layer=1))'''


class House(Prop):
    num = 0
    collision_effect = {'effect_type': 'stun', 'duration': 0.5}
    _images = pyglet.image.ImageGrid(
            pyglet.resource.image('img/sprites/house.png'),
            1, 3)
    builder_data = {'width':5, 'height':5, 'min_y':2, 'max_y': 7,
            'x_variance': 20, 'y_variance': 19}

    def __init__(self, x, y, **kwargs):
        super(House, self).__init__(x, y, **kwargs)
        self.set_sprite(pyglet.sprite.Sprite(self._images[House.num % 3]))
        '''self.add_collider(collider.Collider(
                left=0, right=20, bottom=20, top=180,
                effect={'effect_type': 'stun', 'duration': 0.5},
                layer=1))
        self.add_collider(collider.Collider(
                left=20, right=180, bottom=0, top=20,
                effect={'effect_type': 'stop', 'directions': 'n'},
                layer=1))'''
        House.num += 1


class HeroHouse(House):
    collision_effect = {'effect-type': 'stun', 'duration': 0.5}
    _image = pyglet.resource.image('img/sprites/herohouse.png')

    def __init__(self, x, y, **kwargs):
        super(HeroHouse, self).__init__(x, y, **kwargs)
        self.set_sprite(pyglet.sprite.Sprite(self._image))


class Church(Prop):
    collision_effect = {'effect-type': 'stun', 'duration': 0.5}
    _image = pyglet.resource.image('img/sprites/church.png')
    builder_data = {'width':10, 'height':8, 'min_y':1,
            'x_variance': 5, 'y_variance': 23}

    def __init__(self, x, y, **kwargs):
        super(Church, self).__init__(x, y, **kwargs)
        self.set_sprite(pyglet.sprite.Sprite(self._image))


class Creek(Prop):
    collision_effect = None
    _image = pyglet.resource.image('img/sprites/creek.png')
    _grid = pyglet.image.ImageGrid(_image, 1, 2)
    _anim = _grid.get_animation(1.0, True)
    builder_data = {'width':5, 'height':9,
            'x_variance': 20}

    def __init__(self, x, y, **kwargs):
        super(Creek, self).__init__(x, y, **kwargs)
        self.set_sprite(pyglet.sprite.Sprite(self._anim))


class Skeleton(Prop):
    collision_effect = None
    _image = pyglet.resource.image('img/sprites/skeleton.png')
    builder_data = {'width':1, 'height':1,
            'x_variance': 14, 'y_variance': 4}

    def __init__(self, x, y, **kwargs):
        super(Skeleton, self).__init__(x, y, **kwargs)
        self.set_sprite(pyglet.sprite.Sprite(self._image))


# Actors


class Pebble(Projectile):
    _image = pyglet.resource.image('img/sprites/pebble.png')
    _frame_data = {'thrown': ((0, 3), 0.2, True)}
    animations = Actor.make_animations(_image, 3, _frame_data)
    collision_effect = {'effect_type': 'trip', 'duration': 0.2}

    def __init__(self):
        super(Pebble, self).__init__()
        self.set_sprite(AnimatedSprite(self.animations, default='thrown'))
        self.add_collider(collider.Collider(3, 3, width=1, height=1,
                layer=HASH_AIR, effect=self.collision_effect))

    def on_collision(self, other, rect, speed, effect):
        pass  # self.kill()


class Peasant(Actor):
    _image = pyglet.resource.image('img/sprites/peasant.png')
    _frame_data = {
            'idle': ((0, 2), 1.1, True),
            'run': ((2, 4), 0.2, True),
            'notice': ((4, 6), 1.2, True),
            'aim': ((6, 8), 0.2, True),
            'throw': ((8, 9), 1.2, True),
            'leap': ((9,10), 1, True),
            'trip': ((10,11), 1, True),
            'down': ((11,12), 1, True)
            }
    required_classes = [Pebble]
    animations = Actor.make_animations(_image, 12, _frame_data)

    max_speed = 60.0
    acceleration = (100, 100)
    collision_effect = ('trip', 0.5)

    FIRST_AIM_DELAY = 1.2
    AIM_DELAY = 0.6
    THROW_DELAY = 0.3
    LEAP_SPEED = (220, 0)
    LEAP_TIME = 0.4

    def __init__(self, x, y, **kwargs):
        super(Peasant, self).__init__(x, y, **kwargs)
        self.set_sprite(AnimatedSprite(self.animations, default='idle'))
        self.add_collider(collider.Collider(0,0,30,20, layer=1))
        self.add_collider(collider.Detector(60))
        self.speed = (0, 0)
        self.target = None
        self.next_action_delay = 0.0

    def update_speed(self, dt):
        pass

    def move(self, dt, stage_offset):
        # self.behave(dt)
        Actor.move(self, dt, stage_offset)

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
        self.speed = (0, 0)
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
            self.speed = (0, 0)
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
            self.speed = (0, 0)
            self.behavior = self.behave_down


    def behave_trip(self, dt):
        self.play('trip')
        self.approach_target_speed(dt, (0, 0))
        if self.speed[0] < 20:
            self.speed = (0, 0)
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

    def on_collision(self, other, rect, speed, effect):
        if effect is not None and effect['effect_type'] in ['stun', 'trip']:
            self.behavior = self.behave_trip


class PeasantB(Peasant):
    _image = pyglet.resource.image('img/sprites/peasant_rc0.png')

    max_speed = 60.0
    acceleration = (100, 100)
    # collision_effect = ('trip', 0.5)

    FIRST_AIM_DELAY = 0.6
    AIM_DELAY = 0.3
    NUMBER_OF_THROWS = 4

    def update_speed(self, dt):
        pass

    def move(self, dt, stage_offset):
        # self.behave(dt)
        Actor.move(self, dt, stage_offset)

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
            self.speed = (0, 0)
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


class PeasantC(PeasantB):
    _image = pyglet.resource.image('img/sprites/peasant_rc1.png')
    FIRST_AIM_DELAY = 0.6
    AIM_DELAY = 0.1
    THROW_DELAY = 0.1
    NUMBER_OF_THROWS = 8

    max_speed = 300

    def reset(self, x, y):
        Actor.reset(self, x, y)
        self.target = None
        self.frustration = 0
        self.behavior = self.behave_idle
        self.aiming = False
        self.throwing = False
        self.sprite.color = (63, 0, 0)


class Preacher(Actor):
    _image = pyglet.resource.image('img/sprites/preacher.png')
    _frame_data = {
            'idle': ((0, 2), 1.1, True),
            'run': ((2, 4), 0.2, True),
            'notice': ((4, 6), 1.2, True),
            'aim': ((6, 8), 0.2, True),
            'strike': ((8, 9), 0.4, True),
            'command': ((9, 11), 0.2, True),
            'crouch': ((11, 13), 0.2, True),
            'charge': ((13, 15), 0.2, True)
            }
    animations = Actor.make_animations(_image, 15, _frame_data)

    max_speed = 120.0
    acceleration = (100, 100)
    collision_effect = ('trip', 0.5)

    def __init__(self, x, y, **kwargs):
        super(Preacher, self).__init__(x, y, **kwargs)
        self.set_sprite(AnimatedSprite(self.animations, default='idle'))
        self.add_collider(collider.Collider(0,0,30,20, layer=1))
        self.speed = (120, 0)
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
