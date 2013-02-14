import pyglet

from pyglet.window import key

from actor import Actor

class Hero(Actor):
    _anim_set = "ANIMSET_HERO"

    max_speed = 80.0
    acceleration = (200, 400)

    def __init__(self):
        super(Hero, self).__init__(0, 0)

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

