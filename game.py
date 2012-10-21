import argparse
from src.constants import GAME_VERSION

parser = argparse.ArgumentParser(description="A danmaku runner.")
parser.add_argument('-v', '--version', action='version', version=GAME_VERSION)
parser.add_argument('-fs', '--fullscreen', action='store_true',
        dest='fullscreen', help='launch the game in fullscreen mode')
parser.add_argument('-ed', '--level-editor', action='store_true',
        dest='editor', help='activate level editor functions')
args = parser.parse_args()

import pyglet
from src import gui

# Main window?
gui.MainWindow(fullscreen=args.fullscreen)

pyglet.app.run()
