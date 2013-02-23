import logging
log = logging.getLogger(__name__)

import pyglet

import spritehandler
SH = spritehandler

import world

from graphics import AnimSet
from vector import *


class GameObject(pyglet.event.EventDispatcher):
    def __init__(self, position, size, offset=VECTOR_NULL, layer=0, **kwargs):
        if len(kwargs) > 0:
            log.warning(W_EXTRA_KWARGS.format(kwargs=kwargs))
        self.position = position
        self.size = size
        self.offset = offset
        self.behavior = None
        self.speed = None
        self.sprite = None
        self.layer = layer

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    @property
    def width(self):
        return self.size.x

    @property
    def height(self):
        return self.size.y

    def kill(self):
        self.dead = True

    def set_sprite(self, sprite):
        self.sprite = sprite
        self.width = self.width or self.sprite.width
        self.height = self.height or self.sprite.height

    def allocate_sprite(self):
        assert self.sprite is None
        self.sprite = SH.get_sprite(SH.FG, self.layer)

    def update_sprite(self, stage_offset):
        self.sprite.position = (int(self.x - stage_offset), int(self.y))

    def align_sprite(self, stage_offset):
        self.sprite.position = self.position + self.offset - stage_offset

    def set_image(self, image):
        self.sprite.image = image

    def despawn(self):
        self.recycle()
        self.dispatch_event('on_despawn', self)

    def recycle(self):
        spritehandler.recycle(self.sprite)
        self.sprite = None

    def update(self, dt):
        if self.speed is not None:
            self.position += self.speed * dt

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

    def show(self):
        self.sprite.visible = True

GameObject.register_event_type('on_despawn')


class AnimatedGameObject(GameObject):
    _anim_set = None

    def __init__(self, position, size, **kwargs):
        super(AnimatedGameObject, self).__init__(position, size, **kwargs)
        self.current_anim = None

    def play(self, anim_key, force_restart=False):
        if force_restart or anim_key != self.current_anim:
            self.set_image(self.anim_set.get_anim(anim_key))
            self.current_anim = anim_key

    @property
    def anim_set(self):
        return world.anim_sets[self._anim_set]


W_EXTRA_KWARGS = 'GameObject received extra kwargs: {kwargs}.'
