import pyglet
import math
from pyglet.window import key

class Actor(pyglet.sprite.Sprite):
    @classmethod
    def make_animations(cls, image, number_of_frames, frame_data):
        """Makes an animation set for an Actor subclass.
        
        Keyword arguments:
        image -- the image to be used as a sprite sheet
        number_of_frames
        frame_data -- data on how to process the sprite sheet
        
        The frame data is given in the form of a dictionary,
        where the keys are the names of the animations, and the
        values are tuples following this formula:
            ((fa, fz), speed, loop),
        where fa and fz are the start and end index of the frames
        to be used, speed is the duration of each frame, and
        loop is a boolean value determining whether to loop the
        animation.
        
        """
        fis = pyglet.image.Animation.from_image_sequence
        grid = pyglet.image.ImageGrid(image, 1, number_of_frames)
        animations = {}
        for name, template in frame_data.items():
            animations[name] = fis(grid[slice(*template[0])], *template[1:])
        return animations

    def __init__(self, animations=None, default=None):
        if animations is not None:
            self.animations = animations
        if default is None:
            default = self.animations.keys()[0]
            print("No default anim; using %s" % default)
        pyglet.sprite.Sprite.__init__(self, self.animations[default])
    
    def play(self, animation):
        if animation in self.animations:
            self.image = self.animations[animation]
        else:
            print("WARNING: %s tried to play invalid animation %s" %
                  (self, animation))


class Hero(Actor):
    _image = pyglet.resource.image('img/sprites/hero__sprite.png')
    _frame_data = {'run': ((0, 2), 0.12, True),
                   'sprint': ((2, 4), 0.12, True),
                   'stop': ((4, 6), 0.12, True)}
    animations = Actor.make_animations(_image, 6, _frame_data)

    def __init__(self):
        Actor.__init__(self, default='run')
        self.dx = 0.0
        self.dy = 0.0
        self.speed = 80.0

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


class Woodpecker(Actor):
    _image = pyglet.resource.image('img/sprites/woodpecker__sprite.png')
    _frame_data = {'fly': ((0, 2), 0.1, True)}
    animations = Actor.make_animations(_image, 2, _frame_data)

    def __init__(self):
        Actor.__init__(self, default='fly')
        self.dx = 0.0
        self.dy = 0.0
        self.speed = 1.0
        self.angle = math.pi / 2.0

