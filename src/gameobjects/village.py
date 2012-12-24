import pyglet
from _baseclasses.prop import *


class Rock(Prop):
    collision_effect = {'effect_type': 'stun', 'duration': 0.5}
    _image = pyglet.resource.image('img/sprites/rock__sprite.png')

    def __init__(self):
        super(Rock, self).__init__()
        self.set_sprite(pyglet.sprite.Sprite(self._image))
        self.add_collider(collider.Collider(5, 10, 25, 30,
                effect=self.collision_effect, layer=HASH_GROUND))


class DummyStone(Rock):
    pass

'''
class Stone(Prop):
    BUILDER_NAME = 'PROP_STONE'
    collision_effect = {'effect_type': 'trip', 'duration': 0.75}
    _image = pyglet.resource.image('REMOVED')

    def __init__(self):
        super(Stone, self).__init__()
        self.set_sprite(pyglet.sprite.Sprite(self._image))
        self.add_collider(collider.Collider(0, 0, 10, 10,
                effect=self.collision_effect, layer=HASH_GROUND))
'''

class House(Prop):
    num = 0
    collision_effect = {'effect_type': 'stun', 'duration': 0.5}
    _images = pyglet.image.ImageGrid(
            pyglet.resource.image('img/sprites/pict_houses.png'),
            1, 3)

    def __init__(self):
        super(House, self).__init__()
        self.set_sprite(pyglet.sprite.Sprite(self._images[House.num % 3]))
        self.add_collider(collider.Collider(
                left=0, right=20, bottom=20, top=180,
                effect={'effect_type': 'stun', 'duration': 0.5},
                layer=HASH_GROUND))
        self.add_collider(collider.Collider(
                left=20, right=180, bottom=0, top=20,
                effect={'effect_type': 'stop', 'directions': 'n'},
                layer=HASH_GROUND))
        House.num += 1


BUILDER_NAMES = {
    'PROP_HOUSE': House,
    'PROP_ROCK': Rock,
    'PROP_STONE': DummyStone
}
