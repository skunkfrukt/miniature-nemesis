import pyglet

TITLE = "O Accursed Editor of Levels, to What Dost Thou Not Compel Human Hats"

class EditorWindow(pyglet.window.Window):
    def __init__(self):
        super(EditorWindow, self).__init__(800, 600, resizable=True,
            caption=TITLE)

    def on_draw(self):
        """ Draw as much of the stage as the current window size allows,
            then the GUI.
        """
        pass

win = EditorWindow()
pyglet.app.run()