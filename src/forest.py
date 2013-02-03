import logging
log = logging.getLogger(__name__)

import pyglet
from prop import *


class Tree(Prop):
    collision_effect = {'effect_type': 'stun', 'duration': 0.5}
    _image = pyglet.resource.image('img/sprites/tree.png')

    def __init__(self, x, y, **kwargs):
        super(Tree, self).__init__(x, y, **kwargs)
        self.set_sprite(pyglet.sprite.Sprite(self._image))
        '''self.add_collider(collider.Collider(5, 10, 25, 30,
                effect=self.collision_effect, layer=HASH_GROUND))'''


BUILDER_NAMES = {
    'PROP_TREE': Tree,
}
