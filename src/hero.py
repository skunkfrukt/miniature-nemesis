import logging
log = logging.getLogger(__name__)

import random

import pyglet

from pyglet.window import key

from actor import Actor

from vector import *


HITBOX_HERO = Vector(16, 16)
OFFSET_HERO = Vector(-14, -3)

SOUND_TRIP = pyglet.resource.media('sound/trip.wav', streaming=False)
SOUND_KNOCKBACK = pyglet.resource.media('sound/knockback.wav', streaming=False)
SOUND_WALL = pyglet.resource.media('sound/wall.wav', streaming=False)


class Hero(Actor):
    _anim_set = "ANIMSET_HERO"

    max_speed = 80.0
    acceleration = 200

    def __init__(self, position):
        super(Hero, self).__init__(position, HITBOX_HERO, offset=OFFSET_HERO)
        self.apply_status = self.send_effect

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

    def animate(self):
        if self.status == 'knockback':
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
            if self.status in ('ok',):
                SOUND_TRIP.play()
                log.info('Jean-Baptiste Flynn tripped!')
                self.status = 'trip'
                self.next_action_delay = 0.2
        elif effect == 'tumble':
            if self.status in ('trip',):
                self.status = 'tumble'
        elif effect == 'rise':
            if self.status in ('tumble',):
                self.status = 'rise'
                self.speed = VECTOR_NULL
                self.next_action_delay = 0.4
        elif effect == 'knockback':
            if self.status in ('ok', 'trip', 'tumble', 'rise'):
                SOUND_KNOCKBACK.play()
                log.info('Jean-Baptiste Flynn was knocked back!!')
                self.status = 'knockback'
                self.speed = self.speed * -0.5 + Vector(-100, 0)
        elif effect == 'wall':
            if self.status in ('ok', 'trip', 'tumble', 'rise'):
                SOUND_WALL.play()
                log.info('Jean-Baptiste Flynn ran into a wall!!!')
                self.status = 'knockback'
                self.speed = self.speed * -0.5 + Vector(-150, 0)
        elif effect == 'drown':
            if self.status in ('tumble', 'rise'):
                # Die ^_^
                log.info('Jean-Baptiste Flynn drowned!!!!')
            else:
                # We won't fall into the river if we can help it.
                self.send_effect('knockback')
        elif effect == 'burn':
            # Die \^_^/
            log.info('Jean-Baptiste Flynn was burnt to a crisp!!!!!')
        elif effect == 'ok': #TODO: Fulfix!
            self.status = 'ok'

