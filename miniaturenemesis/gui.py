import pyglet
from .constants import *
from pyglet.window import key

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
    def draw(self):
        pass
    def update(self, dt):
        pass

class MenuState(GameState):
    def __init__(self):
        self.title_bg = pyglet.resource.image('png/title.png')
    def draw(self):
        self.title_bg.blit(0,0)
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            pass # TODO: Carry out current menu command.
    def update(self, dt):
    	pass

class PlayState(GameState):
    def draw(self):
        guy.draw()
    def on_key_press(self, symbol, modifiers):
        if symbol == key.W:
            guy.dy = 75.0
        elif symbol == key.A:
            guy.dx = -50.0
        elif symbol == key.S:
            guy.dy = -75.0
        elif symbol == key.D:
            guy.dx = 75.0

        if guy.dx < 0:
            guy.play('stop')
        elif guy.dx > 0:
            guy.play('sprint')
        else:
            guy.play('run')
            
    def on_key_release(self, symbol, modifiers):
        if symbol == key.W:
            guy.dy = 0.0
        elif symbol == key.A:
            guy.dx = 0.0
        elif symbol == key.S:
            guy.dy = 0.0
        elif symbol == key.D:
            guy.dx = 0.0
            
    def update(self, dt):
        guy.x += guy.dx * dt
        guy.y += guy.dy * dt

    
class Hero(pyglet.sprite.Sprite):
    def __init__(self):
        fis = pyglet.image.Animation.from_image_sequence
        guy_png = pyglet.resource.image('png/hero__spriteset00.png') # sprite sheet
        guy_grid = pyglet.image.ImageGrid(guy_png, 1, 6) # 1 row, 6 cols
        self.anims = {
            'run': fis(guy_grid[:2], 0.12, True),
            'sprint': fis(guy_grid[2:4], 0.12, True),
            'stop': fis(guy_grid[4:6], 0.12, True)
        }
        super(Hero, self).__init__(self.anims['run'])
        self.dx = 0.0
        self.dy = 0.0
    
    def play(self, anim_name):
        if anim_name in self.anims:
            self.image = self.anims[anim_name]


guy = Hero()

class MainWindow(pyglet.window.Window):
    def __init__(self):
        super(MainWindow, self).__init__(WIN_WIDTH, WIN_HEIGHT, WIN_TITLE)
        guy.x = self.width//2
        guy.y = self.height//2
        self.state = MenuState()
        pyglet.clock.schedule_interval(self.update,0.05)
        
    def on_key_press(self, symbol, modifiers):
        self.state.on_key_press(symbol, modifiers)
            
    def on_key_release(self, symbol, modifiers):
        self.state.on_key_release(symbol, modifiers)
    
    def on_draw(self):
        self.clear()
        self.state.draw()
        
    def update(self,dt):
        self.state.update(dt)