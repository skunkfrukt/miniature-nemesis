import pyglet

TITLE = "O Accursed Editor of Levels, to What Dost Thou Not Compel Human Hats"

images = {}

houses = pyglet.image.ImageGrid(pyglet.resource.image('img/sprites/house.png'),
    1, 3)
images['HouseA'] = houses[0]
images['HouseB'] = houses[1]
images['HouseC'] = houses[2]

class EditorWindow(pyglet.window.Window):
    def __init__(self):
        super(EditorWindow, self).__init__(800, 600, resizable=True,
            caption=TITLE)
        self.camera = Camera()
        self.objects = []
        self.dragging = None

    def on_draw(self):
        """ Draw as much of the stage as the current window size allows,
            then the GUI.
        """
        self.clear()
        for obj in self.objects:
            obj.x = obj.stage_x + self.camera.stage_x * obj.scroll_factor_x
            obj.y = obj.stage_y + self.camera.stage_y * obj.scroll_factor_y
            obj.draw()

    def add_object(self, obj):
        self.objects.append(obj)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.RIGHT:
            self.dragging = self.camera
        elif button == pyglet.window.mouse.LEFT:
            for obj in self.objects:
                if x >= obj.x and x < obj.x + obj.width and y >= obj.y and y < obj.y + obj.height:
                    self.dragging = obj
                    self.dragging.color = (255, 255, 0)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragging is not None:
            self.dragging.stage_x += dx
            self.dragging.stage_y += dy

    def on_mouse_release(self, x, y, button, modifiers):
        if self.dragging is not None:
            self.dragging.color = (255, 255, 255)
            self.dragging = None


class Camera(object):
    def __init__(self):
        self.x = 0
        self.y = 0

    @property
    def color(self):
        return None

    @color.setter
    def color(self, c):
        pass

    @property
    def stage_x(self):
        return self.x

    @stage_x.setter
    def stage_x(self, x):
        self.x = min(0, x) ## Todo also clip to max x.

    @property
    def stage_y(self):
        return self.y

    @stage_y.setter
    def stage_y(self, y):
        self.y = 0


class EditorObject(pyglet.sprite.Sprite):
    def __init__(self, object_type, x, y):
        self.object_type = object_type
        super(EditorObject, self).__init__(images[object_type], x, y)
        self.stage_x = self.x
        self.stage_y = self.y
        self.scroll_factor_x = 1
        self.scroll_factor_y = 1


win = EditorWindow()
win.add_object(EditorObject('HouseC', 100, 100))
win.add_object(EditorObject('HouseA', 200, 200))
win.add_object(EditorObject('HouseC', 300, 300))
b = EditorObject('HouseB', 300, -100)
b.scale = 2
b.scroll_factor_x = 1.4
win.add_object(b)
pyglet.app.run()