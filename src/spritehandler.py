import pyglet

import logging
log = logging.getLogger(__name__)

BG, FG, UI = 0, 1, 2

_placeholder_sprite_image = pyglet.image.Texture.create(1,1)

_batch = pyglet.graphics.Batch()
_sprite_layers = {}

class Layer(pyglet.graphics.OrderedGroup):
    def __init__(self, order, parent=None):
        super(Layer, self).__init__(order, parent)
        self._all_sprites = set()
        self._unused_sprites = set()

    def get_sprite(self):
        try:
            sprite = self._unused_sprites.pop()
            log.debug('Reused old sprite.')
        except KeyError:
            sprite = self.make_sprite()
            log.debug('Made new sprite.')
        return sprite

    def make_sprite(self):
        new_sprite = pyglet.sprite.Sprite(_placeholder_sprite_image,
            batch=_batch, group=self)
        new_sprite.visible = False
        self._all_sprites.add(new_sprite)
        return new_sprite

    def recycle(self, sprite):
        assert sprite in self._all_sprites
        sprite.visible = False
        self._unused_sprites.add(sprite)


def get_sprite(*layer_index):
    layer = get_layer(*layer_index)
    sprite = layer.get_sprite()
    return sprite

def show_sprite(*layer_index):
    sprite = get_sprite(*layer_index)
    sprite.visible = True
    return sprite

def get_layer(*layer_index):
    if not layer_index:
        return None
    if layer_index not in _sprite_layers:
        make_layer(*layer_index)
    return _sprite_layers[layer_index]

def make_layer(*layer_index):
    parent = layer_index[:-1]
    child = layer_index[-1]
    new_layer = Layer(child, parent=get_layer(*parent))
    _sprite_layers[layer_index] = new_layer
    log.debug(D_MAKE_LAYER.format(child, parent))
    return new_layer

def recycle(sprite):
    sprite.group.recycle(sprite)


E_INVALID_LAYER_INDEX = "No layer with index {}."
D_MAKE_LAYER = "New layer {} with parent {}."

make_layer(BG)
make_layer(FG)
make_layer(UI)
