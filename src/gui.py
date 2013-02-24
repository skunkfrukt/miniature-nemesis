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

    def setup(self):
        pass

    def teardown(self):
        pass

    def update(self, dt):
        pass

    def switch_state(self, state):
        self.dispatch_event('on_switch_state', state)

GameState.register_event_type('on_switch_state')
GameState.register_event_type('on_quit_game')


class MenuState(GameState):
    def __init__(self):
        super(MenuState, self).__init__()
        self.menu = menu.GameMenu()
        # If no levels have been beaten, add simple Run button.
        plr = pyglet.image.ImageGrid(
            pyglet.resource.image('img/sprites/hero.png'), 1, 14)
        self.menu.add_element(menu.MenuButton('RUN',
            *plr[2:5], x=396+(640-396-50)/2, y=100, layer=2))
        # Else, add smaller Run button with level icons.
        self.menu.add_element(menu.MenuButton('QUIT',
            *plr[8:11], x=396+(640-396-50)/2, y=50, layer=2))
        bg_img = pyglet.resource.image('img/gui/title_bg.png')
        logo_img = pyglet.resource.image('img/gui/pict_logo_gold.png')
        self.bg = menu.MenuObject(bg_img, 0, 0)
        self.logo = menu.MenuObject(logo_img, 0, 0, layer=1)

    def setup(self):
        self.bg.allocate_sprite()
        self.logo.allocate_sprite()
        self.bg.show()
        self.logo.show()
        self.menu.setup()

    def teardown(self):
        self.bg.recycle()
        self.logo.recycle()
        self.menu.teardown()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            if self.menu.get_selection() == 'RUN':
                self.switch_state(PlayState())
            elif self.menu.get_selection() == 'QUIT':
                self.quit()
        elif symbol == key.UP:
            self.menu.previous_option()
        elif symbol == key.DOWN:
            self.menu.next_option()

    def on_key_release(self, symbol, modifiers):
        pass

    def update(self, dt):
        pass

    '''def unselect_menu_item(self, index):
        self.menu.labels[index].color = (0,0,0,255)

    def select_menu_item(self, index):
        self.menu.labels[index].color = (255,0,0,255)'''

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
    icon = pyglet.resource.image('img/icons/128x128.png')

    def __init__(self, fullscreen=False):
        super(MainWindow, self).__init__(WIN_WIDTH + world.ZERO*2, WIN_HEIGHT,
                WIN_TITLE, fullscreen=fullscreen)
        self.state = None
        menustate = MenuState()
        self.set_state(menustate)
        self.push_handlers(keys)
        try:
            self.set_icon(self.icon)
        except AttributeError:
            pass  # If the icon refuses to work, that's no big deal for now.
        pyglet.clock.schedule(self.update)

    def set_state(self, new_state):
        for layer in spritehandler._sprite_layers:
            log.info('Layer {}: {}'.format(layer,
                len(spritehandler._sprite_layers[layer]._all_sprites)))
        if self.state is not None:
            self.state.teardown()
            self.state.pop_handlers()
        self.state = new_state
        if self.state is not None:
            self.state.setup()
            self.state.push_handlers(self)

    def on_key_press(self, symbol, modifiers):
        self.state.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.state.on_key_release(symbol, modifiers)

    def on_draw(self):
        if self.state is not None:
            spritehandler._batch.draw()

    def on_switch_state(self, new_state):
        self.set_state(new_state)

    def on_close(self):
        self.on_quit_game()

    def on_quit_game(self):
        self.set_state(None)
        pyglet.app.exit()

    def update(self,dt):
        self.state.update(dt)
