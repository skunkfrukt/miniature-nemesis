import logging
log = logging.getLogger(__name__)

import random

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
        self.speed = VECTOR_NULL
        self.sprite = None
        self.layer = layer
        '''try:
            hitbox_color = pyglet.image.SolidColorImagePattern((255,255,255,255))
            hitbox_img = hitbox_color.create_image(self.size.x, 1)
            hitbox_img2 = hitbox_color.create_image(1, self.size.y)
            self.image.blit_into(hitbox_img, -self.offset.x, -self.offset.y, 0)
            self.image.blit_into(hitbox_img, -self.offset.x, -self.offset.y + self.size.y, 0)
            self.image.blit_into(hitbox_img2, -self.offset.x, -self.offset.y, 0)
            self.image.blit_into(hitbox_img2, -self.offset.x + self.size.x, -self.offset.y, 0)
        except:
            try:
                for img in self.anim_set.grid:
                    hitbox_color = pyglet.image.SolidColorImagePattern((255,255,255,255))
                    hitbox_img = hitbox_color.create_image(self.size.x, 1)
                    hitbox_img2 = hitbox_color.create_image(1, self.size.y)
                    img.blit_into(hitbox_img, -self.offset.x, -self.offset.y, 0)
                    img.blit_into(hitbox_img, -self.offset.x, -self.offset.y + self.size.y, 0)
                    img.blit_into(hitbox_img2, -self.offset.x, -self.offset.y, 0)
                    img.blit_into(hitbox_img2, -self.offset.x + self.size.x, -self.offset.y, 0)
            except:
                pass #TODO: Remove this when no longer needed.'''

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

    def allocate_sprite(self):
        assert self.sprite is None
        self.sprite = SH.get_sprite(SH.FG, self.layer)

    def update_sprite(self):
        self.sprite.image = self.image

    def align_sprite(self, stage_offset):
        self.sprite.position = self.position + self.offset - stage_offset

    def set_image(self, image):
        self.sprite.image = image

    def despawn(self):
        self.recycle()
        self.dispatch_event('on_despawn', self)

    def recycle(self):
        spritehandler.recycle(self.sprite)
        self.sprite.color = (255, 255, 255)
        self.sprite = None

    def update(self, dt):
        if self.speed is not None:
            self.move(dt)

    def move(self, dt):
        self.position += self.speed * dt

    def behave(self, dt):
        if self.behavior is not None:
            self.behavior(dt)

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, value):
        self.position = Vector(value, self.y)

    @property
    def right(self):
        return self.x + self.width

    @right.setter
    def right(self, value):
        self.position = Vector(value - self.width, self.y)

    @property
    def bottom(self):
        return self.y

    @bottom.setter
    def bottom(self, value):
        self.position = Vector(self.x, value)

    @property
    def top(self):
        return self.y + self.height

    @top.setter
    def top(self, value):
        self.position = Vector(self.x, value - self.height)

    @property
    def rect(self):
        return (self.left, self.bottom, self.right, self.top)

    def show(self):
        self.sprite.visible = True

    @property
    def image(self):
        return self._image

    def collide(self, other, vector, direction):
        """ Handles a collision with another GameObject.

            other - what we're colliding with.
            vector - the collision vector seen from this object's perspective
                (i.e. as if this object were static).
            direction - the direction of the first impact.
        """
        r = random.randint(0, 1) * 255
        g = random.randint(0, 1) * 255
        b = random.randint(0, 1) * 255
        self.sprite.color = (r, g, b)

    def send_effect(self, effect, **kwargs):
        pass

GameObject.register_event_type('on_despawn')


class AnimatedGameObject(GameObject):
    _anim_set = None

    def __init__(self, position, size, **kwargs):
        super(AnimatedGameObject, self).__init__(position, size, **kwargs)
        self.current_anim = None

    def play(self, anim_key, force_restart=False):
        if force_restart or anim_key != self.current_anim:
            self.current_anim = anim_key
            self.update_sprite()

    @property
    def anim_set(self):
        return world.anim_sets[self._anim_set]

    def show(self):
        self.update_sprite()
        super(AnimatedGameObject, self).show()

    @property
    def image(self):
        return self.anim_set.get_anim(self.current_anim)


W_EXTRA_KWARGS = 'GameObject received extra kwargs: {kwargs}.'
