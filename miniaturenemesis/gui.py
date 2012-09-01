import pyglet
from .constants import *
from pyglet.window import key

guy = pyglet.sprite.Sprite(pyglet.resource.image('png/testguy.png'))
guy.dx = 0.0
guy.dy = 0.0


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