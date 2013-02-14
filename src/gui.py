import math
import pyglet
import sys
from constants import *
from pyglet.window import key

import logging
log = logging.getLogger(__name__)


keys = key.KeyStateHandler()
import actor
import stagebuilder

import world
import spritehandler
SH = spritehandler
import menu

class GameState(pyglet.event.EventDispatcher):
    def __init__(self):
        self.batch = pyglet.graphics.Batch()

    def update(self, dt):
        pass

    def switch_state(self, state):
        self.dispatch_event('on_switch_state', state)

GameState.register_event_type('on_switch_state')
GameState.register_event_type('on_quit_game')


class MenuState(GameState):
    def __init__(self):
        super(MenuState, self).__init__()
        bg_img = pyglet.resource.image('img/gui/title_bg.png')
        logo_img = pyglet.resource.image('img/gui/pict_logo_gold.png')
        self.title_bg = SH.show_sprite(SH.BG, 0)
        self.title_bg.image = bg_img
        self.logo = SH.show_sprite(SH.BG, 1)
        self.logo.image = logo_img
        self.menu = menu.GameMenu(['Run','Quit'])
        self.menu.labels = []
        menu_item_center = (self.logo.width + WIN_WIDTH) // 2
        for o in self.menu.options:
            ly = 60 - len(self.menu.labels) * 20
            l = pyglet.text.Label(o, font_name='Uncial Antiqua',
                font_size=16, color=(0, 0, 0, 255),
                anchor_x='center', batch=spritehandler._batch,
                x=menu_item_center, y=ly,
                group=spritehandler.get_layer(spritehandler.UI, 1))
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
        stg = world.stages['Proto Village']
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
        self.level.send_keys_to_hero(keys, pressed=symbol)

    def on_key_release(self, symbol, modifiers):
        self.level.send_keys_to_hero(keys, released=symbol)

    def update(self, dt):
        if not self.paused:
            self.level.update(dt)
        else:
            self.level.update(0)

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
                font_name='Uncial Antiqua', font_size=80,
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
                font_name='Uncial Antiqua', font_size=80,
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
        pyglet.clock.schedule(self.update)

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
        # self.state.draw()
        spritehandler._batch.draw()

    def on_switch_state(self, new_state):
        self.set_state(new_state)

    def on_close(self):
        self.on_quit_game()

    def on_quit_game(self):
        pyglet.app.exit()

    def update(self,dt):
        self.state.update(dt)
