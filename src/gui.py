import math
import pyglet
import sys
from .constants import *
from pyglet.window import key


keys = key.KeyStateHandler()
import actor
import stage


class GameMenu:
    def __init__(self,options, initial_option = 0, wrap = True):
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

class GameState:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()

    def draw(self):
        self.batch.draw()

    def update(self, dt):
        pass


class MenuState(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.switch_to = None
        if '--skipmenu' in sys.argv:
            self.switch_state(PlayState())
        self.bg_group = pyglet.graphics.OrderedGroup(0)
        self.button_group = pyglet.graphics.OrderedGroup(1)
        self.title_bg = pyglet.sprite.Sprite(pyglet.resource.image(
                'img/gui/title.png'), batch=self.batch, group=self.bg_group)
        self.menu = GameMenu(['Run','Quit'])
        self.menu.labels = []
        for o in self.menu.options:
            ly = 60 - len(self.menu.labels) * 20
            l = pyglet.text.Label(o, font_size=16, color=(0, 0, 0, 255),
                    anchor_x='center', batch=self.batch, x=320, y=ly,
                    group=self.button_group)
            self.menu.labels.append(l)
        self.select_menu_item(self.menu.selected_option())

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            if self.menu.selected_option_name() == 'Run':
                self.switch_state(PlayState())
            elif self.menu.selected_option_name() == 'Quit':
                self.quit()
        elif symbol == key.UP:
            self.unselect_menu_item(self.menu.selected_option())
            self.menu.previous_option()
            self.select_menu_item(self.menu.selected_option())
        elif symbol == key.DOWN:
            self.unselect_menu_item(self.menu.selected_option())
            self.menu.next_option()
            self.select_menu_item(self.menu.selected_option())

    def on_key_release(self, symbol, modifiers):
        pass

    def update(self, dt):
        pass

    def unselect_menu_item(self, index):
        self.menu.labels[index].color = (0,0,0,255)

    def select_menu_item(self, index):
        self.menu.labels[index].color = (255,0,0,255)

    def quit(self):
        pyglet.app.exit()
        #self.switch_to = 'QUIT'

    def switch_state(self, state):
        self.switch_to = state


class PlayState(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.gui_group = pyglet.graphics.OrderedGroup(1)
        self.switch_to = None
        self.level = stage.Stage('Derpington Abbey', (0,127,0,255),
                stage.village_props)
        self.game_over_label = None
        self.paused = False

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.switch_to = MenuState()  # pyglet.app.exit()
        elif symbol == key.O:
            print("%s active game objects." % len(self.level.active_objects))
        elif symbol == key.P:
            self.paused = not self.paused
        self.level.send_keys_to_hero(keys, pressed=symbol)

    def on_key_release(self, symbol, modifiers):
        self.level.send_keys_to_hero(keys, released=symbol)

    def update(self, dt):
        if not self.paused:
            self.level.update(dt)
        else:
            self.level.update(0)

    def draw(self):
        if self.level.ready:
            self.level.batch.draw()
        self.batch.draw()


fps_display = pyglet.clock.ClockDisplay()

class MainWindow(pyglet.window.Window):
    icons = (pyglet.resource.image('img/icons/16x16.png'),
            pyglet.resource.image('img/icons/24x24.png'),
            pyglet.resource.image('img/icons/32x32.png'),
            pyglet.resource.image('img/icons/48x48.png'),
            pyglet.resource.image('img/icons/72x72.png'),
            pyglet.resource.image('img/icons/128x128.png'))

    def __init__(self):
        fs = '-fs' in sys.argv
        super(MainWindow, self).__init__(WIN_WIDTH, WIN_HEIGHT, WIN_TITLE, fullscreen=fs)
        self.state = MenuState()
        self.push_handlers(keys)
        try:
			self.set_icon(*self.icons)
        except AttributeError:
			pass  # If the icon refuses to work, that's no big deal for now.
        pyglet.clock.schedule_interval(self.update,0.02)

    def on_key_press(self, symbol, modifiers):
        self.state.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.state.on_key_release(symbol, modifiers)

    def on_draw(self):
        self.clear()
        if self.state.switch_to is None:
            self.state.draw()
        else:
            self.state = self.state.switch_to
        # fps_display.draw()

    def update(self,dt):
        self.state.update(dt)
