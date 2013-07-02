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
    acceleration = 100
    despawn_on_exit = False

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
            self.accelerate(dt, target_speed)
        elif self.status == 'rise':
            if self.next_action_delay <= 0:
                self.apply_status('ok', force=True)
        elif self.status == 'tumble':
            if self.speed.x == 0:
                self.apply_status('rise', force=True)
            else:
                self.accelerate(dt/2.0, VECTOR_NULL)
        elif self.status == 'trip':
            if self.next_action_delay <= 0:
                self.apply_status('tumble', force=True)
        elif self.status == 'knockback':
            if self.speed.x == 0:
                self.apply_status('ok', force=True)
            else:
                self.accelerate(dt, VECTOR_NULL)
        self.next_action_delay -= dt

    def accelerate(self, dt, target_speed):
        diff = target_speed - self.speed
        frame_acceleration = self.acceleration * dt
        if diff.length <= frame_acceleration:
            self.speed = target_speed
        else:
            self.speed += diff.unit * frame_acceleration

    def update(self, dt):
        self.behave(dt)
        self.update_speed(dt)
        super(Actor, self).update(dt)
        self.animate()

    def animate(self):
        pass

    def fire_projectile(self, projectile):
        self.dispatch_event('on_emit', projectile)

    def reset(self, position):
        super(Actor, self).reset(position)
        self.dispatch_event('on_spawn', self, position)

Actor.register_event_type('on_emit')
Actor.register_event_type('on_spawn')
