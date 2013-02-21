import logging
log = logging.getLogger(__name__)

import pyglet
import math
from gameobject import AnimatedGameObject
from projectile import Projectile
from pyglet.window import key

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
    acceleration = (100, 100)
    preferred_rendering_group_index = 2

    def __init__(self, x, y, **kwargs):
        super(Actor, self).__init__(x, y, **kwargs)
        self.collider = None
        self.direction = (0, 0)
        self.speed = (0.0, 0.0)
        self.next_action_delay = 0.0
        self.current_action_priority = 0
        self.status = 'ok'
        # self.apply_status('ok')

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

    def update(self, dt):
        self.behave(dt)
        self.update_speed(dt)
        super(Actor, self).update(dt)
        self.animate()

    def animate(self):
        pass

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
        super(Actor, self).reset(x, y)
        self.dispatch_event('on_spawn', self, x, y)

Actor.register_event_type('on_projectile_fired')
Actor.register_event_type('on_spawn')
