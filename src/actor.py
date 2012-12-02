import pyglet
import math
import collider
from common import AnimatedSprite, GameObject, Projectile
from pyglet.window import key
from constants import *

import logging
log = logging.getLogger(__name__)

MIN_Y, MAX_Y = 0, 275


status_severity = {
        'ok': 0,
        'rise': 3,
        'tumble': 2,
        'trip': 1,
        'stun': 4,
        'dead': 999
        }


class Actor(GameObject):
    max_speed = 0.0
    acceleration = (100, 100)
    preferred_rendering_group_index = R_GROUP_ACTORS_BACK

    @classmethod
    def make_animations(cls, image, number_of_frames, frame_data):
        fis = pyglet.image.Animation.from_image_sequence
        grid = pyglet.image.ImageGrid(image, 1, number_of_frames)
        animations = {}
        for name, template in frame_data.items():
            animations[name] = fis(grid[slice(*template[0])], *template[1:])
        return animations

    def __init__(self):
        super(Actor, self).__init__()
        self.collider = None
        self.direction = (0, 0)
        self.speed = (0.0, 0.0)
        self.next_action_delay = 0.0
        self.current_action_priority = 0
        self.status = 'ok'
        self.apply_status('ok')

    def play(self, animation):
        self.sprite.play(animation)

    def wait(self, duration, priority=0):
        self.current_action_priority = priority
        self.next_action_delay = duration

    def update_speed(self, dt):
        if self.status == 'ok':
            dirx, diry = self.direction
            tx, ty = 100 + dirx * self.max_speed, diry * self.max_speed
            self.approach_target_speed(dt, (tx, ty))
        elif self.status == 'rise':
            if self.next_action_delay <= 0:
                self.apply_status('ok', force=True)
        elif self.status == 'tumble':
            if self.speed[0] < 1:
                self.apply_status('rise', force=True)
            else:
                self.approach_target_speed(dt, (0,0))
        elif self.status == 'trip':
            if self.next_action_delay <= 0:
                self.apply_status('tumble', force=True)
        elif self.status == 'stun':
            if self.next_action_delay <= 0:
                self.speed = (0, 0)
                self.apply_status('ok', force=True)
        self.next_action_delay -= dt

    def approach_target_speed(self, dt, target=(0, 0)):
        dx, dy = self.speed
        tx, ty = target
        ax, ay = self.acceleration
        if tx < dx:
            dx -= ax * dt
            dx = max(dx, tx)
        elif tx > dx:
            dx += ax * dt
            dx = min(dx, tx)
        if ty < dy:
            dy -= ay * dt
            dy = max(dy, ty)
        elif ty > dy:
            dy += ay * dt
            dy = min(dy, ty)
        self.speed = (dx, dy)

    def move(self, dt, stage_offset):
        self.update_speed(dt)
        GameObject.move(self, dt, stage_offset)
        self.animate()

    def animate(self):
        pass

    def apply_status(self, effect_type=None, priority=0, force=False,
            **kwargs):
        if not force:
            # temp:
            if effect_type in status_severity:
                priority = status_severity[effect_type]
            # end temp
            if priority <= self.current_action_priority:
                return False
        try:
            effect_method = getattr(self, effect_type)
        except AttributeError:
            log.debug('{} has no method {}'.format(self, effect_type))
        else:
            effect_method(**kwargs)
            self.status = effect_type

    def stun(self, duration=0.5, **kwargs):
        self.speed = (-100, 0)
        self.wait(duration, priority=4)

    def stop(self, directions='nesw', **kwargs):
        dx, dy = self.speed
        dir_x, dir_y = cmp(dx, 0), cmp(dy, 0)
        if dir_x < 0 and 'w' in directions:
            dx = 0
        elif dir_x > 0 and 'e' in directions:
            dx = 0
        if dir_y < 0 and 's' in directions:
            dy = 0
        elif dir_y > 0 and 'n' in directions:
            dy = 0
        self.speed = (dx, dy)
        self.status = 'ok'

    def trip(self, duration=0.2, **kwargs):
        self.wait(duration, priority=1)

    def ok(self, **kwargs):  # temp
        self.wait(0)

    def rise(self, **kwargs):  # temp
        self.speed = (0, 0)
        self.wait(0.3, priority=3)

    def tumble(self, **kwargs):  # temp
        self.speed = (self.max_speed * 2, 0)
        self.wait(1.0, priority=2)

    def dead(self, **kwargs):  # temp
        self.speed = (0, 0)

    def setup_sprite(self, batch, group):
        if self.sprite is not None:
            if batch is not None:
                self.sprite.batch = batch
            if group is not None:
                self.sprite.group = group

    def reset(self, x, y):
        self.speed = (0,0)
        super(Actor, self).reset(x, y)
        self.apply_status('ok')

    def fire_projectile(self, projectile_cls, speed, target=None):
        origin_x = self.x + 30
        origin_y = self.y + 30
        if target is not None:
            target_x, target_y = target.x + 100, target.y + 25
        else:
            target_x = self.x  # origin_x + 1
            target_y = self.y  # origin_y
        self.dispatch_event('on_projectile_fired',
                projectile_cls, origin_x, origin_y,
                target_x, target_y, speed)

    def reset(self, x, y):
        GameObject.reset(self, x, y)
        self.dispatch_event('on_spawn', self, x, y)

    def add_collider(self, collider):
        collider.parent = self
        GameObject.add_collider(self, collider)

Actor.register_event_type('on_projectile_fired')
Actor.register_event_type('on_spawn')


class Hero(Actor):
    _image = pyglet.resource.image('img/sprites/anim_hero.png')
    _frame_data = {
            'idle': ((0, 2), 0.12, True),
            'run': ((2, 4), 0.12, True),
            'sprint': ((4, 6), 0.12, True),
            'stop': ((6, 8), 0.12, True),
            'hurt': ((8, 10), 0.12, False),
            'trip': ((10, 11), 0.12, False),
            'tumble': ((11, 13), 0.12, True),
            'rise': ((13, 14), 0.12, False)
            }
    animations = Actor.make_animations(_image, 14, _frame_data)
    preferred_rendering_group_index = R_GROUP_HERO

    max_speed = 80.0
    acceleration = (200, 400)

    def __init__(self):
        super(Hero, self).__init__()
        self.set_sprite(AnimatedSprite(self.animations, default='run'))
        self.add_collider(collider.Collider(11, 0, width=20, height=10,
                layer=HASH_GROUND))
        self.add_collider(collider.Collider(13, 14, width=18, height=26,
                layer=HASH_AIR))
        self.add_collider(collider.Collider(0, 0,
                width=self.width, height=self.height, layer=HASH_TRIGGER))

    def fixSpeed(self, keys):
        dirx = 0
        diry = 0
        if keys[key.W] or keys[key.UP]:
            diry += 1
        if keys[key.S] or keys[key.DOWN]:
            diry -= 1
        if keys[key.A] or keys[key.LEFT]:
            dirx -= 1
        if keys[key.D] or keys[key.RIGHT]:
            dirx += 1
        self.direction = (dirx, diry)

    def move(self, dt, stage_offset):
        dirx, diry = self.direction
        Actor.move(self, dt, stage_offset)

    def animate(self):
        dirx, diry = self.direction
        if self.status == 'stun':
            self.play('hurt')
        elif self.status == 'trip':
            self.play('trip')
        elif self.status == 'tumble':
            self.play('tumble')
        elif self.status == 'rise':
            self.play('rise')
        elif self.status == 'ok':
            if dirx > 0:
                self.play('sprint')
            elif dirx < 0 and self.speed[0] > 0:
                self.play('stop')
            else:
                self.play('run')

    def on_collision(self, other, rect, speed, effect):
        if effect:
            self.apply_status(**effect)


class Pebble(Projectile):
    _image = pyglet.resource.image('img/sprites/missile_pebble_minimal.png')
    _frame_data = {'thrown': ((0, 3), 0.2, True)}
    animations = Actor.make_animations(_image, 3, _frame_data)
    collision_effect = {'effect_type': 'trip', 'duration': 1.0}

    def __init__(self):
        super(Pebble, self).__init__()
        self.set_sprite(AnimatedSprite(self.animations, default='thrown'))
        self.add_collider(collider.Collider(3, 3, width=1, height=1,
                layer=HASH_AIR, effect=self.collision_effect))

    def on_collision(self, other, rect, speed, effect):
        pass  # self.kill()


class Peasant(Actor):
    _image = pyglet.resource.image('img/sprites/anim_peasant-a.png')
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

    def __init__(self):
        super(Peasant, self).__init__()
        self.set_sprite(AnimatedSprite(self.animations, default='idle'))
        self.add_collider(collider.Collider(0,0,30,20, layer=HASH_GROUND))
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
        if self.target is not None:
            self.play('notice')
            self.next_action_delay = 0.4
            self.behavior = self.behave_notice

    def behave_notice(self, dt):
        self.play('notice')
        if self.next_action_delay <= 0:
            self.behavior = self.behave_pursue

    def behave_pursue(self, dt):
        self.play('run')
        self.pursue(self.target, dt)
        dist_x = self.target.x - 60 - self.x
        if dist_x > 300:
            self.frustration += dt + dt
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


    def pursue(self, target, dt):
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
        tx, ty = dirx * (100 + self.max_speed), diry * (100 + self.max_speed)
        self.approach_target_speed(dt, (tx, ty))


    def on_detection(self, target):
        if self.target is None and type(target) is Hero:
            if abs(self.y - target.y) < 200:
                self.target = target


class PeasantB(Peasant):

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
    _image = pyglet.resource.image('img/sprites/anim_priest.png')
    _frame_data = {
            'run': ((0, 2), 0.2, True),
            }
    animations = Actor.make_animations(_image, 2, _frame_data)

    max_speed = 120.0
    acceleration = (100, 100)
    collision_effect = ('trip', 0.5)

    def __init__(self):
        super(Preacher, self).__init__()
        self.set_sprite(AnimatedSprite(self.animations, default='run'))
        self.add_collider(collider.Collider(0,0,30,20, layer=HASH_GROUND))
        self.speed = (120, 0)
        self.target = None
        self.next_action_delay = 0.0
