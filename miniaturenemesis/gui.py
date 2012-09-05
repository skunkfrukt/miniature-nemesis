import math
import pyglet
from .constants import *
from pyglet.window import key

keys = key.KeyStateHandler()

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
        self.switch_to = None
        self.title_bg = pyglet.resource.image('png/title.png')
        self.menu = GameMenu(['Run','Quit'])
        self.menu.labels = []
        for o in self.menu.options:
            l = pyglet.text.Label(o, font_size=16, color=(0,0,0,255), anchor_x = 'center', x = 320)
            l.y = 60 - len(self.menu.labels) * 20
            self.menu.labels.append(l)
        self.select_menu_item(self.menu.selected_option())
    def draw(self):
        self.title_bg.blit(0,0)
        for l in self.menu.labels:
            l.draw()
        
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
        self.switch_to = None
        self.level = Level('Derpington Abbey')
    def draw(self):
        off = int(self.level.offset) % 32
        for x in range(-off,639,32):
            self.level.bg.blit(x, 0)
        guy.draw()
        peck.draw()
    def on_key_press(self, symbol, modifiers):
        guy.fixSpeed()
            
    def on_key_release(self, symbol, modifiers):
        guy.fixSpeed()
            
    def update(self, dt):
        guy.x += guy.dx * dt
        guy.y += guy.dy * dt
        peck.angle += peck.speed * dt
        peck.x += 100.0 * math.cos(peck.angle) * dt
        peck.y += 100.0 * math.sin(peck.angle) * dt
        self.level.offset += 100 * dt


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
        self.speed = 60.0
    
    def play(self, anim_name):
        if anim_name in self.anims:
            self.image = self.anims[anim_name]
            
    def fixSpeed(self):
        self.dx = 0.0
        self.dy = 0.0
        if keys[key.W]:
            self.dy += self.speed
        if keys[key.S]:
            self.dy -= self.speed
        if keys[key.A]:
            self.dx -= self.speed
        if keys[key.D]:
            self.dx += self.speed
        if self.dx and self.dy:
            self.dx /= 1.4
            self.dy /= 1.4
        if self.dx > 0:
            self.play('sprint')
        elif self.dx < 0:
            self.play('stop')
        else:
            self.play('run')


class Woodpecker(pyglet.sprite.Sprite):
    def __init__(self):
        fis = pyglet.image.Animation.from_image_sequence
        wpeck_png = pyglet.resource.image('png/woodpecker__spritesheet00.png') # sprite sheet
        wpeck_grid = pyglet.image.ImageGrid(wpeck_png, 1, 2) # 1 row, 2 cols
        self.anims = {
            'fly': fis(wpeck_grid, 0.1, True)
        }
        super(Woodpecker, self).__init__(self.anims['fly'])
        self.dx = 0.0
        self.dy = 0.0
        self.speed = 1.0
        self.angle = math.pi / 2.0


class Level:
    def __init__(self, id):
        self.id = id
        self.offset = 0
        self.bg = pyglet.resource.image('png/testbg.png')

guy = Hero()
peck = Woodpecker()

class MainWindow(pyglet.window.Window):
    def __init__(self):
        super(MainWindow, self).__init__(WIN_WIDTH, WIN_HEIGHT, WIN_TITLE)
        guy.x = self.width//2
        guy.y = self.height//2
        peck.x = guy.x + 75 - peck.image.get_max_width()//2
        peck.y = guy.y + peck.image.get_max_height()//2
        self.state = MenuState()
        self.push_handlers(keys)
        pyglet.clock.schedule_interval(self.update,0.05)
        
    def on_key_press(self, symbol, modifiers):
        self.state.on_key_press(symbol, modifiers)
            
    def on_key_release(self, symbol, modifiers):
        self.state.on_key_release(symbol, modifiers)
    
    def on_draw(self):
        self.clear()
        if not self.state.switch_to:
            self.state.draw()
        else:
            if self.state.switch_to == 'QUIT':
                self.close()
            else:
                self.state = self.state.switch_to
                print(self.state)
        
    def update(self,dt):
        self.state.update(dt)