import pyglet

afis = pyglet.image.Animation.from_image_sequence

import logging
log = logging.getLogger(__name__)


class AnimSet(object):
    def __init__(self, name, image, rows, cols):
        self.name = name
        self.anims = {}
        self.grid = None
        self.set_image_grid(image, rows, cols)

        log.debug(D_INIT.format(obj=self))

    def set_image_grid(self, image, rows, cols):
        self.grid = pyglet.image.ImageGrid(image, rows, cols)

    def add_anim(self, key, frames, period, loop):
        if key in self.anims:
            log.warning(W_DUPLICATE_ANIM.format(key=key, animset=self.name))
        anim = afis([self.grid[f] for f in frames], period, loop)
        if len(self.anims) == 0:
            self.anims[None] = anim
        self.anims[key] = anim

        log.debug(D_ADD_ANIM.format(key=key, animset=self.name))

    def get_anim(self, key):
        try:
            return self.anims[key]
        except KeyError:
            log.error(E_NO_SUCH_ANIM.format(key=key, animset=self.name))


E_NO_SUCH_ANIM = 'No Anim {key} in AnimSet {animset}.'
W_DUPLICATE_ANIM = 'Anim {key} already exists in AnimSet {animset}.'
D_ADD_ANIM = 'Added Anim {key} to AnimSet {animset}.'
D_INIT = 'Initialised {obj.__class__.__name__} {obj.name}.'
