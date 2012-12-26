import logging
log = logging.getLogger(__name__)

import pyglet
from _baseclasses.prop import *


class Rock(Prop):
    collision_effect = {'effect_type': 'stun', 'duration': 0.5}
    _image = pyglet.resource.image('img/sprites/rock.png')

    def __init__(self, x, y, **kwargs):
        super(Rock, self).__init__(x, y, **kwargs)
        self.set_sprite(pyglet.sprite.Sprite(self._image))
        '''self.add_collider(collider.Collider(5, 10, 25, 30,
                effect=self.collision_effect, layer=HASH_GROUND))'''


class Stone(Prop):
    BUILDER_NAME = 'PROP_STONE'
    collision_effect = {'effect_type': 'trip', 'duration': 0.75}
    _image = pyglet.resource.image('img/sprites/stone.png')

    def __init__(self, x, y, **kwargs):
        super(Stone, self).__init__(x, y, **kwargs)
        self.set_sprite(pyglet.sprite.Sprite(self._image))
        '''self.add_collider(collider.Collider(0, 0, 10, 10,
                effect=self.collision_effect, layer=HASH_GROUND))'''


class House(Prop):
    num = 0
    collision_effect = {'effect_type': 'stun', 'duration': 0.5}
    _images = pyglet.image.ImageGrid(
            pyglet.resource.image('img/sprites/house.png'),
            1, 3)

    def __init__(self, x, y, **kwargs):
        super(House, self).__init__(x, y, **kwargs)
        self.set_sprite(pyglet.sprite.Sprite(self._images[House.num % 3]))
        '''self.add_collider(collider.Collider(
                left=0, right=20, bottom=20, top=180,
                effect={'effect_type': 'stun', 'duration': 0.5},
                layer=HASH_GROUND))
        self.add_collider(collider.Collider(
                left=20, right=180, bottom=0, top=20,
                effect={'effect_type': 'stop', 'directions': 'n'},
                layer=HASH_GROUND))'''
        House.num += 1


class HeroHouse(House):
    collision_effect = {'effect-type': 'stun', 'duration': 0.5}
    _image = pyglet.resource.image('img/sprites/herohouse.png')

    def __init__(self, x, y, **kwargs):
        super(HeroHouse, self).__init__(x, y, **kwargs)
        self.set_sprite(pyglet.sprite.Sprite(self._image))


class Church(Prop):
    collision_effect = {'effect-type': 'stun', 'duration': 0.5}
    _image = pyglet.resource.image('img/sprites/church.png')

    def __init__(self, x, y, **kwargs):
        super(Church, self).__init__(x, y, **kwargs)
        self.set_sprite(pyglet.sprite.Sprite(self._image))


class Creek(Prop):
    collision_effect = None
    _image = pyglet.resource.image('img/sprites/creek.png')
    _grid = pyglet.image.ImageGrid(_image, 1, 2)
    _anim = _grid.get_animation(1.0, True)

    def __init__(self, x, y, **kwargs):
        super(Creek, self).__init__(x, y, **kwargs)
        self.set_sprite(pyglet.sprite.Sprite(self._anim))

class Skeleton(Prop):
    collision_effect = None
    _image = pyglet.resource.image('img/sprites/skeleton.png')

    def __init__(self, x, y, **kwargs):
        super(Skeleton, self).__init__(x, y, **kwargs)
        self.set_sprite(pyglet.sprite.Sprite(self._image))


BUILDER_NAMES = {
    'PROP_CHURCH': Church,
    'PROP_CREEK': Creek,
    'PROP_HEROHOUSE': HeroHouse,
    'PROP_HOUSE': House,
    'PROP_ROCK': Rock,
    'PROP_SKELETON': Skeleton,
    'PROP_STONE': Stone
}
