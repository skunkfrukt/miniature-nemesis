from gameobject import GameObject
from vector import *

LAYER_BULLET = 3
SIZE_BULLET = Vector(1, 1)

class Projectile(GameObject):
    def __init__(self, position, size=SIZE_BULLET, speed=VECTOR_NULL,
        offset=VECTOR_NULL):
        super(Projectile, self).__init__(
            position, size, layer=LAYER_BULLET, offset=offset)
        self.speed = speed
