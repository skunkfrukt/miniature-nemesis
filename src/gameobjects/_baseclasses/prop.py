from gameobject import GameObject

class Prop(GameObject):
    collision_effect = None
    preferred_rendering_group_index = 1  # R_GROUP_PROPS

    def __init__(self):
        super(Prop, self).__init__()
        self.collider = None

    def setup_sprite(self, batch, group):
        if self.sprite is not None:
            if batch is not None:
                self.sprite.batch = batch
            if group is not None:
                self.sprite.group = group
