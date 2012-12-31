import math
import pyglet
import sys
from constants import *
from pyglet.window import key

import logging
log = logging.getLogger(__name__)


keys = key.KeyStateHandler()
import gameobjects._baseclasses.actor
import stagebuilder

import world

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

class GameState(pyglet.event.EventDispatcher):
    def __init__(self):
        self.batch = pyglet.graphics.Batch()

    def draw(self):
        self.batch.draw()

    def update(self, dt):
        pass

    def switch_state(self, state):
        self.dispatch_event('on_switch_state', state)

GameState.register_event_type('on_switch_state')
GameState.register_event_type('on_quit_game')


class MenuState(GameState):
    _logo = pyglet.resource.image('img/gui/pict_logo_gold.png')

    def __init__(self):
        super(MenuState, self).__init__()
        if '--skipmenu' in sys.argv:
            self.switch_state(PlayState())
        self.bg_group = pyglet.graphics.OrderedGroup(0)
        self.button_group = pyglet.graphics.OrderedGroup(1)
        self.title_bg = pyglet.sprite.Sprite(pyglet.resource.image(
                'img/gui/title_bg.png'), batch=self.batch, group=self.bg_group)
        self.logo = pyglet.sprite.Sprite(self._logo,
                batch=self.batch, group=self.button_group)
        self.menu = GameMenu(['Run','Quit'])
        self.menu.labels = []
        menu_item_center = (self.logo.width + WIN_WIDTH) // 2
        for o in self.menu.options:
            ly = 60 - len(self.menu.labels) * 20
            l = pyglet.text.Label(o, font_size=16, color=(0, 0, 0, 255),
                    anchor_x='center', batch=self.batch,
                    x=menu_item_center, y=ly,
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
        self.dispatch_event('on_quit_game')


class PlayState(GameState):
    def __init__(self):
        super(PlayState, self).__init__()
        self.gui_group = pyglet.graphics.OrderedGroup(1)
        stg = world.stages['ProtoVillage']
        stg.setup()
        self.level = stg
        self.level.push_handlers(self)
        self.game_over_label = None
        self.paused = False

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.switch_state(MenuState())
        elif symbol == key.O:
            print("%s active game objects." % len(self.level.active_objects))
        elif symbol == key.P:
            self.paused = not self.paused
        elif symbol == key.C:
            pass
        # self.level.send_keys_to_hero(keys, pressed=symbol)

    def on_key_release(self, symbol, modifiers):
        pass  # self.level.send_keys_to_hero(keys, released=symbol)

    def update(self, dt):
        if not self.paused:
            self.level.update(dt)
        else:
            self.level.update(0)

    def draw(self):
        self.level.batch.draw()
        # self.batch.draw()

    def on_hero_death(self):
        bm = pyglet.image.get_buffer_manager()
        id = bm.get_color_buffer().get_image_data()
        # id.format = 'L'
        self.switch_state(GameOverState(id))

    def on_stage_end(self, stage_id):
        bm = pyglet.image.get_buffer_manager()
        id = bm.get_color_buffer().get_image_data()
        # id.format = 'L'
        self.switch_state(WinState(id))


class GameOverState(GameState):
    def __init__(self, image):
        super(GameOverState, self).__init__()
        self.bg_group = pyglet.graphics.OrderedGroup(0)
        self.gui_group = pyglet.graphics.OrderedGroup(1)
        self.snapshot = pyglet.sprite.Sprite(image,
                batch=self.batch, group=self.bg_group)
        self.snapshot.color = (127,0,0)
        self.game_over_label = pyglet.text.Label(
                text='Thou diest!', color=(255, 0, 0, 255),
                font_name='Papyrus', font_size=80,
                x=320, y=180, anchor_x='center', anchor_y='center',
                batch=self.batch, group=self.gui_group)

    def on_key_press(self, symbol, modifiers):
        self.switch_state(MenuState())


class WinState(GameState):
    def __init__(self, image):
        super(WinState, self).__init__()
        self.bg_group = pyglet.graphics.OrderedGroup(0)
        self.gui_group = pyglet.graphics.OrderedGroup(1)
        self.snapshot = pyglet.sprite.Sprite(image,
                batch=self.batch, group=self.bg_group)
        self.snapshot.color = (191,127,0)
        self.game_over_label = pyglet.text.Label(
                text='Hurrah!', color=(255, 255, 0, 255),
                font_name='Comic Sans MS', font_size=80,
                x=320, y=180, anchor_x='center', anchor_y='center',
                batch=self.batch, group=self.gui_group)

    def on_key_press(self, symbol, modifiers):
        self.switch_state(MenuState())


fps_display = pyglet.clock.ClockDisplay()

class MainWindow(pyglet.window.Window):
    icons = (pyglet.resource.image('img/icons/16x16.png'),
            pyglet.resource.image('img/icons/24x24.png'),
            pyglet.resource.image('img/icons/32x32.png'),
            pyglet.resource.image('img/icons/48x48.png'),
            pyglet.resource.image('img/icons/72x72.png'),
            pyglet.resource.image('img/icons/128x128.png'))

    def __init__(self, fullscreen=False):
        super(MainWindow, self).__init__(WIN_WIDTH + world.ZERO*2, WIN_HEIGHT,
                WIN_TITLE, fullscreen=fullscreen)
        self.state = None
        self.set_state(MenuState())
        self.push_handlers(keys)
        try:
            self.set_icon(*self.icons)
        except AttributeError:
            pass  # If the icon refuses to work, that's no big deal for now.
        pyglet.clock.schedule(self.update)  # _interval(self.update, 0.02)

    def set_state(self, new_state):
        if self.state is not None:
            self.state.pop_handlers()
        self.state = new_state
        self.state.push_handlers(self)

    def on_key_press(self, symbol, modifiers):
        self.state.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.state.on_key_release(symbol, modifiers)

    def on_draw(self):
        self.state.draw()

    def on_switch_state(self, new_state):
        self.set_state(new_state)

    def on_quit_game(self):
        pyglet.app.exit()

    def update(self,dt):
        self.state.update(dt)
