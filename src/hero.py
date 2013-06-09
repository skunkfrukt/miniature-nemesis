import logging
log = logging.getLogger(__name__)

import random

import pyglet

from pyglet.window import key

from actor import Actor

from vector import *


HITBOX_HERO = Vector(16, 16)
OFFSET_HERO = Vector(-14, -3)


class Hero(Actor):
    _anim_set = "ANIMSET_HERO"

    max_speed = 80.0
    acceleration = 200

    def __init__(self, position):
        super(Hero, self).__init__(position, HITBOX_HERO, offset=OFFSET_HERO)

    def fixSpeed(self, keys):
        dir = VECTOR_NULL
        if keys[key.W] or keys[key.UP]:
            dir += VECTOR_NORTH
        if keys[key.S] or keys[key.DOWN]:
            dir += VECTOR_SOUTH
        if keys[key.A] or keys[key.LEFT]:
            dir += VECTOR_WEST
        if keys[key.D] or keys[key.RIGHT]:
            dir += VECTOR_EAST
        self.direction = dir

    def move(self, dt, stage_offset):
        Actor.move(self, dt, stage_offset)

    def animate(self):
        if self.status == 'stun':
            self.play('hurt')
        elif self.status == 'trip':
            self.play('trip')
        elif self.status == 'tumble':
            self.play('tumble')
        elif self.status == 'rise':
            self.play('rise')
        elif self.status == 'ok':
            if self.direction.x > 0:
                self.play('sprint')
            elif self.direction.x < 0 and self.speed.x > 0:
                self.play('stop')
            else:
                self.play('run')

    def collide(self, other, vector, direction):
        super(Hero, self).collide(other, vector, direction)
        other.send_effect('hero_hit')

    def send_effect(self, effect, **kwargs):
        if effect == 'trip':
            log.info('Jean-Baptiste Flynn tripped!')
            pass
        elif effect == 'knockback':
            log.info('Jean-Baptiste Flynn was knocked back!!')
            self.speed = Vector(-150, 0)
        elif effect == 'wall':
            log.info('Jean-Baptiste Flynn ran into a wall!!!')
            self.speed = Vector(-250, 0)
        elif effect == 'drown':
            log.info('Jean-Baptiste Flynn drowned!!!!')
        elif effect == 'burn':
            log.info('Jean-Baptiste Flynn was burnt to a crisp!!!!!')

