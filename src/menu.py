import pyglet

import spritehandler
SH = spritehandler


STATE_PASSIVE = 0
STATE_HOVER = 1
STATE_ACTIVE = 2


class GameMenu:
    def __init__(self, initial_option=0, wrap=True):
        self.elements = []
        self.initial = initial_option
        self.selected_index = initial_option
        self.wrap_around = wrap

    def setup(self):
        for el in self.elements:
            el.allocate_sprite()
            el.show()
        self.set_selected_index(self.initial)

    def teardown(self):
        for el in self.elements:
            el.recycle()

    def next_option(self):
        self.change_selected_index(1)

    def previous_option(self):
        self.change_selected_index(-1)

    def set_selected_index(self, index):
        old_element = self.selected_element
        self.selected_index = index
        new_element = self.selected_element
        if old_element is not None:
            old_element.set_state(STATE_PASSIVE)
        if new_element is not None:
            new_element.set_state(STATE_HOVER)

    def change_selected_index(self, di):
        new_selected_index = self.selected_index + di
        if self.wrap_around or new_selected_index in range(len(self.elements)):
            while new_selected_index < 0:
                new_selected_index += len(self.elements)
            self.set_selected_index(new_selected_index % len(self.elements))
        else:
            pass # Throw some kind of an error or do nothing, maybe.

    def add_element(self, element):
        self.elements.append(element)

    @property
    def selected_element(self):
        return self.elements[self.selected_index]

    def get_selection(self):
        return self.selected_element.name


class MenuObject(object):
    def __init__(self, image, x=0, y=0, layer=0):
        self._image = image
        self.x = x
        self.y = y
        self.sprite = None
        self.layer = layer

    def recycle(self):
        spritehandler.recycle(self.sprite)
        self.sprite = None

    def allocate_sprite(self):
        assert self.sprite is None
        self.sprite = SH.get_sprite(SH.UI, self.layer)
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.image = self.image

    def show(self):
        self.sprite.visible = True

    def hide(self):
        self.sprite.visible = False

    @property
    def image(self):
        return self._image


class MenuButton(MenuObject):
    def __init__(self, name, default_img, hover_img=None, active_img=None,
        x=0, y=0, layer=0):
        super(MenuButton, self).__init__(default_img, x, y)
        self.state = STATE_PASSIVE
        self.state_images = [default_img, hover_img, active_img]
        self.name = name

    @property
    def image(self):
        if self.state_images[self.state] is not None:
            return self.state_images[self.state]
        else:
            return self.state_images[STATE_PASSIVE]

    def set_state(self, state):
        self.state = state
        self.sprite.image = self.image

    def set_image(self, state, image):
        self.state_images[state] = image
