import math
import pyglet


class AnimatedSprite(pyglet.sprite.Sprite):
    def __init__(self, animations=None, default=None):
        self.animations = animations
        if default is None:
            default = self.animations.keys()[0]
            print("No default anim; using %s" % default)
        pyglet.sprite.Sprite.__init__(self, self.animations[default])
        
    def play(self, animation):
        if animation == self.current_animation:
            return
        elif animation in self.animations:
            self.image = self.animations[animation]
            self.current_animation = animation
        else:
            print("WARNING: %s tried to play invalid animation %s" %
                  (self, animation))


class GameObject(pyglet.event.EventDispatcher):
    '''Superclass of all objects that are drawn on stage.'''
    def __init__(self):
        self.dead = True
        self.x, self.y = 0, 0
        
    def kill(self):
        self.dead = True
        
    def reset(self, x, y):
        self.x, self.y = x, y
        self.dead = False
        
        
class Point(object):
    '''A point in 2D space.'''
    def __init__(self, x, y):
        self.x = x
        self.y = y