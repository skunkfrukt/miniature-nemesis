import pyglet
from .constants import *
from pyglet.window import key

guy = pyglet.sprite.Sprite(pyglet.resource.image('png/testguy.png'))
guy.dx = 0.0
guy.dy = 0.0

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
        pass


class MainWindow(pyglet.window.Window):
    def __init__(self):
        super(MainWindow, self).__init__(WIN_WIDTH, WIN_HEIGHT, WIN_TITLE)
        self.title_bg = pyglet.resource.image('png/title.png')
        self.start_button = pyglet.text.HTMLLabel('<b>Start</b>',
                                                  x = self.width//3,
                                                  y = 20)
        guy.x = self.width//2
        guy.y = self.height//2
        pyglet.clock.schedule_interval(self.update,0.05)
        
    def on_key_press(self, symbol, modifiers):
        global guy
        if symbol == key.W:
            guy.dy = 100.0
        elif symbol == key.A:
            guy.dx = -100.0
        elif symbol == key.S:
            guy.dy = -100.0
        elif symbol == key.D:
            guy.dx = 100.0
            
    def on_key_release(self, symbol, modifiers):
        global guy
        if symbol == key.W:
            guy.dy = 0.0
        elif symbol == key.A:
            guy.dx = 0.0
        elif symbol == key.S:
            guy.dy = 0.0
        elif symbol == key.D:
            guy.dx = 0.0
            
    
    def on_draw(self):
        self.clear()
        self.title_bg.blit(0,0)
        guy.draw()
        self.start_button.draw()
        
        
    def update(self,dt):
        guy.x += guy.dx * dt
        guy.y += guy.dy * dt