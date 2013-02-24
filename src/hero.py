import pyglet

from pyglet.window import key

from actor import Actor

from vector import *


HITBOX_HERO = Vector(30, 20)
OFFSET_HERO = VECTOR_NULL


class Hero(Actor):
    _anim_set = "ANIMSET_HERO"

    max_speed = 80.0
    acceleration = Vector(200, 400)

    def __init__(self, position):
        super(Hero, self).__init__(position, HITBOX_HERO)

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

