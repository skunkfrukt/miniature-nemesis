import pyglet

from pyglet.window import key

from actor import Actor
from animatedsprite import AnimatedSprite

class Hero(Actor):
    _image = pyglet.resource.image('img/sprites/hero.png')
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
    preferred_rendering_group_index = 4  # R_GROUP_HERO

    max_speed = 80.0
    acceleration = (200, 400)

    def __init__(self):
        super(Hero, self).__init__(0, 0)
        self.set_sprite(AnimatedSprite(self.animations, default='run'))
        '''self.add_collider(collider.Collider(11, 0, width=20, height=10,
                layer=HASH_GROUND))
        self.add_collider(collider.Collider(13, 14, width=18, height=26,
                layer=HASH_AIR))
        self.add_collider(collider.Collider(0, 0,
                width=self.width, height=self.height, layer=HASH_TRIGGER))'''

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
