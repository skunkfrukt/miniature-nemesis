import logging
log = logging.getLogger(__name__)

import pyglet
import math
from gameobject import AnimatedGameObject
from projectile import Projectile
from pyglet.window import key

from vector import *

MIN_Y, MAX_Y = 0, 275


status_severity = {
        'ok': 0,
        'rise': 3,
        'tumble': 2,
        'trip': 1,
        'stun': 4,
        'dead': 999
        }


class Actor(AnimatedGameObject):
    max_speed = 0.0
    acceleration = Vector(100, 100)

    def __init__(self, position, size, **kwargs):
        super(Actor, self).__init__(position, size, layer=1, **kwargs)
        self.direction = VECTOR_NULL
        self.speed = VECTOR_NULL
        self.next_action_delay = 0.0
        self.current_action_priority = 0
        self.status = 'ok'

    def wait(self, duration, priority=0):
        self.current_action_priority = priority
        self.next_action_delay = duration

    def update_speed(self, dt):
        if self.status == 'ok':
            target_speed = self.direction * self.max_speed + VECTOR_EAST * 100
            self.approach_target_speed(dt, target_speed)
        elif self.status == 'rise':
            if self.next_action_delay <= 0:
                self.apply_status('ok', force=True)
        elif self.status == 'tumble':
            if self.speed[0] < 1:
                self.apply_status('rise', force=True)
            else:
                self.approach_target_speed(dt, VECTOR_NULL)
        elif self.status == 'trip':
            if self.next_action_delay <= 0:
                self.apply_status('tumble', force=True)
        elif self.status == 'stun':
            if self.next_action_delay <= 0:
                self.speed = VECTOR_NULL
                self.apply_status('ok', force=True)
        self.next_action_delay -= dt

    def approach_target_speed(self, dt, target):
        ##TODO## Do this is a nicer way with vectors.
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
        self.speed = Vector(dx, dy)

    def update(self, dt):
        self.behave(dt)
        self.update_speed(dt)
        super(Actor, self).update(dt)
        self.animate()

    def animate(self):
        pass

    '''def reset(self, position):
        self.speed = VECTOR_NULL
        super(Actor, self).reset(position)
        self.apply_status('ok')'''

    def fire_projectile(self, projectile_cls, speed, target=None):
        origin = self.position
        if target is not None:
            target_pos = target.position
        else:
            target_pos = origin + VECTOR_EAST
        self.dispatch_event('on_projectile_fired',
                projectile_cls, origin, target_pos, speed)

    def reset(self, position):
        super(Actor, self).reset(position)
        self.dispatch_event('on_spawn', self, position)

Actor.register_event_type('on_projectile_fired')
Actor.register_event_type('on_spawn')
