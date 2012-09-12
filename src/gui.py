import math
import pyglet
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
        self.switch_to = 'QUIT'
        
    def switch_state(self, state):
        self.switch_to = state


class PlayState(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.bg_group = pyglet.graphics.OrderedGroup(0)
        self.bg_prop_group = pyglet.graphics.OrderedGroup(1)
        self.actor_group = pyglet.graphics.OrderedGroup(2)
        # self.projectile_group = pyglet.graphics.OrderedGroup(3)
        self.actor_group = pyglet.graphics.OrderedGroup(4)
        # self.fg_prop_group = pyglet.graphics.OrderedGroup(5)
        # self.gui_group = pyglet.graphics.OrderedGroup(6)
        self.switch_to = None
        self.level = stage.Stage('Derpington Abbey', (95,127,63,255))
        self.bg = pyglet.sprite.Sprite(self.level.background, batch=self.batch,
                group=self.bg_group)
        guy.batch = self.batch
        self.stuff = []
        self.new_stone = True
        self.props = stage.village_stage['props']
        self.graveyard = {stage.Rock: []}
        for i in range(10):
            r = stage.Rock()
            self.graveyard[stage.Rock].append(r)
            r.batch = self.batch
            r.group = self.bg_prop_group
        
    def on_key_press(self, symbol, modifiers):
        guy.fixSpeed(keys)
            
    def on_key_release(self, symbol, modifiers):
        guy.fixSpeed(keys)
            
    def update(self, dt):
        bg_movement = 100 * dt
        guy.x += guy.dx * dt
        guy.y += guy.dy * dt
        self.level.offset += bg_movement
        while len(self.props) and self.props[0][1] <= self.level.offset + 700:
            prop = self.props.pop(0)
            cls, prop_x, prop_y = prop
            if len(self.graveyard[cls]) > 0:
                new_prop = self.graveyard[cls].pop(0)
            else:
                new_prop = cls()
                new_prop.batch = self.batch
                new_prop.group = self.bg_prop_group
            new_prop.stage_x = prop_x
            new_prop.y = prop_y
            new_prop.visible = True
            self.stuff.append(new_prop)
        for thing in self.stuff:
            thing.x = thing.stage_x - self.level.offset
            if thing.stage_x < self.level.offset - thing.width:
                thing.visible = False
                self.stuff.remove(thing)
                self.graveyard[thing.__class__].append(thing)
        else:
        

guy = actor.Hero()

class MainWindow(pyglet.window.Window):
    def __init__(self):
        super(MainWindow, self).__init__(WIN_WIDTH, WIN_HEIGHT, WIN_TITLE)
        guy.x = 0
        guy.y = 0
        self.state = MenuState()
        self.push_handlers(keys)
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
            if self.state.switch_to == 'QUIT':
                self.close()
            else:
                self.state = self.state.switch_to
        
    def update(self,dt):
        self.state.update(dt)