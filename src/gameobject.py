import logging
log = logging.getLogger(__name__)

import pyglet

import spritehandler
SH = spritehandler

from graphics import AnimSet

class GameObject(pyglet.event.EventDispatcher):
    '''Superclass of all objects that are drawn on stage.'''
    required_classes = []

    def __init__(self, x, y, layer=0, **kwargs):
        if len(kwargs) > 0:
            log.warning(W_EXTRA_KWARGS.format(kwargs=kwargs))
        self.x, self.y = x, y
        # self.kill()
        self.behavior = None
        self.width = None
        self.height = None
        self.speed = None
        self.sprite = None
        self.layer = layer

    def kill(self):
        pass
        self.x = 0
        self.y = 360
        self.dead = True

    def reset(self, x, y):
        self.x, self.y = x, y
        self.dead = False

    def set_sprite(self, sprite):
        self.sprite = sprite
        self.width = self.width or self.sprite.width
        self.height = self.height or self.sprite.height

    def allocate_sprite(self):
        assert self.sprite is None
        self.sprite = SH.get_sprite(SH.FG, self.layer)

    def update_sprite(self, stage_offset):
        self.sprite.position = (int(self.x - stage_offset), int(self.y))

    def set_image(self, image):
        self.sprite.image = image

    def check_despawn(self, stage_offset):
        if self.right <= stage_offset:
            return True
        return False

    def despawn(self):
        spritehandler.recycle(self.sprite)
        self.sprite = None
        self.dispatch_event('on_despawn', self)

    def update(self, dt):
        if self.speed is not None:
            dx, dy = (spd * dt for spd in self.speed)
            self.x += dx
            self.y += dy
        else:
            dx, dy = 0, 0

    def behave(self, dt):
        if self.behavior is not None:
            self.behavior(dt)

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, value):
        self.x = value

    @property
    def right(self):
        return self.x + self.width

    @right.setter
    def right(self, value):
        self.x = value - self.width

    @property
    def bottom(self):
        return self.y

    @bottom.setter
    def bottom(self, value):
        self.y = value

    @property
    def top(self):
        return self.y + self.height

    @top.setter
    def top(self, value):
        self.y = value - self.height

    @property
    def rect(self):
        return (self.left, self.bottom, self.right, self.top)

GameObject.register_event_type('on_despawn')


class AnimatedGameObject(GameObject):
    anim_set = None

    def __init__(self, x, y, layer=0, **kwargs):
        super(AnimatedGameObject, self).__init__(x, y, layer, **kwargs)
        self.current_anim = None

    def play(self, anim_key, force_restart=False):
        if force_restart or anim_key != self.current_anim:
            self.set_image(self.anim_set.get_anim(anim_key))
            self.current_anim = anim_key


W_EXTRA_KWARGS = 'GameObject received extra kwargs: {kwargs}.'
