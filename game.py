GAME_VERSION = "0.0.2"

import argparse

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()
# log.setLevel(logging.DEBUG)


parser = argparse.ArgumentParser(description="A danmaku runner.")
parser.add_argument('-v', '--version', action='version', version=GAME_VERSION)
parser.add_argument('-fs', '--fullscreen', action='store_true',
        dest='fullscreen', help='launch the game in fullscreen mode')
parser.add_argument('-ed', '--level-editor', action='store_true',
        dest='editor', help='activate level editor functions')
args = parser.parse_args()

import pyglet
from src import gui, worldbuilder

log.info('Loading game data.')

game_world = worldbuilder.json_to_world('data/world.json')

log.info('Launching game.')

gui.MainWindow(fullscreen=args.fullscreen)

pyglet.app.run()

log.info('Exiting game.')
