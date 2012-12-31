import logging
log = logging.getLogger(__name__)

import pyglet

class GameObject(pyglet.event.EventDispatcher):
    '''Superclass of all objects that are drawn on stage.'''
    preferred_rendering_group_index = None
    required_classes = []

    def __init__(self, x, y, layer=0, **kwargs):
        if len(kwargs) > 0:
            log.warning(W_EXTRA_KWARGS.format(kwargs=kwargs))
        self.x, self.y = x, y
        self.relative_layer = kwargs.pop('layer', 0)
        # self.kill()
        self.behavior = None
        self.width = 1
        self.height = 1
        self.speed = None
        self.sprite = None
        self.collider = None
        self.colliders = None
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
        self.width = self.sprite.width
        self.height = self.sprite.height

    def setup_sprite(self, batch, group):
        assert self.sprite is not None, "%s setting up None-sprite." % self
        self.sprite.batch = batch
        self.sprite.group = group

    def update_sprite(self, stage_offset):
        self.sprite.position = (int(self.x - stage_offset), int(self.y))

    def check_despawn(self, stage_offset):
        if self.right <= stage_offset:
            return True
        return False

    def despawn(self):
        self.sprite.delete()
        self.kill()
        self.dispatch_event('on_despawn', self)

    def update(self, dt):
        if self.speed is not None:
            dx, dy = (spd * dt for spd in self.speed)
            self.x += dx
            self.y += dy
        else:
            dx, dy = 0, 0
        if self.colliders is not None:
            for collider in self.colliders:
                collider.move(self.x, self.y, (dx, dy))

    def behave(self, dt):
        if self.behavior is not None:
            self.behavior(dt)

    def add_collider(self, collider):
        if collider is None:
            return
        if self.colliders is None:
            self.colliders = []
        collider.parent = self
        self.colliders.append(collider)
        collider.move(self.x, self.y)
        collider.push_handlers(self)

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

    def on_collision(self, other, rect, speed, effect):
        pass

GameObject.register_event_type('on_despawn')


W_EXTRA_KWARGS = 'GameObject received extra kwargs: {kwargs}.'
