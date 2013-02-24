import logging
log = logging.getLogger(__name__)

import pyglet
from prop import *


from vector import *


HITBOX_TREE = Vector(1, 1)


class Tree(Prop):
    collision_effect = {'effect_type': 'stun', 'duration': 0.5}
    image = pyglet.resource.image('img/sprites/tree.png')

    def __init__(self, position, **kwargs):
        super(Tree, self).__init__(position, HITBOX_TREE, **kwargs)
        '''self.add_collider(collider.Collider(5, 10, 25, 30,
                effect=self.collision_effect, layer=HASH_GROUND))'''


BUILDER_NAMES = {
    'PROP_TREE': Tree,
}
