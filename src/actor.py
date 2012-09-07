import pyglet
import math
from pyglet.window import key

class Hero(pyglet.sprite.Sprite):
    def __init__(self):
        fis = pyglet.image.Animation.from_image_sequence
        guy_png = pyglet.resource.image('img/hero__spriteset00.png') # sprite sheet
        guy_grid = pyglet.image.ImageGrid(guy_png, 1, 6) # 1 row, 6 cols
        self.anims = {
            'run': fis(guy_grid[:2], 0.12, True),
            'sprint': fis(guy_grid[2:4], 0.12, True),
            'stop': fis(guy_grid[4:6], 0.12, True)
        }
        super(Hero, self).__init__(self.anims['run'])
        self.dx = 0.0
        self.dy = 0.0
        self.speed = 60.0
    
    def play(self, anim_name):
        if anim_name in self.anims:
            self.image = self.anims[anim_name]
            
    def fixSpeed(self, keys):
        self.dx = 0.0
        self.dy = 0.0
        if keys[key.W]:
            self.dy += self.speed
        if keys[key.S]:
            self.dy -= self.speed
        if keys[key.A]:
            self.dx -= self.speed
        if keys[key.D]:
            self.dx += self.speed
        if self.dx and self.dy:
            self.dx /= 1.4
            self.dy /= 1.4
        if self.dx > 0:
            self.play('sprint')
        elif self.dx < 0:
            self.play('stop')
        else:
            self.play('run')

class Woodpecker(pyglet.sprite.Sprite):
    def __init__(self):
        fis = pyglet.image.Animation.from_image_sequence
        wpeck_png = pyglet.resource.image('img/woodpecker__spritesheet00.png') # sprite sheet
        wpeck_grid = pyglet.image.ImageGrid(wpeck_png, 1, 2) # 1 row, 2 cols
        self.anims = {
            'fly': fis(wpeck_grid, 0.1, True)
        }
        super(Woodpecker, self).__init__(self.anims['fly'])
        self.dx = 0.0
        self.dy = 0.0
        self.speed = 1.0
        self.angle = math.pi / 2.0

