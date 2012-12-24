import pyglet

class AnimatedSprite(pyglet.sprite.Sprite):
    def __init__(self, animations=None, default=None):
        self.animations = animations
        if default is None:
            default = self.animations.keys()[0]
            print("No default anim; using %s" % default)
        super(AnimatedSprite, self).__init__(self.animations[default])
        self.current_animation = default

    def play(self, animation):
        if animation == self.current_animation:
            return
        elif animation in self.animations:
            self.image = self.animations[animation]
            self.current_animation = animation
        else:
            print("WARNING: %s tried to play invalid animation %s" %
                  (self, animation))
