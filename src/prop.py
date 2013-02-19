import gameobject

class Prop(gameobject.GameObject):
    collision_effect = None

    def __init__(self, x, y, **kwargs):
        super(Prop, self).__init__(x, y, **kwargs)
        # self.collider = None

    def show(self):
        self.sprite.image = self.image
        super(Prop, self).show()

    '''def setup_sprite(self, batch, group):
        if self.sprite is not None:
            if batch is not None:
                self.sprite.batch = batch
            if group is not None:
                self.sprite.group = group'''
