import pyglet

import spritehandler


STATE_PASSIVE = 0
STATE_HOVER = 1
STATE_ACTIVE = 2


class GameMenu:
    def __init__(self,options, initial_option = 0, wrap = True):
        self.elements = []
        self.options = options
        self.selected_index = initial_option
        self.wrap_around = wrap

    def next_option(self):
        return self.change_selected_index(1)

    def previous_option(self):
        return self.change_selected_index(-1)

    def change_selected_index(self, di):
        new_selected_index = self.selected_index + di
        if self.wrap_around:
            while new_selected_index < 0:
                new_selected_index += len(self.options)
            self.selected_index = new_selected_index % len(self.options)
        elif new_selected_index in range(len(self_options)):
            self.selected_index = new_selected_index
        else:
            pass # Throw some kind of an error or do nothing, maybe.
        return self.selected_index

    def selected_option(self):
        return self.selected_index

    def selected_option_name(self):
        return self.options[self.selected_option()]


class MenuObject(object):
    def __init__(self, image, x=0, y=0, layer=0):
        self.image = image
        self.x = x
        self.y = y

    def recycle(self):
        spritehandler.recycle(self.sprite)
        self.sprite = None

    def allocate_sprite(self):
        assert self.sprite is None
        self.sprite = SH.get_sprite(SH.BG, self.layer)


class MenuButton(MenuObject):
    def __init__(self, name, default_img, hover_img=None, active_img=None):
        self.state = STATE_PASSIVE
        self.state_images = [default_img, hover_img, active_img]

    def get_image(self):
        if self.state_images[self.state] is not None:
            return self.state_images[self.state]
        else:
            return self.state_images[STATE_PASSIVE]

    def set_state(self, state):
        self.state = state
        self.sprite.image = self.get_image()

    def set_image(self, state, image):
        self.state_images[state] = image

    def allocate_sprite(self):
        assert self.sprite is None
        self.sprite = SH.get_sprite(SH.UI, self.layer)
