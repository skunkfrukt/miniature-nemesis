import gameobject

class Prop(gameobject.GameObject):
    collision_effect = None

    def __init__(self, position, size, **kwargs):
        super(Prop, self).__init__(position, size, **kwargs)

    def show(self):
        self.sprite.image = self.image  ##TODO## Should this be elsewhere?
        super(Prop, self).show()
