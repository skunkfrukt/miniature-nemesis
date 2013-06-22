from src.cutscene import *
import pyglet


win = pyglet.window.Window(640, 360)
win.clear()


class TestCutscene(Cutscene):
    def setup(self):
        self.add_image('village', 'img/cinematics/ews_village.png', layer=0)
        self.add_image('cloudy', 'img/cinematics/ews_cloud01.png', layer=1)
        self.add_image('cloudier', 'img/cinematics/ews_cloud00.png', layer=2)
        self.add_image('cloudiest', 'img/cinematics/temp_cloud.png', layer=1)
        self.add_image('cloudiester', 'img/cinematics/temp_cloud.png', layer=1)
        self.add_image('cloudiestest', 'img/cinematics/temp_cloud.png', layer=1)
        self.add_image('cloudiestestest', 'img/cinematics/temp_cloud.png', layer=1)
        self.do(self.show, 0, 'village')
        self.do(self.tint, 0, 'village', 0, 0, 0, 0, algorithm=LINEAR)
        self.do(self.tint, 0.1, 'village', 255, 255, 255, 2.9, algorithm=LINEAR)
        self.do(self.show, 3.5, 'cloudiest', 640, 260)
        self.do(self.move, 3.5, 'cloudiest', -1000, 0, 30)
        self.do(self.show, 5.5, 'cloudiester', 640, 300)
        self.do(self.move, 5.5, 'cloudiester', -1000, 0, 30)
        self.do(self.show, 10.5, 'cloudiestest', 640, 280)
        self.do(self.move, 10.5, 'cloudiestest', -1000, 0, 30)
        self.do(self.show, 12.5, 'cloudiestestest', 640, 150)
        self.do(self.move, 12.5, 'cloudiestestest', -1000, 0, 30)


scene = TestCutscene()
pyglet.app.run()