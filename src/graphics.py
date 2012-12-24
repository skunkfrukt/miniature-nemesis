import logging
log = logging.getLogger(__name__)

class AnimSet(object):
    def __init__(self, name):
        self.name = name
        self.animations = {}
        self.default_animation = None

        log.debug('Initialised AnimSet {}.'.format(self.name))

    def get(self, animation_name):
        try:
            return self.animations[animation_name]
        except KeyError:
            log.warning('No Animation {} in AnimSet {}.'.format(
                    animation_name, self.name))
            try:  ##TODO## Remove this.
                return self.animations[self.default_animation]
            except KeyError:
                log.error('AnimSet {} has no default animation.'.format(
                        self.name))

    def get_default(self):
        pass  ##TODO## Add code for default anim.

    def add(self, key, animation):
        if key in self.animations:
            log.warning(
                    'Animation {} already exists in AnimSet {}.'.format(
                    key, self.name))
        self.animations[key] = animation
        if self.default_animation is None:
            self.default_animation = key

        log.debug('Added Animation {} to AnimSet {}.'.format(
                key, self.name))


class AnimSprite(pyglet.sprite.Sprite):
    def __init__(self, anim_set):
        self.anim_set = anim_set
        super(AnimSprite, self).__init__(self.anim_set.get(None)) ##TODO## None

    def play(self,
